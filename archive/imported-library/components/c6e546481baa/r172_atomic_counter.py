"""R172 — additive adapter: R171 causal preflight inside preserved R18 SQLite event_commit.
LAB-ONLY fixture, local pure-memory native v0.8.1 Scene. Original modules untouched.
No external effects or campaign writes; historical UNKNOWN_EFFECT runs are excluded.
"""
from __future__ import annotations
import copy, hashlib, json, os, sys, sqlite3, pathlib
from dataclasses import asdict
from fractions import Fraction
ROOT=pathlib.Path(__file__).resolve().parents[1]
STAGE=ROOT/'deps/r61_extracted/work/fusion_stage12' if (ROOT/'deps/r61_extracted/work/fusion_stage12').exists() else ROOT/'sources/r61_extracted/work/fusion_stage12'
NATIVE=ROOT/'deps/native_v081_controlled' if (ROOT/'deps/native_v081_controlled').exists() else pathlib.Path('/mnt/data/vlab_recovery/work/r161_r170/native_v081_controlled')
R171=ROOT/'deps/R171_counter_causal_guard' if (ROOT/'deps/R171_counter_causal_guard').exists() else pathlib.Path('/mnt/data/vlab_recovery/R171_counter_causal_guard')
for path in [str(R171),str(STAGE),str(NATIVE)]:
 if path not in sys.path:sys.path.insert(0,path)
from vlab_effects_v08 import (Scene,Combatant,AbilitySource,ActorActionState,FrozenRuleEvidence,EffectBlocked,
                             Resistances,declare_counterattack,apply_weapon_attack)
from r171_counter_causal import execute_causally_linked_counter,independent_validate_chain
import vlab_r18_interactive as r18

CODE_VERSION='R172-R18-ATOMIC-CAUSAL-COUNTER-LAB-1'
PAGE='https://app.notion.com/p/3f3c2b324ede819496ddd7f93bd7e5d2'
RULE_HASH=hashlib.sha256(b'R50-R51 controlled synthetic fixture').hexdigest()
PROOF=FrozenRuleEvidence(PAGE,'R50-R51-TEST-FIXTURE',RULE_HASH,'2026-10-17','R171-TEST-FIXTURE-NOT-PHYSICAL-AUDIT')
SRC=AbilitySource('r171-counter','reaction','REACTION',PAGE,'R50-R51-TEST-FIXTURE','RULE-DERIVED',target_scope='SELF',reaction_trigger='ATTACK_DECLARED',effect_adapter_ready=True,effect_adapter_id='V08-R50-R51')
ATT=AbilitySource('r171-attack','attack','STANDARD',PAGE,'R50-R51-TEST-FIXTURE','RULE-DERIVED',effect_adapter_ready=True,effect_adapter_id='V08-ATTACK')

def legal_state(who,react=False,other='A'):
 return ActorActionState(who,1,120,('r171-counter',) if react else ('r171-attack',),reaction_trigger_observed='ATTACK_DECLARED' if react else None,enemy_ids_visible=(other,))

def fixture_scene(state):
 fighters={}
 for aid,obj in state['actors'].items():
  resource=copy.deepcopy(obj['resource'])
  if resource.get('maximum_hp') is None:resource['maximum_hp']=obj['stats']['hp']
  fighters[aid]=Combatant(**resource)
 return Scene(fighters,events=copy.deepcopy(state.get('r172_native_events',[])),seed=state['seed'],provenance='R172-R171-R18-PURE-MEMORY-SYNTHETIC')

def validate_payload(payload):
 if type(payload)!=dict or set(payload)!={'attacker','defender','attack','counter','source_scope'}:raise EffectBlocked('R172 payload schema')
 if payload['source_scope']!='R171_TEST_FIXTURE_ONLY' or not all(isinstance(payload[x],str) for x in ('attacker','defender')):
  raise EffectBlocked('R172 source not admitted')
 a=payload['attack']; c=payload['counter']
 if not isinstance(a,dict) or set(a)!={'score','damage','rd','advanced'}:raise EffectBlocked('attack schema')
 if not isinstance(c,dict) or set(c)!={'attempts','bonus','critical','damage_groups','damage_roll_groups','flat','tag','rd'}:raise EffectBlocked('counter schema')
 if payload['attacker']==payload['defender']:raise EffectBlocked('self attack forbidden')
 if any(type(a[k])!=int or a[k]<0 for k in ('score','damage','rd')):raise EffectBlocked('numeric attack fields')
 if not isinstance(a['advanced'],bool):raise EffectBlocked('advanced flag')
 if any(type(c[k])!=int or c[k]<0 for k in ('rd',)):raise EffectBlocked('numeric counter rd')
 if not isinstance(c['tag'],str) or c['tag']!='perfurante':raise EffectBlocked('unverified counter type')

