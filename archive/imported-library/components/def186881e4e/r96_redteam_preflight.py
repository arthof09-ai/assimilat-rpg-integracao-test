"""Additive adversarial QA in disposable copies; original ledgers remain byte-for-byte unchanged.
Semantics independently checked using R95 pure-stdlib auditor; chain rehash uses stdlib only.
"""
from __future__ import annotations
import copy,hashlib,json,sqlite3,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import r95_fixed_order_cold_auditor as auditor
import r93_team2x1 as team
import r95_fixed_order_adapter as a

def canon(o):return json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(o):return hashlib.sha256(canon(o).encode()).hexdigest()
base=ROOT/'r95_runs'/'R95-GRIFO-INIT-B'/'R95BENCH_495101_B_LEFT.sqlite'
out=ROOT/'r96_redteam';out.mkdir(exist_ok=True)
mutations={
  'HIT_INVERT':lambda attack: attack.update(hit=not attack['hit']),
  'SCORE_PLUS_1':lambda attack: attack.update(score=attack['score']+1),
  'RD_PLUS_4':lambda attack: attack.update(rd=attack['rd']+4),
  'DAMAGE_NET_PLUS_7':lambda attack: attack.update(damage_net_potential=attack['damage_net_potential']+7),
  'HP_RECEIPT_PLUS_3':lambda attack: attack.update(hp_after=attack['hp_after']+3),
  'FAKE_PA_SPENT':lambda attack: attack.update(pa_spent=30),
}
results=[]
source_profile={b:a.FIXTURE['profiles'][a.FIXTURE['matchups'][0][b]] for b in ('B','E')}
for name,mutation in mutations.items():
    fn=out/(name+'.sqlite');shutil.copy2(base,fn)
    with sqlite3.connect(fn) as con:
        con.execute('BEGIN IMMEDIATE')
        rows=con.execute('SELECT seq,row_json FROM events ORDER BY seq').fetchall()
        prev=con.execute("SELECT value FROM meta WHERE key='genesis'").fetchone()[0]
        tampered=False
        for seq,serialized in rows:
            row=json.loads(serialized)
            if row['kind']=='NORMAL_ATTACK' and not tampered:
                mutation(row['detail']['attack']);tampered=True
            row['prev']=prev
            digest=sha(row)
            con.execute('UPDATE events SET prev=?, row_json=?, row_sha=? WHERE seq=?',(prev,canon(row),digest,seq))
            prev=digest
        assert tampered
        con.execute("UPDATE meta SET value=? WHERE key='head'",(prev,))
    # structural verification independent historical native chain (will accept semantic alteration)
    historic_status='NOT_CHECKED'
    try:
        a.core.load(fn);historic_status='STRUCTURAL_PASS'
    except Exception as e:
        historic_status='STRUCTURAL_REJECT_'+str(e)[:120]
    # independent auditor expects genesis path copied from original, no replay is mutated
    shutil.copy2(base.with_suffix('.genesis.json'),fn.with_suffix('.genesis.json'))
    try:
        auditor.audit(fn,source_profile)
        semantic='WRONG_PASS'
    except Exception as e:
        semantic='REJECT_'+type(e).__name__+'_'+str(e)[:120]
    assert historic_status=='STRUCTURAL_PASS' and semantic.startswith('REJECT_'),(name,historic_status,semantic)
    results.append({'mutation':name,'structural':historic_status,'independent_semantic':semantic})

# Pure-preflight negative tests: invalid commands MUST reject before an intent creates an SQLite pending row
s=copy.deepcopy(json.loads((ROOT/'team_runs'/'R93TEAM_493111_F_LEFT.genesis.json').read_text()))
errors=[]
for name,kind,p in [
 ('BAD_INIT_PAYLOAD','INIT',{'action':'NOT_INIT'}),
 ('ATTACK_DURING_INIT','TEAM_TURN',{'actor':'F','target':'V','reaction':'NONE'}),
 ('CENSOR_DURING_INIT','CENSOR',{'horizon':team.PREREG['horizon']}),
 ('UNDEFINED_COMMAND','NOOP',{}),
]:
 original=copy.deepcopy(s)
 try:team.preflight(s,kind,p);status='WRONG_PASS'
 except team.Deny:status='REJECT_PRE_INTENT'
 assert status=='REJECT_PRE_INTENT' and s==original
 errors.append({'test':name,'status':status,'state_unchanged':True})
# R95 rejects wrong horizon before creating a ledger
try:a.run(495999,'B_LEFT',ROOT/'r96_bad_horizon_not_created',max_turns=120);wrong='WRONG_PASS'
except a.Deny:wrong='REJECT_PRE_INTENT'
assert wrong=='REJECT_PRE_INTENT' and not (ROOT/'r96_bad_horizon_not_created').exists()
errors.append({'test':'HORIZON_MISMATCH_BEFORE_CREATION','status':wrong,'state_unchanged':True})
result={'semantic_mutations':results,'negative_preflight':errors,'mutations_rejected':len(results),'preflights_rejected':len(errors),'quarantine':True,'originals_mutated':False,'all_pass':True}
(ROOT/'R96_SEMANTIC_REDTEAM.json').write_text(canon(result)+'\n')
print(canon({'mutations_rejected':len(results),'preflights_rejected':len(errors),'all_pass':True}))
