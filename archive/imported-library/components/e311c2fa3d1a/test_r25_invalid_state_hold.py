"""R25 safety patch: block stale/negative preimage rather than levelling it."""
import unittest
from r16_gate import prata_fixture
from engine_r17 import bronze1_fixture,validate_r17,R17Hold,plan_r17

class CorruptInputHOLD(unittest.TestCase):
    def test_negative_normal_hp_does_not_enter_planner(self):
        b=prata_fixture();b['NORMAL']['hp_current']=-2
        with self.assertRaises(R17Hold):validate_r17(b)
    def test_stale_spendable_pa_does_not_enter_planner(self):
        b=prata_fixture();b['NORMAL']['pa_spendable_now']=999
        with self.assertRaises(R17Hold):validate_r17(b)
    def test_negative_spirit_reserves_rejected(self):
        for field in ('hp_bonus_current','pa_bonus_current','hp_bonus_max','pa_bonus_max'):
            with self.subTest(field=field):
                b=prata_fixture();b['TRANSFORM'][field]=-1
                with self.assertRaises(R17Hold):validate_r17(b)
    def test_invalid_hp_field_wrong_type(self):
        b=prata_fixture();b['NORMAL']['hp_current']=True
        with self.assertRaises(R17Hold):validate_r17(b)
    def test_normal_reserve_over_max_rejected(self):
        b=prata_fixture();b['NORMAL']['hp_current']=b['NORMAL']['hp_max']+1
        with self.assertRaises(R17Hold):validate_r17(b)
    def test_negative_pa_spendable_implicit(self):
        b=prata_fixture();b['NORMAL']['pa_committed']=b['NORMAL']['pa_current']+1
        b['NORMAL']['pa_spendable_now']=-1
        with self.assertRaises(R17Hold):validate_r17(b)
    def test_normal_and_bronze_baselines_still_valid(self):
        for b in (prata_fixture(),bronze1_fixture()):self.assertTrue(validate_r17(b))

if __name__=='__main__':unittest.main()
