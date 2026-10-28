import unittest
from report_audit_v05 import validate_player_report,pa_spend_policy_guard,ReportHold

B={'Vida':'50/100','Alma':'25/40','CA':30}
A={'Vida':'50/120','Alma':'25/40','CA':32}
M={'Vida':{'before':'50/100','after':'50/120'},'CA':{'before':30,'after':32}}

class ReportTest(unittest.TestCase):
 def test_complete_report_candidate(self):
    x=validate_player_report(before=B,after=A,report_fields=M,written_field_keys={'Vida','CA'},
        detail='Sua Vida máxima passou de cem para cento e vinte, e CA aumentou em dois.')
    self.assertEqual(x['changed'],2)
    self.assertFalse(x['safe_to_send_to_party'])
 def test_missing_changed_field(self):
    with self.assertRaises(ReportHold):
        validate_player_report(before=B,after=A,report_fields={'Vida':M['Vida']},written_field_keys={'Vida','CA'},detail='Sua Vida máxima mudou bastante.')
 def test_secret_bap_leak(self):
    with self.assertRaises(ReportHold):
        validate_player_report(before=B,after=A,report_fields=M,written_field_keys={'Vida','CA'},detail='Seu BAP oculto Mestre-side foi recalculado.')
 def test_pa_priority_hold(self):
    x=pa_spend_policy_guard(normal_pa_available=30,spirit_pa_available=100,technique_cost=20,explicit_policy=None)
    self.assertEqual(x['status'],'HOLD_NO_CANONICAL_PA_SPEND_PRIORITY')
 def test_negative_pa_invalid(self):
    with self.assertRaises(ReportHold):pa_spend_policy_guard(normal_pa_available=-1,spirit_pa_available=0,technique_cost=2,explicit_policy=None)
 def test_pa_insufficient_hold(self):
    x=pa_spend_policy_guard(normal_pa_available=10,spirit_pa_available=5,technique_cost=20,explicit_policy='NORMAL_FIRST')
    self.assertEqual(x['status'],'HOLD_INSUFFICIENT_TOTAL_PA')

if __name__=='__main__':unittest.main()
