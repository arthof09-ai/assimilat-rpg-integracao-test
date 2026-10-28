"""R165 source-scoped Iskiel Flecha de Trava, explicit end-of-target-next-turn; current v0.8.1 controlled copy+R18.
Cocoon's '2 turnos' expiry stays normatively HOLD; not auto-used here.
"""
import sys,copy,hashlib,json,sqlite3
from pathlib import Path
from dataclasses import asdict
from fractions import Fraction
HERE=Path(__file__).parent
BASE=Path('/mnt/data/vlab_r161_work/baseline_r160')
STAGE=BASE/'r61_extracted'/'work'/'fusion_stage12'
NATIVE=HERE/'native_v081_controlled'
sys.path.insert(0,str(STAGE));sys.path.insert(0,str(NATIVE))
import vlab_r18_interactive as core
sys.modules.pop('vlab_effects_v08',None)
sys.path.insert(0,str(NATIVE))
from vlab_effects_v08 import (Combatant,Scene,AbilitySource,ActorActionState,FrozenRuleEvidence,EffectBlocked,
 begin_source_turn,end_source_turn,apply_weapon_attack,move_via_verified_path,effective_movement_speed,
 apply_flecha_trava_post_hit,expire_flecha_trava_next_turn)
from vlab_rd_v08 import Resistances
I_PAGE='3f6c2b324ede81a78a59d3d81fd5e966';A_PAGE='3ebc2b324ede814bb730d47dd7bd5f02';C_PAGE='3ebc2b324ede81f1be4be8804ac113c0'
seedlist=list(range(1185001,1189500))
def rolls(seed,who,term,index,n,faces):return core.dice(seed,index,'R165-'+who+'-'+term,n,faces)
def critical_seq(seed):return [rolls(seed,'I',f'FLECHA-CRIT-{i}',1,1,6)[0] for i in range(3)]
directed_candidates=[s for s in seedlist if critical_seq(s)[:2]==[6,6] and critical_seq(s)[2]>=5]
directed_seed=directed_candidates[2]  # V1 partial and V2 post-intent unresolved; do not re-run either
RUN=f'R165_FLECHA_TURN_EXPLICIT_V3_DEV_S{directed_seed}'
PREREG={'run':RUN,'seed':directed_seed,'development_filter':'third seed in 1185001..1189499 with ordered Iskiel Flecha critical positive 6,6,5 or 6; V1 partial and V2 UNKNOWN_EFFECT preserved; source-gated directed not holdout',
'source_is_kiel':'https://app.notion.com/p/'+I_PAGE,'source_auren':'https://app.notion.com/p/'+A_PAGE,
'Iskiel':'ON5, Vida514, PA livre484, Luta DES4d6+89, Flecha de Trava Standard55PA range<=65m 8d10+12 perforating +21 FF on hit',
'Auren':'L3, Vida523, PA719, CA225, physical RD35, ground speed16m, 6d6+193 physical lance damage8d8+211',
'scene_metric':'Iskiel at x=10m Auren at x=0m unobstructed horizontal line, 10m ranged attack, Auren moves toward x=9m within 10m debuffed speed, endpoint distance1m within adjacent melee',
'effect':'6m slow until END OF TARGET NEXT TURN, not immobilized, no stacking extrapolation',
'Casulo':'2 turnos expiration stays HOLD; not borrowed as authority for Flecha',
'censor':'one directed causal sequence, no victory/scientific random sample',
'negative_trial':'11m movement while slow 10m rejected before intent; 9m allowed and persisted',
'no_repeat':'R01-R160 immutable'}
P=HERE/'R165_PREREG_EXPLICIT_FLECHA_TEMPORAL_V3.json'
if P.exists():assert json.loads(P.read_text())==PREREG
else:P.write_text(json.dumps(PREREG,indent=2,ensure_ascii=False)+'\n')

