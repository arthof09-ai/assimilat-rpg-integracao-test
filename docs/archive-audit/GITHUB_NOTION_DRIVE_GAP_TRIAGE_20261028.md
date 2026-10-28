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
