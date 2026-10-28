# VLAB R117 — 17 contratos originais | matriz ANTES/DEPOIS

**Controle:** R105 original imutável; R108–R117 overlay aditivo, 17/17 identificados e 0/17 terminais; evidência local MESTRE-SIDE sem writer.

**Nota:** R93/R95 preservados `TECHNICAL_REPLAY_PASS / NORMATIVE_PARITY_HOLD`. R112 6 SQLite novas auditadas; R109/R110 e R115-AFTER-INTENT em UNKNOWN-EFFECT HOLD; R111 policy drift excluído.

## 01. `ACTION_CATALOG_AIN01`
**Requisito original literal:** `REAL_SOURCE_LOADOUT_AND_FULL_EFFECT_COVERAGE + independent review + applicable NAC-PASS-02`
**ANTES (R107):** R103 6 recibos da Descarga Curta em adaptador aditivo fonte-limitado, NÃO prova menu v0.8.1.
**NOVA EVIDÊNCIA (R108–R117):** Descarga Curta via cast_source_specified_spell de v0.8.1 em quatro eventos de cenas integradas, 55PA cada
**BLOQUEIO ANTERIOR:** Native v0.8.1 SAVE-HALF explicitamente bloqueado; escolhas/efeitos/custos especiais incompletos.
**RESTANTE MÍNIMO:** Catálogo real de todas as ações, outros custos/efeitos, alcance normativo e SAVE-HALF ímpar. Catalogar Magia, Talão, Bico, Descarga, reação, prebuff e equipamento em catálogo com seleção autorizada; usar adaptador original com fontes congeladas.
**Gate de certificação terminal:** REAL_SOURCE_LOADOUT_AND_FULL_EFFECT_COVERAGE + independent review + applicable NAC-PASS-02 + auditor independente competente / NAC-PASS vigente. **Estado: HOLD, não certificado.**

## 02. `ACTOR_SNAPSHOT_SCENARIO`
**Requisito original literal:** `CURRENT_CANON_ACTOR_SNAPSHOTS_AND_SNAPSHOT_FREEZE + independent review + applicable NAC-PASS-02`
**ANTES (R107):** R103 15 genesis/SQLite isolados auditados, nenhuma ficha canônica escrita.
**NOVA EVIDÊNCIA (R108–R117):** Freeze de seis genêses baseados em fontes e readback de seis SQLite, mas PRECREATE != ficha canônica
**BLOQUEIO ANTERIOR:** VZ PRECREATE não materializado, perfil VLAB PAUSED e snapshots de personagens da campanha sem licença de escrita.
**RESTANTE MÍNIMO:** Materialidade e autorização de ficha real, snapshots de cenas integradas e estados transformados. Reabrir e congelar snapshots canônicos das identidades e diferentes estados, 14 gates conforme contrato, testar mutação/reabertura e isolamento de fonte.
**Gate de certificação terminal:** CURRENT_CANON_ACTOR_SNAPSHOTS_AND_SNAPSHOT_FREEZE + independent review + applicable NAC-PASS-02 + auditor independente competente / NAC-PASS vigente. **Estado: HOLD, não certificado.**

## 03. `AUTHORITATIVE_RULES_AND_ADAPTERS`
**Requisito original literal:** `AUTHORITATIVE_SOURCE_FREEZE_AND_CONFLICT_RESOLUTION + independent review + applicable NAC-PASS-02`
**ANTES (R107):** R102 4 ocorrências físicas espelhadas read-only discrepantes, 1 seed real; não alterar R95.
**NOVA EVIDÊNCIA (R108–R117):** Crítico R6 corrigido NO módulo original v0.8.1 copiado; Fraco R7 exato; diff reproduzível e 51 regressões
**BLOQUEIO ANTERIOR:** R95 usou +10 no crítico de 20d10 quando norma atual manda +200; FRACO/esforço final omitidos; v0.8.1 SAVE-HALF bloqueado.
**RESTANTE MÍNIMO:** Revisão independente de paridade integral, negativos de falha crítica, iniciativa natural, transformação e gate oficial. Comparar literalmente Sistema de Combate com implementações e reproduzir TODOS os divergentes; bloquear efeitos conflitantes.
**Gate de certificação terminal:** AUTHORITATIVE_SOURCE_FREEZE_AND_CONFLICT_RESOLUTION + independent review + applicable NAC-PASS-02 + auditor independente competente / NAC-PASS vigente. **Estado: HOLD, não certificado.**

