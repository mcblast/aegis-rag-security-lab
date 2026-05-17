# Aegis RAG Security Lab

## Overview

Aegis RAG Security Lab is a hands-on AI security architecture project focused on building, attacking, hardening, and monitoring Retrieval-Augmented Generation (RAG) systems.

The project is designed to simulate the lifecycle of securing enterprise AI applications that integrate Large Language Models (LLMs), document retrieval pipelines, user context, and policy enforcement mechanisms.

This repository is intentionally structured as a phased security engineering and architecture lab where each branch introduces a new layer of functionality, threat modeling, governance, adversarial testing, and defensive controls.

The primary objective is to develop practical understanding of modern AI security concepts from both an engineering and architectural perspective.

---

# Objectives

This project focuses on developing practical competency in:

- Secure RAG architecture
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

# Project Goals

The lab is designed to answer the following architectural and security questions:

- How do secure enterprise RAG systems operate?
- Where do AI security risks emerge inside modern LLM pipelines?
- How can retrieval systems leak sensitive data?
- How can malicious documents manipulate LLM behavior?
- How should security controls be layered inside AI systems?
- How should AI applications be monitored, evaluated, and governed?
- How do architectural decisions affect AI security posture?

---

# High-Level Architecture

```text
User
 ↓
API Layer
 ↓
Authentication & Role Context
 ↓
Input Validation & Query Classification
 ↓
Retrieval Layer (RAG)
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

# Phase 01 - Baseline RAG Pipeline

Phase 01 implements a minimal local RAG pipeline that can be studied, tested, attacked, and improved in later phases.

The current baseline flow is:

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

## Implemented Components

| Component | File | Purpose |
| --- | --- | --- |
| Document ingestion | `app/ingestion.py` | Loads local `.md` and `.txt` files from the knowledge base. |
| Chunking | `app/chunking.py` | Splits documents into overlapping word chunks with source metadata. |
| Retrieval | `app/retrieval.py` | Uses transparent keyword scoring to return relevant chunks. |
| Mock LLM | `app/mock_llm.py` | Produces a source-aware response without requiring external model APIs. |
| Pipeline orchestration | `app/rag_pipeline.py` | Connects ingestion, chunking, retrieval, and generation. |
| CLI runner | `scripts/run_baseline_rag.py` | Runs the baseline RAG pipeline from the terminal. |
| Tests | `tests/test_baseline_rag.py` | Validates ingestion, chunking, retrieval, and source-aware output. |

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the baseline RAG pipeline:

```bash
python scripts/run_baseline_rag.py "What does the policy say about prompt injection?"
```

Run tests:

```bash
pytest
```

## Example Queries

```bash
python scripts/run_baseline_rag.py "What risks exist in the retrieval layer?"
python scripts/run_baseline_rag.py "How should AI incidents be investigated?"
python scripts/run_baseline_rag.py "What does the policy say about access control?"
```

## Current Security Limitations

The Phase 01 baseline deliberately leaves major risks unresolved:

- No authentication or user role context
- No document-level access control
- No trust scoring for retrieved documents
- No prompt injection detection
- No separation between trusted instructions and untrusted retrieved content
- No output validation
- No audit logging or telemetry
- No poisoned document detection

These limitations are not accidents. They define the attack surface for the next phases.

---

# Security Domains Covered

## RAG Security

- Retrieval pipeline security
- Context boundary enforcement
- Retrieval access control
- Source trust validation
- Sensitive data exposure prevention
- Citation enforcement

## Prompt Injection

- Direct prompt injection
- Indirect prompt injection
- Instruction override attacks
- System prompt extraction attempts
- Retrieval-based manipulation

## AI Governance

- Risk classification
- Policy enforcement
- Human approval workflows
- Security control mapping
- Auditability and traceability

## AI Monitoring & Evaluation

- Security telemetry
- Adversarial evaluation
- Risk scoring
- Attack success tracking
- Unsafe output detection

## Enterprise AI Architecture

- Layered security controls
- Separation of concerns
- Policy-driven design
- Configurable security boundaries
- Operational observability

---

# Repository Structure

```text
aegis-rag-security-lab/
│
├── README.md
├── docs/
├── app/
│   ├── __init__.py
│   ├── ingestion.py
│   ├── chunking.py
│   ├── retrieval.py
│   ├── mock_llm.py
│   └── rag_pipeline.py
├── tests/
│   ├── __init__.py
│   └── test_baseline_rag.py
├── redteam/
├── configs/
├── data/
│   └── knowledge_base/
│       ├── access_control.md
│       ├── ai_security_policy.md
│       └── incident_response.md
└── scripts/
    └── run_baseline_rag.py
