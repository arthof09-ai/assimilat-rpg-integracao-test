"""R177–R186 incremental SOURCE-SCOPED battle, not a new combat engine.
Existing R18 event_commit + v0.8.1 attack/RD/turn resolver are the only core.
One documented item reaction is a correlated pure-memory post-RD adjustment
published in the SAME SQLite transaction, never an external healing action.
Beast initiative bonus remains unknown; order is provable independently of its
non-negative ordinary skill contribution, but source certification remains HOLD.
"""
from __future__ import annotations
import sys,json,hashlib,random,pathlib,copy
from dataclasses import asdict
ROOT=pathlib.Path(__file__).resolve().parents[1]
for p in (ROOT/'runtime/native',ROOT/'runtime/work/fusion_stage12',ROOT/'runtime/r172'):
 sys.path.insert(0,str(p))
from vlab_effects_v08 import Combatant,Scene,AbilitySource,ActorActionState,FrozenRuleEvidence,EffectBlocked,Resistances,apply_weapon_attack,begin_source_turn,end_source_turn
from vlab_action_catalog_v01 import action_menu
import vlab_r18_interactive as r18
from r172_atomic_counter import write_checkpoint
VERSION='R177-R186-NATIVE-R18-V081-VAROK-LEVIATHAN-1'
PRE_SHA='c6d979740af07874201ee12463eed97b5a778c06a6e4eed624780f8a21b49651'
ACTORS={
 'VAROK':dict(name='Sikong Varok',role='NPC_ENCOUNTER_PROPOSAL_NOT_ED',rank='Ouro Negro 5',rank_level=20,page='https://app.notion.com/p/3f6c2b324ede81f49ea9efbe1a811091',edited='2026-10-16T10:33:26.087Z',hp=734,pa=324,ca=83,rd=35,con=57,armor=34,fort=2,reflex=0,des=27,initiative='4d6+29',init_dice=4,init_fixed=29,atk_dice=4,atk_fixed=100,dmg_dice=10,dmg_faces=10,dmg_fixed=48,tag='impacto',weapon='Machado Raiz-Ferro',speed=None),
 'LEVIATHAN':dict(name='Leviata de Ferro Mnemonico',role='BEAST_PRECREATE_NOT_PHYSICALLY_PROMOTED',rank='Lendario 4',rank_level=24,page='https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7',edited='2026-10-08T02:25:14.539Z',hp=6060,pa=4260,ca=110,rd=75,con=150,armor=0,fort=0,reflex=0,des=60,initiative=None,init_dice=6,init_fixed=60,atk_dice=6,atk_fixed=142,dmg_dice=20,dmg_faces=10,dmg_fixed=0,tag='impacto',weapon='Ariete Ferrolunar',speed=49)}
SNIPPETS={'VAROK':'ON5 HP734 PA livre324 CA83 RD35 Iniciativa4d6+29 Machado4d6+100 Dano10d10+48 impacto/corte; Armadura do Carrasco de Ferro Reacao50PA reduz 70 apos RD 1/cena', 'LEVIATHAN':'L4 Titã hp6060 Alma4260 CA110 RD75 DES60 prof geral+22 iniciativa especifica UNKNOWN; Ariete Ferrolunar padrao0PA dano20d10 Impacto; ataque fisico6d6+142; Vel49'}
PROOFS={k:FrozenRuleEvidence(f['page'],VERSION+'-SNAP-'+k,hashlib.sha256(SNIPPETS[k].encode()).hexdigest(),f['edited'],'CURATED_EXCERPT_POINTER_NOT_BINARY_NOTION_SIGNATURE') for k,f in ACTORS.items()}
ATT_SOURCES={k:AbilitySource(VERSION+'-ATT-'+k,'attack','STANDARD',v['page'],PROOFS[k].rule_id,'RULE-DERIVED',required_pa=0,target_scope='ENEMY',effect_adapter_ready=True,effect_adapter_id='V081-PHYSICAL') for k,v in ACTORS.items()}
ARMOR_SOURCE=AbilitySource(VERSION+'-ARMOR-REACTION','reaction','REACTION',ACTORS['VAROK']['page'],PROOFS['VAROK'].rule_id,'RULE-DERIVED',required_pa=50,target_scope='SELF',reaction_trigger='ATTACK_ANNOUNCED',effect_adapter_ready=True,effect_adapter_id='R180-SOURCE-ARMOR-70-50')