def can(o):return json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def proof(page,rule):return (FrozenRuleEvidence(page,rule,hashlib.sha256((page+'|'+rule+'|R165_SOURCE_READ').encode()).hexdigest(),'2026-10-17_NOTION_READ','READ_ONLY_SOURCE_POINTER_NOT_CANON_FREEZE'),)

def source_state(st,who,target,kind):
 r=st['actors'][who]['resource'];page=I_PAGE if who=='I' else A_PAGE
 src=AbilitySource(f'R165-{who}-{kind}', 'move' if kind=='MOVE' else 'attack',
   'MOVEMENT' if kind=='MOVE' else 'STANDARD',page,kind,'RULE-DERIVED',
   required_pa=55 if kind=='FLECHA' else 0,target_scope='NONE' if kind=='MOVE' else 'ENEMY',
   effect_adapter_ready=True,effect_adapter_id='NATIVE-V081-CONTROLLED-R165')
 state=ActorActionState(who,20 if who=='I' else 23,r['pa'],(src.action_id,),standard_available=r['standard']==1,
 movement_available=r['movement']==1,reaction_available=r['reaction']==1,range_confirmed=True,los_confirmed=True,geometry_confirmed=True,
 enemy_ids_visible=(target,) if target else ())
 return src,state,proof(page,kind)

def hit_tape(st,who):
 seed=st['seed'];idx=st['action_nonce'][who]+1
 if who=='I':
  a_dice,flat,damage_groups,df=(4,89,[[8,10]],33);prefix='FLECHA'
 else:a_dice,flat,damage_groups,df=(6,193,[[8,8]],211);prefix='LANCE'
 hit=[rolls(seed,who,prefix+'-HIT',idx,a_dice,6)]
 crit=[rolls(seed,who,f'{prefix}-CRIT-{i}',idx,1,6)[0] for i in range(3)]
 dmg=[rolls(seed,who,f'{prefix}-DAMAGE-{i}',idx,n,f) for i,(n,f) in enumerate(damage_groups)]
 return {'who':who,'nonce':idx,'prefix':prefix,'hit':hit,'crit':crit,'dmg_rolls':dmg,
 'score':sum(hit[0])+flat,'damage':sum(map(sum,dmg))+df,'attack_bonus':flat,'damage_flat':df,'damage_groups':damage_groups}

def init():
 db=HERE/'runs'/f'{RUN}.sqlite';db.parent.mkdir(exist_ok=True)
 if db.exists():raise ValueError('NO_REPEAT')
 core.init_db(db,'A',directed_seed);st=core.initial('A',directed_seed)
 st.update({'scene':RUN,'run_id':RUN,'stage':'R165','seed':directed_seed,'phase':'ACTIVE','round':1,'order':['I','A'],'active':'I','turn_index':0,
 'action_nonce':{'I':0,'A':0},'source_prereg_sha':hashlib.sha256(P.read_bytes()).hexdigest(),
 'temporal_status':{'A':'NOT_ACTIVE'},'cocoon_expiration':'NORMATIVE_HOLD','actors':{}})
 for who,x in {'I':{'hp':514,'pa':484,'ca':132,'con':25,'rd':25,'position':'X10','speed':None,'rank':'Ouro Negro','reflex':2},
   'A':{'hp':523,'pa':719,'ca':225,'con':48,'rd':35,'position':'X0','speed':16,'rank':'Lendário','reflex':2}}.items():
  c=Combatant(who,x['hp'],x['pa'],x['ca'],x['con'],0,0,x['reflex'],x['position'],rank=x['rank'],standard=0,movement=0,reaction=1,
   maximum_hp=x['hp'],base_speed=x['speed'])
  obj=asdict(c);obj['ca']=int(obj['ca']);obj['base_speed']=int(obj['base_speed']) if obj['base_speed'] is not None else None
  st['actors'][who]={'resource':obj,'source':I_PAGE if who=='I' else A_PAGE,'physical_rd':x['rd']}
 anchor=core.sha({'genesis':st,'lineage':'R18_R26_V081_R165_SOURCE_SCOPED_EXPLICIT_END'})
 with core.connect(db) as con:
  for k,v in [('scene',RUN),('genesis',anchor),('head',anchor),('state',core.canonical(st))]:con.execute('update meta set value=? where key=?',(v,k))
 db.with_suffix('.genesis.json').write_text(core.canonical(st)+'\n')
 return db

