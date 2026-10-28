# VLAB — Checkpoint Mestre-only após R302

**Data:** 2026-10-22 · **OP existente:** `OP-VLAB-FUSION-SANDBOX-01` · **Identidade lógica:** CM-000006 / MESTRE-SIDE / TEST. **Writer/INSTANCE-ID/lease/epoch/fencing/GREEN:** NÃO VERIFICADOS, nenhuma reivindicação. Sem novas regras, operação ou motor em paralelo.

## Estado ANTES

- `LAST-VERIFIED R298; FIRST-PENDING R299`. R298 localizou replay A1 multiplicado, `verify_pins` milhares de vezes, sem código alterado.
- R22 original: SHA `04ddf83ba2df69059a9f00f0f46e3bee24e9adbd59094400bf3671fd72942ca6`. Overlay R289–R295: `7c9ac7b1930bf673d745e65140e5a2fd3e5b6ce422e03558a6eb31f4c79d42ec`. Overlay R296: `ecc473187158acea3e815ed5f06ee2d3b32db5743b5bb04e07e66ed856637e9d`.

## R299 — Repetição A1 eliminada em ponto controlado

- `validated_step` agora troca uma reconstrução redundante de `_fresh(st)` por `base.verify_pins()` no pré-commit, depois de `checked_load()` integral; o `_runner` continua replay A1 no journal transacional. Fonte original e histórico v0.8.1/v0.6 preservados.
- 73/73 testes herdados PASS em três segmentos de execução: 50 bases R18/R19/R20/HEAL/JSON/R296, 11 R21 e 12 R22; 4 testes R299 novos PASS (fonte alterada, fail-closed, single commit, idempotência); paridade 5 decisões/SQLite bytewise; cold install 26+4 PASS. A suíte monolítica excedeu limite e não foi computada como PASS.
- Produto `VLAB_R299_A1_REPLAY_TRANSACTION_OPT_MESTRE_ONLY.zip`, SHA256 `5b77d59007a93bf825697015cde66a935e2dfd6ec178eae3c7dc3a7a34f8a3ef`.

## R300 — Controle ABBA, PASS apenas

- Fontes R296 em duas cópias, 111 módulos Python comuns e só um módulo diferente; 4 pares de sementes ×12 PASS por braço = 96 decisões. Quatro pares favoráveis a R299, redução de latência agregada de **13,2461%** em host local. cProfile 8 PASS: `_fresh` 75→67, `verify_pins` 8089→7313 e scheduler step 992→896. Sem extrapolação para campanha/celular.
- Produto `VLAB_R300_ABBA_REPLAY_PERFORMANCE_MESTRE_ONLY.zip`, SHA256 `96f404d4036b72a5c8c076b7b6b1527e3b3c0314f8d6487dac9a3cc25b9b8310`.

## R301 — Combate sintético com efeito nativo

- Quatro seeds 30101–30104, 2 braços por seed e até 9 decisões por cena: **8 cenas** = 72 decisões, 8 iniciativas, 48 ataques v0.8.1, 16 curas fictícias v0.6, 8 reações DEFENDER, 0 créditos oficiais.
- Os 4 pares de arquivo SQLite são **byte a byte idênticos**, têm PRAGMA integrity_check PASS e hashes iguais aos registrados nos oito JSONs. Estado, eventos, cadeia e recepção mecânica também coincidem.
- Ganho observado local no tempo de decisão de efeitos nativos: **9,0% agregado** neste último lote, amostra de 4 pares. Não igualar com ganho PASS-only R300, nem declarar IC populacional.
- Produto `VLAB_R301_NATIVE_BATTLE_PARITY_MESTRE_ONLY.zip`, SHA256 `c6d49ce4a53ad9386d187364df0d946342c7c456009ebc1f442aea39dae088f4`.

## R302 — Leitura canônica de admissibilidade P4

- Fontes `BEAST-FULLSPEC-VZ-06`, `AUD-BEAST-FULLSPEC-VZ-06-01`, `PRECREATE-VZ-MANIFEST-01`, `VZ-MATERIAL-MANIFEST-01` consultadas. Auditoria pré-criação 54/54, ataques/CD 12/12, mas manifestos antigos indicam `PHYSICAL-PAGES=0/6`, `0/14` fichas materiais no pacote e `0/1649` UAT de materialização.
- **Nenhum recibo P4 físico elegível foi confirmado na amostra consultada**; não declarar ausência global. O VLAB não assume materialização de outro Comestre. Dossiê fonte: `VLAB_R302_FONTE_P4_ADMISSIBILIDADE_MESTRE_ONLY.md`.

## Inbox, governança e retorno

- Inbox `CM-000006` reconsultada: nova IBX-167 (minuta `AUTH-NOTION-01 / S4` ciência), explicitamente **NÃO VIGENTE / NÃO HOMOLOGADA**. Demais mensagens não foram reconhecidas em nome de instância sem claim. `BLOCK-PERMIT=RED` / `GREEN=HOLD` persistem. Uso de GitHub opcional, **CI NOT_RUN**.
- **0/17 contratos terminais**; **0/1.875 células oficiais R91**; **0 escrituras Notion, Party e O Primeiro**; zero fichas canônicas alteradas. Testes sintéticos não mudam denominadores.
- **LAST-VERIFIED LOCAL R302 → FIRST-PENDING CANDIDATE R303.** Verificar colisões e Inbox primeiro. Próxima finalidade: atacar um gargalo funcional real de reações/PA ou source P4 após materialização legítima, nunca ampliar R91 por extrapolação; se otimizar replay A1, continuar testes adversariais de fonte mutante, recovery e paridade de engine. Continuar na OP/Library já existentes, sem escrever em Notion até writer competente.
