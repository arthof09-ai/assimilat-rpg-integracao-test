"""Negative regressions: historical provenance must remain HOLD, not fake GREEN."""
import copy
import unittest
from scripts.verify_vlab_stage10_stage12_provenance import source, validate_docs

class HistoricalProvenanceGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stage10=source(10)
        cls.stage12=source(12)

    def test_original_two_documents_remain_hold(self):
        x=validate_docs(self.stage10,self.stage12)
        self.assertEqual(x['stage12_terminal_approved'],0)
        self.assertEqual(x['stage10_source_conflicts'],8)

    def test_fake_17_contracts_approved_rejected(self):
        v=copy.deepcopy(self.stage12)
        v['terminal_acceptance']=17
        with self.assertRaises(AssertionError):
            validate_docs(self.stage10,v)

    def test_false_technical_full_fusion_rejected(self):
        v=copy.deepcopy(self.stage12)
        v['technical_full_fusion_complete']=True
        with self.assertRaises(AssertionError):
            validate_docs(self.stage10,v)

    def test_fake_original_v09_available_rejected(self):
        v=copy.deepcopy(self.stage12)
        v['v09_historical_binary_available']=True
        with self.assertRaises(AssertionError):
            validate_docs(self.stage10,v)

    def test_false_stage10_frozen_source_rejected(self):
        v=copy.deepcopy(self.stage10)
        v['strict_eligible']=True
        with self.assertRaises(AssertionError):
            validate_docs(v,self.stage12)

    def test_fake_stage12_green_row_rejected(self):
        v=copy.deepcopy(self.stage12)
        v['rows'][0]['terminal_certified']=True
        with self.assertRaises(AssertionError):
            validate_docs(self.stage10,v)

if __name__=='__main__':
    unittest.main()
