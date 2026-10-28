import unittest,copy,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from r41_pingente_r44_controlado import run,make_contract,make_lots,RECIPE_KEY,R48
from gate_material_R41 import decide,REQUIRED
sys.path.insert(0,str(R48))
from experimental_engine import SandboxEngine
from r48_factory import IntegratedFactory,FactoryError
from r48_fixtures import lots as historics,order,REVIEW

class R41Tests(unittest.TestCase):
 def test_original_hash(self):self.assertEqual(run()['main_engine_original_hash'],'872dc5bf1e588a9ba6f4c45421a4dddbbe7d261842a4e951fd684bfc374c6801')
 def test_r48_pingente_refused(self):self.assertEqual(run()['r48_top_level'],'DENY:ONLY_TWO_EXISTING_RECIPES')
 def test_r44_admitted_and_ran(self):self.assertEqual(run()['r44_core_mechanical_pipeline'],'EXECUTED_IN_SYNTHETIC_COPY')
 def test_missing_magic_evidence(self):self.assertEqual(run()['negative_missing_evidence'],'REJECTED_QUALITY')
 def test_negative_magic_evidence(self):self.assertEqual(run()['negative_false_transfer'],'REJECTED_QUALITY')
 def test_forged_magic_fixture_trap(self):self.assertFalse(run()['test_of_forged_true_proves_real_magic'])
 def test_no_material_output(self):self.assertEqual(run()['physically_crafted_products'],0)
 def test_no_real_attestation(self):self.assertFalse(run()['r46_r47_real_attestation'])
 def test_no_f5_release(self):self.assertEqual(run()['F5_prod'],'RED')
 def test_all_proofs_absent(self):self.assertFalse(decide({})['RC5'])
 def test_all_synthetic_claims_not_enough(self):self.assertFalse(decide({k:True for k in REQUIRED})['RC5'])
 def test_electronic_claim_not_vetted(self):self.assertEqual(decide({'r47_real_attestation':{'signature':'fixture'}})['missing_authoritative_proofs']['r47_real_attestation'],'CLAIM_UNVERIFIED_NEEDS_AUTHORITATIVE_READBACK')
 def test_no_P4(self):self.assertFalse(decide({k:True for k in REQUIRED})['P4'])
 def test_no_fabrication(self):self.assertFalse(decide({k:True for k in REQUIRED})['official_fabrication'])
 def test_f5_schema_blocked(self):self.assertEqual(decide({k:True for k in REQUIRED})['status'],'HOLD_MATERIAL_UNVERIFIED')
 def test_inputs_3_original_sources(self):self.assertEqual(len(make_contract()['inputs']),3)
 def test_fiber_units_cm_exact(self):self.assertEqual((make_contract()['inputs'][2]['unit'],make_contract()['inputs'][2]['quantity']),('cm',45))
 def test_no_mechanical_bonus(self):self.assertEqual(make_contract()['mechanical_bonus'],0)
 def test_lots_only_simulated(self):self.assertTrue(all(x['fixture_kind']=='SYNTHETIC' for x in make_lots()))
 def test_invalid_qa_magic_fails(self):
  engine=SandboxEngine({RECIPE_KEY:make_contract()},make_lots())
  r=engine.run(RECIPE_KEY,'SBX-R41-NEG', [x['lot_id'] for x in make_lots()],{'ligacao_mecanica_integra':True,'magia_transferida_com_prova_independente':False},make_contract()['tools'],make_contract()['skills'])
  self.assertEqual(r['status'],'REJECTED_QUALITY')
 def test_sha_unchanged_after(self):
  import hashlib
  p=R48/'r48_factory.py';s=hashlib.sha256(p.read_bytes()).hexdigest();run();self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),s)

if __name__=='__main__':unittest.main(verbosity=2)
