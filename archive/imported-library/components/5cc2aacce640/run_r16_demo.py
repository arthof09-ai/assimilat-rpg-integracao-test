"""Execute only a fictional Prata1->Prata2 conversation and local reversible edit."""
from pathlib import Path
import copy,json,tempfile
from r10_recovery import digest
from durable_r14 import DurableStore,DurableController
from dialogue_r16 import Dialogue
from r16_gate import prata_fixture,access,historical_r13_audit

ROOT=Path(__file__).resolve().parent

def write(path,obj):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True),encoding='utf-8')


def run_demo(output=None):
    if output is None:
        root=ROOT/'evidence';root.mkdir(parents=True,exist_ok=True)
        out=Path(tempfile.mkdtemp(prefix='DEMO_R16_CORRECTED_',dir=root))
    else:
        out=Path(output)
        if out.exists() and any(out.iterdir()):
            raise FileExistsError('do not overwrite a previous checkpoint')
        out.mkdir(parents=True,exist_ok=True)
    before=prata_fixture();s=Dialogue(copy.deepcopy(before),7,'SIM-R16-E2E-001')
    transcript=[]
    steps=[2,'FIXO',{'FOR':2},{'FOR':3,'CON':3},'CONFIRMO']
    for answer in steps:
        prompt=s.prompt();response=s.respond(answer)
        transcript.append({'message_candidate':prompt,'test_response':answer,
                           'stage_after':response['status']})
    plan=s.executable_plan()
    store=DurableStore(out/'LOCAL_STORE',before);ctrl=DurableController(store)
    before_hash=digest(store.get_all())
    receipt=ctrl.run(plan);assert receipt['state']=='COMMITTED'
    after=store.get_all();assert after['NORMAL']['level']==7
    repeat=ctrl.run(plan);assert repeat['intent_hash']==receipt['intent_hash']
    after_hash=digest(after);assert digest(store.get_all())==after_hash
    inverse=ctrl.explicit_rollback(s.event_id)
    restored=store.get_all();restored_hash=digest(restored)
    assert restored_hash==before_hash and inverse['state']=='COMMITTED'
    copyplan=copy.deepcopy(plan);copyplan['event_id']='SIM-R16-E2E-REPLAY-002'
    replay=ctrl.run(copyplan);assert replay['state']=='COMMITTED'
    after_replay=store.get_all()
    # Pure mechanical results equal; history receipt is deliberately distinct.
    assert after_replay['NORMAL']['attrs']==after['NORMAL']['attrs']
    assert after_replay['NORMAL']['hp_max']==after['NORMAL']['hp_max']
    assert after_replay['NORMAL']['pa_max']==after['NORMAL']['pa_max']
    write(out/'BEFORE.json',before)
    write(out/'AFTER.json',after)
    write(out/'AFTER_ROLLBACK.json',restored)
    write(out/'AFTER_REPLAY.json',after_replay)
    write(out/'DECISIONS_TRANSCRIPT.json',transcript)
    write(out/'PREVIEW_PRIVATE.json',{'steps':plan['steps'],'before_digest':plan['before_digest'],
                                      'diff':plan['diff'],'level_range':[6,7]})
    report={'status':'PASS_OFFLINE_ONLY',
            'engine':'R13 preserved + R16 Silver gate and dialogue',
            'first_legal_transformation_rank':'PRATA_1_ORDINAL_6',
            'historical_bronze_test':historical_r13_audit(),
            'event_id':s.event_id,'level':[6,7],
            'normal_hp_max':[before['NORMAL']['hp_max'],after['NORMAL']['hp_max']],
            'normal_hp_current':[before['NORMAL']['hp_current'],after['NORMAL']['hp_current']],
            'normal_pa_max':[before['NORMAL']['pa_max'],after['NORMAL']['pa_max']],
            'normal_pa_current':[before['NORMAL']['pa_current'],after['NORMAL']['pa_current']],
            'normal_ff':[before['NORMAL']['derived']['ff'],after['NORMAL']['derived']['ff']],
            'transform_ff_precalculated_inactive':[before['TRANSFORM']['derived']['ff'],after['TRANSFORM']['derived']['ff']],
            'new_ff_lock_deferred_until_real_activation':plan['deferred_until_actual_activation_ff_milestones'],
            'snapshot_verified':True,'idempotent_repeat_verified':True,
            'rollback_exact':restored_hash==before_hash,
            'replay_distinct_event_verified':replay['state']=='COMMITTED',
            'before_sha256':before_hash,'after_sha256':after_hash,
            'rollback_sha256':restored_hash,
            'notion_native_writes':0,'player_real_writes':0,'production_released':False,
            'mode':'FIXED_60_EXPLICIT_SYNTHETIC_CHOICES',
            'player_party_messages_sent':0}
    write(out/'R16_RECEIPT.json',report)
    return report

if __name__=='__main__':print(json.dumps(run_demo(),ensure_ascii=False,indent=2))
