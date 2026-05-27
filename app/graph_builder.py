"""Build a deterministic local knowledge graph for Phase 01.75 GraphRAG.

This module avoids LLM-based entity extraction on purpose. Concepts are defined
with explicit aliases and relationships so graph construction remains explainable
and reviewable during the architecture phase.
"""

from __future__ import annotations

import re
from collections.abc import Iterable

from app.chunking import Chunk
from app.graph_model import GraphChunkLink, GraphEdge, GraphNode, LocalKnowledgeGraph

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9_'-]+")


GRAPH_CONCEPTS: tuple[GraphNode, ...] = (
    GraphNode(
        node_id="prompt_injection",
        label="Prompt Injection",
        aliases=("prompt injection", "instruction override", "ignore previous", "ignore rules"),
        description="Attempts to manipulate model behavior through malicious instructions.",
    ),
    GraphNode(
        node_id="indirect_prompt_injection",
        label="Indirect Prompt Injection",
        aliases=("indirect prompt injection", "external content", "hidden instructions", "retrieved instructions"),
        description="Prompt injection delivered through retrieved or external content.",
    ),
    GraphNode(
        node_id="model_behavior",
        label="Model Behavior",
        aliases=("model behavior", "llm behavior", "model output", "response behavior"),
        description="The way the model interprets context and produces responses.",
    ),
    GraphNode(
        node_id="retrieval_layer",
        label="Retrieval Layer",
        aliases=("retrieval layer", "retrieval", "rag retrieval", "retrieved context"),
        description="The part of the RAG system that selects source chunks for the model.",
    ),
    GraphNode(
        node_id="external_content",
        label="External Content",
        aliases=("external content", "untrusted content", "third-party content", "documents"),
        description="Content that may enter the RAG pipeline from outside trusted instructions.",
    ),
    GraphNode(
        node_id="confidential_source_material",
        label="Confidential Source Material",
        aliases=("confidential", "sensitive", "private", "source material", "knowledge sources"),
        description="Sensitive content stored in or retrieved from the knowledge base.",
    ),
    GraphNode(
        node_id="access_control_failure",
        label="Access Control Failure",
        aliases=("access control failure", "broken access control", "unauthorized", "allowed to see"),
        description="A failure to enforce who can retrieve or view protected information.",
    ),
    GraphNode(
        node_id="sensitive_data_leakage",
        label="Sensitive Data Leakage",
        aliases=("sensitive data leakage", "data leakage", "leak", "expose sensitive", "exposure"),
        description="Unwanted disclosure of sensitive or restricted information.",
    ),
    GraphNode(
        node_id="incident_response",
        label="Incident Response",
        aliases=("incident response", "investigate", "investigation", "forensics", "post-incident"),
        description="Process for investigating, preserving evidence, and responding to AI incidents.",
    ),
    GraphNode(
        node_id="retrieved_context",
        label="Retrieved Context",
        aliases=("retrieved context", "context", "source chunks", "retrieved chunks"),
        description="The selected source material passed toward generation.",
    ),
    GraphNode(
        node_id="model_responses",
        label="Model Responses",
        aliases=("model responses", "answers", "outputs", "generated response"),
        description="The answer generated from retrieved context.",
    ),
    GraphNode(
        node_id="graph_traversal",
        label="Graph Traversal",
        aliases=("graph traversal", "relationship search", "relationship-aware", "connected concepts"),
        description="Following graph relationships to discover connected concepts and source chunks.",
    ),
)


GRAPH_RELATIONSHIPS: tuple[GraphEdge, ...] = (
    GraphEdge("prompt_injection", "manipulates", "model_behavior"),
    GraphEdge("indirect_prompt_injection", "enters_through", "external_content"),
    GraphEdge("external_content", "flows_into", "retrieval_layer"),
    GraphEdge("retrieval_layer", "selects", "retrieved_context"),
    GraphEdge("retrieval_layer", "can_expose", "confidential_source_material"),
    GraphEdge("access_control_failure", "causes", "sensitive_data_leakage"),
    GraphEdge("sensitive_data_leakage", "involves", "confidential_source_material"),
    GraphEdge("incident_response", "preserves", "retrieved_context"),
    GraphEdge("incident_response", "preserves", "model_responses"),
    GraphEdge("graph_traversal", "connects", "retrieved_context"),
    GraphEdge("graph_traversal", "can_surface", "confidential_source_material"),
)


def normalize_text(text: str) -> str:
    """Normalize text for simple deterministic concept matching."""

    return " ".join(token.lower() for token in TOKEN_PATTERN.findall(text))


def _alias_matches(normalized_text: str, alias: str) -> bool:
    normalized_alias = normalize_text(alias)
    return normalized_alias in normalized_text


def find_concept_matches(text: str, concepts: Iterable[GraphNode] = GRAPH_CONCEPTS) -> dict[str, tuple[str, ...]]:
    """Return graph concepts whose aliases appear in text."""

    normalized_text = normalize_text(text)
    matches: dict[str, tuple[str, ...]] = {}

    for concept in concepts:
        matched_aliases = tuple(
            alias for alias in concept.aliases if _alias_matches(normalized_text, alias)
        )
        if matched_aliases:
            matches[concept.node_id] = matched_aliases

    return matches


def build_local_knowledge_graph(chunks: list[Chunk]) -> LocalKnowledgeGraph:
    """Build a local concept graph and link matching source chunks."""

    graph = LocalKnowledgeGraph()

    for concept in GRAPH_CONCEPTS:
        graph.add_node(concept)

    for relationship in GRAPH_RELATIONSHIPS:
        graph.add_edge(relationship)

    for chunk in chunks:
        concept_matches = find_concept_matches(chunk.text)
        for node_id, matched_terms in concept_matches.items():
            graph.link_chunk(
                GraphChunkLink(
                    node_id=node_id,
                    chunk=chunk,
                    matched_terms=matched_terms,
                )
            )

    return graph
