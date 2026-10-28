# PSV — CM-000001 / Instância B — Auditoria CRAFT FAST-CLOSE 03

**AS-OF:** 16/10/2026 · **SIDE:** MESTRE-ONLY  
**OPERATION:** CM-000002 / CM-000002-WS0001 / OP-ARQ-RIN-REC-01 (existente)  
**NATUREZA:** auditoria independente limitada de evidências documentais e recibos publicados; não houve takeover, writer, claim, escritura Notion ou reexecução de código CRAFT.

## Evidência de fontes realmente reabertas

- Notion [Laboratório CRAFT](https://app.notion.com/p/3fbc2b324ede811db848d35d4739eb00), editado em 2026-10-16T13:36:45Z: ordem autônoma pós-FAST-CLOSE 02. NÃO contém nova persistência FC03 no corpo consultado.
- Notion [OP-ARQ-RIN-REC-01](https://app.notion.com/p/3f1c2b324ede81d7aa79c83106240516), perfil [CM-000002](https://app.notion.com/p/3f1c2b324ede81f68127e432303c74b2), [Runtime](https://app.notion.com/p/3f1c2b324ede811c8a42e1416b5c7774) e [IBX-38](https://app.notion.com/p/3f3c2b324ede817fb888ca32aacaf2de): CRAFT/F5 P0/RED, C19-021 UNKNOWN-EFFECT, fencing e writer material não demonstrados.
- Notion [AUD-CRAFT-F5-REMAP-01](https://app.notion.com/p/3f3c2b324ede81c99367e2de46077cbb), receita B30-22 PRE-Q2, [Quitina de Exoesqueleto](https://app.notion.com/p/3f3c2b324ede8141acddf0bb23ffe56c) e [Fibra Boreal](https://app.notion.com/p/3f3c2b324ede815ab04ace5bd1074e79): fontes PS com dimensões/estoque/propriedades reais não verificados. B30-22 PRE-Q2 é uma especificação, não RC5.
- Biblioteca /Comestre: `CRAFT-FAST-CLOSE-03-DELTA-20261016.zip` presente em metadados, 109.623 bytes, Library ID `libfile_e2a105bd5d4881919d86181dd7f1da8f`; `CRAFT-COMESTRE-CHAT-v03(3).zip` e `(4).zip` presentes, 43.805.607 bytes cada. O acesso aos bytes ZIP via materialização falhou com `not authorized raw-byte materialization path`; **CRC, SHA do ZIP, 205/205 manifestados e 331 testes não puderam ser reexecutados por esta Instância B**.
- Biblioteca: arquivos individuais `r48_fresh_execution.json`, `b30_22_experiment_receipts.json`, `triage_B30_03_B30_06.json`, `independent_readback_audit.json` lidos integralmente. Foram aplicadas **27 verificações lógicas independentes e reproduzíveis sobre esses JSONs, 27/27 PASS**; isso NÃO é reexecução dos 331 testes do Executor nem recálculo criptográfico dos ledgers.

## Classificação da entrega

**VERIFICADO DOCUMENTAL:** quatro JSONs acessíveis; IDs das fontes PS correspondem às páginas Notion; o consumo B30-22 relatado concilia 2 placas de quitina + 30 cm de fibra com estoque inicial/final; um produto TEST sintético com ID `SBX-CRAFT-R44-I0016-PRODUCT-SBX-FC03-CASE-0001`; sem REC-ID oficial. QA negativa em store separado rejeita produto, registra sucata sintética e consome insumos após processo; precheck sem estoque rejeita sem consumo/produto. Replay do sucesso preserva saldo; o HEAD do sucesso `bf8cb8ee89d9b52fa4358c35477492551c4b49876acba4a1a4c7941c5bf0ecee` é distinto do HEAD final da mesma store após rejeição sem estoque `051bc39557ce3517bd2acf625952fa4cca62637722e61053a757089189ca8601`, sem contradição.

**VERIFICADO DOCUMENTAL — R48:** os recibos descrevem dois produtos TEST B30-01/B30-03, estoque reconciliado, precheck de terceira tentativa sem efeito, replay idempotente, sequência final 2 e HEAD `a3087ef2b4bf091e669ae707af9c018722331cb91a80785c6ed88802a1d526ac`.

**RELATADO / NÃO REEXECUTADO INDEPENDENTEMENTE:** 205/205 hashes v03, 174 arquivos R48 idênticos à Oficina v02, 40/40 testes R48, 273+40+18=331 testes, ZIP 37 entradas com manifesto 36/36, 36 hashes. Independent_readback_audit.json é um relatório do próprio pacote, não prova de execução independente pelo Coordenador.

**HOLD CIENTÍFICO:** 20 ciclos da dobradiça e 110 graus são valores da fixture `qa_fixture`, não medição física; nenhum teste comparativo real contra estojo comum; preços, MED, capacidade, propriedade mecânica, rendimento e conhecimento técnico estão ausentes. Fonte Fibra: unidade real e árvore-fonte pendentes; fonte Quitina: medidas reais, produção e estoque pendentes. A B30-22 funcionou como transformação por motor histórico R44, mas `r48_extension_scope` informa `R44_ONE_RECIPE_ADDITIVE_WITH_R47_DURABLE_PRIMITIVES; R47_AUTHENTICITY_NOT_EXTENDED`: **integração B30-22 na fábrica R48 completa e autenticação R47 não foram demonstradas**.

**GOVERNANÇA:** RC5 oficiais 0/30, REC-IDs físicos novos 0/30, produto oficial 0. F5/REC-LIB permanece RED. Nenhuma escrita em Notion feita por esta auditoria; inexistem registro ANTES/DEPOIS e readback FC03 nesta passagem.

## Fronteira e próximos cinco atos

- **BASELINE:** R44/R47/R48 existentes; FAST-CLOSE 02; ordem 10 etapas do LAB.
- **LAST-VERIFIED-UNIT:** quatro JSONs integralmente lidos; 27/27 invariantes documentais conferidas; Notion e fontes PS reabertas.
- **FIRST-PENDING:** auditoria de bytes do ZIP delta/v03 e reexecução fria da suíte; técnica: ligação B30-22 ao R48 + R47, com controles atuais de validade.
- **DENOMINATORS:** 27/27 invariantes de recibos PASS; testes do Executor 331/331 RELATADOS, não reexecutados; integrados R48 de B30-22 0/1 comprovados; RC5 0/30; produto físico real 0.
- **NO-REPEAT:** não reconstruir R44–R48; não repetir B30-01/03 por rotina; preservar draft `SBX-R48-BATCH-UI-2afb696406a6e839`; não reutilizar IDs de fixtures/estoque nem alegar evidências retroativas de R47.
- **CONFLICTS:** o executor encerrou o produto B30-22 no R44, não no R48 multiordem pedido; é avanço parcial, não implementação integral. HEAD do sucesso difere do HEAD final após rejeição, por sequência de eventos distinta.
- **UNKNOWN-EFFECT:** histórico `C19-021` persiste; não abrir retry produtivo. Materialização do ZIP falhou somente como acesso nesta auditoria, sem efeito de escrita.
- **AUTHORITY/WRITER:** CM-000001 Instância B, somente leitura/análise; sem writer CRAFT/F5, sem lease, sem reserva, sem alteração de registro compartilhado.
- **NEXT-5:** (1) recuperar bytes v03/delta via canal autorizado e conferir ZIP/manifesto; (2) executar 331 testes em extração limpa, incluindo relógio de validade R47; (3) integrar B30-22 na transação multiordem R48 e autenticação R47 TEST; (4) comparar causalmente função QA de estojo contra caixa comum com controles e manter medição física como PENDENTE até realmente executada; (5) persistir evidências na OP/Diário existente via writer competente, reabrir e enviar comunicação bilateral deduplicada.
- **TARGET-REMAINDER:** demonstrar R48+R47 completo para B30-22 em sandbox, qualificar mérito/insumos/economia, tratar fencing sem confundir com produção.
- **HANDOFF:** RETOMAR exatamente pelo delta FC03 preservado, sem novo motor nem nova operação.

**NAC-PASS-02 proporcional:** APROVADO COM RESSALVAS para auditoria read-only e consistência dos JSONs. HOLD para autenticação ZIP, reexecução de 331 testes, escrita de checkpoint FC03 no Notion, reconhecimento do Executor, gates RC5 e produção.
