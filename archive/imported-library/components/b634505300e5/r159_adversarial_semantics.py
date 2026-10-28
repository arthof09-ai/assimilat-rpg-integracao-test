"""Immutable originals; malicious copies have entire hash chain rehashed.
Independent cold semantic auditors must reject even if SQLite hash chain remains valid.
"""
import sqlite3,json,hashlib,shutil
from pathlib import Path
from r159_cold_tactical_auditor import replay,sha,can
ROOT=Path(__file__).resolve().parent;Q=ROOT/'quarantined';Q.mkdir(exist_ok=True)
CASES=[('R157_TACTIC_BASIC_DEV_S997617','SPELL','PA_spent',79,'SPELL_PA_79_UNDERPAY'),
       ('R158_NEGATIVE_CRITICAL_TACTIC_DEV_S997946','STRIKE','net',1,'CRITICAL_FAIL_GHOST_DAMAGE')]
results=[]
for name,kind,field,value,suffix in CASES:
 src=ROOT/'runs'/(name+'.sqlite');dst=Q/(name+'_'+suffix+'_REHASHED.sqlite')
 if dst.exists():raise ValueError('NO_REPEAT_MUTANT')
 shutil.copy2(src,dst)
 with sqlite3.connect(dst) as c:
  rows=[(a,json.loads(b)) for a,b in c.execute('select seq,row_json from events order by seq')]
  genesis=dict(c.execute('select key,value from meta'))['genesis'];prev=genesis;done=False
  for seq,row in rows:
   if not done and row['kind']==kind:
    row['detail']['native_actions'][0][field]=value;done=True
   row['prev']=prev;digest=sha(row)
   c.execute('update events set prev=?,row_json=?,row_sha=? where seq=?',(prev,can(row),digest,seq))
   prev=digest
  assert done
  c.execute('update meta set value=? where key="head"',(prev,))
 shutil.copy2(src.with_suffix('.genesis.json'),dst.with_suffix('.genesis.json'))
 with sqlite3.connect(dst) as c:
  meta=dict(c.execute('select key,value from meta'));rows=[(i,json.loads(x),r) for i,x,r in c.execute('select seq,row_json,row_sha from events order by seq')]
  p=meta['genesis']
  for i,row,r in rows:assert row['prev']==p and sha(row)==r;p=r
  assert p==meta['head']
 try:replay(dst);rejected=False;message='INDEPENDENT_AUDITOR_ACCEPTED_BAD'
 except Exception as e:rejected=True;message=type(e).__name__+':'+str(e)
 results.append({'mutation':suffix,'source_db':name,'independent_semantic_rejected':rejected,'hash_chain_valid':True,'reason':message})
assert len(results)==2 and all(x['independent_semantic_rejected'] for x in results)
(ROOT/'R159_REDTEAM_RESULTS.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
