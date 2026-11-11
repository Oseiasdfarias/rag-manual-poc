"""Fakes em memória das portas. Os testes unitários não baixam modelos nem usam disco."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import pytest

from rag_manual.domain.models import Chunk, Page, RetrievedChunk


def make_chunk(chunk_id: str, page: int, text: str = "texto", section: str = "") -> Chunk:
    return Chunk(id=chunk_id, page=page, text=text, section=section)


def hit(chunk_id: str, page: int, text: str = "texto", score: float = 0.0) -> RetrievedChunk:
    return RetrievedChunk(chunk=make_chunk(chunk_id, page, text), score=score)


class FakeRetriever:
    """Devolve sempre a mesma lista, cortada em k. Guarda os k pedidos."""

    def __init__(self, results: Sequence[RetrievedChunk]) -> None:
        self._results = list(results)
        self.requested_k: list[int] = []

    def search(self, query: str, k: int) -> list[RetrievedChunk]:
        self.requested_k.append(k)
        return self._results[:k]


class FakeRetrieverByQuery:
    def __init__(self, by_query: dict[str, list[RetrievedChunk]]) -> None:
        self._by_query = by_query

    def search(self, query: str, k: int) -> list[RetrievedChunk]:
        return self._by_query.get(query, [])[:k]


class FakeLoader:
    def __init__(self, pages: Sequence[Page]) -> None:
        self._pages = list(pages)

    def load(self, path: Path) -> list[Page]:
        return list(self._pages)


class FakeEmbedder:
    def __init__(self) -> None:
        self.passages: list[str] = []
        self.queries: list[str] = []

    def embed_passages(self, texts: Sequence[str]) -> list[list[float]]:
        self.passages.extend(texts)
        return [[float(len(t)), 1.0] for t in texts]

    def embed_query(self, text: str) -> list[float]:
        self.queries.append(text)
        return [float(len(text)), 1.0]


class FakeVectorStore:
    def __init__(self) -> None:
        self.chunks: list[Chunk] = []
        self.reset_calls = 0

    def reset(self) -> None:
        self.reset_calls += 1
        self.chunks = []

    def add(self, chunks: Sequence[Chunk], vectors: Sequence[Sequence[float]]) -> None:
        assert len(chunks) == len(vectors)
        self.chunks.extend(chunks)

    def search(self, vector: Sequence[float], k: int) -> list[RetrievedChunk]:
        return [RetrievedChunk(chunk=c) for c in self.chunks[:k]]


class FakeKeywordIndex:
    def __init__(self) -> None:
        self.built: list[Chunk] = []

    def build(self, chunks: Sequence[Chunk]) -> None:
        self.built = list(chunks)

    def search(self, query: str, k: int) -> list[RetrievedChunk]:
        words = query.lower().split()
        scored = [(sum(w in c.text.lower() for w in words), c) for c in self.built]
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [RetrievedChunk(chunk=c, score=float(s)) for s, c in scored[:k]]


class FakeReranker:
    """Nota = quantas palavras da pergunta aparecem no trecho."""

    def score(self, query: str, passages: Sequence[str]) -> list[float]:
        words = query.lower().split()
        return [float(sum(w in p.lower() for w in words)) for p in passages]


class FakeLLM:
    def __init__(self, reply: str = "resposta") -> None:
        self.reply = reply
        self.prompts: list[str] = []

    def complete(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.reply


@pytest.fixture
def fake_embedder() -> FakeEmbedder:
    return FakeEmbedder()
