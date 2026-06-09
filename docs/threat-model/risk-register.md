# Initial Risk Register

## Purpose

This document captures the initial Phase 02 risk register for the AEGIS RAG Security Lab.

The register maps retrieval-layer threats to affected components, retrieval modes, attack paths, qualitative impact, qualitative likelihood, overall risk, and future controls.

## Risk Rating Model

This phase uses a simple qualitative model:

| Rating | Meaning |
| --- | --- |
| Low | Limited impact or unlikely under current lab conditions. |
| Medium | Meaningful impact or plausible attack path. |
| High | Serious impact and plausible attack path. |

The ratings are intentionally lightweight. Later phases can replace this with a more formal scoring system.

## Risk Register

| ID | Threat | Affected Layer | Retrieval Mode | Attack Path | Impact | Likelihood | Risk | Future Control |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RAG-TM-001 | Unauthorized sensitive retrieval through keyword probing | Retrieval | Keyword | AP-001 | High | Medium | High | Pre-retrieval authorization and document classification |
| SEM-TM-001 | Sensitive content retrieved through semantic paraphrase | Retrieval | Semantic | AP-002 | High | Medium | High | Metadata-filtered vector search and role-aware semantic retrieval |
| SEM-TM-002 | Weak semantic matches admitted into context | Retrieval | Semantic | AP-003 | Medium | Medium | Medium | Similarity threshold policy and retrieval quality evaluation |
| RAG-TM-002 | Poisoned source document influences generated answer | Ingestion / Retrieval / Generation | All modes | AP-004 | High | Medium | High | Source approval, document trust scoring, and poisoning checks |
| PI-TM-001 | Retrieved content contains indirect prompt injection | Context / Generation | All modes | AP-005 | High | Medium | High | Prompt boundary enforcement and context sanitization |
| GRAPH-TM-001 | Misleading graph alias match starts unsafe traversal | GraphRAG | GraphRAG | AP-006 | Medium | Medium | Medium | Alias review and concept match confidence scoring |
| GRAPH-TM-002 | Graph traversal exposes sensitive connected concepts | GraphRAG | GraphRAG | AP-007 | High | Medium | High | Node classification, edge trust, and traversal authorization |
| GRAPH-TM-003 | Poisoned or incorrect graph relationship distorts retrieval | GraphRAG | GraphRAG | AP-008 | High | Low | Medium | Edge trust scoring and relationship review workflow |
| GOV-TM-001 | Untrusted content treated as trusted source material | Governance / Retrieval | All modes | AP-009 | High | Medium | High | Source trust labels and trust-aware ranking |
| OBS-TM-001 | Unsafe retrieval cannot be reconstructed after incident | Monitoring / IR | All modes | AP-010 | Medium | High | High | Structured retrieval logging and incident traceability |

## Risk Details

### RAG-TM-001: Unauthorized Sensitive Retrieval Through Keyword Probing

A user can submit direct sensitive terms and retrieve chunks containing protected material because retrieval currently operates without authentication, role context, document classification, or allowed-corpus scoping.

Future controls should enforce authorization before retrieval executes.

### SEM-TM-001: Sensitive Content Retrieved Through Semantic Paraphrase

Semantic retrieval can return sensitive content based on meaning rather than exact terms. This creates a different leakage path than keyword probing because a user does not need to know the exact sensitive vocabulary.

Future controls should combine metadata-filtered vector search with post-retrieval context admission checks.

### SEM-TM-002: Weak Semantic Matches Admitted Into Context

If similarity thresholds are too low, semantic retrieval may return weakly related chunks. These chunks can create noisy, misleading, or unsafe generated responses.

Future controls should define similarity thresholds, retrieval quality metrics, and relevance evaluation tests.

### RAG-TM-002: Poisoned Source Document Influences Generated Answer

A malicious or misleading source document can enter the knowledge base and be retrieved by any retrieval mode. Without source approval or trust scoring, the system has no basis for treating the content as suspicious.

Future controls should introduce document lifecycle state, trust labels, and quarantine workflows.

### PI-TM-001: Retrieved Content Contains Indirect Prompt Injection

A retrieved chunk can contain text that attempts to instruct or override model behavior. The current mock generator is local and deterministic, but a future real LLM integration would need strict prompt boundary separation.

Future controls should separate trusted instructions from untrusted retrieved content and validate outputs before returning them.

### GRAPH-TM-001: Misleading Graph Alias Match Starts Unsafe Traversal

GraphRAG starts traversal from query-matched concepts. If aliases are too broad or misleading, retrieval can start from the wrong concept and return inappropriate context.

Future controls should review aliases, score concept match confidence, and evaluate graph retrieval quality.

### GRAPH-TM-002: Graph Traversal Exposes Sensitive Connected Concepts

Graph traversal can reach concepts that were not directly requested by the user. If those concepts or their linked chunks are sensitive, relationship-aware retrieval can broaden exposure.

Future controls should apply policy checks to graph nodes, edges, and traversal paths.

### GRAPH-TM-003: Poisoned or Incorrect Graph Relationship Distorts Retrieval

Incorrect relationships can make unsafe or irrelevant retrieval paths look legitimate. Even manually defined graphs can drift or encode bad assumptions.

Future controls should add edge trust scoring, graph change review, and relationship-level auditability.

### GOV-TM-001: Untrusted Content Treated as Trusted Source Material

Without source trust labels, all documents are treated equally during retrieval and citation. This can allow weak or untrusted material to influence answers.

Future controls should add source trust labeling and trust-aware ranking.

### OBS-TM-001: Unsafe Retrieval Cannot Be Reconstructed After Incident

The system currently lacks structured audit telemetry. If unsafe retrieval occurs, the project cannot reconstruct the query, matched terms, semantic scores, graph paths, retrieved chunks, or generated output as an incident record.

Future controls should add trace IDs, structured retrieval logs, and incident response workflows.
