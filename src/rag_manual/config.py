"""Configuração lida de variáveis de ambiente, com valores padrão."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

DEFAULT_EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
E5_EMBEDDING_MODEL = "intfloat/multilingual-e5-small"
RERANKER_MODEL = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"


@dataclass(frozen=True)
class Settings:
    pdf_path: Path = Path("data/manual.pdf")
    golden_path: Path = Path("golden.csv")
    index_dir: Path = Path("db")
    collection: str = "manual"
    chunker: str = "fixed"  # "fixed" (tamanho fixo) ou "section" (por seção)
    chunk_size: int = 800  # tamanho máximo do trecho, em caracteres
    chunk_overlap: int = 150  # caracteres repetidos entre trechos vizinhos
    embedding_model: str = DEFAULT_EMBEDDING_MODEL
    reranker_model: str = ""  # vazio = sem reranker
    rerank_candidates: int = 20
    answer_k: int = 5  # trechos enviados ao LLM
    llm_model: str = "gpt-4o-mini"
    llm_base_url: str | None = None  # vazio = OpenAI; Ollama: http://localhost:11434/v1
    llm_api_key: str | None = None
    llm_temperature: float = 0.0

    @property
    def chroma_path(self) -> Path:
        return self.index_dir / "chroma"

    @property
    def chunks_path(self) -> Path:
        return self.index_dir / "chunks.json"

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> Settings:
        env = os.environ if env is None else env
        base = cls()
        return cls(
            pdf_path=Path(env.get("RAG_PDF", str(base.pdf_path))),
            golden_path=Path(env.get("RAG_GOLDEN", str(base.golden_path))),
            index_dir=Path(env.get("RAG_INDEX_DIR", str(base.index_dir))),
            collection=env.get("RAG_COLLECTION", base.collection),
            chunker=env.get("RAG_CHUNKER", base.chunker),
            chunk_size=int(env.get("RAG_CHUNK_SIZE", base.chunk_size)),
            chunk_overlap=int(env.get("RAG_CHUNK_OVERLAP", base.chunk_overlap)),
            embedding_model=env.get("RAG_EMBEDDING_MODEL", base.embedding_model),
            reranker_model=env.get("RAG_RERANKER_MODEL", base.reranker_model),
            rerank_candidates=int(env.get("RAG_RERANK_CANDIDATES", base.rerank_candidates)),
            answer_k=int(env.get("RAG_ANSWER_K", base.answer_k)),
            llm_model=env.get("LLM_MODEL", base.llm_model),
            llm_base_url=env.get("LLM_BASE_URL") or None,
            llm_api_key=env.get("LLM_API_KEY") or env.get("OPENAI_API_KEY") or None,
            llm_temperature=float(env.get("LLM_TEMPERATURE", base.llm_temperature)),
        )
