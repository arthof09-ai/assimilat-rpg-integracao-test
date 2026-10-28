"""R25 real delta: synthetic NORMAL Bronze 1..5 elevation with form never usable.
All scenarios use the EXISTING R17 engine and SafeLocalR17Runner.
"""
import copy,tempfile,unittest
from pathlib import Path
from engine_r17 import bronze1_fixture,bronze5_fixture,R17Hold,plan_r17,dice_contracts,validate_r17
from r16_gate import access
from dialogue_r17 import DialogueR17
from roll_ledger_r17 import RollLedger
from durable_r14 import DurableStore
from safe_runner_r17 import SafeLocalR17Runner
from r10_recovery import digest

COMP=('NORMAL_HP','NORMAL_PA','TRANSFORM_HP','TRANSFORM_PA')

def bronze_choice(target,mode='FIXO',attrs=None):
    return {'target_level':target,
      'normal_allocations':{str(lv):(attrs or {}).get(lv,{'INT':2}) for lv in range(2,target+1)},
      'spirit_allocations':{str(lv):{'FOR':3,'CON':3} for lv in range(2,target+1)},
      'resource_modes':{x:mode for x in COMP},'milestones':{},'roll_receipts':{},
      'conditionals':{},'actor':'SIMULATED_TEST_AGENT','approval':'OFFLINE_SYNTHETIC_ONLY'}

