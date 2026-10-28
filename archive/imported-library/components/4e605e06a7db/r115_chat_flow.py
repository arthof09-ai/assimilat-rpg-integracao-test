"""R115 conversational facade atop R105 preview. No new chatbot or autonomous Notion writer.
Mestre-side TEST authorization is separate from player confirmation; handles cancel/stale/idempotency.
"""
import json,re
from pathlib import Path
from r105_canonical_progression_planner import generate,BASE,delta,Hold as RulesHold
class FlowHold(Exception):pass
ALLOWED_TARGET='3fcc2b324ede819a8993de63eb92bda3'
CONSUMED={'IBX17-R108-INIT-20261016-01'}

def plan(text,fixture_id,confirmation,source_version,live_version,event_id):
 if fixture_id!=ALLOWED_TARGET:raise FlowHold('TARGET_NOT_LAB_FIXTURE')
 if not source_version or source_version!=live_version:raise FlowHold('STALE_SOURCE_VERSION')
 if event_id in CONSUMED:return {'status':'NOOP_ALREADY_COMMITTED','event_id':event_id,'new_writes':0}
 if confirmation=='NEGADO':return {'status':'CANCELED_NO_WRITE','new_writes':0}
 if confirmation not in ('LAB_TEST_EXPLICIT_FROM_MESTRE','REAL_PLAYER_VERIFIED'):
  return {'status':'AWAITING_HUMAN_CONFIRMATION','new_writes':0}
 if confirmation=='REAL_PLAYER_VERIFIED':raise FlowHold('TEST_ROUTE_NOT_REAL_PLAYER_DESTINATION')
 if '0→1' not in text and '0 para 1' not in text:raise FlowHold('MISSING_LEVEL_ROUTE')
 if '+2 FOR' not in text:raise FlowHold('MISSING_EXPLICIT_ALLOCATION')
 if '60%' not in text:raise FlowHold('MISSING_GROWTH_CHOICE')
 receipt=generate(BASE,[delta(FOR=2)],['FIXED60_EXPLICIT'])
 return {'status':'TEST_PREVIEW_REQUIRES_NATIVE_READBACK','level0':receipt['levels'][0],
  'level1':receipt['levels'][1],'confirmation':'TEST_ORDER_ONLY_NOT_REAL_PLAYER','new_writes':0,
  'writer':'EXTERNAL_NATIVE_ADAPTER_ONLY'}

route='Evolua TEST sintético de 0→1, +2 FOR e crescimento fixo 60%'
assert plan(route,ALLOWED_TARGET,'LAB_TEST_EXPLICIT_FROM_MESTRE','v1','v1','new-1')['level1']['hp_max']==18
assert plan(route,ALLOWED_TARGET,'NEGADO','v1','v1','new-2')['new_writes']==0
assert plan(route,ALLOWED_TARGET,'LAB_TEST_EXPLICIT_FROM_MESTRE','v1','v1','IBX17-R108-INIT-20261016-01')['status']=='NOOP_ALREADY_COMMITTED'
for bad in [('source','other'),('fixture','OTHER')]:
 try:plan(route,ALLOWED_TARGET if bad[0]=='source' else bad[1],'LAB_TEST_EXPLICIT_FROM_MESTRE','v1',bad[1] if bad[0]=='source' else 'v1','new-3')
 except FlowHold:pass
 else:raise AssertionError('unguarded stale/wrong target')
assert plan('Subir alguns níveis',ALLOWED_TARGET,'UNCONFIRMED','v1','v1','new-4')['new_writes']==0
out={'status':'PASS_LOCAL_DIALOG_GATES; NATIVE_CONVERSATIONAL_MULTI_TURN_HOLD','positive_existing_native_link':'https://app.notion.com/p/'+ALLOWED_TARGET,
 'human_confirmation_actual':'NOT_OBTAINED_FOR_REAL_PLAYER',
 'mestre_lab_authorization':'USER_ORDER_EXPLICIT',
 'tests':{'synthetic_preview':True,'cancel_no_write':True,'idempotent_replay_no_write':True,'stale_version_rejected':True,'wrong_target_rejected':True,'unknown_confirmation_waits':True},
 'not_claimed':['actual multi-turn confirmation dialogue','automatic Notion credential writer','Party application']}
(Path(__file__).parent/'R115_CHAT_FLOW_LOCAL.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print('R115 local chat gates 6/6 PASS; native distinct conversational final confirmation still HOLD')
