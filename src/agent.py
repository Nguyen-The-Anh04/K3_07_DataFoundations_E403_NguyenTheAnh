from typing import Callable

from .store import EmbeddingStore


class KnowledgeBaseAgent:
    def __init__(
        self,
        store: EmbeddingStore,
        llm_fn: Callable[[str], str],
    ) -> None:
        self.store = store
        self.llm_fn = llm_fn

    def answer(
        self,
        question: str,
        top_k: int = 3,
    ) -> str:
        results = self.store.search(question, top_k=top_k)

        context = "\n\n".join(
            f"[Chunk {i}]\n{item['content']}"
            for i, item in enumerate(results, start=1)
        )

        prompt = (
            "You are a knowledge-base assistant. "
            "Answer only from the provided context. "
            "If the context is insufficient, say that the information "
            "is not available.\n\n"
            f"Context:\n{context or '[No relevant context found]'}\n\n"
            f"Question: {question}\n"
            "Answer:"
        )

        return self.llm_fn(prompt)