def dice(seed,who,turn,label,n,faces):
  entropy=hashlib.sha256(f'{VERSION}|{seed}|{who}|{turn}|{label}|{n}d{faces}'.encode()).digest()
  rr=random.Random(int.from_bytes(entropy,'big'))
  return [rr.randint(1,faces) for _ in range(n)]

def initiative(seed):
  v=dice(seed,'VAROK',0,'INIT',4,6);b=dice(seed,'LEVIATHAN',0,'INIT',6,6)
  vs=sum(v)+29;bs=sum(b)+60
  # The beast specific skill is NOT published. This proof needs NO guessed +22.
  # For any non-negative applicable ordinary proficiency and no external penalties,
  # Leviathan minimum 6+60=66 > Varok maximum 24+29=53.
  return {'VAROK':{'dice':v,'exact':vs,'named_prof_from_sheet':True},'LEVIATHAN':{'dice':b,'floor_without_skill':bs,'named_prof':None},'order':['LEVIATHAN','VAROK'],'proof':'66 > 53 FOR ALL ORDINARY DICE AND ANY NONNEGATIVE BEAST SKILL BONUS','not':'CERTIFIED_BEAST_INITIATIVE_VALUE','external_modifiers':'NONE_SCENARIO_SCOPE'}

def tape(seed,who,turn,weak):
 f=ACTORS[who]
 return {'crit':dice(seed,who,turn,'CRIT',3,6),
   'hit':dice(seed,who,turn,'HIT',f['atk_dice'],6),
   'hit_weak':dice(seed,who,turn,'WEAK',f['atk_dice'],6),
   'damage':dice(seed,who,turn,'DAMAGE',f['dmg_dice'],f['dmg_faces'])}

def numeric_range_gate(*,range_m,dist_m,los,required_ammo=False,ammo_available=None):
 """Source-exact declared numeric ranges only, no invented block-meter converter."""
 if isinstance(dist_m,bool) or type(dist_m) not in (int,float) or dist_m<0:raise EffectBlocked('DISTANCE_UNKNOWN')
 if type(range_m) not in (int,float) or range_m<=0:raise EffectBlocked('NUMERIC_RANGE_NOT_SOURCE_DOCUMENTED')
 if los is not True:raise EffectBlocked('LOS_UNCONFIRMED')
 if required_ammo and ammo_available is not True:raise EffectBlocked('AMMUNITION_NOT_VERIFIED')
 if dist_m>range_m:raise EffectBlocked('SOURCE_RANGE_EXCEEDED')
 return {'distance_m':dist_m,'source_range_m':range_m,'line_of_sight':True,'admitted':True}

def geometry_contact(st):
 g=st['geometry'];return (g.get('frozen')==True and g.get('surface_contact')==True and g.get('same_layer')==True and g.get('motion')==False and g.get('reach_m') is None and g.get('policy')=='PHYSICAL_CONTACT_WITHOUT_METRIC_REACH')

