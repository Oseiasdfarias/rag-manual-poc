# Respostas geradas (qwen2.5:1.5b local, busca vetorial com e5, k=5)

## 1. Até que altitude o motor trabalha sem precisar de ajuste na potência?

**Páginas esperadas:** 54  
**Páginas recuperadas:** [54, 55, 55, 28, 76]

Não encontrei isso no manual.

## 2. Qual a temperatura máxima da água que chega ao motor refrigerado a água?

**Páginas esperadas:** 56  
**Páginas recuperadas:** [56, 56, 53, 36, 54]

p. 56, Tabela 7.4

## 3. Com que frequência devo passar de novo o protetor contra ferrugem na ponta do eixo de um motor parado no estoque?

**Páginas esperadas:** 20  
**Páginas recuperadas:** [22, 13, 53, 59, 59]

Não encontrei isso no manual.

## 4. Quantas vezes posso dar partida seguida no motor?

**Páginas esperadas:** 54  
**Páginas recuperadas:** [54, 52, 45, 44, 54]

De acordo com a informação fornecida no trecho [p. 54], você pode fazer duas partidas sucessivas no motor:

1. Primeira partida: Com o motor frio, isto é, com seus enrolamentos na temperatura ambiente.
2. Segunda partida: Após o motor ter desacelerado até atingir seu repouso.

Portanto, a resposta à pergunta "Quantas vezes posso dar partida seguida no motor?" é:

Pode fazer duas partidas sucessivas no motor, sendo a primeira feita com o motor frio e a segunda após ele ter desacelerado.

## 5. O motor está fazendo um barulho estranho, quais as causas possíveis?

**Páginas esperadas:** 76  
**Páginas recuperadas:** [76, 54, 76, 76, 72]

p. 76  
p. 54  
p. 72

## 6. Motor esquentando demais, o que devo verificar?

**Páginas esperadas:** 76  
**Páginas recuperadas:** [76, 76, 6, 59, 5]

p. 76
p. 59

## 7. O mancal está esquentando, o que pode ser?

**Páginas esperadas:** 60|76  
**Páginas recuperadas:** [60, 1, 76, 59, 47]

p. 221, Tabela 8.9; p. 222, Tabela 8.10 e Tabela 8.11

## 8. Liguei o motor e ele nem gira, nem sem carga. O que checar?

**Páginas esperadas:** 76  
**Páginas recuperadas:** [54, 54, 76, 59, 32]

Não encontrei isso no manual.

## 9. Qual o aperto em Nm para um parafuso sextavado M10 com junta rígida?

**Páginas esperadas:** 73  
**Páginas recuperadas:** [73, 30, 31, 73, 31]

p. 229, Tabela 8.16

Apertar em Nm: 40 a 70

## 10. O que fazer com os drenos de um motor IP65 instalado em lugar muito úmido?

**Páginas esperadas:** 26  
**Páginas recuperadas:** [26, 59, 26, 27, 59]

De acordo com a informação fornecida no manual:

- Para motores com grau de proteção IP65, os drenos devem permanecer na posição fechada (ver Figura 5.5 na página 177), sendo abertos apenas durante a manutenção do motor.

Portanto, para um motor IP65 instalado em lugar muito úmido:

- Deve manter-se o dreno na posição fechada.
- Não deve ser aberto periodicamente para permitir a saída da água condensada.

## 11. Qual a temperatura de alarme e de desligamento do enrolamento com isolamento classe F?

**Páginas esperadas:** 42  
**Páginas recuperadas:** [42, 25, 58, 42, 40]

A temperatura máxima de operação para os enrolamentos classificados como F é 130°C. Portanto:

- Temperatura Máxima de Alarme: 130°C
- Temperatura Máxima de Desligamento: 155°C

## 12. Como se faz a medição da resistência de isolamento do motor?

**Páginas esperadas:** 23|24  
**Páginas recuperadas:** [23, 24, 24, 25, 73]

A medida da resistência de isolamento do motor é realizada seguindo os passos abaixo:

1. A área deve ser segura para a medição.
2. O motor deve estar parado, frio e desconectado da rede elétrica.
3. Usar um megômetro para medir a resistência de isolamento.
4. As medições devem ser feitas após aplicar uma tensão de 500 V por 1 minuto (para motores com tensão nominal até 1,1 kV) ou 250 V por 1 minuto (para motores acima de 1,1 kV).
5. A resistência deve ser corrigida para a temperatura de 40 °C.
6. Todos os equipamentos externos devem estar desconectados e aterrados antes da medição.

