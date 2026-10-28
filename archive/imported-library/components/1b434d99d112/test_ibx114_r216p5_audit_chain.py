"""Audit-chain tamper, replay, phase separation and no-host-claims tests."""
from __future__ import annotations
import unittest,json,copy
from unittest.mock import patch
from ibx114_r216p5_audit_chain import *

class ReviewChain(unittest.TestCase):
 def make_open(self):return append(genesis(),'PREVIEW_ISSUED','preview-1')
 def test_01_genesis_no_approval(self):
  x=replay(genesis());self.assertEqual(x['phase'],'UNISSUED');self.assertFalse(x['transaction_authorized'])
 def test_02_normal_cancel(self):
  t=append(self.make_open(),'CANCEL_REQUESTED','cancel-1');self.assertEqual(replay(t)['phase'],'CANCELED')
 def test_03_normal_submit(self):
  t=append(self.make_open(),'SUBMIT_FOR_APPROVAL','submit-1');self.assertEqual(replay(t)['phase'],'SUBMITTED_PENDING_HUMAN')
 def test_04_no_write_after_claimed_both_receipts(self):
  t=append(self.make_open(),'SUBMIT_FOR_APPROVAL','submit-1')
  t=append(t,'PERSONAL_APPROVAL_EVIDENCE_CLAIMED','claim-1',details={'receipt':'UNVERIFIED'})
  t=append(t,'TRANSACTION_AUTHORITY_EVIDENCE_CLAIMED','claim-2',details={'receipt':'UNVERIFIED'})
  x=replay(t);self.assertFalse(x['transaction_authorized']);self.assertFalse(x['human_preview_approval_physically_verified'])
 def test_05_cannot_cancel_before_issuance(self):
  with self.assertRaises(ChainHold):append(genesis(),'CANCEL_REQUESTED','early')
 def test_06_cannot_submit_twice(self):
  t=append(self.make_open(),'SUBMIT_FOR_APPROVAL','submit');
  with self.assertRaises(ChainHold):append(t,'SUBMIT_FOR_APPROVAL','again')
 def test_07_cannot_add_after_cancel(self):
  t=append(self.make_open(),'CANCEL_REQUESTED','cancel');
  with self.assertRaises(ChainHold):append(t,'SUBMIT_FOR_APPROVAL','later')
 def test_08_recovery_reports_frozen(self):
  t=append(self.make_open(),'HOST_UNCERTAIN_RESULT_REPORTED','timeout');self.assertEqual(replay(t)['phase'],'FROZEN_HOLD')
 def test_09_no_authority_by_boolean(self):
  for k in ('write_authorized','physical_receipt_verified','cas_proven','host_transaction_success'):
   with self.subTest(k=k),self.assertRaises(ChainHold):append(self.make_open(),'SUBMIT_FOR_APPROVAL','fraud',details={k:True})
 def test_10_subject_immutable(self):
  with self.assertRaises(ChainHold):append(self.make_open(),'SUBMIT_FOR_APPROVAL','bad',details={'source_version':'madeup'})
 def test_11_reject_duplicate_id(self):
  with self.assertRaises(ChainHold):append(self.make_open(),'SUBMIT_FOR_APPROVAL','preview-1')
 def test_12_stable_digest(self):
  x=self.make_open();self.assertEqual(x,append(genesis(),'PREVIEW_ISSUED','preview-1'))
 def test_13_copy_immutable(self):
  x=self.make_open();y=append(x,'SUBMIT_FOR_APPROVAL','submit');self.assertEqual(len(x['events']),1);self.assertEqual(len(y['events']),2)
 def test_14_nonfinite_denied(self):
  with self.assertRaises(ValueError):append(self.make_open(),'SUBMIT_FOR_APPROVAL','nan',details={'x':float('nan')})
 def test_15_actor_scope_gated(self):
  with self.assertRaises(ChainHold):genesis(ReviewSubject(owner_route='PARTY'))
 def test_16_wrong_preview_hash_gated(self):
  with self.assertRaises(ChainHold):genesis(ReviewSubject(semantic_sha256='f'*64))
 def test_17_cancel_and_submission_disjoint(self):
  p=self.make_open();a=append(p,'CANCEL_REQUESTED','c');b=append(p,'SUBMIT_FOR_APPROVAL','s')
  self.assertNotEqual(replay(a)['chain_tip_sha256'],replay(b)['chain_tip_sha256'])
 def test_18_dispatched_always_zero(self):self.assertEqual(demo_readonly()['submitted']['host_transactions_dispatched'],0)
 def test_19_generator_drift_blocks_genesis(self):
  with patch('ibx114_r214_selected_preview.generate',return_value={'preview_id':PREVIEW_ID,'sha256_payload_semantic':'0'*64}):
   with self.assertRaises(ChainHold):genesis()
 def test_20_generator_forged_approval_blocks_genesis(self):
  from ibx114_r214_selected_preview import generate
  p=generate();p['authorization']['preview_approved']=True
  with patch('ibx114_r214_selected_preview.generate',return_value=p):
   with self.assertRaises(ChainHold):genesis()

def tamper_case(which):
 def test(self):
  t=append(self.make_open(),'SUBMIT_FOR_APPROVAL','submit',details={'note':'x'})
  t=copy.deepcopy(t)
  if which=='event_type':t['events'][-1]['type']='CANCEL_REQUESTED'
  if which=='payload':t['events'][-1]['payload']['note']='y'
  if which=='sequence':t['events'][-1]['seq']=42
  if which=='prior':t['events'][-1]['prior_sha256']='0'*64
  if which=='hash':t['events'][-1]['entry_sha256']='f'*64
  if which=='remove_issuance':t['events']=t['events'][1:]
  if which=='genesis':t['genesis_hash']='bad'
  if which=='page':t['base']['source_page']='different'
  if which=='new_field':t['events'][-1]['fake']='yes'
  if which=='source_version':t['events'][-1]['payload']['source_version']='stale'
  with self.assertRaises(ChainHold):replay(t)
 return test
for i,name in enumerate(('event_type','payload','sequence','prior','hash','remove_issuance','genesis','page','new_field','source_version'),1):
 setattr(ReviewChain,f'test_tamper_{i:02d}_{name}',tamper_case(name))
if __name__=='__main__':unittest.main()
