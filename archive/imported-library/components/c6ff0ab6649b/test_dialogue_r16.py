import copy,tempfile,unittest
from r16_gate import prata_fixture
from dialogue_r16 import Dialogue,DialogueHold
from durable_r14 import DurableStore,DurableController
from r10_recovery import digest

class PlayerChoiceFlowTests(unittest.TestCase):
    def make(self):return Dialogue(prata_fixture(),7,'SIM-R16-DIALOGUE-001')
    def _ready(self):
        s=self.make()
        s.respond(2);s.respond('FIXO')
        s.respond({'FOR':2});s.respond({'FOR':3,'CON':3})
        s.respond('CONFIRMO')
        return s
    def test_full_questions_and_validated_answers(self):
        s=self.make()
        self.assertIn('quantos pontos de atributos NORMAIS',s.prompt())
        self.assertEqual(s.respond(2)['status'],'MODE')
        self.assertIn('ROLAR',s.prompt())
        self.assertEqual(s.respond('FIXO')['status'],'NORMAL')
        self.assertIn('Como quer distribuir',s.prompt())
        self.assertEqual(s.respond({'FOR':2})['status'],'SPIRIT')
        self.assertIn('pontos próprios',s.prompt())
        self.assertEqual(s.respond({'FOR':3,'CON':3})['status'],'CONFIRM')
        self.assertNotIn('600 de Força Física',s.prompt())
        self.assertIn('Prévia, sem alterar',s.prompt())
        self.assertEqual(s.respond('CONFIRMO')['status'],'READY')
        self.assertEqual(s.summary()['answer_count'],5)
        self.assertEqual(s.executable_plan()['updates']['NORMAL']['level'],7)
    def test_rate_mismatch_holds_master(self):
        s=self.make();o=s.respond(3)
        self.assertEqual(o['status'],'HOLD_MESTRE')
        self.assertEqual(s.phase,'HOLD');self.assertIsNone(s.result)
        with self.assertRaises(DialogueHold):s.executable_plan()
    def test_rate_must_be_player_supplied(self):
        s=self.make()
        with self.assertRaises(DialogueHold):s.respond('2')
        self.assertEqual(s.phase,'RATE')
    def test_roll_path_holds_without_engine(self):
        s=self.make();s.respond(2)
        o=s.respond('ROLAR')
        self.assertEqual(o['status'],'HOLD_TECHNICAL')
        self.assertEqual(s.blocker,'AUDITABLE_ROLL_PROVIDER_NOT_INTEGRATED')
    def test_allocation_must_sum_exact(self):
        s=self.make();s.respond(2);s.respond('FIXO')
        with self.assertRaises(DialogueHold):s.respond({'FOR':1})
        with self.assertRaises(DialogueHold):s.respond({'FOR':1,'LUCK':1})
        self.assertEqual(s.phase,'NORMAL')
        s.respond({'FOR':2})
        with self.assertRaises(DialogueHold):s.respond({'SAB':6})
        self.assertEqual(s.phase,'SPIRIT')
    def test_inactive_form_does_not_request_ghost_ff(self):
        s=self.make();s.respond(2);s.respond('FIXO');s.respond({'FOR':2});s.respond({'FOR':3,'CON':3})
        self.assertEqual(s.phase,'CONFIRM')
        self.assertEqual(s._needed_ff(),[])
        self.assertEqual(s._preview()['deferred_until_actual_activation_ff_milestones'],['6'])
    def test_correction_goes_back(self):
        s=self.make();s.respond(2);s.respond('FIXO');s.respond({'FOR':2});s.respond({'FOR':3,'CON':3})
        s.respond('CORRIGIR')
        self.assertEqual(s.phase,'NORMAL')
        self.assertFalse(s.choices['normal_allocations'])
    def test_no_premature_confirmation(self):
        s=self.make()
        with self.assertRaises(DialogueHold):s.executable_plan()
    def test_no_master_secrets_or_ops_in_prompts(self):
        s=self.make();strs=[s.prompt()]
        s.respond(2);strs.append(s.prompt());s.respond('FIXO');strs.append(s.prompt())
        s.respond({'FOR':2});strs.append(s.prompt());s.respond({'FOR':3,'CON':3});strs.append(s.prompt())
        for msg in strs:
            for secret in ('BAP','CM-000','IBX-','NAC-','writer','lease','checksum','TAP=BAP'):
                self.assertNotIn(secret,msg)
    def test_local_commit_rollback_replay_from_dialogue(self):
        s=self._ready();p=s.executable_plan()
        with tempfile.TemporaryDirectory() as root:
            store=DurableStore(root,s.state);ctrl=DurableController(store)
            before=digest(store.get_all())
            r=ctrl.run(p)
            self.assertEqual(r['state'],'COMMITTED')
            after=digest(store.get_all());self.assertNotEqual(before,after)
            r2=ctrl.run(p)
            self.assertEqual(r2['intent_hash'],r['intent_hash'])
            self.assertEqual(digest(store.get_all()),after)
            ctrl.explicit_rollback(s.event_id)
            self.assertEqual(digest(store.get_all()),before)
            # Intentional replay is a distinct event and cannot retroactively reuse the original receipt.
            import engine_r13
            new=copy.deepcopy(p)
            new['event_id']='SIM-R16-DIALOGUE-REPLAY-002'
            out=ctrl.run(new)
            self.assertEqual(out['state'],'COMMITTED')
            self.assertEqual(store.get_all()['NORMAL']['level'],7)
    def test_multilevel_choices_per_level_and_ff_locks(self):
        s=Dialogue(prata_fixture(),8,'SIM-R16-MULTI-001')
        s.respond(2);s.respond('FIXO')
        s.respond({'FOR':2});s.respond({'FOR':3,'CON':3})
        self.assertEqual(s.phase,'NORMAL');self.assertEqual(s.cursor_level,8)
        s.respond({'DES':2});s.respond({'FOR':3,'CON':3})
        self.assertEqual(s.phase,'CONFIRM')
        s.respond('CONFIRMO')
        pp=s.executable_plan()
        self.assertEqual(len(pp['steps']),2)
        self.assertEqual(pp['updates']['NORMAL']['level'],8)
        self.assertEqual(set(pp['updates']['LOCKS']['milestones']),set(map(str,range(1,6))))
        self.assertEqual(pp['deferred_until_actual_activation_ff_milestones'],['6','7'])

