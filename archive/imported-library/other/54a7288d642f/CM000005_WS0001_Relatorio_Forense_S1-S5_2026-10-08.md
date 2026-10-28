# SCI-SNT-PROV-REPORT-20261008-01 — Auditoria forense S1–S5

**Classificação:** MESTRE-SIDE — PROJETO RPG DO MESTRE / Comestre. Não distribuir à Party/O Primeiro.

**Responsável lógico:** CM-000005 — Comestre Cientista 1; WS0001 — Engenharia do Comestre Agendado.  
**Operação:** PLAN-75 / P0-FRESH-12, 7 de outubro de 2026.  
**Estado deste relatório:** ANÁLISE READ-ONLY / RECONCILIAÇÃO DAS FONTES ACESSÍVEIS CONCLUÍDA / REGISTRO CANÔNICO PENDENTE.  
**Sem takeover de INSTANCE-ID, writer, claim, lease ou epoch.** Não foram criadas nem rearmadas sentinelas e os canários não foram modificados.

## 1. Veredito executivo

- **Contenção do agendador:** S1–S5 estão desativadas, com `COUNT=2` no agendamento final e notificações/e-mail desligados. Isto demonstra estado seguro atual, não a causa individual de cada fim nem PASS científico.
- **Cobertura física eventual:** 12/12 canários possuem M1 standalone após normalização semântica de Markdown/pipe escapado; 13 linhas M1 ao todo.
- **Falha material de correção:** C05 contém **duas** linhas M1 semanticamente equivalentes. Cardinalidade permitida=1, observada=2. Defeito não removido.
- **Estado do crédito:** os 12 canários continuam registrando `STATE=READY`, `RESULT=UNTESTED`, `EMPIRICAL-CREDIT=0` e M1 `COMMITTED-UNVERIFIED`. Valor administrativo registrado: 0/12 créditos; não confundir com inexistência dos efeitos.
- **Confiabilidade:** FRPE da onda, fração de falhas por firing, recovery latency e autoria causal de cada efeito **NÃO DETERMINÁVEIS** com as fontes disponíveis. Meta ≥75% não foi demonstrada.
- **Proveniência:** 16 instantes distintos de `last_run` documentados para S1–S5. São um limite inferior de observações de agendamento, não o inventário completo de firings. A API acessível disponibiliza o último firing por tarefa, sem histórico enumerado de execução/toolcalls.
- **Veredito científico:** `EVENTUAL-MATERIAL-COVERAGE=12/12`; `IDEMPOTENCY=FAIL-CONFIRMED(C05)`; `FRPE=INCONCLUSIVE`; `SCIENTIFIC-PASS=NOT-GRANTED`; `PLAN-75=NOT-CLOSED`.
- **Lacuna de fechamento:** o cientista conversacional não entregou relatório final tempestivo; a arquitetura não possuía fechamento independente demonstrado. A conclusão não depende de comprovar crash do chat. RISK-SCI-CLOSURE-01 e NAC-AUTO-CONT v1.11/v1.12 tratam governança dessa falha.

## 2. Matriz completa de `last_run` recuperados (16/16 observações identificadas)

Todos os horários da matriz são **07/10/2026, America/Recife**. O evento confirmado é a presença histórica do valor `last_run` em uma fonte reaberta. **Nenhuma linha por si prova mutação naquele firing.**

