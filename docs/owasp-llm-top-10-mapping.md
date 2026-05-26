# OWASP Top 10 for LLM Applications Mapping

## Purpose

This document maps the AEGIS RAG Security Lab roadmap to the OWASP Top 10 for LLM Applications.

The goal is not to claim full OWASP coverage immediately. The goal is to use OWASP as a structured threat-modeling and control-mapping framework as the project evolves from baseline retrieval into secure RAG architecture, adversarial testing, governance, monitoring, and agent/tool security.

Official reference:

```text
https://genai.owasp.org/llm-top-10/
```

---

## Mapping Summary

| OWASP ID | Risk | AEGIS Coverage | Project Phase |
| --- | --- | --- | --- |
| LLM01 | Prompt Injection | Direct and indirect prompt injection scenarios against retrieved context and model behavior | Phase 03 / Phase 04 |
| LLM02 | Sensitive Information Disclosure | Retrieval access control, document classification, role-aware filtering, leakage testing | Phase 04 |
| LLM03 | Supply Chain | Dependency, model provider, embedding provider, dataset, and external component risk documentation | Phase 02 / Phase 08 |
| LLM04 | Data and Model Poisoning | Poisoned document tests, malicious knowledge-base content, graph relationship poisoning | Phase 03 / Phase 04 |
| LLM05 | Improper Output Handling | Output validation, unsafe response checks, citation enforcement, policy-driven filtering | Phase 04 / Phase 05 |
| LLM06 | Excessive Agency | Tool restrictions, approval gates, human-in-the-loop workflows, role-aware tool access | Phase 05 / Phase 06 |
| LLM07 | System Prompt Leakage | Prompt extraction tests and instruction boundary validation | Phase 03 / Phase 04 |
| LLM08 | Vector and Embedding Weaknesses | Semantic retrieval ambiguity, threshold tuning, embedding manipulation, noisy retrieval testing | Phase 01.5 / Phase 02 / Phase 04 |
| LLM09 | Misinformation | Source grounding, retrieval quality evaluation, hallucination checks, answer confidence boundaries | Phase 04 / Phase 07 |
| LLM10 | Unbounded Consumption | Query limits, top-k limits, context size controls, rate/cost/resource constraints | Phase 05 / Phase 07 |

---

## LLM01: Prompt Injection

### How it applies

RAG systems are exposed to both direct and indirect prompt injection.

Direct prompt injection occurs when a user tries to override model behavior through the prompt.

Indirect prompt injection occurs when retrieved documents contain malicious instructions that attempt to manipulate the model after retrieval.

### Planned test cases

- User asks the model to ignore system instructions.
- Retrieved document contains hidden instructions.
- Retrieved document attempts to override response rules.
- Retrieved document asks the model to reveal private context.
- Retrieved document attempts to alter citation behavior.

### Planned controls

- Prompt boundary enforcement
- Treat retrieved content as untrusted evidence
- Context sanitization
- Injection pattern detection
- Source-aware response formatting
- Refusal behavior for instruction override attempts

### Relevant phases

- Phase 03: Prompt Injection Lab
- Phase 04: RAG Security Controls

---

## LLM02: Sensitive Information Disclosure

### How it applies

A RAG system can disclose sensitive information if retrieval is based only on relevance and not authorization.

Semantic retrieval can increase this risk because sensitive content may be retrieved even when the user does not use exact sensitive keywords.

### Planned test cases

- Public user query retrieves confidential content.
- Semantic query retrieves sensitive chunks through paraphrase.
- Graph traversal exposes connected sensitive concepts.
- Retrieved context includes data outside the user's role.

### Planned controls

- Role-based retrieval authorization
- Document-level access control
- Document classification labels
- Pre-retrieval authorization filtering
- Post-retrieval validation
- Sensitive data leakage checks

### Relevant phases

- Phase 02: Threat Modeling
- Phase 04: RAG Security Controls

---

## LLM03: Supply Chain

### How it applies

