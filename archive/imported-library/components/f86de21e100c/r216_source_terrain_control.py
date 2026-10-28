"""Source-gated terrain control R216C: Eristan's Raizes, then native movement/attack.
NOT a Beast control nor official world grid; effects in isolated TEST copies only.
"""
import json,hashlib,sys,copy,math
from dataclasses import asdict
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'code'),str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import vlab_r18_interactive as j
import r216_dynamic_multi_actor as base
from vlab_effects_v08 import (Scene,Combatant,AbilitySource,ActorActionState,begin_source_turn,end_source_turn,move_via_verified_path,_require_option)
PREB=(ROOT/'sources/R216_CONTROL_PREREG.json').read_bytes();PRE=json.loads(PREB);PH=hashlib.sha256(PREB).hexdigest()
RAIZES=AbilitySource('R216-ERISTAN-RAIZES-REFUGIO','control','STANDARD',base.old.PAGES['E'],base.E_PROOF.rule_id,'RULE-DERIVED',required_pa=85,
 target_scope='AREA-ENEMY',max_targets=1,requires_range_check=True,effect_adapter_ready=True,effect_adapter_id='R216-RAIZES-SOURCE-LAB')
MOVE=base.MOVE

def init(db,kind):
 rec=PRE[kind];seed=rec['seed'];j.init_db(str(db),'A',seed);st=j.initial('A',seed)
 actors={k:asdict(base.old.actor(k)) for k in ['E','R','V']}
 for k in actors:actors[k]['position']=str(tuple(rec[k]));actors[k]['standard']=0
 st.update({'scene':'R216-RAIZES-'+kind,'seed':seed,'phase':'ACTIVE','active':'E','turn':0,'order':['E','R'],'actors':actors,'native_events':[],
  'r216ctrl':{'pre_hash':PH,'case':kind,'zone':None,'status':'NOT_CAST','source':'ERISTAN_PROPOSED','world_meters_per_block':'UNKNOWN'}})
 c=j.connect(str(db));h=j.sha({'kind':kind,'seed':seed,'pre':PH})
 with c:
  for k,v in [('state',j.canonical(st)),('scene',st['scene']),('genesis',h),('head',h)]:c.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 c.close()

