#!/usr/bin/env python3
"""Cold, read-only native DMG C29 numerical replay using original pinned scripts.

Only writes to a fresh temporary directory. No Notion connection, Party changes,
production writer, network calls or credits required. Not a canonical approval.
"""
import base64
import hashlib
import json
import lzma
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FIX = ROOT / "experiments" / "dmg_c29"
SEPARATOR = b"\0\0SPLIT-C29\0\0"


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    spec = json.loads((FIX / "golden.json").read_text(encoding="utf-8"))
    packed = base64.b64decode((FIX / "original_scripts.xz.b64").read_text().strip(), validate=True)
    assert sha256(packed) == spec["bundle_xz_sha256"], "PINNED_BUNDLE_HASH_MISMATCH"
    parts = lzma.decompress(packed).split(SEPARATOR)
    assert len(parts) == 2, "SOURCE_STRUCTURE_MISMATCH"
    names = ["src/build_c29.py", "src/verify_c29_independent.py"]
    for name, payload in zip(names, parts):
        assert sha256(payload) == spec["source_modules_sha256"][name], "ORIGINAL_SCRIPT_MISMATCH:" + name
    with tempfile.TemporaryDirectory(prefix="assimilat_c29_TEST_") as temp:
        lab = Path(temp)
        (lab / "src").mkdir()
        for name, payload in zip(names, parts):
            (lab / name).write_bytes(payload)
        # Explicitly no production credentials, no inherited Python package path.
        env = {"PATH": os.environ.get("PATH", ""), "HOME": temp, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"}
        records = []
        for name in names:
            proc = subprocess.run([sys.executable, "-I", "-B", str(lab / name)],
                                  cwd=lab, env=env, capture_output=True, text=True, timeout=30,
                                  check=False)
            print(proc.stdout.strip())
            if proc.returncode:
                print(proc.stderr, file=sys.stderr)
                raise RuntimeError("NATIVE_SCRIPT_FAILED:" + name)
            records.append(proc.stdout)
        pub = lab / "publication"
        actual = {p.name: sha256(p.read_bytes()) for p in pub.iterdir() if p.is_file()}
        expected = spec["outputs_sha256"]
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        mismatch = sorted(k for k in expected if k in actual and actual[k] != expected[k])
        assert not (missing or extra or mismatch), {"missing": missing, "extra": extra, "hash_mismatches": mismatch}
        independent = json.loads((pub / "C29_SECOND_NUMERICAL_ALGORITHM.json").read_text())
        assert independent["n"] == spec["expected_numeric_checks"]
        assert independent["passed"] == independent["n"]
        assert all(c["passed"] for c in independent["items"])
        summary = json.loads((pub / "C29_SUMMARY_METRICS.json").read_text())
        assert summary["CANONICAL_DMG_CHANGE"] == 0
        assert summary["F0_FORMAL"] == "4/8 HOLD"
        assert summary["F0_A5_BYTES"] == "0/7 HOLD"
        assert len(actual) == spec["expected_regenerated_files"]
        print(json.dumps({"status":"PASS_C29_NATIVE_COLD_TEST_ONLY", "original_scripts":2,
                          "numeric_checks":independent["passed"],"regenerated_identical":len(actual),
                          "production_writes":0,"canonicity":"HOLD"}, sort_keys=True))


if __name__ == "__main__":
    main()
