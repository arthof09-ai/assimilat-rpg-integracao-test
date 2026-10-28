#!/usr/bin/env python3
"""Local, conservative importer for RPG Assimilacao Library archives.

No network, Git write, Notion write, or automatic commit/push. Requires local
copies of the real file bytes. By default, audit ONLY. --apply copies into an
isolated archive folder after size/hash/CRC and collision checks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEXES = (
    ROOT / "docs/archive-audit/LIBRARY_TECHNICAL_INVENTORY_20261028_PART01.json",
    ROOT / "docs/archive-audit/LIBRARY_TECHNICAL_INVENTORY_20261028_PART02.json",
)
TARGET = ROOT / "archive/imported-library"
ALLOWED = {".zip", ".py", ".js", ".html", ".json", ".csv", ".md", ".svg", ".css"}
EXCLUDED_NAMES = ("PARTY-EXPORT", "PARTY_EXPORT", ".ENV", "CREDENTIAL", "SECRET", "TOKEN", "PASSWORD")
AREA_NAMES = {"vlab", "levelup", "craft", "dmg", "pa", "tabletop", "visual-dev", "other"}
BUFF = 1024 * 1024


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(BUFF), b""):
            h.update(block)
    return h.hexdigest()


def zip_integrity(path: Path) -> tuple[int, str]:
    try:
        with zipfile.ZipFile(path) as archive:
            members = archive.infolist()
            names = [n.filename for n in members]
            if len(names) != len(set(names)):
                return len(members), "DUPLICATE_MEMBERS"
            for name in names:
                v = name.replace("\\", "/")
                if v.startswith("/") or ".." in v.split("/") or "\x00" in v:
                    return len(members), "UNSAFE_MEMBER_PATH"
            broken = archive.testzip()
            return len(members), ("CRC_PASS" if broken is None else "CRC_FAIL:" + broken)
    except Exception as exc:
        return 0, "NOT_VALID_ZIP:" + type(exc).__name__


def load_index() -> dict[str, list[dict]]:
    by_name = defaultdict(list)
    for path in INDEXES:
        if not path.is_file():
            raise FileNotFoundError("Missing official inventory: " + str(path))
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("schema") != "assimilat.library_inventory/1.0":
            raise ValueError("Unknown manifest schema " + str(path))
        for row in data["items"]:
            name = row.get("name", "")
            if Path(name).name != name:
                continue
            if Path(name).suffix.lower() in ALLOWED:
                by_name[name].append(row)
    return by_name


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source-dir", required=True, type=Path,
                    help="Local, predownloaded original Library files; recursive search")
    ap.add_argument("--apply", action="store_true",
                    help="Copy verified bytes into archive/imported-library; NEVER commits/pushes")
    ap.add_argument("--limit", type=int, default=0,
                    help="Max candidate files to inspect (0 means no limit)")
    ap.add_argument("--receipt", type=Path,
                    help="Optional path to write a JSON report")
    args = ap.parse_args()
    source_dir = args.source_dir.resolve()
    if not source_dir.is_dir():
        ap.error("--source-dir is not a directory")
    try:
        source_dir.relative_to(ROOT)
        ap.error("Source must be OUTSIDE the working Git repository")
    except ValueError:
        pass
    index = load_index()
    lfs_available = subprocess.run(["git", "lfs", "version"], cwd=ROOT,
                                  capture_output=True, check=False).returncode == 0
    records = []
    seen_hashes = set()
    checked = 0
    for file in sorted(source_dir.rglob("*")):
        if not file.is_file():
            continue
        name = file.name
        if name not in index or any(word in name.upper() for word in EXCLUDED_NAMES):
            continue
        checked += 1
        if args.limit and checked > args.limit:
            break
        status, info = "PENDING", {}
        try:
            size = file.stat().st_size
            candidates = [row for row in index[name] if row.get("bytes") == size]
            if not candidates:
                status = "HOLD_SIZE_MISMATCH"
            else:
                categories = set(row.get("area") for row in candidates)
                if len(categories) != 1 or categories.pop() not in AREA_NAMES:
                    status = "HOLD_AMBIGUOUS_AREA"
                else:
                    area = candidates[0]["area"]
                    digest = sha256(file)
                    info["sha256"] = digest
                    if digest in seen_hashes:
                        status = "SKIP_DUPLICATE_HASH_IN_BATCH"
                    else:
                        seen_hashes.add(digest)
                        destination = TARGET / area / name
                        info["destination"] = destination.relative_to(ROOT).as_posix()
                        if file.suffix.lower() == ".zip":
                            members, crc = zip_integrity(file)
                            info["zip_members"] = members
                            info["zip_integrity"] = crc
                            if crc != "CRC_PASS":
                                status = "HOLD_ZIP_INVALID"
                        if status == "PENDING" and destination.exists():
                            status = ("SKIP_IDENTICAL_DESTINATION" if
                                      sha256(destination) == digest
                                      else "HOLD_DESTINATION_COLLISION")
                        if status == "PENDING" and file.suffix.lower() == ".zip" and not lfs_available:
                            status = "HOLD_GIT_LFS_REQUIRED"
                        if status == "PENDING":
                            if args.apply:
                                destination.parent.mkdir(parents=True, exist_ok=True)
                                shutil.copy2(file, destination)
                                if sha256(destination) != digest:
                                    destination.unlink(missing_ok=True)
                                    status = "ERROR_READBACK_HASH"
                                else:
                                    status = "COPIED_VERIFIED_NOT_COMMITTED"
                            else:
                                status = "READY_DRY_RUN"
        except Exception as exc:
            status = "ERROR_" + type(exc).__name__
            info["diagnostic"] = str(exc)[:300]
        records.append({"source": str(file), "bytes": file.stat().st_size,
                        "status": status, **info})
        print(status + " " + name)
    result = {"schema": "assimilat.archive_import_receipt/1.0",
              "mode": "APPLY_LOCAL_ONLY" if args.apply else "DRY_RUN",
              "repository": "arthof09-ai/assimilat-rpg-integracao-test",
              "lfs_detected": lfs_available,
              "checked": checked, "records": records,
              "remark": "No automatic commit/push; GitHub presence requires a separately checked commit."}
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                                encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "records"},
                     ensure_ascii=False, indent=2))
    return 0 if not any(r["status"].startswith("ERROR") for r in records) else 2


if __name__ == "__main__":
    sys.exit(main())