if __name__=='__main__':unittest.main()

class NewlyReachedNormalFFMilestoneTests(unittest.TestCase):
    @staticmethod
    def fixture_lendario_near_600():
        """Fictional 21st level Human at 580 genuine FF; next +2 FOR reaches 600."""
        import copy
        from r16_gate import prata_fixture
        from engine_r13 import _derived_normal,_derived_transform,ATTRS
        p=prata_fixture();n,t,lk=p['NORMAL'],p['TRANSFORM'],p['LOCKS']
        n['level']=21
        n['initial_attrs']=dict(zip(ATTRS,[6,6,6,2,2,3]))
        n['attrs']=dict(zip(ATTRS,[24,17,17,2,2,3]))
        n['hp_initial']=16;n['pa_initial']=12
        n['hp_natural']=16+21*(12+17)
        n['pa_natural']=12+21*(12+2)
        n['hp_current']=400;n['pa_current']=100
        n['pa_committed']=10
        t['effective_level']=21;t['spirit']['cap']=25;t['spirit']['bap']=0
        t['overlay']={k:0 for k in ATTRS};t['attrs']=copy.deepcopy(n['attrs'])
        t['tap_carry_half_units']=0
        t['hp_theoretical_natural']=16+21*(18+17)
        t['pa_theoretical_natural']=12+21*(18+2)
        t['hp_bonus_current']=0;t['pa_bonus_current']=0
        lk['history'].append('fictional actual FF 100..500 awarded in earlier valid form')
        _derived_normal(n,lk['milestones']);_derived_transform(n,t,lk['milestones'])
        return p

    def test_real_new_ff_prompt_and_one_time_lock(self):
        p=self.fixture_lendario_near_600()
        d=Dialogue(p,22,'SIM-R16-LENDARIO-FF')
        d.respond(2);d.respond('FIXO');x=d.respond({'FOR':2})
        self.assertEqual(x['status'],'FF')
        self.assertIn('600 de Força Física',d.prompt())
        with self.assertRaises(DialogueHold):d.respond({'type':'CA','rolls':[3]})
        with self.assertRaises(DialogueHold):d.respond({'type':'CA','rolls':[8],'source':'SIMULATED_DICE_ONLY'})
        self.assertEqual(d.respond({'type':'CA','rolls':[3],'source':'SIMULATED_DICE_ONLY'})['status'],'CONFIRM')
        d.respond('CONFIRMO')
        e=d.executable_plan()
        self.assertIn('6',e['updates']['LOCKS']['milestones'])
        self.assertEqual(e['updates']['LOCKS']['milestones']['6']['rolls'],[3])
        self.assertEqual(e['deferred_until_actual_activation_ff_milestones'],[])
