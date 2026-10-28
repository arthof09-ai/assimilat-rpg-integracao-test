"""Source-scoped v0.8.1 exhaustive ordered 3d6 critical tape stress. NO official rules modified."""
import itertools,json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'code'),str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import r234_source_complete_beast_battle as b
from vlab_effects_v08 import Scene,ActorActionState,Resistances,begin_source_turn,apply_weapon_attack,EffectBlocked
from fractions import Fraction
PBYTES=(ROOT/'sources/R242_PREREG.json').read_bytes();P=json.loads(PBYTES);PH=hashlib.sha256(PBYTES).hexdigest()
ATTEMPT=(1,1,1,1,1,1);DMG=(1,)*20

def perform(tape,rd):
 cc=b.load_actor(b.c_actor('C'));gg=b.load_actor(b.c_actor('G'))
 cc.position='(0,0)';gg.position='(1,0)'
 scene=Scene({'C':cc,'G':gg},seed=24200000,provenance='R242_CRIT_SEQUENTIAL_GATE_PRECREATE_TEST')
 begin_source_turn(scene,'C')
 before=(cc.hp,cc.pa,cc.standard,cc.position,gg.hp,gg.pa,gg.standard,len(scene.events))
 try:
  ev=apply_weapon_attack(scene,'C','G',source=b.ATK['C'],state=ActorActionState('C',23,cc.pa,(b.ATK['C'].action_id,),standard_available=True,range_confirmed=True,enemy_ids_visible=('G',)),proofs=(b.PF['C'],),
   roll_score=140,damage=20,damage_tag=b.BE['C']['damage_type'],rd=Resistances(general=rd,provenance='R242_LAB_RD_FACTORIAL'),
   damage_dice_groups=((20,10),),damage_roll_groups=(DMG,),damage_fixed_bonus=0,
   critical_sequence=tape,attack_roll_attempts=(ATTEMPT,),attack_bonus=134,lab_negative_critical_policy=False,final_effort=False)
  return {'tape':tape,'rd':rd,'status':'ADMITTED','critical':ev['critical'],'hit':ev['hit'],'raw':ev['raw'],'rd_applied':ev['rd_applied'],'hp_loss_actual':ev['hp_loss_actual'],
   'attacker_standard_after':cc.standard,'target_hp_after':gg.hp,'events_after':len(scene.events)}
 except EffectBlocked as e:
  after=(cc.hp,cc.pa,cc.standard,cc.position,gg.hp,gg.pa,gg.standard,len(scene.events))
  return {'tape':tape,'rd':rd,'status':'REJECTED','reason':str(e),'pre_effect_unchanged':before==after,'events_after':len(scene.events)}

def run():
 out=[]
 for k in (75,1000):
  for tape in itertools.product(range(1,7),repeat=3):out.append(perform(tape,k))
 # Unambiguous special positive critically hits even on missed score, RD may fully absorb.
 lab_overlays=[]
 # Provenance limitation: negative critical LAB-only effect remains separate and not promoted.
 assert len(out)==432
 counts={str(k):{'rejected':0,'positive':0,'miss':0,'hit':0,'hp_total':0} for k in (75,1000)}
 for x in out:
  q=counts[str(x['rd'])]
  if x['status']=='REJECTED':q['rejected']+=1;assert x['pre_effect_unchanged']
  else:q['hit']+=int(x['hit']);q['positive']+=int(x['critical']=='POSITIVE');q['miss']+=int(not x['hit']);q['hp_total']+=x['hp_loss_actual']
 for k in ('75','1000'):
  assert counts[k]['rejected']==2 and counts[k]['positive']==2 and counts[k]['miss']==212 and counts[k]['hit']==2
 assert counts['75']['hp_total']==2*145
 assert counts['1000']['hp_total']==0
 report={'status':'RUN_EXECUTED_NOT_INDEPENDENT_AUDITED','prereg_sha':PH,'source_beast_sha':b.SH,
  'native_adapter_version':'COMBAT-EFFECT-ADAPTER-PARTIAL-v0.8+R126-POSITION-PA-REACTION-CONTROLLED',
  'ordered_triples_per_rd':216,'rd_factors':2,'total_probes':len(out),'counts':counts,'official_cells':0,'terminal_contracts':0,'source_status':'PRECREATE-NONP4','details':out}
 (ROOT/'reports/R242_RUN_RAW.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='details'},ensure_ascii=False,indent=2))
if __name__=='__main__':run()
