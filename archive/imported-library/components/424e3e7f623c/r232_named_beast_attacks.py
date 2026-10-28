"""R232 named VZ PRECREATE Beast native basic attack actuator. NOT full combat, NO species stats invented."""
import json,hashlib,random,sys,copy
from pathlib import Path
from dataclasses import asdict
from fractions import Fraction
R=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(R/'runtime/native'),str(R/'runtime/fusion_stage12')]
import vlab_r18_interactive as j
sys.modules.pop('vlab_effects_v08',None)
sys.path.insert(0,str(R/'runtime/native'))
from vlab_effects_v08 import Combatant,Scene,AbilitySource,FrozenRuleEvidence,ActorActionState,Resistances,apply_weapon_attack
PRE_B=(R/'sources/R232_PREREG_BEFORE_EXEC.json').read_bytes();PRE=json.loads(PRE_B);PREH=hashlib.sha256(PRE_B).hexdigest()
SOURCE_B=(R/'sources/R232_VZ_FROZEN_PRIMARY_EXCERPTS.json').read_bytes();SOURCE=json.loads(SOURCE_B);SOURCEH=hashlib.sha256(SOURCE_B).hexdigest()
SRC=SOURCE['source_page_id']; TARGET=SOURCE['reference_target']
def roll(seed,label,n,f):
 h=int.from_bytes(hashlib.sha256(f'R232|{seed}|{label}|{n}d{f}'.encode()).digest(),'big');rr=random.Random(h)
 return tuple(rr.randint(1,f) for _ in range(n))
def fixture(seed,sp):
 # Unknown attributes intentionally NOT presented as sourced. HP=1/CA=0 are interface stand-ins only.
 beast=Combatant('BE',1,0,Fraction(0),0,0,0,0,'(0,0)',rank=sp['rank'],maximum_hp=1)
 target=Combatant('VAROK',TARGET['hp'],324,Fraction(TARGET['ca']),20,0,0,0,'(1,0)',rank='Ouro Negro',maximum_hp=TARGET['hp'])
 def fmt(x):v=asdict(x);v['ca']=str(x.ca);return v
 return {'scene':f'R232-SPECIES-{sp["id"]}-S{seed}','phase':'ACTIVE','seed':seed,'round':1,'actors':{'BE':fmt(beast),'VAROK':fmt(target)},'native_events':[],
 'r232':{'seed':seed,'species_id':sp['id'],'source_status':'VZ-PRECREATE-NOT-P4','beast_full_stats':'UNKNOWN','actor_hp_ca':'LAB_INTERFACE_STANDINS_1HP_0CA','referenced_target_source':'VAROK-PROPOSED','geometry':'TEST_ADJACENT_CONFIRMED_FOR_STRIKE_ONLY','source_sha':SOURCEH,'prereg_sha':PREH,'outcome':None}}
def fn(st,payload,seq):
 sp=next(x for x in SOURCE['attacks'] if x['id']==st['r232']['species_id'])
 assert st['phase']=='ACTIVE' and payload['prereg']==PREH and payload['source']==SOURCEH
 actors={k:Combatant(**{**copy.deepcopy(v),'ca':Fraction(v['ca'])}) for k,v in st['actors'].items()}
 s=Scene(actors,events=copy.deepcopy(st['native_events']),seed=st['seed'],provenance='R232-NAMED-VZ-PRECREATE-ATTACK-TEST')
 source=AbilitySource('R232-'+sp['id']+'-'+sp['action'].replace(' ','_'),'attack','STANDARD',SRC,'R232-BASIC-'+sp['id'],'RULE-DERIVED',required_pa=0,requires_range_check=True,effect_adapter_ready=True,effect_adapter_id='V081')
 proof=FrozenRuleEvidence(SRC,source.rule_id,SOURCEH,'2026-10-21','VZ-PRIMARY-EXCERPT-NOT-FULL-PAGE')
 a,f=map(int,sp['attack_dice'].split('d'));n,df=map(int,sp['damage_dice'].split('d'))
 ar=roll(st['seed'],sp['id']+'-ATTACK',a,f);dr=roll(st['seed'],sp['id']+'-DAMAGE',n,df)
 s.record({'action':'R232_FROZEN_RNG_TAPE','species_id':sp['id'],'source_name':sp['name'],'source_action':sp['action'],'source_sha':SOURCEH,'attack_rolls':ar,'damage_rolls':dr,'critical_evidence':(3,4,3),'policy':'DIRECTED_NONCRIT_LAB_ONLY'})
 x=apply_weapon_attack(s,'BE','VAROK',source=source,
 state=ActorActionState('BE',sp['ordinal'],0,(source.action_id,),standard_available=True,range_confirmed=True,enemy_ids_visible=('VAROK',)),
 proofs=(proof,),roll_score=sum(ar)+sp['attack_bonus'],damage=sum(dr),damage_tag=sp['damage_type'],rd=Resistances(general=TARGET['physical_rd'],provenance='VAROK-SOURCE-PHYSICAL-RD'),
 damage_dice_groups=((n,df),),damage_roll_groups=(dr,),damage_fixed_bonus=0,critical_sequence=(3,4,3),attack_roll_attempts=(ar,),attack_bonus=sp['attack_bonus'])
 st['actors']={k:{**asdict(v),'ca':str(v.ca)} for k,v in s.actors.items()};st['native_events']=copy.deepcopy(s.events)
 st['phase']='CENSORED_SINGLE_ATTACK_NOT_FIGHT';st['r232']['outcome']={'hit':x['hit'],'damage':x['hp_loss_actual'],'varok_hp':s.actors['VAROK'].hp,'critical':x['critical'],'native_event_count':len(s.events),'official_benchmark':False}
 return {'new_events':copy.deepcopy(s.events),'result':copy.deepcopy(st['r232']['outcome'])}
def main():
 out=[]
 for seed,sid in zip(PRE['seeds'],PRE['species']):
  db=R/'evidence/db'/f'R232_{sid}_S{seed}.sqlite'
  if db.exists():raise FileExistsError('RUN_ID_USED '+str(db))
  sp=next(x for x in SOURCE['attacks'] if x['id']==sid)
  j.init_db(str(db),'A',seed);st=j.initial('A',seed);st.update(fixture(seed,sp));g=j.sha({'R232_prereg':PREH,'seed':seed,'source_excerpt':SOURCEH})
  con=j.connect(str(db));
  with con:
   for k,v in [('state',j.canonical(st)),('scene',st['scene']),('genesis',g),('head',g)]:con.execute('update meta set value=? where key=?',(v,k))
  con.close()
  j.event_commit(str(db),f'LAB-CMD-R232-{sid}-{seed}','R232_VZ_SOURCE_BASIC_STRIKE',{'prereg':PREH,'source':SOURCEH},fn)
  fin,hd,rev=j.load(str(db));out.append({'species_id':sid,'seed':seed,'commits':rev,'events':len(fin['native_events']),'outcome':fin['r232']['outcome'],'head':hd})
 (R/'evidence/reports/R232_RESULTS.json').write_text(json.dumps({'status':'NEEDS_INDEPENDENT_AUDIT','units':len(out),'new_species_tested':4,'full_fights':0,'official_D_cells':0,'historical_replays':0,'results':out},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
