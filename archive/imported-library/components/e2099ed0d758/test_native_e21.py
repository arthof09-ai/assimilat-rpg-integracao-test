"""Adversarial LAB tests: original R48 modules under two-file TEST extension.
No physical measurement; NEVER produces official item, REC-ID, PA debit or Party write.
"""
from __future__ import annotations
import copy,unittest,hashlib,json,tempfile,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))
from native_pingente_runner import build_factory,make_order,LOTS,KEY,CASE,MEASUREMENTS,RECIPE,REVIEW,PA_SHA
from r48_factory import FactoryError,FactoryCrash,digest,IntegratedFactory
from r48_fixtures import pair,order
from r48_store import DurableFactory
from r48_pa_gate import validate_envelope

class NativeE21Tests(unittest.TestCase):
 def setUp(self):self.f=build_factory()
 def do(self,row,batch='SBX-R48-BATCH-TEST-E21'):return self.f.process_batch(batch,[row],REVIEW)
 def assertNoChange(self,before):
  self.assertEqual(self.f.snapshot(),before)

 def test_01_r39_qualified_envelope(self):
  v=validate_envelope(PA_SHA)
  self.assertEqual(v['status'],'PA_R39_R27_R26_RECEIPT_CONSUMED')
  self.assertEqual(v['pa_por_ativacao'],7)
 def test_02_original_TLI_MICA_canary_after_patch(self):
  result=self.f.process_batch('SBX-R48-BATCH-TEST-TLI-MICA',pair(index=48600),REVIEW)
  self.assertEqual(result['status'],'ALL_SYNTHETIC_QA_PASS')
  self.assertEqual({x['recipe_key'] for x in result['orders']},{'SBX-TLI-R44-v1','SBX-MICA-R44-v1'})
  self.assertTrue(self.f.audit()['ok'])
 def test_03_third_recipe_is_admitted_by_R48(self):
  receipt=self.do(make_order(48601))
  self.assertEqual(receipt['orders'][0]['recipe_key'],KEY)
  self.assertEqual(receipt['orders'][0]['status'],'EXPERIMENTAL_QA_PASS')
  self.assertEqual(receipt['orders'][0]['products'][0]['status'],'SYNTHETIC_OUTPUT_ONLY')
  self.assertEqual(receipt['physical_products'],0)
 def test_04_magic_candidate_blocked_before_reservation(self):
  before=self.f.snapshot()
  with self.assertRaisesRegex(FactoryError,'MAGIC_TRANSFER_NOT_DEMONSTRATED'):
   self.do(make_order(48602,'MAGIC_TEST'))
  self.assertNoChange(before)
 def test_05_pa_insufficient_blocks_magic_before_reservation(self):
  before=self.f.snapshot();row=make_order(48603,'MAGIC_TEST');row['pa_livre_fixture']=6
  with self.assertRaisesRegex(FactoryError,'PA_LIVRE_INSUFICIENTE_TEST'):self.do(row)
  self.assertNoChange(before)
 def test_06_pa_livre_zero_structural_does_not_require_magic(self):
  row=make_order(48604);row['pa_livre_fixture']=0
  self.assertEqual(self.do(row)['orders'][0]['status'],'EXPERIMENTAL_QA_PASS')
 def test_07_pa_fake_sha_blocked_before_reservation(self):
  before=self.f.snapshot();row=make_order(48605);row['pa_envelope_sha256']='a'*64
  with self.assertRaisesRegex(FactoryError,'PA_R39_ENVELOPE_SHA_OR_SOURCE_VERSION_CHANGED'):self.do(row)
  self.assertNoChange(before)
 def test_08_pa_invalid_shape_blocked(self):
  row=make_order(48606);row['pa_envelope_sha256']='invalid'
  with self.assertRaisesRegex(FactoryError,'PINGENTE_PA_ENVELOPE_INVALID'):self.do(row)
 def test_09_pa_context_invalid_blocked(self):
  row=make_order(48607);row['pa_livre_fixture']=-1
  with self.assertRaisesRegex(FactoryError,'PA_LIVRE_FIXTURE_INVALID'):self.do(row)
 def test_10_changed_source_payload_invalidates_envelope(self):
  p=BASE/'native_lab/R48_TEST_EXTENDED/R39_PINGENTE_ENVELOPE_NATIVE.json'
  raw=p.read_bytes()
  try:
   body=json.loads(raw);body['proveniencia_fontes']['evidencias'][0]['url']='https://wrong.invalid'
   p.write_text(json.dumps(body,ensure_ascii=False,sort_keys=True))
   with self.assertRaisesRegex(FactoryError,'PA_R39_ENVELOPE_SHA_OR_SOURCE_VERSION_CHANGED'):
    self.do(make_order(48608))
  finally:p.write_bytes(raw)
 def test_11_rank_effect_change_invalidates_r39(self):
  p=BASE/'native_lab/R48_TEST_EXTENDED/R39_PINGENTE_ENVELOPE_NATIVE.json';raw=p.read_bytes()
  try:
   body=json.loads(raw);body['efeitos'][0]['rank_efeito_proposto']='Prata'
   p.write_text(json.dumps(body,ensure_ascii=False,sort_keys=True))
   with self.assertRaisesRegex(FactoryError,'PA_R39_ENVELOPE_SHA_OR_SOURCE_VERSION_CHANGED'):
    self.do(make_order(48609))
  finally:p.write_bytes(raw)
 def test_12_unknown_key_remains_rejected(self):
  row=order('tli',48610);row['recipe_key']='SBX-UNKNOWN-TEST'
  with self.assertRaisesRegex(FactoryError,'ONLY_TWO_EXISTING_RECIPES'):self.do(row)
 def test_13_wrong_case_id_rejected(self):
  row=make_order(48611);row['case_id']='ANOTHER_CASE'
  with self.assertRaisesRegex(FactoryError,'PINGENTE_CASE_OR_PHASE_INVALID'):self.do(row)
 def test_14_extra_field_in_original_schema_rejected(self):
  row=order('tli',48612);row['experimental_phase']='STRUCTURAL_TEST'
  with self.assertRaisesRegex(FactoryError,'ORDER_CONTRACT_INVALID'):self.do(row)
 def test_15_insufficient_synthetic_material_no_reservation(self):
  row=make_order(48613);self.f.core.state['lots'][LOTS[2]]['quantity']=0
  # direct mutation should be detected BEFORE preflight by original R44 audit
  with self.assertRaisesRegex(FactoryError,'FACTORY_AUDIT_FAILED_PRESTATE'):self.do(row)
 def test_16_lot_missing_rejected_by_original_r44(self):
  row=make_order(48614);row['lot_ids'][2]='SBX-UNKNOWN-LOT-999'
  row['report']['lot_ids']=row['lot_ids'] # signed payload now diverges; quarantine, no consumption
  receipt=self.do(row)
  self.assertEqual(receipt['orders'][0]['status'],'QUARANTINE_EVIDENCE')
  self.assertEqual(receipt['orders'][0]['consumed'],[])
 def test_17_missing_tool_rejected_after_valid_r47(self):
  row=make_order(48615);row['tools']=[]
  receipt=self.do(row)
  self.assertEqual(receipt['orders'][0]['status'],'REJECTED_PRECHECK')
  self.assertEqual(receipt['orders'][0]['consumed'],[])
 def test_18_invalid_signed_report_quarantined(self):
  row=make_order(48616)
  row['attestation']['report_proof']['signature_b64']='MADE_UP_NOT_CRYPTO'
  receipt=self.do(row)
  self.assertEqual(receipt['orders'][0]['status'],'QUARANTINE_EVIDENCE')
  self.assertEqual(receipt['orders'][0]['consumed'],[])
 def test_19_quality_magic_fake_does_not_promote(self):
  row=make_order(48617);row['measurements']['magic_transfer_proven']=True
  receipt=self.do(row)
  self.assertEqual(receipt['orders'][0]['status'],'QUARANTINE_EVIDENCE')
  self.assertFalse(receipt['orders'][0]['products'])
 def test_20_partial_injected_rollback(self):
  row=make_order(48618);before=self.f.snapshot()
  with self.assertRaisesRegex(FactoryCrash,'INJECTED'):
   self.f.process_batch('SBX-R48-BATCH-ROLLBACK-E21',[row],REVIEW,inject='AFTER_FIRST_ORDER_STAGED')
  self.assertNoChange(before)
 def test_21_combined_3_recipe_batch_native(self):
  rows=pair(index=48630)+[make_order(48632)]
  receipt=self.f.process_batch('SBX-R48-BATCH-THREE-INTEGRATED',rows,REVIEW)
  self.assertEqual(receipt['status'],'ALL_SYNTHETIC_QA_PASS')
  self.assertEqual(len(receipt['orders']),3)
  self.assertTrue(self.f.audit()['ok'])
  self.assertEqual(receipt['physical_products'],0)
 def test_22_no_duplicate_on_replay(self):
  row=make_order(48640)
  receipt=self.do(row,'SBX-R48-BATCH-REPLAY-E21')
  state=self.f.snapshot()
  retry=self.do(row,'SBX-R48-BATCH-REPLAY-E21')
  self.assertTrue(retry['idempotent_replay'])
  self.assertEqual(self.f.snapshot(),state)
 def test_23_cross_batch_reuse_rejected(self):
  row=make_order(48650)
  self.do(row,'SBX-R48-BATCH-E21-ONE')
  with self.assertRaisesRegex(FactoryError,'ORDER_ID_REUSED'):self.do(row,'SBX-R48-BATCH-E21-TWO')
 def test_24_magic_missing_evidence_even_if_signed_fake(self):
  row=make_order(48660,'MAGIC_TEST')
  self.assertIn('report_proof',row['attestation'])
  with self.assertRaisesRegex(FactoryError,'MAGIC_TRANSFER_NOT_DEMONSTRATED'):self.do(row)
 def test_25_durable_store_persistence(self):
  with tempfile.TemporaryDirectory(prefix='E21_DURABLE_') as d:
   store=DurableFactory(d);store.initialize(build_factory())
   before,_=store.recover();o=make_order(48670)
   first=store.commit_batch('SBX-R48-BATCH-TEST-DURABLE',[o],REVIEW)
   after,p=store.recover(expected_head=first['r48_head'])
   self.assertEqual(len(after.journal),1)
   self.assertTrue(after.audit()['ok'])
   self.assertEqual(p['sequence'],1)
   self.assertTrue(store.commit_batch('SBX-R48-BATCH-TEST-DURABLE',[o],REVIEW)['idempotent_replay'])
 def test_26_durable_orphan_fails_closed(self):
  with tempfile.TemporaryDirectory(prefix='E21_DURABLE_FAULT_') as d:
   store=DurableFactory(d);store.initialize(build_factory())
   row=make_order(48680)
   with self.assertRaises(FactoryCrash):
    store.commit_batch('SBX-R48-BATCH-ORPHAN-E21',[row],REVIEW,inject='AFTER_CHECKPOINT_BEFORE_HEAD')
   with self.assertRaisesRegex(FactoryError,'UNKNOWN_EFFECT'):
    store.recover()
 def test_27_prevent_reusing_wrong_rin_to_re(self):
  r=json.loads((BASE/'R39_PINGENTE_ENVELOPE_NATIVE.json').read_text())
  self.assertTrue(all(not z['rank_efeito_e0_comprovado'] for z in r['proveniencia_fontes']['evidencias']))
  self.assertEqual([e['rank_efeito_proposto'] for e in r['efeitos']],['Bronze','Prata'])
 def test_28_no_official_product(self):
  receipt=self.do(make_order(48690))
  self.assertEqual(receipt['official_rec_ids'],[])
  self.assertEqual(receipt['official_stock_effect'],0)
  self.assertEqual(receipt['physical_products'],0)
  self.assertIsNone(receipt['orders'][0]['official_rec_id'])

if __name__=='__main__':unittest.main()
