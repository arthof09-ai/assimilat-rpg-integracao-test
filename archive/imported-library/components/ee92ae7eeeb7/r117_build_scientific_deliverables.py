"""Read-only summary and matrix overlay, no source mutation or historical re-execution."""
from pathlib import Path
import json,hashlib,sqlite3,csv,collections,datetime
R=Path(__file__).resolve().parent
BASE=R.parent/'r102_contract_audit'/'R105_ORIGINAL_17_CONTRACTS_MATRIX.json'
old=json.loads(BASE.read_text());audit=json.loads((R/'R113_COLD_CAUSAL_AUDIT.json').read_text());fault=json.loads((R/'R115_FAULT_RECOVERY.json').read_text());prev=json.loads((R/'R116_PROVENANCE_PREFLIGHT_AND_PATCH.json').read_text())
assert len(old['contracts'])==17 and audit['selected_runs']==6 and fault['status']=='PASS' and prev['status']=='PASS'
impacts={
 'AUTHORITATIVE_RULES_AND_ADAPTERS':('Crítico R6 corrigido NO módulo original v0.8.1 copiado; Fraco R7 exato; diff reproduzível e 51 regressões','Revisão independente de paridade integral, negativos de falha crítica, iniciativa natural, transformação e gate oficial'),
 'ACTION_CATALOG_AIN01':('Descarga Curta via cast_source_specified_spell de v0.8.1 em quatro eventos de cenas integradas, 55PA cada','Catálogo real de todas as ações, outros custos/efeitos, alcance normativo e SAVE-HALF ímpar'),
 'PA_AND_PREBUFF_COSTS':('Quatro spells nativos em turnos, gasto agregado 220PA verificado causalmente, testes de insuficiência e segundo uso','Prebuff, gastos condicionais, efeitos de duração, recuperação geral em fluxo real'),
 'ED_VS_BE_DAMAGE':('Grifo L3 × Auren L3 quatro cenas com 4 Descargas, 4 críticos naturais espelhados, 12 ataques Fraco','Iniciativa legal Besta, transformação, reações e políticas completas; independência holdout em famílias'),
 'GENERAL_SPECIFIC_RD':('RD física existente v0.8.1 usada em ataques com crítico +200/+64 e overkill auditados','Interações RD específica Lightning, dupla resistência e efeitos de componente misto em fontes reais'),
 'BATTLE_1X1_2X1_20X20':('Quatro duelos source-bound 1×1 atualizados; R93 2×1 permanece histórico em HOLD normativo','2×1 novo corrigido com EDs comparáveis, scheduler/reação e escala progressiva 20×20'),
 'REACTION_TRIGGER_AND_SINGLE_USE':('Sem nova janela de reação exercida; ataque e spell consomem ação padrão sem criação de slot','Trigger único, duplicidade, competição, interrupção no turno e recuperação em caminhos reais'),
 'TURN_SCHEDULER_EVENT_SOURCING':('Turnos R112 com 212 turn starts e 212 ends, 636 eventos, 2 testes de falha atômica','Iniciativa natural, 3 atores simultâneos, reação, scheduler de equipe, recuperação ampla'),
 'RNG_REPLAY_STATISTICS':('R113 auditor frio independente 6/6, 3 seeds numéricas, espelhos pareados, 2 cortes adversariais','Holdout realmente cego entre famílias, amostra suficiente e validação terminal RNG'),
 'ACTOR_SNAPSHOT_SCENARIO':('Freeze de seis genêses baseados em fontes e readback de seis SQLite, mas PRECREATE != ficha canônica','Materialidade e autorização de ficha real, snapshots de cenas integradas e estados transformados'),
 'BLEED_AND_HEAL_RESTRICTIONS':('Nenhuma evidência nova aceita; não foi ativado em R112','Efetuar sangramento/cura real com custos, restrições, cancelamentos e recovery'),
 'ITEM_EQUIPMENT_AND_ENHANCEMENTS':('Auren manteve bônus de título e equipamento já impressos, sem nova ativação de item','Commit/rollback equipamento/ativação, modificadores e trocas autorizadas'),
 'OFFICIAL_QA_NAC_LEDGERS':('Auditoria fria R113 + 51 regressões R114 + R115 fault; sem homologação independente competente','Independência do aceite terminal, escritor legítimo NAC-PASS competente'),
 'SOURCE_FREEZE_AND_RANK':('Provas fonte Notion R108, ID original e classificação Besta L3/Titã, Grifo L2 derivado preservado','Fontes materiais, fingerprint oficial de cada entidade, 27 potências homologadas'),
 'TACTICAL_AI_AB_FAIRNESS':('Espelhos exógenos B/E registrados, política especial abertura única reparada','Política tática fundamentada, alvos móveis/equipes balanceadas e comparação A/B cega'),
 'TRANSFORMATION_OVERLAY_AI08':('Conflito custo Auren 100+15 vs regra especializada 320 confirmado; nenhuma ativação','Resolver autoridade específica, transformado íntegro com duração e recursos'),
 'TRANSFORMATION_PER_SCENE_AI09':('Sem evidência nova; bloqueio de transformação Auren preservado','Ativação por cena, T9 limites e reuso/recarga auditados')
}
assert set(impacts)=={c['id'] for c in old['contracts']}
rows=[];lines=['# VLAB R117 — 17 contratos originais | matriz ANTES/DEPOIS','',
'**Controle:** R105 original imutável; R108–R117 overlay aditivo, 17/17 identificados e 0/17 terminais; evidência local MESTRE-SIDE sem writer.','',
'**Nota:** R93/R95 preservados `TECHNICAL_REPLAY_PASS / NORMATIVE_PARITY_HOLD`. R112 6 SQLite novas auditadas; R109/R110 e R115-AFTER-INTENT em UNKNOWN-EFFECT HOLD; R111 policy drift excluído.','']
for c in old['contracts']:
    cid=c['id'];delta,left=impacts[cid]
    row={'position':c['position'],'id':cid,'original_requirement_verbatim':c['original_requirement_verbatim'],
       'ANTES_R107':{'historical_evidence':{k:c.get(k) for k in ['R01_R17','R18_R49','R52_R61','R62_R71','R72_R81','R82_R91','R92_R101','R102_R105_new_evidence']},'blocker':c['blocker'],'tests_remaining':c['tests_remaining'],'status':'PARTIAL_OR_UNPROVEN'},
       'DEPOIS_R117':{'new_scoped_functional_evidence':delta,'still_missing':left,'certification_criterion_original':c['minimum_terminal_acceptance'],'NAC_PASS_terminal':'HOLD','certified_terminal':False},
       'source_R105_SHA256':hashlib.sha256(BASE.read_bytes()).hexdigest()}
    rows.append(row)
    lines.extend([f"## {c['position']:02d}. `{cid}`",f"**Requisito original literal:** `{c['original_requirement_verbatim']}`",f"**ANTES (R107):** {c['R102_R105_new_evidence']}",f"**NOVA EVIDÊNCIA (R108–R117):** {delta}",f"**BLOQUEIO ANTERIOR:** {c['blocker']}",f"**RESTANTE MÍNIMO:** {left}. {c['tests_remaining']}",f"**Gate de certificação terminal:** {c['minimum_terminal_acceptance']} + auditor independente competente / NAC-PASS vigente. **Estado: HOLD, não certificado.**",''])
