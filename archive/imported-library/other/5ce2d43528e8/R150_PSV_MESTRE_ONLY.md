# PSV — VLAB / R138–R150 | integração temporal, corrigendum espacial e continuidade

**AS-OF:** 16/10/2026, Recife · **OPERATION:** `CM-000006 / OP-VLAB-FUSION-SANDBOX-01` · **MESTRE-SIDE** · **BASELINE:** R01–R137 preservada; R138–R145 também preservados e reclassificados somente por novo adendo · **LAST-VERIFIED-UNIT:** R150 após readback frio e publicação quando comprovados · **FIRST-PENDING:** causa normativa expiração Marca de três turnos, integração R42 crítico negativo LAB-ONLY, ataque Dark elegível, sangramento equipado real, primeira luta fonte-completa concluída.

## ANTES → execução → DEPOIS

**ANTES R137:** 3 cenas curtas/32 transações/170 PA; Capa, Marca, AoO, cura Eristan 79 efetiva. Banco R130 QA_FAIL (perda de speed) imutável; UNKNOWN_EFFECT R123/R134; escala R124 5×5 censurada. Contratos 0/17; 0/1875 referência oficial. Readback R137 teve **15/15 arquivos avulsos**, comprovante adicional recuperado posteriormente pela Coordenação (não 16/16 original).

**R138–R145 preservados fisicamente:** uma cena multirrodada com 3 atores, 4 rodadas, 40 eventos R18 e 43 subeventos, censo-horizonte sem vitória; cap-cura 96/14/82; seis rejeições pré-intent; dois redteams; crash recovery temporal antes/depois commit; 59/59 regressões no código v0.8.1. R138 havia passado em replays algébricos, mas **revisão mais estrita encontrou precondição espacial de Pulso com distância 2m referida ao instante errado**. R138 agora `TECHNICAL_REPLAY_PASS / SPATIAL_PARITY_HOLD`; o pacote histórico permanece intocado. Consultar `R150_R138_SPATIAL_PARITY_CORRIGENDUM.md`.

**R146 — correção discriminante, NÃO replay histórico:** novo RUN-ID `R146_MULTI_SOURCE_FERYN_ERISTAN_DEV_S995401` e seed995401 de DESENVOLVIMENTO (seed995402 reservada, não executada nem holdout). Ficha Auren ED L3 e propostas Mestre-side Feryn/Eristan ON5 (SEM Espíritos) em 4 rodadas; **40 commits**, **43 ações/subeventos nativos**, 12 turnos próprios, 2 ataques Padrão, 1 AoO, **659 PV de dano físico efetivo** (Feryn com RD física22), **371 PV de cura efetiva**, **430 PA consumidos** (F85/E345). Capa35, Marca25, Passo25, Reconstituição75 ×4, Pulso45 após AoO, luvas de Eristan20 uma vez em cada cura. Estados finais: Auren523PV/719PA; Feryn191PV/339PA; Eristan630PV/459PA. Fase `CENSORED_HORIZON`, sem vencedor; a política experimental faz Auren abdicar ações e não é tática competitiva. Geometria B0-B3 TOPOLÓGICA, com distância de cenário separada: Feryn-Eristan 3m **antes** da saída e 2m **depois**; Pulso acontece entre golpe e movimento. Sem movimento forçado nem AoO simultâneo.

**R147:** auditor escrito sem importar o resolvedor v0.8.1, R18 ou driver, recompõe dice SHA-RNG (experimental), 40 before/after hashes, ordem das ações, janelas, 43 subeventos, dano/PA/cura/luvas e estado final. `40/40 PASS`. Reações Capa e Pulso em turnos diferentes, slots exclusivos por personagem; renovação por início de turno. Não é holdout cego independente nem mecânica oficial de mundo.

**R148:** fonte pre-registrada confere Pulso exatamente a 3m antes do deslocamento e movimento para B2 após efeito; reconstroi **somente o prefixo rev20** a frio e o leitor original R18 reabre a cópia, sem reexecutar nenhum comando antigo. `COLD_RECONSTRUCTED_PREFIX_NOT_LIVE_SAVE`, não salva contemporânea. R149: cópia adversarial re-hasheada troca 3m→2m; o auditor fonte-independente rejeita antes de admitir paridade espacial. Original R146 não foi adulterado.

**R141–R144 histórico do pacote R145:** cura em Eristan cap Vida alvo479: 8d10+25+20 resultou bruto96 e efetivo14, excesso82; PA75 somente uma vez. Seis casos inválidos rejeitados antes da intenção sem escrever efeitos; duas falhas reais de processo com Passo25: após intenção revision0/pending1/PAs intactos, UNKNOWN_EFFECT_HOLD; após commit revision1 com PA debitado e fim de turno posterior em novos commits sem duplicação; auditor independente 2/2. Os dois redteams anteriores foram rejeitados mesmo com hash recalculado. Estes **não são combates adicionais nem seeds cegas**.

## Temporalidade, fonte e fronteiras

