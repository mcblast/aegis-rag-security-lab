# Aegis RAG Security Lab

## Overview

Aegis RAG Security Lab is a hands-on AI security architecture project focused on building, attacking, hardening, and monitoring Retrieval-Augmented Generation (RAG) systems.

The project simulates the lifecycle of securing enterprise AI applications that integrate Large Language Models (LLMs), document retrieval pipelines, user context, policy enforcement mechanisms, and observability controls.

This repository is intentionally structured as a phased security engineering and architecture lab. Historical phase branches are kept as checkpoints so the project’s evolution can be reviewed over time, while `main` represents the current integrated project state.

The primary objective is to develop practical understanding of modern AI security concepts from both an engineering and architectural perspective.

---

## Current Status

```text
Phase 01   - Baseline Keyword RAG Pipeline Implemented
Phase 01.5 - Semantic Retrieval Pipeline Implemented
Phase 02   - Threat Modeling Planned
```

Current `main` includes both the transparent keyword retrieval baseline and the Phase 01.5 semantic retrieval path.

---

## Objectives

This project focuses on developing practical competency in:

- Secure RAG architecture
- Semantic retrieval architecture
- Prompt injection defense
- Indirect prompt injection mitigation
- RAG poisoning detection and containment
- AI governance and policy enforcement
- LLM risk assessment
- Human-in-the-loop security controls
- Retrieval access control
- AI system observability and monitoring
- Security evaluation and adversarial testing
- AI security threat modeling
- Secure enterprise AI integration patterns

---

## Project Goals

The lab is designed to answer the following architectural and security questions:

- How do secure enterprise RAG systems operate?
- Where do AI security risks emerge inside modern LLM pipelines?
- How can retrieval systems leak sensitive data?
- How can malicious documents manipulate LLM behavior?
- How does semantic retrieval change RAG behavior compared to keyword retrieval?
- How should security controls be layered inside AI systems?
- How should AI applications be monitored, evaluated, and governed?
- How do architectural decisions affect AI security posture?

---

## High-Level Architecture

```text
User
 ↓
API Layer
 ↓
Authentication & Role Context
 ↓
Input Validation & Query Classification
 ↓
Retrieval Layer (Keyword and Semantic RAG)
 ↓
Document Access Control
 ↓
Context Builder
 ↓
Prompt Boundary Enforcement
 ↓
LLM Processing Layer
 ↓
Output Validation & Guardrails
 ↓
Audit Logging & Monitoring
 ↓
Response
```

---

## Phase 01 - Baseline Keyword RAG Pipeline

Phase 01 implements a minimal local RAG pipeline that can be studied, tested, attacked, and improved in later phases.

The baseline flow is:

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

This baseline is intentionally simple and intentionally insecure. It does not yet enforce role-based retrieval, prompt boundary protection, context sanitization, poisoned document detection, output validation, or audit logging. Those controls are added in later phases after the baseline behavior is easy to understand.

The keyword retrieval baseline is also intentionally limited. It exists to make retrieval behavior visible before comparing it against the more realistic semantic retrieval path introduced in Phase 01.5.

### Implemented Components

| Component | File | Purpose |
| --- | --- | --- |
| Document ingestion | `app/ingestion.py` | Loads local `.md` and `.txt` files from the knowledge base. |
| Chunking | `app/chunking.py` | Splits documents into overlapping word chunks with source metadata. |
| Keyword retrieval | `app/retrieval.py` | Uses transparent keyword scoring to return relevant chunks. |
| Mock LLM | `app/mock_llm.py` | Produces a source-aware response without requiring external model APIs. |
| Pipeline orchestration | `app/rag_pipeline.py` | Connects ingestion, chunking, keyword retrieval, and generation. |
| CLI runner | `scripts/run_baseline_rag.py` | Runs the baseline RAG pipeline from the terminal. |
| Tests | `tests/test_baseline_rag.py` | Validates ingestion, chunking, retrieval, and source-aware output. |

---

## Phase 01.5 - Semantic Retrieval Pipeline

Phase 01.5 adds a parallel semantic retrieval path beside the keyword baseline.

It does **not** replace the Phase 01 keyword retriever. Instead, it allows keyword and semantic retrieval to be compared side by side before threat modeling and defensive controls are introduced.

The semantic flow is:

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

### Implemented Components