## 04. `BATTLE_1X1_2X1_20X20`
**Requisito original literal:** `COMPLETE_SOURCE_LEGAL_FIGHT_1X1_TO_20X20 + independent review + applicable NAC-PASS-02`
**ANTES (R107):** Nenhum duelo antigo repetido; R103 apenas habilidade isolada.
**NOVA EVIDÊNCIA (R108–R117):** Quatro duelos source-bound 1×1 atualizados; R93 2×1 permanece histórico em HOLD normativo
**BLOQUEIO ANTERIOR:** 1x1 R95 com crítico divergente; 2x1 R93 NPC desigual; 20x20 não executado; políticas incompletas.
**RESTANTE MÍNIMO:** 2×1 novo corrigido com EDs comparáveis, scheduler/reação e escala progressiva 20×20. Admitir lutas completas 1x1, 2x1 e 20x20 com políticas legais, cenários fonte-autênticos, reações, custos, KO, replay.
**Gate de certificação terminal:** COMPLETE_SOURCE_LEGAL_FIGHT_1X1_TO_20X20 + independent review + applicable NAC-PASS-02 + auditor independente competente / NAC-PASS vigente. **Estado: HOLD, não certificado.**

## 05. `BLEED_AND_HEAL_RESTRICTIONS`
**Requisito original literal:** `BLEED_HEAL_SOURCE_AND_EFFECT_ADAPTER_INTEGRATION + independent review + applicable NAC-PASS-02`
**ANTES (R107):** Não se fabricou sangramento/cura.
**NOVA EVIDÊNCIA (R108–R117):** Nenhuma evidência nova aceita; não foi ativado em R112
**BLOQUEIO ANTERIOR:** Sem fonte competente para efeito de sangramento e cura com duração/limites completos no perfil selecionado.
**RESTANTE MÍNIMO:** Efetuar sangramento/cura real com custos, restrições, cancelamentos e recovery. Recuperar efeito físico real, cura/tick/duração/stacks, gates por fonte; executar testes de evento, expiração, negativos e recuperação.
**Gate de certificação terminal:** BLEED_HEAL_SOURCE_AND_EFFECT_ADAPTER_INTEGRATION + independent review + applicable NAC-PASS-02 + auditor independente competente / NAC-PASS vigente. **Estado: HOLD, não certificado.**

## 06. `ED_VS_BE_DAMAGE`
**Requisito original literal:** `REAL_ED_BE_EFFECTS_RANK_AND_SOURCE_FIXTURES + independent review + applicable NAC-PASS-02`
**ANTES (R107):** R102 isolou impacto bruto/pós-RD/realizado e corrigiu interpretação da assimetria.
**NOVA EVIDÊNCIA (R108–R117):** Grifo L3 × Auren L3 quatro cenas com 4 Descargas, 4 críticos naturais espelhados, 12 ataques Fraco
**BLOQUEIO ANTERIOR:** R95 crítica/Fraco divergence e source PRECREATE; fonte da real life/canon de VZ pendente; falta ampla diversidade.
**RESTANTE MÍNIMO:** Iniciativa legal Besta, transformação, reações e políticas completas; independência holdout em famílias. Nova comparação física ED x Besta sob regras completas com não acerto, mitigação, crítico, vários patamares e efeitos especiais.
**Gate de certificação terminal:** REAL_ED_BE_EFFECTS_RANK_AND_SOURCE_FIXTURES + independent review + applicable NAC-PASS-02 + auditor independente competente / NAC-PASS vigente. **Estado: HOLD, não certificado.**

