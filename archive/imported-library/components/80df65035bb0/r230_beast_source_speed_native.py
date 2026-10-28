"""R230 Beast speed across 5 ranks, R18+native movement and physical attack.
No new engine. Source speed proven; attributes LAB-only; battle not canonical benchmark.
"""
import copy,sys,json,hashlib,random
from dataclasses import asdict
from pathlib import Path
from fractions import Fraction
R=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(R/'runtime/native'),str(R/'runtime/fusion_stage12')]
import vlab_r18_interactive as j
sys.modules.pop('vlab_effects_v08',None)
sys.path.insert(0,str(R/'runtime/native'))
from vlab_l04 import build_beast,build_human,RANK_TEST_DICE
from vlab_effects_v08 import (Combatant,Scene,AbilitySource,FrozenRuleEvidence,ActorActionState,Resistances,
 move_via_verified_path,apply_weapon_attack,effective_movement_speed,EffectBlocked)
PRE_B=(R/'sources/R230_PREREG_BEFORE_EXEC.json').read_bytes();PRE=json.loads(PRE_B);PH=hashlib.sha256(PRE_B).hexdigest()
SR_B=(R/'sources/R230_BEAST_SPEED_RULE_EXCERPT.json').read_bytes();RULE=json.loads(SR_B);SH=hashlib.sha256(SR_B).hexdigest()
BSRC='3ebc2b324ede81f4992ac88a3588cacd'; CFSRC='3ebc2b324ede81449222f3c06b840613';COMBAT='3ebc2b324ede81f1be4be8804ac113c0'
MOVE=AbilitySource('R230-SOURCE-R8-MOVEMENT','move','MOVEMENT',BSRC,'R230-SPEED-R8','RULE-DERIVED',target_scope='POSITION',effect_adapter_ready=True,effect_adapter_id='V081')
ATK=AbilitySource('R230-SOURCE-BE-BASIC','attack','STANDARD',BSRC,'R230-BE-BASE-DAMAGE','RULE-DERIVED',requires_range_check=True,effect_adapter_ready=True,effect_adapter_id='V081')
PROOF_MOVE=FrozenRuleEvidence(BSRC,MOVE.rule_id,SH,'2026-10-21','PRIMARY-EXCERPT-R8-ONLY')
PROOF_ATK=FrozenRuleEvidence(BSRC,ATK.rule_id,SH,'2026-10-21','PRIMARY-EXCERPT-DAMAGE-ALLOCATION-HOLD')
RANK_ORDER=['Bronze','Prata','Ouro','Ouro Negro','Lendário']
def source_speed(rank,des,titan):
 form=RULE['titan' if titan else 'normal'][rank];q=int(form.split('+')[0]);return Fraction(q)+Fraction(des,4)
def dice(seed,label,n,faces):
 val=int.from_bytes(hashlib.sha256(f'R230|{seed}|{label}|{n}d{faces}'.encode()).digest(),'big');rd=random.Random(val);return tuple(rd.randint(1,faces) for _ in range(n))
def case(seed,rank,star):
 x=build_beast(rank,star,seed+100);h=build_human('Bronze',1,seed+200)
 speed=source_speed(rank,x.stats['DES'],'Titã' in x.traits)
 level=x.level;pos=f'({int(speed)},0)'
 be=Combatant('BE',x.health,None,Fraction(x.ca['exact']),x.stats['CON'],0,0,0,'(0,0)',rank=rank,maximum_hp=x.health,base_speed=str(speed),beast_rank_index=level)
 ed=Combatant('ED',h.health,h.pa_free,Fraction(h.ca['exact']),h.stats['CON'],0,0,0,pos,rank='Bronze',maximum_hp=h.health)
 br=asdict(be);hr=asdict(ed);br['ca']=str(be.ca);hr['ca']=str(ed.ca)
 state={'scene':f'R230-R8-{rank}-{seed}','phase':'ACTIVE','seed':seed,'round':1,'actors':{'BE':br,'ED':hr},'native_events':[],
  'r230':{'seed':seed,'rank':rank,'star':star,'level':level,'beast_attrs':x.stats,'beast_hp':x.health,'source_speed_exact':str(speed),
  'source_speed_formula':RULE['titan' if 'Titã' in x.traits else 'normal'][rank],'titan':('Titã' in x.traits),
  'beast_damage_base':x.base_attack_dice,'beast_attack_test_dice':RANK_TEST_DICE[rank],'beast_rd':x.rd,
  'beast_stat_origin':'LAB_DISTRIBUTION_ONLY','ED_stat_origin':'LAB_HUMAN_B1','physical_species':None,
  'geometry':'TEST_STRAIGHT_OPEN','world_canon':False,'prereg_sha':PH,'source_excerpt_sha':SH,'outcome':None}}
 return state

