import json
from r117_causal_recovery import classify,sha,authorize_recovery,Hold
B={'NORMAL':{'x':0},'TRANSFORM':{'x':0},'LOCKS':{'x':0}}
A={'NORMAL':{'x':1},'TRANSFORM':{'x':1},'LOCKS':{'x':1}}
r={'before':B,'after':A};ident={'event_id':'S2','target_id':'t','parent_id':'3fbc2b324ede804a95fafcb7b293c92c','source_version':'v1','pre_version':'v0','receipt_hash':sha(r),'authority':'LAB_TEST_EXPLICIT_FROM_MESTRE','actor_id':'actor'}
p={'last_read_version':'v2','target_id':'t','parent_id':ident['parent_id'],'event_id':'S2','source_version':'v1','pre_version':'v0','all_stage_readbacks':True,'proof_review':'INDEPENDENTLY_VERIFIED'}
J=lambda a,b,c:dict(zip(B,(a,b,c)))
def c(physical=A,journal=J('COMMITTED','COMMITTED','COMMITTED'),marker='PREPARED',proof=p,identity=ident,version='v2'):return classify(receipt=r,physical=physical,journals=journal,final_marker=marker,identity=identity,proof=proof,live_version=version)
assert c().classification=='MARKER_ONLY_REPAIR_CANDIDATE'
assert c(proof=p|{'proof_review':'EXECUTOR_SELF_ONLY'}).classification=='TERMINAL_REVIEW_PENDING'
assert c(physical={'NORMAL':A['NORMAL'],'TRANSFORM':A['TRANSFORM'],'LOCKS':B['LOCKS']},journal=J('COMMITTED','PREPARED','PREPARED')).classification=='AFTER_WITHOUT_CAUSAL_JOURNAL'
assert c(physical={'NORMAL':A['NORMAL'],'TRANSFORM':A['TRANSFORM'],'LOCKS':B['LOCKS']},journal=J('COMMITTED','PREPARED','PREPARED'),proof=p|{'stage_receipts':{'TRANSFORM':{'event_id':'S2','target_id':'t','stage':'TRANSFORM','after_hash':sha(A['TRANSFORM']),'native_write_receipt_id':'connectorReceipt','before_version':'v1','after_version':'v2'}}}).classification=='JOURNAL_REPAIR_CANDIDATE'
assert c(physical=B,journal=J('COMMITTED','PREPARED','PREPARED')).classification=='JOURNAL_AHEAD_PHYSICAL'
assert c(physical={'NORMAL':{'x':7},'TRANSFORM':B['TRANSFORM'],'LOCKS':B['LOCKS']},journal=J('PREPARED','PREPARED','PREPARED')).classification=='UNKNOWN_EFFECT'
assert c(physical=B,journal=J('PREPARED','PREPARED','PREPARED'),marker='COMMITTED').classification=='FALSE_TERMINAL_MARKER'
assert c(proof=p|{'concurrent_edit':True}).classification=='CONCURRENT_EVENT'
assert c(version='v3').classification=='STALE_VERSION'
assert c(marker='COMMITTED').classification=='COMMITTED_NOOP'
assert c(physical={'NORMAL':A['NORMAL'],'TRANSFORM':B['TRANSFORM'],'LOCKS':B['LOCKS']},journal=J('COMMITTED','PREPARED','PREPARED')).classification=='PARTIAL_NEXT_STAGE_CANDIDATE'
assert authorize_recovery(c(),new_live_version='v2',authority='LAB_TEST_EXPLICIT_FROM_MESTRE',operator='executor',plan_id='plan')['minimal_writeset']==['FINAL_MARKER']
try:authorize_recovery(c(),new_live_version='v3',authority='LAB_TEST_EXPLICIT_FROM_MESTRE',operator='executor',plan_id='plan')
except Hold:pass
else:raise AssertionError('stale repair allowed')
print('R117: 13/13 directed cases PASSED')
