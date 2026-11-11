"""Três jeitos de buscar: vetorial, por palavra (BM25) e híbrido (RRF)."""
import json
import re
from functools import lru_cache
from pathlib import Path

import chromadb
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

from config import COLLECTION, DB_PATH, MODEL


@lru_cache
def _modelo():
    return SentenceTransformer(MODEL)


@lru_cache
def _colecao():
    return chromadb.PersistentClient(path=DB_PATH).get_collection(COLLECTION)


@lru_cache
def _chunks():
    return json.loads(Path("chunks.json").read_text(encoding="utf-8"))


def _tokens(texto: str) -> list[str]:
    return re.findall(r"\w+", texto.lower())


@lru_cache
def _bm25():
    return BM25Okapi([_tokens(c["texto"]) for c in _chunks()])


def busca_vetorial(pergunta: str, k: int = 10) -> list[dict]:
    vetor = _modelo().encode([pergunta], normalize_embeddings=True)[0].tolist()
    r = _colecao().query(query_embeddings=[vetor], n_results=k)
    return [
        {"id": i, "pagina": m["pagina"], "texto": d}
        for i, m, d in zip(r["ids"][0], r["metadatas"][0], r["documents"][0])
    ]


def busca_bm25(pergunta: str, k: int = 10) -> list[dict]:
    notas = _bm25().get_scores(_tokens(pergunta))
    ordem = sorted(range(len(notas)), key=lambda i: notas[i], reverse=True)[:k]
    cs = _chunks()
    return [{"id": cs[i]["id"], "pagina": cs[i]["pagina"], "texto": cs[i]["texto"]} for i in ordem]


def busca_hibrida(pergunta: str, k: int = 10, c: int = 60) -> list[dict]:
    pontos, por_id = {}, {}
    for lista in (busca_vetorial(pergunta, 20), busca_bm25(pergunta, 20)):
        for posicao, item in enumerate(lista, start=1):
            pontos[item["id"]] = pontos.get(item["id"], 0.0) + 1 / (c + posicao)
            por_id[item["id"]] = item
    melhores = sorted(pontos, key=pontos.get, reverse=True)[:k]
    return [por_id[i] for i in melhores]


BUSCAS = {"vetorial": busca_vetorial, "bm25": busca_bm25, "hibrida": busca_hibrida}
