"""Mock LLM layer for the baseline RAG pipeline.

The mock generator makes the pipeline runnable without external API keys or model
costs. It deliberately does not try to be intelligent; its job is to show how
retrieved context is packaged into a source-aware answer.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.retrieval import RetrievalResult


@dataclass(frozen=True)
class GeneratedResponse:
    """A source-aware generated response from the baseline pipeline."""

    answer: str
    sources: list[str]
    retrieved_chunk_ids: list[str]


def generate_response(query: str, retrieval_results: list[RetrievalResult]) -> GeneratedResponse:
    """Generate a simple source-aware answer from retrieved context."""

    if not retrieval_results:
        return GeneratedResponse(
            answer=(
                "I could not find relevant context in the local knowledge base. "
                "No answer was generated because the baseline pipeline only responds "
                "from retrieved source material."
            ),
            sources=[],
            retrieved_chunk_ids=[],
        )

    evidence_lines = []
    sources: list[str] = []
    chunk_ids: list[str] = []

    for index, result in enumerate(retrieval_results, start=1):
        chunk = result.chunk
        sources.append(chunk.source)
        chunk_ids.append(chunk.chunk_id)
        evidence_lines.append(
            f"{index}. From {chunk.source}: {chunk.text}"
        )

    unique_sources = sorted(set(sources))

    answer = (
        f"Baseline RAG response for query: '{query}'\n\n"
        "The local knowledge base returned the following relevant context:\n"
        + "\n".join(evidence_lines)
        + "\n\n"
        "Sources: "
        + ", ".join(unique_sources)
    )

    return GeneratedResponse(
        answer=answer,
        sources=unique_sources,
        retrieved_chunk_ids=chunk_ids,
    )
