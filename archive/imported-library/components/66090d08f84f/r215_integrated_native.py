"""R215 integration TEST: native attack + post-RD source defense + R50/R51 + 2v1 healing.
Only operates in a fresh copy of OP-VLAB-FUSION-SANDBOX-01. No historic runners.
"""
from __future__ import annotations
import copy, hashlib, json, random, math, sys
from dataclasses import asdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import vlab_r18_interactive as j
sys.modules.pop('vlab_effects_v08',None)
sys.path.insert(0,str(ROOT/'runtime/native'))
from vlab_effects_v08 import (Combatant, Scene, AbilitySource,FrozenRuleEvidence,ActorActionState,
    apply_weapon_attack,declare_counterattack,execute_declared_counterattack,begin_source_turn,end_source_turn,
    apply_reconstituicao_seiva,apply_pulso_estabilizacao,cast_source_specified_spell,EffectBlocked,Resistances)
PRE_BYTES=(ROOT/'sources/R215_PREREG.json').read_bytes();PRE=json.loads(PRE_BYTES);PH=hashlib.sha256(PRE_BYTES).hexdigest()
FROZEN=(ROOT/'sources/R44_R46_FROZEN_MASTER_SOURCE.json').read_bytes();FH=hashlib.sha256(FROZEN).hexdigest()
SRC=json.loads(FROZEN)['sources']
PAGES={**{k:SRC[k]['page'] for k in ('V','R','F')},'E':PRE['sources']['E']}
PROOFS={k:FrozenRuleEvidence(PAGES[k],'R215-FROZEN-SOURCE-BOUND',FH,'2026-10-21','NOTION-REOPEN-R215') for k in PAGES}
STANDARD={k:AbilitySource('R215-NORMAL-'+k,'attack','STANDARD',PAGES[k],PROOFS[k].rule_id,'RULE-DERIVED',target_scope='ENEMY',requires_range_check=True,effect_adapter_ready=True,effect_adapter_id='V081') for k in ('V','R','F')}
GUARD={k:AbilitySource('R215-GUARD-'+k,'reaction','REACTION',PAGES[k],PROOFS[k].rule_id,'RULE-DERIVED',required_pa=c,target_scope='SELF',reaction_trigger='POST_RD_BEFORE_HP',effect_adapter_ready=True,effect_adapter_id='V081') for k,c in [('V',50),('R',40)]}
COUNTER={k:AbilitySource('R215-COUNTER-'+k,'reaction','REACTION',PAGES[k],PROOFS[k].rule_id,'RULE-DERIVED',target_scope='SELF',reaction_trigger='ATTACK_DECLARED',effect_adapter_ready=True,effect_adapter_id='V081') for k in ['F','R']}
HEAL=AbilitySource('R215-E-RECONSTITUICAO','heal','STANDARD',PAGES['E'],PROOFS['E'].rule_id,'RULE-DERIVED',required_pa=75,target_scope='ALLY',effect_adapter_ready=True,effect_adapter_id='V081')
PULSE=AbilitySource('R215-E-PULSO','heal','REACTION',PAGES['E'],PROOFS['E'].rule_id,'RULE-DERIVED',required_pa=45,target_scope='ALLY',reaction_trigger='ALLY_AFTER_DAMAGE',effect_adapter_ready=True,effect_adapter_id='V081')
SPORES=AbilitySource('R215-E-SPORES','spell','STANDARD',PAGES['E'],PROOFS['E'].rule_id,'RULE-DERIVED',required_pa=80,target_scope='ENEMY',requires_range_check=True,effect_adapter_ready=True,effect_adapter_id='V081')
PA={'V':324,'R':344,'F':250,'E':804}
EHP=630; ECA=76; ERD=25
RD={'V':35,'R':30,'F':22,'E':25}
class Gate(Exception):pass

def dice(seed,tag,n,faces):
  h=hashlib.sha256(f'R215|{seed}|{tag}|{n}d{faces}'.encode()).digest()
  gen=random.Random(int.from_bytes(h,'big'))
  return tuple(gen.randint(1,faces) for _ in range(n))

