import copy,tempfile,unittest
from engine_r17 import bronze5_fixture,lendario_ff_fixture,plan_r17,validate_r17,R17Hold,dice_contracts
from r16_gate import prata_fixture,plan_prata,access,authorize_activation,TransformationLocked
from roll_ledger_r17 import RollLedger
from r10_recovery import digest,Conflict
from durable_r14 import DurableStore,DurableController
from engine_r13 import ATTRS,FIXED,_derived_normal,_derived_transform


def choices(level,lvlist,mode='FIXO'):
    return {'target_level':level,'normal_allocations':{str(k):{'FOR':2} for k in lvlist},
            'spirit_allocations':{str(k):{'FOR':3,'CON':3} for k in lvlist},
            'milestones':{},'resource_modes':{q:mode for q in ('NORMAL_HP','NORMAL_PA','TRANSFORM_HP','TRANSFORM_PA')},
            'roll_receipts':{},'conditionals':{},'actor':'SIMULATED_TEST_AGENT','approval':'OFFLINE_SYNTHETIC_ONLY'}


def auto_draw(state,opts,event,ledger):
    for s in dice_contracts(state,opts):
        if opts['resource_modes'][s['component']]=='ROLAR':
            rid=f'{event}_{s["purpose"]}'
            opts['roll_receipts'][rid]=ledger.draw(rid,event,s['purpose'],s['sides'],s['count'])[1]
    return opts

