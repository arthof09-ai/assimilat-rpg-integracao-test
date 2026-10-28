import copy
import unittest
from ibx17_r41_item_provenance import EvidenceHold
from ibx17_r42_preview_bridge import *

SRC={'page_id':'a'*32,'surface':'MESTRE_TEST','source_sha256':'sha-original','captured_at':'2026-10-16T11:30:00Z','original_page_url':'https://app.notion.com/p/'+'a'*32}
ENG={'engine_name':'R17-original-injected-test-stub','version':'fixture-1','source_sha256':'hash-fixture','rule_ref':'SCOPED_SYNTHETIC_TEST_NOT_CANONICAL'}
IMPACT={k:{'status':'ALTERA' if k=='atributos_naturais' else 'NAO_ALTERA_VERIFICADO',
           'source_ref':'synthetic-test-contract','explanation':'isolated fixture, no RPG rule asserted'} for k in REQUIRED_DOMAINS}
BASE={'level':2,'FOR':6,'INT':4,'PA':20,'inventory':['ring-a']}
def level_fn(before, change, receipt):
    after=copy.deepcopy(before); after['level']+=1;after['FOR']+=1;return after

def down_fn(before,change,receipt):
    after=copy.deepcopy(before);after['FOR']-=1;return after

class Preview(unittest.TestCase):
    def mk(self,fn=level_fn,action=LEVEL_UP):return preview(source=SRC,before=BASE,change={'action':action},impact=IMPACT,historical_engine=fn,engine_receipt=ENG)
    def test_01_preview(self):self.assertEqual(self.mk()['status'],'PREVIEW_ONLY_REVIEW_REQUIRED')
    def test_02_no_mutation(self):b=copy.deepcopy(BASE);self.mk();self.assertEqual(BASE,b)
    def test_03_level(self):self.assertEqual(self.mk()['after']['level'],3)
    def test_04_delta(self):self.assertEqual(set(self.mk()['field_deltas']),{'level','FOR'})
    def test_05_inventory_preserved(self):self.assertEqual(self.mk()['after']['inventory'],['ring-a'])
    def test_06_down_no_level_loss(self):self.assertEqual(self.mk(down_fn,LEVEL_DOWN)['after']['level'],2)
    def test_07_down_change(self):self.assertEqual(self.mk(down_fn,LEVEL_DOWN)['after']['FOR'],5)
    def test_08_down_loses_level_blocked(self):
        with self.assertRaisesRegex(EvidenceHold,'LEVEL_DOWN_CANNOT_LOSE_LEVEL'):
            self.mk(lambda before,change,receipt:{**before,'level':1},LEVEL_DOWN)
    def test_09_broken_up_blocked(self):
        with self.assertRaisesRegex(EvidenceHold,'LEVEL_UP_NOT_EXACTLY_ONE_LEVEL'):
            self.mk(lambda before,change,receipt:{**before,'level':4})
    def test_10_no_op_blocked(self):
        with self.assertRaisesRegex(EvidenceHold,'LEVEL_UP_NOT_EXACTLY_ONE_LEVEL'):self.mk(lambda b,c,r:b)
    def test_11_new_fields_blocked(self):
        with self.assertRaisesRegex(EvidenceHold,'UNDECLARED_FIELDS'):self.mk(lambda b,c,r:{**b,'unexpected':10})
    def test_12_missing_fields_blocked(self):
        with self.assertRaises(EvidenceHold):self.mk(lambda b,c,r:{'level':3})
    def test_13_missing_engine_blocked(self):
        with self.assertRaisesRegex(EvidenceHold,'HISTORIC_ENGINE_UNAVAILABLE'):
            preview(source=SRC,before=BASE,change={'action':LEVEL_UP},impact=IMPACT,historical_engine=None,engine_receipt=ENG)
    def test_14_missing_receipt(self):
        with self.assertRaisesRegex(EvidenceHold,'HISTORIC_ENGINE_RECEIPT'):
            preview(source=SRC,before=BASE,change={'action':LEVEL_UP},impact=IMPACT,historical_engine=level_fn,engine_receipt={})
    def test_15_missing_source(self):
        with self.assertRaisesRegex(EvidenceHold,'SOURCE_RECEIPT'):
            preview(source={},before=BASE,change={'action':LEVEL_UP},impact=IMPACT,historical_engine=level_fn,engine_receipt=ENG)
    def test_16_pending_impact(self):
        d=copy.deepcopy(IMPACT);d['magias']['status']='PENDENTE'
        with self.assertRaisesRegex(EvidenceHold,'PENDING_IMPACT'):
            preview(source=SRC,before=BASE,change={'action':LEVEL_UP},impact=d,historical_engine=level_fn,engine_receipt=ENG)
    def test_17_missing_impact(self):
        d=copy.deepcopy(IMPACT);del d['magias']
        with self.assertRaisesRegex(EvidenceHold,'IMPACT_DOMAIN'):
            preview(source=SRC,before=BASE,change={'action':LEVEL_UP},impact=d,historical_engine=level_fn,engine_receipt=ENG)
    def test_18_refusal(self):self.assertEqual(approval_decision(self.mk(),approved=False,authorized_scope='MESTRE_TEST',current_source_sha256='sha-original'),'REFUSED_NO_WRITE')
    def test_19_test_approved(self):self.assertEqual(approval_decision(self.mk(),approved=True,authorized_scope='MESTRE_TEST',current_source_sha256='sha-original'),'TEST_APPROVAL_ELIGIBLE_FOR_NATIVE_GATE')
    def test_20_drift(self):self.assertEqual(approval_decision(self.mk(),approved=True,authorized_scope='MESTRE_TEST',current_source_sha256='other'),'HOLD_SOURCE_DRIFT')
    def test_21_official_hold(self):self.assertEqual(approval_decision(self.mk(),approved=True,authorized_scope='MESTRE_MIRROR_READ_ONLY',current_source_sha256='sha-original'),'HOLD_OFFICIAL_APPROVAL_AND_NAC_PASS_MISSING')
    def test_22_tamper(self):
        p=self.mk();p['field_deltas']['FOR']['after']=999
        self.assertEqual(approval_decision(p,approved=True,authorized_scope='MESTRE_TEST',current_source_sha256='sha-original'),'HOLD_PREVIEW_TAMPERED')
    def test_23_replay_noop(self):p=self.mk();self.assertEqual(replay_plan(p,observed_after_sha256=p['postimage_sha256']),'NOOP_ALREADY_APPLIED')
    def test_24_replay_hold(self):self.assertEqual(replay_plan(self.mk(),observed_after_sha256='mismatch'),'HOLD_UNKNOWN_EFFECT_REOPEN_SOURCE')
    def test_25_replay_reapprove(self):p=self.mk();self.assertEqual(replay_plan(p,observed_before_sha256=p['preimage_sha256']),'PREVIEW_REAPPROVAL_AND_LIVE_SOURCE_REQUIRED')
    def test_26_no_writes(self):self.assertEqual(self.mk()['notion_writes'],0)

if __name__=='__main__':unittest.main()
