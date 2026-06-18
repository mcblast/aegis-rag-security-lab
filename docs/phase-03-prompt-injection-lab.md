# Phase 03 - Prompt Injection and Poisoned Retrieval Lab

## Purpose

Phase 03 turns the Phase 02 threat model into concrete synthetic retrieval-risk scenarios.

This phase defines a small adversarial corpus and a scenario registry that later scripts and tests can run across keyword retrieval, semantic retrieval, and local GraphRAG retrieval.

The goal is to make baseline risk visible before Phase 04 adds controls.

## Scope

This first Phase 03 slice adds only:

- Synthetic knowledge base documents under `data/knowledge_base/adversarial/`.
- Scenario definitions in `redteam/attack_scenarios.py`.
- This Phase 03 documentation file.

This slice does not add runners, tests, telemetry, or defensive controls.

## Phase Boundary

Phase 03 is a demonstration phase, not a hardening phase.

It does not implement authentication, access control, document classification enforcement, source trust scoring, context sanitization, output validation, logging, or policy enforcement.

Those controls belong in Phase 04 and later phases.

## Adversarial Corpus

The Phase 03 corpus lives in:

```text
data/knowledge_base/adversarial/
```

Current files:

| Document | Purpose | Related Attack Paths |
| --- | --- | --- |
| `poisoned-policy-update.md` | Models policy-shaped untrusted source material. | AP-004, AP-009 |
| `indirect-prompt-injection-note.md` | Models instruction-like retrieved content using safe marker language. | AP-005, AP-009 |
| `misleading-source-authority.md` | Models confident but unreviewed source material. | AP-004, AP-009 |
| `graph-ambiguity-note.md` | Models relationship-heavy content for GraphRAG comparison. | AP-006, AP-007, AP-008 |
| `context-decoy.md` | Provides a neutral retrieval comparison target. | AP-001, AP-002, AP-007 |

All documents are fictional lab artifacts.

## Scenario Registry

Phase 03 scenarios are defined in:

```text
redteam/attack_scenarios.py
```

Each scenario records:

- Scenario ID.
- Title.
- Query.
- Related attack path IDs.
- Expected risky source files.
- Expected baseline behavior.
- Retrieval modes covered.

The registry does not execute retrieval and does not implement controls. It provides stable metadata for later Phase 03 scripts and tests.

## Current Scenario IDs

| Scenario ID | Focus |
| --- | --- |
| `P3-POISON-001` | Policy-shaped source retrieval. |
| `P3-PI-001` | Instruction-like content reaching retrieved context. |
| `P3-TRUST-001` | Unreviewed source treated like ordinary source material. |
| `P3-GRAPH-001` | GraphRAG surfacing relationship-heavy context. |
| `P3-CONTEXT-001` | Synthetic context decoy entering retrieved context. |

## Expected Baseline Behavior

The current baseline has no approval workflow, source trust scoring, prompt boundary enforcement, context review, graph traversal policy, or output validation.

Because of that, Phase 03 expects some scenarios to show that synthetic corpus files can be retrieved and included in mock generated responses.

This is intentional. Phase 03 documents and demonstrates baseline behavior so Phase 04 can later show measurable improvement.

## Next Phase 03 Work

The next implementation slice should add a runner that executes the registered scenarios across:

- Keyword retrieval.
- Semantic retrieval.
- GraphRAG retrieval.

The runner should show which source files were retrieved and whether each scenario surfaced the expected files.

After that, Phase 03 should add tests that preserve the current baseline behavior so future controls have something clear to improve.

## Phase 04 Handoff

Phase 04 should use these scenarios as regression targets for defensive controls.

Expected future improvements include source labeling, context admission checks, clearer prompt boundaries, graph traversal policy, and output validation.
