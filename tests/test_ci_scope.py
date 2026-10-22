"""Teste nativo rapido da selecao de CI por arquivos realmente alterados."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / "scripts" / "ci_scope.py"
spec = importlib.util.spec_from_file_location("ci_scope", SOURCE)
ci_scope = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ci_scope)


class ScopeTests(unittest.TestCase):
    def test_vlab_only(self):
        self.assertEqual(ci_scope.choose_tests(["proposals/vlab/candidate.json"]), (True, False, "changed_paths"))

    def test_levelup_only(self):
        self.assertEqual(ci_scope.choose_tests(["proposals/levelup/candidate.json"]), (False, True, "changed_paths"))

    def test_both(self):
        self.assertEqual(ci_scope.choose_tests(["proposals/vlab/candidate.json", "proposals/levelup/candidate.json"]), (True, True, "changed_paths"))

    def test_shared_gate(self):
        self.assertEqual(ci_scope.choose_tests(["scripts/proposal_gate.py"]), (True, True, "changed_paths"))

    def test_shared_selector(self):
        self.assertEqual(ci_scope.choose_tests(["scripts/ci_scope.py"]), (True, True, "changed_paths"))

    def test_docs_alongside_vlab(self):
        self.assertEqual(ci_scope.choose_tests(["README.md", "proposals/vlab/candidate.json"]), (True, False, "changed_paths"))

    def test_only_docs_is_conservative_when_workflow_forced(self):
        self.assertEqual(ci_scope.choose_tests(["README.md", "docs/help.md"]), (True, True, "docs_only_manual_or_fallback"))

    def test_no_diff_fails_closed(self):
        self.assertEqual(ci_scope.choose_tests([]), (True, True, "no_diff_fail_closed"))

    def test_unknown_or_deleted_files_not_silently_skipped(self):
        self.assertEqual(ci_scope.choose_tests(["tests/test_error.py", "proposals/vlab/candidate.json"]), (True, True, "changed_paths"))

    def test_explicit_dispatch_runs_both(self):
        self.assertEqual(ci_scope.choose_tests([], force_all=True), (True, True, "workflow_dispatch_full_coverage"))

    def test_missing_git_commit_fails_closed(self):
        self.assertEqual(ci_scope.changed_paths({"GH_SCOPE_EVENT": "pull_request"}), ([], "missing_commit_range"))

    def test_real_git_diff_uses_changed_file_names_not_pr_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", tmp, "config", "user.email", "lab@example.invalid"], check=True)
            subprocess.run(["git", "-C", tmp, "config", "user.name", "TEST"], check=True)
            (root / "proposals" / "vlab").mkdir(parents=True)
            f = root / "proposals" / "vlab" / "candidate.json"
            f.write_text('"one"')
            subprocess.run(["git", "-C", tmp, "add", "."], check=True)
            subprocess.run(["git", "-C", tmp, "commit", "-qm", "initial"], check=True)
            base = subprocess.check_output(["git", "-C", tmp, "rev-parse", "HEAD"], text=True).strip()
            f.write_text('"two"')
            subprocess.run(["git", "-C", tmp, "commit", "-qam", "actual-code-change"], check=True)
            head = subprocess.check_output(["git", "-C", tmp, "rev-parse", "HEAD"], text=True).strip()
            original_run = subprocess.run
            def in_repo(args, **kwargs):
                return original_run([args[0], "-C", tmp, *args[1:]], **kwargs)
            with patch.object(ci_scope.subprocess, "run", side_effect=in_repo):
                paths, state = ci_scope.changed_paths({"GH_SCOPE_EVENT": "pull_request", "GH_SCOPE_PR_BASE": base, "GH_SCOPE_PR_HEAD": head})
            self.assertEqual((paths, state), (["proposals/vlab/candidate.json"], "verified_git_diff"))


if __name__ == "__main__":
    unittest.main()
