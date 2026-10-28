"""R214 incremental native reaction-intent adapter + R49 priority + bilateral v081 combat; MESTRE-ONLY TEST.
Historical sources are snapshots and are not normalized or canonized.
"""
from __future__ import annotations
import copy,hashlib,json,math,random,sys
from dataclasses import asdict
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import vlab_r18_interactive as j
import vlab_r26_master_rulings as r26
sys.modules.pop('vlab_effects_v08',None)
sys.path.insert(0,str(ROOT/'runtime/native'))
from vlab_effects_v08 import (Combatant,Scene,AbilitySource,FrozenRuleEvidence,ActorActionState,EffectBlocked,
  apply_weapon_attack,move_via_verified_path,declare_opportunity_reaction,begin_source_turn,end_source_turn,Resistances)
SRC=json.loads((ROOT/'sources/R44_R46_FROZEN_MASTER_SOURCE.json').read_text())['sources']
PRE_B=(ROOT/'sources/R214_PREREG.json').read_bytes(); PRE=json.loads(PRE_B); PH=hashlib.sha256(PRE_B).hexdigest()
SP=(ROOT/'sources/R44_R46_FROZEN_MASTER_SOURCE.json').read_bytes(); SH=hashlib.sha256(SP).hexdigest()
RULE='3ebc2b32-4ede-81f1-be4b-e8804ac113c0'
PROOF=FrozenRuleEvidence(RULE,'R214-R44-FIXTURE-EDGE',SH,'2026-10-20','R44-R49-COLD-HISTORIC')
PROOFS={k:FrozenRuleEvidence(SRC[k]['page'],PROOF.rule_id,SH,'2026-10-20','R44-R49-COLD-HISTORIC') for k in ['F','V','R']}
MOVE=AbilitySource('R214-NATIVE-MOVE','move','MOVEMENT',RULE,PROOF.rule_id,'RULE-DERIVED',target_scope='POSITION',effect_adapter_ready=True,effect_adapter_id='V081')
AOO={k:AbilitySource('R214-AOO-'+k,'attack','REACTION',SRC[k]['page'],PROOF.rule_id,'RULE-DERIVED',target_scope='ENEMY',reaction_trigger='EXIT_ADJACENT',effect_adapter_ready=True,effect_adapter_id='V081') for k in ['F','V']}
NORM={k:AbilitySource('R214-NORMAL-'+k,'attack','STANDARD',SRC[k]['page'],PROOF.rule_id,'RULE-DERIVED',target_scope='ENEMY',requires_range_check=True,effect_adapter_ready=True,effect_adapter_id='V081') for k in ['V','R']}
CASE_SEEDS=PRE['aoo_cases']
class Gate(Exception):pass

def dice(seed,label,n,faces):
 entropy=hashlib.sha256(f'R214|{seed}|{label}|{n}d{faces}'.encode()).digest()
 rr=random.Random(int.from_bytes(entropy,'big'))
 return tuple(rr.randint(1,faces) for _ in range(n))

def tape(seed,who,tag):
 a=SRC[who];n,f=a['rank_dice'];dn,df=a['damage_dice']
 return {'crit':dice(seed,tag+'-'+who+'-CRIT',3,6),
   'attempts':(dice(seed,tag+'-'+who+'-HIT0',n,f),dice(seed,tag+'-'+who+'-HIT1',n,f)),
   'damage':(dice(seed,tag+'-'+who+'-DAMAGE',dn,df),)}

def source_actor(id,kind,pos,hp=None):
 a=SRC[kind];c=Combatant(id,hp if hp is not None else a['hp'],None,a['ca'],0,0,0,0,str(tuple(pos)),
   rank='Ouro Negro' if kind!='G' else 'Bronze',maximum_hp=a['hp'],standard=1,movement=1,reaction=1,base_speed='3')
 return {'resource':asdict(c),'source_kind':kind,'source_page':a['page']}

