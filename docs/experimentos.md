# Experimentos

Todos os números usam o mesmo `golden.csv` (13 perguntas com resposta, não editado). Uma mudança por vez, em relação à base. Formato: `acertos/13, MRR@10`. Medido em 2026-11-11.

**Como ler:** uma pergunta vale cerca de 8 pontos de hit@3. Diferença de 1 pergunta é ruído; 2 perguntas pede cautela. Foram 7 índices e 5 estratégias (35 combinações) no mesmo conjunto pequeno, então o melhor valor entre eles tende a estar otimista.

## Configurações

| Nome | Trechos | O que muda em relação à base |
|---|---|---|
| `base` | 265 | trechos fixos de 800 caracteres, sobreposição 150, `paraphrase-multilingual-MiniLM-L12-v2` |
| `chunk400` | 687 | trechos de 400 |
| `chunk1500` | 144 | trechos de 1500 |
| `overlap0` | 236 | sem sobreposição |
| `secao` (B1) | 256 | divisão por seção, com o título da seção no começo do trecho e sem o cabeçalho de página |
| `e5` (B2) | 265 | modelo `intfloat/multilingual-e5-small` (prefixos `query: ` e `passage: `) |
| `secao_e5` (B1+B2) | 256 | divisão por seção e e5 |

O reranker (B3) é `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1` sobre os 20 melhores candidatos. Ele é uma coluna extra: "híbrida+rr" reordena os candidatos da híbrida e "vetorial+rr" os da vetorial.

## Resultados da busca

| Configuração | vetorial | bm25 | híbrida | híbrida+rr | vetorial+rr |
|---|---|---|---|---|---|
| `base` | 7/13, 0,45 | 9/13, 0,68 | 10/13, 0,62 | 10/13, 0,67 | 9/13, 0,68 |
| `chunk400` | 8/13, 0,55 | 9/13, 0,67 | 9/13, 0,63 | 10/13, 0,67 | 9/13, 0,62 |
| `chunk1500` | 6/13, 0,42 | 9/13, 0,72 | 8/13, 0,61 | 11/13, 0,82 | 11/13, 0,81 |
| `overlap0` | 6/13, 0,39 | 10/13, 0,78 | 7/13, 0,55 | 10/13, 0,69 | 8/13, 0,58 |
| `secao` (B1) | 7/13, 0,51 | 10/13, 0,75 | 9/13, 0,66 | 10/13, 0,65 | 8/13, 0,59 |
| `e5` (B2) | **12/13, 0,87** | 9/13, 0,68 | 10/13, 0,80 | 10/13, 0,67 | 9/13, 0,70 |
| `secao_e5` (B1+B2) | 12/13, 0,84 | 10/13, 0,75 | 10/13, 0,75 | 11/13, 0,71 | 10/13, 0,68 |

Arquivos: `results/eval_<nome>.txt` (traz também a lista das perguntas erradas de cada busca).

### Reprodução da base

A base foi refeita pelo código novo (depois da refatoração) e bateu com os números da primeira versão do projeto, inclusive nas perguntas erradas: vetorial 7/13 (MRR 0,45), bm25 9/13 (0,68), híbrida 10/13 (0,62). Os experimentos antigos (`chunk400`, `chunk1500`, `overlap0`) também foram refeitos e deram os mesmos números de antes.

## Conclusões por experimento

### Experimentos antigos (tamanho do trecho e sobreposição)

- **Trechos de 400:** a vetorial melhorou (8/13, 0,55). A híbrida perdeu 1 acerto no hit@3 e ficou igual no MRR.
- **Trechos de 1500:** a vetorial piorou (6/13) como esperado. O BM25 subiu no MRR (0,72).
- **Sem sobreposição:** vetorial e híbrida pioraram (7/13 para 6/13 e 10/13 para 7/13). O BM25 melhorou (10/13, 0,78). Nesta amostra, a sobreposição ajudou a vetorial e a híbrida.

### B1. Divisão por seção

A estrutura ficou como esperado: os 5 trechos da tabela da página 76 agora levam `[10 PROBLEMAS X SOLUÇÕES]`, e o cabeçalho repetido saiu do texto (0 trechos com "Motores Elétricos |").

O efeito na busca **não se separa do ruído**:

| Busca | base | `secao` | diferença |
|---|---|---|---|
| vetorial | 7/13, 0,45 | 7/13, 0,51 | mesmo hit@3, MRR +0,06 |
| bm25 | 9/13, 0,68 | 10/13, 0,75 | +1 pergunta |
| híbrida | 10/13, 0,62 | 9/13, 0,66 | -1 pergunta, MRR +0,04 |

Com o e5 também não ajudou: vetorial 12/13 nos dois, MRR 0,87 contra 0,84; híbrida 10/13 nos dois, MRR 0,80 contra 0,75. A hipótese era que o título ajudaria as perguntas de sintoma (página 76). Mas "barulho estranho", "esquentando" e "não gira" continuam errando em várias configurações, porque o título do capítulo ("10 PROBLEMAS X SOLUÇÕES") não diz qual problema cada linha da tabela descreve.

### B2. Embedding `multilingual-e5-small`

É a maior melhoria do projeto. Só trocando o modelo (trechos iguais), a vetorial foi de 7/13 para 12/13 e o MRR de 0,45 para 0,87. São 5 perguntas, bem acima do ruído. A única pergunta que a vetorial com e5 ainda erra é a do protetor contra ferrugem: o manual fala em "graxa protetiva" e "película protetora" e a pergunta usa "protetor contra ferrugem". Essa pergunta errou em 32 das 35 combinações medidas.

