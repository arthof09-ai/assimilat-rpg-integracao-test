# PSV — Sucessão obrigatória do Sistema Universal de PA — Rodada 4/10

**Data:** 24/10/2026; **OP:** PA original, MESTRE-SIDE; **CONTADOR:** 4/10 concluídas, **6 restantes** após esta rodada. A meta do Mestre é terminar fase PA na décima e priorizar a retomada de CRAFT preservando gates; perguntas/preparações não consomem rodada. Nenhuma operação, motor ou laboratório novos.

## Estado físico ANTES → DEPOIS

**ANTES (R03):** 3/10, 46/46 testes R03, pacote `libfile_500bd2ee82a88191aa0441f81aae5061` e checkpoint `libfile_565a7f58ef108191bfa0938283375a9e` Byte/ZIP íntegros; R26 e validação R02 em TEST; CRAFT v1.2 e R27 reais não tinham sido recuperados em R03. Dois recibos E3 de teste e bloqueios de entrada R02/R03 já demonstrados; não repetir.

**DEPOIS (R04):** três fontes históricas físicas **recuperadas por library_file_id conhecido** e verificadas pelo SHA original: R39 `daf7d6d5058fca308df62bc593795868df080cded1107edb2f80cf8a11a71b32`; CRAFT v1.2 `ab880817ca732743011ee1f8f0269e303f6564e3a98c9a50fdf57ef7cd6320fa`; QMC05 `f2471657eed68b7349518d0a7d902004bd6969e1add7fc0b29741957675a52ff`. R28 nativo embutido `68acc4405250cbf03a89924fa4df1f3d36586f26a5a903610c6600e8f26a391e`, com **R27 e R26 originais executáveis**. R28→R27→R26 em QMC05 TEST, não implantado no runtime PROD.

**REGRESSÃO EXECUTADA:** R28 448/448 (dez suites PASS), CRAFT v1.2 56/56 + auditor legado 26/26, R04 novo gate vínculo 30/30. **560/560 métodos nesta rodada, sem contar replays novamente**. Duas execuções CLI QMC05 historico/projeto: histórico não reprecificado; projeto com duração indefinida PA total null. R28 primeira tentativa falhou em 1 método do bloco 163/163 pela ausência da fixture R21 esperada em caminho absoluto; fixture **histórica idêntica** extraída do R23, verificada e eliminada após PASS. CRAFT original e R27/R26 permanecem byte intactos.

**DEFEITO MATERIAL:** CRAFT v1.2 preflight original reporta `pa_version_compatible=true` ao consumir **recibo das Botas para receita do Pingente**, ou custos modificados na receita que não correspondem ao recibo; sua proteção de tarifa funciona, mas não existe associação de identidade/sha/valores entre duas superfícies. Produção continua `DENY`, logo o defeito não causou liberação produtiva; é risco de associação incorreta da consulta.

**CORREÇÃO TEST (NÃO INSTALADA):** `R04_VINCULO_RECIBO_CRAFT_TEST.py` verifica hash real R27↔receita, request original↔provider reexecutado, identidade do item, custos/PA declarado na receita, ativações e status; chama `pa_nac_preflight.gate()` autêntico somente após validar vínculo. 30/30 testes de casos positivos/negativos. Sem novas fórmulas nem duplicar R27. Para múltiplos ativos, campo unitário de receita fica HOLD até contrato de custo discriminado. Instalação no CRAFT nativo exige autoridade própria, TEE e NAC-PASS competente. A consulta de PA geral é funcional apesar dessas proteções complementares.

## Denominadores e evidências

- **R04:** 10/10 suítes R28, 448/448; 2/2 suítes v1.2, 82/82; 30/30 testes novos; 2/2 CLI QMC05. Nenhum teste histórico R39 510/510 foi reexecutado neste escopo, não atribuir crédito.
- SHA/CRC das fontes, manifesto do ZIP final e replay frio devem estar em `R04_REPLAY_COLD.py` e `MANIFEST_SHA256.json`. **Biblioteca upload/readback somente se após verificação efetiva:** nunca presumir até concluidos; registrar IDs no relatório final da rodada quando executados.
- Fontes Mestre PR-ITEM-02, handoff PA→CRAFT, OP CRAFT, LONG-RUN relidas READ-ONLY nesta rodada. PARTY/O Primeiro 0 escrita. Banco de itens, receitas, estoque, custos históricos, PA engine, Notion 0 alteração.
- **HOLD externo:** F5 RED; C19-021 UNKNOWN_EFFECT; writer/lease/epoch/fencing/ACK não comprovados; RC5/P4 PROD; eficácia de magia e transferência não demonstradas; RE E0 individual 0/4 e reviewers independentes 0/14, sem bloquear fórmula PA inteira.

