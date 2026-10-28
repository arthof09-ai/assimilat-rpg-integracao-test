# PSV R226 — Pares físicos com/s em descarga da Manopla do Trovão Cativo — MESTRE-ONLY TEST

**Data-base:** 21/10/2026. **Operação:** `OP-VLAB-FUSION-SANDBOX-01`. **Identidade lógica:** CM-000006. **Produção/Party/O Primeiro/fichas originais:** HOLD/NO-WRITE. **Contratos terminais:** 0/17. **Matriz oficial:** 0/1.875.

## ANTES → DEPOIS

- **ANTES:** R225 confirmou aritmética de dano com arredondamento para baixo, três novos ensaios, sem promoção normativa. R226 ainda não possuía recibo fonte-vinculado da nova descarga.
- **DEPOIS:** oito pares de duas variantes do mesmo ataque físico equipado, com `apply_weapon_attack` nativo para o componente físico, `mitigate` nativo para o pool adicional Raio, declaração depois do acerto e antes do RNG de dano, um único commit R18 por janela de ataque e turno do alvo, PA e condição temporal preservados. Sem reescrever o motor v0.8.1.

## Fonte, admissibilidade e limites

- **Manopla do Trovão Cativo**, [página Mestre-side](https://app.notion.com/p/3f5c2b324ede81f5ac62fb940204cdac), **PS/SEMICANÔNICO, NÃO P4**, classe Ouro, uma descarga por descanso de oito horas, ativável após confirmar acerto corpo a corpo e antes de rolar dano, 22 PA, +5d8+3 de Raio, sem nova Ação; em dano de Raio efetivo >0 aplica −3 m de velocidade até o final do turno seguinte do alvo. Não soma duas descargas. Não equivale a peça com certificação canônica para Bateria E.
- Réplicas de Arveth e Varok, fontes Mestre-side propostas R44 e páginas primárias. Dano físico `8d10+35`, ataque `4d6+72`, CA83 e RD físico35 reproduzem a fixture informada; **não** benchmark oficial.
- **Limites importantes:** item equipado no clone TEST em ambos os braços; a RD mágica de Varok não está documentada integralmente para a descarga e foi fixada como **0 somente em hipótese TEST**. A velocidade base de 4 m é hipótese numérica de observação de efeito; não estabelece a velocidade oficial de Varok, tamanho do bloco, movimento publicado ou geometria universal. Não há descanso simulado nem prova de recarga.

## Evidência física independente

`R226_PREREG_BEFORE_EXEC.json` pré-registrou oito seeds e dois braços: `SAME_PHYSICAL_NO_MAGIC` versus `SAME_PHYSICAL_WITH_MAGIC`. Os dados ofensivos físicos foram os mesmos em cada par e conferidos independente via SQL.

- **16 bancos SQLite admitidos**, 8 pares de seed, **32 commits** e **174 eventos nativos**.
- **7/8 pares** acertaram o ataque e produziram descarga no braço com magia; **1/8** errou e não gastou os 22 PA.
- **187 PV extras** de Raio nos sete acertos e **154 PA** do item, sob RD mágica zero **hipotética**, 7 aplicações temporárias de `−3 m` com expiração no final do turno seguinte.
- **0 KO**, **16 censuras** após janela de alvo com ação padrão explicitamente passada. **Não são 16 combates integrais** nem evidência de equilíbrio universal.
- Auditor independente `code/r226_independent_sql_audit.py`: não importa motor, reconcilia SHA de duas linhas por SQLite, state/head, dados 4d6 e 8d10, dano/RD, procedência, ativação e evento de expiração. `PASS_R226_INDEPENDENT_PAIR_SQL_AUDIT_SEMICANON_TEST`.
- Quatro adulterações com hashes reconstruídos foram rejeitadas (`FREE_PA`, `HIDDEN_SLOW_PERSISTENCE`, `FAKE_NONCANON`, `FORGED_ITEM_ARM`). Nenhum SQLite de produção foi tocado.
- Existe no pacote uma ideia de **Flecha de Trava** que entrou em rascunho durante preflight simultâneo, mas não foi executada como R226 nem contada. Preservada em `evidence/quarantine/R226_FLECHA_DRAFT_NOT_RUN.py`; a namespace R226 estava ocupada legitimamente pelo experimento da Manopla.

## Ciência e governança

O dado **+187 PV agregados** vale apenas para os oito pares dirigidos TEST com fontes e hipóteses acima. Este estudo demonstra capacidade de separar componente físico de Raio com mesmo chassi, de cobrar o custo sem duplicação de Ação e de expirar efeito fonte-bound; **não** satisfaz o gate de equipamento **canônico** da Bateria E. O total de eventos e ataques não multiplica a quantidade estatística de pares.

**NAC-PASS local:** `PASS TEST SEMICANON CONDICIONAL`. **NAC-PASS canônico:** HOLD. **LAST-VERIFIED-UNIT:** R226 após cold readback. **FIRST-PENDING:** R227 candidato, preflight obrigatório. **NEXT-5:** (1) fechar teste de movimento realmente alterado por um efeito fonte-delimitado; (2) escolher origem com movimento documentado, se existir; (3) ampliar a comparação de duas componentes à RD mágica explicitamente fonte-provada; (4) triagem de controle de Besta e transformação; (5) preparar recibo incremental ao DMG via rota competente, sem duplicar IBX-126.
