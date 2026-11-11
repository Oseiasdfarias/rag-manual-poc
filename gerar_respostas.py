"""Roda ask.responder para todas as perguntas do golden.csv e grava results/respostas.md."""
import csv

from ask import responder

with open("golden.csv", encoding="utf-8") as f:
    linhas = list(csv.DictReader(f, delimiter=";"))

saida = ["# Respostas geradas (qwen2.5:1.5b local, busca híbrida, k=5)\n"]
for n, l in enumerate(linhas, start=1):
    resposta, trechos = responder(l["pergunta"])
    paginas = [t["pagina"] for t in trechos]
    print(n, l["pergunta"], flush=True)
    saida.append(f"## {n}. {l['pergunta']}\n\n**Páginas esperadas:** {l['paginas']}  \n**Páginas recuperadas:** {paginas}\n\n{resposta}\n")
open("results/respostas.md", "w", encoding="utf-8").write("\n".join(saida))
