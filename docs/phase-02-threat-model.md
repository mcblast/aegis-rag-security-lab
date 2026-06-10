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

## Phase 02 Documentation Map

| Document | Purpose |
| --- | --- |
| [Assets](threat-model/assets.md) | Identifies user, query, knowledge base, chunking, retrieval, graph, output, and operational evidence assets. |
| [Trust Boundaries](threat-model/trust-boundaries.md) | Maps where data crosses actors, assumptions, components, and privilege levels. |
| [Attack Paths](threat-model/attack-paths.md) | Captures initial defensive attack paths for keyword, semantic, GraphRAG, poisoning, prompt injection, and auditability risks. |
| [Risk Register](threat-model/risk-register.md) | Maps threats to affected layers, retrieval modes, attack paths, impact, likelihood, risk, and future controls. |
| [Control Backlog](threat-model/control-backlog.md) | Maps the threat model to later defensive controls and implementation sequencing. |

## Assets

The threat model evaluates the assets documented in [docs/threat-model/assets.md](threat-model/assets.md).

## Trust Boundaries

The trust boundaries are documented in [docs/threat-model/trust-boundaries.md](threat-model/trust-boundaries.md).

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

Initial attack paths are documented in [docs/threat-model/attack-paths.md](threat-model/attack-paths.md).

## Threat-to-Boundary Mapping

This mapping connects the [attack paths](threat-model/attack-paths.md), [trust boundaries](threat-model/trust-boundaries.md), [risk register](threat-model/risk-register.md), and [future control backlog](threat-model/control-backlog.md). It is intended to show where each future control should be placed in the architecture.

| Threat / Risk | Attack Path | Primary Trust Boundary | Control Placement Candidate | Future Controls |
| --- | --- | --- | --- | --- |
| Unauthorized sensitive retrieval through keyword probing | AP-001 | TB-001, TB-004, TB-008 | Before keyword retrieval executes | CTRL-001, CTRL-002, CTRL-003 |
| Sensitive content retrieved through semantic paraphrase | AP-002 | TB-001, TB-005, TB-008 | Before semantic retrieval and before context admission | CTRL-001, CTRL-003, CTRL-004 |
| Weak semantic matches admitted into context | AP-003 | TB-005, TB-008 | Semantic thresholding and context admission | CTRL-005, CTRL-020 |
| Poisoned source document influences generated answer | AP-004 | TB-002, TB-008, TB-009 | Knowledge base ingestion and context admission | CTRL-006, CTRL-014, CTRL-018 |
| Retrieved content contains indirect prompt injection | AP-005 | TB-008, TB-009, TB-010 | Prompt construction and output validation | CTRL-007, CTRL-008, CTRL-009 |
| Misleading graph alias match starts unsafe traversal | AP-006 | TB-006, TB-007 | Graph construction, alias review, and traversal start-node selection | CTRL-010, CTRL-013, CTRL-020 |
| Graph traversal exposes sensitive connected concepts | AP-007 | TB-007, TB-008 | Before graph traversal expands related concepts | CTRL-010, CTRL-011, CTRL-012 |
| Poisoned or incorrect graph relationship distorts retrieval | AP-008 | TB-006, TB-007 | Graph edge review and traversal policy | CTRL-011, CTRL-015 |
| Untrusted content treated as trusted source material | AP-009 | TB-002, TB-008, TB-010 | Source scoring, ranking, context admission, and citation display | CTRL-006, CTRL-018, CTRL-019 |
| Unsafe retrieval cannot be reconstructed after incident | AP-010 | TB-008, TB-009, TB-010 | Query, retrieval, graph path, response, and policy logging | CTRL-016, CTRL-017, CTRL-020 |

## Attacker Personas

The current system is local and educational, but the threat model uses enterprise-style attacker personas so later phases can evolve toward realistic security controls.

| Persona | Description | Likely Goal | Relevant Risks |
| --- | --- | --- | --- |
| Curious low-privilege user | A user with limited or no role context who probes the system through natural-language queries. | Discover sensitive chunks or source names. | RAG-TM-001, SEM-TM-001, GRAPH-TM-002 |
| Malicious authenticated user | A user who has legitimate access to some corpus content but attempts to retrieve material outside their authorization scope. | Bypass allowed-corpus boundaries. | RAG-TM-001, SEM-TM-001, GOV-TM-001 |
| Poisoned document contributor | A user, process, or future ingestion source that can introduce misleading or malicious documents into the knowledge base. | Manipulate retrieval or generated answers. | RAG-TM-002, PI-TM-001, GOV-TM-001 |
| Graph manipulator | A user, maintainer mistake, or future automated extraction process that introduces bad aliases, nodes, or edges. | Distort traversal and surface unsafe context. | GRAPH-TM-001, GRAPH-TM-002, GRAPH-TM-003 |
| Incident responder / investigator | A defensive operator who must reconstruct unsafe retrieval or output after the fact. | Determine what happened and which evidence contributed. | OBS-TM-001 |

## Abuse Cases

These abuse cases turn the abstract attack paths into concrete system behaviors that can be demonstrated in later phases.

### Abuse Case 1: Direct Keyword Probing

A low-privilege user asks for documents containing terms such as `confidential`, `private`, or `internal`. Because all chunks are currently searchable, keyword retrieval may return sensitive chunks without checking role, classification, or allowed corpus.

