"""Deterministic synthetic-only invariants, not production certification."""
import copy, json, random, tempfile
from pathlib import Path
from engine_r13 import *
from durable_r14 import *

SEED=20261009
rng=random.Random(SEED)
checks=0
cases=0
for i in range(2500):
    a=make_fixture();ch=make_choices_single()
    raw={k:0 for k in ATTRS}; raw[rng.choice(ATTRS)]+=1;raw[rng.choice(ATTRS)]+=1
    spirit_for=rng.randint(0,6)
    ch['normal_allocations']['3']={k:v for k,v in raw.items() if v}
    ch['spirit_allocations']['3']={'FOR':spirit_for,'CON':6-spirit_for}
    p=plan(a,ch,f'SIM-STRESS-{i}')
    n=p['updates']['NORMAL'];t=p['updates']['TRANSFORM']
    assert sum(n['attrs'].values())-sum(a['NORMAL']['attrs'].values())==2;checks+=1
    assert sum(t['overlay'].values())-sum(a['TRANSFORM']['overlay'].values())==6;checks+=1
    assert n['hp_current']==a['NORMAL']['hp_current'];checks+=1
    assert n['pa_current']==a['NORMAL']['pa_current'];checks+=1
    assert t['hp_bonus_current']==a['TRANSFORM']['hp_bonus_current'];checks+=1
    assert t['pa_bonus_current']==a['TRANSFORM']['pa_bonus_current'];checks+=1
    assert t['attrs']==addattrs(n['attrs'],t['overlay']);checks+=1
    assert '3' in p['updates']['LOCKS']['milestones'];checks+=1
    assert p['updates']['LOCKS']['milestones']['1']==a['LOCKS']['milestones']['1'];checks+=1
    assert n['untouched']==a['NORMAL']['untouched'];checks+=1
    s=make_store(a);j=execute(p,s)
    assert j.state=='COMMITTED' and s.pages==p['updates'];checks+=1
    assert rollback(s,j).state=='ROLLED_BACK_VERIFIED' and s.pages==a;checks+=1
    cases+=1

# Disk scenarios: sample boundary crashes with new processes / persistent readbacks.
boundaries=['BEFORE_PREPARE','AFTER_PREPARE']
for key in ('NORMAL','TRANSFORM','LOCKS'):
    boundaries.extend(['BEFORE_WRITE:'+key,'AFTER_WRITE:'+key,'AFTER_READBACK:'+key])
boundaries.append('AFTER_COMMIT')
disk_cases=0
for i in range(120):
    before=make_fixture();prepared=plan(before,make_choices_single(),f'SIM-DISK-STRESS-{i}')
    boundary=boundaries[i%len(boundaries)]
    with tempfile.TemporaryDirectory() as d:
        c=DurableController(DurableStore(d,before))
        try:c.run(prepared,crash_at=boundary)
        except SimulatedProcessCrash:pass
        restored=DurableController(DurableStore(d))
        result=restored.recover(prepared['event_id'])
        if boundary=='AFTER_COMMIT':
            assert result=='COMMITTED' and restored.store.get_all()==prepared['updates']
        else:
            assert result in ('ROLLED_BACK_VERIFIED','NOT_APPLIED_NO_WAL')
            assert restored.store.get_all()==before
        checks+=2;disk_cases+=1
out={'seed':SEED,'status':'PASS','engine_synthetic_cases':cases,'disk_restart_cases':disk_cases,
     'tested_crash_boundaries':len(boundaries),'assertions':checks,
     'scope':'offline synthetic local; not Notion transaction, Party E2E not tested'}
Path('evidence/STRESS_R14.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(out,ensure_ascii=False))