def commit(db,kind,p):
 st,head,rev=core.load(db);a=st['active'];r=st['actors'][a]['resource']
 if kind=='START':assert p=={'actor':a} and r['standard']==0
 elif kind=='FLECHA':
  assert a=='I' and r['standard']==1 and r['pa']>=55 and p=={'tape':hit_tape(st,'I'),'target':'A','distance_m':10} and st['temporal_status']['A']=='NOT_ACTIVE'
 elif kind=='MOVE':
  assert a=='A' and r['movement']==1 and p.get('target')=='X9' and type(p.get('distance_m'))==int
  speed=Fraction(r['base_speed']-r['timed_source_speed_penalty_m']);assert p['distance_m']<=speed,'MOVEMENT_SLOW_PREINTENT_GATE'
 elif kind=='STRIKE':assert a=='A' and r['standard']==1 and r['position']=='X9' and p=={'tape':hit_tape(st,'A'),'target':'I','distance_m':1}
 elif kind=='END':assert p=={'actor':a} and r['standard']==0
 else:raise ValueError('NOT_REGISTERED_R165')
 cmd='LAB-CMD-R165-'+core.sha({'run':RUN,'rev':rev,'kind':kind,'payload':p})[:38]
 def reducer(s,q,seq):
  sc=Scene({x:Combatant(**v['resource']) for x,v in s['actors'].items()},seed=s['seed'],provenance='MESTRE_ONLY_SOURCE_ISKIEL_AUREN_R165')
  ev=[];who=s['active']
  if kind=='START':ev.append(begin_source_turn(sc,who))
  elif kind in ('FLECHA','STRIKE'):
   t=q['tape'];target=q['target'];src,state,pr=source_state(s,who,target,'FLECHA' if kind=='FLECHA' else 'LANCE')
   x=apply_weapon_attack(sc,who,target,source=src,state=state,proofs=pr,roll_score=t['score'],damage=t['damage'],damage_tag='perfurante',
    rd=Resistances(general=s['actors'][target]['physical_rd'],provenance='DOCUMENTED_PHYSICAL_RD_ONLY'),
    damage_dice_groups=tuple(map(tuple,t['damage_groups'])),damage_roll_groups=tuple(map(tuple,t['dmg_rolls'])),
    damage_fixed_bonus=t['damage_flat'],critical_sequence=tuple(t['crit']),attack_roll_attempts=tuple(map(tuple,t['hit'])),attack_bonus=t['attack_bonus'],
    lab_negative_critical_policy=True)
   ev.append(x);s['action_nonce'][who]+=1
   if kind=='FLECHA':
    ev.append(apply_flecha_trava_post_hit(sc,'I','A',x,source_page=I_PAGE));s['temporal_status']['A']='ACTIVE_UNTIL_END_OF_A_NEXT_TURN'
  elif kind=='MOVE':
   src,state,pr=source_state(s,'A',None,'MOVE')
   ev.append(move_via_verified_path(sc,'A',source=src,state=state,proofs=pr,destination='X9',
     path_evidence='R165_METRIC_10M_TO_1M_NOT_TOPOLOGY_SCALE',travel_cost=Fraction(9),speed=effective_movement_speed(sc.actors['A'])))
  elif kind=='END':
   ev.append(end_source_turn(sc,who))
   if who=='A' and s['temporal_status']['A']=='ACTIVE_UNTIL_END_OF_A_NEXT_TURN':
    ev.append(expire_flecha_trava_next_turn(sc,'A'));s['temporal_status']['A']='EXPIRED_AT_END_OF_TARGET_NEXT_OWN_TURN'
   s['turn_index']+=1;s['active']='A' if who=='I' else None
   if who=='A':s['phase']='ENDED_EXPLICIT_TEMPORAL_AFTER_A_TURN'
  for actor,x in sc.actors.items():
   z=asdict(x);z['ca']=int(z['ca']);z['base_speed']=int(z['base_speed']) if z['base_speed'] is not None else None
   s['actors'][actor]['resource']=z
  return {'native_actions':ev,'source_gate':'ISKIEL_55PA_PHYSICAL_HIT_TEMPORAL_EXPLICIT_NEXT_END',
    'time_policy':'NOT_GENERAL_TWO_TURN_RULE','actors_source':[I_PAGE,A_PAGE],
    'technical_non_canon':True}
 return core.event_commit(db,cmd,kind,p,reducer)

