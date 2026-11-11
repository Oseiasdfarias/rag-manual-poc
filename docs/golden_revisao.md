# Revisão do conjunto de teste (golden.csv)

**Este conjunto é um RASCUNHO para o Oséias revisar e reescrever com as próprias palavras.**
Foi escrito antes de rodar a avaliação (as perguntas não foram ajustadas depois de ver os resultados).

Atenção ao número de página: é o **índice do PDF usado pelo `rag-manual ingest`** (começa em 1), não o número impresso no rodapé do manual.
O `data/manual.pdf` é só a seção em português do manual trilíngue da WEG (páginas 157 a 233 do original). Por isso: **página impressa = índice + 156**.

Observação: 4 das 13 perguntas com resposta caem na mesma página (76, tabela de problemas e soluções). Se quiser variar mais, troque alguma.

| # | Tipo | Pergunta | Página(s) | Trecho de apoio |
|---|---|---|---|---|
| 1 | fato direto | Até que altitude o motor trabalha sem precisar de ajuste na potência? | 54 (impressa 210) | "os motores elétricos são projetados para operar a uma altitude limitada a 1000 m acima do nível do mar e em temperatura ambiente entre -20 °C e +40 °C" |
| 2 | fato direto | Qual a temperatura máxima da água que chega ao motor refrigerado a água? | 56 (212) | "A temperatura da água na entrada não deve exceder 40 °C." |
| 3 | fato direto | Com que frequência devo passar de novo o protetor contra ferrugem na ponta do eixo de um motor parado no estoque? | 20 (176) | "Esta película protetora deve ser reaplicada periodicamente durante o período de armazenagem (pelo menos a cada seis meses)" |
| 4 | fato direto | Quantas vezes posso dar partida seguida no motor? | 54 (210) | "Duas partidas sucessivas, sendo a primeira feita com o motor frio [...] Uma partida com o motor a quente" |
| 5 | sintoma e causa | O motor está fazendo um barulho estranho, quais as causas possíveis? | 76 (232) | "Ruído elevado/anormal: Defeito nos componentes de transmissão [...] Base desalinhada/desnivelada [...] Rolamentos danificados" |
| 6 | sintoma e causa | Motor esquentando demais, o que devo verificar? | 76 (232) | "Aquecimento excessivo no motor: Refrigeração insuficiente [...] Sobrecarga [...] Tensão muito alta / muito baixa" |
| 7 | sintoma e causa | O mancal está esquentando, o que pode ser? | 60, 76 (216, 232) | "Aquecimento do mancal: Graxa/óleo em demasia, Envelhecimento da graxa/óleo, Falta de graxa/óleo" (p. 60: "Graxa em excesso provoca aquecimento do mancal") |
| 8 | sintoma e causa | Liguei o motor e ele nem gira, nem sem carga. O que checar? | 76 (232) | "Motor não parte, nem acoplado e nem desacoplado: Interrupção na alimentação, Fusíveis queimados, Erro na conexão do motor, Mancal travado" |
| 9 | número | Qual o aperto em Nm para um parafuso sextavado M10 com junta rígida? | 73 (229) | Tabela 8.16: "Parafuso sextavado externo/interno (junta rígida) - 3,5 a 5 / 6 a 9 / 14 a 20 / 28 a 40 ..." (M10 = 28 a 40 Nm; conferir a coluna na tabela, a extração perde o cabeçalho) |
| 10 | sigla (IP) | O que fazer com os drenos de um motor IP65 instalado em lugar muito úmido? | 26 (182) | "Para motores com grau de proteção IP56, IP65 ou IP66, os drenos devem permanecer na posição fechada, sendo abertos apenas durante a manutenção do motor." |
| 11 | número | Qual a temperatura de alarme e de desligamento do enrolamento com isolamento classe F? | 42 (198) | Tabela 6.7: "Enrolamento ... F 130 155" (alarme 130 °C, desligamento 155 °C) |
| 12 | procedimento | Como se faz a medição da resistência de isolamento do motor? | 23, 24 (179, 180) | "medida com um megômetro e com o motor parado, frio e completamente desconectado [...] após a tensão ser aplicada pelo período de um minuto" |
| 13 | procedimento | Qual o passo a passo para colocar graxa nos rolamentos com o motor parado? | 68 (224) | "Limpar as proximidades do orifício de entrada de graxa. Abrir a proteção [...] Colocar aproximadamente metade da graxa total [...] girar o motor durante aproximadamente 1 (um) minuto [...] Desligar o motor e colocar o restante da graxa." |
| 14 | sem resposta | Quanto custa um motor trifásico de 10 cv novo? | 0 | O manual não traz preços (busca por "preço" sem resultado). |
| 15 | sem resposta | Qual o nível de ruído em dB(A) de um motor de 4 polos carcaça 132? | 0 | O manual não traz níveis de ruído em dB (busca por "dB" e "decibel" sem resultado). |

## Pontos para você decidir
- Pergunta 9: o PDF vira sopa de números na tabela; confira no PDF original a coluna do M10.
- Pergunta 12: a resposta completa vai até a página 25 (tabelas de tensão e de avaliação). Deixei 23 e 24 como o núcleo do procedimento.
- Pergunta 4: o trecho responde "duas partidas seguidas (uma a frio e outra após o motor parar) ou uma a quente".
