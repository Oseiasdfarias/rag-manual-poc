import pytest

from rag_manual.application.evaluation import (
    EvaluateRetrieval,
    first_hit_rank,
    hit_at_k,
    mean_reciprocal_rank,
    reciprocal_rank,
)
from rag_manual.domain.models import GoldenCase
from tests.conftest import FakeRetrieverByQuery, hit


def test_first_hit_rank():
    assert first_hit_rank([5, 7, 9], {7, 9}) == 2
    assert first_hit_rank([5, 7], {1}) is None


def test_hit_at_k_usa_o_corte():
    assert hit_at_k([1, 2, 3, 4], {3}, k=3)
    assert not hit_at_k([1, 2, 3, 4], {4}, k=3)
    assert not hit_at_k([], {1}, k=3)


def test_reciprocal_rank():
    assert reciprocal_rank([9, 8, 7], {7}) == pytest.approx(1 / 3)
    assert reciprocal_rank([9], {1}) == 0.0


def test_mean_reciprocal_rank():
    assert mean_reciprocal_rank([1.0, 0.5, 0.0]) == pytest.approx(0.5)
    assert mean_reciprocal_rank([]) == 0.0


def test_evaluate_retrieval_conta_acertos_mrr_e_falhas():
    cases = [
        GoldenCase("p1", frozenset({10})),
        GoldenCase("p2", frozenset({20, 21})),
        GoldenCase("p3", frozenset({30})),
        GoldenCase("sem resposta", frozenset()),
    ]
    retriever = FakeRetrieverByQuery(
        {
            "p1": [hit("a", 10)],
            "p2": [hit("b", 1), hit("c", 2), hit("d", 3), hit("e", 21)],
            "p3": [hit("f", 1)],
            "sem resposta": [hit("g", 1)],
        }
    )
    metrics = EvaluateRetrieval(k=3, depth=10).run("teste", retriever, cases)
    assert metrics.total == 3  # ignora a pergunta sem resposta
    assert metrics.hits == 1
    assert metrics.mrr == pytest.approx((1 + 1 / 4 + 0) / 3)
    assert metrics.hit_rate == pytest.approx(1 / 3)
    assert [f.question for f in metrics.failures] == ["p2", "p3"]
    assert metrics.failures[0].expected == (20, 21)
    assert metrics.failures[0].got == (1, 2, 3)


def test_run_all_mantem_os_nomes():
    cases = [GoldenCase("p", frozenset({1}))]
    retrievers = {"a": FakeRetrieverByQuery({"p": [hit("x", 1)]}), "b": FakeRetrieverByQuery({})}
    results = EvaluateRetrieval().run_all(retrievers, cases)
    assert [(m.strategy, m.hits) for m in results] == [("a", 1), ("b", 0)]
