import pytest

from rag_manual.cli import _settings_from, build_parser
from rag_manual.config import RERANKER_MODEL
from rag_manual.domain.models import RetrievalFailure, RetrievalMetrics
from rag_manual.experiments import EXPERIMENTS, find_experiments
from rag_manual.reporting import format_metrics


def test_cli_opcoes_sobrepoem_o_ambiente(monkeypatch):
    monkeypatch.setenv("RAG_CHUNK_SIZE", "400")
    args = build_parser().parse_args(["eval", "--chunker", "section", "--reranker"])
    settings = _settings_from(args)
    assert settings.chunker == "section"
    assert settings.chunk_size == 400
    assert settings.reranker_model == RERANKER_MODEL


def test_cli_reranker_none_desliga(monkeypatch):
    monkeypatch.setenv("RAG_RERANKER_MODEL", "algum/modelo")
    args = build_parser().parse_args(["eval", "--reranker", "none"])
    assert _settings_from(args).reranker_model == ""


def test_cli_exige_subcomando():
    with pytest.raises(SystemExit):
        build_parser().parse_args([])


def test_experimentos_tem_base_e_nomes_unicos():
    names = [e.name for e in EXPERIMENTS]
    assert names[0] == "base" and len(names) == len(set(names))
    assert [e.name for e in find_experiments(["secao"])] == ["secao"]
    with pytest.raises(ValueError):
        find_experiments(["nao_existe"])


def test_format_metrics_mostra_falhas_e_resumo():
    metrics = RetrievalMetrics(
        strategy="bm25",
        k=3,
        depth=10,
        total=13,
        hits=9,
        mrr=0.68,
        failures=(RetrievalFailure("Pergunta?", (54,), (1, 2, 3)),),
    )
    text = format_metrics(metrics)
    assert "[bm25] errou: Pergunta?  esperado [54], veio [1, 2, 3]" in text
    assert "hit@3 = 9/13 (69%)   MRR@10 = 0.68" in text


def test_padrao_e_o_melhor_medido_e_a_base_continua_fixa():
    from rag_manual.config import BASE_EMBEDDING_MODEL, E5_EMBEDDING_MODEL, Settings

    settings = Settings.from_env({})
    assert settings.embedding_model == E5_EMBEDDING_MODEL
    assert settings.retriever == "vetorial"
    assert settings.reranker_model == ""
    base = find_experiments(["base"])[0]
    assert base.overrides["embedding_model"] == BASE_EMBEDDING_MODEL
