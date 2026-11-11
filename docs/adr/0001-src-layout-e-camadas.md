# 0001. Layout `src` e arquitetura em camadas

Status: aceita (2026-11-11)

## Contexto

O projeto começou com seis scripts soltos na raiz (`ingest.py`, `search.py`, `ask.py`, `eval.py`...). Eles dividiam estado global (`lru_cache`, modelo carregado no import) e importavam uns aos outros pelo nome do arquivo. Isso funcionou para a primeira medição, mas travava três coisas: testar sem baixar modelo, trocar uma peça (embedding, reranker, LLM) e rodar vários experimentos em configurações diferentes.

## Decisão

- Pacote `rag_manual` em `src/`, instalado com `pip install -e .`, com o comando `rag-manual`.
- Quatro camadas: `domain` (objetos e portas), `application` (casos de uso), `infrastructure` (adaptadores), `composition` (monta tudo).
- Regra: o domínio não importa nada das outras camadas. A aplicação só conhece as portas. Só `composition.py` conhece as classes concretas.
- As portas são `typing.Protocol`. Os fakes dos testes não precisam herdar de nada.
- Modelos pesados carregam no primeiro uso, dentro do adaptador.

## Consequências

- Os testes unitários usam fakes em memória e rodam em menos de um segundo.
- Adicionar uma busca ou trocar o LLM mexe em um ou dois arquivos (ver `docs/arquitetura.md`).
- Mais arquivos e mais indireção do que um script. Para uma PoC de 500 linhas isso é um custo pequeno, aceito porque o objetivo do projeto também é mostrar a organização.
- A refatoração não mudou os resultados: a base reproduziu os números antigos (vetorial 7/13 e MRR 0,45; bm25 9/13 e 0,68; híbrida 10/13 e 0,62).
