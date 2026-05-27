"""Phase 01.75 local GraphRAG pipeline orchestration.

This pipeline runs beside the Phase 01 keyword baseline and Phase 01.5 semantic
retrieval path. It preserves local ingestion, chunking, and mock generation while
adding relationship-aware graph retrieval.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.chunking import Chunk, chunk_documents
from app.graph_builder import build_local_knowledge_graph
from app.graph_model import LocalKnowledgeGraph
from app.graph_retrieval import GraphRetrievalResult, graph_retrieve
from app.ingestion import Document, load_documents
from app.mock_llm import GeneratedResponse, generate_response
from app.retrieval import RetrievalResult


@dataclass(frozen=True)
class GraphRagPipelineResult:
    """Complete output from a local GraphRAG pipeline run."""

    query: str
    answer: str
    sources: list[str]
    retrieved_chunk_ids: list[str]
    graph_results: list[GraphRetrievalResult]
    document_count: int
    chunk_count: int
    graph_node_count: int
    graph_edge_count: int


class GraphRagPipeline:
    """Local relationship-aware RAG pipeline for Phase 01.75."""

    def __init__(
        self,
        knowledge_base_path: str | Path,
        max_chunk_words: int = 120,
        overlap_words: int = 20,
        top_k: int = 3,
        max_depth: int = 2,
    ) -> None:
        self.knowledge_base_path = Path(knowledge_base_path)
        self.max_chunk_words = max_chunk_words
        self.overlap_words = overlap_words
        self.top_k = top_k
        self.max_depth = max_depth
        self.documents: list[Document] = []
        self.chunks: list[Chunk] = []
        self.graph: LocalKnowledgeGraph | None = None

    def load(self) -> None:
        """Load documents, chunk the knowledge base, and build the graph."""

        self.documents = load_documents(self.knowledge_base_path)
        self.chunks = chunk_documents(
            self.documents,
            max_words=self.max_chunk_words,
            overlap_words=self.overlap_words,
        )
        self.graph = build_local_knowledge_graph(self.chunks)

    def ask(self, query: str) -> GraphRagPipelineResult:
        """Run graph retrieval and mock generation for a query."""

        if not self.chunks or self.graph is None:
            self.load()

        assert self.graph is not None

        graph_results = graph_retrieve(
            query=query,
            chunks=self.chunks,
            top_k=self.top_k,
            max_depth=self.max_depth,
            graph=self.graph,
        )

        # The existing mock generator expects RetrievalResult objects. This adapter
        # lets Phase 01.75 reuse source-aware generation without changing the Phase
        # 01 mock LLM contract.
        adapted_results = [
            RetrievalResult(
                chunk=result.chunk,
                score=result.score,
                matched_terms=[
                    "graph_concepts=" + ",".join(result.matched_concepts),
                    "graph_terms=" + ",".join(result.matched_terms),
                ],
            )
            for result in graph_results
        ]

        generated_response: GeneratedResponse = generate_response(query, adapted_results)

        return GraphRagPipelineResult(
            query=query,
            answer=generated_response.answer,
            sources=generated_response.sources,
            retrieved_chunk_ids=generated_response.retrieved_chunk_ids,
            graph_results=graph_results,
            document_count=len(self.documents),
            chunk_count=len(self.chunks),
            graph_node_count=len(self.graph.nodes),
            graph_edge_count=len(self.graph.edges),
        )