def init(db,seed,case):
 j.init_db(str(db),'A',seed);st=j.initial('A',seed)
 st.update({'scene':'R214-'+case+'-'+str(seed),'seed':seed,'phase':'ACTIVE','round':1,'turn':0,
   'active':'R','actors':{},'native_events':[],'r214':{'case':case,'phash':PH,
    'adjacency':'R44-EXPLICIT-FIXTURE-NOT-METRIC-NORM','world_block_size':'UNKNOWN',
    'interrupt_movement_cost':'UNKNOWN_EFFECT_HOLD','stats':{'windows':0,'aoo':0,'reactions':0,'hits':0,'hp_loss':0,'moves':0,'misses':0},'rng_log':[]}})
 if case=='MISS':
  actors={'R':source_actor('R','F',[0,0]),'A':source_actor('A','F',[1.5,0])}
 elif case=='SPENT_CHAIN':
  actors={'R':source_actor('R','R',[0,0]),'G':source_actor('G','G',[0,0]),'F':source_actor('F','F',[1.5,0])}
 elif case=='NO_ADJ':
  actors={'R':source_actor('R','R',[0,0]),'F':source_actor('F','F',[12,0])}
 elif case=='TIE':
  actors={'R':source_actor('R','R',[0,0]),'A':source_actor('A','F',[1.5,0]),'B':source_actor('B','F',[0,1.5])}
 elif case=='LETHAL':
  actors={'R':source_actor('R','G',[0,0]),'F':source_actor('F','F',[1.5,0]),'V':source_actor('V','V',[0,1.5])}
 else:
  actors={'R':source_actor('R','R',[0,0]),'F':source_actor('F','F',[1.5,0]),'V':source_actor('V','V',[0,1.5])}
 st['actors']=actors
 con=j.connect(str(db));h=j.sha({'preregistered':PH,'seed':seed,'case':case})
 with con:
  for k,v in [('state',j.canonical(st)),('scene',st['scene']),('genesis',h),('head',h)]:con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 con.close()

def from_state(st):
 return Scene({k:Combatant(**copy.deepcopy(v['resource'])) for k,v in st['actors'].items()},events=copy.deepcopy(st['native_events']),seed=st['seed'],provenance='R214-TEST-CONDITIONAL')

def sync(st,s):
 st['native_events']=copy.deepcopy(s.events)
 for k,c in s.actors.items():st['actors'][k]['resource']=asdict(c)

def aoo_context(s,att,target):
 src=AOO[att[1]]
 return ActorActionState(att[0],20,None,(src.action_id,),reaction_available=True,
    reaction_trigger_observed='EXIT_ADJACENT',range_confirmed=True,enemy_ids_visible=(target,))

def priority(s,seed,actors,stats):
 assert actors
 desc={k:SRC[stats[k]]['des'] for k in actors}
 if len(actors)==1:return actors,[]
 if len(set(desc.values()))==len(actors):return sorted(actors,key=lambda k:desc[k],reverse=True),[]
 log=[]
 def reroll(actor,ordinal):
  rolls=dice(seed,'PRIORITY-'+actor+'-ROUND'+str(ordinal),4,6)
  log.append({'actor':actor,'round':ordinal,'dice':rolls,'sum':sum(rolls),'rank':'ON5'})
  return sum(rolls)
 by_des={}
 for a in actors:by_des.setdefault(desc[a],[]).append(a)
 out=[]
 for d in sorted(by_des,reverse=True):
  tied=by_des[d]
  if len(tied)==1:out.extend(tied)
  else:
   # R49 / R26 tie_order exact native history; never sort actor IDs as fallback.
   result=r26.tie_order([{'id':a,'total':0,'des':d} for a in tied],reroll)
   out.extend(result['order'])
 return out,log

