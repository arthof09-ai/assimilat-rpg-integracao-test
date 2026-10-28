# PSV CRAFT R6 — Integridade de custódia do revisor

**MESTRE-SIDE TEST, CM-000002/WS0001, OP-ARQ-RIN-REC-01.**

## ANTES

R5 final confirmado localmente: `CRAFT_R5_BANCADA_ANDROID_V12_REVIEW_20261021.zip` SHA256 `29b4bfb61a726bd4e12bffa8e245552831003ca5f3e1b7e4f5edcbd7f65eb6e8`. Replay integral R5 PASS: 63 testes de bancada, 26 de revisor, 2.000 vetores TEST, Chromium E2E. A interface HTML e `logic.js` permanecem imutáveis.

**Falha real encontrada:** wrapper Node R5 `review_capture.js` usava `writeFileSync` sem criação exclusiva. Com `node review_capture.js entrada.json entrada.json`, o resultado poderia sobrescrever a evidência original; destinos preexistentes também eram substituídos. Não confundir proteção de custódia com certificação de origem.

## DEPOIS

Pacote incremental separado `CRAFT_R6_REVIEWER_CUSTODY_TEST_20261021.zip`: 12.440 bytes SHA256 `03aa75511da00ffae13bed4d6c095dd0528dfa12ac003e409b17b3975a2e0505`. Biblioteca Mestre `/Comestre/CRAFT_R6_REVIEWER_CUSTODY_TEST_20261021.zip`, `libfile_4c480071b010819183889c21304f70f8`, readback SHA idêntico. Inclui `logic.js` pinado do R5, wrapper com criação exclusiva `wx` e modo 0600, 12 testes de preservação, 26 regressões, exemplo sintético, manifesto SHA e guia. ZIP CRC PASS, manifesto 6/6 PASS. Testes repetidos após extração da **cópia da Biblioteca**: 12/12 e 26/26 PASS.

Proteções: recusa destino igual à entrada, caminho equivalente normalizado, arquivo de saída existente, symlink, hardlink e diretório; não destrói arquivo de entrada. Não prova proteção contra usuário malicioso que altere arquivos externamente.

## Persistência e limites

Tentativa de acrescentar ANTES/DEPOIS ao LAB CRAFT existente via conexão Notion retornou **bloqueio de segurança da ferramenta**; não foi declarada escrita nem readback no Notion. Este PSV na Biblioteca é o checkpoint recuperável de R6. Não criar página, Inbox ou operação duplicada para contornar bloqueio.

F5 P0 RED; C19-021 UNKNOWN; IBX-38 e R51 sem comprovação nova; RC5/P4/produção HOLD. Nenhuma ficha, receita, PA, estoque, Party ou O Primeiro alterado. Sem INSTANCE-ID, writer, lease, epoch, ACK, fencing ou GREEN alegados.

## Próximo ponto exato

1. Quando a escrita legítima no Notion estiver disponível, registrar R6 como adendo no LAB e Diário da OP existentes, sem ACK automático.
2. Não repetir testes por métricas: receber medições reais com custódia/operador/calibração e passar pelo R45/R46; a interface Android R5 já está pronta para coleta.
3. Resolver IBX-38/C19 e destino REC-LIB R51 antes de qualquer RC5; P2-SALT-01, P2-ENERGY-02 e lote de Óleo seguem HOLD.
