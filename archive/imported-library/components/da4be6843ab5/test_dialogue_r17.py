import copy,tempfile,unittest
from dialogue_r17 import DialogueR17,DialogueR17Hold
from engine_r17 import bronze5_fixture,lendario_ff_fixture
from r16_gate import prata_fixture
from roll_ledger_r17 import RollLedger
from durable_r14 import DurableStore,DurableController
from r10_recovery import digest

class DialogueEndToEndR17(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.ledger=RollLedger(self.tmp.name+'/rolls')
    def tearDown(self):self.tmp.cleanup()
    def new(self,state=None,target=7,event='SIM-R17-DIALOGUE'):
        return DialogueR17(prata_fixture() if state is None else state,target,event,self.ledger)
    def drive(self,d,mode='FIXO'):
        results=[]
        for a in ('CONFIRMO_NIVEIS',2,mode,{'FOR':2},{'FOR':3,'CON':3}):
            results.append((d.prompt(),a,d.respond(a)['status']))
        if d.phase=='ROLLS':results.append((d.prompt(),'ROLAR_AGORA',d.respond('ROLAR_AGORA')['status']))
        results.append((d.prompt(),'CONFIRMO',d.respond('CONFIRMO')['status']))
        return results
    def test_fixed_complete_conversation(self):
        d=self.new();ans=self.drive(d)
        self.assertEqual(d.phase,'READY');self.assertEqual(len(ans),6)
        self.assertEqual(d.executable_plan()['updates']['NORMAL']['level'],7)
        self.assertIn('PRÉVIA',ans[-1][0]);self.assertIn('quantos pontos',ans[1][0])
    def test_rolled_complete_conversation(self):
        d=self.new()
        self.drive(d,'ROLAR')
        p=d.executable_plan();self.assertEqual(len(p['roll_receipt_hashes']),4)
        self.assertEqual(d.safe_summary()['receipts_generated'],4)
    def test_level_5_to_6_complete(self):
        d=self.new(bronze5_fixture(),6,'SIM-R17-CROSS-DIALOGUE')
        self.drive(d,'ROLAR')
        self.assertEqual(d.executable_plan()['transition_label'],'BRONZE5_PRATA1_CONDITIONAL_SANDBOX')
        self.assertFalse(d.executable_plan()['steps'][0]['legal_transform_activation'])
    def test_rate_mismatch_holds(self):
        d=self.new();d.respond('CONFIRMO_NIVEIS')
        self.assertEqual(d.respond(99)['status'],'HOLD');self.assertEqual(d.blocker,'PLAYER_RATE_MISMATCH_SOURCE')
        with self.assertRaises(DialogueR17Hold):d.executable_plan()
    def test_invalid_attribute_blocks_without_progress(self):
        d=self.new();d.respond('CONFIRMO_NIVEIS');d.respond(2);d.respond('FIXO')
        for bad in ({'FOR':1},{'FOR':-1,'DES':3},{'LUCK':2}):
            with self.assertRaises(DialogueR17Hold):d.respond(bad)
            self.assertEqual(d.phase,'NORMAL')
    def test_invalid_mode_blocks_without_progress(self):
        d=self.new();d.respond('CONFIRMO_NIVEIS');d.respond(2)
        with self.assertRaises(DialogueR17Hold):d.respond({'VIDA':'FIXO'})
        self.assertEqual(d.phase,'MODE')
    def test_no_confirmation_no_plan(self):
        d=self.new()
        with self.assertRaises(DialogueR17Hold):d.executable_plan()
    def test_revision_before_rolling(self):
        d=self.new();d.respond('CONFIRMO_NIVEIS');d.respond(2);d.respond('ROLAR')
        d.respond({'FOR':2});d.respond({'FOR':3,'CON':3})
        self.assertEqual(d.respond('CORRIGIR')['status'],'NORMAL')
        d.respond({'DES':2});d.respond({'FOR':3,'CON':3});d.respond('ROLAR_AGORA');d.respond('CONFIRMO')
        self.assertEqual(d.executable_plan()['updates']['NORMAL']['attrs']['DES'],9)
    def test_revision_after_rolling_keeps_receipts(self):
        d=self.new();d.respond('CONFIRMO_NIVEIS');d.respond(2);d.respond('ROLAR')
        d.respond({'FOR':2});d.respond({'FOR':3,'CON':3});d.respond('ROLAR_AGORA')
        earlier={k:v['receipt_sha256'] for k,v in d.choices['roll_receipts'].items()}
        d.respond('CORRIGIR');d.respond({'DES':2});d.respond({'FOR':3,'CON':3})
        d.respond('ROLAR_AGORA');d.respond('CONFIRMO')
        self.assertEqual({k:v['receipt_sha256'] for k,v in d.choices['roll_receipts'].items()},earlier)
    def test_crash_rebuild_dialogue_reuses_same_dice_event(self):
        d=self.new();self.drive(d,'ROLAR')
        past={k:v['receipt_sha256'] for k,v in d.choices['roll_receipts'].items()}
        d2=self.new();self.drive(d2,'ROLAR')
        restored={k:v['receipt_sha256'] for k,v in d2.choices['roll_receipts'].items()}
        self.assertEqual(past,restored)
        self.assertEqual(d2.executable_plan()['updates'],d.executable_plan()['updates'])
    def test_unique_roll_across_retry_of_same_event(self):
        d=self.new();self.drive(d,'ROLAR')
        same=RollLedger(self.tmp.name+'/rolls')
        receipts={k:v['receipt_sha256'] for k,v in d.choices['roll_receipts'].items()}
        for rid,rec in d.choices['roll_receipts'].items():
            sp=rec['spec'];self.assertEqual(same.draw(rid,sp['event_id'],sp['purpose'],sp['sides'],sp['count'])[1]['receipt_sha256'],receipts[rid])
    def test_confirmation_protects_writes(self):
        d=self.new();self.drive(d)
        p=d.executable_plan()
        store=DurableStore(self.tmp.name+'/store',d.state);ctrl=DurableController(store)
        start=digest(store.get_all());r=ctrl.run(p);after=digest(store.get_all())
        self.assertEqual(r['state'],'COMMITTED')
        self.assertNotEqual(start,after)
        self.assertEqual(ctrl.run(p)['intent_hash'],r['intent_hash'])
        ctrl.explicit_rollback(d.event_id)
        self.assertEqual(digest(store.get_all()),start)
        self.assertEqual(ctrl.run({**p,'event_id':'SIM-R17-SECOND-EXEC'})['state'],'COMMITTED')
    def test_conditional_prompts_multiple(self):
        state=prata_fixture();state['NORMAL']['choice_contracts']=[
            {'id':'SIM-ABILITY','source':'SIMULATED_VERIFIED_CONTRACT','impact':'RECORD_ONLY_TEST','level':7,
             'label':'habilidade fictícia','options':['A','B']},
            {'id':'SIM-RACE','source':'SIMULATED_VERIFIED_CONTRACT','impact':'RECORD_ONLY_TEST','level':7,
             'label':'raça fictícia','options':['R1','R2']}]
        d=self.new(state)
        for a in ('CONFIRMO_NIVEIS',2,'FIXO',{'FOR':2},{'FOR':3,'CON':3}):d.respond(a)
        self.assertEqual(d.phase,'CONDITIONAL')
        self.assertIn('habilidade fictícia',d.prompt())
        d.respond('A');self.assertIn('raça fictícia',d.prompt())
        d.respond('R2');self.assertEqual(d.phase,'CONFIRM')
        d.respond('CONFIRMO')
        self.assertEqual(len(d.executable_plan()['updates']['NORMAL']['synthetic_choice_history']),2)
    def test_unsupported_effect_rejected(self):
        state=prata_fixture();state['NORMAL']['choice_contracts']=[{'id':'SIM-ABILITY','source':'UNVERIFIED','impact':'REAL','level':7,
             'label':'x','options':['A','B']}]
        with self.assertRaises(DialogueR17Hold):self.new(state)
    def test_real_ff_milestone_prompts_and_rolls_once(self):
        d=self.new(lendario_ff_fixture(),22,'SIM-R17-FF-SPECIFIC')
        d.respond('CONFIRMO_NIVEIS');d.respond(2);d.respond('FIXO')
        x=d.respond({'FOR':2})
        self.assertEqual(x['status'],'FF');self.assertIn('600',d.prompt())
        with self.assertRaises(DialogueR17Hold):d.respond('MAGIA')
        d.respond('CA');self.assertEqual(d.phase,'CONFIRM')
        d.respond('CONFIRMO');p=d.executable_plan()
        self.assertEqual(len(p['roll_receipt_hashes']),1)
        self.assertEqual(p['updates']['LOCKS']['milestones']['6']['type'],'CA')
        self.assertEqual(d.safe_summary()['receipts_generated'],1)
    def test_change_ff_type_cannot_trigger_reroll(self):
        d=self.new(lendario_ff_fixture(),22,'SIM-R17-FF-FROZEN')
        for a in ('CONFIRMO_NIVEIS',2,'FIXO',{'FOR':2},'CA','CORRIGIR',{'FOR':2}):
            d.respond(a)
        self.assertEqual(d.phase,'FF')
        with self.assertRaises(DialogueR17Hold):d.respond('DANO')
        d.respond('CA');d.respond('CONFIRMO')
        self.assertEqual(d.safe_summary()['receipts_generated'],1)
    def test_prompts_no_master_secrets(self):
        d=self.new();logs=self.drive(d,'ROLAR');prompts='\n'.join(x[0] for x in logs)
        for key in ('BAP','CM-000','IBX-','NAC-','writer','lease','epoch','SIM-R17','SHA-256','checksum'):
            self.assertNotIn(key,prompts)
    def test_full_2_level_choices(self):
        d=self.new(prata_fixture(),8,'SIM-R17-MULTI-DIALOGUE')
        answers=['CONFIRMO_NIVEIS',2,'FIXO',{'FOR':2},{'FOR':3,'CON':3},
                 {'DES':2},{'CON':3,'FOR':3},'CONFIRMO']
        for a in answers:d.respond(a)
        self.assertEqual(len(d.executable_plan()['steps']),2)
    def test_full_2_level_crossing(self):
        d=self.new(bronze5_fixture(),7,'SIM-R17-MULTI-CROSS-DIALOGUE')
        answers=['CONFIRMO_NIVEIS',2,'FIXO',{'FOR':2},{'FOR':3,'CON':3},
                 {'DES':2},{'CON':3,'FOR':3},'CONFIRMO']
        for a in answers:d.respond(a)
        self.assertEqual(d.executable_plan()['updates']['NORMAL']['level'],7)
        self.assertEqual(d.executable_plan()['steps'][0]['rank'],'Prata')
    def test_cancel_requires_mestre(self):
        d=self.new()
        self.assertEqual(d.respond('REVISAR_NIVEIS')['status'],'HOLD')
        self.assertEqual(d.blocker,'MESTRE_TARGET_RECONCILIATION')
    def test_no_external_write_method(self):
        d=self.new();self.assertFalse(hasattr(d,'send_party_message'))
        self.assertFalse(hasattr(d,'write_notion'))

if __name__=='__main__':unittest.main()
