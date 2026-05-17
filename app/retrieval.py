"""Keyword retrieval for the baseline local RAG pipeline.

Phase 01 uses lexical scoring instead of embeddings so retrieval behavior remains
transparent. This gives us a clean baseline to attack and harden later.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

from app.chunking import Chunk

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9_'-]+")
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "should",
    "that",
    "the",
    "this",
    "to",
    "what",
    "when",
    "where",
    "who",
    "why",
    "with",
}


@dataclass(frozen=True)
class RetrievalResult:
    """A chunk returned by retrieval with an explainable relevance score."""

    chunk: Chunk
    score: float
    matched_terms: list[str]


def tokenize(text: str) -> list[str]:
    """Normalize text into searchable tokens."""

    tokens = [token.lower() for token in TOKEN_PATTERN.findall(text)]
    return [token for token in tokens if token not in STOP_WORDS]


def score_chunk(query_tokens: list[str], chunk: Chunk) -> tuple[float, list[str]]:
    """Score a chunk using simple term-frequency overlap."""

    if not query_tokens:
        return 0.0, []

    chunk_tokens = tokenize(chunk.text)
    chunk_counts = Counter(chunk_tokens)
    unique_query_tokens = sorted(set(query_tokens))

    matched_terms = [term for term in unique_query_tokens if chunk_counts[term] > 0]
    score = float(sum(chunk_counts[term] for term in unique_query_tokens))

    return score, matched_terms


def retrieve(query: str, chunks: list[Chunk], top_k: int = 3) -> list[RetrievalResult]:
    """Retrieve the most relevant chunks for a user query.

    Args:
        query: User question.
        chunks: Available document chunks.
        top_k: Maximum number of results to return.

    Returns:
        Ranked retrieval results with scores and matched terms.
    """

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero")

    query_tokens = tokenize(query)
    results: list[RetrievalResult] = []

    for chunk in chunks:
        score, matched_terms = score_chunk(query_tokens, chunk)
        if score <= 0:
            continue

        results.append(
            RetrievalResult(
                chunk=chunk,
                score=score,
                matched_terms=matched_terms,
            )
        )

    return sorted(
        results,
        key=lambda result: (-result.score, result.chunk.source, result.chunk.chunk_id),
    )[:top_k]
