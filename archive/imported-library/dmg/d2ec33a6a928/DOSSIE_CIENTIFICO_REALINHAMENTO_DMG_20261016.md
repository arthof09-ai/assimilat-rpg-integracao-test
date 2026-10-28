# DOSSIÊ CIENTÍFICO — DMG-RANK v1.1 | Diagnóstico de realinhamento

**MESTRE-SIDE • OP-DMG-CORPUS-EMP-01 • CM-000001 / workstream DMG • 16/10/2026**

**Status:** entrega científica exploratória **REPRODUZÍVEL**, com conclusões limitadas aos estratos selecionados. **Não é** certificação do corpus global, v2 aprovada, atualização do Sistema de Combate, combate nativo, sentença de desequilíbrio universal ou liberação de produção. **DMG-RANK-01 v1.1 INALTERADA.**

## 0. Resumo executivo de decisão

O principal obstáculo observado nesta rodada **não é uma falha demonstrada na fórmula das bandas DMG-RANK**. É a incompatibilidade de objetivos entre três coisas diferentes: (i) bandas intrínsecas destinadas a *gerar valores quando a fonte não oferece dano explícito*; (ii) fichas antigas de Bestas com valor explícito e grandes atributos externos; e (iii) muitas fichas de patamar alto com habilidades descritas, porém sem fórmulas ou classificação interna consistente. Misturar essas três categorias produziria diagnóstico falso.

