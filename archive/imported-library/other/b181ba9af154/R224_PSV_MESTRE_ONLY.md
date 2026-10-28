# PSV R224 — Seleção de amostra por `UNKNOWN-EFFECT` × piso TEST de dano ímpar

**Comestre:** CM-000006 lógico / OP-VLAB-FUSION-SANDBOX-01 / MESTRE-SIDE / 21/10/2026

## Hipótese científica

A orientação provisória do Mestre **“se não me engano ... arredonda para baixo”** poderá remover censura técnica de SAVE-HALF ímpar. Mas uma amostra apenas dos combates sem bloqueio pode sofrer viés de seleção. A R224 mede esse efeito com novos pares de seeds iguais entre os braços.

## Preflight e pré-registro

R223 preservada como baseline com aprovação apenas TEST condicional. Pré-registro R224 SHA256 `f132fe60a582e0e20c87626283c829a27c7d7891d2c33d5f6562f2586a051b0a`. 24 seeds independentes pré-especificadas (22453001–22453024), dois braços por seed: `STRICT_HOLD` e `TENTATIVE_FLOOR`. Mesmas rolagens de iniciativa ON5, mesma fita RNG e scheduler R18. Empate de iniciativa bloqueia antes de iniciar. `STRICT_HOLD` preserva a proibição original; `TENTATIVE_FLOOR` usa somente cópia TEST fonte-vinculada. Não houve replay de IDs antigos.

## Novidade material

**48 braços previstos; 8 bloqueados pré-DB (4 seeds); 20 unidades pareadas admitidas.**

- Piso TEST: **20/20** alcançaram horizonte.
- Regra estrita: **18/20** alcançaram horizonte; **2** interrompidos por salvaguarda ímpar, sem desfecho válido.
- 38 bancos finais, 2 bancos com intenção pendente e `UNKNOWN_EFFECT`.
- 465 commits legítimos, 2841 eventos; 2 conjurações de piso em cenas novas.
- O auditor independente confirmou que os **prefixos de eventos são iguais entre braços por seed** até a primeira diferença provocada pela regra, sem inventar RNG.

## Quarentenas novas

- `22453002`: STRICT_HOLD tem 9 commits antes da tentativa #10; `TENTATIVE_FLOOR` concluiu a cena, com primeiro piso = 36.
- `22453022`: STRICT_HOLD tem 0 commits com primeira intenção pendente; `TENTATIVE_FLOOR` concluiu a cena, com piso = 29.

Esses dois bancos não foram reexecutados nem reparados. Uma intenção pendente é uma falha controlada, não resultado de derrota ou vitória.

## Auditoria

`r224_independent_pair_audit.py` verifica SQL em mode=ro/immutable, R18 hash receipts, eventos, ordem de iniciativa, origem das rolagens, conservação mecânica nos 38 terminais, pendências e prefixos pareados. Cinco clones adversariais (hash rebuilt e pending-base forged) foram corretamente recusados. Nenhum auditor executa runner.

## Conclusão e limites

Na amostra de 20 pares, permitir a regra provisória recuperou dois braços que a especificação estrita censuraria por fonte, isto é **2/20 = 10% da fixture**. Isso **não é taxa global do RPG** nem constitui permissão de usar piso canônico. Os NPCs e geometria são TEST propostos, empate de iniciativa ainda HOLD, RD mágica 0 apenas fixture.

## Governança e sucessão

Produção HOLD; Party/O Primeiro NO-WRITE; writer/INSTANCE-ID não demonstrados. 0/17 contratos terminais e 0/1.875 células oficiais homologadas. R224 PASS técnico condicional, NAC-PASS global HOLD. LAST-VERIFIED: R224 auditada após publicação e recuperação fria. FIRST-PENDING: Mestre ratificar ou retificar arredondamento de dano ímpar e resolver empate de iniciativa. NEXT-5: (1) consulta normativa precisa, (2) testar cenário com dano misto/defesas quando fonte completa, (3) Controle de Besta completo, (4) Transformação Prata1+, (5) benchmark canônico R91.
