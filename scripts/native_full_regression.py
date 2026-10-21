"""Additional ORIGINAL VLAB/LEVEL-UP regression suites, in disposable TEST only.

- Reuses pinned SHA and manifest checking of existing native_engine_ci.py.
- Runs existing unmodified test modules. No new combat/level-up engine.
- Does not invoke Notion, Replit, Party, O Primeiro, host writers or production.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from native_engine_ci import PINS, verify

EXPECTED_VLAB_TESTS = 215
EXPECTED_LEVELUP_MODULES = 55
EXPECTED_LEVELUP_SHARDS = 8
EXPECTED_LEVELUP_TESTS = 2026


def execute(root: Path, argv: list[str], *, timeout: int = 180) -> tuple[str, str]:
    env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": str(root),
        "PYTHONNOUSERSITE": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "LC_ALL": "C.UTF-8",
    }
    proc = subprocess.run([sys.executable, "-I", "-B", *argv], cwd=root, env=env,
                          timeout=timeout, capture_output=True, text=True, check=False)
    if proc.returncode:
        raise AssertionError(
            "ORIGINAL_FULL_REGRESSION_FAILED\n" + (proc.stdout + proc.stderr)[-5000:]
        )
    return proc.stdout, proc.stderr


def run_vlab(root: Path) -> dict:
    src = (
        'import os,sys,unittest;'
        'sys.path.insert(0,os.path.join(os.getcwd(),"runtime","native"));'
        'suite=unittest.defaultTestLoader.discover(start_dir="runtime/native",'
        'pattern="test_*.py",top_level_dir="runtime/native");'
        'r=unittest.TextTestRunner(verbosity=0).run(suite);'
        'print("VLAB_NATIVE_TESTS="+str(r.testsRun)+";ERRORS="+str(len(r.errors))+'
        '";FAILURES="+str(len(r.failures)));'
        'sys.exit(0 if r.wasSuccessful() else 1)'
    )
    out, err = execute(root, ["-c", src], timeout=90)
    receipt = f"VLAB_NATIVE_TESTS={EXPECTED_VLAB_TESTS};ERRORS=0;FAILURES=0"
    if receipt not in out:
        raise AssertionError("VLAB_NATIVE_TEST_COVERAGE_MISMATCH\n" + out[-1500:] + err[-1500:])
    # Existing ORIGINAL R237 script attempts five adversarial modifications on
    # copies, rehashing the forged R18 chain. It must reject all five.
    original = root / "evidence/db/R237_TEAM_GR_C_TRANSITION_S23777002.sqlite"
    digest_before = hashlib.sha256(original.read_bytes()).hexdigest()
    adversarial_source = (
        'import os,sys,runpy;'
        'sys.path.insert(0,os.path.abspath("code"));'
        'runpy.run_path("code/r237_adversarial_rehash.py",run_name="__main__")'
    )
    execute(root, ["-c", adversarial_source], timeout=90)
    proof_path = root / "evidence/reports/R237_ADVERSARIAL_REHASH.json"
    proof = json.loads(proof_path.read_text(encoding="utf-8"))
    expected = {"HP0_FALSE_REVIVAL", "CONTINUE_AFTER_HP0", "UNJUST_WEAK_SPEED",
                "FALSIFY_OVERKILL", "PROMOTE_PRECREATE_TO_P4"}
    observed = proof.get("cases", [])
    if (proof.get("status") != "PASS_R237_ADVERSARIAL_REHASH_5_OF_5"
            or len(observed) != 5
            or {case.get("case") for case in observed} != expected
            or not all(case.get("rejected") is True
                       and case.get("final_R18_chain_rehashed") is True
                       and case.get("original_db_untouched") is True
                       and case.get("reason") != "FALSE_ACCEPT"
                       for case in observed)
            or hashlib.sha256(original.read_bytes()).hexdigest() != digest_before):
        raise AssertionError("VLAB_R237_ADVERSARIAL_GATE_FAILED")
    return {
        "suite": "VLAB_R237_ORIGINAL_NATIVE_UNIT_REGRESSION",
        "test_count": EXPECTED_VLAB_TESTS,
        "native_unittest_status": "PASS",
        "adversarial_rehash_original_cases": len(observed),
        "adversarial_rehash_rejected": len(observed),
        "canonical_promotion": "HOLD",
    }


def run_levelup(root: Path) -> dict:
    runner = root / "orc25_sharded_test_runner.py"
    if not runner.is_file():
        raise AssertionError("LEVELUP_ORIGINAL_SHARDED_RUNNER_NOT_FOUND")
    out, err = execute(root, [runner.name], timeout=240)
    target = root / "orc25_r216p9_equipment_transform" / "P9_SHARDED_TEST_RECEIPT.json"
    if not target.is_file():
        raise AssertionError("LEVELUP_SHARD_RECEIPT_MISSING")
    receipt = json.loads(target.read_text(encoding="utf-8"))
    checks = {
        "classification": receipt.get("classification") == "PARALLEL_MODULE_SHARDS_NOT_MONOLITHIC",
        "modules": receipt.get("module_count") == EXPECTED_LEVELUP_MODULES,
        "total": receipt.get("total_tests") == EXPECTED_LEVELUP_TESTS,
        "shard_count": len(receipt.get("shards", [])) == EXPECTED_LEVELUP_SHARDS,
        "pass": receipt.get("all_shards_pass") is True,
        "duplicate_modules": receipt.get("duplicate_module_count") == 0,
        "per_shard_pass": all(
            shard.get("exit") == 0 and shard.get("tests", 0) > 0
            for shard in receipt.get("shards", [])
        ),
        "printed": f'"total_tests": {EXPECTED_LEVELUP_TESTS}' in out,
    }
    if not all(checks.values()):
        raise AssertionError("LEVELUP_SHARD_COVERAGE_OR_HOLD:" + json.dumps(checks))
    return {
        "suite": "LEVELUP_R216P12_ORIGINAL_HISTORICAL_FULL_MODULE_REGRESSION",
        "module_count": receipt["module_count"],
        "tests": receipt["total_tests"],
        "shards": len(receipt["shards"]),
        "classification": "PARALLEL_MODULE_SHARDS_NOT_MONOLITHIC",
        "canonical_promotion": "HOLD",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine", choices=sorted(PINS), required=True)
    parser.add_argument("--archive", required=True, type=Path)
    args = parser.parse_args()
    archive = args.archive.resolve()
    verified = verify(archive, PINS[args.engine])
    with tempfile.TemporaryDirectory(prefix="assimilat_full_regression_TEST_") as tmp:
        root = Path(tmp)
        with zipfile.ZipFile(archive) as z:
            z.extractall(root)
        result = run_vlab(root) if args.engine == "vlab" else run_levelup(root)
    result.update({
        "status": "PASS_NATIVE_EXTENDED_TEST_ONLY",
        "original_archive_hash_validated": True,
        "verified_member_hashes": verified,
        "notion_writes": 0,
        "party_writes": 0,
        "replit_calls": 0,
    })
    print(json.dumps(result, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
