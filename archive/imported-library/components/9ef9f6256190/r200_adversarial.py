"""Tamper R200 clone DBs, reconstruct structural hashes, demand semantic detection.
Never modify source banks. No audit credit beyond 4 independent scenarios.
"""
from __future__ import annotations
import json,sqlite3,shutil,pathlib,hashlib
from r200_read_only_audit import audit_one,sha
ROOT=pathlib.Path(__file__).resolve().parents[1]
SRC=sorted((ROOT/'evidence/db').glob('*COM_MAGIA_ITEM_PROXY_UNRANKED_TEST.sqlite'))[0]
DEST=ROOT/'evidence/adversarial';DEST.mkdir(parents=True,exist_ok=True)
def recalc(c):
    genesis=c.execute('SELECT value FROM meta WHERE key="genesis"').fetchone()[0]
    rows=c.execute('SELECT seq,row_json,after_sha FROM events ORDER BY seq').fetchall()
    head=genesis
    for seq,v,_ in rows:
        row=json.loads(v);row['prev']=head;head=sha(row)
        c.execute('UPDATE events SET prev=?,row_json=?,row_sha=? WHERE seq=?',(row['prev'],json.dumps(row,ensure_ascii=False,separators=(',',':'),sort_keys=True),head,seq))
    c.execute('UPDATE meta SET value=? WHERE key="head"',(head,))

def attack_tamper(c,change):
    seq,v=c.execute("SELECT seq,row_json FROM events WHERE seq>1 ORDER BY seq LIMIT 1").fetchone()
    row=json.loads(v)
    assert 'attack' in row['detail']
    e=row['detail']['attack']
    if change=='score':e['roll_score']+=23
    elif change=='damage':e['net']+=42
    elif change=='rd':e['rd_applied']+=10
    c.execute('UPDATE events SET row_json=? WHERE seq=?',(json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':')),seq))

def change_rank(c):
    state=json.loads(c.execute('SELECT value FROM meta WHERE key="state"').fetchone()[0]);state['ring']['source_rank']='BRONZE_FAKE'
    c.execute('UPDATE meta SET value=? WHERE key="state"',(json.dumps(state,ensure_ascii=False,sort_keys=True,separators=(',',':')),))
    seq,v=c.execute('SELECT seq,row_json FROM events ORDER BY seq DESC LIMIT 1').fetchone()
    row=json.loads(v);newsha=sha(state);row['after_sha']=newsha
    c.execute('UPDATE events SET after_sha=?,row_json=? WHERE seq=?',(newsha,json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':')),seq))

results=[]
for kind in ['score','damage','rd','rank']:
    p=DEST/('R200_FORGERY_'+kind+'.sqlite');shutil.copy2(SRC,p)
    c=sqlite3.connect(p)
    try:
        with c:
            if kind=='rank':change_rank(c)
            else:attack_tamper(c,kind)
            recalc(c)
    finally:c.close()
    try:audit_one(p)
    except AssertionError as e:results.append({'forgery':kind,'status':'REJECTED','reason':str(e),'hashes_rebuilt':True})
    else:raise RuntimeError('FORGERY_NOT_REJECTED_'+kind)
report={'result':'PASS_R200_SEMANTIC_FORGERY_REJECTION','total':len(results),'rejected':len(results),'clones':results,'source_db':SRC.name,'original_source_unchanged':True}
(DEST/'R200_ADVERSARIAL.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
