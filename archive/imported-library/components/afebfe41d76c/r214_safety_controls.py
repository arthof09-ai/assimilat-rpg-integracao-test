"""R214 NEW isolated safety probes; commits never touch historical data. Includes fault injection test."""
import sys,json,copy,subprocess,hashlib,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
import r214_native_causal_bilateral as m

def blocked(label,fn,obj=None):
 before=None
 if obj is not None:before=json.dumps({'events':obj.events,'actors':{k:vars(a) for k,a in obj.actors.items()}},sort_keys=True,default=str)
 try:fn()
 except Exception as e:
  if obj is not None:
   after=json.dumps({'events':obj.events,'actors':{k:vars(a) for k,a in obj.actors.items()}},sort_keys=True,default=str)
   assert before==after,label+'_MUTATED'
  return {'case':label,'status':'BLOCKED_NO_MUTATION','reason':str(e)[:180]}
 raise AssertionError('UNBLOCKED '+label)

def checks():
 s=m.Scene({'F':m.Combatant('F',479,None,123,0,0,0,0,'(1.5, 0)',rank='Ouro Negro',maximum_hp=479),
            'R':m.Combatant('R',806,None,93,0,0,0,0,'(0, 0)',rank='Ouro Negro',maximum_hp=806)},provenance='R214-NEGATIVE-TEST')
 c=m.aoo_context(s,('F','F'),'R')
 out=[]
 out.append(blocked('NO_TRIGGER',lambda:m.declare_opportunity_reaction(s,'F','R',source=m.AOO['F'],state=m.ActorActionState('F',20,None,(m.AOO['F'].action_id,),reaction_available=True,reaction_trigger_observed=None,range_confirmed=True,enemy_ids_visible=('R',)),proofs=(m.PROOFS['F'],),fixture_adjacency_id='R44-TEST'),s))
 s.actors['F'].reaction=0
 out.append(blocked('NO_REACTION',lambda:m.declare_opportunity_reaction(s,'F','R',source=m.AOO['F'],state=c,proofs=(m.PROOFS['F'],),fixture_adjacency_id='R44-TEST'),s))
 s.actors['F'].reaction=1
 out.append(blocked('WRONG_SOURCE',lambda:m.declare_opportunity_reaction(s,'F','R',source=m.NORM['R'],state=c,proofs=(m.PROOFS['F'],),fixture_adjacency_id='R44-TEST'),s))
 intent=m.declare_opportunity_reaction(s,'F','R',source=m.AOO['F'],state=c,proofs=(m.PROOFS['F'],),fixture_adjacency_id='R44-TEST')
 out.append(blocked('ALREADY_RESERVED',lambda:m.declare_opportunity_reaction(s,'F','R',source=m.AOO['F'],state=c,proofs=(m.PROOFS['F'],),fixture_adjacency_id='R44-TEST'),s))
 out.append(blocked('REQUIRES_INTENT',lambda:m.apply_weapon_attack(s,'F','R',source=m.AOO['F'],state=c,proofs=(m.PROOFS['F'],),roll_score=130,damage=75,damage_tag='cortante',rd=m.Resistances(general=30,provenance='TEST'),attack_origin='OPPORTUNITY',advantage_levels=1),s))
 # Native AoO preflight must demand Advantage after reservation.
 out.append(blocked('ADVANTAGE_REQUIRED',lambda:m.apply_weapon_attack(s,'F','R',source=m.AOO['F'],state=c,proofs=(m.PROOFS['F'],),roll_score=130,damage=75,damage_tag='cortante',rd=m.Resistances(general=30,provenance='TEST'),attack_origin='OPPORTUNITY',opportunity_intent_seq=intent['seq'],advantage_levels=0),s))
 # Existing committed lab command cannot be played a second time.
 db=ROOT/'evidence/db/R214_AOO_DOUBLE_S21441001.sqlite';bef=m.j.load(db)
 out.append(blocked('R18_DUPLICATE',lambda:m.j.event_commit(str(db),'LAB-CMD-R214-DOUBLE-21441001-1','R214_DUP',{},lambda *args:None)))
 aft=m.j.load(db);assert (bef[1],bef[2])==(aft[1],aft[2])
 # R18 crash following durable intent: only pending lock exists. No campaign effects, no auto-retry.
 fault=ROOT/'evidence/db/R214_FAULT_AFTER_INTENT_S21449001.sqlite'
 m.j.init_db(str(fault),'A',21449001)
 # independent sub-process crashes on R18 failpoint; runner MUST not execute.
 child='''import sys\nsys.path.insert(0,sys.argv[2]);import vlab_r18_interactive as j\nj.event_commit(sys.argv[1],'LAB-CMD-R214-FAULT-21449001','FAULT_AFTER_INTENT',{'scope':'R214_TEST'},lambda *a: (_ for _ in ()).throw(RuntimeError('RUNNER_SHOULD_NOT_EXECUTE')),failpoint='AFTER_INTENT')'''
 res=subprocess.run([sys.executable,'-c',child,str(fault),str(ROOT/'runtime/fusion_stage12')],capture_output=True)
 assert res.returncode==78,res.stderr.decode()[:800]
 cc=sqlite3.connect('file:'+str(fault)+'?mode=ro',uri=True)
 try:
  md=dict(cc.execute('SELECT key,value FROM meta'));np=cc.execute('SELECT COUNT(*) FROM pending').fetchone()[0];ne=cc.execute('SELECT COUNT(*) FROM events').fetchone()[0]
  assert np==1 and ne==0 and md['revision']=='0' and md['head']==md['genesis']
 finally:cc.close()
 out.append({'case':'R18_AFTER_INTENT_FAULT','status':'PENDING_UNKNOWN_EFFECT_NO_PUBLISHED_CHANGE','pending':np,'commits':ne,'child_exit':res.returncode})
 # No retry: the real gate must refuse load pending.
 out.append(blocked('PENDING_NO_AUTORETRY',lambda:m.j.load(str(fault))))
 result={'status':'PASS_R214_SAFETY_CONTROLS_EXPLICIT_UNKNOWN_PENDING','probes':out,'existing_history_changed':False}
 (ROOT/'evidence/R214_SAFETY_CONTROLS.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
 print(json.dumps({'status':result['status'],'probes':len(out),'names':[x['case'] for x in out]},indent=2))
if __name__=='__main__':checks()
