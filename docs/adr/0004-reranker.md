# 0004. Reranker

Status: implementado e medido; **desligado por padrão**

## Contexto

Um reranker (cross-encoder) lê a pergunta e o trecho juntos e dá uma nota. É mais preciso que comparar vetores, mas mais lento, então roda só nos candidatos que a busca já trouxe.

## Decisão

Implementar `RerankingRetriever` como decorator de qualquer outra busca (`application/retrieval.py`), com o modelo `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` (multilíngue, cerca de 470 MB), sobre os 20 melhores candidatos.

## Resultado nas medições

Veja `docs/experimentos.md`. O efeito depende da configuração e não é consistente:

- Sobre a híbrida com o embedding original, melhorou o MRR (0,62 para 0,67) sem mudar o hit@3 (10/13).
- Com trechos de 1500 caracteres, subiu de 8/13 para 11/13 (MRR de 0,61 para 0,82). É o maior ganho do reranker e fica dentro de uma única configuração.
- Com o embedding e5, **piorou**: o hit@3 caiu de 12/13 (vetorial) para 9/13 e 10/13, e o MRR de 0,87 para 0,70 e 0,67. O reranker empurrou para o topo a página 54 (condições de operação) em perguntas cuja resposta está na tabela da página 76.

## Consequências

- Reranker desligado no padrão. A melhor configuração medida não o usa.
- Fica disponível com `--reranker` (ou `RAG_RERANKER_MODEL`).
- Não testamos outro reranker. Um modelo treinado em texto técnico, ou o reranker aplicado a trechos por seção com tabelas tratadas, poderia mudar o quadro. É uma hipótese, não um resultado.
