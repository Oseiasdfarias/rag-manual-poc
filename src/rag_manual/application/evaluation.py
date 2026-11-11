"""Métricas de busca (funções puras) e o caso de uso que roda o conjunto de teste."""

from __future__ import annotations

from collections.abc import Collection, Mapping, Sequence

from rag_manual.domain.models import GoldenCase, RetrievalFailure, RetrievalMetrics
from rag_manual.domain.ports import Retriever


def first_hit_rank(pages: Sequence[int], expected: Collection[int]) -> int | None:
    """Posição (a partir de 1) da primeira página correta, ou None se não aparece."""
    return next((i for i, page in enumerate(pages, start=1) if page in expected), None)


def hit_at_k(pages: Sequence[int], expected: Collection[int], k: int) -> bool:
    rank = first_hit_rank(pages, expected)
    return rank is not None and rank <= k


def reciprocal_rank(pages: Sequence[int], expected: Collection[int]) -> float:
    """1 dividido pela posição da primeira página correta. 0 se não aparece."""
    rank = first_hit_rank(pages, expected)
    return 1 / rank if rank else 0.0


def mean_reciprocal_rank(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


class EvaluateRetrieval:
    """Mede hit@k e MRR de várias estratégias. Só usa as perguntas que têm resposta."""

    def __init__(self, k: int = 3, depth: int = 10) -> None:
        self._k = k
        self._depth = depth

    def run(self, name: str, retriever: Retriever, cases: Sequence[GoldenCase]) -> RetrievalMetrics:
        answerable = [c for c in cases if c.answerable]
        hits, reciprocal_ranks = 0, []
        failures: list[RetrievalFailure] = []
        for case in answerable:
            pages = [r.page for r in retriever.search(case.question, self._depth)]
            reciprocal_ranks.append(reciprocal_rank(pages, case.pages))
            if hit_at_k(pages, case.pages, self._k):
                hits += 1
            else:
                failures.append(
                    RetrievalFailure(
                        question=case.question,
                        expected=tuple(sorted(case.pages)),
                        got=tuple(pages[: self._k]),
                    )
                )
        return RetrievalMetrics(
            strategy=name,
            k=self._k,
            depth=self._depth,
            total=len(answerable),
            hits=hits,
            mrr=mean_reciprocal_rank(reciprocal_ranks),
            failures=tuple(failures),
        )

    def run_all(
        self, retrievers: Mapping[str, Retriever], cases: Sequence[GoldenCase]
    ) -> list[RetrievalMetrics]:
        return [self.run(name, retriever, cases) for name, retriever in retrievers.items()]
