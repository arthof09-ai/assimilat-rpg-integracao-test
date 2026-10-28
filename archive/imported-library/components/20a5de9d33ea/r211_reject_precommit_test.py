"""Does not create any historical or new consumed run. Tests rejection before state mutation."""
from pathlib import Path
import sys,json,copy
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
import r211_dynamic_center_native as r211
from vlab_effects_v08 import move_via_verified_path,EffectBlocked
st=r211.core.state_genesis(21110400,r211.TRIO)
st['r211']={'positions_m':copy.deepcopy(r211.PRE['position_start_m'])}
st['actors'][r211.B1]['resource']['position']=str(tuple(st['r211']['positions_m'][r211.B1]))
st['actors'][r211.B1]['resource']['base_speed']=27
st['actors'][r211.B1]['resource']['movement']=1
scene=r211.core.scene(st)
source=r211.MOVE;proofs=(r211.PROOF,)
state=r211.ActorActionState(r211.B1,11,st['actors'][r211.B1]['resource']['pa'],(source.action_id,),geometry_confirmed=True,environment_contract=True)
before=copy.deepcopy(scene.actors[r211.B1].__dict__);eventcount=len(scene.events)
for name,kwargs in [
  ('over_speed',dict(destination='(8,99)',path_evidence='impossible 98m straight',travel_cost=Fraction(98),speed=Fraction(27))),
  ('negative_distance',dict(destination='(8,9)',path_evidence='test',travel_cost=Fraction(-1),speed=Fraction(27))),
  ('missing_path',dict(destination='(8,9)',path_evidence='',travel_cost=Fraction(8),speed=Fraction(27))),
]:
 try:move_via_verified_path(scene,r211.B1,source=source,state=state,proofs=proofs,**kwargs)
 except EffectBlocked:pass
 else:raise AssertionError(name+' passed incorrectly')
 assert before==scene.actors[r211.B1].__dict__ and len(scene.events)==eventcount
bad=copy.deepcopy(st)
try:r211.select(bad,'ILLEGAL_POLICY')
except EffectBlocked:pass
else:raise AssertionError('illegal center selection passed')
assert st==bad
out={'test':'PASS_R211_REJECT_PRECOMMIT_NO_MUTATION','negative_cases':4,'no_db_or_run_id_consumed':True,'production':'HOLD'}
(ROOT/'evidence/R211_NEGATIVE_PREFLIGHT.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
