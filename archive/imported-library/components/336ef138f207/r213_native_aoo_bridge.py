"""R213 TEST conditional: historical R43/R44 fixture adjacency graph -> native v0.8.1 AOO and movement, R18 atomic journal.
CANON: no universal block width or geometry inferred; fixture adjacency validated only for documented R44 coordinates.
"""
from __future__ import annotations
import sys,os,json,copy,hashlib,random,math
from pathlib import Path
from dataclasses import asdict
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import vlab_r18_interactive as j
# Legacy R18 gateway prepends historical v09 imports; force source-gated v0.8.1 R211 copy for this incremental adapter.
sys.modules.pop("vlab_effects_v08", None)
sys.path.insert(0,str(ROOT/"runtime/native"))
from vlab_effects_v08 import (Combatant,Scene,AbilitySource,FrozenRuleEvidence,ActorActionState,
    EffectBlocked,apply_weapon_attack,move_via_verified_path,Resistances)
SRC=json.loads((ROOT/'sources/R44_R46_FROZEN_MASTER_SOURCE.json').read_text())['sources']
PRE=json.loads((ROOT/'sources/R213_PREREG.json').read_text()); PRE_SHA=hashlib.sha256((ROOT/'sources/R213_PREREG.json').read_bytes()).hexdigest()
VERSION='R213-MINIMAL-NATIVE-AOO-RESPONSE-CONTEXT-CONDITIONAL-1'
RULE='3ebc2b32-4ede-81f1-be4b-e8804ac113c0'
PROOF=FrozenRuleEvidence(RULE,'R213-R43-R44-HISTORIC-FIXTURE',hashlib.sha256((ROOT/'sources/R44_R46_FROZEN_MASTER_SOURCE.json').read_bytes()).hexdigest(),'2026-10-20','NOTION-R44-READBACK-R213')
PROOFS={k:FrozenRuleEvidence(SRC[k]['page'],PROOF.rule_id,PROOF.content_sha256,'2026-10-20','NOTION-R44-READBACK-R213') for k in ['F','V']}
MOVE=AbilitySource('R213-MOVE','move','MOVEMENT',RULE,PROOF.rule_id,'RULE-DERIVED',target_scope='POSITION',effect_adapter_ready=True,effect_adapter_id='NATIVE-V081-VERIFIED-PATH')
AOO={k:AbilitySource('R213-AOO-'+k,'attack','REACTION',SRC[k]['page'],PROOF.rule_id,'RULE-DERIVED',target_scope='ENEMY',reaction_trigger='EXIT_ADJACENT',effect_adapter_ready=True,effect_adapter_id='NATIVE-V081-WEAPON') for k in ['F','V']}
NORMAL=AbilitySource('R213-F-NORMAL','attack','STANDARD',SRC['F']['page'],PROOF.rule_id,'RULE-DERIVED',target_scope='ENEMY',requires_range_check=True,effect_adapter_ready=True,effect_adapter_id='NATIVE-V081-WEAPON')
ACTOR_POS={'R':[0.,0.],'G':[0.,0.],'F':[1.5,0.],'V':[0.,1.5]}
DEST=[-1.5,-1.5]
class R213Hold(Exception):pass

def prng(seed,label,count,faces):
 h=hashlib.sha256(f'R213|{seed}|{label}|{count}d{faces}'.encode()).digest()
 rng=random.Random(int.from_bytes(h,'big'));return tuple(rng.randint(1,faces) for _ in range(count))

def tape(seed,who,step):
 a=SRC[who];tag=f'{who}-{step}'
 return {'crit':prng(seed,'CRIT-'+tag,3,6),'attempts':(prng(seed,'HIT0-'+tag,a['rank_dice'][0],6),prng(seed,'HIT1-'+tag,a['rank_dice'][0],6)),
  'damage':(prng(seed,'DMG-'+tag,*a['damage_dice']),)}

def no_neg(seed,case):
 for w in (['F','V'] if case=='DOUBLE' else ['F'] if case=='LETHAL' else ['V'] if case=='REACTION_SPENT' else []):
  c=tape(seed,w,'AOO')['crit']
  if c[:2]==(1,1) and c[2]<=2:return False
 return True

def scene_from(st):
 return Scene({k:Combatant(**copy.deepcopy(v['resource'])) for k,v in st['actors'].items()},events=copy.deepcopy(st['native_events']),seed=st['seed'],provenance=VERSION+'-TEST-CONDITIONAL')

def sync(st,s):
 st['native_events']=copy.deepcopy(s.events)
 for k,c in s.actors.items():st['actors'][k]['resource']=asdict(c)

