"""Run the Phase 01 baseline RAG pipeline from the command line.

Example:
    python scripts/run_baseline_rag.py "What does the policy say about prompt injection?"
"""

from __future__ import annotations

import argparse
from pathlib import Path

from app.rag_pipeline import BaselineRagPipeline

DEFAULT_KNOWLEDGE_BASE = Path("data/knowledge_base")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the baseline local RAG pipeline.")
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
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    pipeline = BaselineRagPipeline(
        knowledge_base_path=args.knowledge_base,
        top_k=args.top_k,
    )
    result = pipeline.ask(args.query)

    print("\n=== AEGIS BASELINE RAG RESULT ===")
    print(f"Query: {result.query}")
    print(f"Documents loaded: {result.document_count}")
    print(f"Chunks indexed: {result.chunk_count}")
    print("\n--- Answer ---")
    print(result.answer)

    print("\n--- Retrieval Details ---")
    if not result.retrieval_results:
        print("No chunks retrieved.")
    else:
        for item in result.retrieval_results:
            print(
                f"{item.chunk.chunk_id} | score={item.score} | "
                f"matched_terms={', '.join(item.matched_terms)}"
            )


if __name__ == "__main__":
    main()
