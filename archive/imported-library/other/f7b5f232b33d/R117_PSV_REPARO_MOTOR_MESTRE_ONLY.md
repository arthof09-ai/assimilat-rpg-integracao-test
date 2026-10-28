# PSV — VLAB R108–R117 / reparo normativo funcional v0.8.1

**AS-OF:** 2026-10-16 · **OPERATION:** CM-000006 / OP-VLAB-FUSION-SANDBOX-01 · **AMBIENTE:** MESTRE-SIDE
**BASELINE:** R01–R107 intacta (incluindo todos os incidentes UNKNOWN-EFFECT e R93/R95). **CONCLUSÃO:** checkpoint local de sandbox, NÃO certificação terminal.

## ANTES → DEPOIS

| Pendência herdada | Evidência R107 | Nova evidência R108–R117 | Status | Restante mínimo |
|---|---|---|---|---|
| Crítico incorreto no adaptador R93/R95 | 20 fórmulas aritméticas isoladas; seis recibos errados | Reparo **dentro de `vlab_effects_v08.py`**, único arquivo alterado em cópia de v0.8.1, SHA `ea998d23b5de67169e3ab9b6d9f68ec7588145722cd80aee69379566d1a06904`; fórmula `dados_normais + bônus_fixo + Σ(n×face)`; 28 legados + 23 novos PASS; 6 bancos completos auditados | PASS LOCAL/COPY | Gate de promoção independente, regressão ampla e fonte de falha crítica |
| Fraco | Ausência em combates anteriores | Entrada/saída estrita HP <10%; 16 ataques com desvantagem auditados, velocidade à metade | PASS LOCAL/COPY | Reações, ataques multi-ação, recuperação de cura e condições compostas |
| Esforço final opcional Besta Ouro+ | Sem transação completa | 2 cenas técnicas dirigidas sob HP inicial condicionado; opção, máximo de dados, bloqueio de repetição e imobilidade próxima ação própria | PARCIAL CONDICIONAL | Falta definir precedência em erro de ataque e sobreposição com crítico natural |
| Descarga Curta em motor | R103 seis casos adaptador, SAVE-HALF nativo bloqueado | 4 transações dentro do `cast_source_specified_spell` preexistente + R18 SQLite, custo 220 PA global, Reflexo CD94 e 14d10 meio dano PAR; 9 pré-rejeições | PASS INTEGRADO LOCAL, NÃO PRODUÇÃO | Arredondamento ímpar, alcance em metros e RD Lightning fonte específica |
| Iniciativa natural Besta | abertura exógena R95 | nenhuma promoção: fonte diz prof +22 por classe mas não elegibilidade para Iniciativa | HOLD específico | competência individual Iniciativa/documento competente |
| Transformação Auren | conflito ficha custo100+15/turno vs especializada320 | conflito mantido e especializado lido, **nenhuma ativação simulada** | HOLD específico | reconciliação NAC-NORM e snapshot da forma |
| 17 contratos | 0/17 terminal | 17/17 overlay individual R117 com evidência funcional adicional e gate intacto | 0/17 terminal | provas originais faltantes + NAC-PASS competente |
| Quatro baterias A-D | 0 oficiais | R112 amplia cenário A/D L3 e B herança Grifo L2 deriva; sem B/D homologadas nem equipe nova comparável | experimentais | grades 25/27/25/27 completas com evidência suficiente |

## Recibos novos aceitos

