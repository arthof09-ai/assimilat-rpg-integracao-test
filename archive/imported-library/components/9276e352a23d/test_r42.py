import unittest,subprocess,sys,os,json,hashlib,copy
from pathlib import Path
from benchmark_data_r42 import CASES
from run_benchmark_r42 import dataset,compare_leave_one_out
from authority_r42 import Authority,Blocked,request_production,can_commit
ROOT=Path(__file__).resolve().parent
class R42Tests(unittest.TestCase):
 def test_12_textual_independent_pattern_labels(self):
  self.assertEqual(len(CASES),12)
  self.assertEqual(len(set(x[0] for x in CASES)),12)
 def test_no_rank_in_input_mechanics(self):
  d,_=dataset()
  for x in d:self.assertNotIn('rank_pattern_e0',x)
 def test_all_ids_opaque_not_source_names(self):
  d,_=dataset();self.assertEqual(len({x['opaque_id'] for x in d}),12)
  for x in d:self.assertEqual(len(x['opaque_id']),16)
 def test_predictions_exclude_self(self):
  d,g=dataset();p=compare_leave_one_out(d,g)
  for a,b in zip(d,p):self.assertNotEqual(a['opaque_id'],b['nearest_other_opaque_id'])
 def test_source_mechanics_integrity(self):
  d,_=dataset()
  for x in d:self.assertEqual(hashlib.sha256(x['mechanics_text'].encode()).hexdigest(),x['mechanics_sha256'])
 def test_rank_coverage_and_low_confidence(self):
  d,g=dataset();p=compare_leave_one_out(d,g)
  self.assertEqual(len(p),12)
  for row in p:self.assertIn(row['rank_predicted_by_nearest_other'],{'Bronze','Prata','Ouro','Ouro Negro','Lendário'})
 def test_production_default_red_denied(self):
  with self.assertRaisesRegex(Blocked,'RED'):can_commit(Authority(),{})
 def test_forge_green_without_fencing_denied(self):
  a=Authority(permit='GREEN',owner='CRAFT-SUCCESSOR',epoch=20,candidate_hash='abc')
  with self.assertRaisesRegex(Blocked,'FENCE'):can_commit(a,{'expected_epoch':20,'owner':'CRAFT-SUCCESSOR','contract_sha256':'abc'})
 def test_stale_epoch_denied_even_with_other_claims(self):
  a=Authority(permit='GREEN',owner='X',epoch=19,predecessor_fenced=True,c19_reconciled=True,stop_ack_or_external_enforcement=True,candidate_hash='abc')
  with self.assertRaisesRegex(Blocked,'EPOCH'):can_commit(a,{'expected_epoch':19,'owner':'X','contract_sha256':'abc'})
 def test_wrong_token_denied(self):
  a=Authority(permit='GREEN',owner='X',epoch=20,predecessor_fenced=True,c19_reconciled=True,stop_ack_or_external_enforcement=True,candidate_hash='abc')
  with self.assertRaisesRegex(Blocked,'STALE'):can_commit(a,{'expected_epoch':20,'owner':'Y','contract_sha256':'abc'})
 def test_even_local_permission_not_remote_enforced(self):
  a=Authority(permit='GREEN',owner='X',epoch=20,predecessor_fenced=True,c19_reconciled=True,stop_ack_or_external_enforcement=True,candidate_hash='abc')
  with self.assertRaisesRegex(Blocked,'UNENFORCED_EXTERNAL_NOTION_FENCE'):request_production(a,{'expected_epoch':20,'owner':'X','contract_sha256':'abc'},lambda:None)
 def test_real_r48_shadow_admission_and_quarantine(self):
  p=subprocess.run([sys.executable,str(ROOT/'r48_extension_r42.py')],text=True,capture_output=True,check=True)
  out=json.loads(p.stdout);self.assertEqual(out['order_status'],'QUARANTINE_EVIDENCE');self.assertTrue(out['synthetic_lot_stock_preserved']);self.assertFalse(out['magic_observed'])
 def test_original_r48_refuses_pingente(self):
  import sys
  sys.path.insert(0,os.environ.get('R42_R48_ORIG',str(ROOT/'parents'/'r48_original')))
  from r48_factory import IntegratedFactory,FactoryError
  from r48_fixtures import lots,order,REVIEW
  factory=IntegratedFactory.fixture_factory(lots())
  r=order('tli',4299);r['recipe_key']='LAB-CRAFT-VIGILIA-BOREAL-20261020-001'
  with self.assertRaisesRegex(FactoryError,'ONLY_TWO_EXISTING_RECIPES'):factory.process_batch('SBX-R48-BATCH-4299',[r],REVIEW)
  self.assertEqual(factory.journal,[])
if __name__=='__main__':unittest.main(verbosity=2)