def commit(st,payload,seq):
 s=Scene({k:Combatant(**{**copy.deepcopy(v),'ca':Fraction(v['ca'])}) for k,v in st['actors'].items()},events=copy.deepcopy(st['native_events']),seed=st['seed'],provenance='R230-BE-SOURCE-R8-LAB-TEST')
 b=s.actors['BE'];e=s.actors['ED'];rec=st['r230'];snap=len(s.events)
 assert st['phase']=='ACTIVE' and payload['prereg']==PH and payload['source']==SH
 speed=effective_movement_speed(b);assert speed==Fraction(rec['source_speed_exact'])
 travel=Fraction(int(speed))
 move_via_verified_path(s,'BE',source=MOVE,
   state=ActorActionState('BE',rec['level'],b.pa,(MOVE.action_id,),movement_available=True,geometry_confirmed=True,environment_contract=True),
   proofs=(PROOF_MOVE,),destination=f'({int(speed)},0)',path_evidence='R230-TEST-OPEN-STRAIGHT-SOURCE-R8',travel_cost=travel,speed=speed)
 # Physical generic base attack via existing native reducer. The mapping is conditional; not official Beast ability.
 expression=rec['beast_damage_base'];n,f=map(int,expression.split('d'))
 an,af=map(int,rec['beast_attack_test_dice'].split('d'))
 tohit=dice(st['seed'],'BE-ATTACK',an,af);dmg=dice(st['seed'],'BE-DAMAGE',n,f)
 bonus=rec['beast_attrs']['FOR']+({False: {'Bronze':6,'Prata':8,'Ouro':10,'Ouro Negro':12}, True:{'Bronze':8,'Prata':11,'Ouro':14,'Ouro Negro':17,'Lendário':22}}[rec['titan']][rec['rank']])
 # Critical tape is fixed and noncritical by experiment design; no statistical critical inference.
 s.record({'action':'R230_BE_PRE_REGISTERED_RNG_TAPE','dice_attack':tohit,'dice_damage':dmg,'dice_critical':(3,4,3),'mode':'DIRECTED_NONCRIT_LAB_ONLY'})
 receipt=apply_weapon_attack(s,'BE','ED',source=ATK,
  state=ActorActionState('BE',rec['level'],b.pa,(ATK.action_id,),standard_available=True,range_confirmed=True,enemy_ids_visible=('ED',)),
  proofs=(PROOF_ATK,),roll_score=sum(tohit)+bonus,damage=sum(dmg),damage_tag='impacto',rd=Resistances(general=0,provenance='ED-UNARMORED-LAB'),
  damage_dice_groups=((n,f),),damage_roll_groups=(dmg,),damage_fixed_bonus=0,
  critical_sequence=(3,4,3),attack_roll_attempts=(tohit,),attack_bonus=bonus)
 st['actors']={k:{**asdict(v),'ca':str(v.ca)} for k,v in s.actors.items()};st['native_events']=copy.deepcopy(s.events)
 st['phase']='CENSORED_AFTER_ONE_BE_TURN';rec['outcome']={'movement_m':str(travel),'attack_hit':receipt['hit'],'attack_net':receipt['hp_loss_actual'],'ED_hp_after':e.hp,'beast_attack_bonus':bonus,
 'NO_KO_CANON':'HP<=0 IS NOT CANONICAL_DEATH','native_event_ids':list(range(snap+1,len(s.events)+1))}
 return {'new_events':copy.deepcopy(s.events[snap:]),'result':copy.deepcopy(rec['outcome'])}

def run():
 out=[]
 for seed,(rank,star) in zip(PRE['seeds'],PRE['rank_stars']):
  db=R/'evidence/db'/f'R230_BE_{rank.replace(" ","")}{star}_S{seed}.sqlite'
  if db.exists():raise FileExistsError('RUN-ID_USED '+str(db))
  j.init_db(str(db),'A',seed);st=j.initial('A',seed);st.update(case(seed,rank,star));con=j.connect(str(db));gen=j.sha({'R230_prereg':PH,'seed':seed,'source_excerpt':SH})
  with con:
   for k,val in [('state',j.canonical(st)),('scene',st['scene']),('genesis',gen),('head',gen)]:con.execute('update meta set value=? where key=?',(val,k))
  con.close()
  j.event_commit(str(db),f'LAB-CMD-R230-{rank.replace(" ","")}{star}-{seed}', 'R230_BE_MOVE_AND_BASIC', {'prereg':PH,'source':SH},commit)
  fin,hd,rev=j.load(str(db));out.append({'seed':seed,'rank':rank,'rank_star':star,'speed':fin['r230']['source_speed_exact'],'hp':fin['r230']['outcome']['ED_hp_after'],'events':len(fin['native_events']),'commits':rev,'head':hd})
 (R/'evidence/reports/R230_RESULTS.json').write_text(json.dumps({'status':'NEEDS_INDEPENDENT_AUDIT','source_status':'RULE_DERIVED_NOT_SPECIES','units':len(out),'historical_replays':0,'cases':out},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':run()
