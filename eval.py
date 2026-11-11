"""Mede a busca: hit@k e MRR para cada estratégia, listando os erros."""
import csv

from search import BUSCAS


def carregar(caminho: str = "golden.csv") -> list[dict]:
    with open(caminho, encoding="utf-8") as f:
        linhas = csv.DictReader(f, delimiter=";")
        casos = [
            {"pergunta": l["pergunta"], "paginas": {int(p) for p in l["paginas"].split("|")}}
            for l in linhas
        ]
    return [c for c in casos if c["paginas"] != {0}]  # sem resposta: avaliado só na parte 6


def avaliar(nome: str, busca, casos: list[dict], k: int = 3) -> None:
    acertos, soma_rr = 0, 0.0
    for c in casos:
        paginas = [t["pagina"] for t in busca(c["pergunta"], 10)]
        posicao = next((i for i, p in enumerate(paginas, start=1) if p in c["paginas"]), None)
        if posicao:
            soma_rr += 1 / posicao
        if posicao and posicao <= k:
            acertos += 1
        else:
            print(f"  [{nome}] errou: {c['pergunta']}  esperado {sorted(c['paginas'])}, veio {paginas[:k]}")
    n = len(casos)
    print(f"{nome:9s} hit@{k} = {acertos}/{n} ({acertos / n:.0%})   MRR@10 = {soma_rr / n:.2f}\n")


if __name__ == "__main__":
    casos = carregar()
    for nome, busca in BUSCAS.items():
        avaliar(nome, busca, casos)