Related artifacts: [AP-001](threat-model/attack-paths.md#ap-001-keyword-probing-for-sensitive-chunks), [RAG-TM-001](threat-model/risk-register.md#rag-tm-001-unauthorized-sensitive-retrieval-through-keyword-probing), [CTRL-001](threat-model/control-backlog.md#ctrl-001-pre-retrieval-authorization).

### Abuse Case 2: Semantic Paraphrase Leakage

A user avoids exact sensitive words and asks a semantically related question such as `Who can view private knowledge sources?`. Semantic retrieval may return protected material based on meaning instead of exact token overlap.

Related artifacts: [AP-002](threat-model/attack-paths.md#ap-002-semantic-paraphrase-retrieval), [SEM-TM-001](threat-model/risk-register.md#sem-tm-001-sensitive-content-retrieved-through-semantic-paraphrase), [CTRL-004](threat-model/control-backlog.md#ctrl-004-metadata-filtered-vector-search).

### Abuse Case 3: Poisoned Document Injection

A document in the local knowledge base contains misleading authority claims or instruction-like text. The current ingestion layer loads it without approval state, trust score, quarantine state, or poisoning checks, allowing any retrieval mode to surface it.

Related artifacts: [AP-004](threat-model/attack-paths.md#ap-004-poisoned-source-document-retrieval), [RAG-TM-002](threat-model/risk-register.md#rag-tm-002-poisoned-source-document-influences-generated-answer), [CTRL-014](threat-model/control-backlog.md#ctrl-014-poisoned-document-detection).

### Abuse Case 4: Indirect Prompt Injection Through Retrieved Context

A retrieved chunk contains text that attempts to instruct a future real LLM. Without prompt boundary enforcement, context sanitization, and output validation, the generation layer may treat untrusted retrieved content as instructions instead of evidence.

Related artifacts: [AP-005](threat-model/attack-paths.md#ap-005-indirect-prompt-injection-through-retrieved-content), [PI-TM-001](threat-model/risk-register.md#pi-tm-001-retrieved-content-contains-indirect-prompt-injection), [CTRL-007](threat-model/control-backlog.md#ctrl-007-prompt-boundary-enforcement).

### Abuse Case 5: Graph Traversal Exposure

A query matches a non-sensitive graph concept, but traversal follows relationships into a sensitive connected concept. Without node classification, edge trust, traversal authorization, and path-level policy checks, GraphRAG may broaden exposure beyond the user's direct request.

Related artifacts: [AP-007](threat-model/attack-paths.md#ap-007-graph-traversal-exposure), [GRAPH-TM-002](threat-model/risk-register.md#graph-tm-002-graph-traversal-exposes-sensitive-connected-concepts), [CTRL-012](threat-model/control-backlog.md#ctrl-012-graph-traversal-policy-checks).

### Abuse Case 6: Missing Audit Trail After Unsafe Output

The system returns unsafe or misleading output, but no structured trace records the query, retrieval mode, matched terms, semantic scores, graph paths, selected chunks, or response metadata. The incident cannot be reconstructed reliably.

Related artifacts: [AP-010](threat-model/attack-paths.md#ap-010-missing-auditability), [OBS-TM-001](threat-model/risk-register.md#obs-tm-001-unsafe-retrieval-cannot-be-reconstructed-after-incident), [CTRL-016](threat-model/control-backlog.md#ctrl-016-structured-retrieval-logging).

## Control Placement Diagram

The threat model identifies where future controls should sit. Controls should be placed before unsafe data crosses the next trust boundary, not only after retrieval has already happened.

```text
User Query
  |
  v
[Query Handling]
  |  CTRL-001 Pre-retrieval authorization
  |  CTRL-003 Allowed-corpus scoping
  v
[Retrieval Mode Selection]
  |
  +--> [Keyword Retrieval]
  |       CTRL-002 Document classification
  |
  +--> [Semantic Retrieval]
  |       CTRL-004 Metadata-filtered vector search
  |       CTRL-005 Similarity threshold policy
  |
  +--> [GraphRAG Retrieval]
          CTRL-010 Graph node classification
          CTRL-011 Graph edge trust scoring
          CTRL-012 Graph traversal policy checks

Retrieved Chunks / Graph Paths
  |
  v
[Context Admission]
  |  CTRL-006 Source trust scoring
  |  CTRL-008 Retrieved context sanitization
  v
[Prompt Construction]
  |  CTRL-007 Prompt boundary enforcement
  v
[Generation]
  |
  v
[Output Validation]
  |  CTRL-009 Output validation
  v
[Response]
  |
  v
[Telemetry / Investigation]
     CTRL-016 Structured retrieval logging
     CTRL-017 Incident response traceability
     CTRL-020 Retrieval evaluation metrics
```

## Risk Register Summary

The initial risk register is documented in [docs/threat-model/risk-register.md](threat-model/risk-register.md).

## Future Control Backlog

The future control backlog is documented in [docs/threat-model/control-backlog.md](threat-model/control-backlog.md).

## Phase 3 Handoff

Phase 03 should turn the Phase 02 threat model into executable attack demonstrations before defensive controls are implemented.

The recommended Phase 03 scope is:

1. Add poisoned and adversarial knowledge base documents that exercise [AP-004](threat-model/attack-paths.md#ap-004-poisoned-source-document-retrieval) and [AP-005](threat-model/attack-paths.md#ap-005-indirect-prompt-injection-through-retrieved-content).
2. Add comparison scripts or tests showing how keyword, semantic, and GraphRAG retrieval surface unsafe context differently.
3. Add expected vulnerable behavior tests so later phases can prove that controls reduce unauthorized retrieval, poisoned retrieval, unsafe context admission, and graph traversal exposure.

Phase 03 should remain an attack lab. It should demonstrate failure modes clearly without prematurely adding the controls reserved for later phases.

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
- Threat-to-boundary mapping exists across attack paths, trust boundaries, risks, and controls.
- Attacker personas and abuse cases are documented.
- A risk register exists for keyword, semantic, and GraphRAG retrieval risks.
- A future control backlog maps risks to planned defensive controls.
- The README accurately reflects Phase 02 status and the next planned implementation steps.
