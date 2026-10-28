"""Deterministic adversarial, simulated only; no Notion interactions."""
from r10_recovery import compare_tables, FakeStore, RecoveryController, media_evidence
import random,json
rng=random.Random(20261009)
tests=0
for idx in range(1000):
    rows=[[f'Cell-{r}-{c}-{idx}' for c in range(3)] for r in range(4)]
    def table(rows,indent):
        return '\n'.join([indent+'<table header-row="true">']+[indent+'<tr>'+''.join('<td>'+cell+'</td>' for cell in row)+'</tr>' for row in rows]+[indent+'</table>'])
    before=table(rows,'')
    assert compare_tables(before,table(rows,'\t'*rng.randint(1,4)))['equal']
    tests+=1
    changed=[row[:] for row in rows];row=rng.randrange(4);col=rng.randrange(3);changed[row][col]+='!'
    assert not compare_tables(before,table(changed,''))['equal']
    tests+=1
    reordered=[row[:] for row in rows];a,b=rng.sample(range(4),2);reordered[a],reordered[b]=reordered[b],reordered[a]
    assert not compare_tables(before,table(reordered,''))['equal']
    tests+=1
    assert media_evidence(source_block_id=str(idx),clone_block_id=str(idx+1000),source_url='s',clone_url='c')['state']=='PENDING'
    tests+=1
for idx in range(300):
    originals={'a':{'life':idx,'alma':idx+1},'b':{'life':idx+2},'c':{'life':idx+3}}
    updates={'a':{'life':idx+100},'b':{'life':idx+200},'c':{'life':idx+300}}
    store=FakeStore(originals);ctrl=RecoveryController(store)
    crash=rng.choice(['BEFORE_PREFLIGHT','AFTER_PREFLIGHT']+[f'{stage}:{p}' for p in updates for stage in ('BEFORE_WRITE','AFTER_WRITE','AFTER_READBACK')]+['AFTER_COMMIT'])
    j=ctrl.run(f'e{idx}',updates,crash_at=crash)
    ctrl.reconcile(j)
    assert store.pages==originals, (idx,j.state,store.pages)
    tests+=1
result={'stress_assertions':tests,'seed':20261009,'status':'PASS','scope':'simulated/offline','production_e2e':'NOT_TESTED'}
open('STRESS_R10.json','w').write(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
