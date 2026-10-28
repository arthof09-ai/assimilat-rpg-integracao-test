"""R146 purely reproducible contract acceptance from recorded Notion readback results.
Readbacks are self-observed, NOT independent auditor evidence. This module does not fetch Notion.
"""
from __future__ import annotations
import json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
OBS={
 'op':{'id':'3f2c2b324ede81f48f80f6d27449d107','last_edited':'2026-10-17T12:06:07.962Z'},
 'r129':{'id':'3fcc2b324ede81a5b708f52d40671379','last_edited':'2026-10-17T11:04:15.043Z','groups_before':3,'groups_committed':0},
 'r130':{'id':'3fcc2b324ede81628c1ff89f4d0a8d90','last_edited':'2026-10-17T11:49:03.999Z','toggles_committed':2,'toggle_total':7,'D':'BEFORE_DISPATCHED'},
 'r131':{'id':'3fcc2b324ede81a19664e8d6ba2f8539','last_edited':'2026-10-17T11:48:45.020Z','same_key_duplicates':2,'errata_present':True},
 'r144_orig_blocked':{'id':'3fcc2b324ede8173a886f886be8926f7','last_edited':'2026-10-17T12:00:40.533Z','written_R144_fields':0,'root_history_consumed_R135':True},
 'r144_test':{'id':'3fcc2b324ede81868256e6db67ece28e','last_edited':'2026-10-17T12:04:36.271Z','stages_verified':3,'stages_expected':3,'level_from_to':[16,17],'HP_max_from_to':[292,309],'PA_max_from_to':[258,273],'current_HP':240,'current_PA':150,'FF':290,'table_rows_after':4,'child_count_after':1},
 'r144_child':{'id':'3fcc2b324ede816baed0f833958640ec','last_edited':'2026-10-17T12:03:53.143Z','legacy_preserved':True,'new_event_recorded':True},
 'r142_r143':{'id':'3fcc2b324ede811592f5f1f59bdb0e90','last_edited':'2026-10-17T11:56:35.431Z','stages_verified':6,'stages_total':6,'normal_hp':20,'normal_pa':30,'activation_scenes':['SCENE-TEST-A','SCENE-TEST-B'],'form_active':False,'synthetic_only':True},
 'r89_orig':{'id':'3fbc2b324ede81ddaa23de51b8d21c13','last_edited':'2026-10-16T18:34:36.884Z','untouched':True},
 'r145':{'id':'3fcc2b324ede81868256e6db67ece28e','source_version':'2026-10-17T12:04:36.271Z','preview_hash':'64f6db1fa69512cfd14ec24bccaeb86e7c109c517dedbd0e2e0498dec32c0e46','state':'AWAITING_CONFIRMATION','human_confirmation':False},
}
MATRIX=[
 {'R':'R137','prior':'R127 accepts repeated plain labels','new':'composite observation keys, duplicate conflict detector, errata R131 and R130 summary','evidence':'R131 and R130 physical reopens','status':'PASS_DOCUMENTARY_SELF'},
 {'R':'R138','prior':'unexplained native refusals','new':'separate security refusal from validation and successful writes, explicit NO-RETRY security policy','evidence':'R129/R130 before after refusal vs R135 successful','status':'PASS_REFUSAL_CLASSIFICATION_CAUSE_UNDISCLOSED'},
 {'R':'R139','prior':'rank engine math but 0 native rank complete','new':'safe diagnostic strategy; no renewed write because security refusal unresolved','evidence':'R129 0/3 PRE','status':'HOLD_NATIVE_SECURITY_REFUSAL'},
 {'R':'R140','prior':'B/C native done; D refused','new':'causal status clarified, no B/C repetition','evidence':'R130 B/C 2/7, D BEFORE','status':'HOLD_NATIVE_SECURITY_REFUSAL'},
 {'R':'R141','prior':'synthetic T6B no authentic creature binding','new':'beast-source identity + provenance + checksum validator, rooted crossname discrepancy surfaced','evidence':'source Lendario2 body Draconis despite Espectro da Morte grouping; audit precedent Nie Li','status':'PARTIAL_SOURCE_BOUND_HOLD'},
 {'R':'R142','prior':'activation guard and reserves local only','new':'native TEST Prata activation with 40PA and independent pools','evidence':'R142/R143 A journal + readback','status':'PASS_NATIVE_SYNTHETIC_TEST_ONLY'},
 {'R':'R143','prior':'no multi-scene native continuation','new':'synthetic damage, deactivate, short rest TEST, second activation in another scene, costs persist','evidence':'R142/R143 6/6 journals and stage receipts','status':'PASS_NATIVE_SYNTHETIC_TEST_ONLY'},
 {'R':'R144','prior':'R135 one root four spans, no child/table transaction','new':'R144 new TEST copy multi-region with table row and linked child, recovery after child write pre-journal','evidence':'R144 3/3 stages, original R89 untouched; earlier ambiguous R135 attempt quarantined','status':'PASS_NATIVE_STRUCTURAL_TEST_WITH_LIMITS'},
 {'R':'R145','prior':'R134 trust caller no observed human confirmation','new':'conversation-ready version+preview-hash bound fixture and proposal presented, no fabricated reply','evidence':'OP R145_PENDING and local state AWAITING','status':'HOLD_REAL_POST_PREVIEW_HUMAN_CONFIRMATION'},
 {'R':'R146','prior':'independent subsystems only','new':'single R144 structural level-up with title and equipment preserved + new row + child proof + recovery; broader R142/R143 separate test','evidence':'R144 readback and R143 readback, self-review','status':'PASS_TEST_INTEGRATION_PARTIAL_CERTIFICATION'},
]

def run():
 from r137_observation_ledger import main as ledger_tests
 from r138_native_refusal_triage import main as refusal_tests
 from r141_source_binding import main as beast_tests
 from r142_143_activation_engine import scenario
 from r144_structural_multiregion import test as structural_tests
 from r145_chat_preview import selftest as chat_tests
 ledger_tests();refusal_tests();beast_tests();scenario();structural_tests();chat_tests()
 assert OBS['r129']['groups_committed']==0 and OBS['r129']['groups_before']==3
 assert OBS['r130']['toggles_committed']==2 and OBS['r130']['D']=='BEFORE_DISPATCHED'
 assert OBS['r142_r143']['stages_verified']==OBS['r142_r143']['stages_total']==6
 assert OBS['r144_test']['stages_verified']==3 and OBS['r144_test']['child_count_after']==1
 assert OBS['r145']['state']=='AWAITING_CONFIRMATION' and OBS['r145']['human_confirmation'] is False
 assert len(MATRIX)==10
 assert not any('PROD_PASS' in x['status'] for x in MATRIX)
 assert OBS['r89_orig']['untouched'] and OBS['r144_child']['legacy_preserved']
 report={'status':'SELF_REVIEW_TEST_ONLY','observations':OBS,'contracts':MATRIX,'checks':8,
 'external_independent_auditor':'NOT_OBSERVED','production':'HOLD','global_percent':'NOT_DETERMINABLE'}
 (BASE/'evidence'/'R146_SELF_AUDIT_AND_CONTRACT_MATRIX.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
 return report
if __name__=='__main__':
 r=run();print(json.dumps({'contracts':len(r['contracts']),'local_audit_checks':r['checks'],'native_test':[x['R'] for x in r['contracts'] if 'PASS_NATIVE' in x['status']],'holds':[x['R'] for x in r['contracts'] if x['status'].startswith('HOLD')],'production':'HOLD'},ensure_ascii=False))
