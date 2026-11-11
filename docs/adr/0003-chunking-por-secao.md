# 0003. Divisão por seção (`SectionAwareChunker`)

Status: implementada e medida; **não é o padrão** (sem ganho claro)

## Contexto

Na avaliação inicial, a tabela "Problemas x Soluções" (página 76) era cortada em 5 trechos e só o primeiro levava o título. Os outros viravam listas soltas de causas, sem o nome do problema. Também havia o cabeçalho de página ("Motores Elétricos | 232 ...") repetido dentro do primeiro trecho de cada página.

## Decisão

Criar o `SectionAwareChunker`:

- tira o cabeçalho repetido, que no manual segue sempre o mesmo padrão (`Motores Elétricos | N` ou `N | Motores Elétricos`, seguido do nome do capítulo em maiúsculas);
- detecta títulos numerados em maiúsculas ("5.3 MANCAIS"), inclusive os que quebram em duas linhas;
- nunca junta texto de duas seções no mesmo trecho e mantém a página;
- põe o título no começo de cada trecho, no formato `[8 MANUTENÇÃO > 8.2 LUBRIFICAÇÃO] ...`.

Resultado em estrutura: os 5 trechos da página 76 passaram a levar `[10 PROBLEMAS X SOLUÇÕES]`.

## Resultado nas medições

Veja `docs/experimentos.md`. Resumo: com o embedding original, vetorial e híbrida ficaram dentro do ruído (±1 pergunta) e o BM25 ganhou 1 acerto. Com o e5, o hit@3 da vetorial ficou igual (12/13) e o MRR caiu de 0,87 para 0,84. Não houve ganho que se possa separar do ruído.

## Consequências

- O padrão continua com trechos de tamanho fixo (mais simples e com número igual ou melhor).
- O chunker por seção fica disponível (`--chunker section`) e testado.
- Limite conhecido: o título da seção em maiúsculas ("10 PROBLEMAS X SOLUÇÕES") não diz qual problema cada linha da tabela descreve. Quem ajudaria mais é tratar a tabela como linhas (problema, causa, solução), o que não foi feito.
- O cabeçalho que aparece nas páginas é removido de forma segura: se uma página não tiver o padrão esperado, o texto fica como está.
