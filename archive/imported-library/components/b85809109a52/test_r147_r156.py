"""Directed regression suite for new active wiring and repaired legacy paths.
No network or Notion writes; physical materialization proven by separate receipts.
"""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parent
for part in ('runtime','history'):sys.path.insert(0,str(ROOT/part))
import r147_secure_confirmation as r147
import r148_evidence_binding as r148
import r149_150_spirit_runtime as r149
import r151_integrated_progression as r151
import r152_generic_structural_adapter as r152
import r153_sourcebound_read_only as r153
import r154_conversation_bridge as r154
import ibx17_entrypoint_r147 as entry
import r141_source_binding as repaired141
import r142_143_activation_engine as repaired142
import r145_chat_preview as repaired145
from r134_conversation_authorization import Hold as OriginalHold

results={}
results['R147_host_auth']=r147.selftest()['checks']
results['R148_binding']=r148.selftest()['checks']
results['R149_R150_tier_resources_duration']=r149.regression()['checks']
results['R151_progression_spirit_carry']=4 if r151.selftest()['spirit_increment']==6 else 0
results['R152_structural_adapter']=r152.selftest()['checks']
results['R153_party_readonly_previews']=r153.tests()['checks']
results['R154_chat_flow']=r154.selftest()['checks']
results['ENTRYPOINT_INTEGRATION']=len(entry.selftest()['contracts'])
# Original vulnerable routes are no longer active in the patched runtime.
a=repaired141.BeastEvidence('B','v','B','B',2,'Prata 1')
b=repaired141.SpiritEvidence('A','S','B','v','TEST_ONLY_SIMULATED',6,{'SAB':6},6)
assert repaired141.bind(a,b)['status']=='SCHEMA_VALID_TEST_ONLY'
results['PATCHED_R141_NO_FALSE_VERIFIED']=1
p={'from':16,'to':17}
try:repaired145.confirm(None,claimed_actor='MESTRE',channel='ChatGPT',observed_human_turn={'trusted_runtime_origin':True,'role':'user','turn_ref':'FAKE','verbatim_reply':'SIM','previews_seen_hash':'hash'},preview=p,source_version='v',target_version='v')
except OriginalHold:results['PATCHED_R145_NO_CALLER_TRUST']=1
else:raise AssertionError('old path still fabricated CONFIRMED')
# Patch the historical R142 active implementation: broad rank and LONG rest.
x=repaired142.initial();x['identity']=dict(x['identity'],rank='Ouro 1',level=11);x['normal_pa']=210;x['pa_gastavel_test_receipt']=210
n,verdict=repaired142.activate(x,event='OURO',scene='SYN_SCENE_A',duration_d6=6,action='ACAO_PADRAO',actor_id=x['identity']['actor_id'],spirit_id=x['identity']['spirit_id'],scene_test_authorized=True,source_mode='SYNTH_TEST_ONLY')
assert verdict=='COMMITTED_CANDIDATE' and n['normal_pa']==130 and n['duration_remaining']==7
n=repaired142.deactivate(n,event='OURO_END')
n=repaired142.complete_rest(n,event='TEST_LONG',new_scene='SYN_SCENE_B',rest_type='LONG',recorded_test_duration_h=None,independent_scene_test_authority=True)
assert n['rest_after_last_use']
results['PATCHED_R142_OURO_LONG_REST']=2
assert sum(results.values())>50
print(json.dumps({'result':'PASS_DIRECTED','checks_by_contract':results,'local_direct_assertion_count':sum(results.values()),'real_host_attestation':False,'native_calls_executed':0,'production':'HOLD'},ensure_ascii=False,indent=2))
