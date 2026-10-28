"""Semantic forgery demonstration using throwaway R198 SQLite clones with recomputed R18 row/head hashes."""
import pathlib,sys,sqlite3,json,shutil,importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
sys.path.insert(0,str(ROOT.parent/'work/runtime/work/fusion_stage12'))
sys.path.insert(0,str(ROOT.parent/'work/runtime/r172'))
sys.path.insert(0,str(ROOT.parent/'work/runtime/native'))
import vlab_effects_v08
import vlab_r18_interactive as r18
import r198_independent_replay as auditor
import r198_magic_independent_audit as magic
from r172_atomic_counter import write_checkpoint
R=ROOT/'evidence/db/R198_CAPANGA_P3_VS_LOBO_P1_19821001.sqlite'
M=ROOT/'evidence/magic_db/R198_MAGIC_ONG_VS_LOBO_19832001_CAST_WHIP.sqlite'
assert R.exists() and M.exists()

def migrate(db,case,mutator,is_magic=False):
 dst=ROOT/'negative'/case;dst.mkdir(parents=True,exist_ok=True)
 clone=dst/db.name;shutil.copy2(db,clone)
 conn=sqlite3.connect(clone)
 try:
  rows=[json.loads(q[0]) for q in conn.execute('SELECT row_json FROM events ORDER BY seq')]
  mutator(rows)
  head=rows[0]['prev']
  with conn:
   for seq,row in enumerate(rows,1):
    row['prev']=head;rowsha=auditor.sha(row)
    conn.execute('UPDATE events SET prev=?,row_json=?,row_sha=? WHERE seq=?',(head,auditor.canonical(row),rowsha,seq))
    head=rowsha
   conn.execute('UPDATE meta SET value=? WHERE key="head"',(head,))
 finally:conn.close()
 # A structural R18 check must still pass: proving semantic checks are additional.
 r18.load(str(clone))
 write_checkpoint(str(clone))
 try:(magic.audit if is_magic else auditor.audit)(clone)
 except Exception as e:return {'case':case,'structural':'PASS_HASHES_REBUILT','semantic':'REJECTED','reason':str(e)[:220],'clone':str(clone.relative_to(ROOT))}
 return {'case':case,'structural':'PASS_HASHES_REBUILT','semantic':'UNDETECTED','clone':str(clone.relative_to(ROOT))}

def change_attack(rows,field,val):rows[1]['detail']['attack'][field]=val
CASES=[
 ('SOURCE_IDENTITY',R,lambda a:a[1]['detail'].__setitem__('source_page','https://app.notion.com/p/FAKE'),False),
 ('ATTACK_SCORE',R,lambda a:change_attack(a,'roll_score',9999),False),
 ('RD_MODIFIED',R,lambda a:change_attack(a,'rd_applied',999),False),
 ('INIT_RESULT',R,lambda a:a[0]['detail']['results']['CAPANGA_P3'].__setitem__('result',9999),False),
 ('CRITICAL_STATUS',R,lambda a:change_attack(a,'critical','POSITIVE'),False),
 ('MAGIC_PA_DEBIT',M,lambda a:next(x for x in a if x['kind']=='SOURCE_SPELL_WHIP_WITH_PA')['detail']['PA_debit_event'].__setitem__('PA_spent',0),True),
 ('MAGIC_TAG',M,lambda a:next(x for x in a if x['kind']=='SOURCE_SPELL_WHIP_WITH_PA')['detail']['attack'].__setitem__('type','raio'),True)
]
result=[migrate(p,name,fn,magic_flag) for name,p,fn,magic_flag in CASES]
report={'status':'PASS_REBUILT_HASH_FORGERY_REJECTED' if all(x['semantic']=='REJECTED' for x in result) else 'FAIL',
 'cases':result,'count':len(result),'warning':'local separate-code audits, not external formal QA; original banks unchanged'}
(ROOT/'evidence/R198_ADVERSARIAL_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