```

---

# Folder Breakdown

## `app/`

Core application and AI pipeline logic.

## `docs/`

Architecture documentation, threat models, governance notes, and security analysis.

## `tests/`

Security validation and automated testing.

## `redteam/`

Adversarial testing payloads, attack playbooks, and evaluation results.

## `configs/`

System and policy configuration files.

## `data/`

Knowledge base documents, poisoned documents, and evaluation datasets.

## `scripts/`

Utility and environment setup scripts.

---

# Development Methodology

The project is intentionally developed in isolated security phases using dedicated Git branches.

Each branch represents a focused learning and implementation domain.

Example workflow:

```text
main
 ├── phase-01-baseline-rag
 ├── phase-02-threat-model
 ├── phase-03-prompt-injection-lab
 ├── phase-04-rag-security-controls
 ├── phase-05-governance-and-policy
 ├── phase-06-agent-tool-security
 ├── phase-07-monitoring-and-evals
 └── phase-08-final-integration
```

This structure preserves architectural evolution, implementation history, and security maturity progression.

---

# Planned Phases

## Phase 01 - Baseline RAG Pipeline

- Local document ingestion
- Chunking
- Retrieval logic
- Mock LLM integration
- Source-aware responses

## Phase 02 - Threat Modeling

- AI threat surface analysis
- Risk register creation
- Trust boundary mapping
- Attack path identification

## Phase 03 - Prompt Injection Lab

- Direct prompt injection testing
- Indirect prompt injection scenarios
- Retrieval poisoning demonstrations
- Attack simulation framework

## Phase 04 - RAG Security Controls

- Retrieval access control
- Document classification
- Context filtering
- Prompt boundary enforcement
- Output validation

## Phase 05 - Governance & Policy

- AI governance controls
- Risk classification
- Human-in-the-loop workflows
- Policy enforcement engine

## Phase 06 - Agent & Tool Security

- Tool invocation restrictions
- Approval gates
- Action logging
- Role-aware tool access

## Phase 07 - Monitoring & Evaluation

- Security telemetry
- Adversarial evaluation metrics
- Attack success tracking
- Risk analytics

## Phase 08 - Final Integration

- Consolidated architecture
- Security documentation
- Final threat model
- End-to-end validation

---

# Threat Model Focus Areas

The lab explores risks including:

- Prompt injection
- Indirect prompt injection
- RAG poisoning
- Sensitive data leakage
- Broken access control
- Unsafe tool invocation
- Over-trusting LLM outputs
- Retrieval manipulation
- Governance failures
- Missing observability

---

# Planned Security Controls

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

---

# Technology Stack

Current and planned technologies include:

- Python
- FastAPI
- Pytest
- YAML configuration
- Local vector retrieval
- OpenAI-compatible LLM interfaces
- Structured logging
- Markdown-based threat modeling

---

# Learning Outcomes

This project is intended to strengthen competency in:

- AI security architecture
- Enterprise AI integration
- Security-focused system design
- AI threat modeling
- RAG pipeline security
- AI governance concepts
- Security control engineering
- Operational AI monitoring
- Security evaluation methodologies
- Technical communication and architecture articulation

---

# Status

Current Status:

```text
Phase 01 - Baseline RAG Pipeline Implemented
```

---

# Disclaimer

This project is intended for educational, research, and defensive security purposes only.

No real organizational data, credentials, or proprietary systems are used in this repository.
