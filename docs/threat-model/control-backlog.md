# Future Control Backlog

## Purpose

This document translates the Phase 02 threat model into a future defensive control backlog.

These controls are not implemented in Phase 02. They are captured here so later phases can implement controls based on explicit risks instead of ad hoc hardening.

## Control Backlog Summary

| ID | Control | Primary Risk Addressed | Target Phase |
| --- | --- | --- | --- |
| CTRL-001 | Pre-retrieval authorization | RAG-TM-001, SEM-TM-001 | Phase 04 |
| CTRL-002 | Document classification | RAG-TM-001, GRAPH-TM-002 | Phase 04 |
| CTRL-003 | Allowed-corpus scoping | RAG-TM-001, SEM-TM-001 | Phase 04 |
| CTRL-004 | Metadata-filtered vector search | SEM-TM-001 | Phase 04 |
| CTRL-005 | Semantic similarity threshold policy | SEM-TM-002 | Phase 04 |
| CTRL-006 | Source trust scoring | RAG-TM-002, GOV-TM-001 | Phase 04 |
| CTRL-007 | Prompt boundary enforcement | PI-TM-001 | Phase 03 / Phase 04 |
| CTRL-008 | Retrieved context sanitization | PI-TM-001 | Phase 04 |
| CTRL-009 | Output validation | PI-TM-001 | Phase 04 |
| CTRL-010 | Graph node classification | GRAPH-TM-002 | Phase 04 |
| CTRL-011 | Graph edge trust scoring | GRAPH-TM-002, GRAPH-TM-003 | Phase 04 |
| CTRL-012 | Graph traversal policy checks | GRAPH-TM-002 | Phase 04 |
| CTRL-013 | Graph alias review workflow | GRAPH-TM-001 | Phase 04 / Phase 05 |
| CTRL-014 | Poisoned document detection | RAG-TM-002 | Phase 03 / Phase 04 |
| CTRL-015 | Poisoned relationship detection | GRAPH-TM-003 | Phase 04 |
| CTRL-016 | Structured retrieval logging | OBS-TM-001 | Phase 07 |
| CTRL-017 | Incident response traceability | OBS-TM-001 | Phase 07 |
| CTRL-018 | Human approval workflow | GOV-TM-001 | Phase 05 |
| CTRL-019 | Policy enforcement engine | Multiple | Phase 05 |
| CTRL-020 | Retrieval evaluation metrics | SEM-TM-002, GRAPH-TM-001 | Phase 07 |

## CTRL-001: Pre-Retrieval Authorization

Before retrieval executes, the system should determine which documents, chunks, indexes, graph nodes, and graph edges the user is allowed to access.

This prevents retrieval from selecting unauthorized material in the first place.

## CTRL-002: Document Classification

Documents should carry sensitivity labels such as public, internal, confidential, or restricted.

Classification should influence ingestion, retrieval, graph linking, context admission, citation behavior, logging, and output handling.

## CTRL-003: Allowed-Corpus Scoping

The retrieval layer should search only the subset of documents available to the current user, role, tenant, or policy context.

This control should apply before keyword, semantic, and GraphRAG retrieval.

## CTRL-004: Metadata-Filtered Vector Search

Semantic retrieval should filter candidate chunks using metadata before similarity ranking.

Filtering only after vector search may still expose unauthorized similarity behavior or create unsafe intermediate results.

## CTRL-005: Semantic Similarity Threshold Policy

Semantic retrieval should use explicit threshold rules to prevent weak matches from entering context.

Thresholds may vary by query risk, document classification, source trust, and retrieval mode.

## CTRL-006: Source Trust Scoring

Documents and chunks should carry trust scores or trust labels.

Trusted internal policies, untrusted external content, stale documents, and quarantined documents should not be ranked or admitted equally.

## CTRL-007: Prompt Boundary Enforcement

Retrieved content should be clearly separated from trusted system and developer instructions.

The model should treat retrieved content as evidence, not as instructions.

## CTRL-008: Retrieved Context Sanitization

Retrieved chunks should be scanned or transformed before entering the prompt context.

Sanitization may remove or label instruction-like content, suspicious directives, or untrusted embedded commands.

## CTRL-009: Output Validation

Generated responses should be checked before being returned to the user.

Validation should look for unsafe disclosure, unsupported claims, policy violations, and missing citations.

## CTRL-010: Graph Node Classification

Graph nodes should carry sensitivity and trust metadata.

A node linked to confidential source material should not be traversed or returned the same way as a public node.

## CTRL-011: Graph Edge Trust Scoring

Graph edges should carry trust scores or review status.

A manually reviewed relationship should be treated differently from a newly generated, inferred, or unverified relationship.

## CTRL-012: Graph Traversal Policy Checks

Traversal should evaluate policy before following paths, not only after results are retrieved.

Policy checks should consider user role, node classification, edge trust, traversal depth, and query risk.

## CTRL-013: Graph Alias Review Workflow

Graph aliases should be reviewed because aliases decide which concepts a query or chunk can activate.

Overbroad aliases can cause unsafe retrieval paths.

## CTRL-014: Poisoned Document Detection

The system should detect documents that attempt to manipulate retrieval or generation.

This includes prompt injection text, suspicious instruction patterns, misleading authority claims, and content optimized to over-match broad queries.

## CTRL-015: Poisoned Relationship Detection

The system should detect graph relationships that appear unsafe, misleading, overbroad, or inconsistent with source evidence.

This becomes more important if future phases introduce automated graph extraction.

## CTRL-016: Structured Retrieval Logging

The system should log query text, retrieval mode, matched terms, semantic scores, graph concepts, graph paths, selected chunks, and response metadata.

Logs must be privacy-aware and should avoid storing sensitive content unnecessarily.

## CTRL-017: Incident Response Traceability

Each response should be reconstructable through a trace ID.

Investigators should be able to determine which query, documents, chunks, graph paths, and model output contributed to an incident.

## CTRL-018: Human Approval Workflow

High-risk actions or high-risk retrieved context may require human approval before response generation or release.

This is especially relevant for sensitive sources, external content, and uncertain graph traversal paths.

## CTRL-019: Policy Enforcement Engine

A policy engine should centralize allow, deny, redact, log, escalate, and require-approval decisions.

Policy decisions should be consistent across keyword, semantic, GraphRAG, agent, and tool-use phases.

## CTRL-020: Retrieval Evaluation Metrics

The project should define evaluation metrics for retrieval safety and quality.

Examples include unauthorized retrieval rate, poisoned retrieval success rate, weak-match admission rate, citation correctness, graph traversal risk, and unsafe output rate.

## Implementation Sequencing

Recommended sequencing:

1. Prompt injection lab scenarios.
2. Retrieval access control and document classification.
3. Trust scoring and context admission checks.
4. Graph node and edge controls.
5. Governance and policy engine.
6. Monitoring, telemetry, and evaluation metrics.

This keeps the project aligned with the existing phase roadmap while allowing the threat model to drive implementation decisions.
