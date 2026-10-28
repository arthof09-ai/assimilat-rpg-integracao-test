#!/usr/bin/env python3
"""Reconstruct and audit exact archived VLAB R326 ZIP; Python standard library."""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for data in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(data)
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path.cwd() / "VLAB_CODIGO_MAE_R326_COMPLETO.zip")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    output = args.output.resolve()
    if output.exists():
        raise SystemExit("STOP: output exists; refusing overwrite: " + str(output))
    if output.parent != root and not output.parent.is_dir():
        raise SystemExit("STOP: output parent must exist")
    parts = manifest["parts"]
    if len(parts) != 11 or sum(p["bytes"] for p in parts) != manifest["source_size_bytes"]:
        raise SystemExit("STOP: manifest inconsistency")
    chunks = []
    for p in parts:
        file = root / p["file"]
        if not file.is_file() or file.stat().st_size != p["bytes"]:
            raise SystemExit("STOP: missing or wrong size: " + str(file))
        if digest(file) != p["sha256"]:
            raise SystemExit("STOP: mismatched part hash: " + str(file))
        chunks.append(file)
    with output.open("xb") as dest:
        for file in chunks:
            with file.open("rb") as source:
                while True:
                    data = source.read(1024 * 1024)
                    if not data:
                        break
                    dest.write(data)
    if output.stat().st_size != manifest["source_size_bytes"] or digest(output) != manifest["source_sha256"]:
        output.unlink(missing_ok=True)
        raise SystemExit("FAIL: concatenated ZIP hash differs; deleted untrusted output")
    try:
        with zipfile.ZipFile(output) as z:
            info = z.infolist()
            if len(info) != manifest["zip_members"]:
                raise ValueError("member count mismatch")
            for member in info:
                name = member.filename.replace("\\", "/")
                if name.startswith("/") or ".." in name.split("/"):
                    raise ValueError("unsafe ZIP member path")
            if z.testzip() is not None:
                raise ValueError("CRC failed")
    except Exception:
        output.unlink(missing_ok=True)
        raise
    print(json.dumps({"status": "PASS", "zip": str(output), "sha256": digest(output),
                      "bytes": output.stat().st_size, "members": len(info)}, ensure_ascii=False))
    return 0
if __name__ == "__main__":
    sys.exit(main())
