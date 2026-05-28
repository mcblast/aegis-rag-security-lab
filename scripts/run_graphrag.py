"""Run the Phase 01.75 local GraphRAG pipeline from the command line.

Example:
    PYTHONPATH=. python scripts/run_graphrag.py "How can retrieval expose sensitive content?"
"""

from __future__ import annotations

import argparse
from pathlib import Path

from app.graphrag_pipeline import GraphRagPipeline

DEFAULT_KNOWLEDGE_BASE = Path("data/knowledge_base")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the local GraphRAG pipeline.")
    parser.add_argument("query", help="Question to ask the local knowledge graph.")
    parser.add_argument(
        "--knowledge-base",
        default=str(DEFAULT_KNOWLEDGE_BASE),
        help="Path to the local knowledge base directory.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Number of graph-linked chunks to retrieve.",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=2,
        help="Maximum graph traversal depth from query-matched concepts.",
    )
    return parser.parse_args()


def format_paths(paths: object) -> str:
    if not paths:
        return "direct concept match"
    return "; ".join(
        f"{path.source_id} --{path.relationship}--> {path.target_id} (depth={path.depth})"
        for path in paths
    )


def main() -> None:
    args = parse_args()

    pipeline = GraphRagPipeline(
        knowledge_base_path=args.knowledge_base,
        top_k=args.top_k,
        max_depth=args.max_depth,
    )
    result = pipeline.ask(args.query)

    print("\n=== AEGIS LOCAL GRAPHRAG RESULT ===")
    print(f"Query: {result.query}")
    print(f"Documents loaded: {result.document_count}")
    print(f"Chunks indexed: {result.chunk_count}")
    print(f"Graph nodes: {result.graph_node_count}")
    print(f"Graph edges: {result.graph_edge_count}")
    print(f"Traversal depth: {args.max_depth}")

    print("\n--- Answer ---")
    print(result.answer)

    print("\n--- Graph Retrieval Details ---")
    if not result.graph_results:
        print("No graph-linked chunks retrieved.")
    else:
        for index, item in enumerate(result.graph_results, start=1):
            print(
                f"{index}. {item.chunk.chunk_id} | score={item.score:.3f} | "
                f"concepts={', '.join(item.matched_concepts)} | "
                f"terms={', '.join(item.matched_terms)}"
            )
            print(f"   paths={format_paths(item.relationship_paths)}")


if __name__ == "__main__":
    main()
