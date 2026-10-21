"""Exact original CRAFT F5/B30 evidence admission gate, cold / TEST / no writer.

This suite exercises evidence_row only. It DOES NOT run the composed() replay,
read original PS pages, test sorption/germination or create recipes/RC5 approvals.
"""
import base64
import hashlib
import importlib.util
import json
import lzma
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / 'experiments/craft_b30'


class CraftEvidenceGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads((FIX / 'golden.json').read_text())
        packed = base64.b64decode((FIX / 'original_evidence_gate.xz.b64').read_text().strip(), validate=True)
        assert hashlib.sha256(packed).hexdigest() == cls.spec['compressed_xz_sha256'], 'CRAFT_PACK_TAMPERED'
        code = lzma.decompress(packed)
        assert hashlib.sha256(code).hexdigest() == cls.spec['original_module_sha256'], 'CRAFT_SOURCE_TAMPERED'
        cls.tmp = tempfile.TemporaryDirectory(prefix='CRAFT_F5_TEST_')
        root = Path(cls.tmp.name)
        (root / 'code').mkdir()
        p = root / 'code/dual_replay.py'
        p.write_bytes(code)
        module_spec = importlib.util.spec_from_file_location('pinned_original_craft_dual_replay', p)
        cls.module = importlib.util.module_from_spec(module_spec)
        sys.modules[module_spec.name] = cls.module
        module_spec.loader.exec_module(cls.module)
        # Does not require/load any of the three ZIP baselines for evidence_row.

    @classmethod
    def tearDownClass(cls):
        sys.modules.pop('pinned_original_craft_dual_replay', None)
        cls.tmp.cleanup()

    def test_only_two_candidates(self):
        self.assertEqual(self.module.SUPPORTED, {'B30-06', 'B30-13'})

    def test_empty_evidence_is_hold(self):
        self.assertEqual(self.module.evidence_row('B30-06', {})['status'], 'DOCUMENTARY_GATES_OPEN_HOLD')

    def test_all_true_still_not_autocanonical(self):
        required = ['source_chain', 'lot_custody', 'operator_witness', 'physical_measurement',
                    'comparison', 'receipts', 'writer_green', 'signed_identity']
        result = self.module.evidence_row('B30-13', {key: True for key in required})
        self.assertEqual(result['status'], 'EXTERNAL_REVIEW_REQUIRED_NO_AUTOCANON')
        self.assertFalse(result['actual_writer_verified'])
        self.assertFalse(result['physical_efficacy_verified'])
        self.assertEqual(result['material_effects'], 0)
        self.assertIsNone(result['rec_id_created'])

    def test_unknown_evidence_rejected(self):
        self.assertEqual(self.module.evidence_row('B30-13', {'notion_write': True})['reason'], 'UNKNOWN_EVIDENCE_FIELDS')

    def test_strings_not_boolean(self):
        self.assertEqual(self.module.evidence_row('B30-06', {'writer_green': 'true'})['reason'], 'EVIDENCE_BOOL_TYPE_INVALID')

    def test_none_not_object(self):
        self.assertEqual(self.module.evidence_row('B30-06', None)['reason'], 'EVIDENCE_NOT_OBJECT')

    def test_unsupported_candidate_no_action(self):
        self.assertEqual(self.module.evidence_row('B30-07', {})['status'], 'UNSUPPORTED_CANDIDATE_NO_ACTION')

    def test_forged_rc5_status_ignored(self):
        self.assertEqual(self.module.evidence_row('B30-06', {'self_claimed_status': 'RC5_PASS'})['status'], 'DOCUMENTARY_GATES_OPEN_HOLD')

    def test_no_party_or_first_writes(self):
        r = self.module.evidence_row('B30-13', {'writer_green': True})
        self.assertEqual(r['party_writes'], 0)
        self.assertEqual(r['o_primeiro_writes'], 0)
        self.assertEqual(r['material_effects'], 0)

    def test_determinism(self):
        a = self.module.evidence_row('B30-13', {'receipts': True})
        b = self.module.evidence_row('B30-13', {'receipts': True})
        self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main()