LLM applications depend on models, embeddings, libraries, datasets, document stores, orchestration frameworks, and deployment infrastructure.

Even this local lab has supply-chain considerations around dependencies, embedding providers, knowledge-base content, and future model/API integrations.

### Planned test cases

- Identify third-party dependencies.
- Document local embedding provider limitations.
- Review model/provider trust assumptions.
- Track future external services added to the architecture.

### Planned controls

- Dependency review
- SBOM-style documentation
- Model/provider trust notes
- Version pinning where appropriate
- Secure configuration review
- Secrets hygiene

### Relevant phases

- Phase 02: Threat Modeling
- Phase 08: Final Integration

---

## LLM04: Data and Model Poisoning

### How it applies

RAG systems can be poisoned through malicious or misleading documents added to the knowledge base.

GraphRAG introduces an additional poisoning path: malicious or incorrect relationships between entities and concepts.

### Planned test cases

- Poisoned document inserted into the knowledge base.
- Document crafted to rank highly for broad security queries.
- Malicious chunk attempts to manipulate model behavior.
- Incorrect graph edge changes retrieval path.
- Poisoned relationship links sensitive concepts to benign queries.

### Planned controls

- Document trust scoring
- Source validation
- Poisoned document detection
- Graph node and edge trust controls
- Retrieval anomaly review
- Adversarial test corpus

### Relevant phases

- Phase 03: Prompt Injection Lab
- Phase 04: RAG Security Controls

---

## LLM05: Improper Output Handling

### How it applies

LLM output should not be trusted as safe by default.

For this project, output risk includes hallucinated claims, unsafe recommendations, missing citations, policy-violating content, or responses that overstate what the retrieved evidence supports.

### Planned test cases

- Model produces answer without source support.
- Model ignores retrieved evidence.
- Model follows malicious retrieved instructions.
- Model outputs sensitive content from restricted context.
- Model returns unsafe or policy-violating output.

### Planned controls

- Output validation
- Citation enforcement
- Evidence-grounded answer checks
- Policy-driven output filtering
- Unsafe output detection
- Response confidence boundaries

### Relevant phases

- Phase 04: RAG Security Controls
- Phase 05: Governance & Policy

---

## LLM06: Excessive Agency

### How it applies

This becomes critical if the RAG system gains tools or agentic capabilities.

Examples include file access, ticket creation, repository actions, cloud API calls, email actions, deployment actions, or database actions.

The core question becomes:

```text
Should this agent be allowed to perform this action right now, in this context, against this resource?
```

### Planned test cases

- Agent attempts to use a tool outside task scope.
- Agent attempts destructive action.
- Agent attempts cross-context credential use.
- Agent attempts production action from a low-risk task.
- Agent attempts action requiring approval.

### Planned controls

- Runtime identity and authorization for AI agents
- Tool invocation restrictions
- Least-privilege tool access
- Approval gates
- Human-in-the-loop workflows
- Action logging
- Role-aware tool access
- Deny-list for destructive operations
- Just-in-time scoped access

### Relevant phases

- Phase 05: Governance & Policy
- Phase 06: Agent & Tool Security

---

## LLM07: System Prompt Leakage

### How it applies

Attackers may attempt to extract system prompts, hidden instructions, policy text, developer notes, or internal reasoning scaffolds.

In RAG systems, this risk can combine with retrieved content that asks the model to reveal hidden instructions.

### Planned test cases

- User asks for system prompt.
- User asks model to encode or transform hidden instructions.
- Retrieved document instructs model to reveal system prompt.
- User attempts roleplay or debugging pretext to extract hidden configuration.

### Planned controls

- System prompt confidentiality tests
- Instruction boundary enforcement
- Refusal behavior for prompt extraction
- Retrieved-content isolation
- Output validation

### Relevant phases

- Phase 03: Prompt Injection Lab
- Phase 04: RAG Security Controls

---

## LLM08: Vector and Embedding Weaknesses

### How it applies

This is one of the most important OWASP categories for this repo.

