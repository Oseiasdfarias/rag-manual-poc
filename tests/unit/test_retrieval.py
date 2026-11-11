from rag_manual.application.retrieval import (
    HybridRetriever,
    KeywordRetriever,
    RerankingRetriever,
    VectorRetriever,
    reciprocal_rank_fusion,
)
from rag_manual.domain.models import Chunk
from tests.conftest import (
    FakeEmbedder,
    FakeKeywordIndex,
    FakeReranker,
    FakeRetriever,
    FakeVectorStore,
    hit,
    make_chunk,
)


def test_rrf_soma_pontos_de_listas_diferentes():
    a = [hit("x", 1), hit("y", 2)]
    b = [hit("y", 2), hit("z", 3)]
    fused = reciprocal_rank_fusion([a, b], c=60)
    assert [r.id for r in fused] == ["y", "x", "z"]
    assert fused[0].score == 1 / 62 + 1 / 61


def test_rrf_empate_vale_a_ordem_de_chegada():
    fused = reciprocal_rank_fusion([[hit("a", 1)], [hit("b", 2)]])
    assert [r.id for r in fused] == ["a", "b"]


def test_rrf_listas_vazias():
    assert reciprocal_rank_fusion([[], []]) == []


def test_hybrid_pede_depth_candidatos_e_corta_em_k():
    first = FakeRetriever([hit(f"a{i}", i) for i in range(30)])
    second = FakeRetriever([hit(f"b{i}", i) for i in range(30)])
    result = HybridRetriever([first, second], depth=20).search("q", 5)
    assert len(result) == 5
    assert first.requested_k == [20] and second.requested_k == [20]


def test_vector_retriever_usa_embedder_e_store():
    store, embedder = FakeVectorStore(), FakeEmbedder()
    store.add([make_chunk("a", 1), make_chunk("b", 2)], [[0.0], [0.0]])
    result = VectorRetriever(embedder, store).search("pergunta", 1)
    assert embedder.queries == ["pergunta"]
    assert [r.id for r in result] == ["a"]


def test_keyword_retriever_delega_ao_indice():
    index = FakeKeywordIndex()
    index.build([Chunk("a", 1, "motor quente"), Chunk("b", 2, "graxa nova")])
    assert [r.page for r in KeywordRetriever(index).search("graxa", 1)] == [2]


def test_reranking_reordena_os_candidatos():
    inner = FakeRetriever(
        [hit("a", 1, "nada a ver"), hit("b", 2, "mancal quente demais"), hit("c", 3, "mancal")]
    )
    result = RerankingRetriever(inner, FakeReranker(), candidates=3).search("mancal quente", 2)
    assert [r.id for r in result] == ["b", "c"]
    assert result[0].score == 2.0


def test_reranking_pede_pelo_menos_candidates_ao_interno():
    inner = FakeRetriever([hit("a", 1)])
    RerankingRetriever(inner, FakeReranker(), candidates=20).search("q", 3)
    assert inner.requested_k == [20]


def test_reranking_sem_resultado_devolve_vazio():
    assert RerankingRetriever(FakeRetriever([]), FakeReranker()).search("q", 3) == []
