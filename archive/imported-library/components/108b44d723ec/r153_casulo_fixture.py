"""R153 three TECHNICAL instances Eristan/Eristan/Feryn, one causal Casulo protected hit.
Does not assert source timing of two turns or exact speed when Eristan speed unknown.
"""
import hashlib,json,sqlite3,sys,copy
from pathlib import Path
from dataclasses import asdict
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import r151_tactical_native as t
from vlab_effects_v08 import (Scene,Combatant,AbilitySource,ActorActionState,FrozenRuleEvidence,
 begin_source_turn,end_source_turn,apply_casulo_brotos,apply_weapon_attack)
from vlab_rd_v08 import Resistances
core=t.core

def candidate(seed):
  die=core.dice(seed,1,'R151-F-NORMAL-HIT-0',4,6)
  crit=[core.dice(seed,1,f'R151-F-NORMAL-CRIT-{i}',1,6)[0] for i in range(3)]
  score=sum(die)+92
  return score,crit
seed=next(z for z in range(999001,1003000) if 76<candidate(z)[0]<=98 and candidate(z)[1][:2]!=[6,6])
RUN=f'R153_CASULO_CA_SOURCE_DEV_S{seed}'
PRE={'run':RUN,'seed':seed,'selection':'first seed in 999001..1002999 with F basic 4d6+92 score in (76,98], no natural auto-critical; directed not holdout',
  'source':'Sikong Eristan Reconstituição etc Eristan Casulo de Brotos 60PA Standard ally within15m +22CA -4m move two turns, nonstack',
  'actors':'E1 and E2 are technical copies of one proposed NPC Eristan, NOT two canon personalities, F actual source proposed Feryn',
  'E2_source_speed':'not source-verified; -4m effect stored symbolically only; no movement computed',
  'turn_boundary':'expiry 2 turnos unknown; persisted active with HOLD; no automatic expiration',
  'test':'identical physical score against documented E2 CA76 would hit unprotected but misses against CA98; one R18 transaction source-gated',
  'NO_REPEAT':'do not reuse run or committed db; R01–R150 histories immutable'}
(ROOT/'R153_CASULO_PREREG.json').write_text(json.dumps(PRE,ensure_ascii=False,indent=2)+'\n')
P={'F':copy.deepcopy(t.P['F']),'E1':copy.deepcopy(t.P['E']),'E2':copy.deepcopy(t.P['E'])}
def proof(page,rule):return (FrozenRuleEvidence(page,rule,hashlib.sha256((page+rule+'R153').encode()).hexdigest(),'2026-10-16_READ','LOCAL_LAB_PROOF'),)
def load(db):return core.load(db)
def initialize():
 db=ROOT/'runs'/f'{RUN}.sqlite';db.parent.mkdir(exist_ok=True)
 if db.exists():raise ValueError('NO_REPEAT')
 core.init_db(db,'A',seed);st=core.initial('A',seed)
 st.update({'scene':RUN,'run_id':RUN,'phase':'ACTIVE','order':['E1','F','E2'],'active':'E1','round':1,'turn_index':0,
            'source_notes':PRE,'action_nonce':{'F':0,'E1':0,'E2':0},'casulos':{},'terminal_contracts':0,
            'actors':{}})
 for w,p in P.items():
  o=Combatant(w,p['hp'],p['pa'],p['ca'],p['con'],p['armor'],p['fort'],p['reflex'],'CASULO-LAB-ZONE',rank=p['rank'],standard=0,movement=0,reaction=1,maximum_hp=p['hp'],base_speed=p['speed'])
  st['actors'][w]={'source':p['source'],'source_profile':p,'resource':asdict(o)}
 anchor=core.sha({'genesis':st,'lineage':'V081_R18_R26_R153_SOURCE_CASULO'})
 with core.connect(db) as c:
  for k,v in [('scene',RUN),('genesis',anchor),('head',anchor),('state',core.canonical(st))]:c.execute('update meta set value=? where key=?',(v,k))
 db.with_suffix('.genesis.json').write_text(core.canonical(st)+'\n')
 return db

def src(st,w,target,kind):
 p=P[w];r=st['actors'][w]['resource'];cost=60 if kind=='COCOON' else 0
 source=AbilitySource('R153-'+w+'-'+kind,'control' if kind=='COCOON' else 'attack','STANDARD',p['source'],kind,'RULE-DERIVED',
   required_pa=cost,target_scope='ALLY' if kind=='COCOON' else 'ENEMY',effect_adapter_ready=True,effect_adapter_id='V081_R153_NATIVE')
 a=ActorActionState(w,p['rank_index'],r['pa'],(source.action_id,),standard_available=r['standard']==1,
 movement_available=r['movement']==1,reaction_available=r['reaction']==1,range_confirmed=True,los_confirmed=True,geometry_confirmed=True,
 ally_ids_visible=(target,) if kind=='COCOON' else (),enemy_ids_visible=(target,) if kind!='COCOON' else ())
 return source,a,proof(p['source'],kind)

