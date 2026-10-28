"""R17 bounded, unique synthetic stress vectors. Deterministic assertions, OS dice.
Actual die outcomes are intentionally not fixed: receipts permit exact reproduction.
"""
from __future__ import annotations
import copy,json,random,tempfile
from pathlib import Path
from engine_r17 import bronze5_fixture,plan_r17,lendario_ff_fixture,R17Hold
from r16_gate import prata_fixture,access,authorize_activation,TransformationLocked
from dialogue_r17 import DialogueR17,DialogueR17Hold
from roll_ledger_r17 import RollLedger
from durable_r14 import DurableStore,DurableController
from r10_recovery import digest,Conflict

SEED=20261009
ROOT=Path(__file__).resolve().parent

def stress(epochs=600):
    rand=random.Random(SEED)
    counts={'dialogues_attempted':0,'dialogues_pass':0,'roll_receipts_unique':0,
            'concurrent_crash_resume_vectors':0,'invalid_answers_blocked':0,
            'idempotent_roll_retries':0,'rollback_replay_cycles':0,
            'checks':0,'failed':0}
    def check(cond):
        counts['checks']+=1
        if not cond:
            counts['failed']+=1;raise AssertionError(f'R17-STRESS check {counts["checks"]}')
    with tempfile.TemporaryDirectory() as root:
        for i in range(epochs):
            fixture=bronze5_fixture() if i%3==0 else prata_fixture()
            target=6 if i%3==0 else (8 if i%3==1 else 7)
            event=f'SIM-R17-STRESS-{i:06d}'
            rolls=RollLedger(Path(root)/f'rolls{i}')
            d=DialogueR17(fixture,target,event,rolls)
            mode=('ROLAR' if i%2 else 'FIXO')
            counts['dialogues_attempted']+=1
            check(d.phase=='TARGET')
            try:d.respond('ERRADO')
            except DialogueR17Hold:counts['invalid_answers_blocked']+=1
            else:raise AssertionError('invalid target accepted')
            d.respond('CONFIRMO_NIVEIS');d.respond(2);d.respond(mode)
            for lv in range(fixture['NORMAL']['level']+1,target+1):
                if i%5==0:
                    try:d.respond({'FOR':1})
                    except DialogueR17Hold:counts['invalid_answers_blocked']+=1
                    else:raise AssertionError('invalid budget accepted')
                allocation={'FOR':2} if rand.randrange(2)==0 else {'DES':2}
                d.respond(allocation)
                d.respond({'FOR':3,'CON':3})
            if mode=='ROLAR':
                check(d.phase=='ROLLS');d.respond('ROLAR_AGORA')
            check(d.phase=='CONFIRM')
            preview=d.prompt()
            check('PRÉVIA' in preview)
            d.respond('CONFIRMO');p=d.executable_plan()
            check(p['writer_authorized'] is False)
            check(p['updates']['NORMAL']['level']==target)
            check(p['updates']['NORMAL']['hp_current']==fixture['NORMAL']['hp_current'])
            check(p['updates']['NORMAL']['pa_current']==fixture['NORMAL']['pa_current'])
            check(p['updates']['TRANSFORM']['activation_state']=='INACTIVE_NO_T6B_REFRESH')
            check(d.safe_summary()['writes_to_player_or_notion']==0)
            if target==6:
                check(p['steps'][0]['rank_rebase'] is True)
                check(p['steps'][0]['legal_transform_activation'] is False)
            for r in d.choices['roll_receipts'].values():
                check(RollLedger.verify(r));counts['roll_receipts_unique']+=1
                spec=r['spec'];r2=rolls.draw(spec['roll_id'],event,spec['purpose'],spec['sides'],spec['count'])[1]
                check(r2['receipt_sha256']==r['receipt_sha256']);counts['idempotent_roll_retries']+=1
            if i%10==0:
                store=DurableStore(Path(root)/f'store{i}',fixture)
                ctrl=DurableController(store);before=digest(store.get_all())
                e=ctrl.run(p);after=digest(store.get_all())
                check(e['state']=='COMMITTED');check(after!=before)
                check(ctrl.run(p)['intent_hash']==e['intent_hash'])
                check(digest(store.get_all())==after)
                inverse=ctrl.explicit_rollback(event)
                check(inverse['state']=='COMMITTED');check(digest(store.get_all())==before)
                # Reopen across new local object, verify same state.
                reopened=DurableStore(Path(root)/f'store{i}')
                check(digest(reopened.get_all())==before)
                counts['rollback_replay_cycles']+=1
            counts['dialogues_pass']+=1
        for lv in range(1,26):
            check(access(lv)['can_activate_transformation']==(lv>=6))
            if lv<=5:
                try:authorize_activation(lv,scene_id='SIM-SCENE',rested=True,used_scene=False)
                except TransformationLocked:counts['invalid_answers_blocked']+=1
                else:raise AssertionError('Bronze transformed')
        # Commit-first crash/restart before reveal; additional independent vectors.
        for k in range(120):
            e=f'SIM-R17-RESUME-{k:03d}';r=RollLedger(Path(root)/f'resume{k}')
            receipt_id=e+'_LV07_NORMAL_HP'
            pre=r.commit(receipt_id,e,'LV07_NORMAL_HP',8,1)
            check(pre['state']=='COMMITTED_HIDDEN')
            recovery=RollLedger(Path(root)/f'resume{k}')
            val=recovery.reveal(receipt_id,e,'LV07_NORMAL_HP',8,1)
            check(RollLedger.verify(val))
            check(recovery.reveal(receipt_id,e,'LV07_NORMAL_HP',8,1)==val)
            counts['concurrent_crash_resume_vectors']+=1
    return {'protocol':'LEVEL-UP R17 LOCAL STRESS','seed_for_case_selection':SEED,
            'entropy':'OS_RANDOM_PER_RECEIPT_NOT_DETERMINISTIC_OUTCOME',
            'status':'PASS' if counts['failed']==0 else 'FAIL',
            **counts,'native_writes':0,'party_communications':0,
            'notion_atomicity_demonstrated':False}

if __name__=='__main__':
    result=stress()
    import os,tempfile
    output=ROOT/'evidence';output.mkdir(exist_ok=True)
    target=output/'STRESS_R17.json'
    if target.exists():
        fd,name=tempfile.mkstemp(prefix='STRESS_R17_RECHECK_',suffix='.json',dir=str(output))
        os.close(fd);target=Path(name)
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