def attack(s,seed,att,target,tag,intent_seq=None,origin='OPPORTUNITY'):
 sk={'A':'F','B':'F'}.get(att,att)
 a=SRC[sk];t=tape(seed,sk,tag+'-'+att)
 src=AOO[sk] if origin=='OPPORTUNITY' else NORM[sk]
 before=len(s.events)
 s.record({'action':'r214_offensive_rng_generated','by':att,'to':target,
   'intent_seq':intent_seq,'crit':t['crit'],'attack_attempts':t['attempts'],'damage_roll_groups':t['damage'],
   'source_tape_stream':f'R214|{seed}|{tag}-{att}'})
 att_bonus=a['attack_bonus'];sc=max(sum(x) for x in t['attempts'])+att_bonus+2 if origin=='OPPORTUNITY' else sum(t['attempts'][0])+att_bonus
 state=(ActorActionState(att,20,None,(src.action_id,),reaction_available=True,reaction_trigger_observed='EXIT_ADJACENT',range_confirmed=True,enemy_ids_visible=(target,))
   if origin=='OPPORTUNITY' else ActorActionState(att,20,None,(src.action_id,),standard_available=True,range_confirmed=True,enemy_ids_visible=(target,)))
 defender=s.actors[target];proof=PROOFS[sk]
 result=apply_weapon_attack(s,att,target,source=src,state=state,proofs=(proof,),roll_score=sc,
  damage=sum(t['damage'][0])+a['damage_bonus'],damage_tag=a['damage_kind'].split('/')[0],
  rd=Resistances(general=SRC[{'A':'F','B':'F'}.get(target,target)]['rd'],provenance='R44-FROZEN-TEST'),
  damage_dice_groups=(tuple(a['damage_dice']),),damage_roll_groups=t['damage'],damage_fixed_bonus=a['damage_bonus'],
  critical_sequence=t['crit'],attack_roll_attempts=t['attempts'] if origin=='OPPORTUNITY' else (t['attempts'][0],),
  attack_bonus=att_bonus,advantage_levels=1 if origin=='OPPORTUNITY' else 0,
  attack_origin=origin,opportunity_intent_seq=intent_seq,lab_negative_critical_policy=True)
 return result

def preflight_window(st,mover,adj,exits):
 if st['phase']!='ACTIVE' or st['active']!=mover:raise Gate('OUT_OF_TURN')
 if mover not in st['actors']:raise Gate('MOVER_ABSENT')
 m=st['actors'][mover]['resource']
 if m['hp']<=0 or m['movement']!=1:raise Gate('MOVER_NO_MOVEMENT')
 if not set(exits).issubset(set(adj)):raise Gate('EXIT_EDGE_NOT_DECLARED')
 if any(a not in st['actors'] for a in adj):raise Gate('ADJACENT_ACTOR_ABSENT')
 return True

