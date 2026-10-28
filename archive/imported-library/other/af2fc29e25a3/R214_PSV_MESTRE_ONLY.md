# PSV R214 — VLAB Temporalidade da Reação / Prioridade R43 / Bilateral

**Data-base:** 20/10/2026 — MESTRE-SIDE / TEST. **OP existente:** `OP-VLAB-FUSION-SANDBOX-01`. **Identidade:** `CM-000006` lógica; INSTANCE-ID e writer **NÃO REIVINDICADOS**. **LAST-VERIFIED-UNIT anterior:** R213. **Produção:** HOLD. **Party/O Primeiro:** NO-WRITE.

## ANTES

R213 havia integrado movimento nativo a oportunidades source-gated, mas o tape RNG era produzido antes de o resolvedor v0.8.1 consumir a Reação. A R49 resolvia 4d6 de prioridade em janelas históricas, sem integração no movimento atual. A cena multiturmo de R213 era unilateral.

## DEPOIS — R214 TEST condicional

R214 realizou extensão isolada do `vlab_effects_v08.py` (cópia histórica v0.8.1) com `declare_opportunity_reaction` e parâmetro `opportunity_intent_seq` de `apply_weapon_attack`. A declaração valida a fonte e reserva a Reação na própria cópia transacional R18, **antes do tape ofensivo**, que então é verificado e resolvido pelo núcleo nativo. Um intent só pode ser utilizado uma vez, vinculado ao atacante, alvo e fonte. A mesma transação R18 publica Reação, RD, dano, Vida e movimento. Nenhuma manipulação para passar por um `reaction=1` falso.

O desempate R43/R49 usa `vlab_r26_master_rulings.tie_order` historicamente existente, `4d6` por Feryn ON5, rerrolagem só dos empatados, sem fallback por ID. Disputa de prioridade vem antes da declaração ofensiva daquele atacante (distinta da RNG ofensiva).

## MEDIÇÕES — NOVAS, NÃO ADICIONAR COMO OBSERVAÇÕES INDEPENDENTES DE EVENTOS

- **12 execuções de oportunidade TEST**, 12 seeds únicas, 14 commits, 120 eventos nativos; 14 oportunidades efetivas, 14 reservas e Reações consumidas, 12 acertos, **2 erros com Reação perdida**, 610 PV efetivos na amostra; 14 janelas, 12 movimentos concluídos; 2 KO do alvo móvel e 2 interrupções sem movimento publicado.
- **3 execuções bilaterais TEST**, 3 seeds, quatro rodadas cada, 24 commits, 93 eventos, 24 ataques físicos (Varok × Arveth), 22 acertos, 1.466 PV retirados no total, **0 KO, 3 censuras**. Ambos participaram com quatro turnos ofensivos em cada seed; sem movimento nem AOO nesta coorte independente. A duração é horizonte de ensaio, não garantia de combate completo de campanha.
- **TOTAL:** 15 execuções novas / 15 seeds, 38 commits, 213 eventos, 38 ataques físicos, 14 de oportunidade, 34 acertos e 2.076 PV experimentais efetivos. Nenhuma comparação de política pareada ou vantagem universal reivindicada.
- **Segunda reação:** `SPENT_CHAIN` prova no mesmo SQLite um ataque anterior que consumiu a Reação e segundo gatilho posteriormente sem novo débito, sem segundo ataque. A passagem entre atores é transição sintética pré-registrada, não paridade de scheduler oficial completo.
- **R43/R49:** duas seeds com Feryn ON5 duplicado, ordem por `4d6`, sem rank Bronze nem ID. Os critérios e RNG foram pré-registrados antes das execuções.
- **KO:** dois casos letal contra Cabra impedem a segunda oportunidade, preservam Reação de Varok e não publicam movimento. Custo da tentativa interrompida: `UNKNOWN_EFFECT/HOLD`.
- **Negativos:** 9 provas de segurança: falta de gatilho, Reação 0, fonte errada, reserva duplicada, ataque sem intent, ausência de Vantagem, comando repetido, falha R18 após intenção e recusa de replay quando `pending` existe.
- **Crash control:** um SQLite novo `R214_FAULT_AFTER_INTENT_S21449001.sqlite`, **quarentena técnica**: intenção pendente 1, commits 0, nenhuma mutação de snapshot ou efeitos publicados; não tentar auto-replay. NÃO SOMAR como combate.

## FONTES E LIMITES

- Sistema de Combate (`3ebc2b32-4ede-81f1-be4b-e8804ac113c0`) para Ação, Reação, Oportunidade com Vantagem, R50/R51; R43 e R49 para concorrência e `4d6` ON5; R45B para ordem declaração → RNG.
- Feryn, Varok, Arveth e Cabra: fontes Mestre-side congeladas já usadas em R44/R46. São **NPCs PROPOSTOS** / contratos TEST. O congelamento de fontes não dispensa futura reconciliação/canonização.
- Adjacência explicitamente declarada pelo contrato de cena R44; **não** corresponde a metragem oficial de bloco. Velocidade de 3 m é hipótese conservadora TEST. Não canonizar geometria, velocidade, arma, dano ou RD a partir desta bancada.
- Críticos negativos usam política experimental antiga VLAB; sem promoção normativa.
- **R212-R43-ADJACENCY-SOURCE continua HOLD:** bloco↔métrico, diagonais e momento de cruzamento não estabelecidos em fonte competente.
- Custo de Movimento interrompido por KO continua `UNKNOWN-EFFECT/HOLD`.
- Não reivindicar que AOO com dois NPCs e combate bilateral Varok/Arveth fechem todos os contratos de 17 ou representem benchmark de potência.

## AUDITORIA E PASS

Independente da execução: `code/r214_independent_sql_audit.py` examina somente SQLite/JSON, reconstitui hash-chain R18, valida intenção anterior à RNG, ligação da intenção ao ataque, Vantagem, RD e Vida, estado da Reação, prioridades e renovação de turnos. `code/r214_safety_controls.py` realizou testes destrutivos somente em cópias TEST. `R214_COLD_PORTABLE_RECOVERY.py` verifica manifesto, CRC, conteúdo e auditor READ-ONLY em extração limpa.

**NAC-PASS técnico local:** PASS condicional à fixture TEST. **NAC-PASS normativo/global e produção:** HOLD. **Contratos terminais:** 0/17. **Matriz oficial:** 0/1.875.

## INTEROPERABILIDADE E INBOX

Os encaminhamentos existentes de Orc × LEVEL-UP e corpus DMG R209–R213 permanecem **PREPARED_NOT_SENT**. Nenhuma mensagem enviada, recebimento ou ACK reivindicados nesta instância; Perfil CM-000006 permanece com writer não demonstrado. Encaminhamento depende de autoria legítima e rota competente, sem atrasar testes TEST isolados.

## FIRST-PENDING / NEXT-5

**FIRST-PENDING:** R215 candidato (confirmar colisão); em paralelo `R212-R43-ADJACENCY-SOURCE` e custo de Movimento interrompido por KO. **NEXT-5:** (1) validar fonte/decisão de blocos e custo interrompido, (2) ampliar reações defensivas em combate bilateral mantendo R50/R51, (3) testar 2×1 tático com movimento, cura e controle, (4) avançar uma Bateria E ou transformação Prata1+ fonte-completa, (5) encaminhar DMG e Orc×LEVEL-UP sob autoria comprovada, com readback. Não duplicar operações, motores, fichas ou regras.

**LAST-VERIFIED-UNIT proposta:** R214 após readback da Biblioteca; enquanto não ocorrer, R214 é auditoria local concluída e publicação pendente.
