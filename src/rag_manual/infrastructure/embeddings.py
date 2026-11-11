"""Embeddings com sentence-transformers. O modelo só é carregado no primeiro uso."""

from __future__ import annotations

from collections.abc import Sequence

E5_QUERY_PREFIX = "query: "
E5_PASSAGE_PREFIX = "passage: "


def default_prefixes(model_name: str) -> tuple[str, str]:
    """Os modelos e5 exigem prefixos: "query: " na pergunta e "passage: " no trecho."""
    if "e5" in model_name.lower():
        return E5_QUERY_PREFIX, E5_PASSAGE_PREFIX
    return "", ""


class SentenceTransformerEmbedder:
    def __init__(
        self,
        model_name: str,
        query_prefix: str | None = None,
        passage_prefix: str | None = None,
        show_progress: bool = False,
    ) -> None:
        default_query, default_passage = default_prefixes(model_name)
        self._model_name = model_name
        self._query_prefix = default_query if query_prefix is None else query_prefix
        self._passage_prefix = default_passage if passage_prefix is None else passage_prefix
        self._show_progress = show_progress
        self._model = None

    def _load(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self._model_name)
        return self._model

    def embed_passages(self, texts: Sequence[str]) -> list[list[float]]:
        prefixed = [self._passage_prefix + t for t in texts]
        vectors = self._load().encode(
            prefixed, normalize_embeddings=True, show_progress_bar=self._show_progress
        )
        return vectors.tolist()

    def embed_query(self, text: str) -> list[float]:
        vector = self._load().encode([self._query_prefix + text], normalize_embeddings=True)[0]
        return vector.tolist()
