"""Text chunking for the baseline local RAG pipeline.

The chunker keeps metadata attached to every chunk so responses can cite their
sources. This is intentionally simple in Phase 01: later phases can improve this
with token-aware chunking, document trust labels, sensitivity labels, and access
control metadata.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.ingestion import Document


@dataclass(frozen=True)
class Chunk:
    """A retrievable piece of a source document."""

    chunk_id: str
    source: str
    text: str


def chunk_text(text: str, max_words: int = 120, overlap_words: int = 20) -> list[str]:
    """Split text into overlapping word chunks.

    Args:
        text: Raw document text.
        max_words: Maximum number of words per chunk.
        overlap_words: Number of words repeated between adjacent chunks.

    Returns:
        A list of chunk strings.

    Raises:
        ValueError: If chunk parameters are invalid.
    """

    if max_words <= 0:
        raise ValueError("max_words must be greater than zero")

    if overlap_words < 0:
        raise ValueError("overlap_words cannot be negative")

    if overlap_words >= max_words:
        raise ValueError("overlap_words must be smaller than max_words")

    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    step = max_words - overlap_words

    for start in range(0, len(words), step):
        end = start + max_words
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))

        if end >= len(words):
            break

    return chunks


def chunk_documents(
    documents: list[Document],
    max_words: int = 120,
    overlap_words: int = 20,
) -> list[Chunk]:
    """Chunk a list of documents and preserve source metadata."""

    chunks: list[Chunk] = []

    for document in documents:
        text_chunks = chunk_text(
            document.text,
            max_words=max_words,
            overlap_words=overlap_words,
        )

        for index, text in enumerate(text_chunks, start=1):
            chunks.append(
                Chunk(
                    chunk_id=f"{document.source}::chunk-{index:03d}",
                    source=document.source,
                    text=text,
                )
            )

    return chunks
