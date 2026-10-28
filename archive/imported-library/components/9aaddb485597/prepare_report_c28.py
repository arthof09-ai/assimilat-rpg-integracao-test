from pathlib import Path
import csv,json,datetime,hashlib
P=Path(__file__).resolve().parent.parent
O=P/'publication'
def read(f): return list(csv.DictReader((O/f).open(encoding='utf-8')))
proxy=read('C28_RI_FIP_NONAUTHORITATIVE_PROXY.csv')
defense=read('C28_PHYSICAL_RDF_SELO_10_CONDITIONAL_FIXTURES.csv')
raio=read('C28_MANOPLA_ELECTRIC_RESISTANCE_THRESHOLDS.csv')
legacy=read('C28_LEGACY_MULTIEFFECT_DECOMPOSITION.csv')
contract=read('C28_PRIMARY_EFFECT_CONTRACTS.csv')
math=json.loads((O/'C28_MATH_ASSERTIONS.json').read_text())
math2=json.loads((O/'C28_SECOND_ALGORITHM_AUDIT.json').read_text())
stress=json.loads((O/'C28_DELIVERY_STRESS_ASSERTIONS.json').read_text())
source_links={
 'DMG-RANK':'https://app.notion.com/p/3f2c2b324ede815498cddb7844245f7e',
 'Atlas':'https://app.notion.com/p/3eec2b324ede81ea8920c52473ecc3ab',
 'Metodologia':'https://app.notion.com/p/3f3c2b324ede81ab8d8ec1c7cce760b3',
 'QA':'https://app.notion.com/p/3f3c2b324ede815cb014dc6294f40170',
 'OP-DMG':'https://app.notion.com/p/3f3c2b324ede813e9fa0c87ebdea0b29',
 'Manopla':'https://app.notion.com/p/3f5c2b324ede81f5ac62fb940204cdac',
 'Lâmina':'https://app.notion.com/p/3f5c2b324ede81e9aa8ec51f568600e8',
 'Martelo':'https://app.notion.com/p/3f5c2b324ede81658982d8f47b3ad647',
 'Selo':'https://app.notion.com/p/3f5c2b324ede81d0874ed4d96752812c',
 'Anel':'https://app.notion.com/p/3f5c2b324ede81ceabf6fc2b97344e43',
 'Pó':'https://app.notion.com/p/3f5c2b324ede8145a12febac8558aeb8',
 'Estandarte':'https://app.notion.com/p/3f5c2b324ede816a9683e0ad40bad4b3',
 'Véu':'https://app.notion.com/p/3f5c2b324ede81bab332f518b2e6a211',
 'Adaga Serpente':'https://app.notion.com/p/3edc2b324ede811787a0de913622b14d',
 'Cajado Eclipse':'https://app.notion.com/p/1cdc2b324ede82ed892f815f21f79ac1',
 'Espada Lendário':'https://app.notion.com/p/3edc2b324ede81ab9e22e168f6d939a9',
 'Arco Elemental':'https://app.notion.com/p/3edc2b324ede8156849bf1aae0ce9fb5',
 'Rinolupo':'https://app.notion.com/p/034c2b324ede83ffa7118144011beaf3',
 'Guardião Pétreo P3':'https://app.notion.com/p/549c2b324ede8375b21181335038aad1',
 'Guardião Pétreo O1':'https://app.notion.com/p/b0ec2b324ede835a927601b4cbd8fca6',
 'Guardião Pétreo O5':'https://app.notion.com/p/371c2b324ede837fad4c01bbfe9a95fb'
}
(O/'C28_CANONICAL_SOURCE_LINKS.json').write_text(json.dumps(source_links,ensure_ascii=False,indent=2),encoding='utf-8')

def x(id,rd):
 return next(q for q in defense if q['effect_id']==id and int(q['RDF'])==rd)