res={'operation':'OP-VLAB-FUSION-SANDBOX-01','baseline':'R01–R107 IMUTÁVEL','AS_OF':'2026-10-16','original_R105_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'count_original':17,'count_terminal':0,'source_R105_original_ids_unchanged':True,'rows':rows,'writer':'CM-000006 PAUSED / NO_WRITER_NO_ACK'}
(R/'R117_17_CONTRACTS_BEFORE_AFTER.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
(R/'R117_17_CONTRACTS_BEFORE_AFTER.md').write_text('\n'.join(lines)+'\n')
# R112 + R111 directly link each event to source evidence, recorded seed, ledger, state and actual HP loss.
att=[];base_source={'B':'https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7','E':'https://app.notion.com/p/3ebc2b324ede814bb730d47dd7bd5f02','F':'https://app.notion.com/p/3f6c2b324ede81ce9c61db8127bf0e31'}
for x in audit['runs']:
    file=R/('r111_runs' if x['run_id'].startswith('R111') else 'r112_runs')/x['file']
    with sqlite3.connect(file) as db:
        event_rows=db.execute("SELECT row_json FROM events ORDER BY seq").fetchall()
    for raw, in event_rows:
        ev=json.loads(raw);k=ev['kind'];
        if k not in ['NATIVE_ATTACK','NATIVE_SPECIAL']:continue
        e=ev['detail']['native_action'];p=ev['payload'];actor=p['actor'];target=p['target']
        if k=='NATIVE_ATTACK':
            raw_amount=e['raw'];actual=e['hp_loss_actual'];net=e['net'];overkill=e['overkill'];normal=e['normal_damage'];crit=e['critical'];max_bonus=e['critical_max_bonus'];rd=e['rd_applied'];weak=e['weak_attacker'];pa=0
        else:
            raw_amount=e['raw'];net=e['effective'];actual=min(e['hp_before'],net);overkill=max(0,net-e['hp_before']);normal=sum(p['damage_rolls']);crit='N/A_SPELL';max_bonus=0;rd=e['rd_applied'];weak=False;pa=55
        att.append({'run_id':x['run_id'],'ledger_file':x['file'],'seed':x['seed'],'side':x['side'],'experiment_type':'GRIFO_VS_AUREN_BASIC_PLUS_ONE_SOURCE_SKILL' if 'G_FULL' in x['run_id'] else 'INJURED_GRIFO_VS_FERYN_FINAL_EFFORT_TECHNICAL','event_seq':ev['seq'],'event_kind':k,'source_actor':base_source[actor],'source_target':base_source[target],'actor_id':actor,'target_id':target,'attack_common_or_special':'SPECIAL_SAVE' if k=='NATIVE_SPECIAL' else 'NATIVE_WEAPON','critical_status':crit,'critical_bonus_corrected':max_bonus,'normal_damage_rolled':normal,'actual_raw_after_crit_and_save':raw_amount,'RD_applied':rd,'potential_after_RD':net,'actual_HP_taken':actual,'overkill':overkill,'weak_attacker':weak,'final_effort_option':bool(e.get('final_effort',False)),'pa_spent':pa,'before_HP_target':e.get('before_hp',e.get('hp_before')),'after_HP_target':e.get('after_hp',e.get('hp_after')),'event_command_id':ev['cmd_id'],'event_row_sha256':hashlib.sha256(json.dumps(ev,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'statistical_unit':'SEED_BY_SCENE_NO_MIRROR_AS_INDEPENDENT','classification':'LAB_NATIVE_V081_CONTROLLED_COPY_ONLY','terminal':False})
assert len(att)==212,len(att)
with (R/'R116_DMG_NATIVE_RECEIPTS_212.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,att[0].keys());w.writeheader();w.writerows(att)
# Consolidate false claims and uncertainties.
handoff='''# VLAB → DMG — handoff científico NÃO ACK / somente suporte Mestre-side

Operações: `OP-VLAB-FUSION-SANDBOX-01` → operação DMG existente `OP-DMG-CORPUS-EMP-01`. **Nenhuma escrita na OP DMG; material na Biblioteca VLAB para roteamento competente, NÃO RECEBIDO/ACEITO oficialmente.**

## Recebimento anterior e errata
- Histórico R97 **1.344 recibos** originais em `R97_ATTACK_RECEIPTS_1344_FOR_DMG.csv` dentro do ZIP R101 guardado na cadeia de arquivos R107; não importar como 1.344 observações independentes.
- R93 e R95: **seis eventos de crítico** históricos com bônus incorreto +face máxima, não soma dos máximos. Classificar `TECHNICAL_REPLAY_PASS / NORMATIVE_PARITY_HOLD`; não reescrever valores contrafactuais como ocorridos. A errata está em `R102_R93_R95_CRITICAL_PARITY_ERRATA.json` preservada no R107 embutido.
- R101 e R107 antigos permanecem intactos, sem mistura automática com a nova ciência.

## Nova evidência R112 + R111 esforço
- `R116_DMG_NATIVE_RECEIPTS_212.csv`: **212 eventos ofensivos**, sendo **208 ataques físicos** e **4 Descargas Curtas** com PA55, em **6 SQLite verificados** e dois cenários distintos. Unidade: bloco cena × seed, lados espelhados correlacionados; 915133 development seed selecionada, 920801 holdout predefinido (não prova cegamento independente), 919982 seed técnica dirigida de esforço final. **6 críticos positivos** contam também espelhos, não seis seeds independentes.
- `R113_COLD_CAUSAL_AUDIT.json` audita 636 eventos e recursos/causalidade sem importar o motor.
- Dano físico: bruto normal rolagem + bônus fixo, máximo de todos os dados somado em crítico, RD específica apenas se fonte. Lightning especial: 14d10, Reflexo CD94 com meia-dano **par**, RD0 específico somente porque ausente fonte de RD Lightning em Auren; suposição experimental condicional que impede promoção universal.
- Ataques de combatente fraco: desvantagem duas rolagens e −2, menor velocidade. Esforço final demonstrado em condição artificial Grifo já ferido versus Feryn NPC ON5 (não ED, não equipe equilibrada).
- Não há batalha live, nem iniciativa natural Besta, nem transformação Auren, nem fonte de arredondamento meio-dano ímpar; exemplos não homologados.
- Overkill > HP fica em campo separado; não somar vida subtraída com dano pós-RD como se fossem iguais.

## Entregáveis e admissibilidade
DMG deve cruzar RUN-ID, fonte Notion, hash ZIP, SQLite original, comando, seed, lado, condição inicial, critical sequence, dado de dano, tipo, RD aplicada, HP efetiva, overkill, PA, censura e estado do auditor. Separar R97 (HOLD de crítico) de R112 (subset controlado; mecanismo corrigido) e R111 esforço artificial. Não se atribuem estimativas universais.

**Status de roteamento:** `PREPARED_IN_VLAB_LIBRARY / NOT_ACKNOWLEDGED_BY_DMG / NO_CROSS_OPERATION_WRITE`.
'''
(R/'R116_DMG_HANDOFF_R97_R112.md').write_text(handoff)
# Persistent PSV
psv=f'''# PSV — VLAB R108–R117 / reparo normativo funcional v0.8.1

**AS-OF:** 2026-10-16 · **OPERATION:** CM-000006 / OP-VLAB-FUSION-SANDBOX-01 · **AMBIENTE:** MESTRE-SIDE
**BASELINE:** R01–R107 intacta (incluindo todos os incidentes UNKNOWN-EFFECT e R93/R95). **CONCLUSÃO:** checkpoint local de sandbox, NÃO certificação terminal.

## ANTES → DEPOIS

| Pendência herdada | Evidência R107 | Nova evidência R108–R117 | Status | Restante mínimo |
|---|---|---|---|---|
| Crítico incorreto no adaptador R93/R95 | 20 fórmulas aritméticas isoladas; seis recibos errados | Reparo **dentro de `vlab_effects_v08.py`**, único arquivo alterado em cópia de v0.8.1, SHA `{prev['corrected_sha256']}`; fórmula `dados_normais + bônus_fixo + Σ(n×face)`; 28 legados + 23 novos PASS; 6 bancos completos auditados | PASS LOCAL/COPY | Gate de promoção independente, regressão ampla e fonte de falha crítica |
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
'''
(R/'R117_PSV_REPARO_MOTOR_MESTRE_ONLY.md').write_text(psv)
# summary compact
summary={'operation':'OP-VLAB-FUSION-SANDBOX-01','baseline':'R01–R107','selected_ledger':6,'events':636,'attack_events':208,'spell_events':4,'crit_plus_events':6,'weak_attacks':16,'efforts':2,'pa_spent':220,'independent_seed_values':[915133,919982,920801],'mirror_not_independent':True,'fault_tests':2,'new_negative_preflight':9,'legacy_unittests':28,'new_native_unittests':23,'terminals':0,'official_cells':0,'receipts_csv_rows':len(att),'local_competent_engine':'v0.8.1 effects v08 source copy with Stage12 R18 SQLite commit bridge','restriction':'No full source official or canonical promotion'}
(R/'R117_SCIENCE_SUMMARY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