| Component | File | Purpose |
| --- | --- | --- |
| Local embedding provider | `app/embeddings.py` | Converts text into deterministic local vector embeddings. |
| Vector index | `app/vector_index.py` | Stores chunk embeddings and performs cosine similarity search. |
| Semantic retriever | `app/semantic_retrieval.py` | Embeds queries and retrieves chunks by vector similarity. |
| Semantic pipeline | `app/semantic_rag_pipeline.py` | Runs ingestion, chunking, semantic retrieval, and mock generation. |
| Semantic CLI | `scripts/run_semantic_rag.py` | Runs the semantic RAG pipeline from the terminal. |
| Retrieval comparison CLI | `scripts/compare_retrieval_modes.py` | Compares keyword and semantic retrieval for the same query. |
| Semantic tests | `tests/test_semantic_retrieval.py` | Validates embeddings, vector search, semantic retrieval, and pipeline behavior. |
| Phase documentation | `docs/phase-01-5-semantic-retrieval.md` | Documents semantic retrieval architecture, tuning findings, and security questions. |

### Local Embedding Strategy

Phase 01.5 uses a deterministic local embedding provider named:

```text
local-semantic-hash-v1
```

This is not a production embedding model. It is a local, dependency-free scaffold that gives the project an embedding-shaped interface without requiring API keys, model downloads, FAISS, pgvector, or a managed vector database.

The provider combines hashed token buckets with concept normalization for prompt injection, indirect prompt injection, access control, retrieval security, and incident response concepts. Future phases can replace this provider with a real embedding backend while preserving the retrieval pipeline contract.

### Retrieval Tuning

Initial testing showed that semantic retrieval can return noisy results when `top_k` is high and the similarity threshold is too low. The comparison CLI now supports semantic thresholding:

```bash
python scripts/compare_retrieval_modes.py "What happens when external content tells the model to ignore its rules?" --top-k 3 --minimum-similarity 0.35
```

The local embedding provider was also tuned so indirect prompt-injection language such as `external content`, `ignore`, and `rules` maps more strongly toward the AI security policy document.

For full Phase 01.5 architecture notes, see:

```text
docs/phase-01-5-semantic-retrieval.md
```

---

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
pytest
```

Run the baseline keyword RAG pipeline:

```bash
PYTHONPATH=. python scripts/run_baseline_rag.py "What does the policy say about prompt injection?"
```

Run the semantic RAG pipeline:

```bash
PYTHONPATH=. python scripts/run_semantic_rag.py "How do hidden instructions affect AI systems?"
```

Compare keyword and semantic retrieval:

```bash
PYTHONPATH=. python scripts/compare_retrieval_modes.py "How can documents manipulate model behavior?"
```

Compare retrieval modes with semantic thresholding:

```bash
PYTHONPATH=. python scripts/compare_retrieval_modes.py "Who is allowed to see private knowledge sources?" --top-k 3 --minimum-similarity 0.45
```

---

## Example Queries

```bash
PYTHONPATH=. python scripts/run_baseline_rag.py "What risks exist in the retrieval layer?"
PYTHONPATH=. python scripts/run_semantic_rag.py "What happens when external content tells the model to ignore its rules?" --minimum-similarity 0.35
PYTHONPATH=. python scripts/compare_retrieval_modes.py "Who is allowed to see private knowledge sources?" --top-k 3 --minimum-similarity 0.45
```

---

## Current Security Limitations

The current implementation deliberately leaves major security controls unresolved:

- No authentication or user role context
- No document-level access control
- No trust scoring for retrieved documents
- No prompt injection detection
- No separation between trusted instructions and untrusted retrieved content
- No context sanitization
- No output validation
- No audit logging or telemetry
- No poisoned document detection
- No policy enforcement engine

These limitations are not accidents. They define the attack surface for Phase 02 threat modeling and later defensive phases.

---

## Security Domains Covered

### RAG Security

- Retrieval pipeline security
- Keyword retrieval behavior
- Semantic retrieval behavior
- Context boundary enforcement
- Retrieval access control
- Source trust validation
- Sensitive data exposure prevention
- Citation enforcement

### Prompt Injection

- Direct prompt injection
- Indirect prompt injection
- Instruction override attacks
- System prompt extraction attempts
- Retrieval-based manipulation
- Semantic retrieval manipulation

### AI Governance

- Risk classification
- Policy enforcement
- Human approval workflows
- Security control mapping
- Auditability and traceability

### AI Monitoring & Evaluation

- Security telemetry
- Adversarial evaluation
- Risk scoring
- Attack success tracking
- Unsafe output detection

### Enterprise AI Architecture

- Layered security controls
- Separation of concerns
- Policy-driven design
- Configurable security boundaries
- Operational observability

---

## Repository Structure

```text
aegis-rag-security-lab/
│
├── README.md
├── docs/
│   └── phase-01-5-semantic-retrieval.md
├── app/
│   ├── __init__.py
│   ├── ingestion.py
│   ├── chunking.py
│   ├── retrieval.py
│   ├── embeddings.py
│   ├── vector_index.py
│   ├── semantic_retrieval.py
│   ├── mock_llm.py
│   ├── rag_pipeline.py
│   └── semantic_rag_pipeline.py
├── tests/
│   ├── __init__.py
│   ├── test_baseline_rag.py
│   └── test_semantic_retrieval.py
├── redteam/
├── configs/
├── data/
│   └── knowledge_base/
│       ├── access_control.md
│       ├── ai_security_policy.md
│       └── incident_response.md
└── scripts/
    ├── run_baseline_rag.py
    ├── run_semantic_rag.py
    └── compare_retrieval_modes.py
