"""CI preflight for the original-engine runner; no external packages or Notion."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("native_engine_ci", ROOT/"scripts/native_engine_ci.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class NativePreflight(unittest.TestCase):
    def test_exact_recovery_pins(self):
        self.assertEqual(module.PINS["vlab"]["files"], 299)
        self.assertEqual(module.PINS["levelup"]["files"], 370)
        self.assertEqual(len(module.PINS["vlab"]["sha"]), 64)
        self.assertEqual(len(module.PINS["levelup"]["sha"]), 64)

    def test_archive_wrong_hash_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/module.PINS["vlab"]["name"]
            p.write_bytes(b"not the original ZIP")
            with self.assertRaisesRegex(ValueError, "ARCHIVE_SHA_MISMATCH"):
                module.verify(p,module.PINS["vlab"])

    def test_archive_wrong_name_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"not-the-original.zip"
            p.write_bytes(b"not the original ZIP")
            with self.assertRaisesRegex(ValueError, "WRONG_SOURCE_ARCHIVE_NAME"):
                module.verify(p,module.PINS["levelup"])

    def test_both_sources_in_test_only_mode(self):
        source=(ROOT/"scripts/native_engine_ci.py").read_text()
        self.assertIn('"canonical_promotion":"HOLD"',source)
        self.assertIn('"notion_writes":0',source)
        self.assertIn('"replit_calls":0',source)
        self.assertIn("TemporaryDirectory",source)
        self.assertNotIn("requests.post(",source)

if __name__=="__main__":
    unittest.main()