| Worker | `last_run` documentado | Fonte | Classificação por disparo |
|---|---|---|---|
| S1 | 13:58:19 | RPT-PLAN75-001 | Firing observado. C01 tem última edição 13:58:16: correlação forte, autoria NÃO comprovada. |
| S1 | 15:05:15 | EXEC-002 | Firing observado; C06 ainda não presente no snapshot posterior; outcome do firing UNKNOWN. |
| S1 | 20:04:45 | Cadastro final | Firing observado; outcome individual UNKNOWN. |
| S2 | 13:08:27 | RPT-PLAN75-001 | Firing observado; C02 já possuía M1 no snapshot, mas último edit da página é 12:09:50, anterior ao firing observado; autoria UNKNOWN. |
| S2 | 14:14:41 | DELTA-01 | Firing observado; 4/12 M1 antes/depois do snapshot segundo relatório; **sem novo target único confirmado**, não converter automaticamente em FAIL/NO-OP. |
| S2 | 15:10:14 | EXEC-002 | Firing observado; C07 ainda ausente na reabertura posterior; outcome individual UNKNOWN. |
| S2 | 20:08:06 | Cadastro final | Firing observado; outcome individual UNKNOWN. |
| S3 | 13:21:56 | RPT-PLAN75-001 | Firing observado. C03 tem última edição 13:21:49: correlação forte, autoria NÃO comprovada. |
| S3 | 15:19:16 | EXEC-002 | Firing observado; C08 não presente no snapshot; outcome individual UNKNOWN. |
| S3 | 20:26:04 | Cadastro final | Firing observado; outcome individual UNKNOWN. |
| S4 | 13:38:53 | RPT-PLAN75-001 | Firing observado; C04 já tinha M1, com última edição 12:39:10. Versão do prompt naquele firing não preservada. |
| S4 | 14:38:33 | EXEC-002 | Firing observado; versão atual é short/direct fixo C04; com target já preenchido, NO-OP é hipótese, não resultado per-run comprovado. |
| S4 | 20:34:12 | Cadastro final | Firing observado; C04 continuava preenchido; resultado do firing UNKNOWN. |
| S5 | 13:47:49 | RPT-PLAN75-001 | Firing observado; C05 ainda sem M1 no snapshot às 13:58; sem efeito novo confirmado naquele snapshot. |
| S5 | 14:46:12 | EXEC-002 | Firing observado; C05 já presente às 15:19, mas autor do efeito UNKNOWN. |
| S5 | 19:47:03 | Cadastro final | Firing observado; C09 tem última edição 19:46:59 (~4 s antes). Fallback para C09 é hipótese forte, não prova de RUN-ID/autor. |

