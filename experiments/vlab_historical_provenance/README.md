# VLAB Stage10 + Stage12 — recuperação de fonte histórica, sem certificar contratos

Foram recuperados do ambiente Mestre os dois **ZIPs originais**, apontados pela própria [OP-VLAB-FUSION-SANDBOX-01](https://app.notion.com/p/3f3c2b324ede819496ddd7f93bd7e5d2). Eles não estavam no bundle R237 e não são versões intercambiáveis do runtime R237.

## Prova de integridade realizada em cópia local

| Pacote original | SHA-256 completo | Membros ZIP | SHA-256 de membros |
|---|---|---:|---:|
| Stage10 (`VLAB_FUSAO_EXPERIMENTAL_STAGE_10.zip`) | `77b1d2e973f4c2cddf5741c74f9263a0c652885201571d645a5b799095a26979` | 689 | 688/688 |
| Stage12 (`VLAB_FUSAO_EXPERIMENTAL_STAGE_12.zip`) | `17342b3377ac6f04c961388d87188fa48029c2e713e9eb9a9aae101ebf170772` | 719 | 718/718 |

Ambos os ZIPs passaram CRC, tiveram índices de hashes sem lacunas e todos os arquivos conferidos. Comparação entre fontes: **689/689 membros Stage10 preservados sem alteração no Stage12, 30 arquivos adicionais e zero exclusões**. Stage12 contém a mesma fonte `reconstruction/STAGE10_SOURCE_RECONCILIATION_MASTER_ONLY.json`, com SHA-256 `e74a45cdd2f7d2b70d0e576f3a519a3c311dccf097a6944b04cd61898e70d1fb`. A matriz `reconstruction/STAGE12_FUNCTIONAL_FUSION_MATRIX_MASTER_ONLY.json` tem SHA-256 `1c1f02e0de5393a81401752757276237b93ed8b32239024c59eccd62991d0c8f`.

**Separação honesta:** os dois ZIPs completos não foram transferidos ao GitHub. Os hashes de 688/718 arquivos e a paridade física 689/689 foram verificados **localmente**, não repetidos no GitHub. O GitHub guarda cópias byte-idênticas das duas **fontes JSON originais**, comprimidas só para transporte e identificadas pelos seus SHA, e reexecuta o gate DOCUMENTAL abaixo.

## Resultado documental dos gates

- Stage10: oito conflitos de fonte Bushi/Wang, status `READ_ONLY_DOCUMENTARY_EVIDENCE_NOT_CANONICAL_FREEZE`, estrita `strict_eligible=false`, zero duelos e zero créditos oficiais.
- Stage12: 17 contratos identificados, **zero terminais aprovados**; 11 `PARTIAL`, três `BLOCKED` e três `REBUILT_TEST_ONLY`. Dos 17, 14 são parciais/bloqueados. O Stage12 não possui prova do binário original v0.9, do motor unificado canônico ou do freeze completo de Bushi/Wang. `NAC-PASS-02=HOLD`.

A [auditoria executável](../../scripts/verify_vlab_stage10_stage12_provenance.py) autentica esses dois documentos por SHA e **rejeita declarações falsas de aprovação terminal**. [Seis testes negativos](../../tests/test_vlab_stage10_stage12_hold.py) atacam as alegações de GREEN, 17/17, fonte congelada e v0.9 recuperado.

## O que NÃO foi executado

A suíte histórica integral de Stage10/Stage12, os motores v0.9, 17 contratos terminais e os comparativos de combates entre estágios **não foram executados por este gate GitHub**. Os testes legítimos do VLAB R237 (8 combates, 215 testes e cinco falsificações rejeitadas) permanecem uma bateria separada. Fichas oficiais, Party, O Primeiro, escritor Notion, cânone e outros laboratórios sem escrita.

**Status:** PROVENIÊNCIA DE DUAS FONTES HISTÓRICAS RECUPERADA / DOCUMENTARY TEST PASS / CERTIFICAÇÃO DE FUSÃO E 17 CONTRATOS HOLD. Sem uso de Replit e sem novo serviço pago.

[Diário GitHub + Replit TEST](https://app.notion.com/p/400c2b324ede8102ad79e3c9d54a34ef)