rdf15_blade=x('O02',15);rdf15_hammer=x('O03',15)
raid20=next(q for q in raio if int(q['hypothetical_Raio_resistance'])==20)
raid25=next(q for q in raio if int(q['hypothetical_Raio_resistance'])==25)
raid30=next(q for q in raio if int(q['hypothetical_Raio_resistance'])==30)

GATES=[('G0','GOVERNANÇA','LOCAL PASS / PRODUCTION HOLD','Fontes Mestre, nenhuma mudança canônica; decisões do Mestre preservadas.'),('G1','DESCOBERTA','G1 BESTAS 411/411 ANTERIOR; GERAL PENDENTE','C28 é coorte dirigida de itens, não censo do RPG.'),('G2','DEDUP','LOCAL PASS','19 linhas de efeitos em 12 páginas únicas; não contam 19 itens ou 19 pesquisadores.'),('G3','EXTRAÇÃO','LOCAL PASS / SEGUNDO CODIFICADOR PENDENTE','Fórmulas reabertas e transcritas; fonte mestre tem precedência.'),('G4','TAXONOMIA','PARCIAL','Separados alvo, Raio, físico, veneno, Vida, cura, utilidade, duração.'),('G5','CLASSIFICAÇÃO','HOLD','RI+FIP de item não certifica RE de cada ataque; 0 de 19 promovidos.'),('G6','MATEMÁTICA','LOCAL PASS','83 checks de primeiro algoritmo e 83 de segundo; mais 16 contratos lógicos.'),('G7','DOSSIÊS','PARCIAL','Equipamentos dirigidos; demais domínios e reconciliações pendentes.'),('G8','ESTATÍSTICA','LOCAL CONDICIONAL','Probabilidades e médias exatas; sem acerto/turnos/população.'),('G9','VIÉS','PARCIAL','Fontes selecionadas, itens históricos e sem randomização.'),('G10','CANDIDATO','NOT STARTED','Sem versão normativa candidata.'),('G11','REGRESSÃO','NOT STARTED','Não existe sistema v2 homologado para confrontar.'),('G12','STRESS','PARCIAL TEST','RDF+Selo, Raio e janelas condicionais; sem full-fight.'),('G13','PLAYTEST','NOT TESTED','Nenhum grupo humano participando desta campanha.'),('G14','MESTRE/NAC','HOLD','NAC-PASS, F0, A5/A7/A8 continuam bloqueados.')]
with (O/'C28_G0_G14_GATE_LEDGER.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['gate','name','status','evidence']);w.writerows(GATES)
phases=[('F0','4/8 HOLD','A5 originais 0/7; revisão independente e snapshot certificados pendentes')]
for i in range(1,19):phases.append((f'F{i}','NO_PROMOTION', 'Nenhum gate formal foi promovido no ciclo C28; análises TEST não homologam fase'))
with (O/'C28_F0_F18_NONPROMOTION_LEDGER.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['phase','state','reason']);w.writerows(phases)

link=lambda n:f'[{n}]({source_links[n]})'
head='''# PSV DMG C28 — Banco de efeitos com contrato de entrega, aferição exata de defesa e diagnóstico RI/FIP

**21/10/2026 — MESTRE-SIDE / TEST — OP-DMG-CORPUS-EMP-01 — CM-000001**  
**Baseline:** C27 + adendo fora do G1 (Biblioteca Mestre) · **Norma:** DMG-RANK-01 v1.1 INALTERADA  
**Produção / Party / O Primeiro:** HOLD / NO-WRITE · **NAC-PASS global:** HOLD · **F0:** 4/8 HOLD.

## 1. Contrato de continuidade e ANTES → DEPOIS

**ANTES:** G1 estrutural de Bestas fechado em **411/411 Page-IDs**, com RE de ataque individual não certificado no corpus C22–C27; adendo C27 localizara casos mais documentados fora do G1. F0-A5 0/7 originais autenticados. O problema não era falta de contagem de páginas, mas **ponte documental RE/FIP × efeito, acionamento/custo e redução por defesa**.

**DEPOIS (C28):** 12 páginas físicas de itens/equipamentos distintas e **19 linhas de contrato de efeito** foram indexadas sem criar itens novos. Cinco diagnósticos *não normativos* de FIP do **item** × banda de DME da norma, 10 células exatas RDF+Selo, 8 níveis **hipotéticos** de resistência a Raio, 9 decomposições legadas, 8 cenários de permanência de Lua de Sangue, 8 fixtures lógicos Selo multi-alvo/evento, 8 modelos de diluição de carga da Manopla, e uma taxonomia rastreável de 7 hipóteses. G5 individual do efeito permanece **HOLD**; os dados não criam RE por inferência.

**Status C28:** ACEITE TÉCNICO LOCAL nas operações de leitura, taxonomia e matemática, **NÃO** aceite de balanceamento normativo, nem transição formal F0–F18. Nenhum escritor canônico/epoch/lease/ACK presumido.

## 2. Autoridades reabertas e princípio de classificação

Fontes superiores aplicadas: %s; %s; %s; %s; %s. O Atlas separa **RN** da Besta, **RI** do equipamento, **RIn** da matéria-prima, **FIP interna** do item e **RE** de um efeito particular. A DMG-RANK exige *efeito → RE/FIP competente → perfil de entrega → orçamento → fórmula*; quando o dano já é canônico ele é preservado. **FIP do item não comprova, por si só, o RE de cada ataque, componente ou modo.**

### 2.1 Limites literais da DMG-RANK v1.1

Banda padrão Ouro Entrada: **22–28 DME**; Ouro Negro Entrada **38–48**; Ouro Negro Média **59–69**; Ouro Negro Ápice **83–96**; Lendário Ápice **137–160**. Essas faixas valem para um efeito padrão, alvo único, Ação Padrão, sem hard-control/bypass maior; não são *pass/fail automático* de artefato, DoT, bônus especializado, múltiplos alvos ou efeito com custo e defesa. A DMG-RANK afirma ainda que arma mágica classificada pode trazer dano intrínseco total comparável ao RI/RE depois de seus riders; aqui essa ponte é usada apenas como **diagnóstico candidato de item** e não como certificação RE do ataque.

## 3. Matriz de fontes físicas, denominadores e arquitetura anti-duplicação

Fonte de verdade: a ficha Notion Mestre específica por **Page-ID**; CSV é índice laboratorial. 19 linhas de contrato não são 19 itens, mas **12 páginas de origem**; a Lâmina e o Martelo têm modos/defesas distintos; o Cajado tem cinco efeitos numericamente distintos; danos legados e linhas de controle aparecem no mesmo inventário sem serem somados. Os dados estão no CSV `C28_PRIMARY_EFFECT_CONTRACTS.csv`, com literal, natureza, entrega, PA, frequência, restrição e status de RE.

| Fonte | Resultado/documentação relevante |
|---|---|
| %s | Ouro–Entrada do **item**; +`5d8+3` Raio no ataque já acertado, 22 PA, um uso por 8h; lentidão −3m apenas se Raio >0 pós-resistência |
| %s | ON–Entrada do item; `7d8+15` Cortante, uma Ação Padrão; ancoragem defensiva é reação separada 18 PA e 1/8h |
| %s | ON–Média do item; `8d10+12` Impacto por ataque; +`6d8` somente em estrutura não viva com 25 PA 1/8h |
| %s | Lendário–Entrada; reação consumível 55 PA, protege até 3 alvos de **uma mesma ocorrência**; redução até 60 por alvo pós-RD |
| %s | ON–Baixa por retorno espacial preparado; não há dano ofensivo numérico |
| %s | Prata–Entrada por defesa de frio climático: até 12 pontos por ocorrência ambiental durante 30 min; não é RD anti-magia Gelo |
| %s e %s | Controle negativo: classificação elevada por proteção mental/ocultação sem dano |
| %s | Adaga ON de fonte legada, FIP não específica; `5d4+5d8+10`; veneno `3d12`/turno sob falha CON CD25; duração e custo ambíguos |
| %s | Cajado com passivo `+7d8`, Lua de Sangue `20d8` contra inimigos e `16d8` cura aliada por rodada 3 rodadas, `20d8` toque; demais condições preservadas |
| %s | Lendário–Ápice analítico com `14d20+14d12+14d8+14d10+390+FOR`, DME 768 **antes da FOR**, desgaste avançado; outlier histórico |
| %s | Lendário de item com dano-base `8d8+25` e `+8d12+10` contra elementais; condição do bônus preservada |

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

Fontes dos defensores reabertas: %s RDF10; %s RDF15; %s RDF20; %s RDF25. Compare **um ataque que acertou**, com natureza física certificada na arma, `max(0, resultado − RDF)`; então aplique o Selo apenas sobre o residual: `max(0, resultado − RDF − 60)`.

| Ataque | RDF | Média pós-RDF sem Selo | Média residual com Selo | Probabilidade de residual positivo |
|---|---:|---:|---:|---:|
| Lâmina | 15 | %.4f | %.8f | %.8f |
| Martelo | 15 | %.4f | %.8f | %.6f |
| Lâmina | 10 | %.4f | %.9f | %.9f |
| Martelo | 10 | %.4f | %.8f | %.6f |

O efeito vale somente sob as seguintes premissas: acerto verdadeiro; reação disponível; 55 PA; Selo não consumido antes; elegibilidade espacial até 4m; não há imunidade/controle que bloqueie reação; e RDF aplicável ao dano físico daquele ataque. **Não** são valores de DPT/ação/combate ou playtest. O Selo não protege três eventos de multi-hit separados; a tabela de 8 cenários `C28_SELO_SCOPE_HYPOTHETICAL_EVENT_FIXTURES.csv` demonstra o erro dessa extrapolação, com exemplos previamente identificados como **hipotéticos**.

A matemática foi feita sobre a distribuição completa de dados: não se usou `max(0, DME−RDF−60)` como substituto da esperança pós-truncamento. Células com probabilidade diminuta preservaram o valor exato em frações, não foram arredondadas a zero sem suporte.

## 6. Raio, resistência e chance do rider da Manopla

`5d8+3` tem suporte de **8–43**, DME 25,5. A lentidão de −3m só é aplicada se o dano de Raio *efetivamente positivo* atravessar as proteções. O cálculo abaixo usa resistências hipotéticas — **NÃO** RDF física de Rinolupo/Guardião, nem defesa de criaturas inventadas.

| Resistência elétrica hipotética | Dano médio Raio líquido | Chance de −3 m após um acerto confirmado |
|---:|---:|---:|
| 20 | %.6f | %.3f%% |
| 25 | %.6f | %.3f%% |
| 30 | %.6f | %.3f%% |

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

- O algoritmo primário soma distribuições em dicionário de inteiros e armazena frações racionais, sem amostragem Monte Carlo. **%d/%d** verificações matemáticas locais PASS.
- Um algoritmo separado gera distribuições por convolução polinomial com inteiros de precisão arbitrária (`numpy` com objetos Python), comparando cada célula. **%d/%d** confrontos PASS. Isso é verificação de implementação, **não** segundo pesquisador de conteúdo Notion.
- O auditor externo ao algoritmo inicial detectou uma saturação de inteiros quando processava `28d10`; ela foi corrigida ANTES do pacote de release, usando inteiros arbitrariamente grandes e repetindo os confrontos. Não se alterou a expressão canônica.
- Mais **%d/%d** casos de lógica do gatilho do Selo e da carga da Manopla PASS. Total de checagens lógicas+matemáticas nesta campanha: **%d**, sob domínios devidamente separados.
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
'''%(link('DMG-RANK'),link('Atlas'),link('Metodologia'),link('QA'),link('OP-DMG'),link('Manopla'),link('Lâmina'),link('Martelo'),link('Selo'),link('Anel'),link('Pó'),link('Estandarte'),link('Véu'),link('Adaga Serpente'),link('Cajado Eclipse'),link('Espada Lendário'),link('Arco Elemental'),link('Rinolupo'),link('Guardião Pétreo P3'),link('Guardião Pétreo O1'),link('Guardião Pétreo O5'),float(rdf15_blade['mean_before_seal']),float(rdf15_blade['mean_after_seal']),float(rdf15_blade['prob_residual_positive']),float(rdf15_hammer['mean_before_seal']),float(rdf15_hammer['mean_after_seal']),float(rdf15_hammer['prob_residual_positive']),float(x('O02',10)['mean_before_seal']),float(x('O02',10)['mean_after_seal']),float(x('O02',10)['prob_residual_positive']),float(x('O03',10)['mean_before_seal']),float(x('O03',10)['mean_after_seal']),float(x('O03',10)['prob_residual_positive']),float(raid20['mean_electric_after']),100*float(raid20['conditional_probability_slow3m']),float(raid25['mean_electric_after']),100*float(raid25['conditional_probability_slow3m']),float(raid30['mean_electric_after']),100*float(raid30['conditional_probability_slow3m']),math['n'],math['n'],math2['check_count'],math2['check_count'],stress['count'],stress['count'],math['n']+math2['check_count']+stress['count'])
(O/'PSV_DMG_C28_MESTRE_ONLY.md').write_text(head,encoding='utf-8')

memo='''# C28 — PARECER CIENTÍFICO DECISÓRIO AO MESTRE — 21/10/2026

**MESTRE-SIDE / LABORATÓRIO TEST · OP-DMG-CORPUS-EMP-01 · NÃO É CANONIZAÇÃO.**

## Veredito

**Manter integralmente DMG-RANK-01 v1.1; F0 4/8 HOLD; NÃO promover bandagem normativa.** O C28 avança o problema de entrega: a fonte possui FIP do **item**, mas não RE específico certificado de cada habilidade. Foram reabertos 12 itens/equipamentos e catalogadas 19 linhas, com 5 aferições proxy, 10 pares de dano pós-RDF/Selo, 8 cenários hipotéticos de resistência elétrica e 9 decomposições de efeitos legados. Um segundo método matemático auditou os resultados e confirmou o pacote, sem substituir revisão humana do Notion.

## Os cinco resultados para decisão

**1. Classe do item não igual a classe automática de todos seus ataques.** A Manopla Ouro–Entrada tem DME adicional 25,5 (dentro Ouro Entrada 22–28), a Lâmina ON–Entrada tem DME 46,5 (dentro 38–48); Martelo ON–Média bate 56 (três abaixo de 59), mas faz 83 apenas contra estrutura não viva gastando 25 PA 1/8h. Classificação do item é multidimensional e restrições de uso importam. Dados NÃO certificam RE.

**2. Selo defensivo altera distribuição inteira.** Contra Lâmina e RDF15 real, o Selo de 60 elimina o dano residual em todas as faces. Contra Martelo RDF15, a chance de residual positivo é %.5f%% e o residual médio %.6f sob um acerto já confirmado. Selo só cobre uma ocorrência hostil; consumível, Reação e 55 PA obrigatórios.

**3. Lentidão da Manopla depende de dano elétrico verdadeiro.** Sob 20/25/30 pontos hipotéticos de mitigação a Raio, a chance pós-acerto é %.2f%% / %.2f%% / %.2f%%, respectivamente. Imunidade impede o rider. Não extrapolar de RDF física.

**4. Duração e área não são ataques grátis.** Cajado Eclipse registra `20d8` de dano necrótico por rodada em 6m por até três rodadas, e `16d8` de cura aliada por rodada; não converter efeitos opostos em dano total nem presumir exposição ou economia de ação inexistente. Adaga Serpente tem veneno `3d12` por tick condicionado a CD25; duração não fornecida.

**5. Casos negativos revelam viés de rank.** Selo Lendário, Anel ON, Pó Prata e Véu ON derivam potência de proteção/retorno/ocultação, não DME ofensivo. Espada do Lendário DME768 é outlier histórico explicitamente separado pela norma, não base para inflar mediana.

## Próximas decisões sem alterar o cânone

Solicitar classificação Atlas competente e expressa do RE de cada modo/ataque (não por analogia do item); obter codificador documental humano separado; determinar PA e gatilhos incompletos; requisitar VLAB TEST controlado se o Coordenador autorizar; autenticar os sete originais F0-A5; conservar anotações antigas `/301` e `/220` sem retcon. Nunca escrever na Party ou no sistema de produção por causa de teste.

**Gates:** G5 HOLD, G6 PASS matemático local; F0 4/8 HOLD; A5 0/7 autenticado; A7/A8 HOLD; NAC-PASS global HOLD; DMG-RANK v1.1 preservada. Nenhuma alteração em Notion Mestre original ou outros executores.

**FIRST-PENDING:** `RE específico do efeito` documentado + segunda codificação; até lá o estudo é de *diagnóstico condicionado* não de calibração definitiva.
'''%(100*float(rdf15_hammer['prob_residual_positive']),float(rdf15_hammer['mean_after_seal']),100*float(raid20['conditional_probability_slow3m']),100*float(raid25['conditional_probability_slow3m']),100*float(raid30['conditional_probability_slow3m']))
(O/'C28_PARECER_DECISORIO_MESTRE_ONLY.md').write_text(memo,encoding='utf-8')

readme='''# C28 — instruções para replay científico

Arquivos `work/*.py` operam somente em dados localmente transcritos de páginas Mestre lidas em 21/10/2026. Nenhuma escrita em Notion, Party, O Primeiro ou VLAB. Preserva `baseline/` C27 sem reexecutar discovery G1.

Executar no diretório do pacote:

```
python work/build_c28.py
python work/independent_math_c28.py
python work/c28_delivery_stress.py
python work/prepare_report_c28.py
```

As saídas na pasta `publication/` podem ser comparadas por SHA-256 aos hashes do manifesto. O código valida aritmética das transcrições, **não** fornece assinatura de segundo auditor humano/independente Notion, nem RE competente por inferência.

`C28_PHYSICAL_RDF_SELO_10_CONDITIONAL_FIXTURES.csv` usa somente ataques explicitamente físicos de Lâmina/Martelo e os quatro defensores RDF reais; RDF não é resistência elétrica. O Selo é uma Reação +55 PA de uso único válida só para uma ocorrência. Os 8 cenários de Selo multi-alvo e 8 de uso de carga da Manopla são hipotéticos, não combates.

**F0:** 4/8 HOLD. **A5:** 0/7 arquivos originais verificados. **Production:** HOLD. **Party/O Primeiro:** NO-WRITE.
'''
(O/'README_C28_MESTRE_ONLY.md').write_text(readme,encoding='utf-8')

# Additional two scientific fronts completed AFTER first report construction; reproducibly append.
vlab=json.loads((O/'C28_VLAB_R205_READONLY_AUDIT.json').read_text())
slash=json.loads((O/'C28_FORENSIC_SLASH_DOSSIER.json').read_text())
appendix=f"""

## 14. Ponte externa VLAB R205 — observação REAL TEST somente leitura

O relatório físico [VLAB-R205](https://app.notion.com/p/3ffc2b324ede81c895eaeb0cd64d1c66) foi reaberto. Recuperou-se o ZIP VLAB original da **Biblioteca VLAB**, SHA-256 `{vlab['checked_archive_sha256']}`, {vlab['size_bytes']:,} bytes, CRC PASS. O DMG **NÃO executou runner**, combate novo, VLAB writer ou mudança de item. A biblioteca VLAB mantém a custódia do arquivo; o ZIP C28 guarda apenas os resumos de leitura e o ponteiro por SHA, não uma segunda cópia canônica dos bancos.

Uma consulta independente SQL `mode=ro` aos **8 SQLite R205** existentes (4 pares de seeds com a mesma Besta sob políticas ON/OFF) confirmou **{vlab['commits']} commits, {vlab['native_events']} eventos, {vlab['attack_attempts']} ataques, {vlab['ring_marks']} marcações, {vlab['ring_returns']} retornos, {vlab['intercepts_before_attack_roll']} ataques interceptados antes da rolagem e {vlab['item_pa_spent_total']} PA de item**. Os resultados são 4 KO e 4 censuras nos 8 ramos; nenhum dos 4 pares mudou o estado final (KO/censura) ou PV final. Em uma seed, a duração cresceu duas rodadas com a reação, mas ainda ocorreu KO.

**Conclusão científica restrita:** há quatro **eventos de invalidação física observados no TEST**, sem demonstração de ganho de PV final ou alteração do desfecho nos quatro pares. Não inferir que reação válida implica vitória ou mitigação efetiva de dano previamente certo; ataques interceptados antes do sorteio não são acertos perdidos garantidos. O Anel estava **semicanônico/incubação**, e a Besta adversária apresentava rank pai ON versus corpo Ouro com ataque genérico condicionado. Isto não é benchmark homologável da Bateria E, não testa Selo nem Manopla, nem acrescenta quatro jogos independentes por contar o par ON/OFF duas vezes. Dados: `C28_VLAB_R205_RING_READONLY_OBSERVATIONS_8.csv`, `C28_VLAB_R205_PAIRED_OUTCOME_4_SEEDS.csv` e `C28_VLAB_R205_READONLY_AUDIT.json`.

## 15. Reconciliação forense dos valores após barra, com uma fonte histórica conflitante

As nove páginas originais de Eletroaquarion (3), Hidrargos (3), Serpentáqua (3) foram reabertas e comparadas com as doze anotações do C22; a fonte histórica [Bagunça (Era da Escuridão)](https://app.notion.com/p/9f9c2b324ede8213968d810c9988bf59) foi reaberta como **comparador externo**, não 13ª página do G1. Os 12 registros G1 têm **11/12** valores dentro do suporte e **11/12** a no máximo 7 pontos de distância da média literal. Entre os 11 compatíveis, a mediana do módulo do desvio é **2**, máximo **7**. Essa concentração **favorece como hipótese** que o campo após a barra era frequentemente uma aproximação da média, mas não prova convenção universal nem observação de rolagem — modelos semelhantes e dependência familiar impedem teste iid ingênuo.

Exceções objetivas e não resolvidas:

- Eletroaquarion Ouro 5: `10d12+132 / 301`; suporte **142–252**, DME **197**. O valor 301 excede o máximo em **49** e a média em **104**. A origem é `UNKNOWN` (erro anotacional, estado diferente, versão incompleta ou modificador ausente), não se altera a ficha.
- Bagunça histórica: `6d12+110 / 220`; suporte **116–182**, DME **149**, anotação acima do máximo em **38**. A ficha Eletroaquarion Ouro 4 registra **a mesma fórmula literal com `/147`**, demonstrando discrepância documental entre fontes de contexto distinto, sem decidir qual contexto adicional seria competente.
- Bagunça usa **18×220 = 3.960** e **10×220 = 2.200** em projeções. Substituir 220 por DME literal 149 em uma projeção hipotética de todos os ataques dá **2.682** e **1.490**, diferença relativa de **{100*slash['relative_inflation_of_220_compared_to_formula_mean']:.2f}%**. **Esses totais não são dano observado nem afirmação de 18 ataques reais.** Mostram como anotações fora de suporte propagam viés se empregadas em estimativas.
- Serpentáqua Ouro 5: FOR **103**, termo literal `+105`; os **2** pontos não são classificados automaticamente como FOR nem bonus intrínseco certificado.

A classificação título/corpo nessas três famílias continua problematizada; reutilização de modelos é hipótese genealógica, não prova de uma regra universal dos três conjuntos. Os 13 registros e confronto foram preservados em `C28_C22_12_NOTES_PLUS_HISTORICAL_1_REAUDITED.csv` e `C28_FORENSIC_SLASH_DOSSIER.json`.

**FIRST-PENDING adicionais:** localizar versão com justificativa explícita de `/301` e `/220` ou obter decisão do Mestre sobre errata prospectiva, sem retcon; separar a revisão de atributos e bônus de Serpentáqua e Croctus da validação RE do ataque. **NO-REPEAT:** as 9 páginas já examinadas pertencem ao G1 411/411 e esta releitura não aumenta o denominador.
"""
with (O/'PSV_DMG_C28_MESTRE_ONLY.md').open('a',encoding='utf-8') as f:f.write(appendix)
with (O/'C28_PARECER_DECISORIO_MESTRE_ONLY.md').open('a',encoding='utf-8') as f:
 f.write(f"""

## Duas descobertas adicionais verificadas

**VLAB R205 — evento não é resultado final:** oito SQLite originais, quatro pares de seeds, 4 ataques invalidados e 144 PA consumidos com Anel, **mas zero pares com diferença de KO/censura ou de PV final**. Combates continuam TEST e o Anel incubação; não basta contar interceptação para provar melhoria de vitória. SHA do pacote VLAB original: `{vlab['checked_archive_sha256']}`. Não executar novos combates no DMG.

**Duas anotações impossíveis:** no G1, Eletroaquarion `10d12+132 /301` (máximo 252); no histórico Bagunça `6d12+110 /220` (máximo 182). A mesma expressão `6d12+110` na ficha original G1 é `/147`. Entre 12 anotações G1, 11 estão a no máximo 7 da média, mas não canonizar a barra como campo DME. A nota `/220` multiplicada por 18 ou 10 ataques já alimenta projeções históricas, potencialmente distorcidas; não interpretar essas projeções como lutas observadas. Continuar sem editar fichas.
""")
with (O/'README_C28_MESTRE_ONLY.md').open('a',encoding='utf-8') as f:
 f.write('\n**Apêndices:** reexecute `python work/forensic_slash_c28.py` após as quatro rotinas. `work/audit_vlab_r205_readonly.py` exige o ZIP VLAB R205 ORIGINAL separado, mantido no domínio VLAB: não duplicado no pacote C28. O arquivo de saída do auditor original está incluído para leitura, mas replay independente desse ramo requer obter o ZIP pelo hash/Library. Nenhuma rotina executa batalhas.\n')
manifest_path=O/'C28_DENOMINATOR_MANIFEST.json'; m=json.loads(manifest_path.read_text())
m.update({'G1_total_pages_prior_C27':411,'G1_new_pages_C28':0,'C28_reopened_G1_for_forensics':9,'C28_historical_other_page_reopened':1,'C28_VLAB_notions_page_reopened':1,'C28_VLAB_R205_readonly_runs':vlab['runs'],'C28_VLAB_R205_paired_seeds':vlab['pairs'],'C28_VLAB_R205_intercepts':vlab['intercepts_before_attack_roll'],'C28_VLAB_R205_combat_runners_executed':0,'slash_records_G1':12,'slash_records_historical_additional':1,'slash_support_valid_G1':11,'primary_math_checks':math['n'],'second_algo_checks':math2['check_count'],'delivery_logic_cases':stress['count'],'checks_all_types':math['n']+math2['check_count']+stress['count']})
manifest_path.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')

print('reports generated',len(head),len(memo),'phases',len(phases),'gates',len(GATES))
