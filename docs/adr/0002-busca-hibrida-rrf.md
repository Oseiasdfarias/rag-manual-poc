# 0002. Busca híbrida com fusão RRF

Status: aceita para a busca disponível; **não é mais a busca padrão** (veja o fim)

## Contexto

Manual técnico mistura dois tipos de pergunta. Algumas têm termo exato (M10, IP65, classe F, megômetro) e a busca por palavra (BM25) acerta. Outras usam palavras diferentes das do manual ("barulho estranho" contra "ruído anormal") e a busca por significado (vetorial) ajuda.

## Decisão

Manter as duas buscas e combiná-las com RRF (Reciprocal Rank Fusion). Cada busca entrega 20 candidatos. Cada trecho ganha a soma de `1 / (60 + posição)` nas listas em que aparece. A fusão usa só a posição, então não precisa normalizar notas de escalas diferentes.

Implementação: `HybridRetriever` e `reciprocal_rank_fusion` em `application/retrieval.py`.

## Consequências

- Com o embedding original (MiniLM), a híbrida teve o melhor hit@3 (10/13), mas o BM25 sozinho teve MRR maior (0,68 contra 0,62). Com 13 perguntas, isso é empate técnico.
- Com `multilingual-e5-small`, a busca **vetorial sozinha** (12/13, MRR 0,87) passou a ser melhor que a híbrida (10/13, MRR 0,80). A parte BM25 passa a puxar para baixo resultados que o vetorial já tinha acertado.
- Por isso o padrão atual para responder é a busca vetorial. A híbrida continua implementada e é medida em todo experimento. Se o conjunto de teste crescer e mudar o quadro, a troca é só a variável `RAG_RETRIEVER`.