def _crash(point,current):
 if point==current:os._exit(74)

def runner(candidate,payload,revision, *, internal_fail=None):
 validate_payload(payload)
 a,d=payload['attacker'],payload['defender']
 if a not in candidate['actors'] or d not in candidate['actors'] or a==d:raise EffectBlocked('actors absent')
 scene=fixture_scene(candidate)
 prior_count=len(scene.events)
 if candidate['phase']=='ACTIVE' and candidate['active']!=a:raise EffectBlocked('actor is not active in preserved scheduler')
 if scene.actors[d].reaction!=1:raise EffectBlocked('reaction unavailable')
 if scene.actors[a].standard!=1:raise EffectBlocked('standard unavailable')
 declaration=declare_counterattack(scene,d,a,source=SRC,state=legal_state(d,True,a),proofs=(PROOF,),declared_before=True)
 _crash(internal_fail,'AFTER_DECLARATION_REACTION_SPENT')
 aa=payload['attack']
 kw={}
 if aa['advanced']:
  kw.update(damage_dice_groups=((1,6),),damage_roll_groups=((aa['damage'],),),damage_fixed_bonus=0,
    critical_sequence=(6,6,5),attack_roll_attempts=((aa['score'],),),attack_bonus=0)
 incoming=apply_weapon_attack(scene,a,d,source=ATT,state=legal_state(a,False,d),proofs=(PROOF,),
    roll_score=aa['score'],damage=aa['damage'],damage_tag='perfurante',rd=Resistances(general=aa['rd']),**kw)
 _crash(internal_fail,'AFTER_ORIGINAL_ATTACK_HP_EVENT')
 cc=payload['counter']
 # Exact vulnerable R171 window: the native responder appends its event, then the
 # unchanged R171 wrapper adds linkage. Crash the memory-only Scene.record after
 # native event/HP mutation, before wrapper can append causal references.
 if internal_fail in ('AFTER_NATIVE_RESPONSE_EVENT_BEFORE_LINK','AFTER_HP_MUTATION_BEFORE_RESPONSE_EVENT'):
  original_record=scene.record
  def sabotaged_record(entry):
   if internal_fail=='AFTER_HP_MUTATION_BEFORE_RESPONSE_EVENT' and entry['action'] in ('COUNTER_RESPONSE','COUNTER_NO_RESPONSE'):os._exit(76)
   row=original_record(entry)
   if internal_fail=='AFTER_NATIVE_RESPONSE_EVENT_BEFORE_LINK' and row['action'] in ('COUNTER_RESPONSE','COUNTER_NO_RESPONSE'):os._exit(75)
   return row
  scene.record=sabotaged_record
 response=execute_causally_linked_counter(scene,d,a,declaration=declaration,incoming=incoming,
     attack_attempts=tuple(tuple(t) for t in cc['attempts']),attack_bonus=cc['bonus'],
     critical_sequence=tuple(cc['critical']),damage_groups=tuple(tuple(t) for t in cc['damage_groups']),
     damage_roll_groups=tuple(tuple(t) for t in cc['damage_roll_groups']),flat=cc['flat'],damage_tag=cc['tag'],
     rd=Resistances(general=cc['rd']))
 _crash(internal_fail,'AFTER_CAUSAL_LINK_BEFORE_COMMIT')
 audit=independent_validate_chain(scene.events)
 if audit['counter_responses'] != sum(1 for x in scene.events if x['action'] in ('COUNTER_RESPONSE','COUNTER_NO_RESPONSE')):
  raise EffectBlocked('R171 causal cardinality mismatch')
 if len(scene.events)-prior_count!=3:raise EffectBlocked('native three event sequence mismatch')
 for aid,actor in scene.actors.items():candidate['actors'][aid]['resource']=asdict(actor)
 candidate['r172_native_events']=copy.deepcopy(scene.events)
 candidate['r172_version']=CODE_VERSION
 candidate['r172_last_links']={'declaration_seq':declaration['seq'],'original_attack_seq':incoming['seq'],
  'response_seq':response['seq'],'tx_seq':revision}
 if candidate['phase']=='ACTIVE':
  if candidate['active'] != a:raise EffectBlocked('scheduler actor mismatch')
  control=r18._next_turn(candidate)
 else:control={'scheduler':'NOT_STARTED_SYNTHETIC_EXCHANGE'}
 return {'r172_engine':CODE_VERSION,'event_range':[prior_count+1,len(scene.events)],
   'native_events':copy.deepcopy(scene.events[prior_count:]),'actor_resources':{aid:asdict(x) for aid,x in scene.actors.items()},
   'response_kind':response['action'],'attack_hit':incoming['hit'],
   'source_scope':'R171_TEST_FIXTURE_ONLY','native_v081_calls':3,'causal_links_embedded_before_r18_commit':True,
   'pure_memory_before_publish':True,'native_scene_sha':scene.checksum(),'scheduler_control':control,
   'official_effects':0,'terminal_certificates':0}