def window(st,p,seq):
 case=st['r214']['case'];seed=st['seed'];mover=p['mover'];adj=p['adj'];exits=p['exits']
 if p['phash']!=PH or p['case']!=case:raise Gate('SOURCE_PREREG_DRIFT')
 preflight_window(st,mover,adj,exits)
 s=from_state(st);m=s.actors[mover];stats={k:st['actors'][k]['source_kind'] for k in s.actors}
 before=len(s.events)
 s.record({'action':'r214_movement_declared','by':mover,'adjacent_before':adj,'departing_edges':exits,'position_before':m.position,
  'scene_rule':'R44-CONDITIONAL-NONMETRIC','movement_published':False})
 eligible=[k for k in exits if s.actors[k].reaction==1 and s.actors[k].hp>0 and k!=mover]
 order=[];tielog=[]
 if eligible:
  order,tielog=priority(s,seed,eligible,stats)
  s.record({'action':'r214_r43_priority','order':order,'des':{k:SRC[stats[k]]['des'] for k in eligible},'tie_draws':tielog,
    'priority_rng_before_attack_intent':True,'R49_4d6':bool(tielog)})
 s.record({'action':'r214_reaction_window_open','by':mover,'potential':exits,'eligible':eligible,'order':order})
 metric=st['r214']['stats'];metric['windows']+=1
 for ix,k in enumerate(order):
  if m.hp<=0:break
  sk=stats[k];src=AOO[sk]
  intent=declare_opportunity_reaction(s,k,mover,source=src,state=aoo_context(s,(k,sk),mover),proofs=(PROOFS[sk],),
    fixture_adjacency_id='R44_SCENE_EDGES_'+case)
  ev=attack(s,seed,k,mover,'AOO-'+case+'-'+str(seq)+'-'+str(ix),intent_seq=intent['seq'])
  metric['aoo']+=1;metric['reactions']+=1;metric['hits']+=int(ev['hit']);metric['misses']+=int(not ev['hit']);metric['hp_loss']+=ev['hp_loss_actual']
  s.record({'action':'r214_aoo_consumed_result','by':k,'against':mover,'intent_seq':intent['seq'],
   'attack_seq':ev['seq'],'reaction_after':s.actors[k].reaction,'movement_published':False})
 if m.hp>0:
  srcpos=m.position;newpos='(-1.5, -1.5)' if mover=='R' else '(0.0, -1.5)'
  ev=move_via_verified_path(s,mover,source=MOVE,state=ActorActionState(mover,1,None,(MOVE.action_id,),movement_available=True,geometry_confirmed=True,environment_contract=True),
   proofs=(PROOF,),destination=newpos,path_evidence='R214-FIXTURE-OPEN-PATH-NO-WORLD-METRIC-BLOCK',travel_cost=Fraction(2),speed=Fraction(3))
  metric['moves']+=1
  outcome='MOVEMENT_COMPLETED'
  s.record({'action':'r214_move_after_aoo','mover':mover,'move_seq':ev['seq'],'prior_position':srcpos,'new_position':newpos})
 else:
  outcome='KO_MOVEMENT_COST_UNKNOWN'
  s.record({'action':'r214_move_interrupted_HP0','by':mover,'position':m.position,'move_cost':'UNKNOWN_EFFECT_HOLD',
    'non_consumed_reactions':[k for k in order if s.actors[k].reaction==1]})
 if case=='SPENT_CHAIN' and mover=='R' and seq==1:st['active']='G'
 else:st['phase']='COMPLETE';st['active']=None
 st['r214']['last_outcome']=outcome
 sync(st,s)
 return {'outcome':outcome,'native_events_added':s.events[before:],'metrics':metric,'next_active':st['active']}

def run_aoo(case,seed):
 db=ROOT/'evidence/db'/f'R214_AOO_{case}_S{seed}.sqlite'
 if db.exists():raise Gate('NO_REUSE_DB')
 init(db,seed,case)
 fixtures={
  'DOUBLE':(['F','V'],['F','V']),
  'MISS':(['A'],['A']),
  'SPENT_CHAIN':(['F'],['F']),
  'TIE':(['A','B'],['A','B']),
  'LETHAL':(['F','V'],['F','V']),
  'NO_ADJ':([],[])}
 adj,exits=fixtures[case]
 total=2 if case=='SPENT_CHAIN' else 1
 for ix in range(total):
  st,_,_=j.load(db);who=st['active']
  payload={'case':case,'mover':who,'adj':adj,'exits':exits,'phash':PH}
  preflight_window(st,who,adj,exits)
  j.event_commit(str(db),f'LAB-CMD-R214-{case}-{seed}-{ix+1}', 'R214_NATIVE_CLAIM_BEFORE_OFFENSIVE_RNG',payload,window)
 st,head,rev=j.load(db)
 return {'case':case,'seed':seed,'file':db.name,'head':head,'commits':rev,'phase':st['phase'],
  'metrics':st['r214']['stats'],'hp':{k:v['resource']['hp'] for k,v in st['actors'].items()},
  'reaction':{k:v['resource']['reaction'] for k,v in st['actors'].items()},
  'positions':{k:v['resource']['position'] for k,v in st['actors'].items()},'event_count':len(st['native_events'])}