## 07. `GENERAL_SPECIFIC_RD`
**Requisito original literal:** `RD_MULTI_TAG_STACKING_BYPASS_NORMATIVE_RULING + independent review + applicable NAC-PASS-02`
**ANTES (R107):** R103 tipo Lightning foi delimitado sem RD tipada de Lightning; não testa múltiplas tags.
**NOVA EVIDÊNCIA (R108–R117):** RD física existente v0.8.1 usada em ataques com crítico +200/+64 e overkill auditados
**BLOQUEIO ANTERIOR:** Regra normativa para empilhamento e bypass ainda HOLD; RD de Auren é físico/Dark tipado.
**RESTANTE MÍNIMO:** Interações RD específica Lightning, dupla resistência e efeitos de componente misto em fontes reais. Teste separadamente RD geral, específica, múltiplos tipos, maior/adição/empilhamento e bypass com autoridade documentada.
**Gate de certificação terminal:** RD_MULTI_TAG_STACKING_BYPASS_NORMATIVE_RULING + independent review + applicable NAC-PASS-02 + auditor independente competente / NAC-PASS vigente. **Estado: HOLD, não certificado.**

## 08. `ITEM_EQUIPMENT_AND_ENHANCEMENTS`
**Requisito original literal:** `CURRENT_EQUIPMENT_CHARGE_SNAPSHOTS + independent review + applicable NAC-PASS-02`
**ANTES (R107):** Auren forma equipada conhecida, prova de cobrança isolada é de habilidade do Grifo, não de item.
**NOVA EVIDÊNCIA (R108–R117):** Auren manteve bônus de título e equipamento já impressos, sem nova ativação de item
**BLOQUEIO ANTERIOR:** Snapshots completos de equip. e cobrança de PA de peças do cenário não testados; nenhum write em ficha.
**RESTANTE MÍNIMO:** Commit/rollback equipamento/ativação, modificadores e trocas autorizadas. Equipamento atual, ativação, compromissos de PA, charges, troca, duração, carga diária, perda/remoção e recuperação.
**Gate de certificação terminal:** CURRENT_EQUIPMENT_CHARGE_SNAPSHOTS + independent review + applicable NAC-PASS-02 + auditor independente competente / NAC-PASS vigente. **Estado: HOLD, não certificado.**

## 09. `OFFICIAL_QA_NAC_LEDGERS`
**Requisito original literal:** `B1_B2_B3_NAC_PASS_AND_OFFICIAL_LEDGER_GATE + independent review + applicable NAC-PASS-02`
**ANTES (R107):** R103 auditor frio local PASS, sem pretensão de QA oficial.
**NOVA EVIDÊNCIA (R108–R117):** Auditoria fria R113 + 51 regressões R114 + R115 fault; sem homologação independente competente
**BLOQUEIO ANTERIOR:** CM-000006 PAUSED; writer/lease/fencing/IBX-101 ACK ausentes; OFFICIAL_READBACK=0.
**RESTANTE MÍNIMO:** Independência do aceite terminal, escritor legítimo NAC-PASS competente. Provar B1/B2/B3, status do writer, fencing, ledger oficial, auditor externo e NAC-PASS terminal com readback.
**Gate de certificação terminal:** B1_B2_B3_NAC_PASS_AND_OFFICIAL_LEDGER_GATE + independent review + applicable NAC-PASS-02 + auditor independente competente / NAC-PASS vigente. **Estado: HOLD, não certificado.**

## 10. `PA_AND_PREBUFF_COSTS`
**Requisito original literal:** `CURRENT_PA_PREBUFF_COSTS_AND_TIMING_AUTHORITY + independent review + applicable NAC-PASS-02`
**ANTES (R107):** R103 6 eventos com -55 PA, standard1->0, 6 half ímpares HOLD sem pending, 3 negativas sem efeito.
**NOVA EVIDÊNCIA (R108–R117):** Quatro spells nativos em turnos, gasto agregado 220PA verificado causalmente, testes de insuficiência e segundo uso
**BLOQUEIO ANTERIOR:** v0.8.1 SAVE-HALF recusa; regra arredondamento ímpar ausente; lifecycle de buff/prebuff ainda não validado.
**RESTANTE MÍNIMO:** Prebuff, gastos condicionais, efeitos de duração, recuperação geral em fluxo real. Gasto PA positivo de fontes e prebuffs em transações indivisíveis, falta PA, rollback, timing, charges, custo em cada turno.
**Gate de certificação terminal:** CURRENT_PA_PREBUFF_COSTS_AND_TIMING_AUTHORITY + independent review + applicable NAC-PASS-02 + auditor independente competente / NAC-PASS vigente. **Estado: HOLD, não certificado.**

