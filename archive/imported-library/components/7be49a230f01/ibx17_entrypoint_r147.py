"""R147–R156 additive IBX-17 TEST entrypoint: replaces unsafe R134/R141/R142
routes without deleting historical code. Planner is pure; ONLY native connector
in MESTRE-SIDE outside Python may perform approved TEST writes after readback.
"""
from __future__ import annotations
import json
import r147_secure_confirmation as auth
import r148_evidence_binding as binding
import r149_150_spirit_runtime as spirit
import r151_integrated_progression as up
import r152_generic_structural_adapter as layout
import r153_sourcebound_read_only as sourcebound
import r154_conversation_bridge as chat

CONFIG={'operation':'LEVEL-UP-ENGINE/IBX-17','lab_parent':'3fbc2b324ede804a95fafcb7b293c92c','active_security_confirm':'r147_secure_confirmation (DENY absent host key)','active_spirit_binding':'r148_evidence_binding (DENY canonical from untrusted dict)','active_transform':'r149_150_spirit_runtime','active_level_spirit':'r151_integrated_progression','active_layout':'r152_generic_structural_adapter','active_party_adapter':'r153_sourcebound_read_only READ_ONLY','active_conversation':'r154_conversation_bridge','writes_permitted_in_script':0,'production':'HOLD'}

def inspect_text_command(text,*,target_id,parent_id,version,source_version):
 return chat.request(text,target_id=target_id,parent_id=parent_id,version=version,source_version=source_version,known_previews=[])

def preview_integrated_level(current_state,*,event,allocation):
 return up.preview(current_state,event=event,allocation=allocation)

def stage_layout_readonly(body,target,config,changes):
 return layout.prepare_write(target=target,body=body,config=config,changes=changes,expected_version=target.version,authorized=target.parent_id==CONFIG['lab_parent'])

def classify_native_status(*,mechanical_after_groups,journal_committed_groups,marker,expected_groups,has_tool_refusal):
 if mechanical_after_groups!=expected_groups or journal_committed_groups!=expected_groups:return 'HOLD_PARTIAL_OR_UNKNOWN_CAUSAL_EFFECT'
 if marker.startswith('COMMITTED'):return 'CANDIDATE_CERTIFIED_NEEDS_LIVE_REOPEN'
 if has_tool_refusal:return 'HOLD_MARKER_REPAIR_SECURITY_REFUSED_DO_NOT_RETRY'
 return 'MARKER_ONLY_CANDIDATE_REQUIRES_AUTHORIZED_REOPEN'

def selftest():
 r=auth.selftest();s=binding.selftest();t=spirit.regression();x=up.selftest();a=layout.selftest();b=sourcebound.tests();c=chat.selftest()
 assert x['decision']=='PREVIEW_READY_TEST_ONLY'
 assert x['after']['spirit_overlay']['distributed_total']==99
 assert x['after']['normal']['pa_max']==290
 assert inspect_text_command('Suba um nível',target_id='TEST',parent_id=CONFIG['lab_parent'],version='v',source_version='r')['status']=='AWAITING_EXPLICIT_ALLOCATIONS_AND_PREVIEW_CONFIRMATION'
 assert classify_native_status(mechanical_after_groups=2,journal_committed_groups=2,marker='INTENT_PREPARED',expected_groups=2,has_tool_refusal=True)=='HOLD_MARKER_REPAIR_SECURITY_REFUSED_DO_NOT_RETRY'
 assert classify_native_status(mechanical_after_groups=2,journal_committed_groups=1,marker='PREPARED',expected_groups=2,has_tool_refusal=False)=='HOLD_PARTIAL_OR_UNKNOWN_CAUSAL_EFFECT'
 return {'status':'PASS_LOCAL_FUNCTIONAL_ENTRYPOINT','contracts':{'R147':r['checks'],'R148':s['checks'],'R149_150':t['checks'],'R151':4,'R152':a['checks'],'R153':b['checks'],'R154':c['checks'],'R155_classifier':2},'state':CONFIG,'host_confirmation':'HOLD_ABSENT_TRUSTED_KEY','r155_native_final_marker':'HOLD_SECURITY_REFUSAL'}
if __name__=='__main__':print(json.dumps(selftest(),ensure_ascii=False,indent=2))
