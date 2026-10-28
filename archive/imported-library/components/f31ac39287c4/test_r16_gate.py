import copy,unittest
from r16_gate import *
from engine_r13 import make_fixture,RulePending
from r10_recovery import digest

class SilverActivationRuleTests(unittest.TestCase):
    def test_every_bronze_level_denied(self):
        for level in range(1,6):
            with self.subTest(level=level):
                self.assertFalse(access(level)['can_activate_transformation'])
                with self.assertRaises(TransformationLocked):
                    authorize_activation(level,scene_id='SIM-S1',rested=True,used_scene=False)
    def test_silver_and_higher_gate(self):
        for level in (6,7,10,11,16,21,25):
            self.assertTrue(access(level)['can_activate_transformation'])
    def test_silver_not_automatic_activation(self):
        x=authorize_activation(6,scene_id='SIM-S2',rested=None,used_scene=False,prior_activation=False)
        self.assertTrue(x['not_activated']);self.assertEqual(x['pa_payment'],'PENDING_T6B_PRIORITY')
    def test_rest_scene_evidence_missing_denied(self):
        for scene,rest,used,prior in [(None,True,False,False),('SIM-S2',False,False,True),('SIM-S2',True,True,False),('SIM-S2',None,False,True),('SIM-S2',True,None,False)]:
            with self.assertRaises(TransformationLocked):authorize_activation(6,scene_id=scene,rested=rest,used_scene=used,prior_activation=prior)
    def test_historical_bronze_status(self):
        self.assertEqual(historical_r13_audit()['R13_Bronze2_to_Bronze3'],'HISTORICAL_MATH_ONLY_NOT_PLAYABLE_FORM')
        with self.assertRaises(TransformationLocked):
            plan_prata(make_fixture(),{'target_level':3},'SIM-HIST-BRONZE')
    def test_prata_legal_snapshot(self):
        p=prata_fixture();self.assertEqual(p['NORMAL']['level'],6)
        self.assertEqual(p['NORMAL']['hp_current'],49)
        self.assertEqual(p['NORMAL']['hp_max'],80)
        self.assertEqual(p['NORMAL']['pa_max'],74)
        self.assertEqual(p['TRANSFORM']['derived']['ff'],580)
        self.assertEqual(p['TRANSFORM']['activation_state'],'INACTIVE_NO_T6B_REFRESH')
        self.assertEqual(p['TRANSFORM']['hp_bonus_current'],0)
    def test_prata_evolution_pure_planner(self):
        p=prata_fixture(); fp=digest(p)
        planned=plan_prata(p,choices_prata_single(),'SIM-R16-PURE')
        after=planned['updates'];self.assertEqual(digest(p),fp)
        self.assertEqual(after['NORMAL']['level'],7)
        self.assertEqual(after['NORMAL']['hp_max'],91)
        self.assertEqual(after['NORMAL']['hp_current'],49)
        self.assertEqual(after['NORMAL']['pa_max'],84)
        self.assertEqual(after['NORMAL']['pa_current'],42)
        self.assertEqual(after['TRANSFORM']['derived']['ff'],660)
        self.assertEqual(after['TRANSFORM']['hp_bonus_current'],0)
        self.assertNotIn('6',after['LOCKS']['milestones'])
        self.assertEqual(planned['deferred_until_actual_activation_ff_milestones'],['6'])
    def test_current_resources_cannot_refill(self):
        p=prata_fixture();ch=choices_prata_single();e=plan_prata(p,ch,'SIM-R16-NOREFILL')
        for k in ('hp_current','pa_current'):
            self.assertEqual(p['NORMAL'][k],e['updates']['NORMAL'][k])
    def test_inactive_form_does_not_grant_ff_lock(self):
        p=prata_fixture();c=choices_prata_single()
        e=plan_prata(p,c,'SIM-R16-NO-GHOST')
        self.assertNotIn('6',e['updates']['LOCKS']['milestones'])
        self.assertIn('6',e['deferred_until_actual_activation_ff_milestones'])
    def test_invalid_bap_or_source_denied(self):
        p=prata_fixture();p['TRANSFORM']['spirit']['bap']=-1
        with self.assertRaises(RulePending):plan_prata(p,choices_prata_single(),'SIM-R16-INVALID')

if __name__=='__main__':unittest.main()
