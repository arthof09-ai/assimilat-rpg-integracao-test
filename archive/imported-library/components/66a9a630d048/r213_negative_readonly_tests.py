"""R213 stateless preflight negative and independent forgery controls; no writes to accepted DBs."""
from pathlib import Path
import sys,hashlib,json,sqlite3,tempfile,shutil,copy
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import vlab_r18_interactive as j
sys.modules.pop('vlab_effects_v08',None);sys.path.insert(0,str(ROOT/'runtime/native'))
from vlab_effects_v08 import Combatant,Scene,EffectBlocked,ActorActionState,FrozenRuleEvidence,AbilitySource,move_via_verified_path,apply_weapon_attack,Resistances
from r213_independent_sql_audit import audit

def neg(name,func):
 try:func()
 except (EffectBlocked,AssertionError) as e:return {'name':name,'status':'PASS_REJECTED','reason':str(e)}
 else:raise AssertionError('FAIL_NOT_REJECTED '+name)

def tests():
 evidence=FrozenRuleEvidence('3ebc2b32-4ede-81f1-be4b-e8804ac113c0','TEST-FROZEN',hashlib.sha256(b'test').hexdigest(),'2026-10-20','R213-NEG')
 x=Combatant('F',479,None,123,24,0,10,10,'(1.5, 0.0)',maximum_hp=479,base_speed='3')
 y=Combatant('R',806,None,93,57,0,12,12,'(0.0, 0.0)',maximum_hp=806,base_speed='3')
 s=Scene({'F':x,'R':y})
 aoo=AbilitySource('N-AOO','attack','REACTION',evidence.source_page_id,evidence.rule_id,'RULE-DERIVED',reaction_trigger='EXIT_ADJACENT',target_scope='ENEMY',effect_adapter_ready=True,effect_adapter_id='TEST-NATIVE')
 ctx=ActorActionState('F',20,None,('N-AOO',),reaction_trigger_observed='EXIT_ADJACENT',enemy_ids_visible=('R',))
 baseline=(x.hp,x.reaction,y.hp,y.position,len(s.events))
 results=[neg('NO_ADVANTAGE_AOO',lambda:apply_weapon_attack(s,'F','R',source=aoo,state=ctx,proofs=(evidence,),roll_score=110,damage=60,damage_tag='cortante',rd=Resistances(general=30),advantage_levels=0,attack_origin='OPPORTUNITY'))]
 results.append(neg('MISSING_SOURCE_PROOF',lambda:apply_weapon_attack(s,'F','R',source=aoo,state=ctx,proofs=(),roll_score=110,damage=60,damage_tag='cortante',rd=Resistances(general=30),advantage_levels=1,attack_origin='OPPORTUNITY')))
 move=AbilitySource('N-MOVE','move','MOVEMENT',evidence.source_page_id,evidence.rule_id,'RULE-DERIVED',target_scope='POSITION',effect_adapter_ready=True,effect_adapter_id='TEST-NATIVE')
 mc=ActorActionState('R',20,None,('N-MOVE',),movement_available=True,geometry_confirmed=True,environment_contract=True)
 results.append(neg('INSUFFICIENT_SPEED',lambda:move_via_verified_path(s,'R',source=move,state=mc,proofs=(evidence,),destination='(5, 0)',path_evidence='LAB-OPEN-ROUTE',travel_cost=__import__('fractions').Fraction(5),speed=__import__('fractions').Fraction(3))))
 assert (x.hp,x.reaction,y.hp,y.position,len(s.events))==baseline
 results.append({'name':'NO_MUTATION_ON_REJECT','status':'PASS','before':str(baseline),'after':str((x.hp,x.reaction,y.hp,y.position,len(s.events)))})
 source=next((ROOT/'evidence/db').glob('R213_AOO_DOUBLE_S21331002.sqlite'))
 with tempfile.TemporaryDirectory() as tmp:
  cloned=Path(tmp)/source.name; shutil.copy2(source,cloned)
  c=sqlite3.connect(cloned); m=c.execute('select value from meta where key="state"').fetchone()[0]; state=json.loads(m);state['actors']['R']['resource']['hp']+=1
  c.execute('update meta set value=? where key="state"',(json.dumps(state),));c.commit();c.close()
  results.append(neg('CORRUPTED_SQLITE_READONLY_AUDITOR',lambda:audit(cloned)))
 (ROOT/'evidence/R213_NEGATIVE_RESULTS.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
 print(json.dumps({'total':len(results),'all_pass':all(x['status'].startswith('PASS') for x in results)},indent=2))
if __name__=='__main__':tests()