def run():
 db=init();cmds=[('START',{'actor':'I'})]
 for k,p in cmds:commit(db,k,p)
 st,_,_=core.load(db);commit(db,'FLECHA',{'tape':hit_tape(st,'I'),'target':'A','distance_m':10})
 commit(db,'END',{'actor':'I'})
 commit(db,'START',{'actor':'A'})
 before=core.load(db)
 try:commit(db,'MOVE',{'target':'X9','distance_m':11});raise AssertionError('11m wrongly accepted')
 except AssertionError as e:
  if 'MOVEMENT_SLOW_PREINTENT_GATE' not in str(e):raise
 assert core.load(db)==before
 slow=before[0]['actors']['A']['resource']
 assert slow['timed_source_speed_penalty_m']==6 and slow['base_speed']==16
 assert effective_movement_speed(Combatant(**slow))==10
 # Checkpoint prefix after effect active, before Auren action.
 with sqlite3.connect(db) as con,sqlite3.connect(db.with_name(db.stem+'_EFFECT_ACTIVE.checkpoint.sqlite')) as cp:con.backup(cp)
 commit(db,'MOVE',{'target':'X9','distance_m':9})
 st,_,_=core.load(db);commit(db,'STRIKE',{'tape':hit_tape(st,'A'),'target':'I','distance_m':1})
 commit(db,'END',{'actor':'A'})
 st,head,rev=core.load(db)
 assert st['actors']['A']['resource']['timed_source_speed_penalty_m']==0
 assert st['actors']['I']['resource']['pa']==429
 assert st['temporal_status']['A']=='EXPIRED_AT_END_OF_TARGET_NEXT_OWN_TURN'
 assert st['actors']['A']['resource']['base_speed']==16
 with sqlite3.connect(db) as con,sqlite3.connect(db.with_suffix('.checkpoint.sqlite')) as cp:con.backup(cp)
 assert core.load(db)==core.load(db.with_suffix('.checkpoint.sqlite'))
 out={'run':RUN,'seed':directed_seed,'commits':rev,'status':'EXPLICIT_NEXT_TURN_TEMPORAL_PASS_SOURCE_LIMITED',
  'critical_positive_is_kiel':True,'Iskiel_spent_PA':55,'target_base_speed_m':16,'target_during_effect_speed_m':10,
  'target_after_expiry_speed_m':16,'move9m_passed':True,'move11m_preintent_rejected':True,'target_Auren_hp':st['actors']['A']['resource']['hp'],
  'no_duplicate_intent':True,'cold_prefix_reopen':True,'turn_end_source':'Flecha Trava Until End of Target NEXT Turn',
  'casulo_2_turns_expiry':'SOURCE_HOLD_SEPARATE','head':head,'checkpoint_after':'PASS','pending':0}
 (HERE/'R165_EXPLICIT_TURN_TEMPORAL_RESULT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2));return out
if __name__=='__main__':run()
