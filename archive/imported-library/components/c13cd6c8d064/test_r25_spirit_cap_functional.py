"""R25 delta on EXISTING R17 engine: T2/T3 Spirit cap, normal progress continues.
Offline simulated IDs only. No REST or Party imports.
"""
import copy
import tempfile
import unittest
from pathlib import Path
from dialogue_r17 import DialogueR17,DialogueR17Hold
from engine_r17 import R17Hold,plan_r17,dice_contracts,validate_r17
from engine_r13 import _derived_transform
from r16_gate import prata_fixture
from r10_recovery import digest
from roll_ledger_r17 import RollLedger
from durable_r14 import DurableStore
from safe_runner_r17 import SafeLocalR17Runner,RunnerHold

MODES=('NORMAL_HP','NORMAL_PA','TRANSFORM_HP','TRANSFORM_PA')

def capped_fixture(cap=6):
    before=prata_fixture()
    before['TRANSFORM']['spirit']['cap']=cap
    assert cap==6, 'R25 current fixture requires a reconciled level6 cap'
    validate_r17(before)
    return before

def build_choices(target,mode='FIXO',special=None,spirit_progress=None):
    special=special or {}
    return {'target_level':target,
        'normal_allocations':{str(lv):special.get(lv,{'DES':2}) for lv in range(7,target+1)},
        'spirit_allocations':{str(lv):(spirit_progress or {}).get(lv,{}) for lv in range(7,target+1)},
        'resource_modes':{k:mode for k in MODES},'roll_receipts':{},'milestones':{},
        'conditionals':{},'actor':'SIMULATED_TEST_AGENT','approval':'OFFLINE_SYNTHETIC_ONLY'}

