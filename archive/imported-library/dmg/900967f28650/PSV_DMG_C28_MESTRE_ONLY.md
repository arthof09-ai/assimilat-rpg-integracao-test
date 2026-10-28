# PSV DMG C28 — Banco de efeitos com contrato de entrega, aferição exata de defesa e diagnóstico RI/FIP

**21/10/2026 — MESTRE-SIDE / TEST — OP-DMG-CORPUS-EMP-01 — CM-000001**  
**Baseline:** C27 + adendo fora do G1 (Biblioteca Mestre) · **Norma:** DMG-RANK-01 v1.1 INALTERADA  
**Produção / Party / O Primeiro:** HOLD / NO-WRITE · **NAC-PASS global:** HOLD · **F0:** 4/8 HOLD.

## 1. Contrato de continuidade e ANTES → DEPOIS

**ANTES:** G1 estrutural de Bestas fechado em **411/411 Page-IDs**, com RE de ataque individual não certificado no corpus C22–C27; adendo C27 localizara casos mais documentados fora do G1. F0-A5 0/7 originais autenticados. O problema não era falta de contagem de páginas, mas **ponte documental RE/FIP × efeito, acionamento/custo e redução por defesa**.

**DEPOIS (C28):** 12 páginas físicas de itens/equipamentos distintas e **19 linhas de contrato de efeito** foram indexadas sem criar itens novos. Cinco diagnósticos *não normativos* de FIP do **item** × banda de DME da norma, 10 células exatas RDF+Selo, 8 níveis **hipotéticos** de resistência a Raio, 9 decomposições legadas, 8 cenários de permanência de Lua de Sangue, 8 fixtures lógicos Selo multi-alvo/evento, 8 modelos de diluição de carga da Manopla, e uma taxonomia rastreável de 7 hipóteses. G5 individual do efeito permanece **HOLD**; os dados não criam RE por inferência.

**Status C28:** ACEITE TÉCNICO LOCAL nas operações de leitura, taxonomia e matemática, **NÃO** aceite de balanceamento normativo, nem transição formal F0–F18. Nenhum escritor canônico/epoch/lease/ACK presumido.

## 2. Autoridades reabertas e princípio de classificação

