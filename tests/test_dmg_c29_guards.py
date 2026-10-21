"""Fail-closed adversarial checks for the cold DMG C29 replica, no production access."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1]
RUNNER = BASE / "tests/run_dmg_c29_native.py"
SOURCE = BASE / "experiments/dmg_c29"


class TestC29ColdFailClosed(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="dmg_c29_guard_TEST_")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "tests").mkdir()
        (self.root / "experiments/dmg_c29").mkdir(parents=True)
        shutil.copyfile(RUNNER, self.root / "tests/run_dmg_c29_native.py")
        for item in ["golden.json", "original_scripts.xz.b64"]:
            shutil.copyfile(SOURCE / item, self.root / "experiments/dmg_c29" / item)
        self.fixture = self.root / "experiments/dmg_c29"

    def run_native(self):
        return subprocess.run([sys.executable, "-I", "-B", str(self.root / "tests/run_dmg_c29_native.py")],
                              capture_output=True, text=True, timeout=30)

    def rewrite_golden(self, change):
        path = self.fixture / "golden.json"
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data))

    def test_original_replica_reproducible(self):
        out = self.run_native()
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn('"total_checks": 43', out.stdout)
        self.assertIn('"formula_checks": 38', out.stdout)
        self.assertIn('"consistency_checks": 5', out.stdout)
        self.assertIn('"regenerated_identical": 10', out.stdout)

    def test_bundle_tampering_fails_closed(self):
        file = self.fixture / "original_scripts.xz.b64"
        text = file.read_text()
        file.write_text(("A" if text[0] != "A" else "B") + text[1:])
        out = self.run_native()
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("PINNED_BUNDLE_HASH_MISMATCH", out.stderr)

    def test_script_provenance_mismatch_fails_closed(self):
        self.rewrite_golden(lambda data: data["source_modules_sha256"].__setitem__("src/build_c29.py", "0" * 64))
        out = self.run_native()
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("ORIGINAL_SCRIPT_MISMATCH", out.stderr)

    def test_output_tampering_fails_closed(self):
        self.rewrite_golden(lambda data: data["outputs_sha256"].__setitem__("C29_SUMMARY_METRICS.json", "0" * 64))
        out = self.run_native()
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("hash_mismatches", out.stderr)

    def test_missing_bundle_fails_closed(self):
        (self.fixture / "original_scripts.xz.b64").unlink()
        out = self.run_native()
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("No such file or directory", out.stderr)


if __name__ == "__main__":
    unittest.main()
