from pathlib import Path

import pytest

from app.chunking import chunk_documents
from app.graph_builder import build_local_knowledge_graph, find_concept_matches
from app.graph_retrieval import graph_retrieve, traverse_graph
from app.graphrag_pipeline import GraphRagPipeline
from app.ingestion import load_documents

FIXTURE_KNOWLEDGE_BASE = Path("data/knowledge_base")


def test_find_concept_matches_detects_prompt_injection_language() -> None:
    matches = find_concept_matches("External content contains hidden instructions to ignore rules.")

    assert "indirect_prompt_injection" in matches
    assert "external_content" in matches
    assert matches["indirect_prompt_injection"]


def test_build_local_knowledge_graph_creates_nodes_edges_and_chunk_links() -> None:
    documents = load_documents(FIXTURE_KNOWLEDGE_BASE)
    chunks = chunk_documents(documents, max_words=80, overlap_words=10)

    graph = build_local_knowledge_graph(chunks)

    assert "prompt_injection" in graph.nodes
    assert "retrieval_layer" in graph.nodes
    assert graph.edges
    assert graph.chunk_links
    assert any(link.chunk.chunk_id for link in graph.chunk_links)


def test_traverse_graph_reaches_related_concepts() -> None:
    documents = load_documents(FIXTURE_KNOWLEDGE_BASE)
    chunks = chunk_documents(documents, max_words=80, overlap_words=10)
    graph = build_local_knowledge_graph(chunks)

    reached = traverse_graph(graph, ["prompt_injection"], max_depth=2)

    assert "prompt_injection" in reached
    assert "model_behavior" in reached
    assert any(path.relationship == "manipulates" for path in reached["model_behavior"])


def test_graph_retrieve_returns_relationship_aware_results() -> None:
    documents = load_documents(FIXTURE_KNOWLEDGE_BASE)
    chunks = chunk_documents(documents, max_words=80, overlap_words=10)

    results = graph_retrieve(
        "How can prompt injection manipulate model behavior?",
        chunks,
        top_k=3,
        max_depth=2,
    )

    assert results
    assert results[0].score > 0
    assert any("Prompt Injection" in result.matched_concepts for result in results)
    assert all(result.chunk.chunk_id for result in results)


def test_graph_retrieve_returns_empty_when_query_has_no_graph_concepts() -> None:
    documents = load_documents(FIXTURE_KNOWLEDGE_BASE)
    chunks = chunk_documents(documents, max_words=80, overlap_words=10)

    results = graph_retrieve("banana spaceship ocean unrelated", chunks, top_k=3)

    assert results == []


def test_graph_retrieve_rejects_invalid_top_k() -> None:
    with pytest.raises(ValueError, match="top_k must be greater than zero"):
        graph_retrieve("prompt injection", [], top_k=0)


def test_graph_retrieve_rejects_invalid_depth() -> None:
    with pytest.raises(ValueError, match="max_depth cannot be negative"):
        graph_retrieve("prompt injection", [], max_depth=-1)


def test_graphrag_pipeline_returns_source_aware_answer() -> None:
    pipeline = GraphRagPipeline(
        FIXTURE_KNOWLEDGE_BASE,
        max_chunk_words=80,
        overlap_words=10,
        top_k=3,
        max_depth=2,
    )

    result = pipeline.ask("How can retrieval expose confidential source material?")

    assert result.document_count >= 3
    assert result.chunk_count >= 3
    assert result.graph_node_count >= 3
    assert result.graph_edge_count >= 3
    assert result.answer
    assert result.sources
    assert result.retrieved_chunk_ids
    assert result.graph_results
    assert "Sources:" in result.answer