- R112 4 duelos L3 Grifo vs Auren, duas seeds numéricas 915133 (dirigida desenvolvimento) e 920801 (pré-congelada, sem cegamento), com lados espelhados. Abrem com Grifo por condição exógena; usam ataques normais, Auren +8 após dois turnos, custo de habilidade 55 PA em abertura, condição Fraco, histórico de críticos e RD. Todos os quatro concluem vitória Auren **sob esta condição**.
- R111-F-EFFORT 2 ensaios técnicos (uma seed919982 + dois lados espelhados) Grifo L3 ferido artificialmente versus NPC Feryn ON5 não ED; sem prova de equipe ou potência.
- Soma selecionada 6/6 bancos auditados, 636 eventos, 208 ataques normais, 4 habilidades, 16 ataques sob Fraco, 6 críticos positivos reportados (contagem por execução, espelhada), 2 esforços finais opcionais, PA220, 212 inícios/terminações de turnos. 3 seeds numéricas em dois cenários. Não tratar 6 como observações independentes.
- `R113_COLD_CAUSAL_AUDIT.json` valida causalidade evento a evento, RNG, recursos, dano/mitigação, checkpoint, reabertura e hash por implementação SEM importar o executor reparado. `R115_FAULT_RECOVERY.json` dois cortes de processo após intenção/commit, com semântica UNKNOWN_EFFECT preservada.

## Quarentena, NO-REPEAT e incidentes

- Original R01–R107 não foi modificado/reexecutado para inflar denominador; R93/R95 continuam `TECHNICAL_REPLAY_PASS / NORMATIVE_PARITY_HOLD`. Nenhum valor contrafactual reivindicado como dano histórico.
- `R109_UNKNOWN_EFFECT_HOLD.json`: intenção durável com erro de resolução; NÃO RETRY. `R110_UNKNOWN_EFFECT_HOLD.json`: falha crítica consequência desconhecida após intenção; NÃO RETRY. `R111_POLICY_DRIFT_HOLD.json`: 4 duelos R111-FULL (mais seus checkpoints) repetiram habilidade, excluídos cientificamente, bases preservadas.
- `R115_FAULT_AFTER_INTENT_931001.sqlite` deliberadamente tem intenção pendente; nenhuma tentativa de recuperar/reaplicar; `AFTER_COMMIT_931002` recuperado exatamente com um dano e sem repetição.
- Contrato técnico **não certifica** regra completa de Crítico/Esforço: críticas negativas têm consequência não especificada, comando pré-rejeitado antes de intenção. Tempo de imobilidade: uma ação de movimento da próxima rodada própria bloqueada, não universalized.

## Denominadores preservados

- Contratos 17/17 rastreados, **0/17 certificados**; benchmark oficial **0/1875**; A=25, B=27, C=25, D=27 posições; nenhuma promovida.
- R101 24/24 lab tecnicamente auditados, preservados e NÃO repetidos; R107 15/15 +20/20 unitários mantidos por arquivo prévio, não contados como novas execuções.
- R108–R117 selected 6 bancos /3 seed numeric/2 cenários, 51 regressões (28 antigas +23 adicionais), 9 pré-rejeições, 2 testes de falha em processo.

## Autoridade, writer e NAC-PASS

**CM-000006:** PAUSED; INSTANCE-ID não reivindicado, IBX-101 ACK não realizado; writer/epoch/lease/fencing não obtidos. **NOTION OP, DIÁRIO, PARTY, O PRIMEIRO, FICHAS, DMG-RANK:** WRITE=0. Biblioteca MESTRE-SIDE isolada da OP original após verificação física. **NAC-PASS:** PASS LOCAL NO ESCOPO, terminal HOLD.

**LAST-VERIFIED-UNIT:** R116/R117 cold auditor + diff reproduzível + R115 fault tests + artefatos readback a constar em comprovante da entrega.
**FIRST-PENDING:** paridade de falha crítica e esforço em hit perdido, convenção meia-dano ímpar, proficiência de iniciativa Besta e transformação de Auren; integração reação + scheduler multiator; equipe comparável e 20×20.
**NO-REPEAT:** R59 e R72 original UNKNOWN, R81 14 históricos, R91 48 selecionados, R93/R95 24 históricos, R103 15 SQLite, R109/R110 pendentes, R111 policy drift, R115 AFTER_INTENT. Reabrir antes de qualquer novo comando.
**NEXT:** reconciliar gates normativos mínimos; estender integração v0.8.1 sem código concorrente; bateria de cena 3 atores com fonte ED comparável; revisar contratos individualmente; DMG ACK pela rota competente.
