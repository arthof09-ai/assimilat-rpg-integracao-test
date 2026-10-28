import copy,json,sys,tempfile,unittest,os
from pathlib import Path
from .maturity_gate_v13 import qualify,load_existing_qa
from .r48_pingente_adapter import admission
from importlib.util import spec_from_file_location,module_from_spec
BASE=Path(__file__).resolve().parents[1]
def read(n):return json.loads((BASE/'fixtures'/n).read_text())
def arc():return read('r48_archived_contract.json')

class Maturity(unittest.TestCase):
 def setUp(self):
  self.old=read('recipe.json');self.new=read('recipe_v1_3_no_false_yield.json');self.pa=read('pa_gate.json')
  with tempfile.TemporaryDirectory() as t:self.r48=admission(self.old,self.pa,arc(),Path(t))
 def q(self,doc=None,pa=None,r48=None,magic=None):return qualify(doc or self.new,pa or self.pa,r48 or self.r48,magic)
 def test_original_auditor_false_positive_reproduced(self):self.assertEqual(load_existing_qa().audit(self.old)['rc_ceiling_test'],'RC5')
 def test_corrected_yield_lowers_ceiling(self):self.assertEqual(load_existing_qa().audit(self.new)['rc_ceiling_test'],'RC3')
 def test_corrected_real_pa(self):self.assertTrue(self.q()['pa_provider_compatible'])
 def test_no_R48_receipt(self):self.assertFalse(self.q()['r48_observed_receipt'])
 def test_full_document_no_magic_never_RC5(self):self.assertFalse(self.q(self.old)['official_RC5'])
 def test_missing_yield_found(self):self.assertIn('NO_APPROVED_MEASURED_YIELD',self.q()['blocks'])
 def test_missing_loss_triggers_original_auditor(self):self.assertIn('RC4_LOSSES_EVIDENCE',[f['code'] for f in self.q()['static_findings']])
 def test_provider_wrong_is_rejected(self):
  pa=copy.deepcopy(self.pa);pa['pa_version_compatible']=False
  self.assertIn('PA_RECEIPT_UNVERIFIED_OR_MISMATCH',self.q(pa=pa)['blocks'])
 def test_synthetic_forged_magic_rejected(self):
  e={'verified':True,'source':'SYNTHETIC','magic_observed':True,'signer':'self'}
  self.assertFalse(self.q(self.old,magic=e)['official_RC5'])
 def test_fake_R48_receipt_untrusted(self):
  r=copy.deepcopy(self.r48);r['original_engine_invoked']=True;r['r48_receipt']={'status':'EXPERIMENTAL_QA_PASS'};r['status']='RECEIPT_VERIFIED_IN_LAB'
  self.assertFalse(self.q(self.old,r48=r)['official_RC5'])
 def test_no_P4_auto_promotion(self):self.assertFalse(self.q()['PS_P4_promoted'])
 def test_no_official_f5(self):self.assertFalse(self.q()['f5_production_authorized'])
 def test_economy_uncertain(self):self.assertIn('CTE_UTE_UNVERIFIED',self.q()['blocks'])
 def test_PS_resource_visible(self):self.assertIn('PS_RESOURCE_JIT_AND_QUALITY_PENDING',self.q()['blocks'])
 def test_independent_magic_unavailable(self):self.assertIn('INDEPENDENT_MAGICAL_MEASUREMENT_VERIFIER_NOT_INSTALLED',self.q()['blocks'])

class ArchivedFactory(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  source=Path(os.environ.get('CRAFT_FC04_ROOT',str(BASE/'baselines/FC04_UNPACK/CRAFT-R48-B30-22-FC04')))/'code/independent_audit.py'
  spec=spec_from_file_location('original_fc04_independent',source);mod=module_from_spec(spec);spec.loader.exec_module(mod);cls.audit=staticmethod(mod.audit_store)
  cls.base=source.parent.parent/'outputs/ACCEPTED_V2'
 def test_archived_good_triple(self):self.assertTrue(self.audit(self.base/'R48_SHARED_TRIPLE_STORE')['ok'])
 def test_archived_qa_negative(self):self.assertTrue(self.audit(self.base/'R48_QA_NEGATIVE_STORE')['ok'])
 def test_archived_expired_certificate(self):self.assertTrue(self.audit(self.base/'R48_EXPIRED_CERT_STORE')['ok'])
 def test_archived_ack_restart(self):self.assertTrue(self.audit(self.base/'R48_LOST_ACK_RECOVERED_STORE')['ok'])
 def test_archived_orphan_rejected(self):self.assertIn('ORPHAN_OR_MISSING_CHECKPOINT',self.audit(self.base/'R48_ORPHAN_FAIL_CLOSED_STORE')['failures'])

if __name__=='__main__':unittest.main()
