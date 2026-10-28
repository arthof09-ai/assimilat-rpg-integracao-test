"""Semantic frauds with valid R18 hashes/checkpoints in disposable clones."""
import sys,sqlite3,shutil,json,pathlib,importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1];BASE=ROOT.parents[0]/'work'
for x in [BASE/'runtime/r172',BASE/'runtime/work/fusion_stage12',BASE/'runtime/native']:sys.path.insert(0,str(x))
from vlab_effects_v08 import Combatant
import vlab_r18_interactive as r18
from r172_atomic_counter import write_checkpoint
spec=importlib.util.spec_from_file_location('auditor', ROOT/'code/r194_independent_replay.py');aud=importlib.util.module_from_spec(spec);spec.loader.exec_module(aud)
SOURCE=ROOT/'evidence/R193_LIU_CONCHA_SEED18719301_LI0_BI0_BL8.sqlite'
if not SOURCE.exists():raise RuntimeError('source missing')
BAD={
 'RANK_RD':lambda rows:rows[1]['detail']['attack'].__setitem__('rd_applied',11),
 'IDENTITY':lambda rows:rows[1]['detail'].__setitem__('source_page','https://app.notion.com/p/FAKE'),
 'HIT':lambda rows:rows[1]['detail']['attack'].__setitem__('hit',not rows[1]['detail']['attack']['hit']),
 'PA_RESOURCE':lambda rows:rows[1]['detail']['pa_after'].__setitem__('LIU',67),
 'INITIATIVE':lambda rows:rows[0]['detail']['initiative']['CONCHA'].__setitem__('score',999),
 'SOURCE_GEOMETRY':lambda rows:rows[0]['payload']['geometry'].__setitem__('contact',False),
 'DAMAGE_TYPE':lambda rows:rows[1]['detail']['attack'].__setitem__('type','gelo'),
 'SOURCE_ROLL_TAPE':lambda rows:rows[1]['payload']['tape']['hit'].__setitem__(0,1 if rows[1]['payload']['tape']['hit'][0]!=1 else 2),
 'OVERKILL':lambda rows:rows[-1]['detail']['attack'].__setitem__('overkill',999),
 'EVENT_SEQUENCE':lambda rows:rows[1]['detail']['new_native_events'][0].__setitem__('seq',999)
}
results=[]
for case,mutate in BAD.items():
 dest=ROOT/'negative'/case;dest.mkdir(parents=True,exist_ok=True);clone=dest/SOURCE.name
 shutil.copyfile(SOURCE,clone)
 con=sqlite3.connect(clone)
 raw=list(con.execute('SELECT seq,prev,row_json FROM events ORDER BY seq'));rows=[json.loads(x[2]) for x in raw]
 mutate(rows)
 prev=rows[0]['prev']
 with con:
  for i,row in enumerate(rows):
   row['prev']=prev
   h=aud.sha(row)
   con.execute('UPDATE events SET prev=?,row_json=?,row_sha=? WHERE seq=?',(prev,aud.canonical(row),h,i+1));prev=h
  con.execute('UPDATE meta SET value=? WHERE key="head"',(prev,))
 con.close()
 # Native R18's hash-chain checker must accept the recomputed hashes.
 structural=False
 try:r18.load(str(clone));structural=True
 except Exception as e:results.append({'case':case,'structural_pass':False,'error':str(e)});continue
 write_checkpoint(str(clone))
 try:aud.verify(clone);rejected=False;reason='UNDETECTED'
 except Exception as e:rejected=True;reason=str(e)[:240]
 results.append({'case':case,'structural_pass':structural,'semantic_rejected':rejected,'reason':reason})
result={'status':'PASS' if all(x.get('structural_pass') and x.get('semantic_rejected') for x in results) else 'FAIL','cases':results,'adversarial_count':len(results)}
(ROOT/'evidence/R194_ADVERSARIAL_REPORT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
