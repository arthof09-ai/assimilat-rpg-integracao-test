import copy, unittest
from engine_r13 import *
from r10_recovery import RecoveryController, export_journal, import_journal

class TestR13E2E(unittest.TestCase):
    def setUp(self):self.before=make_fixture();self.choices=make_choices_single()
    def test_e2e_before_preview_after(self):
        p=plan(self.before,self.choices,'SIM-E2E-001')
        s=make_store(self.before);self.assertEqual(execute(p,s).state,'COMMITTED')
        self.assertEqual(s.pages,p['updates']);self.assertEqual(s.pages['NORMAL']['level'],3)
    def test_attributes_budget(self):
        p=plan(self.before,self.choices,'SIM-ATTR');self.assertEqual(p['updates']['NORMAL']['attrs']['FOR'],8)
        self.assertEqual(p['updates']['TRANSFORM']['overlay']['CON'],10)
    def test_resources_not_healed(self):
        p=plan(self.before,self.choices,'SIM-RES')
        self.assertEqual([p['updates']['NORMAL'][k] for k in ('hp_max','hp_current','pa_max','pa_current','pa_free','pa_spendable_now')],[32,17,30,16,27,13])
        self.assertEqual([p['updates']['TRANSFORM'][k] for k in ('hp_bonus_max','hp_bonus_current','pa_bonus_max','pa_bonus_current')],[34,12,11,8])
    def test_derived_and_ff(self):
        p=plan(self.before,self.choices,'SIM-DER');n=p['updates']['NORMAL'];t=p['updates']['TRANSFORM']
        self.assertEqual((n['derived']['ca'],n['derived']['magic_cd'],n['derived']['ff']),(15,6,180))
        self.assertEqual(t['derived']['ff'],360);self.assertEqual(t['derived']['ff_bonus_damage'],5)
    def test_ff_locks_are_persistent(self):
        p=plan(self.before,self.choices,'SIM-LOCK');old=self.before['LOCKS']['milestones'];new=p['updates']['LOCKS']['milestones']
        self.assertEqual(new['1'],old['1']);self.assertEqual(new['2'],old['2']);self.assertEqual(new['3']['rolls'],[2])
    def test_unchanged_synthetic_inventory(self):
        p=plan(self.before,self.choices,'SIM-INVENT');self.assertEqual(p['updates']['NORMAL']['untouched'],self.before['NORMAL']['untouched']);self.assertEqual(p['updates']['TRANSFORM']['untouched'],self.before['TRANSFORM']['untouched'])
    def test_preview_pure_and_detects_all_sections(self):
        frozen=digest(self.before);p=plan(self.before,self.choices,'SIM-PURE');v=preview_summary(p)
        self.assertEqual(digest(self.before),frozen);self.assertEqual(set(v['sha256']),{'NORMAL','TRANSFORM','LOCKS'});self.assertEqual(v['level'],[2,3])
    def test_restore_exact(self):
        p=plan(self.before,self.choices,'SIM-RESTORE');s=make_store(self.before);j=execute(p,s)
        self.assertEqual(rollback(s,j).state,'ROLLED_BACK_VERIFIED');self.assertEqual(s.pages,self.before)
    def test_duplicate_event_idempotent(self):
        p=plan(self.before,self.choices,'SIM-IDEMP');s=make_store(self.before)
        j=execute(p,s);versions=dict(s.versions);self.assertIs(execute(p,s),j);self.assertEqual(s.versions,versions)
    def test_replay_after_rollback_needs_new_event(self):
        p=plan(self.before,self.choices,'SIM-UNDO-ID');s=make_store(self.before);j=execute(p,s);rollback(s,j)
        self.assertEqual(execute(p,s).state,'ROLLED_BACK_VERIFIED');self.assertEqual(s.pages,self.before)
        p2=plan(s.pages,self.choices,'SIM-REDO-NEW-ID');self.assertEqual(execute(p2,s).state,'COMMITTED')
    def test_no_real_player(self):
        q=copy.deepcopy(self.choices);q['approval']='REAL';
        with self.assertRaises(RulePending):plan(self.before,q,'SIM-FAIL')
    def test_reject_missing_choice(self):
        q=copy.deepcopy(self.choices);q['normal_allocations']={}
        with self.assertRaises(RulePending):plan(self.before,q,'SIM-FAIL')
    def test_reject_excess(self):
        q=copy.deepcopy(self.choices);q['normal_allocations']['3']={'FOR':3}
        with self.assertRaises(RulePending):plan(self.before,q,'SIM-FAIL')
    def test_reject_missing_ff_choice(self):
        q=copy.deepcopy(self.choices);q['milestones']={}
        with self.assertRaises(RulePending):plan(self.before,q,'SIM-FAIL')
    def test_reject_spirit_diversion(self):
        q=copy.deepcopy(self.choices);q['spirit_allocations']['3']={'CAR':6}
        with self.assertRaises(RulePending):plan(self.before,q,'SIM-FAIL')
    def test_reject_level26(self):
        q=copy.deepcopy(self.choices);q['target_level']=26
        with self.assertRaises(RulePending):plan(self.before,q,'SIM-FAIL')
    def test_reject_stale_plan(self):
        p=plan(self.before,self.choices,'SIM-STALE');s=make_store(self.before)
        v=s.versions['NORMAL'];s.cas('NORMAL',v,{**s.pages['NORMAL'],'hp_current':10})
        with self.assertRaises(Conflict):execute(p,s)
    def test_reject_modified_fixture(self):
        q=copy.deepcopy(self.before);q['NORMAL']['fixture_only']=False
        with self.assertRaises(RulePending):plan(q,self.choices,'SIM-FAIL')
    def test_journal_export_checksum(self):
        p=plan(self.before,self.choices,'SIM-JOURNAL');j=execute(p,make_store(self.before))
        self.assertEqual(import_journal(export_journal(j)).state,'COMMITTED')
    def test_new_event_does_not_auto_choose_roll(self):
        q=copy.deepcopy(self.choices);q['milestones']['3']['rolls']=[5]
        with self.assertRaises(RulePending):plan(self.before,q,'SIM-FAIL')