def genesis(db,seed,case):
 j.init_db(str(db),'A',seed)
 actors=['R','F','V'] if case!='LETHAL' else ['G','F','V'];mover='G' if case=='LETHAL' else 'R'
 st=j.initial('A',seed)
 st.update({'scene':'R213-'+case+'-'+str(seed),'seed':seed,'phase':'TURN','round':1,'turn':0,'active':mover,'order':[mover,'F','V'],
  'actors':{},'native_events':[],'r213':{'version':VERSION,'prereg_sha':PRE_SHA,'case':case,'source_status':'TEST_CONDITIONAL',
  'metrics':{'movement':0,'aoo':0,'hits':0,'reaction_spent':0,'hp_loss':0,'standard_normal':0},'path_events':[],
  'adjacency_contract':'R44_SCENE_DECLARED_EDGES_NOT_METRIC_CANON','general_block_width':'UNKNOWN'},
  'synthetic':True})
 for who in actors:
  a=SRC[who]; pos=ACTOR_POS[who][:]
  if case=='NONADJACENT' and who in ('F','V'):pos=([10.,0.] if who=='F' else [0.,10.])
  # No canonical Arveth/Cabra speed derived; 3m is explicit fixture-only admissibility assumption; do not promote.
  c=Combatant(who,a['hp'],None,a['ca'],0,0,0,0,str(tuple(pos)),rank='Ouro Negro' if who!='G' else 'Bronze',
      maximum_hp=a['hp'],standard=1 if who==mover else 0,movement=1,reaction=1,base_speed="3")
  st['actors'][who]={'resource':asdict(c),'source':a['page'],'stats':a}
 if case=='REACTION_SPENT':
  # Snapshot explicitly declared test-only, never claimed to originate from historical on-turn action.
  st['actors']['F']['resource']['reaction']=0
  st['r213']['spent_snapshot']='PREREG_TEST_ALREADY_SPENT; no transaction history claimed'
 conn=j.connect(str(db))
 with conn:
  conn.execute('UPDATE meta SET value=? WHERE key="state"',(j.canonical(st),))
  conn.execute('UPDATE meta SET value=? WHERE key="scene"',(st["scene"],))
  h=j.sha({"seed":seed,"scene":st["scene"],"prereg":PRE_SHA,"sources":PROOF.content_sha256})
  conn.execute('UPDATE meta SET value=? WHERE key="genesis"',(h,))
  conn.execute('UPDATE meta SET value=? WHERE key="head"',(h,))
 conn.close()
 return st

def execute_attack(s,who,mover,seed,step='AOO'):
 a=SRC[who];tr=tape(seed,who,step)
 if tr['crit'][:2]==(1,1) and tr['crit'][2]<=2:raise R213Hold('NEGATIVE_CRIT_POLICY_UNRESOLVED')
 score=max(sum(z) for z in tr['attempts'])+a['attack_bonus']+2
 dmg=sum(tr['damage'][0])+a['damage_bonus']; target=SRC[mover]
 return apply_weapon_attack(s,who,mover,source=AOO[who],state=ActorActionState(who,20,None,(AOO[who].action_id,),
  reaction_available=True,reaction_trigger_observed='EXIT_ADJACENT',range_confirmed=True,enemy_ids_visible=(mover,)),proofs=(PROOFS[who],),
  roll_score=score,damage=dmg,damage_tag=a['damage_kind'].split('/')[0],rd=Resistances(general=target['rd'],provenance='R44-FROZEN-NPC-SOURCE-TEST'),
  damage_dice_groups=(tuple(a['damage_dice']),),damage_roll_groups=tr['damage'],damage_fixed_bonus=a['damage_bonus'],
  critical_sequence=tr['crit'],attack_roll_attempts=tr['attempts'],attack_bonus=a['attack_bonus'],
  advantage_levels=1,attack_origin='OPPORTUNITY')

