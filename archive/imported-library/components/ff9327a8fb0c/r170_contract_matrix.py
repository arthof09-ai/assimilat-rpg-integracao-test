"""R170 append-only original 17 contract matrix lineage. Never change historical requirements or certification count."""
import json,copy,hashlib
from pathlib import Path
H=Path(__file__).parent
R160=Path('/mnt/data/vlab_r161_work/baseline_r160/r151_r160/R160_17_CONTRACTS_BEFORE_AFTER.json')
z=json.loads(R160.read_text());assert z['original_denominator']==len(z['rows'])==17 and z['after_terminal']==0
exec_info={
 'ACTION_CATALOG_AIN01':('R165 Iskiel Flecha de Trava source attack 55PA, real damage and explicit temporal slow; R166 Casulo CA and displacement -4m both applied.', 'No complete catalogue, typed multi-component effects, range/saves universally supported; still 0 terminal.'),
 'ACTOR_SNAPSHOT_SCENARIO':('New documented Auren,Crocodilo,Iskiel,Eristan,Feryn,Varok source bindings in 5 independent physical scenes; R167 candidate gates.', 'No canonical actor snapshot freeze, missing Beast Initiative and second ED.'),
 'AUTHORITATIVE_RULES_AND_ADAPTERS':('R165 exact Iskiel temporal end of next target turn source and test; R164/R167 source-authority search and HOLD exacts.', 'Casulo 2 turn ending; Beast natural initiative; Lightning RD; two-turn time norm; transform conflict.'),
 'BATTLE_1X1_2X1_20X20':('R168 2 source-conditional complete Crocodilo L3 vs Auren L3 bouts, 198 native R18 commits each, winner Auren HP523.', 'No source-complete special-repertoire Beast initiative nor ED duo or official 20x20 full battles.'),
 'BLEED_AND_HEAL_RESTRICTIONS':('R161 corrected HP-effective receipts 154/154, and R162 prospective classifier prevents overkill counted as Life lost.', 'Not a new cure/bleed mechanic; requires authorized bleeding actor/equipped ability and cure interplay.'),
 'ED_VS_BE_DAMAGE':('R168 different species Crocodilo L3 versus Auren L3 physical-only, 2 full 66-turn fights, cold audit 396/396.', 'Natural Beast Initiative absent; no special attacks, elemental RDs, rank table admission or official cell.'),
 'GENERAL_SPECIFIC_RD':('R161/R162 distinguishes post RD 11870, actual Life 11808, overkill 62 and restores three receipts, R169 additional overkills.', 'General/specific stacking, Dark actual attack and separated mixed damage still HOLD; receipt arithmetic is not resistance-rule approval.'),
 'ITEM_EQUIPMENT_AND_ENHANCEMENTS':('No new activation/deactivation proof; R166 Eristan equipped snapshot and PA804 carried unchanged except Casulo60.', 'Full equipment charge snapshot, deactivation, bonded PA and effect removal tests still pending.'),
 'OFFICIAL_QA_NAC_LEDGERS':('R161 466 original R18 commits reconciled without edits; R165/R166/R168 413 new; R169 two semantically forged-but-hashed DB copies rejected.', 'Official QA writer, external auditor independent certification, NAC-PASS-02 still HOLD.'),
 'PA_AND_PREBUFF_COSTS':('R165 Flecha 55PA source-paid, slows target and expires on explicit boundary; R166 Casulo 60PA charged once with measured speed/CA.', 'Casulo exact expiration and other maintenance/prebuff/source timing across full fight still HOLD.'),
 'REACTION_TRIGGER_AND_SINGLE_USE':('R166 two concurrent Opportunity slots sorted Feryn DES80 ahead Varok DES29; second reaction canceled after initial KO, surviving reaction preserved.', 'R43 same-DES die tie in current integration, nested interruptions beyond this prefix and source actor eligibility still open.'),
 'RNG_REPLAY_STATISTICS':('Five new selected DBs 413 commits cold-replayed; two semantic-forged copies rejected; R168 reserved nonblind seed honestly distinguished.', 'No independent blind holdout, no canonical RNG stream proof, n=2 cannot support general outcome distributions.'),
 'SOURCE_FREEZE_AND_RANK':('R164 source gate on Crocodilo distinct species, Grifo, Auren and original hierarchy; R167 second-ED disqualification traced.', 'Need true frozen source current snapshots, 27-level species progression, competent official admission and review.'),
 'TACTICAL_AI_AB_FAIRNESS':('R168 two complete 1x1 basic-policy wins with no deliberate action abstention, separate from R160 Grifo special contrast.', 'No A/B balanced full-policy comparison, independent blind seeds or matchup representativeness.'),
 'TRANSFORMATION_OVERLAY_AI08':('No new transform execution; source cost disagreement preserved in R164 gates.', 'Current source 100PA+15/turn vs L3 320PA conflict requires NAC-NORM resolution.'),
 'TRANSFORMATION_PER_SCENE_AI09':('No new transform execution, preserved source gate.', 'No source-complete transform action/PA/duration/rest/replay.'),
 'TURN_SCHEDULER_EVENT_SOURCING':('R165 documented Next-turn end of -6m effect changed physical movement and expired; R166 simultaneous AoOs+KO under one R18 transaction.', 'Casulo temporal HOLD, full source-legal initiative tie/complex interrupts, production writer and official QA.'),
}
rows=[]
for old in z['rows']:
 id=old['id'];new,remaining=exec_info[id];r=copy.deepcopy(old)
 r['ANTES_R160']=copy.deepcopy(old['DEPOIS_R160'])
 r['DEPOIS_R170']={'new_executed_or_investigated_evidence':new,'original_requirement_verbatim_unchanged':old['original_requirement_verbatim'],
   'new_functional_progress':id not in ('ITEM_EQUIPMENT_AND_ENHANCEMENTS','TRANSFORMATION_OVERLAY_AI08','TRANSFORMATION_PER_SCENE_AI09'),
   'remaining_after_R170':remaining,
   'independent_audit_scope':'R165/R166/R168 read-only stdlib replay, R161 old nine source receipts, R169 copied semantic tamper' if id not in ('TRANSFORMATION_OVERLAY_AI08','TRANSFORMATION_PER_SCENE_AI09') else 'no new execution; historical only',
   'NAC_PASS':'TECHNICAL_BOUNDED_ONLY_TERMINAL_HOLD','terminal_certified':False}
 rows.append(r)