É importante lembrar que o processo deve ser realizado em um local seguro e com precauções de segurança, como descarregamento dos terminais elétricos antes e depois das medições para evitar risco de choque.

## 13. Qual o passo a passo para colocar graxa nos rolamentos com o motor parado?

**Páginas esperadas:** 68  
**Páginas recuperadas:** [68, 68, 69, 3, 70]

Passos para colocar graxa nos rolamentos quando o motor está parado:

1. Limpar as proximidades do orifício de entrada de graxa.
2. Abrir a proteção da entrada de graxa.
3. Colocar aproximadamente metade da graxa total recomendada na placa de identificação do motor e girar o motor durante aproximadamente 1 (um) minuto na rotação nominal;
4. Desligar o motor e colocar o restante da graxa.
5. Recolocar a proteção de entrada de graxa e tampa da saída de graxa.

Este procedimento é aplicado para relubrificação dos rolamentos com motores parados, seguindo as instruções específicas do motor em questão (por exemplo, motores IEEE Std 841).

## 14. Quanto custa um motor trifásico de 10 cv novo?

**Páginas esperadas:** 0  
**Páginas recuperadas:** [57, 55, 65, 61, 62]

Não encontrei isso no manual.

## 15. Qual o nível de ruído em dB(A) de um motor de 4 polos carcaça 132?

**Páginas esperadas:** 0  
**Páginas recuperadas:** [63, 55, 62, 48, 67]

Não encontrei isso no manual.

---

# Avaliação manual das respostas (RASCUNHO para o Oséias revisar)

Notas feitas por leitura, conferindo as respostas contra o texto do manual (páginas 23 a 26, 54, 56, 68, 73 e 76 do `data/manual.pdf`). Ainda não foram revisadas pelo Oséias. Modelo: qwen2.5:1.5b, temperatura 0, busca vetorial com `multilingual-e5-small`, k=5. Mesmo critério de `respostas_base_hibrida_qwen2.5-1.5b.md`.

| # | Correta? | Citou a página certa? | Inventou algo fora dos trechos? | Observação |
|---|---|---|---|---|
| 1 | não | não | não | Falsa recusa. A página 54 era o 1º trecho. |
| 2 | não | sim (p. 56) | não | Só disse "p. 56, Tabela 7.4", sem o valor (40 °C). |
| 3 | não | não | não | Recusou. A página 20 não foi recuperada, então a recusa foi o comportamento seguro. |
| 4 | sim | sim (p. 54) | não | Duas partidas seguidas, a 1ª a frio. Não citou a opção "uma a quente". |
| 5 | não | só lista as páginas | não | Respondeu apenas "p. 76, p. 54, p. 72", sem nenhuma causa. |
| 6 | não | só lista as páginas | não | Respondeu apenas "p. 76, p. 59", sem nenhuma causa. |
| 7 | não | não | sim | Citou "p. 221, Tabela 8.9; p. 222...", páginas impressas que não estão entre os trechos recuperados, e não respondeu nada. |
| 8 | não | não | não | Falsa recusa. A página 76 era o 3º trecho. |
| 9 | não | não (citou a impressa, 229) | sim | Disse "40 a 70". Na tabela, M10 é 28 a 40 Nm (40 a 70 mistura outras colunas). |
| 10 | sim | não | não | Dreno fechado, aberto só na manutenção. Certo. |
| 11 | sim | não | não | 130 °C de alarme e 155 °C de desligamento, certo. |
| 12 | parcial | não | sim | Megômetro, motor parado e frio, 1 minuto, 500 V e correção para 40 °C certos. "250 V acima de 1,1 kV" não está no manual (a Tabela 5.3 usa faixas de 1000, 2500 V...). |
| 13 | sim (com falhas) | não | sim (leve) | Passo a passo fiel, mas pulou "remover a tampa de saída de graxa" e deslocou a observação do IEEE Std 841 para o fim. |
| 14 | sim (recusa) | n/a | não | "Não encontrei isso no manual." |
| 15 | sim (recusa) | n/a | não | "Não encontrei isso no manual." |

**Resumo:** das 13 perguntas com resposta, 4 corretas, 1 parcial, 8 erradas. Falsas recusas (página certa nos trechos): 2 (perguntas 1 e 8). Páginas certas citadas no texto: 4 de 13, mas em 2 delas (5 e 6) só como lista de páginas, sem conteúdo. Recusa correta nas 2 sem resposta: 2 de 2.

A página certa estava entre os 5 trechos em 12 das 13 perguntas (só a pergunta 3 ficou sem). Nessas 12, o modelo acertou 4 e deu 1 parcial. Duas respostas (5 e 6) devolveram só números de página.