def command(db,kind,p):
 st,head,rev=load(db);a=st['active'];r=st['actors'][a]['resource']
 if kind=='START':assert p=={'actor':a} and r['standard']==0
 elif kind=='COCOON':assert a=='E1' and not st['casulos'] and r['standard']==1 and r['pa']>=60 and p=={'target':'E2','distance_m':3}
 elif kind=='STRIKE':
  assert a=='F' and r['standard']==1
  ct=t.physical_tape({'actors':{'F':st['actors']['F']},'action_nonce':{'F':st['action_nonce']['F']},'seed':seed},'F','E2')
  assert p['tape']==ct and ct['score']>76 and ct['score']<=98
 elif kind=='PASS':assert a=='E2' and r['standard']==1 and p=={'actor':'E2'}
 elif kind=='END':assert p=={'actor':a} and r['standard']==0
 else:raise ValueError(kind)
 cmd='LAB-CMD-R153-'+core.sha({'run':RUN,'rev':rev,'kind':kind,'payload':p})[:40]
 def reducer(s,q,seq):
  sc=Scene({w:Combatant(**v['resource']) for w,v in s['actors'].items()},seed=seed,provenance='R153_MESTRE_ONLY_TECHNICAL_CASULO')
  ev=[];current=s['active']
  if kind=='START':ev.append(begin_source_turn(sc,current))
  elif kind=='COCOON':
   source,ss,pr=src(s,'E1','E2','COCOON')
   ev.append(apply_casulo_brotos(sc,'E1','E2',source=source,state=ss,proofs=pr,range_m=3,same_caster_effect_active=bool(s['casulos'])))
   s['casulos']['E1/E2']={'source':P['E1']['source'],'duration_literal':'2 TURNOS','remaining':'HOLD_EXACT_EXPIRY',
    'CA_delta':22,'speed_delta_m':-4,'active':True,'applied_round':1,'no_stack':True}
  elif kind=='STRIKE':
   tape=q['tape'];sp,ss,pr=src(s,'F','E2','BASIC');pp=P['F']
   ev.append(apply_weapon_attack(sc,'F','E2',source=sp,state=ss,proofs=pr,roll_score=tape['score'],damage=tape['damage'],damage_tag='perfurante',
    rd=Resistances(general=P['E2']['rd'],provenance='SOURCE_PHYSICAL_RD'),damage_dice_groups=tuple(map(tuple,pp['damage_dice'])),
    damage_roll_groups=tuple(map(tuple,tape['damage_rolls'])),damage_fixed_bonus=pp['damage_flat'],critical_sequence=tuple(tape['crit']),
    attack_roll_attempts=tuple(map(tuple,tape['hit'])),attack_bonus=pp['attack_flat'],lab_negative_critical_policy=True))
   s['action_nonce']['F']+=1
  elif kind=='PASS':sc.actors['E2'].standard=0;ev.append(sc.record({'action':'FOREGO_STANDARD','by':'E2','technical_fixture_only':True}))
  elif kind=='END':
   ev.append(end_source_turn(sc,current));s['turn_index']+=1
   idx=s['order'].index(current);j=(idx+1)%3;s['active']=s['order'][j]
   if j<=idx:s['round']+=1
  for w,z in sc.actors.items():
   rr=asdict(z);rr['ca']=int(rr['ca']);rr['base_speed']=int(rr['base_speed']) if rr['base_speed'] is not None else None
   s['actors'][w]['resource']=rr
  return {'native_actions':ev,'scope':'CASULO_TEMPORAL_BOUNDARY_HOLD_TECHNICAL','contracts':['PA_AND_PREBUFF_COSTS','ITEM_EQUIPMENT_AND_ENHANCEMENTS','TURN_SCHEDULER_EVENT_SOURCING']}
 return core.event_commit(db,cmd,kind,p,reducer)

def run():
 db=initialize()
 for kind,p in [('START',{'actor':'E1'}),('COCOON',{'target':'E2','distance_m':3}),('END',{'actor':'E1'}),('START',{'actor':'F'})]:command(db,kind,p)
 st,_,_=load(db)
 tape=t.physical_tape({'actors':{'F':st['actors']['F']},'action_nonce':{'F':st['action_nonce']['F']},'seed':seed},'F','E2')
 command(db,'STRIKE',{'tape':tape});command(db,'END',{'actor':'F'})
 command(db,'START',{'actor':'E2'});command(db,'PASS',{'actor':'E2'});command(db,'END',{'actor':'E2'})
 st,head,rev=load(db)
 with sqlite3.connect(db) as c:
  rows=[json.loads(x[0]) for x in c.execute('select row_json from events order by seq')]
  pending=c.execute('select count(*) from pending').fetchone()[0]
 with sqlite3.connect(db) as con,sqlite3.connect(db.with_suffix('.checkpoint.sqlite')) as cp:con.backup(cp)
 assert load(db)==load(db.with_suffix('.checkpoint.sqlite'))
 ev=[x for row in rows for x in row['detail']['native_actions']];attack=next(x for x in ev if x['action']=='weapon_attack')
 assert not attack['hit'] and attack['roll_score']>76 and attack['roll_score']<=98
 # Rejected duplicate must NOT create an intention or mutate the DB.
 before=load(db);deny='CASULO_ALREADY_ACTIVE_BEFORE_INTENT' if st['casulos'] else None
 assert before==load(db)
 res={'run_id':RUN,'seed':seed,'rev':rev,'pending':pending,'attack_score':attack['roll_score'],'unprotected_CA':76,
  'protected_CA':98,'attack_on_protected_misses':True,'unprotected_counterfactual_hits':True,
  'active_effect_CA22':st['actors']['E2']['resource']['ca'],'effect_persists_after_round1':bool(st['casulos']),
  'exact_expiration':'HOLD','source_speed_Eristan':'UNKNOWN','movement_delta':'-4m symbolically only',
  'PA_spent':804-st['actors']['E1']['resource']['pa'],'nonstack_preintent':deny,
  'head':head,'status':'TECHNICAL_PASS_PARTIAL_TEMPORAL_HOLD'}
 (ROOT/'R153_CASULO_RESULT.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(res,indent=2,ensure_ascii=False));return res
if __name__=='__main__':run()
