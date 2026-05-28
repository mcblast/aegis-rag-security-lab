"""Local graph model primitives for Phase 01.75 GraphRAG.

The graph model is intentionally small, deterministic, and dependency-free. Phase
01.75 is about making relationship-aware retrieval inspectable before Phase 02
threat modeling, not introducing an external graph database or opaque extraction
framework.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.chunking import Chunk


@dataclass(frozen=True)
class GraphNode:
    """A concept or entity represented inside the local knowledge graph."""

    node_id: str
    label: str
    aliases: tuple[str, ...] = ()
    description: str = ""


@dataclass(frozen=True)
class GraphEdge:
    """A directed relationship between two graph nodes."""

    source_id: str
    relationship: str
    target_id: str
    evidence: str = ""


@dataclass(frozen=True)
class GraphRetrievalPath:
    """A traversed relationship path used to explain graph retrieval."""

    source_id: str
    relationship: str
    target_id: str
    depth: int


@dataclass(frozen=True)
class GraphChunkLink:
    """A mapping between a graph concept and a source chunk."""

    node_id: str
    chunk: Chunk
    matched_terms: tuple[str, ...]


@dataclass
class LocalKnowledgeGraph:
    """A small in-memory concept graph with source-chunk links."""

    nodes: dict[str, GraphNode] = field(default_factory=dict)
    edges: list[GraphEdge] = field(default_factory=list)
    chunk_links: list[GraphChunkLink] = field(default_factory=list)

    def add_node(self, node: GraphNode) -> None:
        """Add or replace a graph node by node id."""

        self.nodes[node.node_id] = node

    def add_edge(self, edge: GraphEdge) -> None:
        """Add a directed relationship between graph nodes."""

        if edge.source_id not in self.nodes:
            raise ValueError(f"Unknown source node: {edge.source_id}")
        if edge.target_id not in self.nodes:
            raise ValueError(f"Unknown target node: {edge.target_id}")
        self.edges.append(edge)

    def link_chunk(self, link: GraphChunkLink) -> None:
        """Attach a source chunk to a graph node."""

        if link.node_id not in self.nodes:
            raise ValueError(f"Unknown linked node: {link.node_id}")
        self.chunk_links.append(link)

    def neighbors(self, node_id: str) -> list[GraphEdge]:
        """Return outgoing edges for a graph node."""

        return [edge for edge in self.edges if edge.source_id == node_id]

    def links_for_node(self, node_id: str) -> list[GraphChunkLink]:
        """Return source chunks linked to a graph node."""

        return [link for link in self.chunk_links if link.node_id == node_id]