class TestR14Advanced(unittest.TestCase):
    def setUp(self):self.before=make_fixture()
    def _multi(self):
        x=make_choices_single();x['target_level']=6
        x['normal_allocations']={str(i):{'FOR':2} for i in range(3,7)}
        x['spirit_allocations']={str(i):{'FOR':6} for i in range(3,6)}
        x['spirit_allocations']['6']={'INT':6}
        x['milestones']={str(i):{'type':'DANO','rolls':[i%4+1]} for i in range(3,7)}
        return x
    def test_multilevel_rank_rebase(self):
        a=copy.deepcopy(self.before);a['TRANSFORM']['spirit']['cap']=10;a['TRANSFORM']['spirit']['allowed_attrs'].append('INT')
        p=plan(a,self._multi(),'SIM-MULTI');n=p['updates']['NORMAL'];t=p['updates']['TRANSFORM']
        self.assertEqual(n['level'],6);self.assertEqual(n['hp_natural'],74);self.assertEqual(n['pa_natural'],68)
        self.assertEqual(t['effective_level'],6);self.assertEqual(len(t['abilities_active']),2)
        self.assertEqual([s['rank_rebase'] for s in p['steps']],[False,False,False,True])
    def test_spirit_cap_stops_progress(self):
        x=self._multi();x['spirit_allocations']['6']={};self.before['TRANSFORM']['pa_bonus_current']=0;p=plan(self.before,x,'SIM-CAP')
        self.assertEqual(p['updates']['TRANSFORM']['effective_level'],5)
        self.assertEqual(len(p['updates']['TRANSFORM']['abilities_active']),1)
    def test_retroactive_title_granted_once_and_then_rate(self):
        x=self._multi();x['target_level']=5;x['spirit_allocations'].pop('6');x['normal_allocations']['5']={'FOR':7}
        x['title_events']={'5':[{'id':'SYNTH-TITLE-RETRO','per_level':1,'retroactive':True,
                         'source':'SYNTHETIC_TITLE_EVENT','approved':'SYNTHETIC_EXPLICIT'}]}
        p=plan(self.before,x,'SIM-TITLE');self.assertEqual([s['normal_budget'] for s in p['steps']],[2,2,7]);self.assertEqual(p['updates']['NORMAL']['title_credits']['SYNTH-TITLE-RETRO'],5)
        y={'target_level':6,'normal_allocations':{'6':{'FOR':3}},'spirit_allocations':{'6':{}},
           'milestones':{'6':{'type':'CA','rolls':[2]}},'resource_choice':'60_PERCENT_FIXED',
           'actor':'SIMULATED_TEST_AGENT','approval':'OFFLINE_SYNTHETIC_ONLY'}
        p['updates']['TRANSFORM']['pa_bonus_current']=0  # explicitly drained in this synthetic scenario, no recovery implied
        p2=plan(p['updates'],y,'SIM-TITLE-2');self.assertEqual(p2['steps'][0]['normal_budget'],3)
    def test_title_duplicate_rejected(self):
        x=self._multi();x['target_level']=5;x['normal_allocations']['5']={'FOR':7};x['title_events']={'5':[{'id':'DUP','per_level':1,'retroactive':True,'source':'SYNTHETIC_TITLE_EVENT','approved':'SYNTHETIC_EXPLICIT'}, {'id':'DUP','per_level':1,'retroactive':True,'source':'SYNTHETIC_TITLE_EVENT','approved':'SYNTHETIC_EXPLICIT'}]}
        with self.assertRaises(RulePending):plan(self.before,x,'SIM-FAIL')
    def test_fractional_tap_carry(self):
        a=copy.deepcopy(self.before);t=a['TRANSFORM'];t['spirit']['bap']=11;t['overlay']['CON']=5;t['attrs']=addattrs(a['NORMAL']['attrs'],t['overlay']);t['hp_theoretical_natural']=44;t['hp_bonus_max']=21;t['tap_carry_half_units']=0
        p=plan(a,self._frac_choices(),'SIM-FRAC')
        self.assertEqual(p['steps'][0]['tap_budget'],5);self.assertEqual(p['updates']['TRANSFORM']['tap_carry_half_units'],1)
        self.assertEqual(sumattrs(p['updates']['TRANSFORM']['overlay']),16)
    def _frac_choices(self):
        x=make_choices_single();x['spirit_allocations']['3']={'FOR':5};return x
    def test_fractional_tap_second_level_6(self):
        a=copy.deepcopy(self.before);t=a['TRANSFORM'];t['spirit']['bap']=11;t['overlay']['CON']=5;t['attrs']=addattrs(a['NORMAL']['attrs'],t['overlay']);t['hp_theoretical_natural']=44;t['hp_bonus_max']=21;t['tap_carry_half_units']=0
        x=self._frac_choices();x['target_level']=4;x['normal_allocations']['4']={'FOR':2};x['spirit_allocations']['4']={'FOR':6};x['milestones']['4']={'type':'DANO','rolls':[3]}
        p=plan(a,x,'SIM-FRAC2');self.assertEqual([z['tap_budget'] for z in p['steps']],[5,6]);self.assertEqual(p['updates']['TRANSFORM']['tap_carry_half_units'],0)
    def test_crash_recovery_all_boundaries(self):
        p=plan(self.before,make_choices_single(),'SIM-FAULT')
        boundaries=['BEFORE_PREFLIGHT','AFTER_PREFLIGHT','BEFORE_WRITE:NORMAL','AFTER_WRITE:NORMAL','AFTER_READBACK:NORMAL',
                    'BEFORE_WRITE:TRANSFORM','AFTER_WRITE:TRANSFORM','AFTER_READBACK:TRANSFORM',
                    'BEFORE_WRITE:LOCKS','AFTER_WRITE:LOCKS','AFTER_READBACK:LOCKS','AFTER_COMMIT']
        for name in boundaries:
            with self.subTest(name=name):
                s=make_store(self.before);j=execute(p,s,crash_at=name)
                self.assertEqual(j.state,'UNKNOWN_EFFECT')
                after=rollback(s,j)
                if name.startswith('AFTER_WRITE:'):
                    # write could land before journal acknowledged; conservative HOLD is correct.
                    self.assertIn(after.state,('ROLLED_BACK_VERIFIED','HOLD_CONCURRENT_CONFLICT'))
                else:self.assertIn(after.state,('ROLLED_BACK_VERIFIED','NOT_APPLIED','HOLD_CONCURRENT_CONFLICT'))
    def test_journal_mismatch_aborts(self):
        p=plan(self.before,make_choices_single(),'SIM-COLLIDE');s=make_store(self.before)
        j=execute(p,s);q=copy.deepcopy(p);q['updates']['NORMAL']['attrs']['FOR']+=1
        with self.assertRaises(Conflict):execute(q,s)
    def test_concurrent_modified_page_hold(self):
        p=plan(self.before,make_choices_single(),'SIM-CONCURRENT');s=make_store(self.before)
        j=execute(p,s,crash_at='AFTER_READBACK:NORMAL');s.cas('NORMAL',s.versions['NORMAL'],{**s.pages['NORMAL'],'hp_current':10})
        self.assertEqual(rollback(s,j).state,'HOLD_CONCURRENT_CONFLICT')
    def test_aba_version_change_hold(self):
        p=plan(self.before,make_choices_single(),'SIM-ABA');s=make_store(self.before)
        j=execute(p,s,crash_at='AFTER_READBACK:NORMAL');v=s.versions['NORMAL'];s.cas('NORMAL',v,self.before['NORMAL']);s.cas('NORMAL',v+1,p['updates']['NORMAL'])
        self.assertEqual(rollback(s,j).state,'HOLD_CONCURRENT_CONFLICT')
    def test_undo_concurrent_protection(self):
        p=plan(self.before,make_choices_single(),'SIM-UNDO-CONFLICT');s=make_store(self.before);j=execute(p,s)
        s.cas('LOCKS',s.versions['LOCKS'],{**s.pages['LOCKS'],'history':['CHANGED']})
        with self.assertRaises(Conflict):rollback(s,j)
    def test_replay_must_not_grant_duplicate_title(self):
        x=self._multi();x['target_level']=5;x['normal_allocations']['5']={'FOR':7};x['title_events']={'5':[{'id':'T','per_level':1,'retroactive':True,'source':'SYNTHETIC_TITLE_EVENT','approved':'SYNTHETIC_EXPLICIT'}]}
        p=plan(self.before,x,'SIM-TITLE-IDEMP');s=make_store(self.before);j=execute(p,s);prior=digest(s.pages)
        self.assertIs(execute(p,s),j);self.assertEqual(digest(s.pages),prior)

if __name__=='__main__':unittest.main()
