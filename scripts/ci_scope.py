"""Conservative test scope selector. Real Git commit diff, never PR title/body.
If impact is unknown, both engines run; this is not a new RPG engine.
"""
from __future__ import annotations
import os
from pathlib import Path
import subprocess

SHARED = frozenset({
    "scripts/proposal_gate.py",
    "scripts/ci_scope.py",
    ".github/workflows/comestre-candidate.yml",
})
DOCS = frozenset({"README.md", "AGENTS.md"})


def choose_tests(paths: list[str] | tuple[str, ...], *, force_all: bool = False) -> tuple[bool, bool, str]:
    if force_all:
        return True, True, "workflow_dispatch_full_coverage"
    if not paths:
        return True, True, "no_diff_fail_closed"
    affected: set[str] = set()
    for path in paths:
        if path.startswith("proposals/vlab/"):
            affected.add("vlab")
        elif path.startswith("proposals/levelup/"):
            affected.add("levelup")
        elif path in DOCS or path.startswith("docs/"):
            continue
        elif path in SHARED:
            affected.update(("vlab", "levelup"))
        else:
            # Unknown dependencies and deletions are not silently skipped.
            affected.update(("vlab", "levelup"))
    if not affected:
        return True, True, "docs_only_manual_or_fallback"
    return "vlab" in affected, "levelup" in affected, "changed_paths"


def changed_paths(env: dict[str, str]) -> tuple[list[str], str]:
    event = env.get("GH_SCOPE_EVENT", "")
    if event == "workflow_dispatch":
        return [], "dispatch"
    if event == "pull_request":
        a, b = env.get("GH_SCOPE_PR_BASE", ""), env.get("GH_SCOPE_PR_HEAD", "")
        revs = [f"{a}...{b}"] if a and b else []
    elif event == "push":
        a, b = env.get("GH_SCOPE_BEFORE", ""), env.get("GH_SCOPE_HEAD", "")
        revs = [a, b] if a and b and a != "0" * 40 else []
    else:
        return [], "unsupported_event"
    if not revs:
        return [], "missing_commit_range"
    proc = subprocess.run(
        ["git", "diff", "--name-only", "-z", *revs, "--"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if proc.returncode:
        return [], "diff_unavailable_fail_closed"
    return [os.fsdecode(path) for path in proc.stdout.split(b"\0") if path], "verified_git_diff"


def main() -> None:
    env = dict(os.environ)
    paths, source = changed_paths(env)
    vlab, levelup, why = choose_tests(
        paths, force_all=env.get("GH_SCOPE_EVENT") == "workflow_dispatch"
    )
    status = (
        f"vlab={str(vlab).lower()}\n"
        f"levelup={str(levelup).lower()}\n"
        f"source={source}\n"
        f"reason={why}\n"
    )
    output = env.get("GITHUB_OUTPUT")
    if output:
        with Path(output).open("a", encoding="utf-8") as stream:
            stream.write(status)
    print("TEST_SCOPE: " + status.replace("\n", " ").strip())
    summary = env.get("GITHUB_STEP_SUMMARY")
    if summary:
        with Path(summary).open("a", encoding="utf-8") as stream:
            stream.write(
                f"**Seletor TEST:** VLAB={'RUN' if vlab else 'SKIPPED_NOT_AFFECTED'}; "
                f"LEVEL-UP={'RUN' if levelup else 'SKIPPED_NOT_AFFECTED'}; "
                f"origem={source}; motivo={why}; arquivos={len(paths)}. "
                "SKIPPED nao equivale a PASS.\n"
            )


if __name__ == "__main__":
    main()
