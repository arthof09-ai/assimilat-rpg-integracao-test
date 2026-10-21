import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import sys
import warnings
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.audit_zip import audit_archive


class ArchiveIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def fixture(self, name="fixture.zip", payload=b"test", *, broken=False, unlisted=False, unsafe=False, duplicate=False):
        path = Path(self.tmp.name) / name
        digest = hashlib.sha256(payload).hexdigest()
        with zipfile.ZipFile(path, "w") as z:
            z.writestr("code/demo.txt", payload)
            z.writestr("MANIFEST_SHA256.json", json.dumps({"files": {"code/demo.txt": "0" * 64 if broken else digest}}))
            if unlisted: z.writestr("unexpected.txt", "not listed")
            if unsafe: z.writestr("../escape.txt", "not safe")
            if duplicate:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    z.writestr("code/demo.txt", payload)
        return path

    def test_valid(self): self.assertEqual(audit_archive(self.fixture())["status"], "PASS")
    def test_bad_manifest(self): self.assertEqual(audit_archive(self.fixture(broken=True))["status"], "HOLD")
    def test_extra_file(self): self.assertEqual(audit_archive(self.fixture(unlisted=True))["status"], "HOLD")
    def test_traversal(self): self.assertEqual(audit_archive(self.fixture(unsafe=True))["status"], "HOLD")
    def test_duplicate(self): self.assertEqual(audit_archive(self.fixture(duplicate=True))["status"], "HOLD")
    def test_no_execution(self):
        x = audit_archive(self.fixture(payload=b"__import__('os').system('exit 99')"))
        self.assertEqual((x["status"], x["external_writes"], x["canonical_effects"]), ("PASS", 0, 0))
    def test_bad_crc(self):
        p=self.fixture(payload=b"VALID_ONLY")
        payload=p.read_bytes();p.write_bytes(payload.replace(b"VALID_ONLY",b"BAD__ONLY"))
        self.assertEqual(audit_archive(p)["status"], "HOLD")
    def test_can_read_from_different_folder(self):
        self.assertEqual(audit_archive(self.fixture(name="independent.zip"))["status"], "PASS")


if __name__ == "__main__": unittest.main()
