# Auditoria de lacunas GitHub × Notion × Drive — 2026-10-28

**Estado:** TRIAGEM PARCIAL VERIFICADA; não equivale a inventário completo nem prova de ausência. **Escopo:** repositório `arthof09-ai/assimilat-rpg-integracao-test`, Notion Mestre e Drive RPG. **Diretriz expressa:** material Mestre-side técnico é elegível a GitHub público; nenhuma proibição genérica baseada na origem Mestre. Sem tokens/credenciais/dados pessoais, sem confundir publicação com promoção canônica.

## Repositório — evidências de material já presente (não duplicar)

- `archive/levelup/R049_ORC_ANDROID_OFFLINE_MESTRE_ONLY_TEST.html`; `docs/levelup/RECUPERACAO_R216_P23_CLAUDE_20261028.md`; `docs/levelup/R216_P23_NOTION_MANIFEST.json`.
- `archive/craft/CRAFT_R49_REVISOR_ANDROID_MESTRE_TEST.html`, `experiments/craft_b30/`.
- `archive/vlab/VLAB_BACKUP_MANIFEST_MESTRE_ONLY_2026-10-27.json`; `docs/canonical-snapshots/VLAB_BACKUP_AUDIT_20261027.notion.md`; `scripts/verify_vlab_stage10_stage12_provenance.py`.
- `experiments/dmg_c29/`, `tests/run_dmg_c29_native.py`, `docs/canonical-snapshots/DMG_RANK_01.notion.md`.
- `docs/archive-audit/LIBRARY_TECHNICAL_INVENTORY_20261028_PART02.json`, `docs/production/PROTOCOLO_INTEGRADO_PRODUCAO_2_5D_v1_0_TEST.md`.

## Fontes externas concretas encontradas para reconciliação

