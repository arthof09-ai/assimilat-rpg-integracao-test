# PA Universal R05 — Parecer científico, executivo e de governança (MESTRE-SIDE)

**AS-OF 17/10/2026. Ambiente: TEST. Baseline físico preservado: PA R04 SHA-256 `2c64788b33b6e486f3edc45334b462f88fce8fb2db02fc742aa6b0b2e954cc46`; QMC-02 SHA-256 `2763d96ba3624741a89d0d2159000826584ed932e11fbf6ef8e637ab3858d92a`.**

## 1. Correção expressa do Mestre: atributo = 5 PA/dia por ponto

O Mestre determinou na ordem R05, em 17/10/2026: **"1 atributo = 5 pontos de PA por dia. Os itens que não seguem essa regra estão erradas."** Aplicação: bônus numérico de atributo **permanente/enquanto equipado**. Portanto, `Custo_PA_dia_atributos = 5 × soma dos bônus numéricos de FOR/DES/CON/INT/SAB/CAR`, contabilizando cada componente apenas uma vez e excluindo perícias, Reflexo, percepção, CA ou bônus de ataque, que NÃO são pontos de atributo. A determinação é **normativa do Mestre**, NÃO coeficiente inferido estatisticamente. Para ativação transitória/1x dia, o Mestre definiu a taxa diária do bônus permanente, NÃO automaticamente a tarifa PA/uso.

Consequências funcionais: um item cujo ÚNICO efeito seja `+5 DES` em manutenção diária tem **25 PA/dia** pela regra. Se o item também confere dano ou proteção, **25 é parcela de atributo**, e o total diário fica **INDETERMINADO** até completar as outras famílias de efeito; não presumir taxa base positiva ou sinergia zero. A regra não foi escrita no Notion canônico: sua autoridade vem da correção direta do Mestre nesta conversa, e a canonização física deverá passar por NAC-NORM-01 e writer/registro competente.

## 2. Auditoria de conflitos contra a regra

Fontes individuais reabertas no Notion Mestre e preservadas nos dados R04; matriz no arquivo `RESULTADOS/AUDITORIA_ATRIBUTOS_R05.json`.

