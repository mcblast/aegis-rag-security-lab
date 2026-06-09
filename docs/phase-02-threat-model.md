# Phase 02 - Threat Modeling

## Purpose

Phase 02 defines the initial threat model for the AEGIS RAG Security Lab.

The purpose of this phase is to analyze the security risks created by the current retrieval architecture before implementing defensive controls. The project now contains three retrieval modes: keyword retrieval, semantic retrieval, and local GraphRAG retrieval. Each mode exposes different failure modes, trust assumptions, and attack paths.

This phase turns those risks into an explicit architecture artifact.

## Scope

Phase 02 covers threat modeling only.

It evaluates:

- The current keyword retrieval baseline.
- The current semantic retrieval pipeline.
- The current local GraphRAG retrieval path.
- The trust boundaries around ingestion, chunking, retrieval, graph traversal, context construction, mock response generation, and source-aware output.
- The risks created by missing authorization, classification, trust scoring, prompt boundary enforcement, telemetry, and policy controls.

## Current System Context

The current system is intentionally local, deterministic, and inspectable. It uses local Markdown and text documents, chunks them with source metadata, retrieves relevant chunks through one or more retrieval modes, and generates source-aware mock responses.

The system does not currently enforce real authentication, role-aware retrieval, document classification, trust scoring, prompt injection detection, context sanitization, output validation, audit logging, or policy enforcement.

Those missing controls are not treated as implementation defects in this phase. They define the attack surface to be analyzed.

## Retrieval Modes Covered

### Keyword Retrieval

Keyword retrieval exposes exact term matching behavior. It is transparent and easy to inspect, but it can leak sensitive content when users probe for protected terms or when retrieval is not scoped by role or document classification.

### Semantic Retrieval

Semantic retrieval uses deterministic local embeddings and similarity scoring. It can retrieve relevant context even when exact keywords are absent, but it also introduces ambiguity, threshold tuning risk, and semantically close but incorrect retrieval.

### GraphRAG Retrieval

GraphRAG retrieval uses concept matching and graph traversal to return chunks linked to related security concepts. It makes relationship-aware retrieval visible, but it also introduces graph-specific risks such as poisoned relationships, unsafe traversal, concept alias abuse, and missing node or edge trust scoring.

## Assets

The threat model evaluates the assets documented in:

```text
docs/threat-model/assets.md
```

## Trust Boundaries

The trust boundaries are documented in:

```text
docs/threat-model/trust-boundaries.md
```

## Data Flows

The main data flow is:

```text
User query
  -> query handling
  -> retrieval mode selection
  -> document/chunk retrieval
  -> retrieved context
  -> mock LLM response generation
  -> source-aware answer
```

The GraphRAG-specific flow adds:

```text
User query
  -> concept matching
  -> graph traversal
  -> graph-linked chunk retrieval
  -> relationship-aware retrieved context
```

## Threat Surface Summary

The main threat surfaces are:

- User-controlled queries.
- Local knowledge base content.
- Chunking and source metadata.
- Keyword matching logic.
- Embedding and semantic similarity behavior.
- Graph concepts, aliases, edges, and traversal depth.
- Retrieved context passed toward generation.
- Source-aware generated responses.
- Missing authorization and policy gates.
- Missing telemetry and incident response evidence.

## Initial Attack Paths

Initial attack paths are documented in:

```text
docs/threat-model/attack-paths.md
```

## Risk Register Summary

The initial risk register is documented in:

```text
docs/threat-model/risk-register.md
```

## Future Control Backlog

The future control backlog is documented in:

```text
docs/threat-model/control-backlog.md
```

## Phase Boundary

Phase 02 does not implement security controls.

This phase does not add:

- Authentication.
- Role-based access control.
- Document-level authorization.
- Document classification.
- Trust scoring.
- Prompt injection detection.
- Context sanitization.
- Output validation.
- Audit logging.
- Policy enforcement.

Those controls belong in later implementation phases after the threat model defines why each control is needed.

## Acceptance Criteria

Phase 02 is complete when:

- The system assets are documented.
- Trust boundaries are documented.
- Initial data flows are documented.
- Retrieval-specific attack paths are documented.
- A risk register exists for keyword, semantic, and GraphRAG retrieval risks.
- A future control backlog maps risks to planned defensive controls.
- The README accurately reflects Phase 02 status.
