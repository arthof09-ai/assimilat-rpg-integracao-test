"""Run four reproducible local-only RPG level-up conversations and receipts.

This is not a Party sender and never calls any connector. The R16 historical code
remains unmodified; all changes are additive R17.
"""
from pathlib import Path
import copy,json,tempfile
from dialogue_r17 import DialogueR17
from engine_r17 import bronze5_fixture,lendario_ff_fixture,validate_r17
from r16_gate import prata_fixture
from roll_ledger_r17 import RollLedger
from durable_r14 import DurableStore,DurableController
from safe_runner_r17 import SafeLocalR17Runner
from r10_recovery import digest

ROOT=Path(__file__).resolve().parent

def write(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2),encoding='utf-8')

def scenario(name,fixture,target,mode,responses,out,ev):
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    ledger=RollLedger(out/'ROLL_LEDGER')
    d=DialogueR17(copy.deepcopy(fixture),target,ev,ledger)
    transcript=[]
    answers=['CONFIRMO_NIVEIS',2,mode]+responses
    for response in answers:
        question=d.prompt(); result=d.respond(response)
        transcript.append({'question_candidate':question,'synthetic_player_answer':response,
                           'phase_after':result['status']})
    if d.phase=='ROLLS':
        q=d.prompt();result=d.respond('ROLAR_AGORA');transcript.append(
            {'question_candidate':q,'synthetic_player_answer':'ROLAR_AGORA','phase_after':result['status']})
    if d.phase!='CONFIRM':raise AssertionError('full questions not complete')
    confirmation_text=d.prompt()
    result=d.respond('CONFIRMO');transcript.append(
        {'question_candidate':confirmation_text,'synthetic_player_answer':'CONFIRMO',
         'phase_after':result['status']})
    plan=d.executable_plan()
    state=DurableStore(out/'LOCAL_3_PAGE_WAL',fixture)
    ctrl=DurableController(state)
    safe=SafeLocalR17Runner(state)
    before=digest(state.get_all())
    receipt=safe.execute(d)
    if receipt['status']!='COMMITTED_LOCAL_VERIFIED':raise AssertionError('confirmed safe local commit failed')
    after_state=state.get_all()
    if not validate_r17(after_state):raise AssertionError('state validation failed')
    after=digest(after_state)
    identical=safe.execute(d)
    if identical['status']!='NOOP_VERIFIED_IDEMPOTENT' or digest(state.get_all())!=after:
        raise AssertionError('same ID must never double-apply')
    undo=safe.rollback(d)
    if undo['status']!='ROLLED_BACK_VERIFIED_LOCAL' or digest(state.get_all())!=before:raise AssertionError('rollback failed')
    # Explicitly label as reapplication of the same historical saved intent,
    # not a fresh player evolution, new roll or authorized Party operation.
    replayplan=copy.deepcopy(plan)
    replayplan['event_id']=ev+'-RECORDED-INTENT-REAPPLY'
    if not all(RollLedger.verify(r) for r in d.choices['roll_receipts'].values()):
        raise AssertionError('roll receipt compromised before intent reapply')
    replay=ctrl.run(replayplan)
    replaystate=state.get_all()
    if replay['state']!='COMMITTED' or digest(replaystate)!=after:
        raise AssertionError('reapplication changed mechanical result')
    write(out/'BEFORE.json',fixture)
    write(out/'AFTER.json',after_state)
    write(out/'AFTER_ROLLBACK.json',plan['before'])
    write(out/'AFTER_REAPPLIED_INTENT.json',replaystate)
    write(out/'TRANSCRIPT_SYNTHETIC.json',transcript)
    write(out/'ROLL_RECEIPTS_MASTER_SIDE.json',list(d.choices['roll_receipts'].values()))
    write(out/'PLAN_HASHES_MASTER_SIDE.json',{'before':plan['before_digest'],'diff':plan['diff'],
                                               'steps':plan['steps'],'roll_hashes':plan['roll_receipt_hashes']})
    out_report={'scenario':name,'status':'PASS_LOCAL_SYNTHETIC_ONLY',
         'initial_level':fixture['NORMAL']['level'],'target_level':target,
         'character_label':'SYNTHETIC_TEST_ACTOR',
         'dialogue_turns':len(transcript),'roll_receipts':len(d.choices['roll_receipts']),
         'receipt_hashes':[r['receipt_sha256'] for r in d.choices['roll_receipts'].values()],
         'FF_locks_new':sorted(set(after_state['LOCKS']['milestones'])-set(fixture['LOCKS']['milestones'])),
         'level_gain':[fixture['NORMAL']['level'],after_state['NORMAL']['level']],
         'hp_max':[fixture['NORMAL']['hp_max'],after_state['NORMAL']['hp_max']],
         'hp_current':[fixture['NORMAL']['hp_current'],after_state['NORMAL']['hp_current']],
         'pa_max':[fixture['NORMAL']['pa_max'],after_state['NORMAL']['pa_max']],
         'pa_current':[fixture['NORMAL']['pa_current'],after_state['NORMAL']['pa_current']],
         'activation_state':after_state['TRANSFORM']['activation_state'],
         'transition_label':plan['transition_label'],
         'before_digest':before,'after_digest':after,'rollback_digest':before,
         'idempotent_same_id':True,'rollback_exact':True,
         'reapply_recorded_intent_with_same_rolls':True,
         'party_messages_sent':0,'notion_writes':0,'official_formula_certified':False}
    write(out/'R17_SCENARIO_RECEIPT.json',out_report)
    return out_report

def run_demo(dest):
    dest=Path(dest)
    if dest.exists() and any(dest.iterdir()):raise FileExistsError('new checkpoint required; never overwrite a receipt')
    dest.mkdir(parents=True,exist_ok=True)
    silver=prata_fixture();bronze=bronze5_fixture();ff=lendario_ff_fixture()
    cases=[
        ('PRATA1_PRATA2_DADOS',silver,7,'ROLAR',[{'FOR':2},{'FOR':3,'CON':3}],'SIM-R17-E2E-SILVER-ROLL'),
        ('BRONZE5_PRATA1_FIXO',bronze,6,'FIXO',[{'FOR':2},{'FOR':3,'CON':3}],'SIM-R17-E2E-BRONZE-SILVER'),
        ('BRONZE5_PRATA2_DADOS',bronze,7,'ROLAR',[{'FOR':2},{'FOR':3,'CON':3},
                                                   {'DES':2},{'FOR':3,'CON':3}],'SIM-R17-E2E-BRONZE-MULTI'),
        ('LENDARIO1_LENDARIO2_FF',ff,22,'FIXO',[{'FOR':2},'CA'],'SIM-R17-E2E-FF600')]
    result=[]
    for name,fixture,target,mode,answers,event in cases:
        result.append(scenario(name,fixture,target,mode,answers,dest/name,event))
    summary={'suite':'R17_OFFLINE_E2E','cases':len(result),'passing':sum(x['status']=='PASS_LOCAL_SYNTHETIC_ONLY' for x in result),
             'roll_receipts':sum(x['roll_receipts'] for x in result),
             'transcript_messages':sum(x['dialogue_turns'] for x in result),
             'results':result,'notion_writes':0,'party_messages':0,
             'claim':'SIMULATED_PROOF_ONLY_NOT_AUTHORIZED_NATIVE_OR_PLAYER_OPERATION'}
    write(dest/'DEMO_R17_SUMMARY.json',summary)
    return summary

if __name__=='__main__':
    output=ROOT/'evidence'/'DEMO_R17_SAFE_RUNNER_V2'
    print(json.dumps(run_demo(output),ensure_ascii=False,indent=2))
