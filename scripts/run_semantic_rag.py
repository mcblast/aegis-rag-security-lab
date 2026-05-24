"""Run the Phase 01.5 semantic RAG pipeline from the command line.

Example:
    python scripts/run_semantic_rag.py "How do hidden instructions affect AI systems?"
"""

from __future__ import annotations

import argparse
from pathlib import Path

from app.semantic_rag_pipeline import SemanticRagPipeline

DEFAULT_KNOWLEDGE_BASE = Path("data/knowledge_base")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the semantic local RAG pipeline.")
    parser.add_argument("query", help="Question to ask the local knowledge base.")
    parser.add_argument(
        "--knowledge-base",
        default=str(DEFAULT_KNOWLEDGE_BASE),
        help="Path to the local knowledge base directory.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Number of chunks to retrieve.",
    )
    parser.add_argument(
        "--minimum-similarity",
        type=float,
        default=0.0,
        help="Minimum semantic similarity required for returned chunks.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    pipeline = SemanticRagPipeline(
        knowledge_base_path=args.knowledge_base,
        top_k=args.top_k,
        minimum_similarity=args.minimum_similarity,
    )
    result = pipeline.ask(args.query)

    print("\n=== AEGIS SEMANTIC RAG RESULT ===")
    print(f"Query: {result.query}")
    print(f"Embedding model: {result.embedding_model}")
    print(f"Documents loaded: {result.document_count}")
    print(f"Chunks indexed: {result.chunk_count}")
    print("\n--- Answer ---")
    print(result.answer)

    print("\n--- Semantic Retrieval Details ---")
    if not result.semantic_results:
        print("No chunks retrieved.")
    else:
        for item in result.semantic_results:
            print(
                f"{item.chunk.chunk_id} | similarity={item.similarity:.3f} | "
                f"model={item.embedding_model}"
            )


if __name__ == "__main__":
    main()
