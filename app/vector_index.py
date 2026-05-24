"""In-memory vector index for Phase 01.5 semantic retrieval.

This module intentionally keeps vector search simple and inspectable. Production
systems may use FAISS, pgvector, Pinecone, Weaviate, or another vector database;
this lab starts with a local index so retrieval behavior remains visible.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from app.chunking import Chunk


@dataclass(frozen=True)
class VectorRecord:
    """A document chunk and its embedding."""

    chunk: Chunk
    embedding: list[float]


@dataclass(frozen=True)
class VectorSearchResult:
    """A vector search hit with similarity score."""

    chunk: Chunk
    similarity: float


class InMemoryVectorIndex:
    """Small in-memory vector index using cosine similarity."""

    def __init__(self) -> None:
        self.records: list[VectorRecord] = []

    def add(self, chunk: Chunk, embedding: list[float]) -> None:
        """Add a single chunk embedding to the index."""

        if not embedding:
            raise ValueError("embedding cannot be empty")

        self.records.append(VectorRecord(chunk=chunk, embedding=embedding))

    def add_many(self, records: list[VectorRecord]) -> None:
        """Add multiple vector records to the index."""

        for record in records:
            self.add(record.chunk, record.embedding)

    def search(self, query_embedding: list[float], top_k: int = 3) -> list[VectorSearchResult]:
        """Return the most similar chunks to the query embedding."""

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero")

        if not query_embedding:
            raise ValueError("query_embedding cannot be empty")

        results = [
            VectorSearchResult(
                chunk=record.chunk,
                similarity=cosine_similarity(query_embedding, record.embedding),
            )
            for record in self.records
        ]

        return sorted(
            results,
            key=lambda result: (-result.similarity, result.chunk.source, result.chunk.chunk_id),
        )[:top_k]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    """Calculate cosine similarity between two vectors."""

    if len(left) != len(right):
        raise ValueError("vectors must have the same dimensionality")

    left_magnitude = math.sqrt(sum(value * value for value in left))
    right_magnitude = math.sqrt(sum(value * value for value in right))

    if left_magnitude == 0 or right_magnitude == 0:
        return 0.0

    dot_product = sum(left_value * right_value for left_value, right_value in zip(left, right))
    return dot_product / (left_magnitude * right_magnitude)
