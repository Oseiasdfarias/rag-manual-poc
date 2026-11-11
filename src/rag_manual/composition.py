"""Monta os objetos a partir das configurações. Único lugar que conhece as classes concretas."""

from __future__ import annotations

from rag_manual.application.answering import AnswerQuestion
from rag_manual.application.ingest import IngestManual
from rag_manual.application.retrieval import (
    HybridRetriever,
    KeywordRetriever,
    RerankingRetriever,
    VectorRetriever,
)
from rag_manual.config import Settings
from rag_manual.domain.ports import Chunker, Embedder, Retriever
from rag_manual.infrastructure.bm25_index import Bm25Index
from rag_manual.infrastructure.chroma_store import ChromaVectorStore
from rag_manual.infrastructure.chunking import FixedSizeChunker, SectionAwareChunker
from rag_manual.infrastructure.embeddings import SentenceTransformerEmbedder
from rag_manual.infrastructure.llm import OpenAICompatibleLLM
from rag_manual.infrastructure.pdf_loader import PypdfLoader
from rag_manual.infrastructure.reranker import CrossEncoderReranker

CHUNKERS = {"fixed": FixedSizeChunker, "section": SectionAwareChunker}


def build_chunker(settings: Settings) -> Chunker:
    try:
        factory = CHUNKERS[settings.chunker]
    except KeyError:
        options = sorted(CHUNKERS)
        raise ValueError(f"Chunker desconhecido: {settings.chunker!r}. Use {options}.") from None
    return factory(settings.chunk_size, settings.chunk_overlap)


def build_embedder(settings: Settings, show_progress: bool = False) -> Embedder:
    return SentenceTransformerEmbedder(settings.embedding_model, show_progress=show_progress)


def build_ingest(settings: Settings) -> IngestManual:
    return IngestManual(
        loader=PypdfLoader(),
        chunker=build_chunker(settings),
        embedder=build_embedder(settings, show_progress=True),
        vector_store=ChromaVectorStore(settings.chroma_path, settings.collection),
        keyword_index=Bm25Index(settings.chunks_path),
    )


def build_retrievers(settings: Settings, with_reranker: bool | None = None) -> dict[str, Retriever]:
    """Todas as estratégias de busca, pelo nome.

    Com reranker configurado entram também "reranker" (híbrida + reranker, a busca usada para
    responder) e "vet+reranker" (só a vetorial + reranker, para comparar).
    """
    vector = VectorRetriever(
        build_embedder(settings), ChromaVectorStore(settings.chroma_path, settings.collection)
    )
    keyword = KeywordRetriever(Bm25Index(settings.chunks_path))
    hybrid = HybridRetriever([vector, keyword])
    retrievers: dict[str, Retriever] = {"vetorial": vector, "bm25": keyword, "hibrida": hybrid}
    use_reranker = bool(settings.reranker_model) if with_reranker is None else with_reranker
    if use_reranker and settings.reranker_model:
        reranker = CrossEncoderReranker(settings.reranker_model)
        candidates = settings.rerank_candidates
        retrievers["reranker"] = RerankingRetriever(hybrid, reranker, candidates)
        retrievers["vet+reranker"] = RerankingRetriever(vector, reranker, candidates)
    return retrievers


def build_default_retriever(settings: Settings) -> Retriever:
    """A busca escolhida em `settings.retriever`."""
    name = settings.retriever
    retrievers = build_retrievers(settings, with_reranker="reranker" in name)
    if name not in retrievers:
        raise ValueError(f"Busca desconhecida ou sem reranker configurado: {name!r}.")
    return retrievers[name]


def build_answerer(settings: Settings) -> AnswerQuestion:
    llm = OpenAICompatibleLLM(
        model=settings.llm_model,
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key,
        temperature=settings.llm_temperature,
    )
    return AnswerQuestion(build_default_retriever(settings), llm, settings.answer_k)
