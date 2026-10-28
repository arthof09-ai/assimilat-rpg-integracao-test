# VLAB — PSV / Estado corrente após R296 (MESTRE-ONLY)

**Operação existente:** `OP-VLAB-FUSION-SANDBOX-01`. **Comestre lógico:** `CM-000006`, identidade/fencing do writer NÃO provados. **Base:** LAST VERIFIED R295 / R296 TEST. **Próxima unidade:** R297 apenas candidata após collision preflight.

## Antes e depois — R296

ANTES: overlay funcional R289–R295 preservado (SHA256 `7c9ac7b1930bf673d745e65140e5a2fd3e5b6ce422e03558a6eb31f4c79d42ec`), 65 testes (47 históricos +18 novos) PASS em cópia limpa, 4 cenas 36 decisões/24 ataques/8 curas/8 defesas; a gênese de um combate R20/R21 em revisão zero permitia alterar por fora do journal valores de PA, consumo de Reação, rodada ou vencedor sem recusa. O HP já era recusado por auditor R292.

R296 TEST: reproduziu fisicamente 4 aceitações indevidas pré-primeiro-evento (PA, Reação, rodada, vencedor) e implementou verificação estrita da criação do roster completo e estado da fase INIT em `fusion_stage12/vlab_r20_configured.py` de **cópia TEST**; 8/8 testes novos PASS para origem legítima, Vida, PA, reação, rodada, vencedor, terceiro ator e imutabilidade do hash inicial. Nenhum motor duplicado, sem edição dos originais R18–R22.

## Testes reais

- **73/73 PASS:** 47 regressões históricas R18–R22 + 12 testes R289/R290 + 6 fronteiras JSON R294 + 8 novos R296; processo `FULL_EXIT:0`, arquivo incluído no ZIP `evidence/R296_FULL_73_TESTS_PASS.log`, duração medida 121.337 s. ResourceWarnings sobre algumas conexões de testes antigos não foram corrigidos ou escondidos; nenhum teste FAIL.
- **Cold install FAST:** partiu do R22 original SHA256 `04ddf83ba2df69059a9f00f0f46e3bee24e9adbd59094400bf3671fd72942ca6`, aplicou R289–R295 + R296 em árvore temporária; 8 novos + 18 anteriores PASS, `R296_FINAL_COLD_REPLAY.json` produzido.
- **Cold install DEEP:** mesma reconstrução com as 47 regressões históricas adicionais; `DEEP_EXIT:0`, `PASS_R296_COLD_TEST_ONLY` e 47 testes herdados no relatório `R296_COLD_DEEP_OUTPUT.json`. Os relatórios da execução profunda estão preservados em ambiente TEST, não em Notion.
- Auditor de fonte R292 limita-se à cura sintética (1d6 e 0PA), não é homologação da v0.8.1 por inferência.

## Fonte, integridade, gates

Original R22 15.403.014 bytes; SHA acima. Módulo `vlab_r20_configured.py` ANTES SHA256 `87514d23181f9228b3f0f4dc6cbb717392d8e3cc490c7d4afaa8991f3237e309`; DEPOIS SHA256 `00e41827fe3fd5b921e479b51594bc3db620484268b60eac96e4b0009b552311`. Delta R296 contém patch source completo, testes, reprodução pré/pós, logs 73 testes, manifestos, verificador CRC/SHA e instalador frio `COLD_REPLAY_R296.py` (requer origem R22 e overlay R295 intactos). Não inclui segundo motor de 15MB.

**Administração:** Notion profile CM-000006 continua `PAUSED / FIRST-INSTANCE-PENDING`, writer/lease/epoch/fencing/ACL/GREEN HOLD. Inbox CM-000006 verificada nesta execução: 17 envelopes `NOVA`, 14 exigem ACK; nenhum ACK, alteração de OP/Diário/Inbox ou Party/O Primeiro feita. GitHub opcional, `GH-NOT-RUN`. `NAC-PASS`: apenas segurança/replay local em TEST; gate terminal/global HOLD. **Oficial: 0/17 contratos e 0/1.875 células R91.**

## Pendências e retomada

1. R297 (candidata): priorizar capacidade real ou gargalo de replay A1 sem reabrir histórico; verificar rejeição de corrupção pós-commit e medir custo dos verificadores de fonte sob lotes antes de reengenharia.
2. Seguir fontes reais P4 de Bestas/itens e regras de reação PA positivo, desempate de iniciativa, crítico negativo e HP0 oficial sem improvizar decisões.
3. Instância legítima/exclusividade de writer requer decisão e infraestrutura separadas; nunca transformar Library em Notion canônico por analogia.

**Checkpoint preciso:** `LAST-VERIFIED R296 (TEST + clean replay); FIRST-PENDING R297 (subject to collision check)`.
