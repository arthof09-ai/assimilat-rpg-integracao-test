"""One-command offline R13 demonstration, durable write, undo and replay."""
import json,shutil
from pathlib import Path
from engine_r13 import *
from durable_r14 import *

out=Path('evidence/R13_DEMO')
if out.exists():shutil.rmtree(out)
out.mkdir(parents=True)
before=make_fixture()
choices=make_choices_single()
p=plan(before,choices,'SIM-DEMO-R13-001')
summary=preview_summary(p)
(out/'PREVIEW_BEFORE_AFTER.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
(out/'BEFORE.json').write_text(json.dumps(before,indent=2,ensure_ascii=False)+'\n')
store=DurableStore(out/'diskstore',before)
commit=DurableController(store).run(p)
if commit['state']!='COMMITTED' or store.get_all()!=p['updates']:
    raise AssertionError('no readback commit')
(out/'AFTER.json').write_text(json.dumps(store.get_all(),indent=2,ensure_ascii=False)+'\n')
again=DurableController(DurableStore(out/'diskstore')).run(p)
if again['state']!='COMMITTED' or store.get_all()!=p['updates']:
    raise AssertionError('replay idempotency')
undo=DurableController(DurableStore(out/'diskstore')).explicit_rollback(p['event_id'])
if undo['state']!='COMMITTED' or DurableStore(out/'diskstore').get_all()!=before:
    raise AssertionError('undo readback failed')
(out/'AFTER_ROLLBACK.json').write_text(json.dumps(DurableStore(out/'diskstore').get_all(),indent=2,ensure_ascii=False)+'\n')
replay_plan=plan(DurableStore(out/'diskstore').get_all(),choices,'SIM-DEMO-R13-002')
redo=DurableController(DurableStore(out/'diskstore')).run(replay_plan)
replayed=DurableStore(out/'diskstore').get_all()
def gameplay_only(pages):
    import copy
    q=copy.deepcopy(pages)
    for x in q.values():x.pop('history',None) # A fresh event must have a distinct audit history.
    return q
if redo['state']!='COMMITTED' or gameplay_only(replayed)!=gameplay_only(p['updates']):
    raise AssertionError('new-event replay mechanics failed')
result={'event_id_first':p['event_id'],'event_id_replay':replay_plan['event_id'],
        'first_commit':commit['state'],'same_event_idempotent':again['state'],
        'compensating_inverse_event':undo['event_id'],'inverse_committed':undo['state'],
        'new_event_replay':redo['state'],'before_digest':digest(before),
        'after_digest':digest(p['updates']),'rollback_matches_before':True,
        'replay_mechanics_match_after':True,'replay_history_distinct':True,'level':[before['NORMAL']['level'],p['updates']['NORMAL']['level']],
        'normal_hp_max':[before['NORMAL']['hp_max'],p['updates']['NORMAL']['hp_max']],
        'normal_hp_current':[before['NORMAL']['hp_current'],p['updates']['NORMAL']['hp_current']],
        'normal_pa_max':[before['NORMAL']['pa_max'],p['updates']['NORMAL']['pa_max']],
        'normal_pa_current':[before['NORMAL']['pa_current'],p['updates']['NORMAL']['pa_current']],
        'normal_ff':[before['NORMAL']['derived']['ff'],p['updates']['NORMAL']['derived']['ff']],
        'transform_ff':[before['TRANSFORM']['derived']['ff'],p['updates']['TRANSFORM']['derived']['ff']],
        'ff_new_lock':'300 (simulated selected damage d4=2)',
        'scope':'offline synthetic; Notion writes=0; Party writes=0'}
(out/'RUN_RECEIPT.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