Efeito colateral: com o e5, a vetorial sozinha (12/13, 0,87) ficou melhor que a híbrida (10/13, 0,80). O BM25 passou a puxar para baixo. Com 13 perguntas, o hit@3 da híbrida (2 perguntas a menos) e o MRR (0,07 a menos) apontam para o mesmo lado, mas continua sendo pouca amostra.

### B3. Reranker multilíngue

O efeito é inconsistente:

- Sobre a híbrida com MiniLM: MRR de 0,62 para 0,67, mesmo hit@3 (10/13).
- Com trechos de 1500: de 8/13 para 11/13 (MRR 0,61 para 0,82). O maior ganho, mas dentro de uma configuração só.
- Com o e5, **piorou**: a vetorial (12/13, 0,87) caiu para 10/13 (0,67) ou 9/13 (0,70). Nas perguntas de sintoma, o reranker colocou a página 54 (condições de operação) no topo no lugar da tabela da página 76.

Interpretação (hipótese, não testada): quando a busca já é boa, o reranker tem pouco a corrigir e pode errar. O modelo foi treinado em perguntas e respostas de texto corrido traduzidas, não em tabelas técnicas.

### Outras combinações medidas

- `secao_e5` com reranker: 11/13 (0,71). Não passa da vetorial sem reranker.
- Reranker sobre a vetorial (`vetorial+rr`): nunca passou da vetorial com e5 sem reranker.

## Configuração escolhida

**Trechos fixos 800/150 + `multilingual-e5-small` + busca vetorial, sem reranker.** Resultado: **12/13 no hit@3 e MRR 0,87**.

Critério: só os números (hit@3 e depois MRR). Em hit@3, `e5` e `secao_e5` empatam com 12/13 na vetorial. O MRR de `e5` é maior (0,87 contra 0,84), uma diferença que é ruído, mas desempata e a configuração é a mais simples. Nenhuma combinação com reranker ou com divisão por seção superou essa.

Cuidados na leitura:

- A escolha foi feita nas mesmas 13 perguntas que serviram para medir. O 92% provavelmente está otimista. O ganho do e5 sobre o MiniLM (5 perguntas) é grande demais para ser só isso. A ordem entre `e5` e `secao_e5` não é.
- Entre as 13 perguntas, 4 caem na mesma página (76), então o resultado depende muito dessa página.
- Decisões em `docs/adr/` (0002 a 0005).

## Geração: `qwen2.5:1.5b` contra `qwen2.5:3b`

Mesma busca (vetorial com e5, 5 trechos), mesmo prompt, temperatura 0, rodando no Ollama em CPU. Só o modelo muda. Notas manuais em `results/respostas_e5_vetorial_qwen2.5-1.5b.md` e `results/respostas_e5_vetorial_qwen2.5-3b.md`. **São rascunhos para o Oséias revisar.**

| | qwen2.5:1.5b | qwen2.5:3b |
|---|---|---|
| Corretas (de 13) | 4 | 6 |
| Parciais | 1 | 1 |
| Erradas | 8 | 6 |
| Falsas recusas (página certa nos trechos) | 2 | 2 |
| Página certa citada no texto | 4 de 13 (2 só como lista de páginas) | 10 de 13 |
| Respostas que só devolveram números de página | 2 (perguntas 5 e 6) | 0 |
| Respostas com algo fora dos trechos | 4 | 3 |
| Recusa correta nas 2 sem resposta | 2 de 2 | 2 de 2 |
| Tempo para as 15 perguntas (CPU, esta máquina) | cerca de 17 min | cerca de 33 min |

Leitura honesta:

- O 3b acertou 2 perguntas a mais (6 contra 4). Com 13 perguntas e uma nota feita por leitura, isso é pouco para afirmar que é melhor em geral.
- A diferença mais clara é de comportamento: o 3b cita a página no formato `(p. N)` e escreve a resposta, em vez de devolver só uma lista de páginas.
- Os dois erram a mesma pergunta de número (parafuso M10, certo: 28 a 40 Nm), pegando a coluna errada da tabela que o PDF desorganiza. O 3b ainda inverteu a regra dos drenos do IP65 (pergunta 10).
- As falsas recusas continuaram (2 em cada), então o prompt de recusa ainda pesa. O 1.5b recusou as perguntas 1 e 8, o 3b as perguntas 7 e 8.
- O 3b copia trechos quase literalmente, o que ajuda na fidelidade e atrapalha na clareza (perguntas 4, 5 e 6).

**Efeito da busca melhor (e5 vetorial contra híbrida com MiniLM), com o mesmo `qwen2.5:1.5b`:** a placa de acertos do modelo ficou igual (4 corretas, 1 parcial, 8 erradas), mas a página certa passou de 10 para 12 entre as 13 perguntas e as falsas recusas passaram de 5 para 2. Ou seja, a busca melhorou, mas o modelo pequeno continuou sendo o gargalo, trocando o tipo de erro (menos recusas, mais respostas só com página ou com valor errado). Arquivo da primeira rodada: `results/respostas_base_hibrida_qwen2.5-1.5b.md`.

Nenhum outro modelo foi testado. O `qwen2.5:3b` é uma melhoria modesta e custa o dobro do tempo.

## O que falta testar

- Um conjunto de teste maior e escrito por usuários reais.
- Trechos por linha da tabela de problemas (problema, causa, solução).
- Expansão de consulta com sinônimos do jargão técnico (a pergunta do protetor contra ferrugem pediria isso).
- Outros modelos de embedding maiores e outro reranker.
