# Threat Model Trust Boundaries

## Purpose

This document identifies the main trust boundaries considered in the Phase 02 threat model.

A trust boundary is any point where data crosses between actors, components, assumptions, or privilege levels. These boundaries matter because the current system does not yet enforce authorization, document classification, trust scoring, prompt boundary controls, telemetry, or policy decisions.

## Boundary Summary

| ID | Boundary | Description | Primary Risk |
| --- | --- | --- | --- |
| TB-001 | User input -> query handling | A user-controlled query enters the system. | Malicious or probing input can steer retrieval. |
| TB-002 | Knowledge base -> ingestion | Local source documents are loaded into the system. | Untrusted, stale, or poisoned documents can enter retrieval. |
| TB-003 | Documents -> chunks | Full documents are split into retrieval units. | Chunking can mix sensitive and non-sensitive content. |
| TB-004 | Chunks -> keyword retrieval | Chunks become searchable through exact term matching. | Sensitive terms can be probed directly. |
| TB-005 | Chunks -> semantic retrieval | Chunks are embedded and searched by similarity. | Sensitive content can be retrieved through paraphrase. |
| TB-006 | Chunks -> graph construction | Chunks are linked to graph concepts through alias matching. | Incorrect concept matches can distort graph retrieval. |
| TB-007 | Query -> graph traversal | Query concepts become graph traversal start nodes. | Traversal can expose connected concepts beyond the direct query. |
| TB-008 | Retrieval results -> context generation | Retrieved chunks become model context. | Unsafe or unauthorized chunks can influence output. |
| TB-009 | Context -> mock LLM response | Retrieved context is transformed into an answer. | The answer can disclose or amplify unsafe context. |
| TB-010 | Response -> user | The generated answer and citations are returned. | Sensitive sources, citations, or summaries may be exposed. |

## TB-001: User Input to Query Handling

The user query is fully user-controlled.

Current assumptions:

- Queries are accepted as plain text.
- No authentication or role context is evaluated.
- No query intent classification is applied.
- No prompt injection detection is applied.

Risk:

A user can probe for sensitive terms, paraphrase restricted concepts, or ask questions that intentionally steer retrieval toward sensitive or unsafe context.

## TB-002: Knowledge Base to Ingestion

The local knowledge base is treated as available source material.

Current assumptions:

- Documents are loaded from local files.
- Documents are not classified by sensitivity.
- Documents are not scored by trust level.
- Documents are not marked as approved, stale, deprecated, or quarantined.

Risk:

A poisoned, stale, or sensitive document can enter the retrieval system without any admission control.

## TB-003: Documents to Chunks

Documents are split into chunks before retrieval.

Current assumptions:

- Chunking preserves source metadata.
- Chunking does not evaluate sensitivity.
- Chunking does not enforce separation between trusted and untrusted content.

Risk:

Chunk boundaries can accidentally combine safe and sensitive content, or preserve malicious instructions beside otherwise useful content.

## TB-004: Chunks to Keyword Retrieval

Keyword retrieval uses exact term matching.

Current assumptions:

- All chunks are searchable.
- Retrieval is not scoped by user role.
- Retrieval is not filtered by document classification.

Risk:

A user can discover sensitive material through direct keyword probing.

## TB-005: Chunks to Semantic Retrieval

Semantic retrieval uses deterministic local embeddings and similarity search.

Current assumptions:

- All chunks are embedded.
- All embedded chunks are available to similarity search.
- Similarity thresholding can reduce noise but does not enforce authorization.

Risk:

A user can retrieve sensitive material without using exact sensitive terms by asking semantically related questions.

## TB-006: Chunks to Graph Construction

Graph construction links chunks to graph concepts using explicit aliases.

Current assumptions:

- Concepts and aliases are manually defined.
- Matching is deterministic and inspectable.
- Nodes and edges do not have trust scores.
- Nodes do not inherit document classification.

Risk:

Incorrect aliases or poisoned text can create misleading graph links, causing graph retrieval to surface irrelevant, sensitive, or unsafe chunks.

## TB-007: Query to Graph Traversal

Graph retrieval starts from query-matched concepts and traverses relationships.

Current assumptions:

- Traversal is bounded by maximum depth.
- Traversal does not check user role.
- Traversal does not check graph node sensitivity.
- Traversal does not check edge trust.

Risk:

A user can reach sensitive connected concepts through graph relationships even when the direct query does not mention sensitive material.

## TB-008: Retrieval Results to Context Generation

Retrieved chunks are admitted into response generation.

Current assumptions:

- Retrieved chunks are passed toward the mock LLM response layer.
- No context admission policy exists.
- No context sanitization exists.
- No source trust validation exists.

Risk:

Unsafe, unauthorized, poisoned, stale, or misleading context can influence the generated response.

## TB-009: Context to Mock LLM Response

The mock LLM response layer generates a source-aware answer from retrieved chunks.

Current assumptions:

- The mock generator is deterministic and local.
- The generator preserves source awareness.
- The generator does not enforce prompt boundary separation.
- The generator does not validate output safety.

Risk:

A future real LLM integration could treat retrieved content as instructions unless prompt boundaries and content separation are enforced.

## TB-010: Response to User

The final answer and source citations are returned to the user.

Current assumptions:

- Responses include source awareness.
- Output is not filtered by policy.
- Citations are not redacted.
- No audit logging records the response path.

Risk:

The system can disclose sensitive content, sensitive source names, or misleading answers without a record suitable for investigation.

## Boundary Design Implication

Phase 02 should treat each trust boundary as a future control placement candidate.

The most important future control points are:

- Before retrieval executes.
- Before retrieved context enters generation.
- Before graph traversal expands related concepts.
- Before output leaves the system.
- Around logging and incident response evidence preservation.
