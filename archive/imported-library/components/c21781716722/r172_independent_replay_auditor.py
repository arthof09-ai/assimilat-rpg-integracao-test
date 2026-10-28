"""R172 independent cold auditor: does not import r172_atomic_counter or its verdicts.
Re-runs frozen R18 commands and original v0.8.1 R50/R51 functions; compares
EVERY event, resource, causal edge and after-state with persistent SQL journal.
A separate audit program is NOT an external human accreditation.
"""
from __future__ import annotations
import copy,hashlib,json,pathlib,sys,sqlite3
from dataclasses import asdict
ROOT=pathlib.Path(__file__).resolve().parents[1]
NATIVE=ROOT/'deps/native_v081_controlled' if (ROOT/'deps/native_v081_controlled').exists() else pathlib.Path('/mnt/data/vlab_recovery/work/r161_r170/native_v081_controlled')
STAGE=ROOT/'deps/r61_extracted/work/fusion_stage12' if (ROOT/'deps/r61_extracted/work/fusion_stage12').exists() else ROOT/'sources/r61_extracted/work/fusion_stage12'
for p in (STAGE,NATIVE):sys.path.insert(0,str(p))
from vlab_effects_v08 import Scene,Combatant,AbilitySource,ActorActionState,FrozenRuleEvidence,Resistances,declare_counterattack,apply_weapon_attack,execute_declared_counterattack
import vlab_r18_interactive as core

PAGE='https://app.notion.com/p/3f3c2b324ede819496ddd7f93bd7e5d2'
PROOF=FrozenRuleEvidence(PAGE,'R50-R51-TEST-FIXTURE',hashlib.sha256(b'R50-R51 controlled synthetic fixture').hexdigest(),'2026-10-17','R171-TEST-FIXTURE-NOT-PHYSICAL-AUDIT')
DECL=AbilitySource('r171-counter','reaction','REACTION',PAGE,'R50-R51-TEST-FIXTURE','RULE-DERIVED',target_scope='SELF',reaction_trigger='ATTACK_DECLARED',effect_adapter_ready=True,effect_adapter_id='V08-R50-R51')
ATK=AbilitySource('r171-attack','attack','STANDARD',PAGE,'R50-R51-TEST-FIXTURE','RULE-DERIVED',effect_adapter_ready=True,effect_adapter_id='V08-ATTACK')

def same(a,b,what):
 if core.canonical(a)!=core.canonical(b):raise AssertionError('CAUSAL_REPLAY_MISMATCH:'+what)

def actor_state(a,target,react):
 return ActorActionState(a,1,120,('r171-counter',) if react else ('r171-attack',),
  reaction_trigger_observed='ATTACK_DECLARED' if react else None,enemy_ids_visible=(target,))

def replay_exchange(state,p,revision):
 a=p['attacker'];d=p['defender']; attack=p['attack'];counter=p['counter']
 before_events=copy.deepcopy(state.get('r172_native_events',[]));before_len=len(before_events)
 actors={}
 for who,entry in state['actors'].items():
  r=copy.deepcopy(entry['resource']);r['maximum_hp']=r.get('maximum_hp') or entry['stats']['hp']
  actors[who]=Combatant(**r)
 scene=Scene(actors,events=before_events,seed=state['seed'],provenance='R172-R171-R18-PURE-MEMORY-SYNTHETIC')
 if scene.actors[d].reaction!=1 or scene.actors[a].standard!=1:raise AssertionError('ILLEGAL_RESOURCE_PRESTATE')
 if state['phase']=='ACTIVE' and state['active']!=a:raise AssertionError('ILLEGAL_SCHEDULER_ACTOR')
 dec=declare_counterattack(scene,d,a,source=DECL,state=actor_state(d,a,True),proofs=(PROOF,),declared_before=True)
 more={}
 if attack['advanced']:
  more={'damage_dice_groups':((1,6),),'damage_roll_groups':((attack['damage'],),),'damage_fixed_bonus':0,
        'critical_sequence':(6,6,5),'attack_roll_attempts':((attack['score'],),),'attack_bonus':0}
 hit=apply_weapon_attack(scene,a,d,source=ATK,state=actor_state(a,d,False),proofs=(PROOF,),roll_score=attack['score'],
      damage=attack['damage'],damage_tag='perfurante',rd=Resistances(general=attack['rd']),**more)
 response=execute_declared_counterattack(scene,d,a,declaration=dec,incoming=hit,
      attack_attempts=tuple(tuple(x) for x in counter['attempts']),attack_bonus=counter['bonus'],
      critical_sequence=tuple(counter['critical']),damage_groups=tuple(tuple(x) for x in counter['damage_groups']),
      damage_roll_groups=tuple(tuple(x) for x in counter['damage_roll_groups']),flat=counter['flat'],
      damage_tag=counter['tag'],rd=Resistances(general=counter['rd']))
 # Independent event correlator only after in-memory native effects.
 response.update(declaration_seq=dec['seq'],original_attack_seq=hit['seq'])
 if response['seq']!=len(scene.events) or hit['seq']+1!=response['seq'] or dec['seq']+2!=response['seq']:
  raise AssertionError('EVENT_LINKAGE')
 if hit['hit'] is True and response['action']!='COUNTER_NO_RESPONSE':raise AssertionError('R50')
 if hit['hit'] is False and response['action']!='COUNTER_RESPONSE':raise AssertionError('R50')
 for aid,x in scene.actors.items():state['actors'][aid]['resource']=asdict(x)
 state['r172_native_events']=copy.deepcopy(scene.events)
 state['r172_version']='R172-R18-ATOMIC-CAUSAL-COUNTER-LAB-1'
 state['r172_last_links']={'declaration_seq':dec['seq'],'original_attack_seq':hit['seq'],
   'response_seq':response['seq'],'tx_seq':revision}
 control=core._next_turn(state) if state['phase']=='ACTIVE' else {'scheduler':'NOT_STARTED_SYNTHETIC_EXCHANGE'}
 return {'r172_engine':'R172-R18-ATOMIC-CAUSAL-COUNTER-LAB-1','event_range':[before_len+1,len(scene.events)],
   'native_events':copy.deepcopy(scene.events[before_len:]),'actor_resources':{aid:asdict(x) for aid,x in scene.actors.items()},
   'response_kind':response['action'],'attack_hit':hit['hit'],
   'source_scope':'R171_TEST_FIXTURE_ONLY','native_v081_calls':3,'causal_links_embedded_before_r18_commit':True,
   'pure_memory_before_publish':True,'native_scene_sha':scene.checksum(),
   'scheduler_control':control,'official_effects':0,'terminal_certificates':0}

