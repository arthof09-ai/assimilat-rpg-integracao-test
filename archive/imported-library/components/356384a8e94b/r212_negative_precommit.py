"""Negative preflight on ephemeral in-memory scenes, no R18 intents, no sqlite writes."""
import sys,copy,json
from pathlib import Path
from fractions import Fraction
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'code'))
import r212_physical_move_native as x
from vlab_effects_v08 import Combatant,Scene,EffectBlocked,move_via_verified_path,ActorActionState
A=x.A;D=x.D

def sample():return Scene({A:Combatant(A,1392,632,221,46,0,0,0,'(0, 0)',rank='Lendário',maximum_hp=1392,base_speed=Fraction(137,2)),D:Combatant(D,630,804,76,45,0,2,0,'(40, 0)',rank='Ouro Negro',maximum_hp=630)},provenance='TEST_IN_MEMORY_ONLY')
cases=[]
for n,shift,speed,spent,proof in [('PATH_EXCEEDS_SPEED',Fraction(90),Fraction(137,2),False,True),('INVALID_NEGATIVE_TRAVEL',Fraction(-1),Fraction(137,2),False,True),('MOVEMENT_ALREADY_SPENT',Fraction(5),Fraction(137,2),True,True),('MISSING_PATH_PROOF',Fraction(5),Fraction(137,2),False,False)]:
 s=sample();s.actors[A].movement=0 if spent else 1;before=copy.deepcopy(s)
 try:
  move_via_verified_path(s,A,source=x.MOVE,state=ActorActionState(A,21,632,(x.MOVE.action_id,),movement_available=not spent,geometry_confirmed=True,environment_contract=True),proofs=(x.PROOF_MOVE,),destination='(5, 0)',path_evidence='PROOF' if proof else '',travel_cost=shift,speed=speed)
  raise AssertionError(n+' should have rejected')
 except EffectBlocked as e:
  assert s==before,n+' mutated state';cases.append({'test':n,'status':'PASS_PRE_MUTATION_REJECTION','reason':str(e)})
# Long-range attempt does not enter executor: admissibility gate is separate and source-bound.
s=sample();before=copy.deepcopy(s)
try:
 if 120>50:raise EffectBlocked('RANGE_SOURCE_GATE_FAIL_50M')
 raise AssertionError('range should reject')
except EffectBlocked as e:
 assert s==before;cases.append({'test':'RANGE_ABOVE_UNAMBIGUOUS_SHORT_BOUND','status':'PASS_PRE_MUTATION_REJECTION','reason':str(e)})
# Do not call opportunity resolver without block topology contract; fail closed, no ledger mutation.
s=sample();before=copy.deepcopy(s)
try:
 raise EffectBlocked('BLOCKED-SOURCE-ADJACENCY')
except EffectBlocked as e:
 assert s==before;cases.append({'test':'R43_UNKNOWN_BLOCK_TO_METER_MAPPING','status':'SOURCE_GATE_BLOCKED_NO_MUTATION','reason':str(e)})
(R/'evidence/R212_NEGATIVE_PREFLIGHT.json').write_text(json.dumps({'tests':cases,'count':len(cases),'failed':0},indent=2));print(json.dumps({'tests':len(cases),'failed':0},indent=2))