def initial(seed,policy):
 st=r18.initial('A',seed)
 st.update({'experiment_version':VERSION,'pre_registration_sha':PRE_SHA,'seed':seed,'policy':policy,'phase':'INIT','round':0,'turn':0,'active':None,'order':[],'winner':None,'finish_reason':None,'actors':{},'native_events':[],'history':[],
  'scene_category':'MESTRE_SIDE_TEST_SOURCE_SCOPED_NPC_VS_PRECREATE_BEAST_NOT_ED_VS_BE',
  'geometry':{'frozen':True,'surface_contact':True,'same_layer':True,'motion':False,'reach_m':None,'policy':'PHYSICAL_CONTACT_WITHOUT_METRIC_REACH','vertical':'CONTACT_TEST_ONLY','natural_encounter':False},
  'unknowns':['LEVIATHAN_NAMED_INITIATIVE_SKILL','LEVIATHAN_PHYSICAL_PAGE_PROMOTION','BEAST_NATURAL_ENGAGEMENT_GEOMETRY','NPC_PROPOSAL_NOT_OFFICIAL_CAMPAIGN','OTHER_BEAST_ABILITIES_NOT_EXERCISED'],
  'init_record':None,'armor_used':False,
  'metrics':{'attack_attempts':0,'hits':0,'gross_hit':0,'post_rd_before_item':0,'item_prevention':0,'hp_lost':0,'overkill':0,'pa_activation':0,'reactions':0,'crit_positive':0,'crit_negative':0}})
 for key,f in ACTORS.items():
  a=Combatant(key,f['hp'],f['pa'],f['ca'],f['con'],f['armor'],f['fort'],f['reflex'],'LAB-CONTACT-SURFACES',rank='Lendario' if key=='LEVIATHAN' else 'Ouro Negro',maximum_hp=f['hp'],base_speed=f['speed'],standard=0,movement=0,reaction=1)
  st['actors'][key]={'stats':{'name':f['name'],'role':f['role'],'rank':f['rank'],'source_url':f['page'],'source_last_edited_at':f['edited'],'initiative_literal':f['initiative'],'attack_fixed':f['atk_fixed'],'rd':f['rd'],'weapon':f['weapon']},'resource':asdict(a)}
 return st

def scene(st):return Scene({k:Combatant(**copy.deepcopy(v['resource'])) for k,v in st['actors'].items()},events=copy.deepcopy(st['native_events']),seed=st['seed'],provenance='R177-R186-SOURCE-SCOPED-PURE-MEMORY-R18')
def sync(st,s):
 st['native_events']=copy.deepcopy(s.events)
 for k,a in s.actors.items():st['actors'][k]['resource']=asdict(a)

def setup(db,seed,policy):
 r18.init_db(db,'A',seed)
 c=r18.connect(db)
 try:
  with c:c.execute('UPDATE meta SET value=? WHERE key="state"',(r18.canonical(initial(seed,policy)),))
 finally:c.close()

def start(st,p,seq):
 if st['phase']!='INIT' or not geometry_contact(st):raise EffectBlocked('SOURCE_GEOMETRY_HOLD')
 proof=initiative(st['seed'])
 if p!={'seed':st['seed'],'initiative':proof,'geometry':st['geometry']}:raise EffectBlocked('INIT_OR_GEOMETRY_PAYLOAD_DRIFT')
 if proof['VAROK']['exact']>=proof['LEVIATHAN']['floor_without_skill']:raise EffectBlocked('INIT_ORDER_NOT_PROVED')
 st['init_record']=proof;st['order']=list(proof['order']);st['phase']='ACTIVE';st['round']=1;st['turn']=0;st['active']='LEVIATHAN'
 ss=scene(st);ev=begin_source_turn(ss,st['active']);sync(st,ss)
 return {'kind':'PROVEN_FIRST_ORDER_WITHOUT_ASSIGNING_BEAST_INITIATIVE','proof':proof,'geometry':copy.deepcopy(st['geometry']),'native_events':[ev]}

