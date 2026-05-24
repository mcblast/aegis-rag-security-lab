# Phase 01.5 - Semantic Retrieval Architecture

## Purpose

Phase 01.5 upgrades the AEGIS RAG Security Lab from transparent keyword retrieval to a parallel semantic retrieval path.

The Phase 01 keyword pipeline remains intact. Phase 01.5 does not replace it. Instead, it adds a second retrieval mode so both approaches can be compared before threat modeling and defensive controls are introduced.

This matters because enterprise RAG systems rarely rely only on exact keyword matching. They commonly use embeddings, vector similarity, reranking, hybrid retrieval, or a combination of those approaches. Semantic retrieval makes the lab more realistic and introduces new security questions that will be analyzed in later phases.

---

## Phase 01 Baseline Flow

```text
Local Markdown/Text Documents
 ↓
Document Ingestion
 ↓
Word-Based Chunking
 ↓
Keyword Retrieval
 ↓
Mock LLM Response Generation
 ↓
Source-Aware Answer
```

The keyword baseline is intentionally simple and explainable. It shows which query terms matched each retrieved chunk.

---

## Phase 01.5 Semantic Flow

```text
Local Markdown/Text Documents
 ↓
Document Ingestion
 ↓
Chunking With Source Metadata
 ↓
Embedding Generation
 ↓
Local Vector Index
 ↓
Query Embedding
 ↓
Similarity Search
 ↓
Retrieved Semantic Context
 ↓
Mock LLM Response Generation
 ↓
Source-Aware Answer
```

The semantic path preserves the same ingestion, chunking, and mock generation layers. The retrieval layer changes from lexical scoring to vector similarity.

---

## Implemented Components

| Component | File | Purpose |
| --- | --- | --- |
| Local embedding provider | `app/embeddings.py` | Converts text into deterministic local vector embeddings. |
| Vector index | `app/vector_index.py` | Stores chunk embeddings and performs cosine similarity search. |
| Semantic retriever | `app/semantic_retrieval.py` | Embeds queries and retrieves chunks by vector similarity. |
| Semantic pipeline | `app/semantic_rag_pipeline.py` | Runs ingestion, chunking, semantic retrieval, and mock generation. |
| Semantic CLI | `scripts/run_semantic_rag.py` | Runs the semantic RAG pipeline from the terminal. |
| Retrieval comparison CLI | `scripts/compare_retrieval_modes.py` | Compares keyword and semantic retrieval for the same query, with optional semantic similarity thresholding. |
| Semantic tests | `tests/test_semantic_retrieval.py` | Validates embeddings, vector search, semantic retrieval, and pipeline behavior. |

---

## Local Embedding Strategy

Phase 01.5 uses a deterministic local embedding provider named:

```text
local-semantic-hash-v1
```

This provider is intentionally lightweight. It avoids external APIs, model downloads, secrets, and nondeterministic test results.

The provider combines hashed token buckets with concept-normalization boosts. This gives the project an embedding-shaped architecture without forcing the first semantic retrieval phase to depend on OpenAI, sentence-transformers, FAISS, or a managed vector database.

This is not a production embedding model. It is a stable local scaffold for learning the architecture.

Future phases can replace the embedding provider with a real model while preserving the retrieval interface.

### Concept Normalization

The local provider maps related words into higher-level retrieval concepts. For example:

| Query Terms | Normalized Concept |
| --- | --- |
| `hidden`, `instruction`, `ignore`, `rules`, `override`, `manipulate` | `prompt_injection` |
| `external`, `content`, `email`, `ticket`, `web`, `page` | `indirect_prompt_injection` |
| `private`, `confidential`, `role`, `authorization`, `least`, `privilege` | `access_control` |
| `incident`, `failure`, `investigate`, `evidence`, `logs`, `triage` | `incident_response` |

The `indirect_prompt_injection` concept also bridges into `prompt_injection`, because indirect prompt injection is a subtype of prompt-injection risk. This improves retrieval behavior for queries such as:

```text
What happens when external content tells the model to ignore its rules?
```

That query should retrieve `ai_security_policy.md`, even though it does not explicitly say `prompt injection`.

---

## Running Semantic Retrieval

Run the semantic pipeline:

```bash
python scripts/run_semantic_rag.py "How do hidden instructions affect AI systems?"
```

Run a keyword-versus-semantic comparison:

```bash
python scripts/compare_retrieval_modes.py "How can documents manipulate model behavior?"
```

