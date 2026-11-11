# 0006. Modelo gerador (LLM)

Status: aceita (a nota de qualidade ainda é rascunho para revisão)

## Contexto

A geração roda localmente com o Ollama, para não depender de API paga. Na primeira avaliação, o `qwen2.5:1.5b` dava muitas falsas recusas ("Não encontrei isso no manual") mesmo com a página certa entre os trechos.

## Decisão

- O LLM é escolhido por variável de ambiente (`LLM_MODEL`, `LLM_BASE_URL`). O código fala o protocolo da OpenAI, que o Ollama também aceita.
- Comparar `qwen2.5:1.5b` com `qwen2.5:3b` (cerca de 1,9 GB) usando a mesma busca (vetorial com e5, 5 trechos, temperatura 0) e o mesmo prompt.
- Nenhum outro modelo foi baixado, para poupar disco.

## Resultado

Veja `docs/experimentos.md`. Resumo, com nota manual (rascunho a revisar):

- `qwen2.5:1.5b`: 4 corretas, 1 parcial e 8 erradas, em 13 perguntas. Citou a página certa em 4 de 13 (em 2 delas só como lista de páginas, sem resposta).
- `qwen2.5:3b`: 6 corretas, 1 parcial e 6 erradas. Citou a página certa em 10 de 13.
- A diferença de 2 perguntas é pequena para uma amostra de 13. A mudança de comportamento (cita a página e escreve a resposta) é mais clara que a de nota.
- O 3b levou o dobro do tempo em CPU.

## Consequências

- O código aceita qualquer modelo pela variável `LLM_MODEL`. O padrão do código continua `gpt-4o-mini` (API OpenAI), como antes. Quem usa o Ollama escolhe o modelo pela variável.
- Para o Ollama local, a recomendação é o `qwen2.5:3b` se o tempo de resposta não for um problema. Os dois erram a pergunta do parafuso M10 e têm falsas recusas, então a geração continua sendo o ponto mais fraco do sistema.
- A nota por pergunta é um rascunho feito por leitura. Antes de citar os números fora daqui, o Oséias precisa conferir.
- Nenhum outro modelo foi baixado, para poupar disco.