# Bilateral physical window: two active source-specified actors, no invented metric adjacency.
def init_bilateral(db,seed):
 j.init_db(str(db),'A',seed);st=j.initial('A',seed)
 st.update({'scene':'R214-BILATERAL-'+str(seed),'seed':seed,'phase':'ACTIVE','round':1,'turn':0,'active':'V','order':['V','R'],
  'actors':{'V':source_actor('V','V',[0,0]),'R':source_actor('R','R',[0,0])},'native_events':[],
  'r214bi':{'phash':PH,'attacks':0,'hits':0,'hp_loss':0,'turns':{'V':0,'R':0},'source':'PROPOSED-NPC-ADJACENCY-DECLARED-TEST',
    'no_aoo':'NO_MOVEMENT', 'max_rounds':PRE['bilateral_round_horizon']}})
 st['actors']['R']['resource']['standard']=0
 con=j.connect(str(db));h=j.sha({'bilateral':PH,'seed':seed})
 with con:
  for k,v in [('state',j.canonical(st)),('scene',st['scene']),('genesis',h),('head',h)]:con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 con.close()

def bilateral_turn(st,p,seq):
 if p['phash']!=PH or st['phase']!='ACTIVE' or p['who']!=st['active'] or p['seed']!=st['seed']:raise Gate('BILATERAL_ORDER')
 who=p['who'];target='R' if who=='V' else 'V';s=from_state(st);att=s.actors[who];defd=s.actors[target]
 if att.standard!=1:raise Gate('NO_STANDARD')
 old=len(s.events)
 ev=attack(s,st['seed'],who,target,'BI-'+str(seq),origin='NORMAL')
 end_source_turn(s,who)
 m=st['r214bi'];m['turns'][who]+=1;m['attacks']+=1;m['hits']+=int(ev['hit']);m['hp_loss']+=ev['hp_loss_actual']
 if defd.hp<=0:
  st['phase']='KO_TEST';st['active']=None;st['finish_reason']='HP0'
 elif who=='R' and st['round']>=PRE['bilateral_round_horizon']:
  st['phase']='CENSORED_HORIZON';st['active']=None;st['finish_reason']='HORIZON_4_ROUNDS'
 else:
  new='R' if who=='V' else 'V'
  if who=='R':st['round']+=1
  st['active']=new
  begin_source_turn(s,new)
 sync(st,s)
 return {'actor':who,'target':target,'attack_seq':ev['seq'],'turn_event_trace':s.events[old:],'phase':st['phase'],
   'new_active':st['active'],'reactions':{k:c.reaction for k,c in s.actors.items()}}

def run_bilateral(seed):
 db=ROOT/'evidence/db'/f'R214_BILATERAL_S{seed}.sqlite'
 if db.exists():raise Gate('NO_REUSE_BILATERAL')
 init_bilateral(db,seed)
 for i in range(PRE['bilateral_round_horizon']*2):
  st,_,_=j.load(db)
  if st['phase']!='ACTIVE':break
  who=st['active'];p={'seed':seed,'who':who,'phash':PH}
  j.event_commit(str(db),f'LAB-CMD-R214-BILATERAL-{seed}-T{i+1}', 'R214_BILATERAL_NATIVE_TURN',p,bilateral_turn)
 st,head,rev=j.load(db)
 return {'case':'BILATERAL','seed':seed,'file':db.name,'head':head,'commits':rev,
  'phase':st['phase'],'stats':st['r214bi'],'hp':{k:v['resource']['hp'] for k,v in st['actors'].items()},
  'reactions':{k:v['resource']['reaction'] for k,v in st['actors'].items()},'event_count':len(st['native_events'])}

def main():
 results=[]
 for case,seeds in CASE_SEEDS.items():
  for seed in seeds:results.append(run_aoo(case,seed))
 for seed in PRE['bilateral_seeds']:results.append(run_bilateral(seed))
 (ROOT/'evidence/R214_NEW_RUN_RESULTS.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
 print(json.dumps({'runs':len(results),'aoo':sum(x.get('metrics',{}).get('aoo',0) for x in results),
    'bilateral':sum(x.get('case')=='BILATERAL' for x in results),'commits':sum(x['commits'] for x in results),
    'aoo_misses':sum(x.get('metrics',{}).get('misses',0) for x in results)},indent=2))
if __name__=='__main__':main()