- `Passo da Fuligem`: fonte `ESTE TURNO` e custo25 PA Movimento. +12m no próprio turno, expirando `END` próprio. Movimentos em B0-B3 não são igualados a metros.
- `Marca dos Passos Perdidos`: custo25 PA Standard, +10 apenas Percepção/Sobrevivência, alvo visto a30m, duração literal `3 turnos`; guardou contagem de inícios de turno, mas **NÃO removeu** efeito nem presumiu marco exato. `HOLD_EXACT_3_TURNS` enquanto autoridade competente não esclarecer.
- `Reconstituição/Pulso` Eristan: aplicabilidade apenas a alvo vivo, não ressuscita, Eristan disponível, 5m/3m respectivamente, equipamento Luvas +20 por conjuração; comprometimento de PA dos itens **não recobrado** como ativação.
- Crítico negativo `1-1-1/1-1-2`: decisão expressa R42 LAB-ONLY reaberta na OP. Consequência experimental definida: erro auto, zero dano, Standard consumida, nenhum castigo inventado. Motor multirrodada R146 **ainda não incorpora** a bridge; caminho bloqueado antes da intenção. Não pedir decisão já existente; integração FIRST-PENDING.
- Auren RD Dark60 literal; nenhum ataque Dark fonte-equipada admissível nestes atores: `RD_DARK_INTEGRATED_HOLD`. RD física22 de Feryn aplicada. Dano misto sem separação autoritativa ou RD stacking `HOLD`.
- Sangramento histórico encontrado em acervo, mas não há portador/equipamento elegível congelado nos três atores: `SOURCE_HOLD`; cura não retira sangramento por inferência.
- Transformação Auren 100+15 PA/turno ficha versus 320 PA Lendário Sistema de Combate/Transformação: NAC-NORM-01 HOLD e nenhuma ativação nesta execução.

## Contra os 17 contratos e ciência de potência

A matriz R150 **preserva os 17 IDs originais**, requisitos e histórico anterior. Avanço de `ACTION_CATALOG_AIN01`, `BLEED_AND_HEAL_RESTRICTIONS`, `ITEM_EQUIPMENT_AND_ENHANCEMENTS`, `PA_AND_PREBUFF_COSTS`, `REACTION_TRIGGER_AND_SINGLE_USE`, `TURN_SCHEDULER_EVENT_SOURCING`, `RNG_REPLAY_STATISTICS` e `OFFICIAL_QA_NAC_LEDGERS` apenas em escopo experimental. Nenhum terminal. `GENERAL_SPECIFIC_RD` segue pendente para Dark/mistura; combate completo, transformação e QA terminal pendem requisitos históricos.

Quatro baterias A (25 ED), B (27 etapas mesma espécie Grifo), C (25 patamares de equipe), D (27 Bestas distintas; ADM26, Divina27): **0/1875 células oficiais**. R146 não é ED comparável em equipe nem ED×Besta; sua única seed e política de abdicação proíbem estimar vitória/potência. L2 Grifo permanece derivação da MESMA espécie, não nova Besta.

## DMG

Coorte R145 antiga R138 com 3 recibos = `SPATIAL_HOLD`, não elegível para benchmark; coorte R150 **R146_ONLY**, três novos recibos no mesmo combate censurado e UMA seed dev, ver CSV; não concatenar às coortes históricas R97(1344), R116(212), R125(165), R137(7) nem R138(3/HOLD). `HANDOFF PREPARED`, nenhum ACK do executor DMG, sem escrita nessa operação.

## Checkpoint/gates

**DENOMINADORES:** 17/17 contratos rastreados, **0/17 terminais**. R146: 1 cena selecionada e 1 seed (espelhamento zero), 4 rodadas/12 turnos, 40/40 commits, 3 ataques, 5 curas, PA430; R141 fixture cap separada (1), 6 rejeições; R143 falhas 2; R149 adulteração 1. R138 sem crédito de paridade espacial. **NO-REPEAT:** R01–R145 imutáveis, inclusive R123/R130/R134/5×5 R124, R143 intent pendente; não reexecutar R146/995401 ou reconstruir novamente prefixo no mesmo caminho.

**WRITER:** CM-000006 `PAUSED`, INSTÂNCIA/epoch/lease/fencing/ACK IBX-101 não comprovados; nenhuma escrita em OP, Diário, Party/O Primeiro, fichas/regras oficiais, DMG. **NAC-PASS:** PASS técnico delimitado para R146 com auditor independente e rollback/copy; gate terminal PRODUTIVO/HOMOLOGAÇÃO `HOLD`. Nunca transformar um benefício de teste em regra universal.

**NEXT-5:** 1) Aplicar R42 LAB-only crítico negativo na cópia v0.8.1 já corrigida e testar integrado com 2+ turnos; 2) obter fonte competente para fim de Marca ou continuar efeitos temporais de fim explícito; 3) curas e reações multiator com incapacitação real sem ressuscitar; 4) fonte Dark elegível e sangramento com portador real; 5) preparar cenários ED×Besta com snapshots completos e acordos materiais, manter handoff DMG em rota competente e certificação terminal original NAC-PASS-02 sob autoridade.

**TARGET REMAINDER:** 17 terminais pendentes; percentual global de cobertura de subcontratos `NÃO DETERMINÁVEL` pois o denominador de subprovas é diferente de 17 e não totalmente fechado.