def actor(k, initial_active=False):
  if k=='E':hp=EHP;ca=ECA;con=45
  else:hp=SRC[k]['hp'];ca=SRC[k]['ca'];con={'V':57,'R':57,'F':24}[k]
  return Combatant(k,hp,PA[k],ca,con,0,0,0,'(0,0)' if k!='R' else '(1.5,0)',rank='Ouro Negro',maximum_hp=hp,standard=0,movement=1,reaction=1)

def initialize(db,seed,suite,policy,order):
  if db.exists():raise Gate('NO_REUSE_DB')
  j.init_db(str(db),'A',seed);st=j.initial('A',seed)
  st.update({'scene':f'R215-{suite}-{seed}-{policy}','seed':seed,'phase':'ACTIVE','round':1,'turn':0,
    'active':order[0], 'order':order, 'suite':suite,'policy':policy, 'actors':{k:asdict(actor(k)) for k in order},
    'native_events':[], 'r215':{'prereg_hash':PH,'source_sha':FH,'source_status':'MESTRE-SIDE-PROPOSED','world_block_size':'UNKNOWN',
      'adjacency_contract':'R44-DECLARED-FIXTURE-NOT-METRIC-NORM','attack_range_fixture':True,'stats':{'attacks':0,'hits':0,'damage':0,
        'guard':0,'guard_pa':0,'guard_prevented':0,'counter_declare':0,'counter_response':0,'cures':0,'healed':0,'heal_pa':0,
        'spells':0,'spore_damage':0,'reaction_heals':0},'turns':{k:0 for k in order},'policy_trace':[]}})
  con=j.connect(str(db));h=j.sha({'seed':seed,'suite':suite,'policy':policy,'prereg':PH})
  with con:
    for k,v in [('state',j.canonical(st)),('scene',st['scene']),('genesis',h),('head',h)]:con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
  con.close()

def scene_of(st):return Scene({k:Combatant(**copy.deepcopy(v)) for k,v in st['actors'].items()},events=copy.deepcopy(st['native_events']),seed=st['seed'],provenance='R215-MESTRE-TEST')
def synch(st,s):
  st['native_events']=copy.deepcopy(s.events)
  for k,c in s.actors.items():st['actors'][k]=asdict(c)

def turn_state(k,src,target):return ActorActionState(k,20,PA[k],(src.action_id,),standard_available=True,range_confirmed=True,enemy_ids_visible=(target,))
def guard_state(k,src,current_pa):return ActorActionState(k,20,current_pa,(src.action_id,),reaction_available=True,reaction_trigger_observed='POST_RD_BEFORE_HP')
def counter_state(k,src,current_pa):return ActorActionState(k,20,current_pa,(src.action_id,),reaction_available=True,reaction_trigger_observed='ATTACK_DECLARED')

def hit_tape(seed,tag,k):
  a=SRC[k];n,f=a['rank_dice'];dn,df=a['damage_dice'];return {'hit':(dice(seed,tag+'H',n,f),),'crit':dice(seed,tag+'C',3,6),'damage':(dice(seed,tag+'D',dn,df),)}

def normal_attack(s,seed,who,target,tag,guard_policy=False):
  src=STANDARD[who];a=SRC[who];t=hit_tape(seed,tag,who);score=sum(t['hit'][0])+a['attack_bonus'];gross=sum(t['damage'][0])+a['damage_bonus']
  critical='POSITIVE' if t['crit'][:2]==(6,6) and t['crit'][2]>=5 else 'NEGATIVE' if t['crit'][:2]==(1,1) and t['crit'][2]<=2 else 'NONE'
  hit=(score>s.actors[target].ca or critical=='POSITIVE') and critical!='NEGATIVE'
  crit_extra=sum(x*y for x,y in (tuple(a['damage_dice']),)) if critical=='POSITIVE' and hit else 0
  net_before_guard=max(0,gross+crit_extra-RD[target]) if hit else 0
  guard=None
  if guard_policy and target in GUARD and net_before_guard>0:
    already=any(e.get('action')=='R215_POST_RD_GUARD' and e.get('by')==target for e in s.events)
    if s.actors[target].reaction and s.actors[target].pa>=GUARD[target].required_pa and not already:
      source=GUARD[target]
      guard={'source':source,'state':guard_state(target,source,s.actors[target].pa),'proofs':(PROOFS[target],),
        'cost':source.required_pa,'limit':70 if target=='V' else 50,'defender_source_page':PAGES[target]}
  s.record({'action':'R215_OFFENSIVE_RNG','by':who,'to':target,'stream':f'R215|{seed}|{tag}',
            'attack_attempts':t['hit'],'crit':t['crit'],'damage_rolls':t['damage']})
  result=apply_weapon_attack(s,who,target,source=src,state=turn_state(who,src,target),proofs=(PROOFS[who],),
    roll_score=score,damage=gross,damage_tag='impacto' if who=='V' else 'perfurante' if who=='R' else 'cortante',
    rd=Resistances(general=RD[target],provenance='R215-REOPEN-ON5'),damage_dice_groups=(tuple(a['damage_dice']),),
    damage_roll_groups=t['damage'],damage_fixed_bonus=a['damage_bonus'],critical_sequence=t['crit'],attack_roll_attempts=t['hit'],attack_bonus=a['attack_bonus'],
    attack_origin='NORMAL',lab_negative_critical_policy=True,post_rd_guard=guard)
  return result, guard

