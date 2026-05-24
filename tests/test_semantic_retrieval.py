from pathlib import Path

from app.chunking import chunk_documents
from app.embeddings import LocalSemanticEmbeddingProvider
from app.ingestion import load_documents
from app.semantic_rag_pipeline import SemanticRagPipeline
from app.semantic_retrieval import semantic_retrieve
from app.vector_index import InMemoryVectorIndex, cosine_similarity


FIXTURE_KNOWLEDGE_BASE = Path("data/knowledge_base")


def test_local_embedding_provider_returns_normalized_vectors() -> None:
    provider = LocalSemanticEmbeddingProvider(dimensions=32)

    embedding = provider.embed_text("prompt injection hidden instruction attack")

    assert len(embedding) == 32
    assert any(value != 0 for value in embedding)
    assert cosine_similarity(embedding, embedding) > 0.99


def test_vector_index_returns_most_similar_chunk() -> None:
    documents = load_documents(FIXTURE_KNOWLEDGE_BASE)
    chunks = chunk_documents(documents, max_words=80, overlap_words=10)
    provider = LocalSemanticEmbeddingProvider(dimensions=64)
    index = InMemoryVectorIndex()

    for chunk in chunks:
        index.add(chunk, provider.embed_text(chunk.text))

    query_embedding = provider.embed_text("hidden instruction attack against the model")
    results = index.search(query_embedding, top_k=3)

    assert results
    assert results[0].similarity >= results[-1].similarity
    assert any(result.chunk.source == "ai_security_policy.md" for result in results)


def test_semantic_retrieve_handles_paraphrased_prompt_injection_query() -> None:
    documents = load_documents(FIXTURE_KNOWLEDGE_BASE)
    chunks = chunk_documents(documents, max_words=80, overlap_words=10)

    results = semantic_retrieve(
        "How do hidden instructions manipulate model behavior?",
        chunks,
        top_k=3,
    )

    assert results
    assert "ai_security_policy.md" in {result.chunk.source for result in results}
    assert all(result.embedding_model for result in results)


def test_semantic_retrieve_handles_access_control_paraphrase() -> None:
    documents = load_documents(FIXTURE_KNOWLEDGE_BASE)
    chunks = chunk_documents(documents, max_words=80, overlap_words=10)

    results = semantic_retrieve(
        "Who is allowed to see private knowledge sources?",
        chunks,
        top_k=3,
    )

    assert results
    assert "access_control.md" in {result.chunk.source for result in results}


def test_semantic_pipeline_returns_source_aware_answer() -> None:
    pipeline = SemanticRagPipeline(
        FIXTURE_KNOWLEDGE_BASE,
        max_chunk_words=80,
        overlap_words=10,
        top_k=3,
    )

    result = pipeline.ask("How should teams investigate AI failures?")

    assert result.document_count >= 3
    assert result.chunk_count >= 3
    assert result.answer
    assert result.sources
    assert result.retrieved_chunk_ids
    assert result.embedding_model == "local-semantic-hash-v1"
    assert "Sources:" in result.answer
    assert "incident_response.md" in result.sources
