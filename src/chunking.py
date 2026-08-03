from __future__ import annotations

import math
import re


class FixedSizeChunker:
    """
    Chia văn bản thành các chunk có kích thước cố định.

    Quy tắc:
    - Mỗi chunk dài tối đa chunk_size ký tự.
    - Các chunk liên tiếp có thể chồng lấn overlap ký tự.
    - Chunk cuối chứa phần văn bản còn lại.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")

        if overlap < 0 or overlap >= chunk_size:
            raise ValueError(
                "overlap must satisfy 0 <= overlap < chunk_size"
            )

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[str]:
        """Chia văn bản thành các chunk có kích thước cố định."""
        if not text:
            return []

        if len(text) <= self.chunk_size:
            return [text]

        step = self.chunk_size - self.overlap
        chunks: list[str] = []

        for start in range(0, len(text), step):
            piece = text[
                start:start + self.chunk_size
            ]

            chunks.append(piece)

            if start + self.chunk_size >= len(text):
                break

        return chunks


class SentenceChunker:
    """
    Chia văn bản theo câu.

    Mỗi chunk chứa tối đa max_sentences_per_chunk câu.
    """

    def __init__(
        self,
        max_sentences_per_chunk: int = 3,
    ) -> None:
        self.max_sentences_per_chunk = max(
            1,
            max_sentences_per_chunk,
        )

    def chunk(self, text: str) -> list[str]:
        """Tách văn bản thành câu rồi nhóm các câu thành chunk."""
        text = text.strip()

        if not text:
            return []

        # Tách tại khoảng trắng đứng sau dấu kết thúc câu:
        # dấu chấm, dấu chấm than hoặc dấu hỏi.
        sentences = [
            sentence.strip()
            for sentence in re.split(
                r"(?<=[.!?])\s+",
                text,
            )
            if sentence.strip()
        ]

        chunks: list[str] = []

        for index in range(
            0,
            len(sentences),
            self.max_sentences_per_chunk,
        ):
            sentence_group = sentences[
                index:index + self.max_sentences_per_chunk
            ]

            chunk_text = " ".join(
                sentence_group
            ).strip()

            if chunk_text:
                chunks.append(chunk_text)

        return chunks


class RecursiveChunker:
    """
    Chia văn bản đệ quy theo thứ tự ưu tiên của separator.

    Thứ tự mặc định:
    1. Đoạn văn
    2. Dòng
    3. Câu
    4. Từ
    5. Ký tự
    """

    DEFAULT_SEPARATORS = [
        "\n\n",
        "\n",
        ". ",
        " ",
        "",
    ]

    def __init__(
        self,
        separators: list[str] | None = None,
        chunk_size: int = 500,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")

        if separators is None:
            self.separators = list(
                self.DEFAULT_SEPARATORS
            )
        else:
            self.separators = list(separators)

        self.chunk_size = chunk_size

    def chunk(self, text: str) -> list[str]:
        """Chia văn bản bằng chiến lược đệ quy."""
        if not text:
            return []

        chunks = self._split(
            current_text=text,
            remaining_separators=self.separators,
        )

        return [
            piece
            for piece in chunks
            if piece
        ]

    def _split(
        self,
        current_text: str,
        remaining_separators: list[str],
    ) -> list[str]:
        """Hàm hỗ trợ chia văn bản theo phương pháp đệ quy."""

        # Base case: đoạn hiện tại đã đủ ngắn.
        if len(current_text) <= self.chunk_size:
            stripped_text = current_text.strip()

            if stripped_text:
                return [stripped_text]

            return []

        # Nếu không còn separator, cắt cứng theo chunk_size.
        if not remaining_separators:
            chunks: list[str] = []

            for index in range(
                0,
                len(current_text),
                self.chunk_size,
            ):
                piece = current_text[
                    index:index + self.chunk_size
                ].strip()

                if piece:
                    chunks.append(piece)

            return chunks

        separator = remaining_separators[0]
        next_separators = remaining_separators[1:]

        # Separator rỗng là bước cuối cùng:
        # cắt trực tiếp theo số ký tự.
        if separator == "":
            return self._split(
                current_text=current_text,
                remaining_separators=[],
            )

        # Nếu separator không xuất hiện,
        # chuyển sang separator tiếp theo.
        if separator not in current_text:
            return self._split(
                current_text=current_text,
                remaining_separators=next_separators,
            )

        raw_parts = current_text.split(separator)
        parts: list[str] = []

        # Gắn lại separator để giữ cấu trúc văn bản.
        for index, part in enumerate(raw_parts):
            is_last_part = (
                index == len(raw_parts) - 1
            )

            if not is_last_part:
                part = part + separator

            if part or not is_last_part:
                parts.append(part)

        smaller_parts: list[str] = []

        # Các phần còn quá dài tiếp tục được chia đệ quy.
        for part in parts:
            if len(part) > self.chunk_size:
                smaller_parts.extend(
                    self._split(
                        current_text=part,
                        remaining_separators=next_separators,
                    )
                )
            elif part.strip():
                smaller_parts.append(part)

        # Ghép các phần nhỏ nếu tổng chiều dài
        # chưa vượt quá chunk_size.
        chunks: list[str] = []
        buffer = ""

        for part in smaller_parts:
            if not buffer:
                buffer = part
                continue

            if (
                len(buffer) + len(part)
                <= self.chunk_size
            ):
                buffer += part
            else:
                if buffer.strip():
                    chunks.append(buffer.strip())

                buffer = part

        if buffer.strip():
            chunks.append(buffer.strip())

        return chunks


def _dot(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    """Tính tích vô hướng của hai vector."""
    return sum(
        value_a * value_b
        for value_a, value_b in zip(
            vector_a,
            vector_b,
        )
    )


def compute_similarity(
    vec_a: list[float],
    vec_b: list[float],
) -> float:
    """
    Tính cosine similarity giữa hai vector.

    Công thức:
        dot(a, b) / (norm(a) * norm(b))

    Trả về 0.0 nếu một trong hai vector
    có độ lớn bằng 0.
    """
    norm_a = math.sqrt(
        sum(
            value * value
            for value in vec_a
        )
    )

    norm_b = math.sqrt(
        sum(
            value * value
            for value in vec_b
        )
    )

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    dot_product = _dot(
        vec_a,
        vec_b,
    )

    return dot_product / (
        norm_a * norm_b
    )


class ChunkingStrategyComparator:
    """
    Chạy và so sánh các chiến lược chunking:
    - fixed_size
    - by_sentences
    - recursive
    """

    def compare(
        self,
        text: str,
        chunk_size: int = 200,
    ) -> dict:
        """So sánh kết quả của ba chiến lược chunking."""

        overlap = min(
            20,
            max(
                0,
                chunk_size // 10,
            ),
        )

        strategies = {
            "fixed_size": FixedSizeChunker(
                chunk_size=chunk_size,
                overlap=overlap,
            ),
            "by_sentences": SentenceChunker(
                max_sentences_per_chunk=3,
            ),
            "recursive": RecursiveChunker(
                chunk_size=chunk_size,
            ),
        }

        comparison: dict = {}

        for strategy_name, chunker in strategies.items():
            chunks = chunker.chunk(text)
            count = len(chunks)

            if count > 0:
                average_length = (
                    sum(
                        len(chunk)
                        for chunk in chunks
                    )
                    / count
                )
            else:
                average_length = 0.0

            comparison[strategy_name] = {
                "count": count,
                "avg_length": average_length,
                "chunks": chunks,
            }

        return comparison