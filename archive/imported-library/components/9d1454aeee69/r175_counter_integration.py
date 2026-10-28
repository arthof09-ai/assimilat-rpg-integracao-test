"""R175 additive policy COUNTER_AUREN using preserved R50/R51 + R171 causality + R18 SQLite.
Does not modify any R174/R173 history, and does not create a parallel counter resolver.
"""
import sys,pathlib,copy,json,hashlib
from dataclasses import asdict
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import r175_ed_be_duel as b
from vlab_effects_v08 import (AbilitySource,FrozenRuleEvidence,ActorActionState,Resistances,EffectBlocked,
 apply_weapon_attack,end_source_turn,declare_counterattack)
from r171_counter_causal import execute_causally_linked_counter,independent_validate_chain
COUNTER_PROOF=FrozenRuleEvidence('https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0',
 'MESTRE_R50_R51_COUNTER_R175',hashlib.sha256(b'Sistema de Combate R50 R51 declared-before miss-only no nested').hexdigest(),
 '2026-10-16T10:45:29.421Z','POINTER_R50_R51_OPERATION_NOT_NOTION_BINARY')
COUNTER_SOURCE=AbilitySource('R175-AUREN-COUNTER','reaction','REACTION',COUNTER_PROOF.source_page_id,
 COUNTER_PROOF.rule_id,'RULE-DERIVED',target_scope='SELF',reaction_trigger='ATTACK_DECLARED',effect_adapter_ready=True,
 effect_adapter_id='V081_R50_R51_COUNTER')

def counter_tape(seed,n):
 return {'rolls':[b.dice(seed,f'AUREN-COUNTER-ROC-TURN{n}-TRY{z}',6,6) for z in (1,2)],
 'critical':b.dice(seed,f'AUREN-COUNTER-ROC-TURN{n}-CRIT',3,6),
 'damage':b.dice(seed,f'AUREN-COUNTER-ROC-TURN{n}-DAMAGE',8,8)}

def roc_attack_with_counter(st,p,seq):
 a='ROC';d='AUREN'
 if st['phase']!='ACTIVE' or st['active']!='ROC' or p['actor']!=a or p['target']!=d or p['seed']!=st['seed']:raise EffectBlocked('actor/phase')
 n=sum(1 for h in st['r175_history'] if h['actor']=='ROC')+1
 if p['actor_turn']!=n or p['tape']!=b.tape(st['seed'],a,n) or p['counter_tape']!=counter_tape(st['seed'],n):raise EffectBlocked('tape')
 f=b.ACTORS[a];fd=b.ACTORS[d];t=p['tape'];ct=p['counter_tape'];scene=b.scene_of(st)
 src=b.SRC[a];att=scene.actors[a];defender=scene.actors[d]
 if att.standard!=1 or att.hp<=0 or defender.hp<=0:raise EffectBlocked('turn')
 before_idx=len(scene.events)
 declaration=None;counter=None
 if defender.reaction==1:
  action=ActorActionState(d,23,defender.pa,(COUNTER_SOURCE.action_id,),reaction_trigger_observed='ATTACK_DECLARED',enemy_ids_visible=(a,))
  declaration=declare_counterattack(scene,d,a,source=COUNTER_SOURCE,state=action,proofs=(COUNTER_PROOF,),declared_before=True,attack_origin='NORMAL')
 weak=10*att.hp<f['hp'];attempts=(tuple(t['hit']),tuple(t['hit_weak'])) if weak else (tuple(t['hit']),)
 score=min(map(sum,attempts))+f['attack_bonus']-2 if weak else sum(t['hit'])+f['attack_bonus']
 original=apply_weapon_attack(scene,a,d,source=src,state=ActorActionState(a,23,att.pa,(src.action_id,),enemy_ids_visible=(d,)),proofs=(b.PROOFS[a],),roll_score=score,damage=sum(t['damage'])+f['flat'],damage_tag=f['damage_tag'],rd=Resistances(general=fd['rd'],provenance='AUREN_PHYSICAL_RD35'),damage_dice_groups=((20,10),),damage_roll_groups=(tuple(t['damage']),),damage_fixed_bonus=0,critical_sequence=tuple(t['critical']),attack_roll_attempts=attempts,attack_bonus=150,lab_negative_critical_policy=True)
 if declaration:
  counter=execute_causally_linked_counter(scene,d,a,declaration=declaration,incoming=original,
    attack_attempts=tuple(tuple(x) for x in ct['rolls']),attack_bonus=193,critical_sequence=tuple(ct['critical']),
    damage_groups=((8,8),),damage_roll_groups=(tuple(ct['damage']),),flat=211,damage_tag='perfurante',
    rd=Resistances(general=75,provenance='ROC_PHYSICAL_RD75'))
  independent_validate_chain(scene.events)
 end_source_turn(scene,a)
 m=st['r175_counts'];m['attempts']+=1;m['hits']+=int(original['hit']);m['post_rd']+=original['net'];m['hp_loss']+=original['hp_loss_actual'];m['overkill']+=original['overkill'];m['crit_positive']+=int(original['critical']=='POSITIVE');m['crit_negative']+=int(original['critical']=='NEGATIVE')
 if declaration:m['reactions_spent']+=1
 if counter and counter['action']=='COUNTER_RESPONSE':
  m['attempts']+=1;m['hits']+=int(counter['hit']);m['post_rd']+=counter['net'];m['hp_loss']+=counter['before_hp']-counter['after_hp'];m['overkill']+=counter['overkill'];m['crit_positive']+=int(counter['critical']=='POSITIVE')
 if scene.actors['ROC'].hp==0:
  st['phase']='FINISHED';st['winner']='AUREN';st['finish_reason']='COUNTER_HP_ZERO_TEST_ONLY';st['active']=None;sched={'ko':'ROC','next':None}
 elif scene.actors['AUREN'].hp==0:
  st['phase']='FINISHED';st['winner']='ROC';st['finish_reason']='NORMAL_HP_ZERO_TEST_ONLY';st['active']=None;sched={'ko':'AUREN','next':None}
 else:
  sched=b.r18._next_turn(st);new=st['active'];scene.actors[new].standard=0
  sched['native_turn_start_seq']=b.begin_source_turn(scene,new)['seq']
 b.sync(st,scene)
 detail={'actor':a,'target':d,'source_page':f['page'],'target_page':fd['page'],'actor_turn':n,'tape':t,
 'counter_tape':ct,'attack':copy.deepcopy(original),'declaration':copy.deepcopy(declaration),'counter':copy.deepcopy(counter),
 'new_native_events':copy.deepcopy(scene.events[before_idx:]),'HP_after':{k:v.hp for k,v in scene.actors.items()},
 'PA_after':{k:v.pa for k,v in scene.actors.items()},'reactions_after':{k:v.reaction for k,v in scene.actors.items()},
 'scheduler':sched,'source_status':st['source_status'],'policy':'AUREN_COUNTER_R50_R51'}
 st['r175_history'].append({'seq':seq,'actor':a,'hit':original['hit'],'crit':original['critical'],
 'net':original['net'],'hp_loss':original['hp_loss_actual'],'overkill':original['overkill'],
 'counter_response':counter['action'] if counter else None,'HP_after':detail['HP_after']})
 return detail

