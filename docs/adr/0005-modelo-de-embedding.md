# 0005. Modelo de embedding: `multilingual-e5-small`

Status: aceita (padrão desde 2026-11-11)

## Contexto

O modelo original, `paraphrase-multilingual-MiniLM-L12-v2`, foi treinado para achar frases parecidas, não para achar o trecho que responde uma pergunta. Na busca vetorial ele ficou em 7/13 (MRR 0,45), abaixo do BM25.

## Decisão

Usar `intfloat/multilingual-e5-small` (cerca de 470 MB), treinado para recuperação de texto em várias línguas. Ele exige prefixos: `query: ` na pergunta e `passage: ` em cada trecho. O adaptador `SentenceTransformerEmbedder` aplica os prefixos sozinho quando o nome do modelo tem "e5".

## Resultado nas medições

Mudando só o modelo (trechos 800/150, sem reranker), a busca vetorial foi de 7/13 para 12/13 e o MRR de 0,45 para 0,87. São 5 perguntas a mais, bem acima do ruído de 1 ou 2 perguntas. É a maior melhoria medida neste projeto.

## Consequências

- Novo padrão em `config.py`. O experimento `base` fixa o MiniLM de propósito, para continuar reproduzindo os números antigos.
- A escolha da melhor configuração entre 7 índices e 5 estratégias foi feita nas mesmas 13 perguntas, então o valor absoluto (92%) tende a estar otimista. Já a diferença entre os dois modelos é grande demais para ser só isso.
- Não comparamos com modelos maiores (por exemplo `multilingual-e5-base`) para poupar disco e tempo.
