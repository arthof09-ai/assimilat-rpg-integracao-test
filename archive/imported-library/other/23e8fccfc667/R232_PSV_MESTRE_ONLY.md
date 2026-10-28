# PSV R232 — Quatro Bestas VZ distintas / ataques físicos nativos — MESTRE-SIDE / TEST

## Resultado científico antes da embalagem

**PASS_R232_INDEPENDENT_NAMED_BEAST_ATTACKS_TEST_CONDITIONAL**; quatro ações físicas de quatro **espécies distintas PRECRIADAS**, cada uma registrada em um banco R18 próprio, 4 commits, 8 eventos nativos, 3 acertos e 1 erro, **0 confrontos bilaterais integrais, 0 células canônicas D**. Auditor sem importação de qualquer módulo do simulador; quatro adulterações, inclusive com hashes recompostos, rejeitadas 4/4.

| Espécie e ação | Rank da pré-criação | Seed | Ataque | Dano bruto se acertou | RD do alvo | Vida removida |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Arraia de Trovão Vítreo — Corte de Membrana | Lendário1 Titã | 23240201 | 163 | 131 | 35 | 96 |
| Tatu Vulcânico de Cobalto — Investida de Placa | Ouro Negro5 | 23240202 | 83 | 0, errou CA83 | 0 | 0 |
| Grifo de Sílica Tempestuosa — Talão de Sílica | Lendário2 Titã | 23240207 | 157 | 98 | 35 | 63 |
| Manta Ferromnésica — Golpe de Membrana | Lendário1 Titã | 23240208 | 152 | 102 | 35 | 67 |

**Cuidado: esses quatro números não podem ser usados para ordenar potência entre espécies**, pois há apenas um ataque por criatura, ranks diferentes e controles direcionados de crítico. A sequência crítica (3,4,3) foi fixada no LAB e não representa distribuição estatística do combate real.

## Fontes recuperadas

- `SPIRIT-BEAST-RUNTIME-VZ-08`, Notion `3f3c2b324ede810a8208c364d64f808d`, atualizado 08/10/2026. Congelados **apenas os quatro excertos mecânicos básicos**, não o texto integral da página; digest validado no arquivo `R232_VZ_FROZEN_PRIMARY_EXCERPTS.json`.
- `Sikong Varok — Carrasco do Tronco (ON5)`, Notion `3f6c2b324ede81f49ea9efbe1a811091`. Referência de alvo **PROPOSTA MESTRE-SIDE** Vida734, CA83, RD física35.
- `vlab_effects_v08` e R18 herdados da R230; sem motor paralelo.

## Escopo de entrada e ausência de falsos poderes

Os atores do laboratório precisam de recursos para inicializar o reducer. Como as páginas físicas das Bestas não estão materializadas ou conferidas por espécie, foram usados **HP1 e CA0 meramente como placeholders de interface para o lado atacante**. Esses números **não são atributos de nenhuma Besta**. Não há turno defensivo de Besta, iniciativa nem movimento/alcance canônico de sua espécie; a adjacência `(0,0)`/`(1,0)` é fixture TEST expressa, e a condição de alcance foi declarada somente para exercitar a ação.

Cada ataque é padrão, custo 0 PA e fonte VZ específica. Não se importou o dano-base 20d10 ao Espírito nem se criou duração/control/escape por inferência. Erro de ataque não causa dano e não consome PA inventado.

## Persistência e controles

- Quatro SQLite válidos, quatro commits R18, oito eventos nativos; cadeias de `row_sha`/`head`/`state` read-only verificadas.
- Um banco SB01 de bootstrap `R232_V0_PREFLIGHT_WRONG_IMPORT` permaneceu separado em quarentena: SQLite inicializada, **0 commits e 0 intenções pendentes**; a importação conflitante foi corrigida e as quatro seeds novas foram registradas. Nenhuma seed histórica foi reexecutada.
- Adulterações com hashes recompostos: Vida terminal, promoção falsa P4, fita de dados alterada e RD zerada → **4/4 rejeitadas**.
- Manifesto, CRC e auditor independente podem ser verificados friamente com `R232_COLD_PORTABLE_RECOVERY.py`, que não chama o executor.

## Baterias e NAC-PASS

A=R229 laboratório condicional, B=R229 laboratório + R230 R18 5 patamares, C=R229 time simples e R216 multiação, D=**4 ataques específicos VZ PRECREATE agora fisicamente executados**, E=R226/227 comparação de equipamento PS/semicanônico. A passagem de D de **0 ataques por criatura** a **4 ataques documentados** é avanço material, mas D ainda não pode ter confrontos completos ou slots oficiais: permanece **0/27 células homologadas**. Global: **0/17 contratos, 0/1.875**. Party, O Primeiro e produção **NO-WRITE/HOLD**.

**LAST-VERIFIED-UNIT R232** somente após publicação/readback. **FIRST-PENDING:** recuperar fichas físicas completas de espécies VZ para permitir contra-ataques, Vida/CA/PA legítimos e combate real; gerar benchmarks A–E com grupos comparáveis, não extrapolar de quatro golpes. **NO-REPEAT:** R01–R231 e R232 seeds, incluindo V0 em quarentena.