def reducer(st,p,seq):
 if st['phase']!='ACTIVE' or p['pre']!=PH or p['actor']!=st['active']:raise ValueError('CTRL_PREFLIGHT')
 s=Scene({k:Combatant(**copy.deepcopy(v)) for k,v in st['actors'].items()},events=copy.deepcopy(st['native_events']),seed=st['seed'],provenance='R216-TERRAIN-CONTROL-TEST')
 k=p['actor'];rec=PRE[st['r216ctrl']['case']];before=len(s.events);begin_source_turn(s,k)
 if k=='E':
  center=rec['center'];p0=base.coords(s.actors['E'].position)
  if math.dist(p0,center)>20:raise ValueError('CAST_CENTER_OUT_OF_RANGE')
  # No ally is given arbitrary immunity: all observed actors are physically outside except target.
  inc=[a for a in ['E','R','V'] if math.dist(base.coords(s.actors[a].position),center)<=4+1e-9]
  if inc != (['R'] if st['r216ctrl']['case']=='inside' else []):raise ValueError('UNEXPECTED_GEOMETRY_PRE')
  sa=ActorActionState('E',20,s.actors['E'].pa,(RAIZES.action_id,),standard_available=True,geometry_confirmed=True,range_confirmed=True,
    enemy_ids_visible=('R',),known_area_targets=('R',))
  _require_option(s,'E',RAIZES,sa,(base.E_PROOF,),target=None)
  if s.actors['E'].pa<85 or s.actors['E'].standard!=1:raise ValueError('NO_RAIZES_ACTION')
  s.actors['E'].pa-=85;s.actors['E'].standard=0
  st['r216ctrl']['zone']={'by':'E','center':center,'radius':4,'fresh':True,'duration_literal':'1 turno','expiry_beyond_observed_target_turn':'HOLD'}
  s.record({'action':'R216_RAIZES_SOURCE_CAST','by':'E','PA_spent':85,'standard_spent':1,'center':center,'radius':4,
   'included_before_target_turn':inc,'source':'ERISTAN_ON5_NOTION_PRIMARY','area_no_extra_damage':True,'duration_literal':'1 turno'})
  st['active']='R'
 elif k=='R':
  zone=st['r216ctrl']['zone'];center=zone['center'];pos=base.coords(s.actors['R'].position)
  within=math.dist(center,pos)<=4+1e-9
  if within:
   rolls=base.old.dice(st['seed'],'R216-RAIZES-REFLEXO',4,6);score=sum(rolls)+23;save_ok=score>76
   s.record({'action':'R216_RAIZES_SAVE_AT_TURN_START','by':'R','source':'ERISTAN','center':center,'position':pos,
    'rolls':rolls,'attribute_DES':23,'total':score,'CD':76,'success':save_ok})
   if not save_ok:
    s.actors['R'].immobile_next_own_turns=1
    s.record({'action':'R216_RAIZES_MOVEMENT_RESTRICTED','by':'R','movement_legal':False,'cause':'FAILED_REFLEX','duration':'THIS_OBSERVED_TARGET_TURN',
      'no_HP_loss':True,'no_movement_debit':True})
  else:
   s.record({'action':'R216_RAIZES_NO_TRIGGER','by':'R','position':pos,'radius':4,'center':center,'no_save':True})
  if s.actors['R'].immobile_next_own_turns==0:
   dst=rec['move_R_to'];mv=move_via_verified_path(s,'R',source=MOVE,state=ActorActionState('R',20,s.actors['R'].pa,(MOVE.action_id,),movement_available=True,geometry_confirmed=True,environment_contract=True),
    proofs=(base.old.PROOFS['V'],),destination=str(tuple(dst)),path_evidence='R216-CTRL-OPEN-1M-PATH-FIXTURE',travel_cost=Fraction(1),speed=Fraction(4))
   assert math.dist(base.coords(mv['from']),base.coords(mv['to']))<=1+1e-9
  at,_=base.old.normal_attack(s,st['seed'],'R','V',f'R216-CONTROL-{st["r216ctrl"]["case"]}-ATTACK',guard_policy=False)
  s.record({'action':'R216_RAIZES_ATTACK_CONTINUES','by':'R','movement_condition':within,'attack_source':'NATIVE_V081',
    'attack_seq':at['seq'],'attack_hit':at['hit'],'effective_HP_loss':at['hp_loss_actual']})
  st['phase']='CENSORED_CONTROL_WINDOW';st['active']=None;st['r216ctrl']['status']='ONE_TARGET_TURN_OBSERVED'
 else:raise ValueError('WRONG_ACTOR')
 end_source_turn(s,k)
 st['native_events']=copy.deepcopy(s.events)
 for a,c in s.actors.items():st['actors'][a]=asdict(c)
 st['turn']+=1
 return {'who':k,'events_added':s.events[before:],'state':st['r216ctrl']['status']}

def run(kind):
 seed=PRE[kind]['seed'];path=ROOT/'evidence/db'/f'R216_CTRL_{kind.upper()}_S{seed}.sqlite'
 if path.exists():raise ValueError('COLLISION')
 init(path,kind)
 for i,k in enumerate(['E','R'],1):
  j.event_commit(str(path),f'LAB-CMD-R216-CONTROL-{kind}-{seed}-{i}','R216_CONTROL_NATIVE_TURN',{'pre':PH,'actor':k},reducer)
 st,head,rev=j.load(path)
 return {'case':kind,'seed':seed,'db':path.name,'commits':rev,'events':len(st['native_events']),
  'hp':{a:x['hp'] for a,x in st['actors'].items()},'pa':{a:x['pa'] for a,x in st['actors'].items()},
  'R_move_remaining':st['actors']['R']['movement'],'R_pos':st['actors']['R']['position'],'status':st['phase']}
if __name__=='__main__':
 v=[]
 for case in ['inside','outside']:v.append(run(case))
 (ROOT/'evidence/reports/R216_CONTROL_RESULTS.json').write_text(json.dumps(v,indent=2,ensure_ascii=False));print(json.dumps(v,indent=2,ensure_ascii=False))