def declare_counter(s,target,who):
  src=COUNTER[target]
  if s.actors[target].reaction!=1:return None
  return declare_counterattack(s,target,who,source=src,state=counter_state(target,src,s.actors[target].pa),
        proofs=(PROOFS[target],),declared_before=True,attack_origin='NORMAL')

def resolve_counter(s,seed,target,who,incoming,dec,tag):
  if incoming['hit']:
    return execute_declared_counterattack(s,target,who,declaration=dec,incoming=incoming,
      attack_attempts=((1,),(1,)),attack_bonus=0,critical_sequence=(1,2,3),damage_groups=((1,6),),damage_roll_groups=((1,),),flat=0,
      damage_tag='cortante',rd=Resistances(general=RD[who]))
  t=hit_tape(seed,tag+'-COUNTER',target)
  t2=(dice(seed,tag+'-COUNTER-H1',4,6),dice(seed,tag+'-COUNTER-H2',4,6))
  s.record({'action':'R215_COUNTER_RNG','by':target,'to':who,'after_declaration':dec['seq'],'rolls':t2,'crit':t['crit'],'damage':t['damage']})
  return execute_declared_counterattack(s,target,who,declaration=dec,incoming=incoming,
      attack_attempts=t2,attack_bonus=SRC[target]['attack_bonus'],critical_sequence=t['crit'],damage_groups=(tuple(SRC[target]['damage_dice']),),
      damage_roll_groups=t['damage'],flat=SRC[target]['damage_bonus'],damage_tag='cortante' if target=='F' else 'perfurante',
      rd=Resistances(general=RD[who],provenance='R215-REOPEN-ON5'))

def heal_reaction(s,seed,tag,damaged):
  he=s.actors['E'];al=s.actors[damaged]
  if al.hp<=0 or al.hp>=al.maximum_hp or he.reaction!=1 or he.pa<45:return None
  src=PULSE;rr=dice(seed,tag+'-PULSE',3,10)
  s.record({'action':'R215_SUPPORT_DECISION','by':'E','to':damaged,'trigger':'ALLY_AFTER_DAMAGE','ally_hp':al.hp,
            'max_hp':al.maximum_hp,'known_reaction':he.reaction,'decision':'PULSO'})
  return apply_pulso_estabilizacao(s,'E',damaged,source=src,state=ActorActionState('E',20,he.pa,(src.action_id,),
        reaction_available=True,reaction_trigger_observed='ALLY_AFTER_DAMAGE',ally_ids_visible=(damaged,)),proofs=(PROOFS['E'],),
        dice_rolls=rr,range_met=True,damage_just_resolved=True,gloves_equipped=True)

def heal_standard(s,seed,tag,damaged):
  src=HEAL;rr=dice(seed,tag+'-RECONST',8,10);he=s.actors['E']
  s.record({'action':'R215_SUPPORT_DECISION','by':'E','to':damaged,'decision':'RECONSTITUICAO',
      'ally_hp':s.actors[damaged].hp,'max_hp':s.actors[damaged].maximum_hp,'known_PA':he.pa})
  return apply_reconstituicao_seiva(s,'E',damaged,source=src,state=ActorActionState('E',20,he.pa,(src.action_id,),standard_available=True,ally_ids_visible=(damaged,)),
    proofs=(PROOFS['E'],),dice_rolls=rr,range_met=True,gloves_equipped=True)

