"""Document ingestion for the baseline local RAG pipeline.

This module intentionally supports only local Markdown and text files for Phase 01.
Keeping ingestion small and explicit makes the later security review easier: we can
clearly see what enters the knowledge base before we add trust scoring, document
classification, access control, or poisoning detection.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

SUPPORTED_EXTENSIONS = {".md", ".txt"}


@dataclass(frozen=True)
class Document:
    """A local source document loaded into the baseline RAG pipeline."""

    source: str
    path: Path
    text: str


def load_documents(directory: str | Path) -> list[Document]:
    """Load supported local documents from a directory.

    Args:
        directory: Directory containing Markdown or text files.

    Returns:
        A list of loaded documents sorted by filename.

    Raises:
        FileNotFoundError: If the directory does not exist.
        NotADirectoryError: If the path exists but is not a directory.
    """

    knowledge_base_path = Path(directory)

    if not knowledge_base_path.exists():
        raise FileNotFoundError(f"Knowledge base directory not found: {knowledge_base_path}")

    if not knowledge_base_path.is_dir():
        raise NotADirectoryError(f"Knowledge base path is not a directory: {knowledge_base_path}")

    documents: list[Document] = []

    for file_path in sorted(knowledge_base_path.iterdir()):
        if not file_path.is_file() or file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        text = file_path.read_text(encoding="utf-8").strip()
        if not text:
            continue

        documents.append(
            Document(
                source=file_path.name,
                path=file_path,
                text=text,
            )
        )

    return documents
