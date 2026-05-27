"""Relationship-aware retrieval for Phase 01.75 local GraphRAG.

Graph retrieval starts from concepts found in the user query, traverses the local
knowledge graph, and returns source chunks linked to the starting and connected
concepts. The result is intentionally explainable: each returned chunk includes
matched concepts, graph paths, and relationship labels.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from app.chunking import Chunk
from app.graph_builder import build_local_knowledge_graph, find_concept_matches
from app.graph_model import GraphRetrievalPath, LocalKnowledgeGraph


@dataclass(frozen=True)
class GraphRetrievalResult:
    """A chunk returned by graph-based retrieval."""

    chunk: Chunk
    score: float
    matched_concepts: list[str]
    matched_terms: list[str]
    relationship_paths: list[GraphRetrievalPath]


def traverse_graph(
    graph: LocalKnowledgeGraph,
    start_node_ids: list[str],
    max_depth: int = 2,
) -> dict[str, list[GraphRetrievalPath]]:
    """Traverse graph relationships from query-matched concepts.

    Returns a mapping of reached node id to the relationship paths that explain
    how the node was reached. Start nodes are included with an empty path list.
    """

    if max_depth < 0:
        raise ValueError("max_depth cannot be negative")

    reached_paths: dict[str, list[GraphRetrievalPath]] = {
        node_id: [] for node_id in start_node_ids if node_id in graph.nodes
    }
    queue: deque[tuple[str, int]] = deque((node_id, 0) for node_id in reached_paths)
    visited_at_depth: dict[str, int] = {node_id: 0 for node_id in reached_paths}

    while queue:
        node_id, depth = queue.popleft()
        if depth >= max_depth:
            continue

        for edge in graph.neighbors(node_id):
            next_depth = depth + 1
            path = GraphRetrievalPath(
                source_id=edge.source_id,
                relationship=edge.relationship,
                target_id=edge.target_id,
                depth=next_depth,
            )
            reached_paths.setdefault(edge.target_id, []).append(path)

            previous_depth = visited_at_depth.get(edge.target_id)
            if previous_depth is None or next_depth < previous_depth:
                visited_at_depth[edge.target_id] = next_depth
                queue.append((edge.target_id, next_depth))

    return reached_paths


def graph_retrieve(
    query: str,
    chunks: list[Chunk],
    top_k: int = 3,
    max_depth: int = 2,
    graph: LocalKnowledgeGraph | None = None,
) -> list[GraphRetrievalResult]:
    """Retrieve chunks through local concept matching and graph traversal."""

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero")
    if max_depth < 0:
        raise ValueError("max_depth cannot be negative")

    knowledge_graph = graph or build_local_knowledge_graph(chunks)
    query_matches = find_concept_matches(query, knowledge_graph.nodes.values())

    if not query_matches:
        return []

    reached_paths = traverse_graph(
        graph=knowledge_graph,
        start_node_ids=list(query_matches.keys()),
        max_depth=max_depth,
    )

    chunk_scores: dict[str, GraphRetrievalResult] = {}

    for node_id, paths in reached_paths.items():
        node = knowledge_graph.nodes[node_id]
        node_links = knowledge_graph.links_for_node(node_id)
        if not node_links:
            continue

        for link in node_links:
            existing = chunk_scores.get(link.chunk.chunk_id)
            direct_match_bonus = 2.0 if node_id in query_matches else 0.0
            relationship_bonus = max(0.0, 1.0 - (min((path.depth for path in paths), default=0) * 0.25))
            concept_score = direct_match_bonus + relationship_bonus + len(link.matched_terms) * 0.25

            if existing is None:
                chunk_scores[link.chunk.chunk_id] = GraphRetrievalResult(
                    chunk=link.chunk,
                    score=concept_score,
                    matched_concepts=[node.label],
                    matched_terms=sorted(set(link.matched_terms)),
                    relationship_paths=paths,
                )
            else:
                chunk_scores[link.chunk.chunk_id] = GraphRetrievalResult(
                    chunk=existing.chunk,
                    score=existing.score + concept_score,
                    matched_concepts=sorted(set(existing.matched_concepts + [node.label])),
                    matched_terms=sorted(set(existing.matched_terms + list(link.matched_terms))),
                    relationship_paths=existing.relationship_paths + paths,
                )

    return sorted(
        chunk_scores.values(),
        key=lambda result: (-result.score, result.chunk.source, result.chunk.chunk_id),
    )[:top_k]
