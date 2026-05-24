"""Compare Phase 01 keyword retrieval against Phase 01.5 semantic retrieval.

Example:
    python scripts/compare_retrieval_modes.py "How do hidden instructions affect AI systems?"
"""

from __future__ import annotations

import argparse
from pathlib import Path

from app.chunking import chunk_documents
from app.ingestion import load_documents
from app.retrieval import retrieve
from app.semantic_retrieval import semantic_retrieve

DEFAULT_KNOWLEDGE_BASE = Path("data/knowledge_base")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare keyword and semantic retrieval results.")
    parser.add_argument("query", help="Question to run through both retrieval modes.")
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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    documents = load_documents(args.knowledge_base)
    chunks = chunk_documents(documents)

    keyword_results = retrieve(args.query, chunks, top_k=args.top_k)
    semantic_results = semantic_retrieve(
        args.query,
        chunks,
        top_k=args.top_k,
        minimum_similarity=args.minimum_similarity,
    )

    print("\n=== AEGIS RETRIEVAL MODE COMPARISON ===")
    print(f"Query: {args.query}")
    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks indexed: {len(chunks)}")
    print(f"Semantic minimum similarity: {args.minimum_similarity:.3f}")

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


if __name__ == "__main__":
    main()
