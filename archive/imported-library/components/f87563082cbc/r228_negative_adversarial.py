"""Source/geometry in-memory reject plus hash-rebuilt immutable clone attacks."""
from pathlib import Path
import json,hashlib,sqlite3,shutil,copy,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'code'),str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import r228_flecha_native as sim
import vlab_effects_v08 as effects
from r228_independent_sql_audit import audit_one,sha
from dataclasses import asdict
from fractions import Fraction
p=ROOT/'sources/R228_PREREG_BEFORE_EXEC.json';ph=hashlib.sha256(p.read_bytes()).hexdigest()
sh=hashlib.sha256((ROOT/'sources/R228_ISKIEL_FROZEN_MECHANICAL_SOURCE.json').read_bytes()).hexdigest()
# Conditional TEST: a legal-source movement exceeding slowed speed must fail before any publication.
v=effects.Combatant('V',708,324,83,0,0,0,0,'(0,0)',rank='Ouro Negro',maximum_hp=734,base_speed='12',timed_source_speed_penalty_m=6)
scene=effects.Scene({'V':v},seed=22879999,provenance='R228-NEGATIVE-TEST')
state=effects.ActorActionState('V',20,324,(sim.MOVE.action_id,),movement_available=True,geometry_confirmed=True,environment_contract=True)
orig=asdict(v);events=copy.deepcopy(scene.events)
try:
 effects.move_via_verified_path(scene,'V',source=sim.MOVE,state=state,proofs=(sim.MPROOF,),destination='(7,0)',path_evidence='R228-TEST-OPEN-LINE',travel_cost=Fraction(7),speed=Fraction(7))
except effects.EffectBlocked as e:
 assert asdict(v)==orig and scene.events==events
 rejection=str(e)
else:raise AssertionError('OVERSPEED_ACCEPTED')
base=ROOT/'evidence/db/R228_HIT_S22871003.sqlite';adv=ROOT/'evidence/adversarial';adv.mkdir(exist_ok=True)
attacks=[]
mods=[('FREE_PA',lambda st:st['actors']['I'].__setitem__('pa',484)),('POSITION_MAGIC',lambda st:st['actors']['V'].__setitem__('position','(15,0)')),
('SLOW_UNEXPIRED',lambda st:st['actors']['V'].__setitem__('timed_source_speed_penalty_m',6)),('WORLD_CANON_LAUNDERED',lambda st:st['r228'].__setitem__('world_canon',True))]
for name,mutation in mods:
 clone=adv/f'R228_FORGED_HASH_{name}.sqlite'
 if clone.exists():raise FileExistsError('NO_REUSE_CLONES')
 shutil.copy2(base,clone)
 c=sqlite3.connect(clone);st=json.loads(dict(c.execute('select key,value from meta'))['state']);mutation(st)
 row=json.loads(c.execute('select row_json from events where seq=3').fetchone()[0]);row['after_sha']=sha(st)
 with c:
  c.execute('update meta set value=? where key="state"',(json.dumps(st,sort_keys=True,separators=(',',':'),ensure_ascii=False),))
  c.execute('update events set row_json=?,row_sha=?,after_sha=? where seq=3',(json.dumps(row,sort_keys=True,separators=(',',':'),ensure_ascii=False),sha(row),row['after_sha']))
  c.execute('update meta set value=? where key="head"',(sha(row),))
 c.close()
 try:audit_one(clone,'HIT',22871003,[3,2,4],ph,sh)
 except AssertionError as exc:attacks.append({'case':name,'reject':str(exc)})
 else:raise AssertionError('MALICIOUS_STATE_ACCEPTED:'+name)
result={'status':'PASS_R228_NEGATIVE_AND_4_ADVERSARIAL','excess_speed_rejected':rejection,'in_memory_state_mutated':False,'adversarial':attacks}
(ROOT/'evidence/reports/R228_NEGATIVE_AND_ADVERSARIAL.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