| Fonte / UUID | Origem | Custo histórico | Bônus | Resultado R05 |
|---|---|---|---|---|
| [Amplificador](https://app.notion.com/p/3c6c2b324ede82baa4a801de533a5975) `3c6c…5975` | Espelho da Party | 15 PA/dia | +3 atributo | Conforme, **espelho não calibra Mestre** |
| [Sabedoria Ancestral](https://app.notion.com/p/3edc2b324ede815699adc0412e96ea2b) `3edc…ea2b` | Catálogo Mestre | 20 PA com leitura R-PA-DIA sensível | +10 SAB e outros poderes | **INCONSISTÊNCIA:** só atributos exigem 50 PA/dia, diferença mínima 30, **caso interpretação diária se confirme**; custos dos outros poderes não identificáveis |
| [Colar cadente](https://app.notion.com/p/3edc2b324ede810daba2cc509677856c) `3edc…856c` | Catálogo Mestre | 14 PA/dia explícitos | +2 SAB normal, +4 SAB sob estrelas | **INCONSISTÊNCIA CONDICIONAL:** +4 exige 20 PA/dia (mínimo 6 acima). +2 exige 10; ainda há 4 não atribuíveis |
| [Amuleto de Inteligência](https://app.notion.com/p/0c4c2b324ede83dd8e1881b52a79e326) `0c4c…e326` | Espelho da Party | 30 PA isolados com R-PA-DIA sensível | +10 INT e outros efeitos | **CONFLITO HISTÓRICO:** atributos exigem 50 PA/dia, mínimo 20 acima, condicionado ao contexto; **sem escrita Party** |
| [Espada do Lendário](https://app.notion.com/p/3edc2b324ede81ab9e22e168f6d939a9) | Mestre | 600 PA/dia | +60 FOR e outros | Parcela de FOR =300; restante não isolável; não afirmar que 600 está correto por isso |
| [Lâmina Aurora Boreal](https://app.notion.com/p/a70c2b324ede83c2ac490135cd512e9f) | Espelho | 95 PA/dia | +5 CAR, +7 FOR, +3 CON | Atributos=75; restante 20 não identificado; nenhum coeficiente extra inferido |

São **10 comparadores** com bônus e custo diário selecionados auditados no arquivo estruturado, com **3 conflitos** identificados (2 Mestre, 1 Espelho). Esta amostra NÃO é censo de todos os itens com atributo.

**Errata de leitura:** [Adaga da Serpente Enfeitiçada](https://app.notion.com/p/3edc2b324ede811787a0de913622b14d): o literal é **"35 de PA."**, após efeitos de dano, seguido por metadado de Anel Dimensional. A R03 converteu para 35 PA/dia. A QMC-02 havia deixado INDETERMINADA. O R05 **preserva a classificação histórica R03 em seu baseline** e **não usa 35 como custo diário certificado** até reconciliação de R-PA-DIA pelo dono da regra/fonte. Não converter automaticamente `N de PA` em `N PA`.

## 3. Corpus e desenho amostral

R04 forneceu **108 fichas físicas distintas**, em três domínios: 88 Mestre indexadas (54 equipamentos + 34 inscrições/matrizes; **14 custos diários numéricos** = 12 explícitos e 2 inferidos R-PA-DIA), 18 Espelho (16 custos diários) e 2 Incubação (zero). A linha `source_type=NOTION_MASTER` de parte do corpus R03 está semanticamente incorreta para fontes do Espelho; utilizar a superfície física reconciliada em R04.

Selecionei **antes da consulta dos custos** três coortes adicionais, com JSON pré-registrado e hashes preservados:

- **19 candidatos por títulos de itens mágicos** encontrados em buscas dirigidas: readbacks físicos mostraram **17 Espelho da Party**, **2 Incubação**, **0 catálogo Mestre oficialmente comparável**. Não promover custos desses grupos.
- **28 Técnicas & Pergaminhos**: todas as 28 fichas-filhas da categoria `RPG / Itens / Técnicas & Pergaminhos`, novas no corpus R03. **Zero custos numéricos de PA no texto lido**, com mecânica às vezes preservada em imagens. São registros Mestre, mas **zero observações energéticas completas**.
- **27 Consumíveis**: **20 Pílulas + 7 Poções** do índice físico Mestre, todos reabertos, **zero custos numéricos de PA no texto lido**. Consumo de medicamento/efeito não implica custo de PA; receitas antigas não autorizam novas receitas.

Somatório **182 UUIDs físicos distintos no conjunto expandido**, particionados: **143 Mestre catalogados (88+55), 35 Espelho (18+17), 4 semicanônicos (2+2)**. **Novas páginas Mestre 55; novas observações Mestre independentes UTILIZÁVEIS PARA CUSTO DE PA: ZERO**. Não afirmar censo global de todos os itens do RPG nem leitura/extração de mecânica de imagens. O único denominador fechado é das categorias indexadas e efetivamente percorridas. Não há holdout Mestre independente com custo numérico após a R04: **0**.

Dos 14 custos Mestre históricamente numéricos: 12 explícitos, 1 R-PA-DIA **sensível** (Sabedoria Ancestral), 1 modalidade não aceita na R05 (Adaga). Excluindo os dois casos em conflito com a regra do Mestre (Sabedoria Ancestral/Colar cadente) e a Adaga ambígua, há **11 fichas com custo diário para análise exploratória**, correspondendo a **10 linhagens provisórias** por causa de possível duplicação do texto Veste Dragão Ascendente/IMPERIAL. A independência científica das linhagens não foi homologada.

## 4. Identificabilidade dos coeficientes

**Identificado por decisão expressa (não estatística):** **5 PA/dia por +1 ponto de atributo permanente**. **Novos coeficientes universais estimados empiricamente no domínio Mestre = 0.** O motor não autoriza estimar custos numéricos de novo dano adicional, RD, CA, RDM, alcance, frequência, área, cura, controle, mobilidade, salvaguardas, percepção ou multiplicador passivo/ativo porque só há misturas com efeitos não isolados ou valores em unidades diferentes. O custo documental de uma habilidade existente (por exemplo, Bota: 5 PA/ativação) continua individualmente utilizável em modo HISTÓRICO, não como tarifa para outra habilidade. Matriz `RESULTADOS/MATRIZ_IDENTIFICABILIDADE_R05.json` registra observações/assunções por parâmetro.

Matemática de dano: bônus +20 por acerto pode ser avaliado quanto ao incremento de dano bruto/condicional pós-RD por tentativa, com parâmetros de acerto e frequência explícitos, mas **não** convertido em PA sem uma regra de preço energético. Para uso 1x/dia, mudar frequência/modo de ativação **não fornece automaticamente PA/uso**.

## 5. Validação negativa reproduzida, limites estatísticos

Regressões antigas R03=128/128 e QMC-02=37/37 **preservadas como baselines**, não contadas como 165 novos testes. Em R05, regressão **dirigida** de 31 casos PASS (regra de Mestre, divergências, modo diário/uso, fonte, payload/segurança, diálogo, orçamento), além de **10 cenários conversacionais A–J**.

Como não apareceu nenhum item Mestre novo com custo numérico, o **holdout confirmatório Mestre segue 0**, sem intervalo de erro válido para novos custos. Foi realizada somente validação exploratória RETROSPECTIVA por grupos: **n=11 páginas com custo tipado não conflitado; 10 agrupamentos provisórios**, cada grupo reservado sucessivamente fora da mediana de treino. Baseline constante 20 PA/dia: **MAE 78,2 PA/dia**; mediana dos demais grupos: **MAE 81,7 PA/dia**. Ambos fracassam como modelo geral e os dados já haviam sido vistos antes da R05, logo NÃO qualificam holdout confirmatório. Grupos pequenos, seleção não aleatória e cauda de 600 PA/dia invalidam generalização causal por família.

## 6. Integração CRAFT QMC-02 — ponto de verdade

**Histórico real, fonte Bota:** executei o **entrypoint original** `BASELINE_QMC02/qmc02/qmc02.py --envelope ... --item ...`, gerando qualificação original `QUALIFICACAO_FONTE_AUTORIZADA_EM_EXTRATO` e campos literais 18 PA/dia, 5 PA/ativação. O motor R05 e a ponte R05 reavaliaram a fonte com identidade/URL e hash de excerto, conferiram custos contra corpus R03 preservado; **recebimento local TEST aprovado**. A ponte tem validação adicional: mesmo um digest recalculado após alteração de custo é rejeitado porque o custo e a extração são verificados contra os originais recuperados. O digest SHA sem chave **NÃO autentica o Notion**.

**Candidato novo (+20 dano, +5 DES):** ponte aceita **parecer TEST sem aprovação**: subtotal obrigatório de atributo =25 PA/dia, total diário `null`, PA/uso `null`, efeito de dano e condições documentados como desconhecidos.

**Limite decisivo:** função ORIGINAL `qmc02.validate_external_pa()` continua retornando `INTERFACE_EXTERNA_NAO_CONTRATADA`. Logo **NÃO HÁ ACEITE NATIVO da QMC-02** nem prova de integração nativa produtiva. O executor CRAFT com autoridade própria deve integrar a versão R05 e realizar teste na bancada original; não modificar aqui sua fonte original por falta de Assignment/writer/lease. Handoff `HANDOFF_PARA_EXECUTOR_CRAFT_QMC02_R05.md` traz contrato, entradas, negativas e gates. O adaptador R05 não é nova fábrica nem receita.

## 7. Orçamento de PA e segurança

[Sistema de Magia](https://app.notion.com/p/3ebc2b324ede81f7b343f7270ff91373): **PA Total − PA comprometido = PA Livre**. A ficha do item informa 25 PA/dia para +5 DES, mas não estabelece universalmente se seu PA diário opera como reserva COMMIT ou débito DEBIT. Com 80 PA Livres declarados, cenário **condicional** de 25 PA comprometidos adicionais deixaria 55 Livres, se os 80 foram medidos ANTES do compromisso; se já forem após o compromisso, não subtrair novamente. Para combinação com dano/movimento de custo desconhecido, resultado permanece INDETERMINADO. A consequência de Exaustão por conjuração mágica não se estende automaticamente à ativação de itens.

## 8. Gate, autoridade, conflitos e próxima fronteira

- OP/IDENTIDADE: executor PA ainda sem atribuição canônica localizada demonstrada; subfrente energética vinculada à operação CRAFT `OP-ARQ-RIN-REC-01` e ao contrato `QMC-PA-INTERCHANGE-CANDIDATE-1` para teste, **não reivindica CM-000002 ou instance-id**.
- Baseline CRAFT/QMC original, R01–R04 e SHA intactos; no new recipes, 0 REC-ID, 0 alterações oficiais, 0 Party/O Primeiro writes.
- F5 RED, `C19-021 UNKNOWN-EFFECT`, writer/lease/fencing produtivo não comprovado, receitas PROIBIDAS e produção HOLD.
- NAC-NORM-01: alteração da regra de atributos determinada pelo Mestre, **precisa registro/canonização no objeto normativo competente**; não criar norma concorrente.
- NAC-PASS-02: integridade/testes TEST local verificados; ciência geral, produção, validação de holdout e aceitação nativa CRAFT em **HOLD**.
- Próximos 5: (1) corrigir fontes atribuindo mudanças apenas após revisão competente; (2) obter pares novos independentes com preço de PA por mesmo efeito, não mais páginas vazias; (3) executar holdout mestre pré-registrado; (4) Executor CRAFT instalar validador nativo com ACK/gate e fazer prova positiva; (5) revisão científica/NAC-PASS de promoção, mantendo receitas suspensas até liberação expressa.
