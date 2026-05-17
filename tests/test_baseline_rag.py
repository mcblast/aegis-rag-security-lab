from pathlib import Path

from app.chunking import chunk_documents, chunk_text
from app.ingestion import load_documents
from app.rag_pipeline import BaselineRagPipeline
from app.retrieval import retrieve, tokenize


FIXTURE_KNOWLEDGE_BASE = Path("data/knowledge_base")


def test_load_documents_reads_supported_files() -> None:
    documents = load_documents(FIXTURE_KNOWLEDGE_BASE)

    assert len(documents) >= 3
    assert {document.source for document in documents} >= {
        "access_control.md",
        "ai_security_policy.md",
        "incident_response.md",
    }
    assert all(document.text for document in documents)


def test_chunk_text_creates_overlapping_chunks() -> None:
    text = " ".join(f"word{i}" for i in range(1, 21))

    chunks = chunk_text(text, max_words=10, overlap_words=2)

    assert len(chunks) == 3
    assert chunks[0].split()[-2:] == chunks[1].split()[:2]


def test_chunk_documents_preserves_source_metadata() -> None:
    documents = load_documents(FIXTURE_KNOWLEDGE_BASE)

    chunks = chunk_documents(documents, max_words=40, overlap_words=5)

    assert chunks
    assert all(chunk.chunk_id for chunk in chunks)
    assert all(chunk.source.endswith((".md", ".txt")) for chunk in chunks)
    assert all(chunk.text for chunk in chunks)


def test_tokenize_removes_common_stop_words() -> None:
    tokens = tokenize("What is the policy for prompt injection?")

    assert "what" not in tokens
    assert "the" not in tokens
    assert "policy" in tokens
    assert "prompt" in tokens
    assert "injection" in tokens


def test_retrieve_returns_relevant_prompt_injection_chunk() -> None:
    documents = load_documents(FIXTURE_KNOWLEDGE_BASE)
    chunks = chunk_documents(documents, max_words=80, overlap_words=10)

    results = retrieve("How should we handle prompt injection?", chunks, top_k=2)

    assert results
    assert results[0].score > 0
    assert "ai_security_policy.md" in {result.chunk.source for result in results}
    assert "prompt" in results[0].matched_terms or "injection" in results[0].matched_terms


def test_pipeline_returns_source_aware_answer() -> None:
    pipeline = BaselineRagPipeline(FIXTURE_KNOWLEDGE_BASE, max_chunk_words=80, overlap_words=10, top_k=2)

    result = pipeline.ask("What risks exist in the retrieval layer?")

    assert result.document_count >= 3
    assert result.chunk_count >= 3
    assert result.answer
    assert result.sources
    assert result.retrieved_chunk_ids
    assert "Sources:" in result.answer


def test_pipeline_handles_no_retrieval_match() -> None:
    pipeline = BaselineRagPipeline(FIXTURE_KNOWLEDGE_BASE, max_chunk_words=80, overlap_words=10, top_k=2)

    result = pipeline.ask("banana spaceship ocean unrelated")

    assert result.answer.startswith("I could not find relevant context")
    assert result.sources == []
    assert result.retrieved_chunk_ids == []
