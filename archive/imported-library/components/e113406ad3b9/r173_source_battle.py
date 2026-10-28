"""R173 scoped *documented actor* duel on R18 WAL and preserved v0.8.1.
No original modification. Conditional INIT/adjacency, thus NOT official full source admissibility.
Source-backed attacks and Auren's Esquiva resolved by historical v0.8.1.
"""
from __future__ import annotations
import sys, pathlib, json, hashlib, copy, random, sqlite3
from dataclasses import asdict
P=pathlib.Path(__file__).resolve().parent
for d in (P/'deps/native_v081_controlled',P/'deps/r61_extracted/work/fusion_stage12',P/'deps/R171_counter_causal_guard',P/'r172_work'):
 sys.path.append(str(d))
from vlab_effects_v08 import Scene,Combatant,AbilitySource,ActorActionState,FrozenRuleEvidence,Resistances,apply_weapon_attack,react_defensively,EffectBlocked
import vlab_r18_interactive as r18
import r172_atomic_counter as r172

VERSION='R173-SOURCE-SCOPED-V081-R18-ATOMIC-LAB-v1'
COMBAT='https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0'
AUREN='https://app.notion.com/p/3ebc2b324ede814bb730d47dd7bd5f02'
BEAST='https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7'
ACTORS={
 'AUREN':{'name':'Sikong Auren','source':AUREN,'kind':'ED','rank':'Lendário3','level':23,'hp':523,'pa':719,'ca':225,'rd_physical':35,'des':164,'con':48,'armor':24,'reflex_bonus':2,'initiative_literal':'6d6+166','attack_base':193,'attack_after_two_turns':201,'attack_dice':(6,6),'damage_dice':(8,8),'damage_flat':211,'attack_name':'Alvorada Rachada (normal)','damage_type':'impacto','reaction':'ESQUIVAR','move_m':16},
 'LEVIATHAN':{'name':'Leviatã de Ferro Mnemônico','source':BEAST,'kind':'BEAST_PRECREATE','rank':'Lendário4','level':24,'hp':6060,'pa':4260,'ca':110,'rd_physical':75,'des':60,'con':150,'armor':None,'reflex_bonus':None,'initiative_literal':None,'attack_base':142,'attack_after_two_turns':142,'attack_dice':(6,6),'damage_dice':(20,10),'damage_flat':0,'attack_name':'Aríete Ferrolunar','damage_type':'impacto','reaction':None,'move_m':49},
}
# Auren source 'DANO NORMAL: Lança 8d8+211', Leviathan 'Aríete 20d10 Impacto'.
# For Auren lance, source damage physical category is not explicitly supplied in the 
# published quick sheet. This scenario uses the equipment's physical lance as source 
# of physical damage; specific subtype impact/perforation is not settled. We use 
# 'perfurante' for spear ONLY as provisional type, and gate source-admissibility accordingly.
ACTORS['AUREN']['damage_type']='perfurante'
PROOFS={
 'AUREN':'AUREN-2026-09-30-source-excerpt-6d6+193-8d8+211-CA225-RD35',
 'LEVIATHAN':'BEAST-FULLSPEC-2026-10-08-LEVIATHAN-6d6+142-20d10-impacto-RD75',
 'ESQUIVAR':'COMBAT-2026-10-07-ESQUIVAR-CA+Reflexo-before-attack',
}
SRC={}
for who in ACTORS:
 s=ACTORS[who]
 SRC[who]=AbilitySource('R173-ATTACK-'+who,'attack','STANDARD',s['source'],PROOFS[who],'RULE-DERIVED',required_pa=0,target_scope='ENEMY',effect_adapter_ready=True,effect_adapter_id='V081-WEAPON')
