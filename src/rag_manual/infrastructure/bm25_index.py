"""Índice BM25. Guarda os trechos em `chunks.json` para recarregar sem refazer a ingestão."""

from __future__ import annotations

import json
import re
from collections.abc import Sequence
from pathlib import Path

from rank_bm25 import BM25Okapi

from rag_manual.domain.models import Chunk, RetrievedChunk


def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


class Bm25Index:
    def __init__(self, chunks_path: Path) -> None:
        self._path = chunks_path
        self._chunks: list[Chunk] | None = None
        self._bm25: BM25Okapi | None = None

    def build(self, chunks: Sequence[Chunk]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        data = [{"id": c.id, "page": c.page, "text": c.text, "section": c.section} for c in chunks]
        self._path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self._chunks, self._bm25 = None, None  # força recarregar do arquivo

    def _load(self) -> tuple[list[Chunk], BM25Okapi]:
        if self._chunks is None or self._bm25 is None:
            data = json.loads(self._path.read_text(encoding="utf-8"))
            self._chunks = [Chunk(**item) for item in data]
            self._bm25 = BM25Okapi([tokenize(c.text) for c in self._chunks])
        return self._chunks, self._bm25

    def search(self, query: str, k: int) -> list[RetrievedChunk]:
        chunks, bm25 = self._load()
        scores = bm25.get_scores(tokenize(query))
        order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [RetrievedChunk(chunk=chunks[i], score=float(scores[i])) for i in order]
