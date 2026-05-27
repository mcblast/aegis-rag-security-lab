"""Compare keyword, semantic, and GraphRAG retrieval modes.

Example:
    PYTHONPATH=. python scripts/compare_all_retrieval_modes.py "How can documents manipulate model behavior?"
"""

from __future__ import annotations

import argparse
from pathlib import Path

from app.chunking import chunk_documents
from app.graph_builder import build_local_knowledge_graph
from app.graph_retrieval import graph_retrieve
from app.ingestion import load_documents
from app.retrieval import retrieve
from app.semantic_retrieval import semantic_retrieve

DEFAULT_KNOWLEDGE_BASE = Path("data/knowledge_base")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare keyword, semantic, and GraphRAG retrieval.")
    parser.add_argument("query", help="Question to run through all retrieval modes.")
    parser.add_argument(
        "--knowledge-base",
        default=str(DEFAULT_KNOWLEDGE_BASE),
        help="Path to the local knowledge base directory.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Number of chunks to retrieve from each mode.",
    )
    parser.add_argument(
        "--minimum-similarity",
        type=float,
        default=0.0,
        help="Minimum semantic similarity required for returned semantic chunks.",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=2,
        help="Maximum GraphRAG traversal depth from query-matched concepts.",
    )
    return parser.parse_args()


def print_overlap(keyword_ids: set[str], semantic_ids: set[str], graph_ids: set[str]) -> None:
    print("\n--- Retrieval Overlap ---")
    print(f"Keyword ∩ Semantic: {', '.join(sorted(keyword_ids & semantic_ids)) or 'none'}")
    print(f"Keyword ∩ GraphRAG: {', '.join(sorted(keyword_ids & graph_ids)) or 'none'}")
    print(f"Semantic ∩ GraphRAG: {', '.join(sorted(semantic_ids & graph_ids)) or 'none'}")
    print(f"All three modes: {', '.join(sorted(keyword_ids & semantic_ids & graph_ids)) or 'none'}")


def main() -> None:
    args = parse_args()
    documents = load_documents(args.knowledge_base)
    chunks = chunk_documents(documents)
    graph = build_local_knowledge_graph(chunks)

    keyword_results = retrieve(args.query, chunks, top_k=args.top_k)
    semantic_results = semantic_retrieve(
        args.query,
        chunks,
        top_k=args.top_k,
        minimum_similarity=args.minimum_similarity,
    )
    graph_results = graph_retrieve(
        args.query,
        chunks,
        top_k=args.top_k,
        max_depth=args.max_depth,
        graph=graph,
    )

    print("\n=== AEGIS ALL-MODE RETRIEVAL COMPARISON ===")
    print(f"Query: {args.query}")
    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks indexed: {len(chunks)}")
    print(f"Graph nodes: {len(graph.nodes)}")
    print(f"Graph edges: {len(graph.edges)}")

    print("\n--- Keyword Retrieval ---")
    if not keyword_results:
        print("No chunks retrieved.")
    else:
        for index, item in enumerate(keyword_results, start=1):
            print(
                f"{index}. {item.chunk.chunk_id} | score={item.score} | "
                f"matched_terms={', '.join(item.matched_terms)}"
            )

    print("\n--- Semantic Retrieval ---")
    if not semantic_results:
        print("No chunks retrieved.")
    else:
        for index, item in enumerate(semantic_results, start=1):
            print(
                f"{index}. {item.chunk.chunk_id} | similarity={item.similarity:.3f} | "
                f"model={item.embedding_model}"
            )

    print("\n--- GraphRAG Retrieval ---")
    if not graph_results:
        print("No graph-linked chunks retrieved.")
    else:
        for index, item in enumerate(graph_results, start=1):
            print(
                f"{index}. {item.chunk.chunk_id} | score={item.score:.3f} | "
                f"concepts={', '.join(item.matched_concepts)} | "
                f"terms={', '.join(item.matched_terms)}"
            )

    print_overlap(
        {item.chunk.chunk_id for item in keyword_results},
        {item.chunk.chunk_id for item in semantic_results},
        {item.chunk.chunk_id for item in graph_results},
    )


if __name__ == "__main__":
    main()