out=copy.deepcopy(z)
out.update({'checkpoint':'R170','before_checkpoint':'R160','as_of':'2026-10-17','rows':rows,'before_terminal':0,'after_terminal':0,
            'new_selected_db_count':5,'new_selected_commits':413,'new_native_receipts':137,
            'independent_holdout_admitted':0,'official_power_coverage':{'numerator':0,'denominator':1875},
            'history_R160_matrix_sha256':hashlib.sha256(R160.read_bytes()).hexdigest(),'original_matrix_id_sequence':[x['id'] for x in rows],
            'source_freeze':'Notion source excerpts directly reopened, no full source hash/official freeze','terminal_count_denominator':17})
assert len(rows)==17 and [x['id'] for x in rows]==[x['id'] for x in z['rows']]
assert all(x['original_requirement_verbatim']==y['original_requirement_verbatim'] and x['source_R105_SHA256']==y['source_R105_SHA256'] for x,y in zip(rows,z['rows']))
(H/'R170_17_CONTRACTS_BEFORE_AFTER.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
md=['# R170 — Matriz individual de 17 contratos históricos','', '**OP-VLAB-FUSION-SANDBOX-01 · MESTRE-SIDE · R160 ANTES → R170 DEPOIS · 0/17 terminais.**','', 'Denominador, sequência e requisitos literais da matriz R160 preservados; nenhum PASS terminal inferido.','']
for x in rows:
 d=x['DEPOIS_R170'];b=x['ANTES_R160']
 md.extend([f"## {x['position']:02d} — {x['id']}", '', f"**Requisito original:** `{x['original_requirement_verbatim']}`",'', '**ANTES R160:** '+str(b.get('minimum_remaining','')),'','**EXECUÇÃO/INVESTIGAÇÃO NOVA:** '+d['new_executed_or_investigated_evidence'],'', '**RESTANTE:** '+d['remaining_after_R170'],'','**Auditoria:** '+d['independent_audit_scope'],'','**Gate:** `0/17 TERM` — PASS técnico restrito / homologação HOLD.',''])
(H/'R170_17_CONTRACTS_BEFORE_AFTER.md').write_text('\n'.join(md))
print('R170 matrix',len(rows),'sha',out['history_R160_matrix_sha256'])