def attack(st,p,seq):
 if st['phase']!='ACTIVE' or not geometry_contact(st):raise EffectBlocked('ACTOR_OR_GEOMETRY_HOLD')
 who=st['active'];other='VAROK' if who=='LEVIATHAN' else 'LEVIATHAN'
 turn=1+sum(h['actor']==who for h in st['history'])
 if p.get('actor')!=who or p.get('target')!=other or p.get('seed')!=st['seed'] or p.get('turn_number')!=turn or p.get('policy')!=st['policy']:raise EffectBlocked('PAYLOAD_IDENTITY_OR_TURN')
 t=tape(st['seed'],who,turn,False)
 if p.get('tape')!=t:raise EffectBlocked('ROLL_TAPE_DRIFT')
 ss=scene(st);actor=ss.actors[who];defender=ss.actors[other];f=ACTORS[who];fd=ACTORS[other]
 if actor.standard!=1 or actor.hp<=0 or defender.hp<=0:raise EffectBlocked('ACTOR_ACTION_SLOT_KO')
 weak=actor.hp*10<f['hp'];attempts=[tuple(t['hit']),tuple(t['hit_weak'])] if weak else [tuple(t['hit'])]
 score=(min(map(sum,attempts))+f['atk_fixed']-2) if weak else (sum(t['hit'])+f['atk_fixed'])
 start_native=len(ss.events);armored=False;decl=None
 if who=='LEVIATHAN' and st['policy']=='ARMOR_ON_FIRST_SOURCE_ATTACK' and not st['armor_used']:
  if defender.reaction!=1 or defender.pa is None or defender.pa<50:raise EffectBlocked('ARMOR_REACTION_UNAVAILABLE')
  state=ActorActionState(other,20,defender.pa,(ARMOR_SOURCE.action_id,),reaction_available=bool(defender.reaction),reaction_trigger_observed='ATTACK_ANNOUNCED')
  comp=action_menu(state,(ARMOR_SOURCE,),phase='REACTION',strict=True,source_evidence=(PROOFS['VAROK'],))
  if len(comp.legal_options)!=1:raise EffectBlocked('ARMOR_SOURCE_OPTION_FAIL')
  defender.reaction=0;defender.pa-=50;st['armor_used']=True;armored=True
  decl=ss.record({'action':'SOURCE_ARMOR_DECLARE','by':'VAROK','incoming_from':'LEVIATHAN','before_attack_roll':True,'source_page':ACTORS['VAROK']['page'],'source':'Armadura do Carrasco de Ferro','reaction_spent':1,'pa_debit':50,'once_per_scene':True})
 raw=sum(t['damage'])+f['dmg_fixed']
 ev=apply_weapon_attack(ss,who,other,source=ATT_SOURCES[who],state=ActorActionState(who,f['rank_level'],actor.pa,(ATT_SOURCES[who].action_id,),enemy_ids_visible=(other,)),proofs=(PROOFS[who],),roll_score=score,damage=raw,damage_tag=f['tag'],rd=Resistances(general=fd['rd'],provenance='SOURCE_PHYSICAL_RD'),damage_dice_groups=((f['dmg_dice'],f['dmg_faces']),),damage_roll_groups=(tuple(t['damage']),),damage_fixed_bonus=f['dmg_fixed'],critical_sequence=tuple(t['crit']),attack_roll_attempts=tuple(attempts),attack_bonus=f['atk_fixed'],lab_negative_critical_policy=True)
 before=ev['before_hp'];post_rd=ev['net'];original_after=ev['after_hp']
 prevented=min(70,post_rd) if armored else 0
 true_post=max(0,post_rd-prevented)
 source_after=max(0,before-true_post)
 hp_loss=before-source_after;over=max(0,true_post-before)
 if armored:
  defender.hp=source_after
  ss.record({'action':'SOURCE_ARMOR_POST_RD_PREVENTION','by':'VAROK','incoming_attack_seq':ev['seq'],'declaration_seq':decl['seq'],'source_page':ACTORS['VAROK']['page'],'post_rd_unmitigated':post_rd,'prevented':prevented,'hp_before':before,'native_hp_temporarily':original_after,'hp_final':source_after,'hp_loss_actual_final':hp_loss,'overkill_final':over,'PA_spent_in_declaration':50,'once_per_scene':True,'provenance_warning':'SOURCE_ITEM_IN_MEMORY_OFFSET_ATOMIC_R18_NOT_HEALING'})
 end_source_turn(ss,who)
 m=st['metrics'];m['attack_attempts']+=1;m['hits']+=int(ev['hit']);m['gross_hit']+=ev['raw'];m['post_rd_before_item']+=post_rd;m['item_prevention']+=prevented;m['hp_lost']+=hp_loss;m['overkill']+=over;m['pa_activation']+=50 if armored else 0;m['reactions']+=int(armored);m['crit_positive']+=int(ev['critical']=='POSITIVE');m['crit_negative']+=int(ev['critical']=='NEGATIVE')
 if defender.hp==0:
  st['phase']='FINISHED';st['winner']=who;st['finish_reason']='HP_ZERO_SOURCE_SCOPED';st['active']=None;sched={'ko':other,'next_turn':None}
 else:
  sched=r18._next_turn(st);up=st['active'];ss.actors[up].standard=0;begin_source_turn(ss,up)
 sync(st,ss)
 detail={'actor':who,'target':other,'actor_turn':turn,'source_page':f['page'],'target_page':fd['page'],'seed':st['seed'],'policy':st['policy'],'tape':copy.deepcopy(t),'attack':copy.deepcopy(ev),'item_active':armored,'item_prevented':prevented,'item_after_hp':source_after,'final_hp_loss':hp_loss,'final_overkill':over,'PA_after':{k:a.pa for k,a in ss.actors.items()},'HP_after':{k:a.hp for k,a in ss.actors.items()},'Reaction_after':{k:a.reaction for k,a in ss.actors.items()},'native_events':copy.deepcopy(ss.events[start_native:]),'scheduler':sched}
 st['history'].append({'seq':seq,'actor':who,'target':other,'hp_loss':hp_loss,'item':armored,'item_prevented':prevented})
 return detail