SRC['ESQUIVAR']=AbilitySource('R173-AUREN-ESQUIVAR','reaction','REACTION',COMBAT,PROOFS['ESQUIVAR'],'RULE-DERIVED',target_scope='SELF',reaction_trigger='BEFORE-ATTACK',effect_adapter_ready=True,effect_adapter_id='V081-DEFENSE')
SOURCE_EXCERPTS={
 'AUREN':'**Lança em duelo:** `6d6+193`\n**Mesmo adversário após 2 turnos:** `6d6+201`\n**Lança:** `8d8+211`\n**RD físico:** 35',
 'LEVIATHAN':'**Elementos:** Spectral/Planta. **Ataque físico:** `6d6+142`. **CD sobrenatural:** 97.\n<td>Aríete Ferrolunar</td>\n<td>Padrão · 0 PA</td>\n<td>20d10 Impacto</td>',
 'ESQUIVAR':'**Esquiva = CA + Reflexo**\nAntes de um ataque inimigo, o personagem pode anunciar o uso de sua Reação',
}
FP={k:FrozenRuleEvidence(src.source_page_id,src.rule_id,hashlib.sha256(SOURCE_EXCERPTS[k].encode()).hexdigest(),'2026-10-18','R173-NOTION-FETCH-LITERAL-EXCERPT-NOT-FULL-PAGE-HASH') for k,src in SRC.items()}

def genesis(seed,policy):
 st=r18.initial('A',seed)
 st['r173_version']=VERSION
 st['r173_provenance']='ACTORS_FROM_NOTION;EXOGENOUS_INITIATIVE;MELEE_AT_START_LAB_CONDITION'
 st['r173_complete_source_admissibility']=False
 st['r173_conditional_assumptions']=['INITIATIVE_ORDER_EXOGENOUS_AUREN_THEN_LEVIATHAN','START_IN_MELEE_CONTACT_NO_GEOMETRIC_PROOF','AUREN_SPEAR_PHYSICAL_SUBTYPE_PROVISIONAL_PERFURANTE','REACTION_REFRESH_NOT_APPLIED']
 st['r173_policy']=policy
 st['r173_native_events']=[];st['r173_turn_history']=[]
 st['r173_metrics']={'attacks':0,'hits':0,'raw_hit_damage':0,'post_rd':0,'hp_loss':0,'overkill':0,'reactions_spent':0,'pa_spent':0,'crit_positive':0,'crit_negative':0,'attempts_by_actor':{'AUREN':0,'LEVIATHAN':0},'hits_by_actor':{'AUREN':0,'LEVIATHAN':0}}
 st['scene']='A';st['synthetic']=True;st['source_status']='SOURCED_ACTORS_CONDITIONAL_ORDER';st['source_confidence']='PARTIAL_SOURCE_GATED_NOT_OFFICIAL'
 st['actors']={}
 for aid,f in ACTORS.items():
  resource=asdict(Combatant(aid,f['hp'],f['pa'],f['ca'],f['con'],f['armor'] or 0,0,f['reflex_bonus'] or 0,'LAB-MELEE-CONTACT',rank='Lendário',maximum_hp=f['hp'],base_speed=f['move_m']))
  st['actors'][aid]={'name':f['name'],'stats':{'source_page':f['source'],'ordinal_level':f['level'],'initiative_literal':f['initiative_literal'],'rd_physical':f['rd_physical'],'damage_type':f['damage_type'],'unknown_fields':['initiative_bonus_specific','reflex','armor'] if aid=='LEVIATHAN' else ['weapon_damage_subtype']},'resource':resource}
 return st

def init_db(db,seed,policy):
 r18.init_db(db,'A',seed)
 # Changes exclusively the virgin experimental Genesis, never any existing event or original DB.
 con=r18.connect(db)
 try:
  assert con.execute('SELECT COUNT(*) FROM events').fetchone()[0]==0
  assert con.execute('SELECT COUNT(*) FROM pending').fetchone()[0]==0
  with con:con.execute('UPDATE meta SET value=? WHERE key="state"',(r18.canonical(genesis(seed,policy)),))
 finally:con.close()

def tape(seed,index,actor):
 def draw(key,n,sides):
  entropy=hashlib.sha256(f'R173-PREREG-DEV|{seed}|{index}|{actor}|{key}|{n}d{sides}'.encode()).digest()
  rand=random.Random(int.from_bytes(entropy,'big'))
  return [rand.randint(1,sides) for _ in range(n)]
 return {'crit':draw('crit',3,6),'hit':draw('hit',6,6),'hit_weak':draw('weak_hit',6,6),
         'damage':draw('damage',ACTORS[actor]['damage_dice'][0],ACTORS[actor]['damage_dice'][1])}