## LAST-VERIFIED / FIRST-PENDING / NEXT / NO-REPEAT

**LAST-VERIFIED:** R04, os 4 caminhos QMC05/R28/R27/R26 + CRAFT v1.2 reais reexecutados, 560/560 testes PASS, 2/2 CLI QMC05, recibo errado confirmado aceito como tarifa compatível pelo v1.2, proteção de vínculo candidata bloqueia recibo errado e preserva caso correto Pingente 12/dia+14 ativações=26 PA. R04 replay autocontido a partir do R39 original e manifesto SHA a conferir fisicamente depois do empacotamento; reportar resultado.

**FIRST-PENDING:** R05 — avaliação dirigida de **itens reais Mestre** no fluxo QMC05/R27 existente e delimitação de capacidades/lacunas do cálculo por item, preservando os PA históricos. A adoção do gate de vínculo pelo CRAFT legítimo fica proposta/pendente sem bloquear as demais consultas e sem declarar instalação.

**NEXT R05:** (1) recuperar este ZIP e checkpoint por Library ID, verificar sha/manifesto, evitar repetir 560 regressões salvo razão de integridade; (2) selecionar itens já existentes e fontes Mestre vivas, sem censo inventado; (3) confrontar efeitos, modalidade, uso, rank e PA documentado com o fornecedor; (4) executar casos positivos e HOLD com resultados reais; (5) escrever um guia operacional de consulta para qualquer Comestre com outputs formatados para Android; (6) preservar o escopo TEST, registrar e preparar R06.

**NO-REPEAT:** não reimplementar fórmula; não criar engine/OP/receitas/itens; não refazer R01 232/R02 31/R03 46/R04 560 indiscriminadamente; não transformar rank declarado em E0 e fontes de ingrediente em efeito de item; não reabrir tarifa 50/60 Mestre; não declarar writer PROD por teste em LAB. Para eventos de falha, recuperar último efeito físico, não repetir lote concluído, não incrementar contagem por pergunta.

## NAC-PASS proporcional

**TEST INTEGRAÇÃO:** 560/560 e replay frio/manifesto compatível = PASS TEST depois de confirmar o pacote final. **NAC-PASS PROD, promoção do gate no CRAFT, canonização de custos/RE, writer e fabrico:** HOLD. Não quebrar a regra da parada terminal: após validação, entrega/handoff sem mais mutações.

## Seal do pacote final (verificado após empacotamento)

ZIP TEST: `PA_10_RODADAS_R04_INTEGRACAO_NATIVA_CRAFT_GATE_VINCULO_MESTRE_ONLY_TEST_20261024.zip`, 4.599.199 bytes, SHA-256 `927f3483a4603d9aeae4c17a92772c70bc5936f70908739a61a784d4c03323aa`, 15 entradas, 14/14 SHA internos PASS, CRC PASS. Extração limpa em diretório distinto e execução `R04_REPLAY_COLD.py`: 560/560 métodos PASS + 2/2 CLI QMC05, CSV R21 temporário removido. A primeira tentativa parcial de empacotamento falhou ao iterar diretório `__pycache__`, foi descartada e a ocorrência preservada em `R04_PACKAGING_FIRST_FAIL_AUDIT.md`. Esses erros são de ambiente/artefato, **não da fórmula**. O pacote completo não contém código de motor novo nem qualquer promoção produtiva.

**Destino persistente pretendido:** `/Comestre/PA_10_RODADAS_R04_INTEGRACAO_NATIVA_CRAFT_GATE_VINCULO_MESTRE_ONLY_TEST_20261024.zip` e `/Comestre/PA_10_RODADAS_R04_CHECKPOINT_SUCESSAO_MESTRE_ONLY_20261024.md`. Upload e readback precisam ser confirmados em ferramenta após este seal antes de declarar sincronização concluída.