def start_three_actor_fixture(db,cmd_id):
 """Existing R18 turn scheduler, one 3rd TEST-only clone actor; no creature or official initiative."""
 def add_and_start(state,p,seq):
  if state['phase']!='INIT' or set(state['actors'])!={'LAB_VIGIA_A','LAB_VIGIA_B'}:raise EffectBlocked('three fixture eligibility')
  third=copy.deepcopy(state['actors']['LAB_VIGIA_B'])
  third['name']='Vigia Terceiro — fixture sintética'
  third['stats'].update(id='LAB_VIGIA_C',name='Vigia Terceiro — fixture sintética',des=12)
  third['resource']['actor_id']='LAB_VIGIA_C'
  state['actors']['LAB_VIGIA_C']=third
  st=r18.do_start(state,{},seq)
  return {'fixture_extension':'R172_THIRD_SYNTHETIC_ACTOR_NO_NEW_SPECIES','source_actor':'LAB_VIGIA_B',
   'new_actor':'LAB_VIGIA_C','not_source_admissible':True,'native_scheduler':st,'official_effects':0}
 return r18.event_commit(db,cmd_id,'R172_THREE_ACTOR_START',{'fixture':'LAB_R18_A_PLUS_DUPLICATE_B'},add_and_start)

def pass_existing_r18_turn(db,cmd_id):
 return r18.event_commit(db,cmd_id,'R172_EXISTING_R18_PASS',{'scheduler':'R18_NATIVE_SYNTHETIC'},
   lambda candidate,p,seq:r18.do_pass(candidate,p,seq))

def counter_payload(*,attacker='LAB_VIGIA_A',defender='LAB_VIGIA_B',score=4,attack_damage=4,attack_rd=0,
                    critical=False,counter_hit=True,counter_flat=5):
 return {'attacker':attacker,'defender':defender,'source_scope':'R171_TEST_FIXTURE_ONLY',
  'attack':{'score':score,'damage':attack_damage,'rd':attack_rd,'advanced':critical},
  'counter':{'attempts':[[6,6,6],[6,6,5]] if counter_hit else [[1],[2]],'bonus':0,
   'critical':[2,3,4],'damage_groups':[[1,6]],'damage_roll_groups':[[4]],'flat':counter_flat,
   'tag':'perfurante','rd':0}}

def execute(db,cmd_id,payload, *, r18_fail=None, internal_fail=None,checkpoint=True):
 validate_payload(payload)
 with r18.connect(db) as c:
  if c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='r172_aborts'").fetchone():
   if c.execute('SELECT 1 FROM r172_aborts WHERE cmd_id=?',(cmd_id,)).fetchone():raise r18.LabHold('R172 aborted command cannot be reused')
  if c.execute('SELECT 1 FROM events WHERE cmd_id=?',(cmd_id,)).fetchone():raise r18.LabHold('DUPLICATE COMMAND REJECTED BEFORE INTENT')
  st,head,rev=r18._read(c)
  a,d=payload['attacker'],payload['defender']
  if a not in st['actors'] or d not in st['actors']:raise r18.LabHold('ACTOR_NOT_IN_SCENE')
  if st['actors'][a]['resource']['standard']!=1 or st['actors'][d]['resource']['reaction']!=1:
   raise r18.LabHold('R172 resource unavailable — no pending intent created')
  if st['phase']=='ACTIVE' and st['active']!=a:raise r18.LabHold('R172 actor not current turn — no pending intent created')
 row=r18.event_commit(db,cmd_id,'R172_COUNTER_EXCHANGE',payload,
     lambda candidate,p,rev:runner(candidate,p,rev,internal_fail=internal_fail),failpoint=r18_fail)
 if checkpoint:write_checkpoint(db)
 return row

