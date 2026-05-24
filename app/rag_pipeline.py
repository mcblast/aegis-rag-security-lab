"""Baseline RAG pipeline orchestration.

This is the Phase 01 end-to-end flow:

local documents -> chunks -> keyword retrieval -> mock generation -> sources

The pipeline is intentionally minimal and insecure. Future phases will threat
model this baseline, attack it, and add controls around retrieval, prompt
boundaries, policy enforcement, and monitoring.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.chunking import Chunk, chunk_documents
from app.ingestion import Document, load_documents
from app.mock_llm import GeneratedResponse, generate_response
from app.retrieval import RetrievalResult, retrieve


@dataclass(frozen=True)
class RagPipelineResult:
    """Complete output from a baseline RAG pipeline run."""

    query: str
    answer: str
    sources: list[str]
    retrieved_chunk_ids: list[str]
    retrieval_results: list[RetrievalResult]
    document_count: int
    chunk_count: int


class BaselineRagPipeline:
    """Small local RAG pipeline used as the Phase 01 insecure baseline."""

    def __init__(
        self,
        knowledge_base_path: str | Path,
        max_chunk_words: int = 120,
        overlap_words: int = 20,
        top_k: int = 3,
    ) -> None:
        self.knowledge_base_path = Path(knowledge_base_path)
        self.max_chunk_words = max_chunk_words
        self.overlap_words = overlap_words
        self.top_k = top_k
        self.documents: list[Document] = []
        self.chunks: list[Chunk] = []

    def load(self) -> None:
        """Load and chunk the local knowledge base."""

        self.documents = load_documents(self.knowledge_base_path)
        self.chunks = chunk_documents(
            self.documents,
            max_words=self.max_chunk_words,
            overlap_words=self.overlap_words,
        )

    def ask(self, query: str) -> RagPipelineResult:
        """Run retrieval and mock generation for a query."""

        if not self.chunks:
            self.load()

        retrieval_results = retrieve(query, self.chunks, top_k=self.top_k)
        generated_response: GeneratedResponse = generate_response(query, retrieval_results)

        return RagPipelineResult(
            query=query,
            answer=generated_response.answer,
            sources=generated_response.sources,
            retrieved_chunk_ids=generated_response.retrieved_chunk_ids,
            retrieval_results=retrieval_results,
            document_count=len(self.documents),
            chunk_count=len(self.chunks),
        )
