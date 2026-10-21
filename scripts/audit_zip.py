"""Read-only archive auditor for independent TEST labs.

Never extracts archives, executes their code or accesses external services.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import stat
import zipfile


def audit_archive(filename: str | pathlib.Path) -> dict:
    path = pathlib.Path(filename)
    report = {"artifact": path.name, "mode": "TEST_READ_ONLY", "status": "HOLD"}
    with zipfile.ZipFile(path, "r") as z:
        infos = [i for i in z.infolist() if not i.is_dir()]
        paths = [i.filename for i in infos]
        unsafe = [
            i.filename for i in infos if pathlib.PurePosixPath(i.filename).is_absolute()
            or ".." in pathlib.PurePosixPath(i.filename).parts
            or "\\" in i.filename
            or stat.S_ISLNK(i.external_attr >> 16)
        ]
        duplicates = sorted({n for n in paths if paths.count(n) > 1})
        try:
            integrity = z.testzip()
        except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
            integrity = "ERROR:" + type(exc).__name__
        candidates = [n for n in paths if n.split("/")[-1] in {
            "MANIFEST_SHA256.json", "SHA256_MANIFEST.json", "C29_SHA256_MANIFEST.json", "MANIFEST_R216P11_SHA256.json"
        } and n.count("/") == 0]
        priority = ["MANIFEST_R216P11_SHA256.json", "C29_SHA256_MANIFEST.json", "SHA256_MANIFEST.json", "MANIFEST_SHA256.json"]
        names = sorted(candidates, key=lambda x: priority.index(x))
        manifest = names[0] if names else None
        mismatches: list[str] = []
        omitted: list[str] = []
        covered = 0
        if manifest and integrity is None:
            spec = json.loads(z.read(manifest))
            entries = spec.get("entries", spec.get("files", spec.get("files_sha256", {})))
            if not isinstance(entries, dict):
                raise ValueError("Unsupported manifest structure")
            for n, expected in entries.items():
                digest = expected if isinstance(expected, str) else expected.get("sha256", "")
                if n not in paths or hashlib.sha256(z.read(n)).hexdigest() != digest:
                    mismatches.append(n)
                else:
                    covered += 1
            omitted = [n for n in paths if n != manifest and n not in entries]
        status = "PASS" if manifest and not any([unsafe, duplicates, integrity, mismatches, omitted]) else "HOLD"
        report.update({
            "status": status,
            "zip_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "manifest": manifest,
            "members": len(infos),
            "hashes_verified": covered,
            "unsafe_entries": unsafe,
            "duplicate_entries": duplicates,
            "crc_bad_member": integrity,
            "mismatches": mismatches,
            "unlisted_members": omitted,
            "external_writes": 0,
            "canonical_effects": 0,
        })
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Independent TEST ZIP integrity checker")
    parser.add_argument("archives", nargs="+", type=pathlib.Path)
    args = parser.parse_args()
    reports = [audit_archive(f) for f in args.archives]
    print(json.dumps(reports, ensure_ascii=False, indent=2))
    raise SystemExit(0 if all(r["status"] == "PASS" for r in reports) else 2)


if __name__ == "__main__":
    main()
