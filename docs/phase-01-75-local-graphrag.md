# Phase 01.75 - Local GraphRAG Retrieval

## Purpose

Phase 01.75 adds a lightweight local GraphRAG retrieval path beside the existing keyword and semantic retrieval modes.

The goal is not to introduce a production graph database or a heavy GraphRAG framework. The goal is to make relationship-aware retrieval visible, testable, and explainable before Phase 02 threat modeling begins.

This phase allows the project to compare three retrieval paradigms:

```text
Keyword retrieval   -> What exact terms matched?
Semantic retrieval  -> What meaning is closest?
GraphRAG retrieval  -> What concepts and relationships connect the answer?
```

## Design Constraints

Phase 01.75 intentionally stays:

- Local
- Deterministic
- Dependency-light
- Inspectable
- Source-aware
- Compatible with the existing mock LLM layer

This phase does not use:

- External graph databases
- LLM-based entity extraction
- Managed graph services
- Heavy GraphRAG frameworks
- Real authorization or policy enforcement controls

Those exclusions are deliberate. The graph layer should be easy to inspect before security controls and adversarial test cases are added.

## Architecture Flow

```text
Local Markdown/Text Documents
 ↓
Document Ingestion
 ↓
Chunking With Source Metadata
 ↓
Rules-Based Concept Matching
 ↓
Local Knowledge Graph Construction
 ↓
Graph Traversal / Relationship Search
 ↓
Related Concepts + Source Chunks
 ↓
Mock LLM Response Generation
 ↓
Source-Aware Answer
```

## Implemented Components

| Component | File | Purpose |
| --- | --- | --- |
| Graph model | `app/graph_model.py` | Defines graph nodes, edges, chunk links, traversal paths, and the local in-memory graph. |
| Graph builder | `app/graph_builder.py` | Defines deterministic concepts, aliases, relationships, and chunk-to-concept links. |
| Graph retriever | `app/graph_retrieval.py` | Finds query concepts, traverses relationships, and returns graph-linked chunks. |
| GraphRAG pipeline | `app/graphrag_pipeline.py` | Runs ingestion, chunking, graph retrieval, and mock generation. |
| GraphRAG CLI | `scripts/run_graphrag.py` | Runs local GraphRAG queries from the terminal. |
| All-mode comparison CLI | `scripts/compare_all_retrieval_modes.py` | Compares keyword, semantic, and GraphRAG retrieval for the same query. |
| GraphRAG tests | `tests/test_graphrag_retrieval.py` | Validates concept matching, graph construction, traversal, retrieval, and pipeline behavior. |

## Local Graph Model

The local graph uses explicit graph nodes and directed edges.

Example node categories include:

- Prompt injection
- Indirect prompt injection
- Model behavior
- Retrieval layer
- External content
- Confidential source material
- Access control failure
- Sensitive data leakage
- Incident response
- Retrieved context
- Model responses
- Graph traversal

Example relationships include:

```text
prompt_injection          --manipulates--> model_behavior
indirect_prompt_injection --enters_through--> external_content
external_content          --flows_into--> retrieval_layer
retrieval_layer           --selects--> retrieved_context
retrieval_layer           --can_expose--> confidential_source_material
access_control_failure    --causes--> sensitive_data_leakage
sensitive_data_leakage    --involves--> confidential_source_material
incident_response         --preserves--> retrieved_context
incident_response         --preserves--> model_responses
graph_traversal           --connects--> retrieved_context
graph_traversal           --can_surface--> confidential_source_material
```

## Retrieval Behavior

GraphRAG retrieval follows this sequence:

1. Match the user query against known concept aliases.
2. Start traversal from the matched graph concepts.
3. Traverse directed graph relationships up to a configurable depth.
4. Collect chunks linked to reached concepts.
5. Score chunks based on direct concept matches, connected relationship matches, and matched alias terms.
6. Return ranked graph retrieval results with explainable concept and path metadata.

The graph result object includes:

- Source chunk
- Graph score
- Matched concepts
- Matched terms
- Relationship paths used to explain traversal

## Example Commands

Run GraphRAG directly:

```bash
PYTHONPATH=. python scripts/run_graphrag.py "How can retrieval expose confidential source material?"
```

Compare all retrieval modes:

```bash
PYTHONPATH=. python scripts/compare_all_retrieval_modes.py "How can documents manipulate model behavior?"
```

Run tests:

```bash
pytest
```

## Security Questions Introduced

GraphRAG expands the retrieval attack surface. Phase 02 should evaluate questions such as:

- Can a poisoned document create misleading graph relationships?
- Can incorrect concept mapping distort retrieval behavior?
- Can graph traversal expose sensitive connected concepts?
- Should graph nodes and edges carry trust scores?
- Should graph nodes inherit document classification labels?
- Can attackers manipulate graph paths instead of only chunk text?
- How should graph retrieval be evaluated against keyword and semantic retrieval?

## Current Limitations

The current GraphRAG implementation is intentionally simple.

Known limitations:

- Concept extraction is rules-based and alias-driven.
- Relationships are manually defined.
- Traversal is directed and shallow.
- No graph node trust scoring exists yet.
- No graph edge trust scoring exists yet.
- No document classification is inherited by graph nodes.
- No authorization filter is applied before graph traversal.
- No poisoned relationship detection exists yet.

These are not bugs. They define the attack surface for threat modeling and later hardening phases.

## Phase Boundary

Phase 01.75 adds relationship-aware retrieval only.

It does not add:

- Authentication
- Role-aware retrieval
- Document-level authorization
- Prompt injection detection
- Context sanitization
- Output validation
- Audit telemetry
- Policy enforcement

Those controls belong in later phases after the retrieval surfaces are fully visible.
