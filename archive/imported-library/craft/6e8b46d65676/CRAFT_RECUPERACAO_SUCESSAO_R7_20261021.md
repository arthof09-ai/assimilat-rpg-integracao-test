# CRAFT — Auditoria de sucessão e correção técnica R7

**Projeto:** RPG Assimilação · **lado:** MESTRE-SIDE · **data-base:** 21/10/2026 (America/Recife) · **operação única:** OP-ARQ-RIN-REC-01 · **workstream de referência histórica:** CM-000002 / WS0001.

**TRACE deste trabalho:** CRAFT-SUCCESSION-AUD-R7-20261021-001. **Resultado:** continuidade técnica assumida em TEST, sem reivindicar INSTANCE-ID, lease, writer, epoch, ACK, fencing nem GREEN. Não houve alteração material nas fichas, Party, O Primeiro, estoque, receitas oficiais, PA ou R48. Este relatório é entregável de sucessão, não NAC-PASS de produção.

## 1. Fontes vivas consultadas — não confundir com memória de chat

- [LAB CRAFT — Produção e Validação Experimental](https://app.notion.com/p/3fbc2b324ede811db848d35d4739eb00): registro técnico, última frente encontrada **R53** (marco no LAB), e consolidação R1–R6 acrescentada enquanto ocorria a recuperação; revalidar novamente em retomadas futuras.
- [OP-ARQ-RIN-REC-01](https://app.notion.com/p/3f1c2b324ede81d7aa79c83106240516): diário da operação original e histórico dos gates.
- [IBX-116](https://app.notion.com/p/3ffc2b324ede817aa3abea3cb7ba8c08): comunicação existente, status NOVA, ACK exigido; não inferir leitura ou aprovação.
- [IBX-38](https://app.notion.com/p/3f3c2b324ede817fb888ca32aacaf2de): fencing técnico de I0014 não comprovado, C19-021 UNKNOWN-EFFECT, F5 P0 RED.
- [R51 — destino REC-LIB](https://app.notion.com/p/3f4c2b324ede812a9153d39281b488f8): parent físico único da biblioteca de receitas ainda não certificado, não autoriza pasta paralela.
- [Kit Comestre — BOOTSTRAP, NAC-CONT-03 e errata PA](https://app.notion.com/p/3edc2b324ede81d0b25ec2f3be128db6); [remap de 30 fichas F5](https://app.notion.com/p/3f3c2b324ede81c99367e2de46077cbb).
- Biblioteca pessoal `/Comestre/`: `REGISTRO_CONSOLIDADO_CRAFT_R1_R6_20261021.md`, `PSV_CRAFT_R6_REVIEW_CUSTODY_20261021.md`, ZIP da custódia R6, ZIP Android/R46 R6, ZIP R53, ZIP R5. Materialização de seis arquivos recuperada na sessão, hashes originais conferidos.

**Classes de evidência:** VERIFICADO nesta sessão (bytes, manifestos, reexecuções locais); VERIFICADO NOS REGISTROS HISTÓRICOS (atos antigos cuja execução não foi integralmente refeita); PROPOSTO (projeto de item/experimento); PENDENTE/HOLD (falta autoridade, amostra ou efeito). Arquivos sintéticos jamais equivalem a observação física.

## 2. O que o CRAFT fez antes de cair

| Frente | Evidência recuperada | Limite |
|---|---|---|
| F5/BACKFILL-30 | 30 fichas PS R01 20 + R02 10 identificadas; meta documental 30/30 recursos cobertos por ≥30 REC-ID RC5 distintos | Checkpoints relatam 0 novas RC5 oficiais; censo total atual depende de readback; F5 RED |
| R44–R50 e fábrica R48 | Fábrica TEST de Tábua Lamelar/Mica recuperada; extensão Pingente Vigília Boreal com ordem estrutural nativa TEST 0→1, diário e idempotência | Nenhuma transferência ou retenção mágica testemunhada, nenhum produto/estoque real |
| Integração PA R26/R27/R39 | Fornecedor correto (errata Mestre) e cálculo prospectivo de Pingente 12 PA/dia + 2×7 PA/ativação = 26 PA TEST | Orçamento não prova efeito real; não retroagir custos históricos |
| H1/H2, receitas de encantamento | Testes de mecanismo H1, preparação H2-3A/B e controle de variantes Mestre versus Espelho | Sal, energização, Óleo de Vedação, lote e testemunha bloqueiam aplicação |
| B30-06 Bolsa Secante | Montagem sintética, RH em pares e correção de pseudorreplicação | Adsorção/materialidade não demonstradas |
| B30-13 Substrato | Auditoria detectou 750mL de húmus + areia condicional versus meta 1L, com simuladores de volume/controle | Sem balanço medido, pH ou germinação reais |
| Corpus de receitas | 34 entradas lidas, 29 receitas em subpáginas e 5 embutidas; dry-run R51; 21/29 divergências de texto/etapa | Nenhum parent físico movido, sem homogeneizar variantes por suposição |
| R4→R5 Android | Interface offline e revisor: v1.0, v1.1 Cordão, v1.2 incerteza e revisão JSON | Chromium mobile não comprova abertura específica no Android físico do Mestre |
| R6 Android/R46 | v1.3 exporta pré-dossiê NÃO NATIVO; 35/35 testes R6, regressões 63/63 + 26/26 R5, 2.000 vetores, 2 E2E Chromium | Falta operador, amostra, calibração, custódia e 4 anexos R46 reais |
| R6-custódia separado | ZIP 12.440 bytes; wrapper `review_capture.js` protegido contra sobrescrita; 12/12 novos testes | Até esta recuperação, patch não integrado ao outro ZIP R6/R46 |
| R53 — último marco LAB técnico localizado | Dois projetos MESTRE/TEST: Sonda de Eco Estático do Vale dos Raios e Tônico Experimental de Passo Elétrico; 99/99 testes digitais, 8 nós e 6 dependências | Ambos `HOLD_TEST_DESIGN`, sem item/fórmula/estoque oficial; teste Android apenas smoke JS |

**Sobre datas:** as seções do LAB e arquivos da Biblioteca podem ser atualizados por outras instâncias. R53 é o último marco técnico de projeto encontrado no LAB; o consolidado e o pacote de custódia R6 são mais recentes no fluxo de documentação da Biblioteca e não contradizem essa descrição.

## 3. Trabalho NOVO desta sucessão — CRAFT R7 CUSTÓDIA INTEGRADA

### Antes

Ao extrair o ZIP **CRAFT_R6_ANDROID_R46_PREDOSSIER_20261021.zip**, SHA256 `a3d28127fee7a4fae43be7b9356832318e359e5ccb560e394324f732f247698f`, foi identificado que **dois wrappers Node** (`review_capture.js` e `r46_predossier_cli.js`) ainda chamavam escrita direta sem exclusividade. Uma saída igual à entrada podia truncar o JSON de origem. Existia pacote de correção R6 separado para `review_capture.js`, mas ele não protegia o CLI de pré-dossiê R46 nem estava incorporado à mesma lib R46.

### Mudança executada

1. Reutilizado sem alterar um byte o patch R6 de custódia de `review_capture.js`, com `writeFileSync` exclusivo (`flag:wx`, modo `0600`).
2. Corrigido `r46_predossier_cli.js` do ramo R6/R46 para recusar caminho igual/normalizado e qualquer destino já existente, sem sobrescrever origem, symlink/hardlink, diretório ou recibo anterior.
3. Adaptado `run_replay_r6.py` para produzir a saída CLI R46 em diretório temporário; não escreve sobre fixture já existente.
4. Acrescentados `test_custody.py` (12 casos pré-existentes da correção separada) e `test_r46_custody.py` (10 casos novos específicos da segunda vulnerabilidade).
5. Preservados integralmente `logic.js` SHA `a346889dd1cc59826d7d0ce24a16a9444d7587d316f63eccd1034dfc8be6e484`, HTML v1.3 R46 SHA `6607aa235196629f5cee6242458787ef2ee4a2056db22cbb3b04f24e4624420c`, transformação R46, e ZIP R5 histórico SHA `29b4bfb61a726bd4e12bffa8e245552831003ca5f3e1b7e4f5edcbd7f65eb6e8`.

### Testes realmente reexecutados nesta recuperação

- 12/12 testes R6 de custódia (`review_capture.js`) **PASS**.
- 10/10 testes novos R7 de custódia (`r46_predossier_cli.js`) **PASS**.
- R5 QA 63/63 + revisor 26/26 **PASS**; R6 pré-dossiê 35/35 **PASS**. São 124 testes de regressão R5/R6 distintos por suíte, não 124 ensaios de laboratório físico.
- 2.000 vetores de fronteira sintéticos **PASS**, não contados como testes de laboratório independentes.
- Dois scripts E2E Chromium mobile (resolução 390×844) **PASS**; comparador navegador/CLI R46 **PASS**.
- ZIP R7 final: **24 entradas = 23 arquivos com SHA + manifesto**, CRC íntegro, baseline R5 pinado e QA byte-idêntico; verificador original R6 **PASS**.
- Extração em diretório limpo, execução novamente de ambas as suítes de custódia e de replay R6 **PASS**; o ZIP final manteve SHA inalterado.
- Independente: ZIP R53 original reextraído e `src/run.js` + cinco suítes executadas **99/99 PASS**, dois projetos retornaram `HOLD_TEST_DESIGN`.

**Incidente de empacotamento fechado:** o primeiro ZIP local continha cinco outputs transitórios criados pelo navegador/test runner que não estavam no manifesto e falhou corretamente na verificação. Os cinco outputs não manifestados foram retirados, o arquivo ZIP foi reempacotado, e o **pacote final** passou CRC/manifesto e replay frio. Não usar o hash da versão provisória.

**Artefato final R7:** `CRAFT_R7_CUSTODIA_INTEGRADA_VERIFIED_20261021.zip`, SHA256 `9655154c60a9376ddaf4f39d912c2b4ef5069cb59e86e076e55db51212296dc7`, **402.885 bytes**. O nome VERiFIED identifica apenas o pacote digital; não sugere homologação de item RPG.

### Gate proporcional

**PASS restrito:** código e testes TEST, integridade, reprodutibilidade, não sobrescrita nos casos auditados, leitura das normas e prevenção de autocanonização.

**HOLD preservado:** autenticação externa, proteção contra concorrência entre processos arbitrários, execução no Android físico do Mestre, custódia real de lotes e medições, prova mágica, ensaio R46 nativo, F5/C19/IBX-38, R51, P2 e RC5. Nenhuma alteração da operação oficial é declarada sem leitura pós-escrita.

## 4. Pendências — primeiro bloqueio e progressão segura

| Ordem | Pendência concreta | Ação exata necessária e autoridade |
|---|---|---|
| 1 — P0 | IBX-38: fencing real I0014, C19-021 UNKNOWN | Ato externo verificável do operador/sessão ou STOP-ACK/RELEASE da instância antiga; auditoria do in-flight + delta C19, claim/epoch/lease/fence e canário. Não chamar revogação documental de fencing técnico. |
| 2 — P0 | R51 destino físico REC-LIB único | Identificar parent autoritativo existente e reconciliar 29 subpáginas + 5 embutidas, sem novo parent especulativo e sem mover até gate de escrita. |
| 3 — P0 | F5/BACKFILL-30 | Revisão 30/30 PS; meta ≥30 REC-ID RC5 legítimos somente após gate físico/autoridade e readback. Nenhuma receita por quota. |
| 4 — P1 | P2 SALT e ENERGY | Mestre/autor competente fixar Sal Geodo Santo versus Encantado, etapa/quantidade da energia (Pedra da Luz OU Pote). Não simular decisão canônica. |
| 5 — P1 | Óleo de Vedação (28/29 receitas o citam) | Comparar as variantes dos pós e essências, origem, lote, quantidade, processo, operador, custo; não confundir peça com pó ou “existe no Notion” com estoque. |
| 6 — P1 | H2-3A/B / Pingente | Após insumos e decisão legítimos, observar aplicação/energização/retensão sob módulo ENC/EQA e auditoria; caso contrário manter HOLD. |
| 7 — P1 | R45/R46 medição material B30-01/03/02 | Operador, instrumento serial/calibração, data e fuso, amostras e lotes, 4 anexos primários/custódia, revisor independente, sem substituir por JSON sintético. |
| 8 — P2 | B30-06, B30-13, 21/29 divergências, Matriz Cultivo UUID e Proteção `Ex` | Teste comparador independente e readback de fontes; não “consertar” sem autoridade sobre o corpus. |
| 9 — P2 | Protótipos R53 | Buscar suportes/veículos e compatibilidade de materiais em fontes existentes; registrar custo MED/CTE como variável, não preço definido; nenhuma promoção P4. |

## 5. Ponto exato de retomada para outro chat

`OP=OP-ARQ-RIN-REC-01 | LAB=3fbc2b32-4ede-811d-b848-d35d4739eb00 | LAST VERIFIED UNIT=R7 CUSTÓDIA CLIs TEST SHA 9655154c... + R53 99/99 cold PASS | FIRST PENDING=verificação de persistência do R7 na Library/Notion; se ambos confirmados, revisar gate IBX38/R51; se continuarem HOLD, prosseguir engenharia TEST útil sem novos motores | F5=RED | C19-021=UNKNOWN | AUTHORITY=NO WRITER/LEASE/ACK/FENCE | Party/O Primeiro=NO-WRITE`.

**NÃO REPETIR:** fábrica R48, PA R26/R27, tentativas mágicas já recusadas, triagem B30-01/03/06, 34 páginas do corpus, auditorias R51, módulo R45/R46, UI Android R4–R6 ou os dois protótipos R53. A nova proteção R7 não prova que um objeto RC5 pode ser criado.
