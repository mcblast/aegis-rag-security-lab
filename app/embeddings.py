"""Embedding providers for Phase 01.5 semantic retrieval.

The first provider is intentionally local and deterministic. It gives the project
an embedding-shaped interface without requiring API keys, model downloads, or
network access. Later phases can replace this with sentence-transformer, OpenAI,
or another embedding backend without changing the retrieval pipeline.
"""

from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass
from typing import Protocol

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9_'-]+")

# Lightweight concept normalization makes the local embedding provider useful for
# architecture learning and deterministic tests. This is not a replacement for a
# production embedding model; it is a stable local semantic scaffold.
CONCEPT_ALIASES = {
    "attack": "prompt_injection",
    "attacks": "prompt_injection",
    "bypass": "prompt_injection",
    "hidden": "prompt_injection",
    "ignore": "prompt_injection",
    "inject": "prompt_injection",
    "injection": "prompt_injection",
    "instruction": "prompt_injection",
    "instructions": "prompt_injection",
    "jailbreak": "prompt_injection",
    "malicious": "prompt_injection",
    "manipulate": "prompt_injection",
    "manipulates": "prompt_injection",
    "manipulated": "prompt_injection",
    "override": "prompt_injection",
    "policy": "prompt_injection",
    "prompt": "prompt_injection",
    "rule": "prompt_injection",
    "rules": "prompt_injection",
    "system": "prompt_injection",
    "authority": "prompt_injection",
    "content": "indirect_prompt_injection",
    "email": "indirect_prompt_injection",
    "emails": "indirect_prompt_injection",
    "external": "indirect_prompt_injection",
    "page": "indirect_prompt_injection",
    "pages": "indirect_prompt_injection",
    "ticket": "indirect_prompt_injection",
    "tickets": "indirect_prompt_injection",
    "web": "indirect_prompt_injection",
    "authorized": "access_control",
    "authorization": "access_control",
    "confidential": "access_control",
    "leak": "access_control",
    "leakage": "access_control",
    "least": "access_control",
    "privilege": "access_control",
    "private": "access_control",
    "role": "access_control",
    "roles": "access_control",
    "access": "access_control",
    "boundary": "incident_response",
    "boundaries": "incident_response",
    "evidence": "incident_response",
    "failure": "incident_response",
    "failures": "incident_response",
    "incident": "incident_response",
    "incidents": "incident_response",
    "investigate": "incident_response",
    "investigated": "incident_response",
    "investigator": "incident_response",
    "investigators": "incident_response",
    "logs": "incident_response",
    "preserve": "incident_response",
    "triage": "incident_response",
    "telemetry": "incident_response",
    "retrieval": "retrieval_security",
    "retrieved": "retrieval_security",
    "context": "retrieval_security",
    "documents": "retrieval_security",
    "source": "retrieval_security",
    "sources": "retrieval_security",
}

# Some higher-level concepts should reinforce nearby parent concepts. For
# example, indirect prompt injection is still a prompt-injection risk, so a query
# about external content telling the model to ignore rules should land near the
# AI security policy instead of drifting toward unrelated retrieval context.
CONCEPT_BRIDGES = {
    "indirect_prompt_injection": ("prompt_injection",),
}


class EmbeddingProvider(Protocol):
    """Interface for converting text into vector embeddings."""

    model_name: str

    def embed_text(self, text: str) -> list[float]:
        """Embed a single text string."""

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple text strings."""


@dataclass(frozen=True)
class LocalSemanticEmbeddingProvider:
    """Deterministic local embedding provider for the Phase 01.5 lab.

    The provider combines hashed token buckets with small concept-normalization
    boosts. This lets the semantic retrieval path demonstrate meaning-oriented
    retrieval behavior while staying dependency-free and testable.
    """

    dimensions: int = 96
    model_name: str = "local-semantic-hash-v1"

    def embed_text(self, text: str) -> list[float]:
        if self.dimensions <= 0:
            raise ValueError("dimensions must be greater than zero")

        vector = [0.0 for _ in range(self.dimensions)]
        tokens = self._tokenize(text)

        for token in tokens:
            self._add_token(vector, token, weight=1.0)

            concept = CONCEPT_ALIASES.get(token)
            if concept:
                self._add_token(vector, concept, weight=2.5)
                for bridged_concept in CONCEPT_BRIDGES.get(concept, ()): 
                    self._add_token(vector, bridged_concept, weight=1.5)

        return self._normalize(vector)

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_text(text) for text in texts]

    def _tokenize(self, text: str) -> list[str]:
        return [token.lower() for token in TOKEN_PATTERN.findall(text)]

    def _add_token(self, vector: list[float], token: str, weight: float) -> None:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        bucket = int.from_bytes(digest[:4], byteorder="big") % self.dimensions
        vector[bucket] += weight

    def _normalize(self, vector: list[float]) -> list[float]:
        magnitude = math.sqrt(sum(value * value for value in vector))
        if magnitude == 0:
            return vector
        return [value / magnitude for value in vector]