**Fontes desta matriz:**
- [RPT-REFLEX-PLAN75-001](https://app.notion.com/p/3f2c2b324ede81379c18c312a50b3aab) (snapshot 13:58)
- [DELTA-01 S2](https://app.notion.com/p/3f2c2b324ede81c185bbe8af7301eb40) (14:14)
- [RPT-REFLEX-EXEC-002](https://app.notion.com/p/3f2c2b324ede818cb42cd4cedf5c2d50) (snapshot 15:19)
- Cadastro atual de automações S1–S5 (task IDs na seção 5).

**Denominador:** 16 observações distintas identificadas e reconciliadas 16/16. **Isso não significa 16 firings totais nem 100% do histórico real recuperado.** Firings intermediários sem registro observável são UNKNOWN.

## 3. Matriz dos 12 canários: leitura física atual

Horário **última edição da página** em Recife; não é um carimbo dedicado ao append M1 e não fornece autoria do worker. Cada página foi reaberta; `READY`, `UNTESTED` e crédito 0 permanecem. Filtros de M1: linha standalone, remoção de backticks, `\\|`→`|`, whitespace normalizado; menções na instrução/EXPECTED foram excluídas.

| Alvo | M1 standalone | Última edição da página (07/10 BRT) | Leitura da autoria |
|---|---:|---|---|
| C01 | 1 | 13:58:16 | Coincide temporalmente com S1 13:58:19; provável, não provado |
| C02 | 1 | 12:09:50 | Compatível com afinidade S2, sem firing de 12:09 recuperado |
| C03 | 1 | 13:21:49 | Coincide com S3 13:21:56; provável, não provado |
| C04 | 1 | 12:39:10 | Compatível com S4/direct, antes do primeiro `last_run` recuperado de S4 |
| C05 | **2** | 16:49:44 | Primeiro M1 já observado às 15:19; horário de cada uma das duas linhas é desconhecido |
| C06 | 1 | 16:58:56 | Afinidade S1; sem RUN-ID |
| C07 | 1 | 18:12:58 | Afinidade S2; sem RUN-ID |
| C08 | 1 | 16:26:40 | Afinidade S3; sem RUN-ID |
| C09 | 1 | 19:46:59 | Fallback de S5 19:47:03 plausível; sem RUN-ID |
| C10 | 1 | 15:46:05 | Afinidade S5; marker escapado já presente ANTES de supervisora posterior |
| C11 | 1 | 19:01:53 | Afinidade S1; sem RUN-ID |
| C12 | 1 | 19:08:12 | Afinidade S2; sem RUN-ID |

**Prova material e IDs canônicos:** [P0 pai](https://app.notion.com/p/3f2c2b324ede819bbb02c03abdbb94d6), com links para C01–C12. [POSTWAVE-003 — errata](https://app.notion.com/p/3f2c2b324ede813ab13de721c41a9a94) e [Diário OP-SCI-CX99-02](https://app.notion.com/p/3f1c2b324ede81e5a480ef85fb003b8e).

**Snapshot drift:** relato das 13:58 mostra 4/12; EXEC-002 posterior identifica 5/12 incluindo C05 após corrigir false-negative. Contenção do Coordenador havia listado 6/12 sem C05; este valor não deve ser tratado como contagem semântica total se a linha escapada já estava presente. POSTWAVE-003 foi corrigido por errata de 11/12 para 12/12. Nenhum snapshot histórico pode superar a reabertura final.

## 4. Taxonomia de falhas, créditos e limitações

| Dimensão | Conclusão | Confiança |
|---|---|---|
| Scheduler | 5 tasks desativadas; COUNT=2 nas cinco programações finais; notify/email OFF | VERIFICADO no cadastro final |
| Ocorrências de last_run | 16 valores históricos distintos documentados | VERIFICADO nas fontes acessíveis |
| Total real de firings | Não disponível: primeiras/intermediárias e histórico por run ausentes | UNKNOWN |
| Cobertura eventual semântica | 12/12 = 100% dos **targets**, não da confiabilidade | VERIFICADO |
| Linhas M1 | 13 linhas em 12 targets | VERIFICADO |
| Excedente de duplicação | C05 +1 linha, afetando 1/12 targets | FALHA MATERIAL CONFIRMADA |
| Falhas por firing | Não há denominador nem outcomes individuais completos | NÃO CALCULÁVEL |
| FRPE-FIRST | Exposição 1 elegível e autoria de cada M1 desconhecidas | NÃO CALCULÁVEL |
| Recovery tardio | Snapshots revelam crescimento 4→5→12, com oportunidades anteriores sem progresso em afinidades | SUPORTADO COMO FENÔMENO, NÃO TAXA/CAUSA |
| S2 14:14 | Novo `last_run`; snapshot manteve 4/12, sem novo efeito único observado | VERIFICADO; motivo UNKNOWN |
| S4 comparabilidade | Prompt atual é P0-SHORT-v1 fixed C04, outros 4 shared queue | HETEROGENEIDADE CONFIRMADA |
| C10 | M1 já existia com pipe escapado em página editada 15:46:05; não foi produzido pela sentinela supervisora das 20:26 | MATERIAL PRESENTE; autor UNKNOWN |
| C05 causa raiz | Escape de pipe / matcher literal inadequado é hipótese plausível; race/claim também possível | NÃO ATRIBUÍDA |
| Efeito material com verificação de crédito | 12 páginas ainda dizem `EMPIRICAL-CREDIT=0` e `RESULT=UNTESTED` | CRÉDITO REGISTRADO 0/12 |
| Pass científico da onda | Não concedível com duplicação e FRPE indeterminado | NOT-PASS / ANALYSIS-RECONCILED |

**Atenção:** o `COUNT=2` foi instalado como retrofit às 18h de 07/10. Ele não equivale a duas ativações no total histórico da onda, e `is_enabled=false` não prova sozinho que cada encerramento decorreu exatamente de consumir COUNT.

## 5. Identidade das cinco tarefas (NO-REARM)

| Tarefa | Task ID final | Configuração de última leitura |
|---|---|---|
| S1 | `6ac65ff19974819193f37c275c67a0fe` | `COUNT=2`, off, shared queue / affinities C01/C06/C11 |
| S2 | `6ac65ffbeb58819199c64f9bd98f4bf0` | `COUNT=2`, off, shared queue / affinities C02/C07/C12 |
| S3 | `6ac66007c0d88191b4780b5d853a2201` | `COUNT=2`, off, shared queue / affinities C03/C08 |
| S4 | `6ac660102e4481918b6460062dcaadcd` | `COUNT=2`, off, short/direct C04 |
| S5 | `6ac66017f56c8191aecc2e3985796a02` | `COUNT=2`, off, shared queue / affinities C05/C10 |

**Supervisoras consultivas:** SCI Reflex Supervisor — P0 Delta registrou firing posterior, mas entrega consultiva correspondente não foi identificada como relatório novo naquele primeiro audit. SCI Supervisor Canary One-Shot leu C10 e o registro `SCI-SUP-CANARY-E2E-20261008` está presente no REFLEX-LAB (reabertura posterior confirma presença), sem atribuição do M1 à supervisora. Essas tasks NÃO fazem parte da taxa FRPE de S1–S5.

## 6. Lacunas e disposição

1. **LAC-01 — Run history completo S1–S5:** as fontes acessíveis expõem somente o último firing por task no cadastro atual e snapshots históricos isolados; sem listagem confiável de todos os runs, chamadas de ferramenta, falhas por execução, RUN-ID nem destino tentado. `STATUS=UNAVAILABLE-IN-ACCESSIBLE-SOURCES`, não declarar impossível em toda a plataforma.
2. **LAC-02 — Primeira exposição elegível por canário:** não há ledger completo pré/fim por RUN-ID; C01/C03 são candidatos a recovery tardio; não marcar FRPE=FAIL sem prova da primeira exposição.
3. **LAC-03 — Autor de cada M1:** proximidade cronológica e afinidade são evidência circunstancial, não rastreio técnico.
4. **LAC-04 — Origem da segunda linha C05:** falha de idempotência confirmada, parser/pipe e corrida concorrente ainda hipóteses.
5. **LAC-05 — Semântica dos NO-OP:** S2 14:14 documenta ausência de ganho no snapshot, mas não distingue no-op válido, ferramenta indisponível, timeout ou falha de resolução.
6. **LAC-06 — Verifier/PASS:** campos canônicos permanecem UNTESTED/credit 0; sem crédito independente nem denominação FRPE segura.
7. **LAC-07 — Encerramento individual COUNT:** tasks estão off; histórico individual da causa de desativação não consta dos metadados acessíveis.
8. **LAC-08 — Registro final canônico:** esta execução possui leitura, mas a permissão de `notion_update_page` não foi disponibilizada pela integração; gravar/fechar no Notion permanece PENDING-WRITE. Não tratar este arquivo como fonte canônica superior ao Notion.

**Condições de reabertura:** obter logs do provider com RUN-ID e worker/toolcalls, se a plataforma passar a disponibilizá-los; recuperar e preservar links/evidências, não repetir a onda para forçar percentuais. Próximo experimental somente após gates próprios, normalização/claim-fence e autorização expressa.

## 7. Handoff Vivo / NAC

- `OPERATION=CM-000005-WS0001 / PLAN75-P0-FRESH-12-POSTWAVE`
- `DENOMINATOR-OBSERVED-LAST_RUN=16`, `RECONCILED=16/16` (universo de snapshots visíveis, **não total real**)
- `DENOMINATOR-TARGETS=12`, `REOPENED=12/12`, `MATERIAL-PRESENT=12/12`, `RAW-M1-LINES=13`
- `DUPLICATE=C05 x2`, `FIRST-PENDING=AUTHORITATIVE-RUN-HISTORY-OR-CLOSURE-REPORT-WRITE`
- `FRPE=NOT-DETERMINABLE`, `SCIENTIFIC-PASS=NOT-GRANTED`, `PLAN-75-GLOBAL=NOT-CLOSED`
- `WRITER=NONE-CLAIMED-BY-THIS-REPORT`, `INSTANCE-ID=NOT-CLAIMED`, `LEASE=NONE-INHERITED`, `BLOCK-PERMIT=RED-EXPERIMENT`
- `UNKNOWN-EFFECT=FIRING-LEVEL-ATTRIBUTION-AND-FAILURE-CAUSES`, `NO-REPEAT=S1-S5-NO-REARM; PRESERVE-C05; DO-NOT-MANUALLY-CREATE-C10`
- `NAC-PASS / SCIENCE=HOLD` (duplicate + métricas causalmente inconclusivas + registro oficial pendente); `NAC-PASS / DOCUMENT=NOT-EXECUTED` (sem escrita canônica autorizada nesta sessão)
- `NEXT`: se Notion escrita autorizada for restaurada, REGISTRAR ANTES → verificar claim documental/Inbox e ausência de collision → anexar este dossiê a Diário existente/PLAN com fonte primária e referência secundária sem duplicar → reabrir e verificar → REGISTRAR DEPOIS → NAC-PASS documental estrito. Não editar targets nem atribuir crédito.

**Fontes adicionais de governança:** [NAC-AUTO-CONT-01 v1.12](https://app.notion.com/p/3f1c2b324ede81b48526f059e6184c49) · [RISK-SCI-CLOSURE-01](https://app.notion.com/p/3f2c2b324ede81bc8a58de7578653453) · [PLAN-75](https://app.notion.com/p/3f2c2b324ede810ea992f49e3c606544) · [Diário](https://app.notion.com/p/3f1c2b324ede81e5a480ef85fb003b8e).

**Declaração de integridade:** este relatório preserva os dados disponíveis e os desconhecidos. Não alega execução em background, não declara queda do Cientista anterior sem logs, não converte cobertura eventual em confiabilidade nem simulação em experimento real.