**Resultado de fonte nova:** uma coorte congelada antes da leitura dos corpos examinou **24/24 páginas**, oito de cada título Ouro 5, Ouro Negro 1 e Lendário 1. **23/24 não possuem dano ofensivo numericamente completo em suas habilidades**; a única com expressão ofensiva completa possui **duas** ações (`1d6+INT66`), mas título, corpo e ancestral não concordam. **0/24** é elegível para inferência de dano por rank de classificação integralmente reconciliado. São páginas com criaturas e habilidades, **não páginas que causam zero dano**. Quantidades de *drops* (`1d10`, `1d8` etc.) e cura de `1d6` não foram convertidas em ataques. Exemplos: [Cervatox](https://app.notion.com/p/0e2c2b324ede83fa8032016593efec3e), [Aurora Radiante em título Ouro 5](https://app.notion.com/p/2e9c2b324ede829eba23815d22d51794), [Carpe Draco em título Ouro Negro 1](https://app.notion.com/p/294c2b324ede83cc8529017b8555b5be), [Elefante Colossal em título Lendário 1](https://app.notion.com/p/ffec2b324ede8289a99101f42099c55c).

**Resultado histórico recomputado:** no conjunto pré-selecionado **R03/R04, 29 habilidades iniciais em 26 páginas portadoras de fórmulas, examinadas entre 53 páginas**, a soma das contribuições de atributos impressos é **1.011** de **1.199,5** pontos de média bruta condicional: **84,29%**. A porcentagem é uma **composição ponderada pelas expressões selecionadas**, não prevalência ou parâmetro universal do RPG. **28/29** ações contêm atributo expresso; uma não contém, e isso não é razão para descartá-la. Custo, probabilidade de acertar, classificação do efeito, origem do poder e distinções entre páginas da mesma criatura podem mudar o veredito.

**Achado mecânico experimental novo:** a Patada Prata 1 de Lupusventus/Lobo da Caverna `2d6+FOR25` e a variante TEST `4d6+18` têm **a mesma média bruta 32**, mas sob cenário de RD35 aplicada integralmente à parcela física, a média líquida condicional muda de **1/9 ≈ 0,1111** para **229/648 ≈ 0,3534**. Logo, classificar fórmulas somente por esperança, sem distribuição, perde informação relevante sobre atravessar limiares de RD. As duas formas **não** são igualmente eficazes apenas porque têm a mesma média. O resultado não autoriza reforma do DMG nem garante a mesma chance de acerto.

**Posição sobre v2:** **NÃO HÁ EVIDÊNCIA PARA PROPOR UMA SUBSTITUIÇÃO GLOBAL** neste checkpoint. É justificável testar melhorias **de metodologia e parâmetros condicionais**, com fontes faltantes tratadas em réplicas TEST, sem mudar fórmulas explícitas históricas.

## 1. Estado ANTES, recuperação e fronteiras

- **OP existente:** https://app.notion.com/p/3f3c2b324ede813e9fa0c87ebdea0b29; histórico antigo R11–R23 é diferente da numeração local pós-R10. O **R11 original** em ZIP está fisicamente acessível, com matriz B01–B18 (18 requisitos) e manifesto de entradas verificável; os R23 decisórios constam de evidência documental histórica, não são aqui promovidos a originais digitalmente auditados.
- **Norma vigente:** https://app.notion.com/p/3f2c2b324ede815498cddb7844245f7e, DMG-RANK-01 v1.1. A precedência da fórmula explícita e a distinção DME intrínseco / atributos externos foram confirmadas por consulta à norma.
- **Fonte especializada de RD para Bestas:** https://app.notion.com/p/3ebc2b324ede81f4992ac88a3588cacd. RD normal Bronze 5, Prata 15, Ouro 25, Ouro Negro 35; Titã/CON acima de 100 usa tabela especializada, não se presume a mesma RD para toda criatura.
- **Arquivos efetivamente lidos:** `R02_DAMAGE_A_B_C.csv` (22 linhas de fórmulas recuperadas, nove elegíveis na coorte B5), `R03_INITIAL_DAMAGE.csv` (21 linhas elegíveis iniciais de arquivo histórico, seis critérios três-vias), `R04_ALL_INITIAL_ACTIONS.csv` (29 linhas); cópias com hash ficam em `readonly_sources/`. Integridade das **entradas do ZIP R11** verificada independentemente. O pacote `AUTO10_REPLICAS_20261016` permanece referência histórica preservada, não novo experimento.
- **Lote 002:** 45 páginas e 58 registros são denominadores **HISTÓRICOS RELATADOS**, não reautenticados por ZIP físico aqui. **Lote 003:** 71 páginas, 56 fórmulas de 35 fontes e 108 componentes **RELATADOS**; **0/71** de pertencimento individual autenticado neste checkpoint. Sem soma com a nova coorte, cujo vínculo ao lote não foi demonstrado.
- **CSV I0003 originais:** **0/9** autenticados neste checkpoint. União derivada de 198 IDs permanece **RELATADA**. Não se repetiu varredura de 47 CSV/114 ZIP sem novo localizador.
- **B01–B18:** no documento R11, **1/18 PASS documental B02**. Demais requisitos preservados e não certificados por estes cálculos; a matriz R23 relata **9 PARTIAL, 6 BLOCKED, 2 NOT-TESTED, 0/2 STRICT**, sujeita à reconciliação dos arquivos da própria R23.
- **F0:** mantém baseline **4/8 documentais**, sem certificação global ou holdout independente. **VLAB:** operação independente, último corpo recuperado R51, decisões R50/R51 válidas, **0/17 contratos terminais**, sem alegação de novos combates. Nenhum dado desta rodada foi devolvido ao VLAB como aceite confirmado.

**Antecedente preservacional da sessão:** nenhuma claim de INSTANCE-ID, writer/epoch/lease/fencing produtivo foi herdada. Não foram alterados OP, Diário, Inbox, fichas originais, Party, O Primeiro, normas nem motores. Registro entregue em pacote de arquivos MESTRE-SIDE; a sincronização Notion exige gate próprio.

## 2. Como interpretar corretamente as bandas da v1.1

Bandas intrínsecas totais da norma para efeito-padrão elegível, alvo único, Ação Padrão, sem hard-control/bypass maior:

| Rank de Efeito | DME intrínseco de entrada até ápice |
|---|---:|
| Bronze | 4–18 |
| Prata | 14–36 |
| Ouro | 22–62 |
| Ouro Negro | 38–96 |
| Lendário | 58–160 |

A **classificação nominal de uma criatura** não identifica automaticamente o **Rank de Efeito** da habilidade. FIP, chassi, modalidade, custo, alvo e autoridade especializada são dimensões próprias. A fonte de uma Besta que já informa `1d6+FOR` mantém esse dano explícito. Não se pode corrigir retroativamente para a banda da norma só porque sua média intrínseca `3,5` parece baixa.

**Auditoria diagnóstica sem reinterpretação canônica:** entre **9 ações B5** de 7 páginas da coorte R02, **7/9** têm média intrínseca abaixo do início da banda Bronze; entre **6 ações estritamente classificadas** da R03 (Prata1 ×3, Prata5 ×2, Ouro1 ×1), **6/6** têm DME intrínseco abaixo do início da banda nominal correspondente. O total **13/15** descreve *como essas fórmulas explícitas se distribuem*, **não 13 violações** da v1.1. Não houve neste recorte teste válido do procedimento gerador de uma habilidade nova sem dano explícito e com RE/FIP certificados.

**Diagnóstico do modelo v1.1:** sua finalidade como orçamento para preencher vazios está bem definida; sua calibração frente a todas as Bestas históricas **permanece INDETERMINADA**. Uma v2 que se baseasse na média bruta dos personagens para ampliar cegamente as bandas intrínsecas duplicaria atributos externos em muitos casos. O contrário — rebaixar a força ofensiva por ter DME baixo — também seria injustificado.

## 3. Estudos quantitativos estratificados (e denominadores)

| Coorte | Ações numéricas / páginas-fonte | DME médio | Bruto médio | Mediana bruta | Parcela agregada de atributos |
|---|---:|---:|---:|---:|---:|
| Bronze 5, R02 reconstrução | 9 / 7 | 3,9444 | 24,1667 | 26,5 | 83,68% |
| Classificação três-vias, R03 | 6 / 6 | 6,8333 | 41,8333 | 41,25 | 83,67% |
| R03+R04, amostra maior parcialmente conflitante | 29 / 26 páginas portadoras de fórmula | 188,5/29 = 6,5 | 1.199,5/29 = 41,3621 | ver arquivo linha a linha | 84,29% |

**Atenção à dependência:** R02 e R03+R04 não são amostras universais ou cegas; as 29 ações pertencem a **26 páginas**, de **53 páginas examinadas** em dois recortes, com famílias e versões correlacionadas. Não adicionar essas linhas para estimar prevalência mundial. Dados históricos distintos podem se sobrepor ao L002/L003.

**Subestrato R03 com título, corpo e ancestral concordantes, 6 ações/6 páginas:**

| Rank nominal | Ações | Bruto médio | Faixa de médias por habilidade |
|---|---:|---:|---:|
| Prata 1 | 3 | 35,0 | 32–40,5 |
| Prata 5 | 2 | 48,75 | 42–55,5 |
| Ouro 1 | 1 | 48,5 | 48,5 |

**Leitura correta:** Prata5 e Ouro1 se sobrepõem nesses casos; a diferença 48,75 → 48,5 **não** demonstra regressão de rank, pois Ouro1 tem apenas uma observação. Papéis, fontes e tipo de dano não são homólogos. Um único estrato vazio não impede análise legítima dos demais.

**Coorte física nova:** 24 páginas (8 Ouro5, 8 Ouro Negro1, 8 Lendário1), **23 sem fórmula numérica ofensiva completa**, **1 página com duas**, **0 páginas elegíveis à estatística estrita por rank**. Entre as fontes do grupo Lendário1 consta Wyvern com ancestral Lendário4, que não pode ser silenciosamente inserida em Lendário1. Quase todos os demais casos têm corpo classificado em patamar distinto, muitas vezes `Bronze` genérico. Não foram adjudicados. A atribuição dessa coorte aos lotes históricos permanece PENDENTE.

## 4. Papel dos atributos e limites da média

Os atributos impressos explicam **84,29% da soma das médias condicionais** das 29 habilidades de R03/R04 e **83,68%** da coorte Bronze5 R02. Isso sustenta uma **suspeita de grande sensibilidade dos números brutos a FOR/DES/INT nas fontes selecionadas**, mas não prova desequilíbrio, porque os atributos, custos, papéis e defesas obedecem a condições próprias. Ações correlacionadas devem ser pareadas antes de inferir efeito de rank ou estrela.

A hipótese de que "mesma esperança = mesma eficiência após RD" foi **refutada matematicamente num ensaio controlado**:

- **Fonte real:** [Lupusventus, Patada](https://app.notion.com/p/4bac2b324ede8321af6b01eb96452d04) `2d6+FOR25`, média **32**.
- **TEST média igual:** `4d6+18`, média **32**, mas maior variância.
- **TEST atributo +5:** `2d6+30`, média **37**.
- **TEST mais um dado:** `3d6+25`, média **35,5**.

Os oráculos exatos *condicionados à aplicação da mesma RD à parcela de dano e à realização da ação* mostram:

| Alternativa | Bruto médio | E(líquido), RD35 | P(líquido > 0), RD35 | E(líquido), RD42 |
|---|---:|---:|---:|---:|
| Patada real 2d6+25 | 32 | 0,1111 | 8,33% | 0 |
| TEST 4d6+18 (mesma média) | 32 | 0,3534 | 15,90% | 0 |
| TEST 2d6+30 (atributo +5) | 37 | 2,2778 | 72,22% | 0 |
| TEST 3d6+25 (dado +1d6) | 35,5 | 1,4583 | 50,00% | 0,00463 |

**Ponto novo e discriminante:** em RD42 o bônus de atributo +5 produz **0** dano líquido em todos os acertos, ao passo que um dado adicional pode produzir **1 dano em 1/216 combinações**, embora sua média bruta seja menor. É um efeito de cauda da distribuição, não uma anomalia do RPG. Não implica que o ataque 3d6 seja, em geral, melhor que bônus de atributo.

O exemplo deve ser aplicado somente a alvos para os quais a mesma RD realmente seja a mitigação competente. Não houve chance de acerto, reação, crítico, geometria ou combate nativo no cálculo.

## 5. Tipos, formas de aplicação, custos e defesa

A nova coorte contém descrições de área, regeneração, DoT, empurrão, controle e fraqueza; não contém, em 23 páginas, os números necessários para lhes atribuir DPS. O catalogador que extraísse automaticamente `1d10` de *drops* como dano criaria uma falsa curva de progressão. No [Escarlate Flamejante](https://app.notion.com/p/19ec2b324ede8335b35c01fff05380ec), `1d6 por turno` aparece em **Cura Solar**, não no dano da Chama Ardente.

Em experimentos anteriores, o arco de Iskiel e a magia de Eristan já permitiram investigar ataque/CA e Salvaguarda/PA. São controles, **não descobertas novas desta execução**. Sobreposição de RD física, resistência por componente, duração de DoT, mitigação de dano misto e ações dependentes de Reação permanecem limitadas à autoridade realmente documentada, sem inferir solução universal.

A ciência daqui em diante deve distinguir **DME intrínseco**, **dano bruto condicional**, **chance de acertar**, **pós-RD**, **esperado por tentativa**, **eficiência por PA/ação** e **dano realizado em cena**, no formato da carta do laboratório. Sem ficha integral de ataque/defesa, não se estima acerto universal nem vitória.

## 6. Matriz de anomalias / explicações alternativas

| Achado | Classificação científica | Hipótese alternativa / limitação | Ação dirigida |
|---|---|---|---|
| Fórmulas antigas têm DME abaixo da faixa nominal em 13/15 casos | **CONFIRMADO como observação amostral, NÃO erro v1.1** | Fonte explícita anterior, Rank de Efeito ≠ Rank da Besta, chassi de Besta especializado | Não retcon; criar contrato de elegibilidade RE/FIP e teste de geração ausente |
| 28/29 fórmulas selecionadas têm atributo impresso; agregação 84,29% | **INDÍCIO** de peso elevado nas amostras | Seleção de fórmulas completas, espécies/versionamentos correlacionados, papéis e custos variáveis | Ampliar comparações intraficha e estratos validáveis, com clusters |
| Apenas 1/24 fontes novas com fórmula ofensiva completa | **CONFIRMADO na coorte congelada** | Seleção por título, alto nível com descrições qualitativas; fonte parcial, não dano zero | Contrato de backfill experimental em réplicas TEST e provenance |
| 0/24 novas fichas com classificação integralmente coerente | **CONFIRMADO na coorte congelada** | Conflitos de versão/árvore/nome, estrela não declarada no corpo | Adjudicação por autoridade, sem classificação de conveniência |
| Mesma média bruta, eficiência pós-RD distinta | **CONFIRMADO matematicamente em TEST** | Caudas e piso zero da RD, não bug | Incluir PMF/quantis e chance pós-RD em relatórios candidatos |
| Progressão Prata5 → Ouro1 de 48,75 → 48,5 | **INDETERMINADO** | n=2 versus n=1, fontes diferentes | Não afirmar queda de rank; obter amostra pareada abrangente |
| Fraqueza elemental / multi-hit / duração | **PENDENTE** de contratos de tipologia/ação e provas | Quantidades de drop, cura, controle não equivalem a dano | Separar por família, não construir DPS ausente |

## 7. Carteira priorizada de aprimoramento — NÃO CANÔNICA

**CAND-01 (PRIORIDADE ALTA) — Qualificador de elegibilidade e proveniência para aplicar DMG-RANK**. Antes de gerar valores, exigir `fonte com dano numérico?`, `Rank de Efeito/FIP legitimados?`, `tipo/chassi`, `caráter Ação Padrão/alvo único`, `condições/custo/controle`, `campo original intocado`, `flag TEST`. Pode ser ferramenta/documentação operacional, sem editar v1.1. **Falsificador:** ferramenta encontra falsas exclusões em fontes autoritativas conhecidas ou inventa rank; corrigir antes de expandir.

**CAND-02 (PRIORIDADE ALTA) — Relatório de risco pós-RD por distribuição, além da média**. Para qualquer habilidade cuja RD competente seja conhecida, exibir expectativa pós-RD, fração de rolagens com dano positivo, intervalo mínimo/máximo, quantis e custo aplicável. Não muda os dados nem transforma dado bruto em regra. **Falsificador:** casos independentes homologados onde métrica é calculada incorretamente ou não tem utilidade discriminante.

**CAND-03 (PRIORIDADE MÉDIA) — Backfill de habilidade numérica ausente APENAS em réplicas**. Selecionar ficha com identidade/rank verificados, derivar variantes pelo DMG-RANK, manter original, comparar intervalo predito com ataques completos de mesmo contexto e avaliar trade-offs por PA/controle/área. Não inventar fórmula para 24 fontes conflitantes sem reconciliação. **Falsificador:** premissas RE/FIP inválidas, colisão com chassi da Besta ou dupla contagem de bônus.

**CAND-04 (PRIORIDADE MÉDIA) — Teste agrupado de progressão nominal, condicionado ao contexto**. Comparar efeitos de mesma família/tipo/ação/custo entre estrelas com fontes e estado de atributos completos; estimar variação de DME, bruto, acerto e RD. Reservar holdout de novas famílias não consultadas. **Falsificador:** desaparecimento do efeito após controle por atributo e tipo, ou dados insuficientes.

**CAND-05 (HOLD) — Alteração numérica universal das bandas / DMG-RANK v2.** A amostra atual não sustenta escolha de novos coeficientes; não propor números arbitrários. Só liberar candidata se coortes representativas e elegíveis demonstrarem desvios não explicados, testes comparativos e revisão normativa/independente.

## 8. Validação matemática, interface VLAB e requisitos históricos

`REPRODUCE_DIAGNOSTIC.py` refaz as distribuições pela **convolução discreta**, enquanto `INDEPENDENT_AUDIT.py` percorre **todas as faces com `itertools.product`**, além de comparar o manifesto interno do ZIP R11. **116/116 verificações locais passaram**. Isso comprova consistência aritmética e o registro recuperado, **não** a correção de um motor ou a integridade física das 24 fichas além da reabertura no Notion.

**Interface VLAB:** nenhum novo combate foi enviado ou executado nesta operação. O handoff read-only solicita futuramente, se necessário, apenas eventos discriminantes relacionados a atributos/cauda pós-RD ou mitigação legal, com seed, tipo, custos e mecanismos existentes; não demanda scheduler, multi-reatividade ou obra de motor. Antes de enviar, verificar se VLAB R52+ já resolveu a questão.

**B01–B18:** matriz histórica preservada. Esta análise gera elementos matemáticos auxiliares, mas não altera 1/18 PASS documental nem as pendências do R23. **STRICT 0/2, F0 4/8, I0003 0/9, L003 0/71 e VLAB terminal 0/17** ficam separados. Nenhum percentual global válido de cobertura F0–F18 foi calculado.

## 9. Dez etapas da ordem atual — produto e aceite proporcional

| Etapa | Entrega produzida | Estado |
|---|---|---|
| 1 Recuperação | CSV R02/R03/R04, matriz física R11, identidade de fontes, 24 páginas novas, manifest | **PARTIAL**: L002/L003, I0003 e writer pendentes |
| 2 Diagnóstico v1.1 | Tabela RE×DME e matriz 15 ações observadas; separação de escopo | **PASS ANALÍTICO** (não normativa) |
| 3 Atributos/dados | 9 B5, 6 estritas, 29 ações histórico R04; contribuição e sensibilidade | **PASS ANALÍTICO** |
| 4 Rank/estrela | Prata1/Prata5/Ouro1 três-vias, 24 novos Ouro5/ON1/L1 e lacunas | **PARTIAL**, sem generalização |
| 5 Tipos/modalidades | Roles reais numéricos versus cura, drops, DoT/área e variantes | **PARTIAL**, tipos/custos incompletos |
| 6 Eficiência | RD exata nas variantes, chance de líquido positivo; acerto não inventado | **PASS MATH-ONLY**, não combate |
| 7 Anomalias | Distinção dados/precedência, documentação, cauda da RD, explicações alternativas | **PASS DIAGNÓSTICO** |
| 8 Melhorias | Cinco candidatas com 4 propostas limitadas + 1 HOLD v2 global | **PASS PROPOSITIVO** |
| 9 Validação | 116/116 QA independente e negativos de imputação/rank | **PASS LOCAL** |
| 10 Dossiê | PSV integrado, matriz, arquivos, manifests e fronteira de sucessão | **PASS LOCAL**, sincronização Notion pendente |

## 10. PSV-FAST-RESUME / Handoff para possível sucessão

- **AS-OF:** 2026-10-16, operação MESTRE-SIDE.
- **OPERATION:** CM-000001 / OP-DMG-CORPUS-EMP-01, mesma operação. **BASELINE:** DMG-RANK-01 v1.1 oficial inalterada.
- **LAST-VERIFIED-UNIT:** 24/24 páginas da nova coorte reabertas; 15/15 fórmulas de coortes R02+R03 recomputadas com suas premissas; 29/29 ações R04 reanalisadas em composição ponderada; 116/116 QA matemáticas/recuperação do R11 PASS.
- **FIRST-PENDING:** fonte real de patamar alto com **classificação três-vias e dano/RE/FIP legitimamente admitidos**; antes de comparar progressão, resolver a classificação da fonte e risco de referência de versões. Em paralelo, recuperar primários I0003/L003 *somente com localizador novo*.
- **DENOMINATORS:** novo recorte 24 páginas/3 estratos/8 por estrato, 1 página portadora de 2 fórmulas ofensivas, 23 incompletas, 0 elegíveis para inferência estrita; coorte B5 9 ações/7 páginas, estrita R03 6/6, R04 29 ações/26 páginas portadoras de expressão de 53 examinadas; histórico L002 45 relatadas, L003 71 relatadas e 0/71 individualmente certificadas; F0 4/8; B 1/18; STRICT 0/2; CSV I0003 0/9; VLAB 0/17 terminal.
- **NO-REPEAT:** não repetir R03/R04, Galidemus/Iskiel, R50/R51 ou confrontos VLAB sem nova hipótese; não conferir 47 CSV/114 ZIP sem novo localizador; não contar réplicas/testes como Bestas independentes; não somar lotes desconhecidos.
- **CONFLICTS:** 24/24 nova coorte sem concordância rank plena; título/body/ancestor, nome e versão; 0/24 elegíveis. Exemplos Aurora/Ouro5↔Prata5 e Wyvern/Lendário1↔Lendário4.
- **UNKNOWN-EFFECT:** não houve escrita Notion ou chamadas a motores nesta rodada; nenhum efeito remoto desconhecido. Upload da Library somente se realizado e validado ao encerrar o pacote.
- **AUTHORITY/WRITER:** decisão Mestre DIR-MESTRE-LABS-REPLICAS-20261016-001 autoriza experimentação em cópias isoladas, mas não prova assignment exclusivo, writer/lease/epoch/fencing produtivo, nem entrega/ACK de outro Comestre. Nenhum documento original foi editado.
- **NEXT-5:** (1) recuperar exemplar tri-validado de Besta sem fórmula e com RE/FIP competente ou concluir razão da ausência; (2) testar candidatura CAND-01 em cópia, sem novo cânone; (3) construir pareamento controlado por tipo/ação/custo entre estrelas de mesma família, se fontes permitirem; (4) reservar holdout independente e auditar causalidade de rank/tipo/atributo; (5) somente depois avaliar se há evidência para mudar bandas e remeter ao Mestre cenário de trade-offs, sem canonizar.
- **TARGET-REMAINDER:** F0–F18 cobertura global **NÃO DETERMINÁVEL**; fontes físicas e aceites B restantes só mudam por evidência própria. Produzir próximo modelo que compare **critério atual vs alternativa** em famílias com admissibilidade comprovada.
- **NAC-PASS:** verificação científica local/isolamento de escrita e código **PASS**; validação de fonte atualizada, laboratório Notion físico, writer, publicação do registro operacional, produção/canônico **HOLD**. Nenhuma alteração na v1.1.
- **HANDOFF:** `HANDOFF_VLAB_RESEARCH_ONLY.json` encaminhável apenas após controle de não duplicação; nada foi recebido ou executado pelo VLAB nesta rodada.

### Proveniência mínima do pacote

`PREREG_SOURCE_SAMPLE.json` (congelado antes dos 24 fetches) → `results/SOURCE_LEDGER_24.json` → `readonly_sources/*.csv` e `DMG-F1-R11...zip` → `REPRODUCE_DIAGNOSTIC.py` → `results/DIAGNOSTIC_RESULTS.json` → `INDEPENDENT_AUDIT.py` → `results/INDEPENDENT_AUDIT.json` → `figures/*.png` → `MANIFEST_SHA256.json` → pacote final. Os arquivos de coortes históricas são cópias read-only e seus originais não foram reescritos.

**Aceite de coordenação:** a entrega central é este *diagnóstico limitado mas utilizável*, não uma segunda execução dos contratos VLAB nem simples aumento de números de testes.
