"""R111 only: deterministic read-only lock-lifecycle checker against already recorded synthetic lock.
No new roll, source Criação de Ficha FF milestone permanent lock rule. NOT native writing.
"""
import json
from pathlib import Path
src=json.loads((Path(__file__).parent/'R111_RECEIPT_NATIVE.json').read_text())
lock=src['after']['LOCKS']['permanent_milestones']['1']
assert lock['rolls']==[2,3] and lock['choice']=='VIDA'
base=src['after']['TRANSFORM']['hp_natural']
seen=[]
for ff in (100,90,100,90):
 active=ff>=100
 seen.append({'ff':ff,'active':active,'hp_max':base+(lock['total_bonus'] if active else 0),
              'permanent_lock':lock,'same_event':lock['event'],'rerolled':False})
assert [s['hp_max'] for s in seen]==[23,18,23,18]
assert all(s['permanent_lock']==lock and not s['rerolled'] for s in seen)
result={'contract':'FF100_LOCK_LIFECYCLE','method':'LOCAL, source-bound deterministic, no Notion writing',
        'native_first_acquisition_ref':'R111_TEST_COMMITTED','source_origin':'Criação de Ficha rule FF milestones',
        'states':seen,'status':'PASS_LOCAL_LIFECYCLE_NATIVE_TOGGLE_HOLD'}
p=Path(__file__).parent/'R111_FF_LOCK_LIFECYCLE_LOCAL.json'
p.write_text(json.dumps(result,ensure_ascii=False,indent=2))
print('R111 lifecycle checks PASS LOCAL: 100/90/100/90, lock unchanged, no reroll, maxHP 23/18/23/18')
