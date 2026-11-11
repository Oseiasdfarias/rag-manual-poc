"""Estratégias de busca. Todas seguem a porta `Retriever` e podem ser combinadas."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace

from rag_manual.domain.models import RetrievedChunk
from rag_manual.domain.ports import Embedder, KeywordIndex, Reranker, Retriever, VectorStore

RRF_CONSTANT = 60
HYBRID_DEPTH = 20


class VectorRetriever:
    """Busca por significado: compara o vetor da pergunta com o vetor de cada trecho."""

    def __init__(self, embedder: Embedder, store: VectorStore) -> None:
        self._embedder = embedder
        self._store = store

    def search(self, query: str, k: int) -> list[RetrievedChunk]:
        return self._store.search(self._embedder.embed_query(query), k)


class KeywordRetriever:
    """Busca por palavra (BM25)."""

    def __init__(self, index: KeywordIndex) -> None:
        self._index = index

    def search(self, query: str, k: int) -> list[RetrievedChunk]:
        return self._index.search(query, k)


def reciprocal_rank_fusion(
    rankings: Sequence[Sequence[RetrievedChunk]], c: int = RRF_CONSTANT
) -> list[RetrievedChunk]:
    """Junta várias listas ordenadas. Cada trecho ganha soma de 1/(c + posição).

    Em empate, vale a ordem em que o trecho apareceu primeiro nas listas.
    """
    scores: dict[str, float] = {}
    by_id: dict[str, RetrievedChunk] = {}
    for ranking in rankings:
        for position, item in enumerate(ranking, start=1):
            scores[item.id] = scores.get(item.id, 0.0) + 1 / (c + position)
            by_id[item.id] = item
    ordered = sorted(scores, key=lambda chunk_id: scores[chunk_id], reverse=True)
    return [replace(by_id[chunk_id], score=scores[chunk_id]) for chunk_id in ordered]


class HybridRetriever:
    """Junta várias buscas com RRF. Cada busca entrega `depth` candidatos."""

    def __init__(
        self,
        retrievers: Sequence[Retriever],
        depth: int = HYBRID_DEPTH,
        c: int = RRF_CONSTANT,
    ) -> None:
        self._retrievers = list(retrievers)
        self._depth = depth
        self._c = c

    def search(self, query: str, k: int) -> list[RetrievedChunk]:
        rankings = [r.search(query, self._depth) for r in self._retrievers]
        return reciprocal_rank_fusion(rankings, self._c)[:k]


class RerankingRetriever:
    """Decorator: pega os `candidates` melhores de outra busca e reordena com um reranker."""

    def __init__(self, inner: Retriever, reranker: Reranker, candidates: int = 20) -> None:
        self._inner = inner
        self._reranker = reranker
        self._candidates = candidates

    def search(self, query: str, k: int) -> list[RetrievedChunk]:
        found = self._inner.search(query, max(self._candidates, k))
        if not found:
            return []
        scores = self._reranker.score(query, [item.text for item in found])
        ranked = sorted(zip(found, scores, strict=True), key=lambda pair: pair[1], reverse=True)
        return [replace(item, score=score) for item, score in ranked][:k]
