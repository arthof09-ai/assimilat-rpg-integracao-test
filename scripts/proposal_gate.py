"""Gate de proposta de codigo TEST. Usa motores ORIGINAIS; nenhuma escrita no Notion.
Aplica UMA substituicao exata em um arquivo autorizado, apenas em pasta temporaria,
e roda os testes ORIGINAIS correspondentes. Nao toca nos ZIPs, Party ou canone.
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

ROOT = Path(__file__).resolve().parents[1]
ALLOW = {
    "vlab": ("runtime/native/vlab_rd_v08.py", "test_vlab_rd_v08", 24),
    "levelup": ("ibx114_r216p12_master_correction.py", "test_ibx114_r216p12_master_correction", 184),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine", required=True, choices=sorted(ALLOW))
    parser.add_argument("--archive", required=True, type=Path)
    args = parser.parse_args()
    archive = args.archive.resolve()
    verify(archive, PINS[args.engine])
    proposal_path = ROOT / "proposals" / args.engine / "candidate.json"
    candidate = json.loads(proposal_path.read_text(encoding="utf-8"))
    target, test_module, expected_tests = ALLOW[args.engine]

    if set(candidate) != {"origin", "before", "after", "note"} or candidate["origin"] != target:
        raise AssertionError("UNAUTHORIZED_PROPOSAL_SCOPE")
    before, after = candidate["before"], candidate["after"]
    if not all(isinstance(v, str) and 0 < len(v) < 380
               for v in (before, after, candidate["note"])):
        raise AssertionError("INVALID_PROPOSAL")
    if before == after:
        raise AssertionError("NO_CODE_CHANGE")

    with tempfile.TemporaryDirectory(prefix="assimilat_comestre_candidate_TEST_") as tmp:
        root = Path(tmp)
        with zipfile.ZipFile(archive) as zipped:
            zipped.extractall(root)
        path = root / target
        original = path.read_text(encoding="utf-8")
        if original.count(before) != 1:
            raise AssertionError("PROPOSAL_DOES_NOT_MATCH_ORIGINAL_SOURCE")
        patched = original.replace(before, after, 1)
        path.write_text(patched, encoding="utf-8")

        test_root = root / "runtime/native" if args.engine == "vlab" else root
        script = (
            "import os,sys,unittest;"
            + f"sys.path.insert(0,{str(test_root)!r});"
            + ('sys.path.insert(0,os.path.join(os.getcwd(),"baseline","code"));'
               if args.engine == "levelup" else "")
            + f"r=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromName({test_module!r}));"
            + 'print(f"CANDIDATE_TESTS={r.testsRun};FAILURES={len(r.failures)};ERRORS={len(r.errors)}");'
            + "sys.exit(not r.wasSuccessful())"
        )
        env = {"PATH": os.environ.get("PATH", ""), "HOME": tmp,
               "PYTHONNOUSERSITE": "1", "PYTHONDONTWRITEBYTECODE": "1"}
        proc = subprocess.run([sys.executable, "-I", "-B", "-c", script],
                              cwd=root, env=env, text=True, capture_output=True, timeout=120)
        print(proc.stdout[-4000:])
        print(proc.stderr[-4000:], file=sys.stderr)
        if proc.returncode or f"CANDIDATE_TESTS={expected_tests};FAILURES=0;ERRORS=0" not in proc.stdout:
            print(json.dumps({"status": "REJECTED_TEST_PROPOSAL", "engine": args.engine,
                              "tests_expected": expected_tests,
                              "original_changed": False, "candidate_merge": "BLOCKED"},
                             sort_keys=True))
            raise SystemExit(2)
        print(json.dumps({"status": "PASS_TEST_PROPOSAL", "engine": args.engine,
                          "tested_original_module": test_module, "tests": expected_tests,
                          "candidate_sha256": hashlib.sha256(patched.encode()).hexdigest(),
                          "original_changed": False, "canonical_promotion": "HOLD"},
                         sort_keys=True))


if __name__ == "__main__":
    main()
