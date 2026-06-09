# Initial Attack Paths

## Purpose

This document captures the initial attack paths considered in the Phase 02 threat model.

These attack paths are defensive analysis artifacts. They describe how the current architecture could fail so later phases can implement targeted controls.

## Attack Path Summary

| ID | Attack Path | Retrieval Mode | Primary Risk |
| --- | --- | --- | --- |
| AP-001 | Keyword probing for sensitive chunks | Keyword | Direct discovery of protected content. |
| AP-002 | Semantic paraphrase retrieval | Semantic | Sensitive content retrieved without exact sensitive terms. |
| AP-003 | Overbroad semantic retrieval | Semantic | Weak matches admitted as context. |
| AP-004 | Poisoned source document retrieval | All modes | Malicious or misleading content enters generated answers. |
| AP-005 | Indirect prompt injection through retrieved content | All modes | Retrieved content attempts to influence model behavior. |
| AP-006 | Graph concept alias abuse | GraphRAG | Query or document text triggers unsafe concept matches. |
| AP-007 | Graph traversal exposure | GraphRAG | Traversal reaches sensitive connected concepts. |
| AP-008 | Poisoned graph relationship path | GraphRAG | Incorrect relationships distort retrieval. |
| AP-009 | Missing source trust validation | All modes | Untrusted content is treated like trusted content. |
| AP-010 | Missing auditability | All modes | Incidents cannot be reconstructed after unsafe retrieval. |

## AP-001: Keyword Probing for Sensitive Chunks

### Scenario

A user submits queries containing sensitive terms such as confidential, private, internal, source material, or authorization.

### Current System Behavior

Keyword retrieval searches all available chunks and scores exact term overlap.

### Security Concern

If sensitive chunks exist in the knowledge base, direct keyword probing can retrieve them because no role-aware or classification-aware filter runs before retrieval.

### Future Controls

- Pre-retrieval authorization.
- Document classification.
- Allowed-corpus scoping.
- Sensitive-term query risk scoring.

## AP-002: Semantic Paraphrase Retrieval

### Scenario

A user avoids exact sensitive terms but asks semantically related questions, such as asking who can view private knowledge sources without using a protected document title.

### Current System Behavior

Semantic retrieval embeds the query and compares it against embedded chunks.

### Security Concern

Semantic retrieval can surface sensitive content through meaning rather than exact keyword overlap.

### Future Controls

- Metadata-filtered vector search.
- Role-aware semantic retrieval.
- Sensitivity-aware similarity thresholds.
- Post-retrieval context admission checks.

## AP-003: Overbroad Semantic Retrieval

### Scenario

A query retrieves weakly related chunks because top-k is high or minimum similarity is low.

### Current System Behavior

Semantic retrieval can return multiple chunks even when some matches are weak unless a useful minimum similarity threshold is configured.

### Security Concern

Weakly related context can mislead the generated response or pull in unrelated sensitive content.

### Future Controls

- Tuned semantic thresholds.
- Retrieval quality evaluation.
- Query-specific threshold policy.
- Relevance validation before context admission.

## AP-004: Poisoned Source Document Retrieval

### Scenario

A local knowledge base document contains misleading, hostile, or maliciously crafted content.

### Current System Behavior

The ingestion layer loads local documents without trust scoring, approval state, or poisoning checks.

### Security Concern

Poisoned content can be retrieved by keyword, semantic, or graph retrieval and then included in generated answers.

### Future Controls

- Source approval workflow.
- Document trust scoring.
- Poisoned document detection.
- Quarantine and re-index workflow.

## AP-005: Indirect Prompt Injection Through Retrieved Content

### Scenario

A document contains instructions that attempt to override system behavior when retrieved as context.

### Current System Behavior

Retrieved chunks are passed toward generation without prompt boundary enforcement or context sanitization.

### Security Concern

A future real LLM integration could treat malicious retrieved text as instructions rather than untrusted evidence.

### Future Controls

- Prompt boundary separation.
- Retrieved content labeling.
- Context sanitization.
- Instruction hierarchy enforcement.
- Output validation.

## AP-006: Graph Concept Alias Abuse

### Scenario

A query or document includes terms that match graph aliases in a misleading way.

### Current System Behavior

GraphRAG matches aliases deterministically and uses matched concepts as traversal start points.

### Security Concern

A misleading alias match can start traversal from the wrong concept and retrieve irrelevant, unsafe, or sensitive chunks.

### Future Controls

- Alias review process.
- Concept match confidence scoring.
- Node classification labels.
- Human-reviewable graph changes.

## AP-007: Graph Traversal Exposure

### Scenario

A user query matches a non-sensitive concept, but graph traversal reaches connected sensitive concepts.

### Current System Behavior

Graph traversal follows directed relationships up to the configured maximum depth.

### Security Concern

Relationship-aware retrieval can expose sensitive connected concepts even when the direct query appears low risk.

### Future Controls

- Traversal authorization checks.
- Node sensitivity labels.
- Edge trust scores.
- Depth limits by query risk.
- Path-level policy checks.

## AP-008: Poisoned Graph Relationship Path

### Scenario

A graph relationship incorrectly links a benign concept to a sensitive or misleading concept.

### Current System Behavior

Graph relationships are manually defined and trusted by traversal logic.

### Security Concern

Incorrect relationships can distort retrieval by making unsafe paths look legitimate.

### Future Controls

- Edge trust scoring.
- Relationship review workflow.
- Graph change auditing.
- Poisoned relationship detection.

## AP-009: Missing Source Trust Validation

### Scenario

Trusted and untrusted documents are both available to retrieval without distinction.

### Current System Behavior

The current system does not label sources by trust level.

### Security Concern

Generated answers can treat untrusted content as equally authoritative as trusted content.

### Future Controls

- Source trust labels.
- Trust-aware ranking.
- Trust-aware citation display.
- Context admission policy.

## AP-010: Missing Auditability

### Scenario

The system returns unsafe, sensitive, or misleading output, but no structured record exists showing why.

### Current System Behavior

The current system returns source-aware answers but does not produce audit telemetry.

### Security Concern

Without query, retrieval, source, graph path, and response records, incidents cannot be investigated or remediated reliably.

### Future Controls

- Structured retrieval logging.
- Query and response trace IDs.
- Graph traversal path logging.
- Incident response workflow.
- Evaluation and monitoring dashboards.
