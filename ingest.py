"""Lê o PDF, divide em trechos guardando a página e grava no Chroma."""
import json
import re
import sys
from pathlib import Path

import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from config import CHUNK, COLLECTION, DB_PATH, MODEL, OVERLAP


def limpar(texto: str) -> str:
    texto = re.sub(r"-\n(\w)", r"\1", texto)  # junta palavra hifenizada no fim da linha
    texto = re.sub(r"\s+", " ", texto)        # quebras e espaços repetidos viram um espaço
    return texto.strip()


def dividir(texto: str, tamanho: int, sobra: int) -> list[str]:
    """Corta em trechos de até `tamanho` caracteres, preferindo terminar num ponto final."""
    trechos, inicio = [], 0
    while inicio < len(texto):
        fim = min(inicio + tamanho, len(texto))
        if fim < len(texto):
            corte = texto.rfind(". ", inicio + tamanho // 2, fim)
            if corte != -1:
                fim = corte + 1
        trechos.append(texto[inicio:fim].strip())
        if fim >= len(texto):
            break
        inicio = fim - sobra
    return [t for t in trechos if len(t) > 50]  # descarta restos muito curtos


def main(pdf: Path) -> None:
    leitor = PdfReader(pdf)
    chunks = []
    for n, pagina in enumerate(leitor.pages, start=1):
        texto = limpar(pagina.extract_text() or "")
        for i, t in enumerate(dividir(texto, CHUNK, OVERLAP)):
            chunks.append({"id": f"p{n}-c{i}", "pagina": n, "texto": t})

    print(f"{len(leitor.pages)} páginas, {len(chunks)} trechos")
    if not chunks:
        sys.exit("Nenhum texto extraído: o PDF deve ser imagem e precisaria de OCR.")

    modelo = SentenceTransformer(MODEL)
    vetores = modelo.encode(
        [c["texto"] for c in chunks], normalize_embeddings=True, show_progress_bar=True
    )

    cliente = chromadb.PersistentClient(path=DB_PATH)
    try:
        cliente.delete_collection(COLLECTION)  # recria do zero a cada ingestão
    except Exception:
        pass
    colecao = cliente.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})
    colecao.add(
        ids=[c["id"] for c in chunks],
        documents=[c["texto"] for c in chunks],
        embeddings=vetores.tolist(),
        metadatas=[{"pagina": c["pagina"]} for c in chunks],
    )
    Path("chunks.json").write_text(json.dumps(chunks, ensure_ascii=False), encoding="utf-8")
    print("Ingestão concluída.")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "data/manual.pdf"))
