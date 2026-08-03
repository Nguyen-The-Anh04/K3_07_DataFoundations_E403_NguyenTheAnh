from __future__ import annotations

from typing import Any, Callable

from .chunking import _dot
from .embeddings import _mock_embed
from .models import Document


class EmbeddingStore:
    """
    A vector store for text chunks.

    Tries to use ChromaDB if available; falls back to an in-memory store.
    The embedding_fn parameter allows injection of mock embeddings for tests.
    """

    def __init__(
        self,
        collection_name: str = "documents",
        embedding_fn: Callable[[str], list[float]] | None = None,
    ) -> None:
        self._embedding_fn = embedding_fn or _mock_embed
        self._collection_name = collection_name
        self._use_chroma = False
        self._store: list[dict[str, Any]] = []
        self._collection = None
        self._next_index = 0

        try:
            import chromadb

            client = chromadb.EphemeralClient()
            self._collection = client.get_or_create_collection(name=collection_name)
            self._use_chroma = True
        except Exception:
            self._use_chroma = False
            self._collection = None

    def _make_record(self, doc: Document) -> dict[str, Any]:
        return {
            "id": doc.id,
            "content": doc.content,
            "metadata": dict(doc.metadata or {}),
            "embedding": list(self._embedding_fn(doc.content)),
        }

    def _search_records(self, query: str, records: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
        if top_k <= 0:
            return []
        query_embedding = self._embedding_fn(query)
        scored = []
        for record in records:
            score = _dot(query_embedding, record["embedding"])
            result = {key: value for key, value in record.items() if key != "embedding"}
            result["score"] = score
            scored.append(result)
        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored[:top_k]

    def add_documents(self, docs: list[Document]) -> None:
        """
        Embed each document's content and store it.

        For ChromaDB: use collection.add(ids=[...], documents=[...], embeddings=[...])
        For in-memory: append dicts to self._store
        """
        if not docs:
            return
        records = [self._make_record(doc) for doc in docs]
        if self._use_chroma and self._collection is not None:
            try:
                self._collection.add(
                    ids=[record["id"] for record in records],
                    documents=[record["content"] for record in records],
                    embeddings=[record["embedding"] for record in records],
                    metadatas=[record["metadata"] or {"_empty": True} for record in records],
                )
                return
            except Exception:
                # Keep the classroom implementation usable if Chroma rejects
                # a metadata value; the in-memory path is deterministic.
                self._use_chroma = False
                self._collection = None
        self._store.extend(records)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """
        Find the top_k most similar documents to query.

        For in-memory: compute dot product of query embedding vs all stored embeddings.
        """
        if self._use_chroma and self._collection is not None:
            try:
                result = self._collection.query(
                    query_embeddings=[self._embedding_fn(query)],
                    n_results=max(0, top_k),
                    include=["documents", "metadatas", "distances"],
                )
                ids = (result.get("ids") or [[]])[0]
                documents = (result.get("documents") or [[]])[0]
                metadatas = (result.get("metadatas") or [[]])[0]
                distances = (result.get("distances") or [[]])[0]
                return [
                    {
                        "id": ids[index],
                        "content": documents[index],
                        "metadata": {k: v for k, v in (metadatas[index] or {}).items() if k != "_empty"},
                        "score": 1.0 - distances[index],
                    }
                    for index in range(len(ids))
                ]
            except Exception:
                pass
        return self._search_records(query, self._store, top_k)

    def get_collection_size(self) -> int:
        """Return the total number of stored chunks."""
        if self._use_chroma and self._collection is not None:
            try:
                return int(self._collection.count())
            except Exception:
                pass
        return len(self._store)

    def search_with_filter(self, query: str, top_k: int = 3, metadata_filter: dict = None) -> list[dict]:
        """
        Search with optional metadata pre-filtering.

        First filter stored chunks by metadata_filter, then run similarity search.
        """
        if not metadata_filter:
            return self.search(query, top_k=top_k)
        records = [
            record for record in self._store
            if all(record.get("metadata", {}).get(key) == value for key, value in metadata_filter.items())
        ]
        return self._search_records(query, records, top_k)

    def delete_document(self, doc_id: str) -> bool:
        """
        Remove all chunks belonging to a document.

        Returns True if any chunks were removed, False otherwise.
        """
        if self._use_chroma and self._collection is not None:
            try:
                result = self._collection.get(include=["metadatas"])
                ids = [
                    record_id
                    for record_id, metadata in zip(result.get("ids", []), result.get("metadatas", []))
                    if metadata and metadata.get("doc_id") == doc_id
                ]
                if ids:
                    self._collection.delete(ids=ids)
                    return True
                return False
            except Exception:
                pass
        before = len(self._store)
        self._store = [
            record for record in self._store
            if record.get("id") != doc_id
            and record.get("metadata", {}).get("doc_id") != doc_id
        ]
        return len(self._store) < before