Run comparison with semantic thresholding:

```bash
python scripts/compare_retrieval_modes.py "What happens when external content tells the model to ignore its rules?" --top-k 3 --minimum-similarity 0.35
```

Run tests:

```bash
pytest
```

---

## Retrieval Tuning Findings

Initial testing showed two separate retrieval-quality issues:

1. **Overbroad retrieval caused by `top_k` and low thresholding.**
   With only three knowledge-base chunks and `top_k=3`, semantic retrieval returned every chunk when the minimum similarity threshold was `0.0`. This was expected behavior, but it made weak matches look more meaningful than they were.

2. **Incorrect top semantic match caused by incomplete concept normalization.**
   The query `What happens when external content tells the model to ignore its rules?` originally ranked `access_control.md` above `ai_security_policy.md`. The local semantic provider did not yet connect terms like `external`, `content`, `ignore`, and `rules` strongly enough to indirect prompt-injection risk.

The implementation was updated to address both findings:

- `scripts/compare_retrieval_modes.py` now supports `--minimum-similarity` for semantic results.
- `app/embeddings.py` now includes expanded concept aliases for indirect prompt injection and prompt-injection behavior.
- `indirect_prompt_injection` now bridges into `prompt_injection` during local embedding generation.

After tuning, the query:

```bash
python scripts/compare_retrieval_modes.py "What happens when external content tells the model to ignore its rules?" --top-k 3 --minimum-similarity 0.35
```

returns only the AI security policy document in the semantic results:

```text
--- Semantic Retrieval ---
1. ai_security_policy.md::chunk-001 | similarity=0.890 | model=local-semantic-hash-v1
```

The access-control paraphrase also behaves correctly:

```bash
python scripts/compare_retrieval_modes.py "Who is allowed to see private knowledge sources?" --top-k 3 --minimum-similarity 0.45
```

Expected semantic result:

```text
--- Semantic Retrieval ---
1. access_control.md::chunk-001 | similarity=0.729 | model=local-semantic-hash-v1
```

These findings are important because they show that semantic retrieval quality depends on more than adding vector search. Retrieval thresholds, concept modeling, scoring behavior, and test queries all affect whether the system retrieves useful context or noisy context.

---

## Architectural Comparison

| Area | Keyword Retrieval | Semantic Retrieval |
| --- | --- | --- |
| Matching method | Exact token overlap | Vector similarity |
| Explainability | High | Lower |
| Handles paraphrase | Weak | Better |
| Operational realism | Lower | Higher |
| Failure mode | Misses meaning if words differ | May retrieve semantically close but wrong content |
| Security concern | Obvious term-based leakage | Less obvious similarity-based leakage |

---

## Security Questions Introduced

Semantic retrieval introduces new security and governance questions:

- Can sensitive content be retrieved even when the user does not use exact sensitive keywords?
- Can poisoned documents be written to become semantically attractive to broad user queries?
- Can semantically similar but incorrect chunks mislead the model response?
- How explainable is semantic retrieval compared to keyword matching?
- Should authorization filtering happen before vector search, after vector search, or both?
- Should document trust labels and sensitivity labels affect vector retrieval?
- How should semantic retrieval behavior be evaluated before security controls are added?
- What similarity threshold should separate useful context from retrieval noise?
- How should retrieval quality be tested when a query spans multiple security domains?

These questions are intentionally not fully solved in Phase 01.5. They become inputs for Phase 02 threat modeling and later defensive phases.

---

## Current Security Limitations

Phase 01.5 still does not enforce:

- Authentication
- Role-based document retrieval
- Document classification
- Trust scoring
- Prompt boundary enforcement
- Context sanitization
- Poisoned document detection
- Output validation
- Audit logging
- Policy enforcement

The purpose of this phase is retrieval realism, not security hardening.

---

## Acceptance Criteria

Phase 01.5 is complete when:

- The Phase 01 keyword pipeline still works.
- The semantic retrieval pipeline runs locally.
- Chunks are embedded with source metadata preserved.
- A local vector index supports cosine similarity search.
- Query embeddings retrieve semantically relevant chunks.
- Semantic responses remain source-aware.
- Keyword and semantic retrieval can be compared from the CLI.
- Similarity thresholding can be used to suppress weak semantic matches.
- Tests validate embedding generation, vector indexing, semantic retrieval, and pipeline output.
- Documentation explains the architectural tradeoff, retrieval tuning findings, and security implications.
