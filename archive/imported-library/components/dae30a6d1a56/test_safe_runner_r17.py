import copy,tempfile,unittest
from safe_runner_r17 import SafeLocalR17Runner,RunnerHold
from dialogue_r17 import DialogueR17
from r16_gate import prata_fixture
from roll_ledger_r17 import RollLedger
from durable_r14 import DurableStore
from r10_recovery import digest,Conflict

class SafeGateBeforeCommitTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.before=prata_fixture()
        self.dialogue=DialogueR17(copy.deepcopy(self.before),7,'SIM-R17-SAFE-RUNNER',RollLedger(self.tmp.name+'/roll'))
        self.store=DurableStore(self.tmp.name+'/store',self.before)
        self.runner=SafeLocalR17Runner(self.store)
    def tearDown(self):self.tmp.cleanup()
    def ready(self):
        for answer in ('CONFIRMO_NIVEIS',2,'FIXO',{'FOR':2},{'FOR':3,'CON':3},'CONFIRMO'):
            self.dialogue.respond(answer)
    def test_cannot_execute_before_final_confirmation(self):
        with self.assertRaises(RunnerHold):self.runner.execute(self.dialogue)
        self.assertEqual(digest(self.store.get_all()),digest(self.before))
    def test_commit_after_confirmation_and_exact_rollback(self):
        self.ready();receipt=self.runner.execute(self.dialogue)
        self.assertEqual(receipt['status'],'COMMITTED_LOCAL_VERIFIED')
        self.assertNotEqual(digest(self.store.get_all()),digest(self.before))
        again=self.runner.execute(self.dialogue)
        self.assertEqual(again['status'],'NOOP_VERIFIED_IDEMPOTENT')
        out=self.runner.rollback(self.dialogue)
        self.assertEqual(out['status'],'ROLLED_BACK_VERIFIED_LOCAL')
        self.assertEqual(digest(self.store.get_all()),digest(self.before))
        with self.assertRaises(RunnerHold):self.runner.execute(self.dialogue)
    def test_stale_snapshot_after_preview_holds(self):
        self.ready()
        before,version=self.store.read('NORMAL')
        before['history'].append('SYNTHETIC_CONCURRENT_WRITER')
        self.store.cas('NORMAL',version,before)
        with self.assertRaises(RunnerHold):self.runner.execute(self.dialogue)
    def test_tamper_generated_after_before_commit_denied(self):
        self.ready()
        self.dialogue.result['updates']['NORMAL']['hp_max']+=50
        with self.assertRaises(RunnerHold):self.runner.execute(self.dialogue)
        self.assertEqual(digest(self.store.get_all()),digest(self.before))
    def test_tamper_roll_receipt_denied(self):
        self.dialogue.respond('CONFIRMO_NIVEIS');self.dialogue.respond(2);self.dialogue.respond('ROLAR')
        self.dialogue.respond({'FOR':2});self.dialogue.respond({'FOR':3,'CON':3})
        self.dialogue.respond('ROLAR_AGORA');self.dialogue.respond('CONFIRMO')
        key=next(iter(self.dialogue.result['choices']['roll_receipts']))
        self.dialogue.result['choices']['roll_receipts'][key]['rolls'][0]=99
        with self.assertRaises(Exception):self.runner.execute(self.dialogue)
    def test_cancelled_dialogue_cannot_execute(self):
        self.dialogue.respond('REVISAR_NIVEIS')
        with self.assertRaises(RunnerHold):self.runner.execute(self.dialogue)
    def test_not_notion_writer(self):
        self.assertFalse(hasattr(self.runner,'write_to_notion'))
    def test_no_inverse_without_prior_commit(self):
        self.ready()
        with self.assertRaises(RunnerHold):self.runner.rollback(self.dialogue)

if __name__=='__main__':unittest.main()