The semantic retrieval path introduces risks from similarity search, embedding ambiguity, noisy retrieval, weak thresholding, and semantically attractive malicious content.

GraphRAG will add relationship-based retrieval risks.

### Current project relevance

Phase 01.5 already includes:

- Local embedding provider
- Vector index
- Semantic retrieval
- Similarity thresholding
- Keyword-versus-semantic comparison
- Retrieval tuning notes

### Planned test cases

- Query retrieves semantically close but incorrect chunk.
- Low similarity threshold returns noisy context.
- Broad query retrieves sensitive content.
- Malicious document is written to be semantically attractive.
- Graph relationship manipulation changes retrieval result.
- Similarity scores create false confidence.

### Planned controls

- Similarity thresholds
- Retrieval comparison testing
- Trust labels
- Sensitivity labels
- Pre-retrieval authorization filtering
- Post-retrieval validation
- Graph edge trust scoring
- Retrieval evaluation metrics

### Relevant phases

- Phase 01.5: Semantic Retrieval
- Phase 01.75: GraphRAG
- Phase 02: Threat Modeling
- Phase 04: RAG Security Controls

---

## LLM09: Misinformation

### How it applies

A RAG system can produce incorrect or unsupported answers if retrieval fails, context is incomplete, retrieved chunks are misleading, or the model overstates evidence.

The lab should evaluate not just whether retrieval returns something, but whether the final answer is grounded, bounded, and traceable.

### Planned test cases

- Query with no good source match.
- Query with conflicting sources.
- Query with incomplete retrieved context.
- Query where model must admit uncertainty.
- Query where semantic retrieval returns plausible but wrong context.

### Planned controls

- Source-aware responses
- Citation enforcement
- Evidence-grounding checks
- Uncertainty handling
- Retrieval quality evaluation
- Hallucination tracking

### Relevant phases

- Phase 04: RAG Security Controls
- Phase 07: Monitoring & Evaluation

---

## LLM10: Unbounded Consumption

### How it applies

LLM applications can be abused or misconfigured in ways that cause excessive resource usage, cost, latency, or denial-of-service conditions.

For this lab, the risk is local and conceptual at first, but it becomes more realistic if external models, APIs, large document stores, or agent tools are introduced.

### Planned test cases

- Excessive top-k retrieval.
- Oversized input query.
- Oversized context window.
- Repeated expensive retrieval calls.
- Agent loops or repeated tool calls.
- Large document ingestion without limits.

### Planned controls

- Query length limits
- Chunk size limits
- Top-k limits
- Context budget enforcement
- Rate limiting
- Tool execution limits
- Cost and latency telemetry

### Relevant phases

- Phase 05: Governance & Policy
- Phase 07: Monitoring & Evaluation

---

## Implementation Guidance

The OWASP Top 10 mapping should be used as a living control map.

Each future phase should update this document with:

- implemented tests
- implemented controls
- known gaps
- relevant files
- validation commands
- findings from red-team scenarios

The project should avoid claiming complete OWASP coverage until controls and tests exist in code.

The correct claim is:

```text
AEGIS uses the OWASP Top 10 for LLM Applications as a security mapping framework for phased RAG threat modeling, adversarial testing, and control implementation.
```

---

## Current Coverage Status

| Status | Meaning |
| --- | --- |
| Implemented | Code or tests exist in the repository |
| Planned | Included in roadmap but not yet implemented |
| Partially Implemented | Some architecture exists, but security controls are incomplete |
| Documentation Only | Captured as a design/security consideration |

| OWASP ID | Current Status |
| --- | --- |
| LLM01 | Planned |
| LLM02 | Planned |
| LLM03 | Documentation Only |
| LLM04 | Planned |
| LLM05 | Planned |
| LLM06 | Planned |
| LLM07 | Planned |
| LLM08 | Partially Implemented |
| LLM09 | Planned |
| LLM10 | Planned |

---

## Notes

This mapping is intentionally conservative.

The repository should not present planned controls as implemented controls. A security roadmap is useful only if it separates current capability from future intent.