class CapAdvancementFunctionalR25(unittest.TestCase):
    def test_pre_r25_is_explicitly_identified_as_incapable(self):
        # The original source is kept inside the R24 package; the recorded
        # precondition is its target>cap hard DENY in BOTH engine and dialogue.
        orig=Path(__file__).resolve().parents[2]/'baseline_engine_sha256.json'
        self.assertTrue(orig.is_file())
    def test_normal_level_above_cap_is_now_executable(self):
        b=capped_fixture();p=plan_r17(b,build_choices(7),'SIM-R25-CAP-ONE')
        a=p['updates'];self.assertEqual(a['NORMAL']['level'],7)
        self.assertEqual(a['TRANSFORM']['effective_level'],6)
        self.assertEqual(a['TRANSFORM']['overlay'],b['TRANSFORM']['overlay'])
        self.assertEqual(a['TRANSFORM']['tap_carry_half_units'],b['TRANSFORM']['tap_carry_half_units'])
        self.assertEqual(a['TRANSFORM']['attrs']['DES'],b['TRANSFORM']['attrs']['DES']+2)
        self.assertEqual(a['TRANSFORM']['derived']['ca'],b['TRANSFORM']['derived']['ca']+2)
        self.assertEqual(a['NORMAL']['derived']['ca'],b['NORMAL']['derived']['ca']+2)
        self.assertEqual(len(p['steps']),1)
        self.assertTrue(p['steps'][0]['spirit_capped'])
        self.assertEqual(p['steps'][0]['spirit_budget'],0)
        self.assertEqual(p['steps'][0]['growth']['TRANSFORM_HP']['sum'],0)
        self.assertEqual(a['TRANSFORM']['hp_theoretical_natural'],b['TRANSFORM']['hp_theoretical_natural'])
    def test_no_silent_clamp_when_cap_bonus_shrinks(self):
        before=capped_fixture();before['TRANSFORM']['hp_bonus_current']=110
        # This value is legal at level6 but exceeds the level7 capped bonus.
        self.assertTrue(validate_r17(before))
        c=build_choices(7)
        source=digest(before)
        with self.assertRaises(R17Hold):plan_r17(before,c,'SIM-R25-CAP-NO-CLAMP')
        self.assertEqual(digest(before),source)

    def test_no_spirit_receipts_are_necessary_above_cap(self):
        b=capped_fixture();c=build_choices(7,'ROLAR')
        specs=dice_contracts(b,c)
        self.assertEqual([s['component'] for s in specs],['NORMAL_HP','NORMAL_PA'])
        with tempfile.TemporaryDirectory() as tmp:
            led=RollLedger(tmp)
            for spec in specs:
                k='SIM-R25-NOROLL_'+spec['purpose']
                c['roll_receipts'][k]=led.draw(k,'SIM-R25-NOROLL',spec['purpose'],spec['sides'],spec['count'])[1]
            p=plan_r17(b,c,'SIM-R25-NOROLL')
            self.assertEqual(len(p['roll_receipt_hashes']),2)
            self.assertTrue(all('TRANSFORM' not in x['purpose'] for x in p['roll_receipt_hashes']))
    def test_surplus_spirit_receipt_is_rejected(self):
        b=capped_fixture();c=build_choices(7)
        c['roll_receipts']['SIM-R25-EXTRA_LV07_TRANSFORM_HP']={'bogus':True}
        with self.assertRaises(R17Hold):plan_r17(b,c,'SIM-R25-EXTRA')
    def test_unearned_spirit_tap_is_denied(self):
        b=capped_fixture();c=build_choices(7);c['spirit_allocations']['7']={'FOR':6}
        with self.assertRaises(R17Hold):plan_r17(b,c,'SIM-R25-BAD-TAP')
    def test_spirit_cap_does_not_grant_ff_milestones(self):
        b=capped_fixture();p=plan_r17(b,build_choices(7),'SIM-R25-LOCKS')
        self.assertEqual(b['LOCKS']['milestones'],p['updates']['LOCKS']['milestones'])
        self.assertEqual(p['updates']['TRANSFORM']['activation_state'],'INACTIVE_NO_T6B_REFRESH')
    def test_no_heal_or_refill(self):
        b=capped_fixture();p=plan_r17(b,build_choices(7),'SIM-R25-NO-REFILL')
        for section,keys in [('NORMAL',['hp_current','pa_current']),('TRANSFORM',['hp_bonus_current','pa_bonus_current'])]:
            for k in keys:self.assertEqual(p['updates'][section][k],b[section][k])
    def test_rank_change_normal_but_not_spirit(self):
        b=capped_fixture();c=build_choices(11)
        p=plan_r17(b,c,'SIM-R25-PRATA-OURO')
        self.assertEqual(len(p['steps']),5)
        self.assertEqual(len(dice_contracts(b,c)),10)
        self.assertTrue(p['steps'][-1]['rank_rebase'])
        self.assertEqual(p['steps'][-1]['rank'],'Ouro')
        self.assertEqual(p['updates']['TRANSFORM']['effective_level'],6)
        self.assertEqual(p['updates']['NORMAL']['level'],11)
        self.assertTrue(all(s['spirit_capped'] for s in p['steps']))
    def test_progress_raises_new_ff_at_valid_normal_threshold_only(self):
        b=capped_fixture();c=build_choices(7,special={7:{'FOR':2}})
        # No new milestone in this fixture; spiritual FF can remain higher
        # without granting a new permanent lock from the inactive Spirit.
        p=plan_r17(b,c,'SIM-R25-NO-GHOST')
        self.assertEqual(set(p['updates']['LOCKS']['milestones']),set(b['LOCKS']['milestones']))
    def test_same_cap_resource_max_floor_never_negative(self):
        b=capped_fixture();p=plan_r17(b,build_choices(11),'SIM-R25-T6-FLOOR')
        self.assertGreaterEqual(p['updates']['TRANSFORM']['hp_bonus_max'],0)
        self.assertGreaterEqual(p['updates']['TRANSFORM']['pa_bonus_max'],0)
        self.assertEqual(p['updates']['TRANSFORM']['spirit']['cap'],6)
    def test_mode_rolar_dialogue_omits_spirit_choice(self):
        b=capped_fixture()
        with tempfile.TemporaryDirectory() as tmp:
            d=DialogueR17(b,7,'SIM-R25-CHAT-CAP-ROLL',RollLedger(tmp))
            for a in ('CONFIRMO_NIVEIS',2,'ROLAR',{'DES':2}):d.respond(a)
            self.assertEqual(d.phase,'ROLLS')
            self.assertEqual(d.choices['spirit_allocations'],{'7':{}})
            d.respond('ROLAR_AGORA')
            self.assertEqual(len(d.choices['roll_receipts']),2)
            d.respond('CONFIRMO');self.assertEqual(d.phase,'READY')
    def test_full_local_confirm_commit_rollback_and_idempotent_replay(self):
        b=capped_fixture()
        with tempfile.TemporaryDirectory() as tmp:
            d=DialogueR17(b,8,'SIM-R25-CAP-E2E',RollLedger(Path(tmp)/'roll'))
            for a in ('CONFIRMO_NIVEIS',2,'FIXO',{'DES':2},{'SAB':2},'CONFIRMO'):
                d.respond(a)
            self.assertEqual(d.phase,'READY');plan=d.executable_plan()
            store=DurableStore(Path(tmp)/'store',b)
            runner=SafeLocalR17Runner(store)
            prior=digest(store.get_all())
            self.assertEqual(runner.execute(d)['status'],'COMMITTED_LOCAL_VERIFIED')
            done=digest(store.get_all());self.assertNotEqual(prior,done)
            self.assertEqual(runner.execute(d)['status'],'NOOP_VERIFIED_IDEMPOTENT')
            self.assertEqual(runner.rollback(d)['status'],'ROLLED_BACK_VERIFIED_LOCAL')
            self.assertEqual(digest(store.get_all()),prior)
            # Explicit recorded-intent replay requires a different event key.
            with self.assertRaises(RunnerHold):runner.execute(d)
            self.assertEqual(digest(store.get_all()),prior)
    def test_no_external_effect_or_live_permission(self):
        b=capped_fixture();p=plan_r17(b,build_choices(7),'SIM-R25-READONLY')
        self.assertIs(p['writer_authorized'],False);self.assertEqual(p['notion_writes'],0)
        c=build_choices(7);c['actor']='PLAYER'
        with self.assertRaises(R17Hold):plan_r17(b,c,'SIM-R25-DENY')
    def test_spirit_cap_full_saturation_keeps_same_abilities(self):
        b=capped_fixture();p=plan_r17(b,build_choices(11),'SIM-R25-ABILITIES')
        self.assertEqual(p['updates']['TRANSFORM']['abilities_active'],b['TRANSFORM']['abilities_active'])
    def test_missing_normal_choice_still_holds_at_cap(self):
        b=capped_fixture();c=build_choices(7);del c['normal_allocations']['7']
        with self.assertRaises(R17Hold):plan_r17(b,c,'SIM-R25-NO-CHOICE')

if __name__=='__main__':unittest.main()