Fontes superiores aplicadas: [DMG-RANK](https://app.notion.com/p/3f2c2b324ede815498cddb7844245f7e); [Atlas](https://app.notion.com/p/3eec2b324ede81ea8920c52473ecc3ab); [Metodologia](https://app.notion.com/p/3f3c2b324ede81ab8d8ec1c7cce760b3); [QA](https://app.notion.com/p/3f3c2b324ede815cb014dc6294f40170); [OP-DMG](https://app.notion.com/p/3f3c2b324ede813e9fa0c87ebdea0b29). O Atlas separa **RN** da Besta, **RI** do equipamento, **RIn** da matéria-prima, **FIP interna** do item e **RE** de um efeito particular. A DMG-RANK exige *efeito → RE/FIP competente → perfil de entrega → orçamento → fórmula*; quando o dano já é canônico ele é preservado. **FIP do item não comprova, por si só, o RE de cada ataque, componente ou modo.**

### 2.1 Limites literais da DMG-RANK v1.1

Banda padrão Ouro Entrada: **22–28 DME**; Ouro Negro Entrada **38–48**; Ouro Negro Média **59–69**; Ouro Negro Ápice **83–96**; Lendário Ápice **137–160**. Essas faixas valem para um efeito padrão, alvo único, Ação Padrão, sem hard-control/bypass maior; não são *pass/fail automático* de artefato, DoT, bônus especializado, múltiplos alvos ou efeito com custo e defesa. A DMG-RANK afirma ainda que arma mágica classificada pode trazer dano intrínseco total comparável ao RI/RE depois de seus riders; aqui essa ponte é usada apenas como **diagnóstico candidato de item** e não como certificação RE do ataque.

## 3. Matriz de fontes físicas, denominadores e arquitetura anti-duplicação

Fonte de verdade: a ficha Notion Mestre específica por **Page-ID**; CSV é índice laboratorial. 19 linhas de contrato não são 19 itens, mas **12 páginas de origem**; a Lâmina e o Martelo têm modos/defesas distintos; o Cajado tem cinco efeitos numericamente distintos; danos legados e linhas de controle aparecem no mesmo inventário sem serem somados. Os dados estão no CSV `C28_PRIMARY_EFFECT_CONTRACTS.csv`, com literal, natureza, entrega, PA, frequência, restrição e status de RE.

| Fonte | Resultado/documentação relevante |
|---|---|
| [Manopla](https://app.notion.com/p/3f5c2b324ede81f5ac62fb940204cdac) | Ouro–Entrada do **item**; +`5d8+3` Raio no ataque já acertado, 22 PA, um uso por 8h; lentidão −3m apenas se Raio >0 pós-resistência |
| [Lâmina](https://app.notion.com/p/3f5c2b324ede81e9aa8ec51f568600e8) | ON–Entrada do item; `7d8+15` Cortante, uma Ação Padrão; ancoragem defensiva é reação separada 18 PA e 1/8h |
| [Martelo](https://app.notion.com/p/3f5c2b324ede81658982d8f47b3ad647) | ON–Média do item; `8d10+12` Impacto por ataque; +`6d8` somente em estrutura não viva com 25 PA 1/8h |
| [Selo](https://app.notion.com/p/3f5c2b324ede81d0874ed4d96752812c) | Lendário–Entrada; reação consumível 55 PA, protege até 3 alvos de **uma mesma ocorrência**; redução até 60 por alvo pós-RD |
| [Anel](https://app.notion.com/p/3f5c2b324ede81ceabf6fc2b97344e43) | ON–Baixa por retorno espacial preparado; não há dano ofensivo numérico |
| [Pó](https://app.notion.com/p/3f5c2b324ede8145a12febac8558aeb8) | Prata–Entrada por defesa de frio climático: até 12 pontos por ocorrência ambiental durante 30 min; não é RD anti-magia Gelo |
| [Estandarte](https://app.notion.com/p/3f5c2b324ede816a9683e0ad40bad4b3) e [Véu](https://app.notion.com/p/3f5c2b324ede81bab332f518b2e6a211) | Controle negativo: classificação elevada por proteção mental/ocultação sem dano |
| [Adaga Serpente](https://app.notion.com/p/3edc2b324ede811787a0de913622b14d) | Adaga ON de fonte legada, FIP não específica; `5d4+5d8+10`; veneno `3d12`/turno sob falha CON CD25; duração e custo ambíguos |
| [Cajado Eclipse](https://app.notion.com/p/1cdc2b324ede82ed892f815f21f79ac1) | Cajado com passivo `+7d8`, Lua de Sangue `20d8` contra inimigos e `16d8` cura aliada por rodada 3 rodadas, `20d8` toque; demais condições preservadas |
| [Espada Lendário](https://app.notion.com/p/3edc2b324ede81ab9e22e168f6d939a9) | Lendário–Ápice analítico com `14d20+14d12+14d8+14d10+390+FOR`, DME 768 **antes da FOR**, desgaste avançado; outlier histórico |
| [Arco Elemental](https://app.notion.com/p/3edc2b324ede8156849bf1aae0ce9fb5) | Lendário de item com dano-base `8d8+25` e `+8d12+10` contra elementais; condição do bônus preservada |

## 4. Auditoria das bandas de referência — RI/FIP do item não equivale a RE

| Diagnóstico | DME | Banda do RI/FIP declarada | Leitura |
|---|---:|---|---|
| Manopla: incremento `5d8+3` | **25,5** | Ouro Entrada 22–28 | Encaixe numérico, porém rider sem Ação Padrão adicional, 22 PA e raridade de ativação |
| Lâmina: ataque `7d8+15` | **46,5** | ON Entrada 38–48 | Encaixe numérico condicionado ao golpe padrão |
| Martelo: ataque normal `8d10+12` | **56** | ON Média 59–69 | Três pontos abaixo do piso Média, mas o perfil total inclui demolição |
| Martelo: golpe único contra estrutura `8d10+12+6d8` | **83** | ON Média 59–69 | Só contra estruturas não vivas, 25 PA e 1/8h. Valor equivalente ao piso ON Ápice *não promove o item/ataque contra criaturas* |
| Espada do Lendário, antes de FOR | **768** | Lendário Ápice 137–160 | Fora da banda comum, mas é outlier histórico degradado citado expressamente pela norma, não âncora para inflar o centro |

**Conclusão:** aplicar a FIP do item ao DME de uma habilidade é diagnóstico dirigido, não recategorização canônica. A inconsistência superficial do Martelo não basta para propor mudança; a fonte especifica especialização, frequência, custo e alvo. Nenhuma fonte examinada neste lote declara inequivocamente `RE deste ataque = X`; portanto **0/19 foram certificados como RE individual**.

## 5. Prova matemática de mitigação em defensores com RDF real e Selo

Fontes dos defensores reabertas: [Rinolupo](https://app.notion.com/p/034c2b324ede83ffa7118144011beaf3) RDF10; [Guardião Pétreo P3](https://app.notion.com/p/549c2b324ede8375b21181335038aad1) RDF15; [Guardião Pétreo O1](https://app.notion.com/p/b0ec2b324ede835a927601b4cbd8fca6) RDF20; [Guardião Pétreo O5](https://app.notion.com/p/371c2b324ede837fad4c01bbfe9a95fb) RDF25. Compare **um ataque que acertou**, com natureza física certificada na arma, `max(0, resultado − RDF)`; então aplique o Selo apenas sobre o residual: `max(0, resultado − RDF − 60)`.

| Ataque | RDF | Média pós-RDF sem Selo | Média residual com Selo | Probabilidade de residual positivo |
|---|---:|---:|---:|---:|
| Lâmina | 15 | 31.5000 | 0.00000000 | 0.00000000 |
| Martelo | 15 | 41.0000 | 0.02002935 | 0.007114 |
| Lâmina | 10 | 36.5000 | 0.000000477 | 0.000000477 |
| Martelo | 10 | 46.0000 | 0.12963750 | 0.036877 |

O efeito vale somente sob as seguintes premissas: acerto verdadeiro; reação disponível; 55 PA; Selo não consumido antes; elegibilidade espacial até 4m; não há imunidade/controle que bloqueie reação; e RDF aplicável ao dano físico daquele ataque. **Não** são valores de DPT/ação/combate ou playtest. O Selo não protege três eventos de multi-hit separados; a tabela de 8 cenários `C28_SELO_SCOPE_HYPOTHETICAL_EVENT_FIXTURES.csv` demonstra o erro dessa extrapolação, com exemplos previamente identificados como **hipotéticos**.

A matemática foi feita sobre a distribuição completa de dados: não se usou `max(0, DME−RDF−60)` como substituto da esperança pós-truncamento. Células com probabilidade diminuta preservaram o valor exato em frações, não foram arredondadas a zero sem suporte.

## 6. Raio, resistência e chance do rider da Manopla

`5d8+3` tem suporte de **8–43**, DME 25,5. A lentidão de −3m só é aplicada se o dano de Raio *efetivamente positivo* atravessar as proteções. O cálculo abaixo usa resistências hipotéticas — **NÃO** RDF física de Rinolupo/Guardião, nem defesa de criaturas inventadas.

| Resistência elétrica hipotética | Dano médio Raio líquido | Chance de −3 m após um acerto confirmado |
|---:|---:|---:|
| 20 | 5.864868 | 83.038% |
| 25 | 2.319092 | 50.000% |
| 30 | 0.534485 | 16.962% |

Com proteção elétrica de 43 ou imunidade, a lentidão não dispara pelo contrato. A chance de acerto e crítico original permanece fora do modelo. Uma carga usada uma vez por descanso de 8h não equivale a um bônus repetível em todos os acertos: a tabela de diluição `C28_MANOPLA_SINGLE_CHARGE_PER_CONFIRMED_HIT_COUNT.csv` calcula a contribuição de uma única carga distribuída hipoteticamente por N acertos confirmados, sem alegar DPT.

## 7. Fontes legadas, efeitos temporais e vieses

- **Adaga Serpente:** ataque literal de DME **45**; veneno condicional DME **19,5 por tick** sob falha de Constituição CD25, mas a fonte não define duração final ou quantos ticks ocorrerão; o texto isolado `35 de PA` tampouco identifica inequivocamente o custo do modo. Não somar `45 + 19,5×N` como dano garantido.
- **Cajado Eclipse:** Lua de Sangue DME **90 contra um inimigo por rodada** e **72 de cura para um aliado por rodada**, num efeito de 6m e duração até três rodadas; uma permanência **hipotética** de 0/1/2/3 rodadas corresponde a 0/90/180/270 de magnitude média ao inimigo, mas não comprova acerto, permanência, disponibilidade de alvos, imunidades, nem ação de ativação. Drenagem passiva `7d8` é bônus no ataque elegível, não golpe autônomo. O Toque Vampírico `20d8` cura o usuário pelo valor drenado; não converter ambos em 180 de dano.
- **Espada histórica:** DME 768 antes de FOR, suporte 446–1090, porém a manutenção 600 PA/dia, o próprio bônus +60 FOR e a condição de desgaste exigem reconciliação de uso e stacking. Artefato único não fixa média do rank Lendário.
- **Estandarte/Anel/Pó/Véu/Selo:** controles negativos mostram que RI e FIP não são medidas unidimensionais de dano.
- **Seleção:** a coorte é dirigida para fichas mecanicamente completas, sem amostra aleatória; 19 linhas não são observações independentes; a distribuição de seleção não permite estimar prevalência de defeitos no restante do RPG.

## 8. Hipóteses científicas e capacidade de refutação

`C28_HYPOTHESIS_RECONCILIATION.csv` registra sete hipóteses, contraevidências e sua classificação: (1) FIP do item não é automaticamente RE individual; (2) golpe especializado contra estrutura não se transfere a criatura; (3) média com RDF/Selo deve usar truncamento por face; (4) rider elétrico depende de dano elétrico positivo; (5) duração da área não garante exposição; (6) a aparente divergência da FIP do Martelo não prova erro; (7) Espada Lendária outlier não deve recalibrar a mediana por si só. As duas primeiras e a quarta são especialmente úteis para proteger o RPG contra **multiplicação indevida de dano em combos e inventários**.

## 9. QA matemático, garantia e rastreabilidade

- O algoritmo primário soma distribuições em dicionário de inteiros e armazena frações racionais, sem amostragem Monte Carlo. **83/83** verificações matemáticas locais PASS.
- Um algoritmo separado gera distribuições por convolução polinomial com inteiros de precisão arbitrária (`numpy` com objetos Python), comparando cada célula. **83/83** confrontos PASS. Isso é verificação de implementação, **não** segundo pesquisador de conteúdo Notion.
- O auditor externo ao algoritmo inicial detectou uma saturação de inteiros quando processava `28d10`; ela foi corrigida ANTES do pacote de release, usando inteiros arbitrariamente grandes e repetindo os confrontos. Não se alterou a expressão canônica.
- Mais **16/16** casos de lógica do gatilho do Selo e da carga da Manopla PASS. Total de checagens lógicas+matemáticas nesta campanha: **182**, sob domínios devidamente separados.
- Reprodução portátil é exigida para os resultados derivados, mas não deve ser confundida com a exatidão dos textos copiados do Notion. Os links da fonte, data de edição e fórmula literal acompanham cada linha. Dados de versões anteriores estão no ZIP C27 baseline, que permanece imutável.

## 10. Gates, fases e ausência de promoções indevidas

- **G0** PASS local sem writer; **G1** G1 Bestas 411/411 permanece no histórico C27, sem conclusão global; **G2–G3** deduplicação/extracção dirigidas locais; **G4** taxonomia parcial; **G5** HOLD por RE individual não comprovado; **G6** PASS matemático local; **G7–G9** parciais; **G10–G11** nenhum v2; **G12** stress condicional TEST; **G13** playtest humano NOT-TESTED; **G14** Mestre/NAC HOLD. Livro de gates físico: `C28_G0_G14_GATE_LEDGER.csv`.
- **F0–F18:** F0 **4/8 HOLD**; F1–F18 sem transição, ledger `C28_F0_F18_NONPROMOTION_LEDGER.csv`. **D0–D9/E01–E24** não foram declarados concluídos por inferência.
- **A5:** sete bytes de anexos originais continuam **0/7 autenticados**. Pesquisa local de ZIPs e nomes `DMG_F0_A5_SNAP_01..07` não encontrou arquivos originais; a Biblioteca respondeu com resultados sem correspondência, não conclusão de inexistência global. **A7/A8:** HOLD. Não afirmar ACK ou autorização da Inbox sem escrita física.
- **NAC-CONT-03/NAC-NORM-01/NAC-PASS-02:** preservar autoridade de decisão do Mestre e histórico; não alterar DMG-RANK, fichas originais, Party, O Primeiro, VLAB ou produções.

## 11. Decisão científica para o Mestre

1. **P0:** pedir ao classificador Atlas competente um **RE individual** explícito por efeito (base, bônus, modo especializado, DoT), incluindo três comparadores de poder; NÃO reaproveitar RI/FIP automaticamente.
2. **P0:** obter segunda codificação humana documental em amostra estratificada de fórmulas e títulos internos, mantendo respostas divergentes e adjudicação.
3. **P1:** para o Martelo, revisar em bancada somente a distinção baseline 56 × demolição 83 antes de propor mudança; a FIP do item é multidimensional e não define percentil da sua batida comum.
4. **P1:** validar em VLAB por requisição coordenada, sem escrever no banco do VLAB, os casos de Selo, manopla e ao menos um efeito temporal; exigir condição de alvo, logs e contrato de reação, evitando pseudocombates.
5. **P1:** recuperar A5 7 bytes originais e garantir snapshot/fingerprint para que F0 possa ser reavaliado.
6. **P2:** inspecionar anotações antigas `/301`, `/220`, bônus `+105`, Croctus duas FOR e Peste Negra somente após estabelecer códigos de proveniência e sem corrigir fichas automaticamente.

## 12. Recovery — checkpoint preservado

**LAST-VERIFIED-UNIT:** C28 leitura de 12 páginas Mestre + cinco proxies diagnósticos + 10 RDF×Selo + 8 resis. elétricas hipotéticas + 9 fórmulas legadas + 8 cenários de exposição + 16 casos de gatilhos, com dois algoritmos de matemática convergentes.  
**FIRST-PENDING:** obter `RE específico da habilidade` autenticado e não o RI/FIP item; segundo codificador documental real; recuperar snapshots originais A5.  
**NEXT-5:** (i) formalizar ponte Atlas → RE por efeito, (ii) resolver documentação de custo/ação/ticks, (iii) codificação independente, (iv) VLAB TEST de reação/defesa após despacho coordenado, (v) auditoria A5 + NAC-PASS antes de qualquer aprovação.  
**NO-REPEAT:** não recatalogar G1 411/411 ou regenerar C22–C27 como descoberta; usar seus manifests como baseline e manter o adendo C27 distinto.  
**TARGET-REMAINDER:** corpus global de magias/técnicas/itens além de 12 fontes, F0–F18, D0–D9, E01–E24, oito gates, F0-A5/A7/A8 e decisão Mestre. Nenhum cronômetro de execução foi presumido.

## 13. Manifesto e persistência

Este PSV acompanha CSVs reexecutáveis, ledger normativo, sete hipóteses, fontes, código `build_c28.py`, `independent_math_c28.py`, `c28_delivery_stress.py`, `prepare_report_c28.py`, duas bases JSON de asserções, relatório decisório, baseline C27 e manifesto SHA-256. Após ZIP, executar replay frio e *readback* do arquivo na Biblioteca Mestre; somente então declarar persistência física.


## 14. Ponte externa VLAB R205 — observação REAL TEST somente leitura

O relatório físico [VLAB-R205](https://app.notion.com/p/3ffc2b324ede81c895eaeb0cd64d1c66) foi reaberto. Recuperou-se o ZIP VLAB original da **Biblioteca VLAB**, SHA-256 `62a9851b3a5ae7919b9225d9379a3d32c8736448e76bfcea4729dcbfe933cead`, 20,800,905 bytes, CRC PASS. O DMG **NÃO executou runner**, combate novo, VLAB writer ou mudança de item. A biblioteca VLAB mantém a custódia do arquivo; o ZIP C28 guarda apenas os resumos de leitura e o ponteiro por SHA, não uma segunda cópia canônica dos bancos.

Uma consulta independente SQL `mode=ro` aos **8 SQLite R205** existentes (4 pares de seeds com a mesma Besta sob políticas ON/OFF) confirmou **384 commits, 1156 eventos, 186 ataques, 4 marcações, 4 retornos, 4 ataques interceptados antes da rolagem e 144 PA de item**. Os resultados são 4 KO e 4 censuras nos 8 ramos; nenhum dos 4 pares mudou o estado final (KO/censura) ou PV final. Em uma seed, a duração cresceu duas rodadas com a reação, mas ainda ocorreu KO.

**Conclusão científica restrita:** há quatro **eventos de invalidação física observados no TEST**, sem demonstração de ganho de PV final ou alteração do desfecho nos quatro pares. Não inferir que reação válida implica vitória ou mitigação efetiva de dano previamente certo; ataques interceptados antes do sorteio não são acertos perdidos garantidos. O Anel estava **semicanônico/incubação**, e a Besta adversária apresentava rank pai ON versus corpo Ouro com ataque genérico condicionado. Isto não é benchmark homologável da Bateria E, não testa Selo nem Manopla, nem acrescenta quatro jogos independentes por contar o par ON/OFF duas vezes. Dados: `C28_VLAB_R205_RING_READONLY_OBSERVATIONS_8.csv`, `C28_VLAB_R205_PAIRED_OUTCOME_4_SEEDS.csv` e `C28_VLAB_R205_READONLY_AUDIT.json`.

## 15. Reconciliação forense dos valores após barra, com uma fonte histórica conflitante

As nove páginas originais de Eletroaquarion (3), Hidrargos (3), Serpentáqua (3) foram reabertas e comparadas com as doze anotações do C22; a fonte histórica [Bagunça (Era da Escuridão)](https://app.notion.com/p/9f9c2b324ede8213968d810c9988bf59) foi reaberta como **comparador externo**, não 13ª página do G1. Os 12 registros G1 têm **11/12** valores dentro do suporte e **11/12** a no máximo 7 pontos de distância da média literal. Entre os 11 compatíveis, a mediana do módulo do desvio é **2**, máximo **7**. Essa concentração **favorece como hipótese** que o campo após a barra era frequentemente uma aproximação da média, mas não prova convenção universal nem observação de rolagem — modelos semelhantes e dependência familiar impedem teste iid ingênuo.

Exceções objetivas e não resolvidas:

- Eletroaquarion Ouro 5: `10d12+132 / 301`; suporte **142–252**, DME **197**. O valor 301 excede o máximo em **49** e a média em **104**. A origem é `UNKNOWN` (erro anotacional, estado diferente, versão incompleta ou modificador ausente), não se altera a ficha.
- Bagunça histórica: `6d12+110 / 220`; suporte **116–182**, DME **149**, anotação acima do máximo em **38**. A ficha Eletroaquarion Ouro 4 registra **a mesma fórmula literal com `/147`**, demonstrando discrepância documental entre fontes de contexto distinto, sem decidir qual contexto adicional seria competente.
- Bagunça usa **18×220 = 3.960** e **10×220 = 2.200** em projeções. Substituir 220 por DME literal 149 em uma projeção hipotética de todos os ataques dá **2.682** e **1.490**, diferença relativa de **47.65%**. **Esses totais não são dano observado nem afirmação de 18 ataques reais.** Mostram como anotações fora de suporte propagam viés se empregadas em estimativas.
- Serpentáqua Ouro 5: FOR **103**, termo literal `+105`; os **2** pontos não são classificados automaticamente como FOR nem bonus intrínseco certificado.

A classificação título/corpo nessas três famílias continua problematizada; reutilização de modelos é hipótese genealógica, não prova de uma regra universal dos três conjuntos. Os 13 registros e confronto foram preservados em `C28_C22_12_NOTES_PLUS_HISTORICAL_1_REAUDITED.csv` e `C28_FORENSIC_SLASH_DOSSIER.json`.

**FIRST-PENDING adicionais:** localizar versão com justificativa explícita de `/301` e `/220` ou obter decisão do Mestre sobre errata prospectiva, sem retcon; separar a revisão de atributos e bônus de Serpentáqua e Croctus da validação RE do ataque. **NO-REPEAT:** as 9 páginas já examinadas pertencem ao G1 411/411 e esta releitura não aumenta o denominador.
