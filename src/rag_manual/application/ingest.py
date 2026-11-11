"""Caso de uso: ler o manual, dividir em trechos e gravar nos índices."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from rag_manual.domain.ports import Chunker, DocumentLoader, Embedder, KeywordIndex, VectorStore


class NoTextExtractedError(RuntimeError):
    """O PDF não trouxe texto. Provavelmente é imagem e precisaria de OCR."""


@dataclass(frozen=True)
class IngestReport:
    pages: int
    chunks: int


class IngestManual:
    def __init__(
        self,
        loader: DocumentLoader,
        chunker: Chunker,
        embedder: Embedder,
        vector_store: VectorStore,
        keyword_index: KeywordIndex,
    ) -> None:
        self._loader = loader
        self._chunker = chunker
        self._embedder = embedder
        self._vector_store = vector_store
        self._keyword_index = keyword_index

    def run(self, pdf_path: Path) -> IngestReport:
        pages = self._loader.load(pdf_path)
        chunks = self._chunker.chunk(pages)
        if not chunks:
            raise NoTextExtractedError("Nenhum texto extraído: o PDF deve ser imagem.")
        vectors = self._embedder.embed_passages([c.text for c in chunks])
        self._vector_store.reset()
        self._vector_store.add(chunks, vectors)
        self._keyword_index.build(chunks)
        return IngestReport(pages=len(pages), chunks=len(chunks))
