"""Deterministic R16 stress, seed fixed. Not a Notion/Party rehearsal."""
from __future__ import annotations
import json,random,copy,tempfile
from pathlib import Path
from dialogue_r16 import Dialogue
from r16_gate import prata_fixture,access,authorize_activation,TransformationLocked
from r10_recovery import digest
from durable_r14 import DurableStore,DurableController

rnd=random.Random(20261009)
assertions=0
cases=0
for lv in range(1,26):
    gate=access(lv)
    assert gate['can_activate_transformation']==(lv>=6);assertions+=1
    if lv<6:
        try:authorize_activation(lv,scene_id='SIM-SCENE',rested=True,used_scene=False)
        except TransformationLocked:assertions+=1
        else:raise AssertionError('Bronze activation incorrectly permitted')
# 1200 varied fictional dialogues; never send prompts to real players.
for i in range(1200):
    fixture=prata_fixture()
    dialog=Dialogue(fixture,7,f'SIM-R16-STRESS-{i:05d}')
    assert dialog.respond(2)['status']=='MODE';assertions+=1
    dialog.respond('FIXO');a=rnd.randint(0,2)
    alloc={'FOR':a,'DES':2-a};dialog.respond(alloc)
    b=rnd.randint(0,6)
    dialog.respond({'FOR':b,'CON':6-b})
    while dialog.phase=='FF':
        option=rnd.choice(['DANO','CA','VIDA'])
        v=[rnd.randint(1,6) for _ in range(2)] if option=='VIDA' else [rnd.randint(1,4)]
        dialog.respond({'type':option,'rolls':v,'source':'SIMULATED_DICE_ONLY'})
    assert dialog.phase=='CONFIRM';assertions+=1
    dialog.respond('CONFIRMO');p=dialog.executable_plan()
    a=p['updates']['NORMAL'];t=p['updates']['TRANSFORM'];locks=p['updates']['LOCKS']['milestones']
    assert a['level']==7;assertions+=1
    assert a['hp_current']==fixture['NORMAL']['hp_current'];assertions+=1
    assert a['pa_current']==fixture['NORMAL']['pa_current'];assertions+=1
    assert t['activation_state']=='INACTIVE_NO_T6B_REFRESH';assertions+=1
    assert t['hp_bonus_current']==0 and t['pa_bonus_current']==0;assertions+=1
    assert len(locks)==5 and '6' not in locks and len(locks)==len(set(locks));assertions+=1
    assert p['deferred_until_actual_activation_ff_milestones']==['6'];assertions+=1
    cases+=1

# Additional 40 actual local WAL commit/inverse/replay, distinct synthetic actors.
wal_cases=40
for i in range(wal_cases):
    fixture=prata_fixture();d=Dialogue(fixture,7,f'SIM-R16-WAL-{i:03d}')
    d.respond(2);d.respond('FIXO');d.respond({'FOR':2});d.respond({'FOR':3,'CON':3});
    d.respond('CONFIRMO')
    with tempfile.TemporaryDirectory(prefix='r16-wal-') as td:
        store=DurableStore(td,fixture);ctrl=DurableController(store)
        before=digest(store.get_all());p=d.executable_plan()
        x=ctrl.run(p);assert x['state']=='COMMITTED';assertions+=1
        x2=ctrl.run(p);assert x2['intent_hash']==x['intent_hash'];assertions+=1
        ctrl.explicit_rollback(p['event_id']);assert digest(store.get_all())==before;assertions+=1
        p2=copy.deepcopy(p);p2['event_id']=f'SIM-R16-REPLAY-WAL-{i:03d}'
        assert ctrl.run(p2)['state']=='COMMITTED';assertions+=1
out={'seed':20261009,'status':'PASS','scenario_dialogues':cases,
     'rollback_replay_wal_cases':wal_cases,'transformation_levels_checked':25,
     'bronze_levels_refused':5,'assertions':assertions,
     'scope':'synthetic local, not Notion native, no Party messages',
     'real_page_evolutions':0}
fp=Path(__file__).resolve().parent/'evidence'/'R16_STRESS_CORRECTED_A1.json'
fp.parent.mkdir(parents=True,exist_ok=True);fp.write_text(json.dumps(out,indent=2,ensure_ascii=False))
print(json.dumps(out,ensure_ascii=False))