class BronzeNormalR25(unittest.TestCase):
    def test_bronze1_baseline_is_synthetic_hypothesis_only(self):
        b=bronze1_fixture()
        self.assertTrue(validate_r17(b));self.assertEqual(b['NORMAL']['level'],1)
        self.assertTrue(all(x['fixture_only'] for x in b.values()))
        self.assertEqual(b['TRANSFORM']['activation_state'],'INACTIVE_NEVER_LEGAL_BRONZE')
        self.assertEqual(b['TRANSFORM']['abilities_active'],[])
        self.assertEqual(b['TRANSFORM']['bronze_accounting'],'SYNTHETIC_HYPOTHESIS_NOT_CANON')
    def test_bronze1_to_bronze2_normal_growth_now_supported(self):
        b=bronze1_fixture();p=plan_r17(b,bronze_choice(2),'SIM-R25-BRONZE-ONE')
        a=p['updates'];s=p['steps']
        self.assertEqual(a['NORMAL']['level'],2)
        self.assertEqual(a['NORMAL']['attrs']['INT'],b['NORMAL']['attrs']['INT']+2)
        self.assertEqual(a['TRANSFORM']['attrs']['INT'],a['NORMAL']['attrs']['INT'])
        self.assertEqual(s[0]['growth']['NORMAL_HP']['dice'],'1d6')
        self.assertEqual(s[0]['growth']['TRANSFORM_HP']['dice'],'1d8')
        self.assertEqual(p['transition_label'],'BRONZE_STAGED_NORMAL_ONLY_SANDBOX')
        self.assertFalse(s[0]['activation_eligible_after_level'])
    def test_bronze1_to5_multilevel_is_consistent(self):
        b=bronze1_fixture();p=plan_r17(b,bronze_choice(5),'SIM-R25-BRONZE-MULTI')
        a=p['updates'];self.assertEqual(len(p['steps']),4)
        self.assertEqual(a['NORMAL']['level'],5)
        self.assertEqual(a['TRANSFORM']['effective_level'],5)
        self.assertEqual(sum(a['TRANSFORM']['overlay'].values()),30)
        self.assertTrue(all(not s['activation_eligible_after_level'] for s in p['steps']))
        self.assertEqual(a['TRANSFORM']['abilities_active'],[])
        self.assertEqual(a['TRANSFORM']['hp_bonus_current'],0)
    def test_crossing_bronze_to_prata_does_not_unlock_activation_automatically(self):
        b=bronze1_fixture();c=bronze_choice(6)
        c['normal_allocations']['6']={'DES':2}
        c['spirit_allocations']['6']={'FOR':3,'CON':3}
        p=plan_r17(b,c,'SIM-R25-BRONZE-CROSS')
        self.assertEqual(p['updates']['NORMAL']['level'],6)
        self.assertTrue(p['steps'][-1]['activation_eligible_after_level'])
        self.assertFalse(p['steps'][-1]['legal_transform_activation'])
        self.assertEqual(p['updates']['TRANSFORM']['activation_state'],'INACTIVE_NO_T6B_REFRESH')
        self.assertEqual(p['transition_label'],'BRONZE_TO_PRATA_CONDITIONAL_SANDBOX')
    def test_legacy_bronze_without_staging_flag_still_denied(self):
        b=bronze1_fixture();del b['TRANSFORM']['bronze_accounting']
        c=bronze_choice(2)
        with self.assertRaises(R17Hold):plan_r17(b,c,'SIM-R25-UNTAGGED')
    def test_spirit_rolls_in_bronze_are_staged_not_playable(self):
        b=bronze1_fixture();c=bronze_choice(2,'ROLAR')
        with tempfile.TemporaryDirectory() as tmp:
            led=RollLedger(tmp)
            for s in dice_contracts(b,c):
                rid='SIM-R25-BRONZE-ROLL_'+s['purpose']
                c['roll_receipts'][rid]=led.draw(rid,'SIM-R25-BRONZE-ROLL',s['purpose'],s['sides'],s['count'])[1]
            p=plan_r17(b,c,'SIM-R25-BRONZE-ROLL')
            self.assertEqual(len(p['roll_receipt_hashes']),4)
            self.assertEqual(p['updates']['TRANSFORM']['abilities_active'],[])
            self.assertIs(p['writer_authorized'],False)
    def test_ff_real_normal_boundary_still_requires_player_choice(self):
        b=bronze1_fixture();c=bronze_choice(5,attrs={2:{'FOR':2},3:{'FOR':2},4:{'FOR':2},5:{'FOR':2}})
        with self.assertRaises(R17Hold):plan_r17(b,c,'SIM-R25-FF-DENY')
    def test_actual_normal_pa_is_not_refilled_during_bronze(self):
        b=bronze1_fixture();p=plan_r17(b,bronze_choice(3),'SIM-R25-NO-RESTORE')
        self.assertEqual(p['updates']['NORMAL']['pa_current'],b['NORMAL']['pa_current'])
        self.assertEqual(p['updates']['NORMAL']['hp_current'],b['NORMAL']['hp_current'])
    def test_bronze_dialogue_omits_forbidden_activation(self):
        b=bronze1_fixture()
        with tempfile.TemporaryDirectory() as tmp:
            d=DialogueR17(b,2,'SIM-R25-BRONZE-DIALOGUE',RollLedger(tmp))
            for answer in ('CONFIRMO_NIVEIS',2,'FIXO',{'INT':2},{'FOR':3,'CON':3},'CONFIRMO'):
                d.respond(answer)
            self.assertEqual(d.phase,'READY')
            self.assertEqual(d.executable_plan()['updates']['NORMAL']['level'],2)
            self.assertFalse(access(2)['can_activate_transformation'])
    def test_bronze_local_commit_and_rollback_exact(self):
        b=bronze1_fixture()
        with tempfile.TemporaryDirectory() as tmp:
            d=DialogueR17(b,2,'SIM-R25-BRONZE-COMMIT',RollLedger(Path(tmp)/'rolls'))
            for answer in ('CONFIRMO_NIVEIS',2,'FIXO',{'INT':2},{'FOR':3,'CON':3},'CONFIRMO'):
                d.respond(answer)
            store=DurableStore(Path(tmp)/'state',b)
            runner=SafeLocalR17Runner(store);h=digest(store.get_all())
            self.assertEqual(runner.execute(d)['status'],'COMMITTED_LOCAL_VERIFIED')
            self.assertEqual(runner.execute(d)['status'],'NOOP_VERIFIED_IDEMPOTENT')
            self.assertEqual(runner.rollback(d)['status'],'ROLLED_BACK_VERIFIED_LOCAL')
            self.assertEqual(digest(store.get_all()),h)

if __name__=='__main__':unittest.main()
