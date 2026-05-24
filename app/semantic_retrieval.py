"""Semantic retrieval for Phase 01.5.

Semantic retrieval runs beside the Phase 01 keyword retriever. It uses an
embedding provider and vector index to rank chunks by vector similarity instead
of exact keyword overlap.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.chunking import Chunk
from app.embeddings import EmbeddingProvider, LocalSemanticEmbeddingProvider
from app.vector_index import InMemoryVectorIndex, VectorRecord


@dataclass(frozen=True)
class SemanticRetrievalResult:
    """A chunk returned by semantic retrieval."""

    chunk: Chunk
    similarity: float
    embedding_model: str


def build_vector_index(
    chunks: list[Chunk],
    embedding_provider: EmbeddingProvider | None = None,
) -> InMemoryVectorIndex:
    """Embed chunks and store them in an in-memory vector index."""

    provider = embedding_provider or LocalSemanticEmbeddingProvider()
    embeddings = provider.embed_batch([chunk.text for chunk in chunks])

    index = InMemoryVectorIndex()
    index.add_many(
        [
            VectorRecord(chunk=chunk, embedding=embedding)
            for chunk, embedding in zip(chunks, embeddings)
        ]
    )

    return index


def semantic_retrieve(
    query: str,
    chunks: list[Chunk],
    top_k: int = 3,
    embedding_provider: EmbeddingProvider | None = None,
    minimum_similarity: float = 0.0,
) -> list[SemanticRetrievalResult]:
    """Retrieve chunks by semantic vector similarity.

    Args:
        query: User question.
        chunks: Available document chunks.
        top_k: Maximum number of results to return.
        embedding_provider: Optional embedding backend.
        minimum_similarity: Drop results below this similarity threshold.

    Returns:
        Ranked semantic retrieval results with similarity scores.
    """

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero")

    provider = embedding_provider or LocalSemanticEmbeddingProvider()
    index = build_vector_index(chunks, provider)
    query_embedding = provider.embed_text(query)

    results = index.search(query_embedding, top_k=top_k)

    return [
        SemanticRetrievalResult(
            chunk=result.chunk,
            similarity=result.similarity,
            embedding_model=provider.model_name,
        )
        for result in results
        if result.similarity >= minimum_similarity
    ]
