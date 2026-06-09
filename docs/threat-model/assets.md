# Threat Model Assets

## Purpose

This document identifies the system assets considered in the Phase 02 threat model.

An asset is anything the system uses, transforms, exposes, protects, or depends on for retrieval and response generation.

## User and Query Assets

| Asset | Description | Security Relevance |
| --- | --- | --- |
| User query | The natural-language question submitted to the system. | User-controlled input can probe, manipulate, or steer retrieval. |
| Query intent | The implied goal behind a query. | Ambiguous or hostile intent may affect retrieval and response safety. |
| Query terms | Exact tokens used during keyword matching. | Sensitive terms may retrieve restricted chunks if authorization is missing. |
| Query concepts | Concepts inferred through semantic or graph matching. | Concept expansion can retrieve related material beyond exact user wording. |

## Knowledge Base Assets

| Asset | Description | Security Relevance |
| --- | --- | --- |
| Knowledge base documents | Local Markdown and text files used as source material. | Documents can contain sensitive, stale, misleading, or malicious content. |
| Document source names | File names and source identifiers attached to chunks. | Source metadata supports traceability but may also reveal sensitive structure. |
| Document content | The body text loaded during ingestion. | Content can influence retrieval and generation. |
| Document lifecycle state | Whether a document is current, stale, approved, or deprecated. | The current system does not track lifecycle state. |
| Document trust level | Whether a document comes from a trusted or untrusted source. | The current system does not assign trust labels. |
| Document sensitivity level | Whether a document is public, internal, confidential, or restricted. | The current system does not classify documents. |

## Chunking Assets

| Asset | Description | Security Relevance |
| --- | --- | --- |
| Document chunks | Segments produced from source documents. | Chunks are the direct retrieval units passed toward generation. |
| Chunk identifiers | IDs assigned to chunks. | IDs support traceability and attack-path reconstruction. |
| Chunk source metadata | Metadata linking chunks back to source documents. | Metadata supports citation and incident investigation. |
| Chunk boundaries | The text ranges created by chunking. | Poor boundaries can mix trusted and untrusted content or leak adjacent material. |

## Retrieval Assets

| Asset | Description | Security Relevance |
| --- | --- | --- |
| Keyword retrieval scores | Scores based on exact term matching. | Scoring behavior can expose how to probe for sensitive content. |
| Matched terms | Query terms that matched retrieved chunks. | Useful for explainability but may reveal sensitive indexing behavior. |
| Embeddings | Local deterministic vector representations of text. | Embeddings can retrieve semantically similar content without exact terms. |
| Vector index | In-memory structure used for semantic search. | Missing metadata filters can allow broad retrieval across all chunks. |
| Similarity scores | Numeric semantic match scores. | Weak thresholding can admit noisy or unsafe context. |
| Semantic threshold | Minimum similarity required for returned semantic chunks. | A low threshold can over-retrieve; a high threshold can miss relevant evidence. |

## GraphRAG Assets

| Asset | Description | Security Relevance |
| --- | --- | --- |
| Graph nodes | Security concepts used by the local knowledge graph. | Nodes may need classification, trust, or policy labels in later phases. |
| Graph aliases | Terms used to match text and queries to graph concepts. | Alias abuse can steer traversal or create false concept matches. |
| Graph edges | Relationships between graph concepts. | Incorrect or poisoned relationships can distort retrieval. |
| Graph traversal paths | Paths followed from query-matched concepts. | Traversal can expose connected concepts beyond the user's direct query. |
| Graph traversal depth | Maximum number of relationship hops. | Excessive depth can broaden retrieval and increase exposure risk. |
| Graph chunk links | Links between source chunks and graph nodes. | Incorrect links can cause misleading or unsafe retrieval. |

## Generation and Output Assets

| Asset | Description | Security Relevance |
| --- | --- | --- |
| Retrieved context | Chunks selected for response generation. | This is the main bridge between retrieval and model output. |
| Mock LLM response | Source-aware generated response. | Responses can disclose, summarize, or amplify retrieved content. |
| Source citations | Source list attached to responses. | Citations support traceability but may reveal sensitive source names. |
| Retrieved chunk IDs | IDs included in pipeline results. | Chunk IDs support debugging and incident analysis. |

## Future Operational Assets

| Asset | Description | Security Relevance |
| --- | --- | --- |
| Audit logs | Future records of queries, retrieval decisions, and responses. | Needed for detection, investigation, and governance. |
| Policy decisions | Future allow, deny, redact, or escalate outcomes. | Needed for enforceable control behavior. |
| Incident records | Future records of suspected misuse, poisoning, or leakage. | Needed for response and recovery. |
| Evaluation results | Future adversarial test outcomes and retrieval metrics. | Needed to measure whether controls reduce risk. |
