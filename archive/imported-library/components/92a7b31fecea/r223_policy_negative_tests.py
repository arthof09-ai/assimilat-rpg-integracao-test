"""Negative source-gated no-mutation tests, new ephemeral TEST replicas, not historical replay."""
from pathlib import Path
import sys,copy,json
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'code'),str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import r223_round_reducer as rd
from vlab_effects_v08 import Scene,ActorActionState,cast_source_specified_spell,EffectBlocked,Resistances

def mk(provenance):
 E=rd.old.actor('E');R=rd.old.actor('R');E.standard=1
 return Scene({'E':E,'R':R},seed=22381234,provenance=provenance)

def attempt(sc,policy=None,source=None,damage=61,save=True):
 src=rd.old.SPORES
 return cast_source_specified_spell(sc,'E','R',source=src,state=ActorActionState('E',20,sc.actors['E'].pa,(src.action_id,),standard_available=True,range_confirmed=True,enemy_ids_visible=('R',)),proofs=(rd.E_PROOF,),damage=damage,damage_tag='planta',rd=Resistances(general=0,provenance='R209-TEST'),explicit_save_effect='SAVE-HALF',target_save_exceeds_cd=save,damage_rolls=(5,5,5,5,5,5,5,5,5,6) if damage==61 else None,damage_faces=10 if damage==61 else None,documented_flat_bonus=10 if damage==61 else 0,odd_half_rounding_test_policy=policy,rounding_decision_source=source)

def run():
 out=[]
 for name,scene_status,pol,source in [
  ('NO_POLICY','R223-TEST',None,None),
  ('INVALID_SOURCE','R223-TEST','FLOOR_MASTER_TENTATIVE_TEST','OTHER'),
  ('NON_TEST_PROVENANCE','R223-NONCANON','FLOOR_MASTER_TENTATIVE_TEST','USER_MESTRE_UNCERTAIN_2026-10-21'),
  ('INVALID_POLICY','R223-TEST','CEIL','USER_MESTRE_UNCERTAIN_2026-10-21'),
 ]:
  s=mk(scene_status);snapshot=(s.actors['E'].pa,s.actors['E'].standard,s.actors['R'].hp,len(s.events))
  try:attempt(s,pol,source);raise AssertionError('BAD_POLICY_ACCEPTED:'+name)
  except EffectBlocked as e:
   assert snapshot==(s.actors['E'].pa,s.actors['E'].standard,s.actors['R'].hp,len(s.events)),'MUTATION_IN_REJECTION';out.append({'case':name,'rejected':True,'no_mutation':True,'reason':str(e)})
 # Positive exact test, source gate with odd successful saving throw. Spell consumes 80 PA once.
 s=mk('R223-TEST');b=(s.actors['E'].pa,s.actors['R'].hp)
 result=attempt(s,'FLOOR_MASTER_TENTATIVE_TEST','USER_MESTRE_UNCERTAIN_2026-10-21')
 assert result['raw']==30 and result['effective']==30 and b[0]-s.actors['E'].pa==80 and b[1]-s.actors['R'].hp==30
 out.append({'case':'SUCCESS_ODD_FLOOR','raw':result['raw'],'pa_spent':80,'hp_loss':30,'source_status':'MASTER_TENTATIVE_TEST_ONLY'})
 obj={'status':'PASS_R223_TEST_ONLY_SOURCE_GATED_NO_MUTATION','cases':out}
 (ROOT/'evidence/reports/R223_POLICY_NEGATIVE_PREFLIGHT.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(obj,ensure_ascii=False,indent=2))
if __name__=='__main__':run()
