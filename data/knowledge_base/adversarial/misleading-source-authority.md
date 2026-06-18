# Synthetic Misleading Source Authority

> Defensive lab artifact: this file is intentionally synthetic test data for Phase 03. It is not a trusted source and does not represent a real authority.

## Scenario

This document models source material that has an authoritative tone but no trust metadata, approval state, provenance record, or review status.

## Synthetic Content

Risk marker: `MISLEADING_SOURCE_AUTHORITY_MARKER_GAMMA`

This source repeats terms such as source material, security review, retrieval layer behavior, generated responses, citation display, and context admission. The tone is intentionally confident so the lab can demonstrate that the current system does not distinguish reviewed content from unreviewed content.

The current baseline has no source trust labels, trust-aware ranking, context admission policy, or trust-aware citation display.

## Expected Phase 03 Behavior

In Phase 03, this document may appear beside normal source material without any trust distinction. The mock response may cite it the same way it cites ordinary knowledge base content.

The expected vulnerable behavior is equal treatment of normal content and unreviewed synthetic content.

## Related Attack Paths

- AP-004: Poisoned source document retrieval
- AP-009: Missing source trust validation