def run(path,seed=b.SEED,max_turns=120):
 path=pathlib.Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 b.init_db(path,seed,'AUREN_FIRST')
 c=b.r18.connect(path)
 try:
  st,_,_=b.r18._read(c)
  st['r175_counter_policy']='AUREN_R50_R51_DECLARED_BEFORE_EACH_ROC_NORMAL_ATTACK_WHEN_AVAILABLE'
  with c:c.execute('UPDATE meta SET value=? WHERE key="state"',(b.r18.canonical(st),))
 finally:c.close()
 b.r18.event_commit(path,'LAB-CMD-R175-COUNTER-INIT','R175_SOURCE_START',{'order':'AUREN_FIRST'},b.start)
 for i in range(max_turns):
  st,_,_=b.r18.load(path)
  if st['phase']=='FINISHED':break
  who=st['active'];n=sum(1 for h in st['r175_history'] if h['actor']==who)+1
  p={'actor':who,'target':'AUREN' if who=='ROC' else 'ROC','seed':seed,'actor_turn':n,'tape':b.tape(seed,who,n)}
  if who=='ROC':
   p['counter_tape']=counter_tape(seed,n)
   b.r18.event_commit(path,f'LAB-CMD-R175-COUNTER-{i+1:04d}','R175_SOURCE_PHYSICAL_COUNTER',p,roc_attack_with_counter)
  else:b.r18.event_commit(path,f'LAB-CMD-R175-COUNTER-{i+1:04d}','R175_SOURCE_PHYSICAL_ATTACK',p,b.attack)
 st,head,rev=b.r18.load(path);b.r172.write_checkpoint(path)
 return {'db':path.name,'phase':st['phase'],'winner':st['winner'],'round':st['round'],'metrics':st['r175_counts'],
 'hp':{k:v['resource']['hp'] for k,v in st['actors'].items()},'pa':{k:v['resource']['pa'] for k,v in st['actors'].items()},
 'reactions':sum(1 for x in st['r175_native_events'] if x['action']=='COUNTER_DECLARE'),
 'counter_responses':sum(1 for x in st['r175_native_events'] if x['action']=='COUNTER_RESPONSE'),
 'native_events':len(st['r175_native_events']),'revision':rev,'head':head}

if __name__=='__main__':print(json.dumps(run(sys.argv[1]),ensure_ascii=False,indent=2))
