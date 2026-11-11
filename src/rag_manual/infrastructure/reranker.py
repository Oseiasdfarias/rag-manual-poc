"""Reranker: um cross-encoder lê pergunta e trecho juntos e dá uma nota."""

from __future__ import annotations

from collections.abc import Sequence


class CrossEncoderReranker:
    def __init__(self, model_name: str) -> None:
        self._model_name = model_name
        self._model = None

    def _load(self):
        if self._model is None:
            from sentence_transformers import CrossEncoder

            self._model = CrossEncoder(self._model_name)
        return self._model

    def score(self, query: str, passages: Sequence[str]) -> list[float]:
        scores = self._load().predict([(query, p) for p in passages])
        return [float(s) for s in scores]
