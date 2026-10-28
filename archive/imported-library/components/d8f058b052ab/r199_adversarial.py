"""Forged R199 clones: rewrite hash chain/head, never touch legitimate or historic DBs."""
from __future__ import annotations
import pathlib,sqlite3,shutil,json,sys
ROOT=pathlib.Path(__file__).resolve().parents[3];R199=ROOT/'new/r199'
sys.path.insert(0,str(R199/'code'));sys.path.insert(0,str(ROOT/'work/runtime/work/fusion_stage12'));sys.path.insert(0,str(ROOT/'work/runtime/r172'));sys.path.insert(0,str(ROOT/'work/runtime/native'))
import r199_independent_replay as audit
import vlab_r18_interactive as r18
def write_checkpoint(db):
 hist=r18.history(db)
 body={'format':'R172_EXPORTED_CHECKPOINT_ONLY','db':pathlib.Path(db).name,
       'revision':hist['revision'],'head':hist['head'],'state':hist['state'],
       'events':hist['events'],'official_effects':0}
 dst=pathlib.Path(str(db)+'.checkpoint.json')
 dst.write_text(json.dumps({'body':body,'sha256':audit.sha(body)},indent=2,sort_keys=True,ensure_ascii=False))

DBS=R199/'evidence/db'
FORM=DBS/'R199_ONG_LOBO_19999101_ACTIVATE_FORM_AND_CAST.sqlite'
FORM2=DBS/'R199_ONG_LOBO_19999104_ACTIVATE_FORM_AND_CAST.sqlite'
BEAST=DBS/'R199_LOBO_ANCESTRAL_VS_CAPANGA_19999201_ANCESTRAL_PLUS2_IF_NOT_INCLUDED.sqlite'

def change(form,field,value):
 form[field]=value

def target_row(rows,kind):return next(x for x in rows if x['kind']==kind)
CASES=[
 ('TRANSFORM_PA',FORM,lambda r:target_row(r,'R199_TRANSFORM_ACTIVATE')['detail']['event'].__setitem__('cost',0)),
 ('TRANSFORM_DURATION',FORM,lambda r:target_row(r,'R199_TRANSFORM_ACTIVATE')['detail']['event'].__setitem__('duration_roll',6)),
 ('SPELL_WATER_TYPE',FORM,lambda r:target_row(r,'R199_WATER_WHIP')['detail']['attack'].__setitem__('type','dark')),
 ('SPELL_PA_UNDEBITED',FORM,lambda r:target_row(r,'R199_WATER_WHIP')['detail']['paid'].__setitem__('PA_spent',0)),
 ('INIT_WOLF_SCORE',FORM,lambda r:target_row(r,'R199_INIT')['detail']['results']['LOBO_P1'].__setitem__('result',999)),
 ('BEAST_EXTRA_STR',BEAST,lambda r:target_row(r,'R199_SOURCE_SCOPED_PHYSICAL_ATTACK')['detail'].get('source_passive_overlay',{}).__setitem__('FOR_plus',99)),
 ('BEAST_ATTACK_RAW',BEAST,lambda r:target_row(r,'R199_SOURCE_SCOPED_PHYSICAL_ATTACK')['detail']['attack'].__setitem__('raw',9999)),
 ('TRANSFORM_END_PA',FORM2,lambda r:next(x for x in r if x['kind']=='R199_WATER_WHIP' and x['detail'].get('expiration'))['detail']['expiration']['after'].__setitem__('pa',999)),
]

def clone_case(name,original,mutator):
 dest=R199/'evidence/negative'/name;dest.mkdir(parents=True,exist_ok=True)
 clone=dest/original.name
 if clone.exists():raise RuntimeError('NO_CLONE_REUSE')
 shutil.copyfile(original,clone)
 c=sqlite3.connect(clone)
 try:
  rows=[json.loads(t[0])for t in c.execute('SELECT row_json FROM events ORDER BY seq')]
  mutator(rows)
  head=rows[0]['prev']
  with c:
   for i,row in enumerate(rows,1):
    row['prev']=head;h=audit.sha(row)
    c.execute('UPDATE events SET prev=?,row_json=?,row_sha=? WHERE seq=?',(head,audit.canon(row),h,i))
    head=h
   c.execute('UPDATE meta SET value=? WHERE key="head"',(head,))
 finally:c.close()
 # Rewritten hash chain is self-consistent to original R18 structural verify.
 r18.load(str(clone));write_checkpoint(str(clone))
 try:audit.semantic(clone)
 except Exception as exc:return {'case':name,'R18_structural':'PASS_REHASHED','R199_semantic':'REJECTED','reason':str(exc)[:220], 'clone':str(clone.relative_to(ROOT))}
 return {'case':name,'R18_structural':'PASS_REHASHED','R199_semantic':'UNDETECTED','clone':str(clone.relative_to(ROOT))}

def main():
 result=[clone_case(name+"_V2",orig,fn) for name,orig,fn in CASES];success=all(x['R199_semantic']=='REJECTED' for x in result)
 out={'status':'PASS_R199_FORGERY_REJECTED' if success else 'FAIL_ADVERSARIAL','tests':result,'total':len(result),
  'originals_unchanged':True,'auditor_independence':'SEPARATE_LOCAL_CODE_NOT_EXTERNAL_AUTHORITY'}
 (R199/'evidence/R199_ADVERSARIAL_REPORT.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
 print(json.dumps({'status':out['status'],'rejected':sum(x['R199_semantic']=='REJECTED' for x in result),'total':len(result)}))
 if not success:raise AssertionError(result)
if __name__=='__main__':main()