def spores(s,seed,tag):
  # E at (0,0), V at (0,0), R at (1.5,0); center (6,0), radius5. Only R inside.
  assert math.dist((6,0),(1.5,0))<=5 and math.dist((6,0),(0,0))>5
  rr=dice(seed,tag+'-SPORES-DMG',10,10);save=dice(seed,tag+'-SPORES-SAVE',4,6)
  # Arveth equipped CON57, pure attribute save (not Fortitude trained 4d6+59).
  passed=sum(save)+57>76;damage=sum(rr)+10
  if passed and damage%2:raise Gate('UNKNOWN_HALF_ODD_ROUNDING_SOURCE_HOLD')
  s.record({'action':'R215_SPORES_GEOMETRY_AND_SAVE','by':'E','to':'R','center':[6,0],
    'radius':5,'positions':{'E':[0,0],'V':[0,0],'R':[1.5,0]},'included':['R'],'excluded':['V','E'],
    'fort_pure_rolls':save,'fort_pure_total':sum(save)+57,'spell_cd':76,'passed':passed,'rolls':rr})
  src=SPORES;res=cast_source_specified_spell(s,'E','R',source=src,state=ActorActionState('E',20,s.actors['E'].pa,(src.action_id,),standard_available=True,range_confirmed=True,enemy_ids_visible=('R',)),
       proofs=(PROOFS['E'],),damage=damage,damage_tag='planta',rd=Resistances(general=0,provenance='R209-TEST-MAGIC-RD-UNKNOWN'),
       explicit_save_effect='SAVE-HALF',target_save_exceeds_cd=passed,damage_rolls=rr,damage_faces=10,documented_flat_bonus=10)
  return res

def reducer(st,p,seq):
  if st['phase']!='ACTIVE' or p['seed']!=st['seed'] or p['prereg']!=PH or p['who']!=st['active']:raise Gate('TURN_PREFLIGHT_INVALID')
  who=p['who'];suite=st['suite'];policy=st['policy'];s=scene_of(st);begin_source_turn(s,who)
  x=st['r215']['stats'];prev=len(s.events);target=None;dec=None
  if suite=='GUARD':
    target='R' if who=='V' else 'V'
    atk,guard=normal_attack(s,st['seed'],who,target,f'G-{policy}-ROUND{st["round"]}-{who}',guard_policy=(policy=='FIRST_DAMAGE_GUARD'))
    x['attacks']+=1;x['hits']+=int(atk['hit']);x['damage']+=atk['hp_loss_actual']
    if guard:x['guard']+=1;x['guard_pa']+=guard['cost'];x['guard_prevented']+=atk['post_rd_guard_reduction']
  elif suite=='COUNTER':
    target='F' if who=='R' else 'R'
    if who=='R':dec=declare_counter(s,target,who);x['counter_declare']+=1
    atk,guard=normal_attack(s,st['seed'],who,target,f'C-{st["round"]}-{who}')
    x['attacks']+=1;x['hits']+=int(atk['hit']);x['damage']+=atk['hp_loss_actual']
    if dec:
      r=resolve_counter(s,st['seed'],target,who,atk,dec,f'C-{st["round"]}-{who}')
      if r['action']=='COUNTER_RESPONSE':x['counter_response']+=1;x['damage']+=r['before_hp']-r['after_hp']
  elif suite=='TEAM':
    if who=='V':
      atk,_=normal_attack(s,st['seed'],who,'R',f'T-{policy}-ROUND{st["round"]}-V')
      x['attacks']+=1;x['hits']+=int(atk['hit']);x['damage']+=atk['hp_loss_actual']
    elif who=='R':
      # Opponent pre-registered target selection: primary defender V while standing.
      atk,_=normal_attack(s,st['seed'],'R','V',f'T-{policy}-ROUND{st["round"]}-R')
      x['attacks']+=1;x['hits']+=int(atk['hit']);x['damage']+=atk['hp_loss_actual']
      if atk['hp_loss_actual']>0 and s.actors['V'].hp>0 and s.actors['E'].reaction==1:
        if policy=='PROTECTIVE':
          rx=heal_reaction(s,st['seed'],f'T-{st["round"]}', 'V');x['reaction_heals']+=1;x['healed']+=rx['actual_heal'];x['heal_pa']+=45;x['cures']+=1
    else:
      missing=s.actors['V'].maximum_hp-s.actors['V'].hp
      threshold=PRE['team_decision_thresholds'][policy]
      if missing>=threshold and s.actors['V'].hp>0:
        result=heal_standard(s,st['seed'],f'T-{policy}-{st["round"]}','V');x['cures']+=1;x['healed']+=result['actual_healed'];x['heal_pa']+=75
      else:
        result=spores(s,st['seed'],f'T-{policy}-{st["round"]}');x['spells']+=1;x['spore_damage']+=result['hp_before']-result['hp_after']
  else:raise Gate('UNKNOWN_SUITE')
  end_source_turn(s,who)
  xturn=st['r215']['turns'];xturn[who]+=1
  st['turn']+=1
  # Respect KO before granting another turn.
  alive_primary=all(s.actors[z].hp>0 for z in (('V','R') if suite!='COUNTER' else ('R','F')))
  if not alive_primary:
    st['phase']='KO_HP0';st['active']=None
  elif who==st['order'][-1] and st['round']>=PRE['max_rounds'][suite.lower()]:
    st['phase']='CENSORED_HORIZON';st['active']=None
  else:
    i=st['order'].index(who)
    if i==len(st['order'])-1:st['round']+=1
    st['active']=st['order'][(i+1)%len(st['order'])]
  synch(st,s)
  return {'suite':suite,'who':who,'phase':st['phase'],'events_added':s.events[prev:],'turn':st['turn']}

