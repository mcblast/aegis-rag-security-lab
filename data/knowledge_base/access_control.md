# Access Control Standard

Enterprise AI systems must enforce least-privilege access to knowledge sources. Users should only retrieve documents that match their role, business need, and authorization context.

Access control failures in RAG systems can expose confidential source material through retrieved context. Even if the final model response appears harmless, the retrieval layer may have already leaked sensitive information into the prompt context.

Baseline Phase 01 does not enforce role-based retrieval. This document exists so later phases can demonstrate how unrestricted retrieval creates security risk.
