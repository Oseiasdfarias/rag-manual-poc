from pathlib import Path

from rag_manual.config import Settings
from rag_manual.infrastructure.embeddings import (
    SentenceTransformerEmbedder,
    default_prefixes,
)
from rag_manual.infrastructure.golden_csv import load_golden_cases


def test_settings_padrao_sem_ambiente():
    settings = Settings.from_env({})
    assert settings.chunk_size == 800 and settings.chunk_overlap == 150
    assert settings.chroma_path == Path("db/chroma")
    assert settings.chunks_path == Path("db/chunks.json")
    assert settings.llm_base_url is None


def test_settings_le_variaveis():
    env = {
        "RAG_CHUNKER": "section",
        "RAG_CHUNK_SIZE": "400",
        "RAG_INDEX_DIR": "outro",
        "LLM_BASE_URL": "http://localhost:11434/v1",
        "LLM_MODEL": "qwen2.5:3b",
        "RAG_RERANKER_MODEL": "algum/modelo",
    }
    settings = Settings.from_env(env)
    assert settings.chunker == "section" and settings.chunk_size == 400
    assert settings.index_dir == Path("outro")
    assert settings.llm_model == "qwen2.5:3b"
    assert settings.llm_base_url == "http://localhost:11434/v1"
    assert settings.reranker_model == "algum/modelo"


def test_prefixos_e5():
    assert default_prefixes("intfloat/multilingual-e5-small") == ("query: ", "passage: ")
    assert default_prefixes("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2") == (
        "",
        "",
    )


def test_embedder_prefixo_pode_ser_sobreposto_sem_carregar_modelo():
    embedder = SentenceTransformerEmbedder("intfloat/multilingual-e5-small", query_prefix="")
    assert embedder._query_prefix == ""
    assert embedder._passage_prefix == "passage: "
    assert embedder._model is None  # carga preguiçosa


def test_golden_csv_trata_zero_como_sem_resposta(tmp_path):
    csv_file = tmp_path / "golden.csv"
    csv_file.write_text("pergunta;paginas\nA?;54\nB?;60|76\nC?;0\n", encoding="utf-8")
    cases = load_golden_cases(csv_file)
    assert [c.pages for c in cases] == [frozenset({54}), frozenset({60, 76}), frozenset()]
    assert [c.answerable for c in cases] == [True, True, False]