## 11. `REACTION_TRIGGER_AND_SINGLE_USE`
**Requisito original literal:** `MULTI_TRIGGER_INTERRUPTS_AND_NORMATIVE_PRECEDENCE + independent review + applicable NAC-PASS-02`
**ANTES (R107):** R71 mantém 10 AoO e 181 counters históricos, sem rerun.
**NOVA EVIDÊNCIA (R108–R117):** Sem nova janela de reação exercida; ataque e spell consomem ação padrão sem criação de slot
**BLOQUEIO ANTERIOR:** Prioridade concorrente/nested não adjudicada; nenhum gatilho novo pós-R71.
**RESTANTE MÍNIMO:** Trigger único, duplicidade, competição, interrupção no turno e recuperação em caminhos reais. Dois gatilhos mesmo turno, consumo único, janela/renovação, simultâneas, aninhadas, rollback e precedência documentada.
**Gate de certificação terminal:** MULTI_TRIGGER_INTERRUPTS_AND_NORMATIVE_PRECEDENCE + independent review + applicable NAC-PASS-02 + auditor independente competente / NAC-PASS vigente. **Estado: HOLD, não certificado.**

## 12. `RNG_REPLAY_STATISTICS`
**Requisito original literal:** `CANONICAL_DICE_SOURCE_AND_STATISTICAL_HOLDOUT + independent review + applicable NAC-PASS-02`
**ANTES (R107):** R102 recontou blocos independentes; R103 3 seeds em 6 ledgers causalmente frios; não são seis seeds.
**NOVA EVIDÊNCIA (R108–R117):** R113 auditor frio independente 6/6, 3 seeds numéricas, espelhos pareados, 2 cortes adversariais
**BLOQUEIO ANTERIOR:** 2 seeds R95, 3 seeds R103 e espelhos não fornecem validação independente de famílias nem RNG de rolagem oficial.
**RESTANTE MÍNIMO:** Holdout realmente cego entre famílias, amostra suficiente e validação terminal RNG. Source-canonical RNG, seed freeze, pares lado, replays completos, estatística pré-registrada, holdout independente cego por famílias.
**Gate de certificação terminal:** CANONICAL_DICE_SOURCE_AND_STATISTICAL_HOLDOUT + independent review + applicable NAC-PASS-02 + auditor independente competente / NAC-PASS vigente. **Estado: HOLD, não certificado.**

## 13. `SOURCE_FREEZE_AND_RANK`
**Requisito original literal:** `REAL_BESTIARY_RANK_SNAPSHOTS_14_ACTOR_GATES + independent review + applicable NAC-PASS-02`
**ANTES (R107):** R104 derivação de Grifo L2, 7 candidatas agrupadas em 4 patamares, sem promoção.
**NOVA EVIDÊNCIA (R108–R117):** Provas fonte Notion R108, ID original e classificação Besta L3/Titã, Grifo L2 derivado preservado
**BLOQUEIO ANTERIOR:** BEAST-FULLSPEC=suporte PRECREATE VZ, 0/14 físicos no HANDOFF; sem equivalência automática às fichas principais.
**RESTANTE MÍNIMO:** Fontes materiais, fingerprint oficial de cada entidade, 27 potências homologadas. Congelar identidades/versionamento e pelo menos 14 gateways de atores fontes canônicas, rank/estrela/27 patamares de potência.
**Gate de certificação terminal:** REAL_BESTIARY_RANK_SNAPSHOTS_14_ACTOR_GATES + independent review + applicable NAC-PASS-02 + auditor independente competente / NAC-PASS vigente. **Estado: HOLD, não certificado.**

