"""R94 exact-frontier recovery after process timeout: no replay of published events.
Only db with pending=0 and authenticated source sha can continue; any UNKNOWN_EFFECT is HOLD.
"""
import json,sqlite3,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import r94_fixed_order_adapter as a
FROZEN=json.loads((ROOT/'R94_SOURCE_FREEZE.json').read_text())
PR=json.loads((ROOT/'R94_PREREG_FIXED_OPENING.json').read_text())
REPORT=[]
def resume(db,matchup,seed,side):
    a.configure(matchup)
    with sqlite3.connect(db) as conn:
        if conn.execute('SELECT COUNT(*) FROM pending').fetchone()[0]!=0:raise RuntimeError('UNKNOWN_EFFECT_STOP')
        if conn.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise RuntimeError('SQLITE_BAD')
        historic_count=conn.execute("SELECT COUNT(*) FROM events WHERE json_extract(row_json, '$.kind')='TURN_END'").fetchone()[0]
    s,head,rev=a.core.load(db)
    if s['source_gate']['sha']!=a.profile_sha() or s['run_id']!=f'R94R101_{matchup["id"]}_{seed}_{side}':raise RuntimeError('WRONG_RUN')
    if s['phase']!='ACTIVE':raise RuntimeError('NOT_IN_PROGRESS')
    publication=rev;turns=historic_count
    while turns<PR['horizon']:
        s,_,_=a.core.load(db)
        if s['phase']!='ACTIVE':break
        act=s['active'];b='B' if act=='E' else 'E'
        if s['actors'][act]['resource']['standard']==1:
            a.commit(db,'NORMAL_ATTACK',{'actor':act,'target':b,'reaction':'NONE'},a.do_attack)
        elif s['actors'][act]['resource']['standard']!=0:raise RuntimeError('INVALID_SLOT')
        s,_,_=a.core.load(db)
        if s['phase']=='ACTIVE':a.commit(db,'TURN_END',{'actor':s['active']},a.do_end)
        turns+=1
    else:
        s,_,_=a.core.load(db)
        if s['phase']=='ACTIVE':a.commit(db,'CENSOR',{'horizon':PR['horizon']},a.do_censor)
    cp=db.with_suffix('.checkpoint.sqlite')
    if cp.exists():raise RuntimeError('CHECKPOINT_EXISTS_NOT_RETRY')
    with sqlite3.connect(db) as c,sqlite3.connect(cp) as b:c.backup(b)
    assert a.core.load(db)==a.core.load(cp)
    s,_,end=a.core.load(db)
    return {'run_id':s['run_id'],'recovered_from_revision':publication,'continued_new_events':end-publication,'final_revision':end,'phase':s['phase'],'winner':s['winner'],'hp_end':{x:s['actors'][x]['resource']['hp'] for x in ('B','E')}}

def main():
    for m in FROZEN['matchups']:
        a.configure(m)
        folder=ROOT/'fixed_runs'/m['id'];folder.mkdir(parents=True,exist_ok=True)
        for cohort,seeds in PR['seeds'].items():
            for sd in seeds:
                for side in PR['sides']:
                    db=folder/f'R94BENCH_{sd}_{side}.sqlite';cp=db.with_suffix('.checkpoint.sqlite')
                    if cp.exists():continue
                    if db.exists():
                        x=resume(db,m,sd,side);x['recovery']='APPEND_TO_VERIFIED_STATE_ONLY'
                    else:
                        x=a.run(sd,side,folder,PR['horizon']);x['recovery']='NEW_RUN_NO_EXISTING_DB'
                    REPORT.append({'matchup':m['id'],'seed':sd,'side':side,'cohort':cohort,'result':x})
                    print(json.dumps(REPORT[-1],ensure_ascii=False),flush=True)
    (ROOT/'R94_RECOVERY_EXACT_FRONTIER.json').write_text(a.canon(REPORT)+'\n')
if __name__=='__main__':main()