def write_checkpoint(db):
 # External checkpoint may be lost after atomic event commit: authoritative journal is SQLite.
 hist=r18.history(db)
 body={'format':'R172_EXPORTED_CHECKPOINT_ONLY','db':pathlib.Path(db).name,
       'revision':hist['revision'],'head':hist['head'],'state':hist['state'],
       'events':hist['events'],'official_effects':0}
 blob={'body':body,'sha256':r18.sha(body)}
 name=pathlib.Path(str(db)+'.checkpoint.json');tmp=pathlib.Path(str(name)+'.tmp')
 with open(tmp,'x',encoding='utf-8') as f:
  json.dump(blob,f,ensure_ascii=False,sort_keys=True,indent=2,default=str);f.flush();os.fsync(f.fileno())
 os.replace(tmp,name)
 return name

def cold_status(db):
 con=r18.connect(db)
 try:
  m=r18._meta(con);pending=con.execute('SELECT cmd_id,base_head,kind,payload_json FROM pending').fetchall()
  events=con.execute('SELECT cmd_id FROM events ORDER BY seq').fetchall()
  if pending:return {'state':'PENDING_NO_AUTORETRY','revision':int(m['revision']),
   'pending_cmd_ids':[x[0] for x in pending],'committed_cmd_ids':[x[0] for x in events]}
  state,head,rev=r18._read(con)
  return {'state':'COLD_COMMITTED','revision':rev,'head':head,'committed_cmd_ids':[x[0] for x in events],
          'state_sha':r18.sha(state)}
 finally:con.close()

def abort_pending_lab_only(db,cmd_id):
 # Reconcile in a controlled experimental DB ONLY. No retries, no original history.
 # A verified pure in-memory code path cannot externally commit prior to R18 event_commit.
 con=r18.connect(db)
 try:
  con.execute('BEGIN IMMEDIATE')
  pending=con.execute('SELECT base_head,kind,payload_json FROM pending WHERE cmd_id=?',(cmd_id,)).fetchone()
  if not pending or pending[1]!='R172_COUNTER_EXCHANGE':raise r18.LabHold('NOT_AN_R172_PENDING_INTENT')
  if con.execute('SELECT 1 FROM events WHERE cmd_id=?',(cmd_id,)).fetchone():raise r18.LabHold('COMMIT_EXISTS')
  base_head,_,payload_json=pending
  if r18._meta(con)['head']!=base_head:raise r18.LabHold('HEAD_AFTER_INTENT_CHANGED')
  con.execute('SAVEPOINT precommit_probe')
  con.execute('DELETE FROM pending WHERE cmd_id=?',(cmd_id,))
  state,head,rev=r18._read(con)
  con.execute('ROLLBACK TO SAVEPOINT precommit_probe')
  con.execute('RELEASE SAVEPOINT precommit_probe')
  # Preserve cold-read intent and prohibit command ID reuse. No synthetic effect log event.
  con.execute('CREATE TABLE IF NOT EXISTS r172_aborts(cmd_id TEXT PRIMARY KEY,base_head TEXT NOT NULL,payload_sha TEXT NOT NULL,state_sha TEXT NOT NULL,status TEXT NOT NULL)')
  con.execute('INSERT INTO r172_aborts VALUES (?,?,?,?,?)',(cmd_id,base_head,
   hashlib.sha256(payload_json.encode()).hexdigest(),r18.sha(state),'ABORTED_PURE_MEMORY_NO_EFFECT_RETRY_FORBIDDEN'))
  con.execute('DELETE FROM pending WHERE cmd_id=?',(cmd_id,))
  con.commit()
  return {'state':'EXPERIMENTAL_ABORT_VERIFIED','cmd_id':cmd_id,'head':head,'revision':rev,
   'retry_allowed':False,'no_historical_writes':True}
 except:con.rollback();raise
 finally:con.close()

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--db',required=True);p.add_argument('--cmd',required=True);
 p.add_argument('--seed',type=int,default=1720001);p.add_argument('--r18-fail',default=None);p.add_argument('--internal-fail',default=None);
 p.add_argument('--attack-score',type=int,default=4);p.add_argument('--critical',action='store_true');p.add_argument('--attack-rd',type=int,default=0);
 p.add_argument('--defender',default='LAB_VIGIA_B');p.add_argument('--attacker',default='LAB_VIGIA_A');p.add_argument('--counter-flat',type=int,default=5)
 o=p.parse_args();db=pathlib.Path(o.db)
 if not db.exists():r18.init_db(db,'A',o.seed)
 payload=counter_payload(attacker=o.attacker,defender=o.defender,score=o.attack_score,critical=o.critical,attack_rd=o.attack_rd,counter_flat=o.counter_flat)
 result=execute(db,o.cmd,payload,r18_fail=o.r18_fail,internal_fail=o.internal_fail)
 print(json.dumps({'receipt':result,'status':cold_status(db)},indent=2,default=str))