def attack_transaction(st,p,seq):
 assert st['phase']=='ACTIVE' and st['active'] in ACTORS
 attacker=st['active'];defender='LEVIATHAN' if attacker=='AUREN' else 'AUREN'
 t=p['roll_tape'];idx=p['attack_index']
 if p['actor']!=attacker or p['target']!=defender or p['seed']!=st['seed'] or p['policy']!=st['r173_policy'] or p['roll_tape']!=tape(st['seed'],idx,attacker):raise EffectBlocked('UNAUTHORIZED_TAPE_OR_ACTOR')
 old=st['r173_native_events'];fighters={x:Combatant(**copy.deepcopy(o['resource'])) for x,o in st['actors'].items()}
 scene=Scene(fighters,events=copy.deepcopy(old),seed=st['seed'],provenance='R173-PRECREATE-LAB-NOT-CANON')
 a=scene.actors[attacker];d=scene.actors[defender]
 if a.hp<=0 or d.hp<=0 or a.standard!=1:raise EffectBlocked('INVALID_ALIVE_STANDARD')
 # Declare defense before applying attack, based exclusively on pre-roll source ranges and policy.
 # This test uses no inference of hit outcome in the policy (no peek at dice).
 defense=None
 if defender=='AUREN' and d.reaction==1 and st['r173_policy']=='ALWAYS_DODGE':
  re=SRC['ESQUIVAR'];rs=ActorActionState(defender,23,d.pa,(re.action_id,),reaction_trigger_observed='BEFORE-ATTACK',enemy_ids_visible=(attacker,))
  # Method needs attack score, but roll tape is already frozen in input before the atomic compute;
  # the POLICY to declare was computed from source ranges, not that score.
  hit_score=sum(t['hit'])+ACTORS[attacker]['attack_base']
  defense=react_defensively(scene,defender,kind='ESQUIVAR',attack_score=hit_score,announced_before=True,trigger_source='BEFORE-ATTACK',source=re,state=rs,proofs=(FP['ESQUIVAR'],))
 src=SRC[attacker];fs=ACTORS[attacker]
 weak=(scene.actors[attacker].hp>0 and scene.actors[attacker].hp*10<fs['hp'])
 hits=[tuple(t['hit']),tuple(t['hit_weak'])] if weak else [tuple(t['hit'])]
 penalty=-2 if weak else 0
 bonus=fs['attack_after_two_turns'] if attacker=='AUREN' and st.get('r173_auren_turns',0)>=2 else fs['attack_base']
 score=(min(map(sum,hits))+bonus-2 if weak else sum(t['hit'])+bonus)
 crit=tuple(t['crit']);critical=(crit[:2]==(6,6) and crit[2]>=5)
 if defense is not None and weak:raise EffectBlocked('DEFENSE_SCORE_VS_WEAK_ATTACK_DIFFERENT_TAPE_REJECTED')
 dmg=sum(t['damage'])+fs['damage_flat']
 proof=FP[attacker];actor_state=ActorActionState(attacker,fs['level'],a.pa,(src.action_id,),enemy_ids_visible=(defender,))
 receipt=apply_weapon_attack(scene,attacker,defender,source=src,state=actor_state,proofs=(proof,),roll_score=score,damage=dmg,damage_tag=fs['damage_type'],rd=Resistances(general=ACTORS[defender]['rd_physical'],provenance='VERIFIED_PHYSICAL_RD_SOURCE'),strict=True,
   defense_event=defense,damage_dice_groups=(fs['damage_dice'],),damage_roll_groups=(tuple(t['damage']),),damage_fixed_bonus=fs['damage_flat'],critical_sequence=crit,
   attack_roll_attempts=tuple(hits),attack_bonus=bonus,lab_negative_critical_policy=True)
 # Include within R18 atomic state / log, not a post-commit annotation.
 receipt['r173_source_rule']=src.rule_id;receipt['r173_source_page']=src.source_page_id
 receipt['r173_tx_seq']=seq;receipt['r173_defense_event_seq']=defense['seq'] if defense else None
 receipt['r173_actor_name']=fs['name'];receipt['r173_defender_name']=ACTORS[defender]['name']
 if defense:defense['r173_response_to_attack_seq']=receipt['seq']
 st['r173_native_events']=copy.deepcopy(scene.events)
 for actor,obj in scene.actors.items():st['actors'][actor]['resource']=asdict(obj)
 m=st['r173_metrics'];m['attacks']+=1;m['hits']+=int(receipt['hit']);m['raw_hit_damage']+=receipt['raw'];m['post_rd']+=receipt['net'];m['hp_loss']+=receipt['hp_loss_actual'];m['overkill']+=receipt['overkill'];m['reactions_spent']+=int(bool(defense));m['crit_positive']+=int(receipt['critical']=='POSITIVE');m['crit_negative']+=int(receipt['critical']=='NEGATIVE');m['attempts_by_actor'][attacker]+=1;m['hits_by_actor'][attacker]+=int(receipt['hit'])
 if attacker=='AUREN':st['r173_auren_turns']=st.get('r173_auren_turns',0)+1
 if scene.actors[defender].hp==0:
  st['phase']='FINISHED';st['winner']=attacker;st['finish_reason']='HP0_LAB_CONDITIONAL';st['active']=None
  scheduler={'phase':'FINISHED','winner':attacker,'reason':'HP0'}
 else:
  # Existing preserved scheduler; explicitly NO synthetic auto-refresh of reaction.
  scheduler=r18._next_turn(st)
 detail={'type':'R173_SOURCE_ATTACK','actor':attacker,'defender':defender,'policy':st['r173_policy'],
  'native_events':copy.deepcopy(scene.events[len(old):]),'attack_event_seq':receipt['seq'],
  'defense_event_seq':defense['seq'] if defense else None,'receipt':copy.deepcopy(receipt),
  'scheduler':scheduler,'source_page':src.source_page_id,'source_proof_pointer':proof.content_sha256,
  'HP_after':{aid:obj.hp for aid,obj in scene.actors.items()},'PA_after':{aid:obj.pa for aid,obj in scene.actors.items()},
  'reaction_after':{aid:obj.reaction for aid,obj in scene.actors.items()},'official_effects':0}
 st['r173_turn_history'].append({'tx_seq':seq,'actor':attacker,'target':defender,'events':[x['seq'] for x in detail['native_events']],'HP_after':detail['HP_after'],'PA_after':detail['PA_after'],'reaction_after':detail['reaction_after'],'winner':st['winner']})
 return detail