## 14. `TACTICAL_AI_AB_FAIRNESS`
**Requisito original literal:** `OBSERVABLE_TACTICAL_POLICY_FAIRNESS_BLIND_AUDIT + independent review + applicable NAC-PASS-02`
**ANTES (R107):** Nenhuma vitória do Auren foi creditada como sinergia coletiva.
**NOVA EVIDÊNCIA (R108–R117):** Espelhos exógenos B/E registrados, política especial abertura única reparada
**BLOQUEIO ANTERIOR:** R93 2x1 targeting fixo, sem sinergia de papéis; fonte de equipe equilibrada não formada.
**RESTANTE MÍNIMO:** Política tática fundamentada, alvos móveis/equipes balanceadas e comparação A/B cega. Duas políticas legítimas A/B blindadas, targeting, movimento, controle, recursos, contrajogo e equidade verificada independentemente.
**Gate de certificação terminal:** OBSERVABLE_TACTICAL_POLICY_FAIRNESS_BLIND_AUDIT + independent review + applicable NAC-PASS-02 + auditor independente competente / NAC-PASS vigente. **Estado: HOLD, não certificado.**

## 15. `TRANSFORMATION_OVERLAY_AI08`
**Requisito original literal:** `CURRENT_TRANSFORMATION_SOURCE_AND_FULL_DURATION + independent review + applicable NAC-PASS-02`
**ANTES (R107):** Auditoria documental registra o conflito, 0 transformações novas.
**NOVA EVIDÊNCIA (R108–R117):** Conflito custo Auren 100+15 vs regra especializada 320 confirmado; nenhuma ativação
**BLOQUEIO ANTERIOR:** Auren fonte individual descreve ativação 100PA/15 por turno, Sistema de Combate Lendário 320PA; resolver precedência antes de executar.
**RESTANTE MÍNIMO:** Resolver autoridade específica, transformado íntegro com duração e recursos. Usar Espírito compatível/overlay materializado, ficha transformada, fórmulas derivadas, PA, duração, dispel, regressão.
**Gate de certificação terminal:** CURRENT_TRANSFORMATION_SOURCE_AND_FULL_DURATION + independent review + applicable NAC-PASS-02 + auditor independente competente / NAC-PASS vigente. **Estado: HOLD, não certificado.**

## 16. `TRANSFORMATION_PER_SCENE_AI09`
**Requisito original literal:** `REAL_SCENE_REST_BOUNDARY_AND_GATE_AUTHORITY + independent review + applicable NAC-PASS-02`
**ANTES (R107):** Nenhum contador de cena inventado.
**NOVA EVIDÊNCIA (R108–R117):** Sem evidência nova; bloqueio de transformação Auren preservado
**BLOQUEIO ANTERIOR:** Falta fonte dos limites por cena e paridade v0.9 genuína; nenhuma ativação legítima executada.
**RESTANTE MÍNIMO:** Ativação por cena, T9 limites e reuso/recarga auditados. Provar limites por cena, gasto e renovação/rest/cooldown, reentrância, salvamento/recovery, fonte genuína v0.9.
**Gate de certificação terminal:** REAL_SCENE_REST_BOUNDARY_AND_GATE_AUTHORITY + independent review + applicable NAC-PASS-02 + auditor independente competente / NAC-PASS vigente. **Estado: HOLD, não certificado.**

## 17. `TURN_SCHEDULER_EVENT_SOURCING`
**Requisito original literal:** `CANON_INITIATIVE_TIE_INTERRUPTION_AND_SOURCE_COMPLETE_EVENTS + independent review + applicable NAC-PASS-02`
**ANTES (R107):** R104 demonstrou intervalo matemático sem atribuir proficiência à Besta; R103 ação isolada não comprova scheduler.
**NOVA EVIDÊNCIA (R108–R117):** Turnos R112 com 212 turn starts e 212 ends, 636 eventos, 2 testes de falha atômica
**BLOQUEIO ANTERIOR:** Competência de Iniciativa do Grifo/Croc não publicada; R95 exógena, R93 usa hipótese de iniciativa; v0.9 parity/rewind não certificada.
**RESTANTE MÍNIMO:** Iniciativa natural, 3 atores simultâneos, reação, scheduler de equipe, recuperação ampla. Iniciativa natural real, tie, turnos 3+ e 20x20, interrupção, KO, reação/ressuprimento, snapshots e recuperação causal.
**Gate de certificação terminal:** CANON_INITIATIVE_TIE_INTERRUPTION_AND_SOURCE_COMPLETE_EVENTS + independent review + applicable NAC-PASS-02 + auditor independente competente / NAC-PASS vigente. **Estado: HOLD, não certificado.**

