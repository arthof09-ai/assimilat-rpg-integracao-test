# OP-DMG-CORPUS-EMP-01 — Checkpoint READ-ONLY v0.2
Data: 2026-10-08. MESTRE-SIDE. Sem escrita no Notion; sem instância ou lease assumidos.

## Evidência
- 104 IDs locais únicos: 48 Gelo diretos, 43 Fogo diretos, 13 referências cruzadas Fogo.
- 49 expressões ofensivas preliminares, 49 componentes com pool de dados identificado.
- 69 divergências textuais segundo parser v0.2, 24 concordâncias, 5 concordâncias parciais, 6 indeterminados. A alegação anterior de 71 não foi reproduzida; adjudicar a diferença, não substituir silenciosamente.
- 0/104 FULL-FIGHT liberados. Valores estatísticos de dados NÃO são dano final nem DME por tentativa.
- 239 pais e 412 ponteiros pertencem ao checkpoint estrutural anterior; não se confundem com o corpus analítico.

## Pendências de recuperação
1. Recuperar bytes dos CSV de I0003; o Notion apresenta referências para os anexos, mas o conteúdo não foi incorporado neste dataset.
2. Extrair IDs do conjunto anterior de 149; só então calcular interseção, união e novidade contra os 104.
3. Resolver Fogo 44 × 43 confrontando as linhas dos dois CSV Fogo do predecessor com os 24 pais e as seis referências cruzadas.
4. Adjudicar 71 relatados × 69 reproduzidos; considerar grafias alternativas e classificações fora da escala (ex.: Épico).
5. Reabrir as 104 fichas somente seletivamente para completar Vida/CA/atributos/RD/ações e ancoragem por bloco, sem recontar pais.
6. Retomar demais famílias após confirmar fronteira exata dos lotes já executados pelo predecessor.

## Governança
- CM-000001-I0003: predecessor sem transferência de lease comprovada.
- CM-000001-I0004: comprometida em outro workstream.
- CM-000001-I0005: apenas candidata, não consumida.
- Nenhum registro foi criado no Notion nesta execução.
- DMG-RANK-01 v1.1 OFICIAL preservado.
- O Laboratório de Combate Virtual recebe somente contrato e dados, não alterações de motor.

## Arquivos
- OP-DMG-CORPUS-NORMALIZED-READONLY-v02.json
- OP-DMG-RANK-CONFLICTS-READONLY-v02.csv
- OP-DMG-ATTACKS-READONLY-v02.csv
- OP-DMG-FULL-FIGHT-ELIGIBILITY-v02.csv
- OP-DMG-VLAB-INTEGRATION-CONTRACT-v02.json
- OP-DMG-F1-RECOVERY-READONLY-20261008.json (fonte local anterior)

## Gate de aceitação
READ-ONLY LOCAL CHECKPOINT, não NAC-PASS terminal. Progresso F0–F18 indeterminável.