def replay_start(state,p,seq):
 if state['phase']!='INIT' or set(state['actors'])!={'LAB_VIGIA_A','LAB_VIGIA_B'}:raise AssertionError('BAD_FIXTURE_START')
 third=copy.deepcopy(state['actors']['LAB_VIGIA_B']);third['name']='Vigia Terceiro — fixture sintética'
 third['stats'].update(id='LAB_VIGIA_C',name='Vigia Terceiro — fixture sintética',des=12)
 third['resource']['actor_id']='LAB_VIGIA_C';state['actors']['LAB_VIGIA_C']=third
 st=core.do_start(state,{},seq)
 return {'fixture_extension':'R172_THIRD_SYNTHETIC_ACTOR_NO_NEW_SPECIES','source_actor':'LAB_VIGIA_B',
  'new_actor':'LAB_VIGIA_C','not_source_admissible':True,'native_scheduler':st,'official_effects':0}

def audit(db,check_checkpoint=False):
 hist=core.history(db) # verifies native R18 SQLite chain and structural hashes
 final_state=hist['state']; rows=hist['events']; genesis=core.initial('A',final_state['seed'])
 with sqlite3.connect(db) as conn:
  meta=dict(conn.execute('SELECT key,value FROM meta'))
  if meta['genesis']!=core.sha({'seed':final_state['seed'],'scene':'A','version':core.VERSION}):raise AssertionError('GENESIS_FORGERY')
  if conn.execute('SELECT COUNT(*) FROM pending').fetchone()[0]:raise AssertionError('PENDING_HOLD')
 state=genesis
 checked=[];last_head=meta['genesis']
 for idx,row in enumerate(rows,1):
  if row['prev']!=last_head or row['seq']!=idx:raise AssertionError('R18_CHAIN')
  if core.sha(state)!=row['before_sha']:raise AssertionError('WRONG_BEFORE_STATE')
  typ=row['kind'];p=row['payload']
  if typ=='R172_COUNTER_EXCHANGE':detail=replay_exchange(state,p,idx)
  elif typ=='R172_THREE_ACTOR_START':detail=replay_start(state,p,idx)
  elif typ=='R172_EXISTING_R18_PASS':detail=core.do_pass(state,p,idx)
  else:raise AssertionError('UNKNOWN_R172_COMMAND:'+str(typ))
  same(detail,row['detail'],'row_'+str(idx)+'_DETAIL')
  if core.sha(state)!=row['after_sha']:raise AssertionError('COLD_REPLAY_STATE_SHA_'+str(idx))
  checked.append({'seq':idx,'kind':typ,'cmd_id':row['cmd_id'],'head':row['hash']})
  last_head=row['hash']
 same(state,final_state,'FINAL_STATE')
 if meta['head']!=last_head:raise AssertionError('FINAL_HEAD')
 if check_checkpoint:
  p=pathlib.Path(str(db)+'.checkpoint.json')
  if not p.exists():raise AssertionError('MISSING_EXPORTED_CHECKPOINT')
  x=json.loads(p.read_text());same(x['sha256'],core.sha(x['body']),'CHECKPOINT_HASH')
  same(x['body']['state'],final_state,'CHECKPOINT_STATE');same(x['body']['head'],meta['head'],'CHECKPOINT_HEAD')
  same(x['body']['events'],rows,'CHECKPOINT_EVENTS')
 return {'result':'PASS_INDEPENDENT_COLD_CAUSAL_REPLAY','journal_rows':len(rows),
  'native_events':len(state.get('r172_native_events',[])),'actors':len(state['actors']),
  'head':meta['head'],'state_sha':core.sha(state),'commands':checked,
  'audit_module_is_separate_from_producer':True,'formal_external_human_audit':False,
  'official_cells':0,'terminal_contracts':0}

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('db');p.add_argument('--checkpoint',action='store_true');a=p.parse_args()
 print(json.dumps(audit(a.db,a.checkpoint),indent=2,ensure_ascii=False))