def do_start(st,p,seq):
 if st['phase']!='INIT' or p!= {'order':['AUREN','LEVIATHAN'],'authority':'EXOGENOUS_LAB_CONDITIONAL_NOT_CANON'}:raise EffectBlocked('UNSUPPORTED_INIT')
 st['phase']='ACTIVE';st['round']=1;st['turn']=0;st['order']=p['order'];st['active']='AUREN'
 return {'conditional_order':p['order'],'source_battle_admissibility':'PARTIAL_INITIATIVE_NOT_ADMITTED','attack_source_proofs':'NOTION_EXCERPTS','official_effects':0}

def fight(directory,seed,policy,max_attacks=95):
 directory=pathlib.Path(directory);directory.mkdir(parents=True,exist_ok=True)
 db=directory/f'R173_SOURCE_LEVIATHAN_{policy}_{seed}.sqlite'
 init_db(db,seed,policy)
 r18.event_commit(db,'LAB-CMD-R173-INIT-'+policy,'R173_CONDITIONAL_INIT',{'order':['AUREN','LEVIATHAN'],'authority':'EXOGENOUS_LAB_CONDITIONAL_NOT_CANON'},do_start)
 for i in range(max_attacks):
  state,_,_=r18.load(db)
  if state['phase']=='FINISHED':break
  actor=state['active'];p={'actor':actor,'target':'LEVIATHAN' if actor=='AUREN' else 'AUREN',
       'seed':seed,'policy':policy,'attack_index':i+1,'roll_tape':tape(seed,i+1,actor)}
  cmd=f'LAB-CMD-R173-{policy}-{i+1:04d}'
  r18.event_commit(db,cmd,'R173_SOURCE_ATTACK',p,attack_transaction)
 st,_,_=r18.load(db)
 r172.write_checkpoint(db)
 return db,st

if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('dir');ap.add_argument('--seed',type=int,default=1730101);ap.add_argument('--max-attacks',type=int,default=95);o=ap.parse_args()
 for policy in ['ALWAYS_DODGE','TACTICAL_SAVE']:
  db,st=fight(o.dir,o.seed,policy,o.max_attacks)
  print(json.dumps({'db':str(db),'policy':policy,'phase':st['phase'],'winner':st['winner'],'metrics':st['r173_metrics'],'actor_hp':{x:y['resource']['hp'] for x,y in st['actors'].items()},'rounds':st['round'],'turn_history_count':len(st['r173_turn_history'])},ensure_ascii=False))