def action(st,p,seq):
 case=st['r213']['case']; seed=st['seed'];mover=st['active'];r=st['r213']
 if p!={'case':case,'seed':seed,'prereg_sha':PRE_SHA} or seq!=1:raise R213Hold('PRECOMMIT_SOURCE_DRIFT')
 s=scene_from(st);before=len(s.events);m=s.actors[mover]
 if m.movement!=1 or m.hp<=0:raise R213Hold('MOVEMENT_NOT_AVAILABLE')
 adjacency=PRE['fixtures'][case]['adjacent_at_departure']
 exits=PRE['fixtures'][case]['exits_adjacency']
 if case!='NONADJACENT' and adjacency!=['F','V']:raise R213Hold('INVALID_FIXTURE_EDGES')
 if case=='NONADJACENT' and adjacency:raise R213Hold('CONTROL_ADJACENCY_LEAK')
 start=[0.,0.]; dest=PRE['fixtures'][case]['destination_m'];speed=Fraction(3)
 if math.dist(start,dest)>float(speed):raise R213Hold('SPEED_BUDGET')
 if m.position!=str(tuple(start)):raise R213Hold('PRE_MOVE_POSITION')
 # Source- and scene-limited adjacency DECLARATION. Metric distances are logged, never treated as universal adjacency definition.
 eligible=[w for w in exits if w in s.actors and s.actors[w].hp>0 and s.actors[w].reaction==1]
 queue=sorted(eligible,key=lambda w:SRC[w]['des'],reverse=True)
 if len(queue)>=2 and SRC[queue[0]]['des']==SRC[queue[1]]['des']:raise R213Hold('R43_TIE_USE_HISTORIC_R49_GATE')
 gate=s.record({'action':'r213_departure_preflight','mover':mover,'from_m':start,'to_m':dest,
    'fixture_adjacent_before':adjacency,'fixture_exits':exits,'potential_attackers':exits,
    'eligible_reactions':eligible,'priority':queue,'priority_rule':'R43_DESC_DES_R49_RANK_DICE_IF_TIE',
    'metric_conversion':'UNDEFINED_WORLD_RULE','movement_published':False})
 for who in queue:
  if m.hp<=0:break
  # Movement remains uncommitted in scene; attack resolves at departure point.
  ev=execute_attack(s,who,mover,seed)
  r['metrics']['aoo']+=1;r['metrics']['hits']+=int(ev['hit']);r['metrics']['hp_loss']+=ev['hp_loss_actual'];r['metrics']['reaction_spent']+=1
  s.record({'action':'r213_aoo_result','by':who,'against':mover,'native_attack_seq':ev['seq'],'remaining_reaction':s.actors[who].reaction,
      'mover_hp_after':m.hp,'movement_published':False})
 if m.hp<=0:
  r['movement_outcome']='KO_INTERRUPTED_COST_UNRESOLVED'
  s.record({'action':'r213_ko_before_move','by':mover,'position':m.position,'movement_cost':'UNKNOWN_EFFECT_HOLD',
     'not_executed':[w for w in queue if s.actors[w].reaction==1]})
 else:
  ev=move_via_verified_path(s,mover,source=MOVE,state=ActorActionState(mover,1 if mover=='G' else 20,None,(MOVE.action_id,),
      movement_available=True,geometry_confirmed=True,environment_contract=True),proofs=(PROOF,),
      destination=str(tuple(dest)),path_evidence='R213-R44-DECLARED-FIXTURE-NO-GENERAL-BLOCK-WIDTH',
      travel_cost=Fraction(str(math.dist(start,dest))),speed=speed)
  r['metrics']['movement']+=1
  r['movement_outcome']='COMPLETE_TEST_CONDITIONAL'
  s.record({'action':'r213_movement_after_reaction','mover':mover,'native_move_seq':ev['seq'],'new_position':m.position})
 r['path_events']=copy.deepcopy(s.events[before:]);sync(st,s);st['phase']='R213_WINDOW_CLOSED'
 return {'outcome':r['movement_outcome'],'native_events_added':r['path_events'],'metrics':r['metrics'],'final_reactions':{a:s.actors[a].reaction for a in s.actors},'final_hp':{a:s.actors[a].hp for a in s.actors}}

def run_case(case,seed):
 db=ROOT/'evidence/db'/f'R213_AOO_{case}_S{seed}.sqlite'
 if db.exists():return {'case':case,'seed':seed,'status':'QUARANTINED_PERSISTENT_PENDING_PRECOMMIT','db':db.name,'admissible':False}
 if not no_neg(seed,case):return {'case':case,'seed':seed,'status':'PRECOMMIT_NEGATIVE_CRIT_HOLD'}
 genesis(db,seed,case)
 cmd=f'LAB-CMD-R213-{case}-S{seed}'
 j.event_commit(str(db),cmd,'R213_NATIVE_AOO_MOVE_ATOMIC',{'case':case,'seed':seed,'prereg_sha':PRE_SHA},action)
 st,head,rev=j.load(str(db));res=st['r213']['metrics']
 # Historical R18 duplicate committed cmd must fail without changing any state.
 try:j.event_commit(str(db),cmd,'R213_NATIVE_AOO_MOVE_ATOMIC',{'case':case,'seed':seed,'prereg_sha':PRE_SHA},action)
 except Exception as e:duplicate_block=str(e)
 else:raise AssertionError('DUPLICATE_NOT_REJECTED')
 st2,h2,rev2=j.load(str(db));assert (h2,rev2)==(head,rev)
 return {'case':case,'seed':seed,'status':st['r213']['movement_outcome'],'db':db.name,'head':head,'commits':rev,
  'native_events':len(st['native_events']),'metrics':res,'final_hp':{k:v['resource']['hp'] for k,v in st['actors'].items()},
  'final_reactions':{k:v['resource']['reaction'] for k,v in st['actors'].items()},
  'final_position':st['actors'][st['active']]['resource']['position'],'duplicate_rejected':duplicate_block}

def main():
 out=[]
 for case in PRE['cases']:
  for seed in PRE['cases'][case]['seeds']:
   out.append(run_case(case,seed))
 (ROOT/'evidence/R213_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
 print(json.dumps({'rows':len(out),'committed':sum('db' in x for x in out),'aoo':sum(x.get('metrics',{}).get('aoo',0) for x in out),
  'moves':sum(x.get('metrics',{}).get('movement',0)for x in out),'hp_loss':sum(x.get('metrics',{}).get('hp_loss',0) for x in out)},indent=2))
if __name__=='__main__':main()