| Família | Arquivo existente no Drive RPG | Tamanho reportado | Próximo teste de lacuna |
|---|---|---:|---|
| VLAB | [OP-VLAB-FUSION-SANDBOX-01](https://drive.google.com/file/d/1ZpQsANAfobENHRKTDaVYdWPxIFqNkPSL/view) | 199941 bytes | Comparar versão, conteúdo e anexos com `docs/canonical-snapshots` e `archive/vlab`; não confundir cópia da OP com código nativo |
| VLAB | [VLAB IBX39 — gateway/fencing](https://drive.google.com/file/d/1VM29Jm6KKa4bqCJsD905xU9n9jTrc_0v/view) | 54048 bytes | Verificar se regras/contratos operacionais já têm representação no repo |
| CRAFT | [Laboratório CRAFT](https://drive.google.com/file/d/1Z3RNX6K402yyvh_OQHx6jCYqeTnRi6Rm/view) | 493528 bytes | Distinguir diário histórico, contrato, código, anexos |
| CRAFT | [AUTO-RUNTIME-CRAFT-01](https://drive.google.com/file/d/13al7Ex9dgR5n16w1eQQWWNy5eYLZFzTR/view) | 162767 bytes | Reconciliar contrato de runtime com `experiments/craft_b30` |
| CRAFT | [AUD-CRAFT-F5-REMAP-01](https://drive.google.com/file/d/1V6N2Djwz8tOf8kq3Xaa4MYAWgRKdkER2/view) | 188702 bytes | Comparar documentação técnica com fontes GitHub |
| LEVEL-UP | [LEVEL-UP R21](https://drive.google.com/file/d/1_y1psivBkjqiDeXrVNRUWwaIFItd6Lxp/view) | 44830 bytes | Determinar se há código/contratos ausentes |
| LEVEL-UP | [Guia P12→P23](https://docs.google.com/document/d/1DmtfRx0KA55pxokH86xA88CjnRBvKZu3rU9Je8XulxY/edit) | 4904 bytes (metadata) | Já existe equivalente `docs/levelup/RECUPERACAO_R216_P23_CLAUDE_20261028.md`; não duplicar |
| GitHub/coordenação | [Diário Operacional LAB GITHUB+REPLIT](https://drive.google.com/file/d/14oZ1pWMB1Wz2y3hDvybRf009wfezwisx/view) | 105561 bytes | Distinguir status/histórico de arquivos de código faltantes |

## Critério de promoção de arquivos faltantes

1. Obter bytes originais do Drive/Biblioteca/Notion, identificar arquivo, origem, data, SHA256 e versão; separar código/binário de narrativa.
2. Verificar se o mesmo conteúdo já existe no GitHub por hash/assinatura/versão, não só pelo nome; não criar duplicata.
3. Arquivar fontes originais sob `archive/<workstream>/` ou `docs/canonical-snapshots/` conforme natureza; registrar URL original e classificação (TEST/PROPOSTO/CANÔNICO), sem sobrescrever arquivo vigente.
4. Para código executável, testar em branch isolada antes de CI, com rollback e gates; commits de preservação não promovem engine.
5. Se a conexão não disponibilizar bytes, registrar `BYTES_PENDING` e não fingir migração. Não usar a justificativa “Mestre-side” para bloquear.

## Pendências prioritárias

- **P0**: obter bytes dos pacotes nativos LEVEL-UP P23/P44, VLAB Código-Mãe, CRAFT e artefatos DMG que não estejam fisicamente no repo; auditar hashes e presença. A simples referência Notion/Drive não demonstra recuperação binária.
- **P1**: cruzar árvore completa do repositório com inventários Drive e Biblioteca; esta rodada só fez buscas temáticas no índice GitHub, não árvore exaustiva.
- **P2**: publicar apenas faltantes comprovados e preservar proveniência/estado; verificar readback de cada commit.

**Limite de prova:** buscas no Drive e GitHub verificadas; a busca geral Notion não retornou conteúdo útil nesta rodada. Não é legítimo declarar “tudo migrado”, nem atribuir toda ausência à antiga restrição sem histórico específico.

## Sucessão — Reconciliação nominal dos 35 arquivos (28/10/2026)

**STATUS: VERIFICADO (índices / listagem de Library / readback GitHub); PARCIAL quanto a bytes e testes.** Apêndice do relatório existente: preserva o histórico e não substitui documentos anteriores.

### Denominador e causa da divergência

- Biblioteca Mestre `/Comestre`: paginação integral 18 páginas, **3.476 entradas = 3.467 arquivos + 9 pastas**. Inventários já presentes: PART01 (2.991 arquivos, 2.654 candidatos técnicos), PART02 (476 arquivos, 441 candidatos). **3.095 candidatos técnicos** totais, não equivalem a 3.095 fontes únicas ou conteúdos SHA únicos.
- PART02: `scope.entries=476`, `counts.technical_candidates=441`, `items.length=441`. Comparação nominal por `library_id` com últimas 476 entradas da Biblioteca encontrou **35 arquivos excluídos de items**, exclusivamente **24 PNG + 10 XLSX + 1 DOCX**. As demais extensões têm diferença ZERO entre cabeçalho e itens. O delta `other:278−243=35` é o mesmo. Causa quantitativa identificada; intenção do filtro do gerador permanece não verificada. Não corrigir números silenciosamente.
- GitHub `main` no check-in: `a31438287ed6d3eee8880ca70cb44ae81d432340`; árvore recursiva não truncada com **94 blobs/arquivos**; **23 branches**, **0 releases** retornadas. O PART01, README e pasta `archive/library-source/other/` já existem, logo não duplicar.
- `archive/vlab-source/R326/` já contém 11 partes binárias, manifesto e reassemblador. O manifesto **declara** ZIP 15.951.561 B, SHA256 `420fa4c9f084df449e68075e30fec50ad392bfe041070433b9a4feaf4daf17d5`. Existência da árvore comprovada; SHA256 do ZIP reassemblado e CRC nesta instância ainda não reexecutados. Não tratar como ausente nem canonizar.

### Recuperação real deste lote

- Quatro sidecars `.zip.sha256` da ponte VLAB ↔ Tabletop lidos nas **duas contas do Google Drive**; conteúdo textualmente idêntico em pares **4/4**. Foram publicados como arquivos reais em `archive/vlab/bridge-checksums/` na branch `audit/recovery-20261028-library35-drive-checksums` e relidos com igualdade exata **4/4**; manifesto `MANIFEST_20261028.json` contém dois URLs de origem para cada um, hash do próprio sidecar e digest declarado do ZIP-alvo. **Não afirmar que os ZIPs foram migrados.** Sem teste de código executável, branch não mesclada à main.
- Materialização raw tentada para `IBX17_R37_CONTINUIDADE_VERIFICAVEL.zip`, `PA_R68_AUDITORIA_INTEGRIDADE_RETOMADA_MESTRE_ONLY_TEST_20261023.zip` e `LEVELUP_R216_P23_010_FF_FIXTURE_CLONE_TEST_ONLY.zip`: resposta **'This Project file does not have an authorized raw-byte materialization path.'** Classificação **BYTES_PENDING**, sem criação substituta.
- Consultas aos dois Drives por ZIP e pelos nomes R049/R326 localizam metadados/documentação e checksums, mas não demonstram cópias binárias dos três ZIPs. **Não confundir busca parcial com censo integral**; raízes/pastas do Drive novo foram acessíveis.

### 35 registros presentes na Biblioteca, não incluídos em `PART02.items`

| # | Nome original | Bytes declarados no índice Library | ID Library | Extensão |
|---:|---|---:|---|---|
| 1 | Dama de Gelo sob a Lua Cheia.png | 3442254 | `file_00000000b4a0820e8c7b7222c4b711e6` | png |
| 2 | Feiticeira da Nevasca Lunar.png | 3316636 | `file_000000005ca0820e94ca7c57de4d56c7` | png |
| 3 | Espírito de Gelo sob a Lua.png | 3324938 | `file_000000003e18820eb0107f4462c2f320` | png |
| 4 | Transformação Demoníaca sob a Lua Roxa.png | 3469242 | `file_000000007e04820eadff0ab5e0f406e0` | png |
| 5 | Feiticeira Lunar entre Cristais de Gelo.png | 2906044 | `file_0000000071dc820eab615f697da8d949` | png |
| 6 | Feiticeira sob a lua entre cristais de gelo.png | 3126947 | `file_000000008fec820ea251850190af0920` | png |
| 7 | Guerreira Lunar entre Cristais de Gelo.png | 3016621 | `file_00000000efa4820e912dcc792b1afb2f` | png |
| 8 | Sacerdotisa de Gelo sob a Lua.png | 2981805 | `file_000000003f28820e86bd09ffccbfd884` | png |
| 9 | Donzela Lunar da Floresta Congelada.png | 3014291 | `file_00000000dcac820e8f4fd657d929b165` | png |
| 10 | Nobreza Ferida sob a Neve Eterna.png | 3005339 | `file_00000000478c820e8976d6b8a3641b19` | png |
| 11 | Demônio Vampírico sob a Lua Púrpura.png | 3023222 | `file_00000000cf28820ebf39ec70200fd6b2` | png |
| 12 | Demônio Integrado sob a Lua Roxa.png | 3153087 | `file_00000000b474820ea5d76006d17d459b` | png |
| 13 | Demônio Lunar com Boca no Peito.png | 3135207 | `file_000000007d44820eb3a9bd548b608dff` | png |
| 14 | Demônio Sob a Lua Violeta.png | 3421348 | `file_00000000433c820e9557355683761cb9` | png |
| 15 | Guerreiro Demônio Sob a Lua Roxa.png | 3257493 | `file_00000000b8d0820ebfa379b5f71c575a` | png |
| 16 | Feiticeiro Ferido na Floresta Nebulosa.png | 2935875 | `file_000000007f30820e99c797417bbc2bcb` | png |
| 17 | Feiticeiro Ferido sob a Lua Violeta.png | 3166401 | `file_000000007b88820eb8773da2bfaa4f66` | png |
| 18 | Mago Ferido sob a Lua Carmesim.png | 3176618 | `file_00000000300c820e934cf6b001c461e5` | png |
| 19 | Feiticeiro Ferido sob a Lua Púrpura.png | 3116635 | `file_000000009c94820e8cdbfaf993a10141` | png |
| 20 | Prisioneiro de Prata nas Ruínas Góticas.png | 3035331 | `file_00000000b170820eb47f0607759e72fc` | png |
| 21 | DOSSIER_DECISORIO_R23.docx | 47196 | `file_0000000069e0820eb2bda834cd07dbb7` | docx |
| 22 | VZ_WS0003_R08_SCIENCE_DASHBOARD(1).xlsx | 34467 | `file_0000000095c0820e9801516038c53667` | xlsx |
| 23 | VZ_WS0003_R08_SCIENCE_DASHBOARD.xlsx | 34467 | `file_00000000520c820e9b2588d401a00f5d` | xlsx |
| 24 | VZ_WS0003_R07_AUDIT_MATRICES.xlsx | 30842 | `file_00000000ca2c820e9ca698feedd0780d` | xlsx |
| 25 | VZ_WS0003_R04_SOURCE_OFFER_MATEMATICA_PRECRIACAO_20261009.xlsx | 97595 | `file_000000009290820e926016a0c84c4188` | xlsx |
| 26 | VZ_WS0003_R04_SOURCE_OFFER_MATEMATICA_PRECRIACAO_20261009.xlsx | 97595 | `file_0000000017d4820eac376dfed45cd31f` | xlsx |
| 27 | VZ_WS0003_R03_SOURCE420_OFFER1008_PRECREACAO_20261008.xlsx | 153105 | `file_000000001134820e9074957256ce2bf5` | xlsx |
| 28 | VZ_WS0003_R03_SOURCE420_OFFER1008_PRECREACAO_20261008.xlsx | 153105 | `file_00000000037c820eaed39ff59eaf37b9` | xlsx |
| 29 | VZ_WS0003_V2_Caderno_Prepronto_20261008.xlsx | 67288 | `file_00000000a668820e918f15ae1cea5a5b` | xlsx |
| 30 | VZ_WS0003_V2_Caderno_Prepronto_20261008.xlsx | 67288 | `file_0000000090d4820e91e666ccf1d846dd` | xlsx |
| 31 | VZ_WS0003_Painel_QA(1).png | 178864 | `file_000000000344820eb1687d17279417ff` | png |
| 32 | VZ_WS0003_Pacote_Corretivo_200_Drops_20261008.xlsx | 69997 | `file_000000001ce0820e94394d29e9c08c71` | xlsx |
| 33 | VZ_WS0003_Painel_QA.png | 178864 | `file_00000000d294820e9ba9f4144b617de7` | png |
| 34 | Matriz Regional de Recursos F4.png | 2071686 | `file_00000000bd34820e93a486e85dc02696` | png |
| 35 | Painel F4: Matriz Regional de Recursos.png | 2294230 | `file_00000000d0c0820ea40134447ab5c3ee` | png |

**Risco de duplicatas:** nomes repetidos (alguns XLSX) e tamanhos iguais não demonstram SHA idêntico; preservar origem e caminho antes de deduplicar.

**GATE:** PASS documental de publicação/readback dos 4 checksums + manifesto em branch; HOLD de PR/merge, ZIP bytes, testes executáveis, integralidade Drive e NAC-PASS terminal. **FIRST-PENDING:** recuperar primeiro ZIP de bytes efetivamente acessíveis, comparar SHA256 e CRC, identificar duplicatas, versionar em branch e testar, sem tocar Party/produção. **NO-REPEAT:** não republicar os R326 já presentes, não reconstruir ZIPs sem bytes e não chamar sidecars de código executável.
