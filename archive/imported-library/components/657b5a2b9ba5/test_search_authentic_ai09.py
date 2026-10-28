import io
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile
from search_authentic_ai09 import scan, evaluate, EXPECTED_NAME, EXPECTED_BYTES

class HistoricalRecoveryGateTests(unittest.TestCase):
    def test_empty_directory_remains_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = scan([Path(tmp)])
            self.assertFalse(r['authenticated'])
            self.assertEqual(r['status'], 'BLOCKED_NO_AUTHENTIC_BYTES')

    def test_name_only_does_not_authenticate(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, EXPECTED_NAME).write_bytes(b'fake zip')
            r = scan([Path(tmp)])
            self.assertEqual(r['direct_candidates'][0]['reason'], 'SIZE_MISMATCH')

    def test_size_only_does_not_authenticate(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, 'original_from_chat.zip').write_bytes(b'0'*EXPECTED_BYTES)
            r = scan([Path(tmp)])
            self.assertFalse(r['authenticated'])
            self.assertEqual(r['direct_candidates'][0]['reason'], 'HASH_MISMATCH')

    def test_nested_fake_zip_is_detected_but_not_authenticated(self):
        with tempfile.TemporaryDirectory() as tmp:
            zfile=Path(tmp,'archive.zip')
            with ZipFile(zfile,'w') as z:z.writestr('old/'+EXPECTED_NAME,b'wrong binary')
            r = scan([Path(tmp)])
            self.assertEqual(r['nested_zip_candidates'],1)
            self.assertFalse(r['authenticated'])

    def test_candidate_exact_size_in_container_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            zfile=Path(tmp,'archive.zip')
            with ZipFile(zfile,'w') as z:z.writestr('old/'+EXPECTED_NAME,b'a'*EXPECTED_BYTES)
            r = scan([Path(tmp)])
            self.assertEqual(r['nested_candidates'][0]['reason'],'HASH_MISMATCH')

    def test_symlink_to_false_artifact_is_not_followed(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            (p/'decoy').write_bytes(b'b'*EXPECTED_BYTES)
            (p/EXPECTED_NAME).symlink_to(p/'decoy')
            r=scan([p])
            self.assertEqual(r['regular_files_scanned'],1)
            self.assertFalse(r['authenticated'])

    def test_identical_bytes_rejects_forged_original(self):
        r=evaluate(b'fake zip',EXPECTED_NAME)
        self.assertFalse(r['authenticated'])
        self.assertEqual(r['reason'],'SIZE_MISMATCH')

if __name__=='__main__': unittest.main()
