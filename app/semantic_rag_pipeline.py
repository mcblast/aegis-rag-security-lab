"""Phase 01.5 semantic RAG pipeline orchestration.

This pipeline runs beside the Phase 01 keyword baseline. It preserves the same
local ingestion, chunking, and mock generation layers while replacing keyword
retrieval with embedding-based vector similarity search.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.chunking import Chunk, chunk_documents
from app.embeddings import EmbeddingProvider, LocalSemanticEmbeddingProvider
from app.ingestion import Document, load_documents
from app.mock_llm import GeneratedResponse, generate_response
from app.retrieval import RetrievalResult
from app.semantic_retrieval import SemanticRetrievalResult, semantic_retrieve


@dataclass(frozen=True)
class SemanticRagPipelineResult:
    """Complete output from a semantic RAG pipeline run."""

    query: str
    answer: str
    sources: list[str]
    retrieved_chunk_ids: list[str]
    semantic_results: list[SemanticRetrievalResult]
    document_count: int
    chunk_count: int
    embedding_model: str


class SemanticRagPipeline:
    """Local semantic RAG pipeline for Phase 01.5."""

    def __init__(
        self,
        knowledge_base_path: str | Path,
        embedding_provider: EmbeddingProvider | None = None,
        max_chunk_words: int = 120,
        overlap_words: int = 20,
        top_k: int = 3,
        minimum_similarity: float = 0.0,
    ) -> None:
        self.knowledge_base_path = Path(knowledge_base_path)
        self.embedding_provider = embedding_provider or LocalSemanticEmbeddingProvider()
        self.max_chunk_words = max_chunk_words
        self.overlap_words = overlap_words
        self.top_k = top_k
        self.minimum_similarity = minimum_similarity
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

    def ask(self, query: str) -> SemanticRagPipelineResult:
        """Run semantic retrieval and mock generation for a query."""

        if not self.chunks:
            self.load()

        semantic_results = semantic_retrieve(
            query=query,
            chunks=self.chunks,
            top_k=self.top_k,
            embedding_provider=self.embedding_provider,
            minimum_similarity=self.minimum_similarity,
        )

        # The existing mock generator expects keyword RetrievalResult objects.
        # This adapter lets Phase 01.5 reuse source-aware generation without
        # changing the Phase 01 mock LLM contract.
        adapted_results = [
            RetrievalResult(
                chunk=result.chunk,
                score=result.similarity,
                matched_terms=[f"semantic_similarity={result.similarity:.3f}"],
            )
            for result in semantic_results
        ]

        generated_response: GeneratedResponse = generate_response(query, adapted_results)

        return SemanticRagPipelineResult(
            query=query,
            answer=generated_response.answer,
            sources=generated_response.sources,
            retrieved_chunk_ids=generated_response.retrieved_chunk_ids,
            semantic_results=semantic_results,
            document_count=len(self.documents),
            chunk_count=len(self.chunks),
            embedding_model=self.embedding_provider.model_name,
        )
