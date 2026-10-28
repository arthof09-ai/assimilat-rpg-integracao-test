import importlib.util
import unittest
from pathlib import Path

P=Path(__file__).resolve().parents[1]/'scripts'/'acceptance_evidence_check.py'
sp=importlib.util.spec_from_file_location('acceptance',P); mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod)

class Acceptance(unittest.TestCase):
    def test_incomplete_is_hold(self):
        self.assertEqual(mod.assess({'scope':'OP-VLAB-FUSION-SANDBOX-01:ENGINEERING-DOCS'})['result'],'HOLD')
    def test_wrong_scope_is_hold(self):
        self.assertIn('AUTHORIZED_SCOPE',mod.assess({'scope':'Party'})['missing'])
    def test_complete_self_asserted_still_not_green(self):
        a={k:{'observed':True,'evidence_ref':'NOTION-EVIDENCE-PLACEHOLDER-01'} for k in mod.REQUIRED}
        result=mod.assess({'scope':'OP-VLAB-FUSION-SANDBOX-01:ENGINEERING-DOCS','assertions':a})
        self.assertEqual(result['result'],'READY_FOR_INDEPENDENT_REVIEW_NOT_GREEN')
    def test_bare_true_does_not_count(self):
        doc={'scope':'OP-VLAB-FUSION-SANDBOX-01:ENGINEERING-DOCS','assertions':{'old_writer_token_denied':True}}
        self.assertIn('old_writer_token_denied',mod.assess(doc)['missing'])
