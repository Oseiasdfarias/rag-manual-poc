"""Interfaces (portas) que a aplicação usa. A infraestrutura implementa."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Protocol

from rag_manual.domain.models import Chunk, Page, RetrievedChunk


class DocumentLoader(Protocol):
    def load(self, path: Path) -> list[Page]: ...


class Chunker(Protocol):
    def chunk(self, pages: Sequence[Page]) -> list[Chunk]: ...


class Embedder(Protocol):
    def embed_passages(self, texts: Sequence[str]) -> list[list[float]]: ...

    def embed_query(self, text: str) -> list[float]: ...


class VectorStore(Protocol):
    def reset(self) -> None: ...

    def add(self, chunks: Sequence[Chunk], vectors: Sequence[Sequence[float]]) -> None: ...

    def search(self, vector: Sequence[float], k: int) -> list[RetrievedChunk]: ...


class KeywordIndex(Protocol):
    def build(self, chunks: Sequence[Chunk]) -> None: ...

    def search(self, query: str, k: int) -> list[RetrievedChunk]: ...


class Reranker(Protocol):
    def score(self, query: str, passages: Sequence[str]) -> list[float]: ...


class LLM(Protocol):
    def complete(self, prompt: str) -> str: ...


class Retriever(Protocol):
    """Qualquer estratégia de busca: devolve os `k` melhores trechos, do melhor para o pior."""

    def search(self, query: str, k: int) -> list[RetrievedChunk]: ...
