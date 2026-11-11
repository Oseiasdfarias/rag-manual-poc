"""Banco vetorial Chroma, em disco."""

from __future__ import annotations

import contextlib
from collections.abc import Sequence
from pathlib import Path

import chromadb

from rag_manual.domain.models import Chunk, RetrievedChunk


class ChromaVectorStore:
    def __init__(self, path: Path, collection: str = "manual") -> None:
        self._path = path
        self._collection_name = collection
        self._client = None

    def _get_client(self):
        if self._client is None:
            self._client = chromadb.PersistentClient(path=str(self._path))
        return self._client

    def reset(self) -> None:
        client = self._get_client()
        with contextlib.suppress(Exception):  # a coleção pode não existir ainda
            client.delete_collection(self._collection_name)  # recria do zero a cada ingestão
        client.create_collection(self._collection_name, metadata={"hnsw:space": "cosine"})

    def add(self, chunks: Sequence[Chunk], vectors: Sequence[Sequence[float]]) -> None:
        collection = self._get_client().get_collection(self._collection_name)
        collection.add(
            ids=[c.id for c in chunks],
            documents=[c.text for c in chunks],
            embeddings=[list(v) for v in vectors],
            metadatas=[{"page": c.page, "section": c.section} for c in chunks],
        )

    def search(self, vector: Sequence[float], k: int) -> list[RetrievedChunk]:
        collection = self._get_client().get_collection(self._collection_name)
        result = collection.query(query_embeddings=[list(vector)], n_results=k)
        return [
            RetrievedChunk(
                chunk=Chunk(id=chunk_id, page=meta["page"], text=doc, section=meta["section"]),
                score=1 - distance,
            )
            for chunk_id, meta, doc, distance in zip(
                result["ids"][0],
                result["metadatas"][0],
                result["documents"][0],
                result["distances"][0],
                strict=True,
            )
        ]