def fight(outdir,seed,policy,max_attacks=70):
 if policy not in ('ARMOR_ON_FIRST_SOURCE_ATTACK','ARMOR_OFF'):raise EffectBlocked('POLICY_UNREGISTERED')
 outdir=pathlib.Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
 db=outdir/f'R180_VAROK_LEVIATHAN_{policy}_SEED{seed}.sqlite'
 setup(db,seed,policy)
 st,_,_=r18.load(db)
 r18.event_commit(db,f'LAB-CMD-R180-{policy}-{seed}-INIT','SOURCE_ORDER_CONTACT_START',{'seed':seed,'initiative':initiative(seed),'geometry':st['geometry']},start)
 for i in range(max_attacks):
  st,_,_=r18.load(db)
  if st['phase']!='ACTIVE':break
  who=st['active'];other='VAROK' if who=='LEVIATHAN' else 'LEVIATHAN'
  turn=1+sum(h['actor']==who for h in st['history'])
  r18.event_commit(db,f'LAB-CMD-R180-{policy}-{seed}-{i+1:04d}','SOURCE_PHYSICAL_ATTACK_WITH_OPTIONAL_ARMOR',{'actor':who,'target':other,'seed':seed,'turn_number':turn,'policy':policy,'tape':tape(seed,who,turn,False)},attack)
 st,head,rev=r18.load(db);write_checkpoint(db)
 return {'db':db.name,'seed':seed,'policy':policy,'phase':st['phase'],'winner':st['winner'],'rounds':st['round'],'attempts':st['metrics']['attack_attempts'],'metrics':st['metrics'],'hp_final':{k:v['resource']['hp'] for k,v in st['actors'].items()},'pa_final':{k:v['resource']['pa'] for k,v in st['actors'].items()},'commits':rev,'native_events':len(st['native_events']),'head':head,'censored':st['phase']!='FINISHED'}

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('outdir');p.add_argument('--seed',type=int,default=17718001);p.add_argument('--policy',default='ARMOR_ON_FIRST_SOURCE_ATTACK');a=p.parse_args();print(json.dumps(fight(a.outdir,a.seed,a.policy),indent=2,ensure_ascii=False))