```

---

## Folder Breakdown

### `app/`

Core application and AI pipeline logic.

### `docs/`

Architecture documentation, phase notes, threat models, governance notes, and security analysis.

### `tests/`

Security validation and automated testing.

### `redteam/`

Adversarial testing payloads, attack playbooks, and evaluation results.

### `configs/`

System and policy configuration files.

### `data/`

Knowledge base documents, poisoned documents, and evaluation datasets.

### `scripts/`

Utility and environment setup scripts.

---

## Development Methodology

The project is developed in isolated security phases using dedicated Git branches.

Historical phase branches are kept as architectural checkpoints. They show how the project evolved over time. `main` represents the current integrated system state.

Example workflow:

```text
main
 ├── phase-01-baseline-rag
 ├── phase-01-5-semantic-retrieval
 ├── phase-02-threat-model
 ├── phase-03-prompt-injection-lab
 ├── phase-04-rag-security-controls
 ├── phase-05-governance-and-policy
 ├── phase-06-agent-tool-security
 ├── phase-07-monitoring-and-evals
 └── phase-08-final-integration
```

---

## Planned Phases

### Phase 01 - Baseline Keyword RAG Pipeline

- Local document ingestion
- Word-based chunking
- Keyword retrieval logic
- Mock LLM integration
- Source-aware responses

### Phase 01.5 - Embedding-Based Semantic Retrieval

- Embedding generation for document chunks
- Local vector indexing
- Query embedding
- Similarity search
- Semantic retrieval comparison against keyword retrieval
- Source-aware semantic responses

### Phase 02 - Threat Modeling

- AI threat surface analysis
- Risk register creation
- Trust boundary mapping
- Attack path identification
- Threat modeling for both keyword retrieval and semantic retrieval

### Phase 03 - Prompt Injection Lab

- Direct prompt injection testing
- Indirect prompt injection scenarios
- Retrieval poisoning demonstrations
- Attack simulation framework

### Phase 04 - RAG Security Controls

- Retrieval access control
- Document classification
- Context filtering
- Prompt boundary enforcement
- Output validation

### Phase 05 - Governance & Policy

- AI governance controls
- Risk classification
- Human-in-the-loop workflows
- Policy enforcement engine

### Phase 06 - Agent & Tool Security

- Tool invocation restrictions
- Approval gates
- Action logging
- Role-aware tool access

### Phase 07 - Monitoring & Evaluation

- Security telemetry
- Adversarial evaluation metrics
- Attack success tracking
- Risk analytics

### Phase 08 - Final Integration

- Consolidated architecture
- Security documentation
- Final threat model
- End-to-end validation

---

## Threat Model Focus Areas

The lab explores risks including:

- Prompt injection
- Indirect prompt injection
- RAG poisoning
- Sensitive data leakage
- Broken access control
- Unsafe tool invocation
- Over-trusting LLM outputs
- Retrieval manipulation
- Semantic retrieval manipulation
- Embedding-based retrieval ambiguity
- Governance failures
- Missing observability

---

## Planned Security Controls

Examples of planned controls include:

- Role-based retrieval authorization
- Prompt boundary separation
- Context sanitization
- Citation enforcement
- Policy-driven output filtering
- Human approval checkpoints
- Security telemetry logging
- Retrieval source validation
- Query risk scoring
- Adversarial evaluation pipelines
- Retrieval quality evaluation
- Semantic retrieval filtering

---

## Technology Stack

Current and planned technologies include:

- Python
- FastAPI
- Pytest
- YAML configuration
- Keyword retrieval
- Local vector retrieval
- Embedding-based semantic search
- OpenAI-compatible LLM interfaces
- Structured logging
- Markdown-based threat modeling

---

## Learning Outcomes

This project is intended to strengthen competency in:

- AI security architecture
- Enterprise AI integration
- Security-focused system design
- AI threat modeling
- RAG pipeline security
- Semantic retrieval architecture
- AI governance concepts
- Security control engineering
- Operational AI monitoring
- Security evaluation methodologies
- Technical communication and architecture articulation

---

## Disclaimer

This project is intended for educational, research, and defensive security purposes only.

No real organizational data, credentials, or proprietary systems are used in this repository.
