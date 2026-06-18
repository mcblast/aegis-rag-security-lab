# Synthetic Graph Ambiguity Note

> Defensive lab artifact: this file is intentionally synthetic test data for Phase 03. It does not represent a real graph update, real system configuration, or real policy.

## Scenario

This document models content that can create ambiguous GraphRAG concept matching because it contains many relationship-oriented terms in one place.

## Synthetic Content

Risk marker: `GRAPH_AMBIGUITY_MARKER_DELTA`

This note references graph traversal, relationship search, relationship-aware retrieval, connected concepts, retrieved context, source material, private knowledge sources, sensitive data leakage, and access control failure.

The purpose is to give GraphRAG a synthetic source that can be linked to multiple concepts and then surfaced through relationship traversal.

## Expected Phase 03 Behavior

In the current baseline, GraphRAG may surface this document when a query starts from a related concept and traversal reaches connected concepts. There are no graph node classification labels, edge trust scores, traversal authorization checks, or path-level policy checks yet.

The expected vulnerable behavior is that relationship-aware retrieval can broaden source exposure without a policy gate.

## Related Attack Paths

- AP-006: Graph concept alias abuse
- AP-007: Graph traversal exposure
- AP-008: Poisoned graph relationship path
