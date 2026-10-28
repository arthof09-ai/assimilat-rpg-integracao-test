"""R25 runtime safe-report capability; no external delivery."""
import copy,json,tempfile,unittest
from pathlib import Path
from engine_r17 import bronze1_fixture
from r16_gate import prata_fixture
from roll_ledger_r17 import RollLedger
from dialogue_r17 import DialogueR17
from durable_r14 import DurableStore
from safe_runner_r17 import SafeLocalR17Runner,RunnerHold

class LocalSafeReport(unittest.TestCase):
    def setup_case(self,tmp,bronze=True):
        state=bronze1_fixture() if bronze else prata_fixture()
        d=DialogueR17(state,2 if bronze else 7,'SIM-R25-REPORT',RollLedger(Path(tmp)/'roll'))
        answers=['CONFIRMO_NIVEIS',2,'FIXO',{'INT':2},{'FOR':3,'CON':3}] if bronze else ['CONFIRMO_NIVEIS',2,'FIXO',{'DES':2},{'FOR':3,'CON':3}]
        for a in answers:d.respond(a)
        d.respond('CONFIRMO')
        return d,SafeLocalR17Runner(DurableStore(Path(tmp)/'store',state))
    def test_report_not_available_prior_to_commit(self):
        with tempfile.TemporaryDirectory() as t:
            d,runner=self.setup_case(t)
            with self.assertRaises(RunnerHold):runner.verified_player_safe_local_report(d)
    def test_report_available_after_commit_and_is_allowlisted(self):
        with tempfile.TemporaryDirectory() as t:
            d,runner=self.setup_case(t);runner.execute(d)
            report=runner.verified_player_safe_local_report(d)
            self.assertEqual(report['nivel_anterior'],1)
            self.assertEqual(report['nivel_atual'],2)
            self.assertEqual(report['alteracoes_atributos_normais']['INT'],{'antes':4,'depois':6})
            self.assertEqual(report['vida_atual']['antes'],report['vida_atual']['depois'])
            self.assertIn('Bronze',report['observacao_forma'])
            text=json.dumps(report,ensure_ascii=False)
            for secret in ('bap','tap','sim-r25','roll_receipts','receipt_sha256','writer_authorized','CM-000','milestones','secret','SPIRIT','hash'):
                self.assertNotIn(secret.lower(),text.lower(),secret)
            self.assertEqual(report['aviso'],'Demonstração local: nenhuma ficha do Notion foi alterada; não enviar à Party.')
    def test_report_rejected_after_rollback(self):
        with tempfile.TemporaryDirectory() as t:
            d,runner=self.setup_case(t);runner.execute(d)
            runner.rollback(d)
            with self.assertRaises(RunnerHold):runner.verified_player_safe_local_report(d)
    def test_report_rejected_if_data_mutated_after_commit(self):
        with tempfile.TemporaryDirectory() as t:
            d,runner=self.setup_case(t);runner.execute(d)
            altered,v=runner.store.read('NORMAL')
            altered['attrs']['INT']+=99
            runner.store.cas('NORMAL',v,altered)
            with self.assertRaises(RunnerHold):
                runner.verified_player_safe_local_report(d)
    def test_silver_report_not_mistaken_for_spirit_activation(self):
        with tempfile.TemporaryDirectory() as t:
            d,runner=self.setup_case(t,bronze=False);runner.execute(d)
            report=runner.verified_player_safe_local_report(d)
            self.assertIn('não ativou',report['observacao_forma'])
            self.assertEqual(report['nivel_atual'],7)
            self.assertNotIn('spirit',str(report).lower())

if __name__=='__main__':unittest.main()
