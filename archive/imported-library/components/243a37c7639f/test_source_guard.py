import unittest, copy, hashlib
from craft_p2_source_guard import evaluate,P2_BOM,ENERGY_OPTIONS,OIL_OFFICIAL_BOM,OIL_HIST_IRON

SHA='a'*64

def lot(q,finished=False):
 d={'lot_id':'SYNTHETIC-LAB','custody':'synthetic','authenticity_sha256':SHA,'provenance_ref':'fixture','quantity':q}
 if finished:d.update({'quality_ref':'synthetic QA fixture','product_identity':'Óleo de Vedação'})
 return d

def complete(route='FINISHED_LOT'):
 return {
  'salt_decision':{'choice':'SANTO','authority_decision_id':'TEST-FAKE','authority_ref':'no real proof'},
  'energy_decision':{'choice':'Pedra da Luz','authority_decision_id':'TEST-FAKE','authority_ref':'no real proof','process_step':'fixture','activation_method':'fixture'},
  'oil_route':route,'finished_oil_lot':lot(1,True),
  'oil_manufacture_decision':{'authority_decision_id':'TEST-FAKE','authority_ref':'test','complete_procedure_ref':'test','bom_reconciliation_ref':'test'},
  'oil_inputs':{k:lot(n) for k,n in OIL_OFFICIAL_BOM.items()},
  'p2_inputs':{k:lot(n) for k,n in {**P2_BOM,'Pedra da Luz':2}.items()},
  'parchment_coupon':{'specimen_id':'TEST','origin_ref':'test','qa_ref':'test'},
  'operator':{'operator_id':'TEST','p2_competence_ref':'test','appointment_ref':'test'},
  'witnesses':['TEST1','TEST2'],
  'test_authority':{'decision_id':'TEST','scope':'H2-3A-PARCHMENT-TEST','evidence_ref':'test'},
 }

class GuardTests(unittest.TestCase):
 def test_default_holds(self):self.assertEqual(evaluate({})['documentary_gate'],'HOLD')
 def test_no_application_with_complete_synthetic(self):self.assertFalse(evaluate(complete())['authorization_to_apply'])
 def test_no_magic_with_complete_synthetic(self):self.assertFalse(evaluate(complete())['magic_observed'])
 def test_no_r48_with_complete_synthetic(self):self.assertEqual(evaluate(complete())['r48_action'],'NONE')
 def test_finished_oil_does_not_need_ingredient_mfg(self):
  f=complete();f.pop('oil_inputs');f.pop('oil_manufacture_decision');self.assertEqual(evaluate(f)['documentary_gate'],'CONDITIONAL_READBACK_REQUIRED')
 def test_finished_oil_requires_quality(self):
  f=complete();del f['finished_oil_lot']['quality_ref'];self.assertIn('OIL_FINISHED_BATCH_WITH_TRACE_AND_QA_UNPROVEN',evaluate(f)['blocked_reasons'])
 def test_finished_oil_requires_lot(self):
  f=complete();f['finished_oil_lot']['quantity']=0;self.assertIn('OIL_FINISHED_BATCH_WITH_TRACE_AND_QA_UNPROVEN',evaluate(f)['blocked_reasons'])
 def test_finished_oil_requires_hash_format(self):
  f=complete();f['finished_oil_lot']['authenticity_sha256']='garbage';self.assertIn('OIL_FINISHED_BATCH_WITH_TRACE_AND_QA_UNPROVEN',evaluate(f)['blocked_reasons'])
 def test_manufacture_requires_official_three_iron(self):
  f=complete('MANUFACTURE');f['oil_inputs']['Pó de Ferro Celestial']['quantity']=2
  self.assertIn('OIL_RAW_LOT_UNVERIFIED:Pó de Ferro Celestial',evaluate(f)['blocked_reasons'])
 def test_manufacture_three_iron_does_not_authorize(self):
  f=complete('MANUFACTURE');self.assertEqual(evaluate(f)['documentary_gate'],'CONDITIONAL_READBACK_REQUIRED');self.assertFalse(evaluate(f)['authorization_to_apply'])
 def test_manufacture_requires_procedure_authority(self):
  f=complete('MANUFACTURE');f.pop('oil_manufacture_decision');self.assertIn('OIL_RECIPE_CONFLICTS_UNRESOLVED',evaluate(f)['blocked_reasons'])
 def test_no_salt_without_decision(self):
  f=complete();f['salt_decision']={};self.assertIn('P2-SALT-01_NO_COMPETENT_DOCUMENTED_DECISION',evaluate(f)['blocked_reasons'])
 def test_salt_alt_branch_changes_lot(self):
  f=complete();f['salt_decision']['choice']='ENCANTADO';f['p2_inputs']['Sal de Geodo Encantado']=lot(2);f['p2_inputs'].pop('Sal de Geodo Santo')
  self.assertEqual(evaluate(f)['documentary_gate'],'CONDITIONAL_READBACK_REQUIRED')
 def test_salt_alt_without_lot(self):
  f=complete();f['salt_decision']['choice']='ENCANTADO';self.assertIn('P2_LOT_UNVERIFIED:Sal de Geodo Encantado',evaluate(f)['blocked_reasons'])
 def test_energy_exclusive_one_branch(self):
  f=complete();self.assertEqual(evaluate(f)['required_p2_lots']['Pedra da Luz'],2);self.assertNotIn('Pote de Essência Mágica',evaluate(f)['required_p2_lots'])
 def test_energy_alternative(self):
  f=complete();f['energy_decision']['choice']='Pote de Essência Mágica';f['p2_inputs']['Pote de Essência Mágica']=lot(2)
  self.assertEqual(evaluate(f)['documentary_gate'],'CONDITIONAL_READBACK_REQUIRED')
 def test_energy_stage_absent(self):
  f=complete();f['energy_decision'].pop('process_step');self.assertIn('P2-ENERGY-02_NO_COMPETENT_PROCESS_DECISION',evaluate(f)['blocked_reasons'])
 def test_missing_operator(self):
  f=complete();f['operator'].pop('appointment_ref');self.assertIn('OPERATOR_P2_COMPETENCE_AND_ASSIGNMENT_UNVERIFIED',evaluate(f)['blocked_reasons'])
 def test_witness_duplicates(self):
  f=complete();f['witnesses']=['A','A'];self.assertIn('TWO_DISTINCT_WITNESSES_NOT_ESTABLISHED',evaluate(f)['blocked_reasons'])
 def test_unknown_authority(self):
  f=complete();f['test_authority'].pop('evidence_ref');self.assertIn('TEST_EXECUTION_AUTHORITY_NOT_EVIDENCED',evaluate(f)['blocked_reasons'])
 def test_unauthorized_scope(self):
  f=complete();f['test_authority']['scope']='PROD';self.assertIn('TEST_EXECUTION_AUTHORITY_NOT_EVIDENCED',evaluate(f)['blocked_reasons'])
 def test_bool_not_accepted_as_inventory_count(self):
  f=complete();f['finished_oil_lot']['quantity']=True;self.assertIn('OIL_FINISHED_BATCH_WITH_TRACE_AND_QA_UNPROVEN',evaluate(f)['blocked_reasons'])
 def test_official_iron_exactly_three(self):self.assertEqual(OIL_OFFICIAL_BOM['Pó de Ferro Celestial'],3)
 def test_historical_iron_only_comparator(self):self.assertEqual(OIL_HIST_IRON,2)

if __name__=='__main__':unittest.main(verbosity=2)