class R17EngineTest(unittest.TestCase):
    def test_fixed_silver_exact_mechanical_parity_r16(self):
        before=prata_fixture();c=choices(7,[7]);event='SIM-R17-PARITY'
        p=plan_r17(before,c,event)
        old=plan_prata(before,{'target_level':7,'normal_allocations':c['normal_allocations'],
            'spirit_allocations':c['spirit_allocations'],'milestones':{},'resource_choice':'60_PERCENT_FIXED',
            'actor':'SIMULATED_TEST_AGENT','approval':'OFFLINE_SYNTHETIC_ONLY'},event)
        for section in ('NORMAL','TRANSFORM'):
            for k in ('attrs','hp_max' if section=='NORMAL' else 'hp_bonus_max',
                      'pa_max' if section=='NORMAL' else 'pa_bonus_max','derived'):
                self.assertEqual(p['updates'][section][k],old['updates'][section][k])
        self.assertEqual(p['deferred_spirit_milestones'],['6'])
    def test_silver_rolled_resources_and_replay(self):
        b=prata_fixture();c=choices(7,[7],'ROLAR')
        with tempfile.TemporaryDirectory() as t:
            auto_draw(b,c,'SIM-R17-ROLL',RollLedger(t+'/r'))
            p=plan_r17(b,c,'SIM-R17-ROLL')
            growth=p['steps'][0]['growth']
            self.assertEqual(len(p['roll_receipt_hashes']),4)
            self.assertEqual(p['updates']['NORMAL']['hp_natural'],b['NORMAL']['hp_natural']+growth['NORMAL_HP']['sum']+b['NORMAL']['attrs']['CON'])
            store=DurableStore(t+'/store',b);ctrl=DurableController(store)
            before=digest(store.get_all());r=ctrl.run(p)
            self.assertEqual(r['state'],'COMMITTED');after=digest(store.get_all())
            self.assertNotEqual(before,after)
            self.assertEqual(ctrl.run(p)['intent_hash'],r['intent_hash'])
            self.assertEqual(digest(store.get_all()),after)
            ctrl.explicit_rollback('SIM-R17-ROLL')
            self.assertEqual(digest(store.get_all()),before)
            rr=ctrl.run({**p,'event_id':'SIM-R17-ROLL-REPLAY'})
            self.assertEqual(rr['state'],'COMMITTED')
    def test_bronze_fixture_is_not_activated(self):
        s=bronze5_fixture()
        self.assertEqual(s['TRANSFORM']['activation_state'],'INACTIVE_NEVER_LEGAL_BRONZE')
        self.assertEqual(set(s['LOCKS']['milestones']),{'1','2'})
        self.assertFalse(access(5)['can_activate_transformation'])
        with self.assertRaises(TransformationLocked):authorize_activation(5,scene_id='X',rested=True,used_scene=False)
    def test_bronze_to_silver_fixed_rebases_every_level(self):
        b=bronze5_fixture();p=plan_r17(b,choices(6,[6]),'SIM-R17-CROSS')
        self.assertEqual(p['steps'][0]['growth']['NORMAL_HP']['dice'],'6d8')
        self.assertEqual(p['steps'][0]['growth']['TRANSFORM_HP']['dice'],'6d10')
        self.assertTrue(p['steps'][0]['rank_rebase'])
        self.assertFalse(p['steps'][0]['legal_transform_activation'])
        self.assertTrue(p['steps'][0]['activation_eligible_after_level'])
        self.assertEqual(p['updates']['TRANSFORM']['activation_state'],'INACTIVE_NO_T6B_REFRESH')
        self.assertEqual(p['updates']['NORMAL']['hp_natural'],14+6*5+6*6)
        self.assertEqual(p['updates']['NORMAL']['hp_current'],39)
        self.assertEqual(p['updates']['NORMAL']['pa_current'],32)
        self.assertEqual(set(p['updates']['LOCKS']['milestones']),{'1','2'})
    def test_bronze_to_silver_rolled_full_rebase(self):
        b=bronze5_fixture();c=choices(6,[6],'ROLAR')
        with tempfile.TemporaryDirectory() as t:
            auto_draw(b,c,'SIM-R17-CROSS-ROLL',RollLedger(t))
            p=plan_r17(b,c,'SIM-R17-CROSS-ROLL')
            hp=p['steps'][0]['growth']['NORMAL_HP']['sum']
            self.assertEqual(p['updates']['NORMAL']['hp_natural'],14+hp+6*6)
            self.assertEqual(len(p['roll_receipt_hashes']),4)
            self.assertEqual(len(c['roll_receipts']['SIM-R17-CROSS-ROLL_LV06_NORMAL_HP']['rolls']),6)
    def test_bronze5_to_silver2_multilevel(self):
        b=bronze5_fixture();p=plan_r17(b,choices(7,[6,7]),'SIM-R17-MULTI-CROSS')
        self.assertEqual(len(p['steps']),2);self.assertEqual(p['steps'][0]['growth']['NORMAL_HP']['dice'],'6d8')
        self.assertEqual(p['steps'][1]['growth']['NORMAL_HP']['dice'],'1d8')
        self.assertEqual(p['steps'][1]['growth']['TRANSFORM_HP']['dice'],'1d10')
        self.assertEqual(p['updates']['NORMAL']['level'],7)
        self.assertEqual(set(p['updates']['LOCKS']['milestones']),{'1','2'})
    def test_silver_multilevel_rolls_one_per_new_level(self):
        b=prata_fixture();c=choices(8,[7,8],'ROLAR')
        with tempfile.TemporaryDirectory() as t:
            auto_draw(b,c,'SIM-R17-MULTI',RollLedger(t));p=plan_r17(b,c,'SIM-R17-MULTI')
            self.assertEqual(len(p['roll_receipt_hashes']),8)
            self.assertEqual(p['updates']['NORMAL']['level'],8)
            self.assertEqual(len({x['receipt_sha256'] for x in p['roll_receipt_hashes']}),8)
    def test_mixed_modes_two_receipts(self):
        b=prata_fixture();c=choices(7,[7]);c['resource_modes']['NORMAL_HP']='ROLAR';c['resource_modes']['TRANSFORM_HP']='ROLAR'
        with tempfile.TemporaryDirectory() as t:
            auto_draw(b,c,'SIM-R17-MIX',RollLedger(t));p=plan_r17(b,c,'SIM-R17-MIX')
            self.assertEqual(len(p['roll_receipt_hashes']),2)
            self.assertEqual(p['steps'][0]['growth']['NORMAL_PA']['sum'],5)
    def test_missing_roll_receipt_holds_without_mutation(self):
        b=prata_fixture();prior=digest(b);c=choices(7,[7],'ROLAR')
        with self.assertRaises(R17Hold):plan_r17(b,c,'SIM-R17-MISSING')
        self.assertEqual(digest(b),prior)
    def test_bad_roll_receipt_rejected(self):
        b=prata_fixture();c=choices(7,[7],'ROLAR')
        with tempfile.TemporaryDirectory() as t:
            auto_draw(b,c,'SIM-R17-BAD',RollLedger(t))
            r=c['roll_receipts']['SIM-R17-BAD_LV07_NORMAL_HP'];r['rolls']=[99]
            with self.assertRaises(Exception):plan_r17(b,c,'SIM-R17-BAD')
    def test_wrong_event_receipt_holds(self):
        b=prata_fixture();c=choices(7,[7],'ROLAR')
        with tempfile.TemporaryDirectory() as t:
            auto_draw(b,c,'SIM-R17-WRONG',RollLedger(t))
            with self.assertRaises(R17Hold):plan_r17(b,c,'SIM-R17-OTHER')
    def test_source_mode_unspecified_holds(self):
        b=prata_fixture();c=choices(7,[7]);del c['resource_modes']['NORMAL_HP']
        with self.assertRaises(R17Hold):plan_r17(b,c,'SIM-R17-NOMODE')
    def test_invalid_allocation_no_autofill(self):
        b=prata_fixture();c=choices(7,[7]);c['normal_allocations']['7']={'FOR':1}
        with self.assertRaises(R17Hold):plan_r17(b,c,'SIM-R17-UNDER')
    def test_no_real_actor(self):
        b=prata_fixture();c=choices(7,[7]);c['actor']='PLAYER'
        with self.assertRaises(R17Hold):plan_r17(b,c,'SIM-R17-NOTREAL')
    def test_bronze_1_to_5_cannot_be_promoted_as_transform(self):
        b=bronze5_fixture();c=choices(6,[6]);c['target_level']=5
        with self.assertRaises(R17Hold):plan_r17(b,c,'SIM-R17-BADBRONZE')
    def test_conditional_choice_record_only(self):
        b=prata_fixture();b['NORMAL']['choice_contracts']=[{'id':'SIM-RACE-CLASS-01','source':'SIMULATED_VERIFIED_CONTRACT',
                  'impact':'RECORD_ONLY_TEST','level':7,'label':'seleção racial fictícia','options':['A','B']}]
        c=choices(7,[7]);c['conditionals']={'SIM-RACE-CLASS-01':'B'}
        p=plan_r17(b,c,'SIM-R17-CONDITIONAL')
        self.assertEqual(p['updates']['NORMAL']['synthetic_choice_history'][0]['choice'],'B')
    def test_conditional_unknown_choice_holds(self):
        b=prata_fixture();b['NORMAL']['choice_contracts']=[{'id':'SIM-01','source':'UNVERIFIED',
                  'impact':'REAL_BONUS','level':7,'options':['A','B']}]
        c=choices(7,[7]);c['conditionals']={'SIM-01':'A'}
        with self.assertRaises(R17Hold):plan_r17(b,c,'SIM-R17-COND-HOLD')
    def test_ghost_ff_not_granted(self):
        b=prata_fixture();p=plan_r17(b,choices(7,[7]),'SIM-R17-FF-GHOST')
        self.assertEqual(set(p['updates']['LOCKS']['milestones']),set(b['LOCKS']['milestones']))
        self.assertIn('6',p['deferred_spirit_milestones'])
    def test_real_ff600_milestone_one_receipt(self):
        b=lendario_ff_fixture();c=choices(22,[22]);c['spirit_allocations']['22']={}
        ev='SIM-R17-LENDARIO-LOCK';c['milestones']['6']={'type':'CA'}
        with tempfile.TemporaryDirectory() as t:
            ledger=RollLedger(t);rid=ev+'_FF_6'
            c['roll_receipts'][rid]=ledger.draw(rid,ev,'FF_MILESTONE_006_CA',4,1)[1]
            p=plan_r17(b,c,ev)
            lock=p['updates']['LOCKS']['milestones']['6']
            self.assertEqual(lock['receipt_sha256'],c['roll_receipts'][rid]['receipt_sha256'])
            self.assertEqual(lock['rolls'],c['roll_receipts'][rid]['rolls'])
            self.assertEqual(p['updates']['NORMAL']['derived']['ff'],600)
            self.assertEqual(p['updates']['NORMAL']['derived']['ca'],
                b['NORMAL']['derived']['ca']+sum(lock['rolls']))
    def test_ff_choice_without_receipt_holds(self):
        b=lendario_ff_fixture();c=choices(22,[22]);c['spirit_allocations']['22']={}
        c['milestones']['6']={'type':'CA'}
        with self.assertRaises(R17Hold):plan_r17(b,c,'SIM-R17-NO-FF-RECEIPT')
    def test_d12_fixed_7_unmodified(self):
        self.assertEqual(FIXED[12],7)

if __name__=='__main__':unittest.main()
