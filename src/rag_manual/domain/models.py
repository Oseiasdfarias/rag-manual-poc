"""Objetos do domínio. Todos imutáveis e sem dependência de outras camadas."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Page:
    """Texto bruto de uma página. `number` começa em 1 (índice do PDF, não o número impresso)."""

    number: int
    text: str


@dataclass(frozen=True)
class Chunk:
    """Trecho do manual. `section` guarda o título da seção, quando o chunker souber."""

    id: str
    page: int
    text: str
    section: str = ""


@dataclass(frozen=True)
class RetrievedChunk:
    """Trecho devolvido por uma busca, com a nota dada por ela (a escala muda por estratégia)."""

    chunk: Chunk
    score: float = 0.0

    @property
    def id(self) -> str:
        return self.chunk.id

    @property
    def page(self) -> int:
        return self.chunk.page

    @property
    def text(self) -> str:
        return self.chunk.text


@dataclass(frozen=True)
class Answer:
    """Resposta do LLM junto com os trechos que foram para o prompt."""

    question: str
    text: str
    sources: tuple[RetrievedChunk, ...]

    @property
    def pages(self) -> tuple[int, ...]:
        return tuple(s.page for s in self.sources)


@dataclass(frozen=True)
class GoldenCase:
    """Uma pergunta do conjunto de teste. `pages` vazio significa: o manual não responde."""

    question: str
    pages: frozenset[int]

    @property
    def answerable(self) -> bool:
        return bool(self.pages)


@dataclass(frozen=True)
class RetrievalFailure:
    """Pergunta em que a busca não acertou dentro do corte (k)."""

    question: str
    expected: tuple[int, ...]
    got: tuple[int, ...]


@dataclass(frozen=True)
class RetrievalMetrics:
    """Resultado de uma estratégia de busca sobre o conjunto de teste."""

    strategy: str
    k: int
    depth: int
    total: int
    hits: int
    mrr: float
    failures: tuple[RetrievalFailure, ...] = ()

    @property
    def hit_rate(self) -> float:
        return self.hits / self.total if self.total else 0.0