def run_suite(suite,policy,seed):
  order={'GUARD':['V','R'],'COUNTER':['R','F'],'TEAM':['V','R','E']}[suite]
  db=ROOT/'evidence/db'/f'R215_{suite}_{policy}_S{seed}.sqlite'
  initialize(db,seed,suite,policy,order)
  steps=PRE['max_rounds'][suite.lower()]*len(order)
  for ix in range(steps):
    st,_,_=j.load(db)
    if st['phase']!='ACTIVE':break
    payload={'who':st['active'],'seed':seed,'prereg':PH}
    j.event_commit(str(db),f'LAB-CMD-R215-{suite}-{policy}-{seed}-T{ix+1}','R215_NATIVE_INTEGRATED_TURN',payload,reducer)
  st,head,rev=j.load(db)
  return {'suite':suite,'policy':policy,'seed':seed,'db':db.name,'rev':rev,'head':head,
    'outcome':st['phase'],'stats':st['r215']['stats'],'turns':st['r215']['turns'],'hp':{k:v['hp'] for k,v in st['actors'].items()},
    'pa':{k:v['pa'] for k,v in st['actors'].items()},'events':len(st['native_events'])}

def main():
  out=[]
  for seed in PRE['suite_guard_seeds']:
    for pol in PRE['guard_policies']:out.append(run_suite('GUARD',pol,seed))
  for seed in PRE['suite_counter_seeds']:out.append(run_suite('COUNTER','PREDECLARE',seed))
  for seed in PRE['suite_team_seeds']:
    for pol in PRE['team_policies']:out.append(run_suite('TEAM',pol,seed))
  (ROOT/'evidence/R215_RUN_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
  print(json.dumps({'runs':len(out),'commits':sum(x['rev'] for x in out),'outcomes':{v:sum(x['outcome']==v for x in out) for v in {x['outcome'] for x in out}},
    'suites':{k:sum(x['suite']==k for x in out) for k in ('GUARD','COUNTER','TEAM')},'attacks':sum(x['stats']['attacks'] for x in out),
    'guards':sum(x['stats']['guard'] for x in out),'counter_responses':sum(x['stats']['counter_response'] for x in out),
    'heals':sum(x['stats']['cures'] for x in out),'spells':sum(x['stats']['spells'] for x in out)},indent=2))
if __name__=='__main__':main()
