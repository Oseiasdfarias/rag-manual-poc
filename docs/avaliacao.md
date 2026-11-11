# Avaliação

## Conjunto de teste (golden set)

Arquivo `golden.csv`, separado por `;`, com duas colunas:

| Coluna | Significado |
|---|---|
| `pergunta` | a pergunta, como um técnico faria |
| `paginas` | páginas corretas, separadas por `\|`. `0` quando o manual não tem a resposta |

São 15 perguntas, um conjunto de teste inicial (em revisão): 13 têm resposta no manual e 2 não têm. Detalhes e dúvidas em `docs/golden_revisao.md`.

A página é o **índice do PDF usado** (começa em 1), não o número impresso. Página impressa = índice + 156.

O `golden.csv` não é alterado durante os experimentos. Todas as configurações usam as mesmas perguntas.

## Métricas de busca

Calculadas só nas 13 perguntas com resposta. Cada busca devolve até 10 trechos; a página do trecho é comparada com as páginas corretas.

- **hit@3:** a pergunta conta como acerto se alguma página correta aparece entre os 3 primeiros resultados.
- **MRR@10:** média de 1 dividido pela posição da primeira página correta nos 10 primeiros resultados. Vale 0 se não aparece. Premia quem coloca a página certa mais perto do topo.

As funções estão em `application/evaluation.py` (`hit_at_k`, `reciprocal_rank`, `mean_reciprocal_rank`) e são puras, com testes.

### Como ler os números

Com 13 perguntas, **uma pergunta vale cerca de 8 pontos percentuais** de hit@3. Uma diferença de 1 pergunta é ruído, e de 2 também deve ser lida com cautela. O MRR é mais sensível a mudanças de posição, mas também varia pouco com tão poucas perguntas. Quatro das 13 perguntas caem na mesma página (76), o que pesa nos números.

Por isso as tabelas deste projeto servem para comparar estratégias, não para prometer uma precisão.

## Avaliação da geração

A geração (resposta do LLM) não tem métrica automática. A nota é manual, feita lendo cada resposta e conferindo no trecho do manual. É um **rascunho para o Oséias revisar**.

Para cada uma das 13 perguntas com resposta, três perguntas:

1. **Correta?** `sim`, `parcial` ou `não`. Parcial quando acerta uma parte e erra ou omite outra importante.
2. **Citou a página certa no texto?** A página citada no formato `(p. N)` precisa ser uma das páginas corretas do `golden.csv`.
3. **Inventou algo fora dos trechos?** `sim` quando a resposta traz informação que não está nos trechos enviados ao modelo.

Para as 2 perguntas sem resposta no manual, vale só: o modelo recusou (`Não encontrei isso no manual.`)?

Uma recusa quando a página certa estava nos trechos é chamada de **falsa recusa**.

Os resultados ficam em `results/respostas_*.md`.

## Como rodar

```bash
make eval                    # as buscas, com a configuração padrão
rag-manual experiment --list # lista os experimentos
make experiments             # todos, com reranker (grava em results/)
make answers                 # gera as respostas das 15 perguntas
```
