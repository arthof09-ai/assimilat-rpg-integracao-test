"""Fault tests: durable UNKNOWN_EFFECT HOLD and commit readback after crash."""
import json,sys,hashlib,sqlite3,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import r112_native_battle as bridge
out=ROOT/'r115_faults';out.mkdir(exist_ok=True)
allcases=[]
for mode,seed in [('AFTER_INTENT',931001),('AFTER_COMMIT',931002)]:
    db=out/f'R115_FAULT_{mode}_{seed}.sqlite'
    bridge.init_db(db,'G_FULL',seed,'B_LEFT')
    bridge.commit(db,'TURN_START',{'actor':'B'})
    pre,head,rev=bridge.core.load(db)
    result=subprocess.run([sys.executable,str(ROOT/'r115_fault_worker.py'),str(db),mode],check=False,timeout=15)
    assert result.returncode==({'AFTER_INTENT':78,'AFTER_COMMIT':77}[mode])
    with sqlite3.connect(db) as c:
        meta=dict(c.execute('select key,value from meta'))
        n=c.execute('select count(*) from events').fetchone()[0]
        pending=c.execute('select count(*) from pending').fetchone()[0]
        p_hp=json.loads(meta['state'])['actors']['E']['resource']['hp']
    if mode=='AFTER_INTENT':
        assert (n,pending,p_hp,meta['head'])==(1,1,523,head)
        try:bridge.core.load(db)
        except bridge.core.LabHold as e:assert 'UNKNOWN_EFFECT' in str(e)
        else:raise AssertionError('PENDING_NOT_BLOCKED')
        status='UNKNOWN_EFFECT_HOLD_NO_RETRY_OR_CLAIM'
    else:
        assert (n,pending,p_hp)==(2,0,258)
        r,h,count=bridge.core.load(db)
        assert count==2 and r['actors']['B']['resource']['standard']==0
        with sqlite3.connect(db) as c:
            row=json.loads(c.execute('select row_json from events where seq=2').fetchone()[0])
        a=row['detail']['native_action'];assert (a['critical_max_bonus'],a['raw'],a['net'],a['after_hp'])==(200,300,265,258)
        status='COMMIT_READBACK_PASS_CRASH_AFTER_COMMIT_NO_RETRY'
    allcases.append({'mode':mode,'returncode':result.returncode,'seed':seed,'sqlite':db.name,'events':n,'pending':pending,'E_hp':p_hp,'status':status,'head':meta['head']})
report={'status':'PASS','crashes':2,'pending_held':1,'committed_readback':1,'results':allcases,'production_effects':0,'terminal_contracts':0}
(ROOT/'R115_FAULT_RECOVERY.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,indent=2))
