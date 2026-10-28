"""R216: new TEST 2x1 active multi-actor movement + physical/reaction/cure/spell integration.
Native R18 transaction; R215/214 native resolvers reused; no historical runner invoked.
Fixture adjacency/speed are explicitly LAB, not a world metric definition.
"""
import copy,hashlib,json,math,sys
from pathlib import Path
from dataclasses import asdict
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]; sys.path[:0]=[str(ROOT/'code'),str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import r215_integrated_native as old
import r214_native_causal_bilateral as aoo
import vlab_r18_interactive as j
from vlab_effects_v08 import (Scene,Combatant,AbilitySource,FrozenRuleEvidence,ActorActionState,
 move_via_verified_path,begin_source_turn,end_source_turn,declare_opportunity_reaction,
 apply_reconstituicao_seiva,apply_pulso_estabilizacao,cast_source_specified_spell,Resistances,EffectBlocked)
PRB=(ROOT/'sources/R216_PREREG.json').read_bytes();PR=json.loads(PRB);PH=hashlib.sha256(PRB).hexdigest()
EB=(ROOT/'sources/R216_ERISTAN_PRIMARY_MECHANICAL_SNAPSHOT.json').read_bytes();EH=hashlib.sha256(EB).hexdigest()
E_PROOF=FrozenRuleEvidence(old.PAGES['E'],'R216-ERISTAN-PRIMARY-EXCERPT',EH,'2026-10-21','NOTION-MECHANICAL-EXCERPT-NOT-FULL-PAGE-HASH')
old.PROOFS['E']=E_PROOF
# Only a source pointer is updated, without modifying native effect rules.
for name in ('HEAL','PULSE','SPORES'):
 old_src=getattr(old,name)
 setattr(old,name,AbilitySource(old_src.action_id,old_src.kind,old_src.economy,old_src.source_page_id,E_PROOF.rule_id,
  old_src.source_status,required_pa=old_src.required_pa,target_scope=old_src.target_scope,
  reaction_trigger=old_src.reaction_trigger,requires_range_check=old_src.requires_range_check,
  effect_adapter_ready=True,effect_adapter_id='V081'))
MOVE=AbilitySource('R216-NATIVE-DECLARED-PATH','move','MOVEMENT',old.PAGES['V'],old.PROOFS['V'].rule_id,
 'RULE-DERIVED',target_scope='POSITION',effect_adapter_ready=True,effect_adapter_id='V081')
class R216Gate(RuntimeError):pass

def init(db,seed,policy,team_label='TEAM_A'):
 if db.exists():raise R216Gate('RUN_ID_COLLISION')
 j.init_db(str(db),'A',seed);st=j.initial('A',seed)
 positions={'V':'(0, 0)','R':'(3, 1)','E':'(0, 3)'}
 actors={k:asdict(old.actor(k)) for k in ['V','R','E']}
 for k in actors: actors[k]['position']=positions[k];actors[k]['standard']=0;actors[k]['movement']=1;actors[k]['reaction']=1
 st.update({'scene':f'R216-INTEGRATED-{seed}-{policy}-{team_label}','seed':seed,'phase':'ACTIVE','round':1,
  'turn':0,'active':'V','order':['V','R','E'],'actors':actors,'native_events':[],
  'r216':{'pre_hash':PH,'eristan_excerpt_sha256':EH,'policy':policy,'team_label':team_label,
    'geometry_contract':'EXPLICIT-R44-CONDITIONAL-TEST-NOT-WORLD-CANON',
    'movement_speed_source':'SCENE_LOWER_BOUND_4M_TEST_ONLY',
    'max_rounds':4,'turns':{'V':0,'R':0,'E':0},
    'stats':{'attacks':0,'physical_hits':0,'physical_hp_loss':0,'moves':0,'aoo':0,'aoo_reactions':0,
      'guard':0,'guard_pa':0,'guard_prevented':0,'spells':0,'spell_hp_loss':0,'spell_pa':0,
      'heals':0,'healed':0,'heal_gross':0,'heal_pa':0,'healing_actions':0,'target_switches':0},
    'observed_target_log':[],'decisions':[]}})
 con=j.connect(str(db));h=j.sha({'seed':seed,'prehash':PH,'team_label':team_label,'policy':policy})
 with con:
  for k,v in [('state',j.canonical(st)),('scene',st['scene']),('genesis',h),('head',h)]:con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 con.close()

def scene(st):return Scene({k:Combatant(**copy.deepcopy(v)) for k,v in st['actors'].items()},events=copy.deepcopy(st['native_events']),seed=st['seed'],provenance='R216-MESTRE-SIDE-TEST-CONDITIONAL')
def sync(st,s):
 st['native_events']=copy.deepcopy(s.events)
 for k,c in s.actors.items():st['actors'][k]=asdict(c)

def coords(text):
 import ast
 p=ast.literal_eval(text)
 if not isinstance(p,tuple) or len(p)!=2:return None
 return tuple(float(v) for v in p)

def move(s,actor,to,travel_m,reason):
 a=s.actors[actor];fr=coords(a.position);dist=math.dist(fr,to)
 if dist>travel_m+1e-9:raise R216Gate('TRAVEL_SHORTER_THAN_ACTUAL_DISTANCE')
 src=MOVE;pro=old.PROOFS['V']
 s.record({'action':'R216_PATH_DECISION','by':actor,'from':a.position,'to':list(to),'geometric_distance':dist,
   'contract':'TEST_OPEN_PATH_LOWER_BOUND_NOT_WORLD_ADJACENCY','declared_travel_m':travel_m,'reason':reason})
 return move_via_verified_path(s,actor,source=src,
  state=ActorActionState(actor,20,a.pa,(src.action_id,),movement_available=True,geometry_confirmed=True,environment_contract=True),
  proofs=(pro,),destination=str(tuple(to)),path_evidence='R216_TEST_SCENE_SPECIFIC_SEGMENT_'+reason,
  travel_cost=Fraction(travel_m),speed=Fraction(4))

def aoo_while_R_exits(s,seed,round_no):
 # One declared historical adjacency edge R(3,1) ↔ V(2,1), ending with path R -> (1,3).
 if coords(s.actors['R'].position)!=(3.0,1.0) or coords(s.actors['V'].position)!=(2.0,1.0):raise R216Gate('AOO_FIXTURE_EDGE_MISMATCH')
 if s.actors['V'].reaction!=1:
  s.record({'action':'R216_AOO_DECLINED','by':'V','reason':'REACTION_UNAVAILABLE','pre_pos_R':s.actors['R'].position});return None
 src=aoo.AOO['V']
 s.record({'action':'R216_EXPLICIT_EDGE_EXIT','by':'R','opponent':'V','edge':'R44_SCENE_ONLY','movement_not_published':True})
 intent=declare_opportunity_reaction(s,'V','R',source=src,
  state=ActorActionState('V',20,s.actors['V'].pa,(src.action_id,),reaction_available=True,reaction_trigger_observed='EXIT_ADJACENT',range_confirmed=True,enemy_ids_visible=('R',)),
  proofs=(aoo.PROOFS['V'],),fixture_adjacency_id='R216_TEST_EXPLICIT_EDGE_V_R_R2')
 result=aoo.attack(s,seed,'V','R','R216-'+str(round_no)+'-EXIT',intent_seq=intent['seq'])
 return result

def safe_spores(s,seed,tag):
 own=coords(s.actors['E'].position);ally=coords(s.actors['V'].position);enemy=coords(s.actors['R'].position)
 centers=[(8.,1.),(1.,8.),(-5.,7.),(7.,-3.),(6.,6.)]+[(enemy[0]+5*math.cos(math.pi*k/8), enemy[1]+5*math.sin(math.pi*k/8)) for k in range(16)]
 scored=[]
 for ci,c in enumerate(centers):
  if math.dist(own,c)>25:continue
  included=[k for k,p in [('E',own),('V',ally),('R',enemy)] if math.dist(p,c)<=5+1e-9]
  scored.append({'center':c,'included':included,'ally_hit':int('V' in included),'caster_hit':int('E' in included),'enemy_hit':int('R' in included),'index':ci})
 feasible=[x for x in scored if x['enemy_hit']==1 and x['ally_hit']==0 and x['caster_hit']==0]
 if not feasible:raise R216Gate('NO_SOURCE_LEGAL_SAFE_CENTER')
 choice=sorted(feasible,key=lambda x:(x['index']))[0]
 dmg=old.dice(seed,tag+'-SPORES-DMG',10,10);save=old.dice(seed,tag+'-SPORES-SAVE-R',4,6)
 passed=sum(save)+57>76;gross=sum(dmg)+10
 if passed and gross%2:
  s.record({'action':'R223_TENTATIVE_ROUNDING_EVIDENCE','by':'E','damage_before_half':gross,
    'rounded_down':gross//2,'source_status':'MASTER_TENTATIVE_TEST_ONLY',
    'decision':'USER_MESTRE_UNCERTAIN_2026-10-21','not_world_canon':True})
 s.record({'action':'R216_GEOMETRY_STATE_DECISION','by':'E','position_snapshot':{'E':own,'V':ally,'R':enemy},
  'eligible_centers':scored,'chosen_center':choice['center'],'included':choice['included'],'save_rolls':save,
  'save_total':sum(save)+57,'save_passed':passed,'spell_gross':gross,'source':'ERISTAN_NOTION_20261016'})
 src=old.SPORES
 return cast_source_specified_spell(s,'E','R',source=src,state=ActorActionState('E',20,s.actors['E'].pa,(src.action_id,),standard_available=True,range_confirmed=True,enemy_ids_visible=('R',)),
   proofs=(E_PROOF,),damage=gross,damage_tag='planta',rd=Resistances(general=0,provenance='R209-LAB-ONLY-MAGIC-RD-UNKNOWN'),
   explicit_save_effect='SAVE-HALF',target_save_exceeds_cd=passed,damage_rolls=dmg,damage_faces=10,documented_flat_bonus=10,
   odd_half_rounding_test_policy='FLOOR_MASTER_TENTATIVE_TEST',rounding_decision_source='USER_MESTRE_UNCERTAIN_2026-10-21')

def standard_heal(s,seed,tag):
 if math.dist(coords(s.actors['E'].position),coords(s.actors['V'].position))>5:raise R216Gate('HEAL_RANGE_GT_5')
 rr=old.dice(seed,tag+'-RECONSTITUICAO',8,10)
 src=old.HEAL
 return apply_reconstituicao_seiva(s,'E','V',source=src,state=ActorActionState('E',20,s.actors['E'].pa,(src.action_id,),standard_available=True,ally_ids_visible=('V',)),
  proofs=(E_PROOF,),dice_rolls=rr,range_met=True,gloves_equipped=True)

def reactive_heal(s,seed,tag):
 if math.dist(coords(s.actors['E'].position),coords(s.actors['V'].position))>3:return None
 if s.actors['E'].reaction!=1 or s.actors['V'].hp<=0 or s.actors['V'].hp>=s.actors['V'].maximum_hp:return None
 rr=old.dice(seed,tag+'-PULSO',3,10);src=old.PULSE
 return apply_pulso_estabilizacao(s,'E','V',source=src,state=ActorActionState('E',20,s.actors['E'].pa,(src.action_id,),reaction_available=True,
  reaction_trigger_observed='ALLY_AFTER_DAMAGE',ally_ids_visible=('V',)),proofs=(E_PROOF,),dice_rolls=rr,range_met=True,damage_just_resolved=True,gloves_equipped=True)

def turn(st,p,seq):
 if st['phase']!='ACTIVE' or p['seed']!=st['seed'] or p['pre']!=PH or p['actor']!=st['active']:raise R216Gate('TURN_PREFLIGHT')
 s=scene(st);who=p['actor'];turnno=st['round'];policy=st['r216']['policy'];before=len(s.events)
 stats=st['r216']['stats'];begin_source_turn(s,who)
 if st['turn']==0:
  s.record({'action':'R222_INITIATIVE_EFFECTIVE_ORDER','by':who,'roll_receipts':st['r222']['rolls'],'order':st['order'], 'branch':st['r222']['arm'], 'source':'NOTION_ON5_4d6_PLUS_INITIATIVE_BONUS','pre_hash':st['r222']['prereg_sha256']})
  s.record({'action':'R222_POSITION_AND_GUARD_POLICY_FIXTURE','by':'E','position_E':'(0, 4)','V_precombat_hp':734,'guard_policy':'VAROK_DECLINES_GUARD_IN_ROUND1','pulse_range_source':'3M_NOT_MET','world_block_size':'UNKNOWN','stream_map_mode':st['r222']['mode']})
 if who=='V':
  if turnno==1:
   move(s,'V',(2.,1.),3,'V_APPROACH_R1');stats['moves']+=1
  elif turnno==3 and coords(s.actors['V'].position)==(2.0,1.0):
   move(s,'V',(2.,3.),2,'V_FOLLOW_R3');stats['moves']+=1
  if s.actors['R'].hp>0:
   s.record({'action':'R216_PHYSICAL_RANGE_GATE','by':'V','target':'R','fixture_edge':f'V_R_ROUND_{turnno}','state':{'V':s.actors['V'].position,'R':s.actors['R'].position}})
   attack,guard=old.normal_attack(s,st['seed'],'V','R',f'R216-PHYS-R{turnno}-V',guard_policy=True)
   stats['attacks']+=1;stats['physical_hits']+=int(attack['hit']);stats['physical_hp_loss']+=attack['hp_loss_actual']
   if guard:stats['guard']+=1;stats['guard_pa']+=40;stats['guard_prevented']+=attack['post_rd_guard_reduction']
 elif who=='R':
  if turnno==2 and s.actors['R'].hp>0:
   if s.actors['V'].hp>0:
    reaction=aoo_while_R_exits(s,st['seed'],turnno)
    if reaction:
     stats['aoo']+=1;stats['aoo_reactions']+=1
   if s.actors['R'].hp>0:
    move(s,'R',(1.,3.),3,'R_FLANK_E_R2');stats['moves']+=1
  previous_heals=sum(1 for e in s.events if e.get('by')=='E' and e.get('action') in ('RECONSTITUICAO_SEIVA','PULSO_ESTABILIZACAO'))
  # Decision limited to actor-observable recent support actions + positions, NOT enemy hidden HP.
  chosen='V' if turnno==1 else 'E' if turnno==2 else 'E' if previous_heals>0 and turnno==3 else 'V'
  if chosen=='V' and s.actors['V'].hp<=0:chosen='E'
  if chosen=='E' and s.actors['E'].hp<=0:chosen='V'
  st['r216']['observed_target_log'].append({'round':turnno,'target':chosen,'observed_E_heal_events':previous_heals})
  s.record({'action':'R216_ENEMY_TARGET_DECISION','by':'R','chosen':chosen,'observed_heals':previous_heals,
    'source_visible':'ALLY_RECENT_ACTIONS_AND_POSITIONS','own_position':s.actors['R'].position})
  if s.actors[chosen].hp>0:
   a,_=old.normal_attack(s,st['seed'],'R',chosen,f'R216-PHYS-R{turnno}-R-'+chosen,guard_policy=(chosen=='V' and turnno>1))
   stats['attacks']+=1;stats['physical_hits']+=int(a['hit']);stats['physical_hp_loss']+=a['hp_loss_actual']
   if a.get('post_rd_guard_reduction',0):stats['guard']+=1;stats['guard_pa']+=50;stats['guard_prevented']+=a['post_rd_guard_reduction']
   if chosen=='V' and a['hp_loss_actual']>0 and s.actors['V'].hp>0 and policy=='PROTECTIVE':
    if (s.actors['V'].maximum_hp-s.actors['V'].hp)>=25:
     rh=reactive_heal(s,st['seed'],f'R216-R{turnno}-E-REACTION')
     if rh:stats['heals']+=1;stats['healed']+=rh['actual_heal'];stats['heal_gross']+=rh['gross_heal'];stats['heal_pa']+=45
 elif who=='E':
  missing=s.actors['V'].maximum_hp-s.actors['V'].hp;limit=PR['policy_thresholds'][policy]
  legal_heal=0<s.actors['V'].hp<s.actors['V'].maximum_hp and math.dist(coords(s.actors['E'].position),coords(s.actors['V'].position))<=5
  decision='HEAL' if missing>=limit and legal_heal else 'SPORES'
  st['r216']['decisions'].append({'round':turnno,'policy':policy,'missing_V':missing,'distance_V':math.dist(coords(s.actors['E'].position),coords(s.actors['V'].position)),
    'heal_range_met':legal_heal,'chosen':decision,'E_pa_before':s.actors['E'].pa})
  s.record({'action':'R216_SUPPORT_OBSERVED_STATE','by':'E','ally':'V','missing_hp':missing,'policy_threshold':limit,'heal_legal':legal_heal,'choice':decision})
  if decision=='HEAL':
   ev=standard_heal(s,st['seed'],f'R222-HEAL-BANK-{turnno}');stats['heals']+=1;stats['healed']+=ev['actual_healed'];stats['heal_gross']+=ev['gross_heal'];stats['heal_pa']+=75;stats['healing_actions']+=1
  else:
   ev=safe_spores(s,st['seed'],f'R222-SPORE-BANK-{turnno}');stats['spells']+=1;stats['spell_pa']+=80;stats['spell_hp_loss']+=ev['hp_before']-ev['hp_after']
 else:raise R216Gate('UNKNOWN_ACTOR')
 if s.actors[who].standard==1: raise R216Gate('TURN_WITH_UNUSED_STANDARD')
 end_source_turn(s,who)
 st['r216']['turns'][who]+=1;st['turn']+=1
 ko=[a for a in ['V','R','E'] if s.actors[a].hp<=0]
 if ko:st['phase']='KO_HP0';st['active']=None
 elif who==st['order'][-1] and st['round']>=st['r216']['max_rounds']:st['phase']='CENSORED_HORIZON';st['active']=None
 else:
  idx=st['order'].index(who)
  if idx==len(st['order'])-1:st['round']+=1
  st['active']=st['order'][(idx+1)%3]
 sync(st,s)
 return {'who':who,'round':turnno,'events_added':s.events[before:],'phase':st['phase']}

def execute(seed,policy,team_label='TEAM_A'):
 db=ROOT/'evidence/db'/f'R216_TEAM_{policy}_{team_label}_S{seed}.sqlite';init(db,seed,policy,team_label)
 for i in range(12):
  st,_,_=j.load(db)
  if st['phase']!='ACTIVE':break
  j.event_commit(str(db),f'LAB-CMD-R216-{seed}-{policy}-{team_label}-{i+1}','R216_INTEGRATED_TURN',
   {'seed':seed,'pre':PH,'actor':st['active']},turn)
 st,head,rev=j.load(db);return {'seed':seed,'policy':policy,'team_label':team_label,'db':db.name,
  'commits':rev,'phase':st['phase'],'round':st['round'],'turns':st['r216']['turns'],
  'stats':st['r216']['stats'],'hp':{k:v['hp'] for k,v in st['actors'].items()},
  'pa':{k:v['pa'] for k,v in st['actors'].items()},'reactions':{k:v['reaction'] for k,v in st['actors'].items()},
  'positions':{k:v['position'] for k,v in st['actors'].items()},'events':len(st['native_events']),'head':head}

def main():
 results=[];blocked=[]
 for seed in PR['run_seeds']:
  for policy in PR['arms']:
   try:results.append(execute(seed,policy))
   except Exception as e:blocked.append({'seed':seed,'policy':policy,'error':repr(e),'sqlite':'R216_TEAM_'+policy+'_TEAM_A_S'+str(seed)+'.sqlite'})
 (ROOT/'evidence/reports/R216_EXECUTION_RESULTS.json').write_text(json.dumps({'results':results,'blocked':blocked},indent=2,ensure_ascii=False))
 print(json.dumps({'admitted':len(results),'blocked':blocked,'commits':sum(x['commits'] for x in results),
  'censures':sum(x['phase']=='CENSORED_HORIZON' for x in results),'KO':sum(x['phase']=='KO_HP0' for x in results)},indent=2))
if __name__=='__main__':main()
