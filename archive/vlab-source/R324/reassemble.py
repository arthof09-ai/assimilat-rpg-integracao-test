#!/usr/bin/env python3
"""Reconstitui o ZIP historico VLAB a partir de partes reais, valida SHA256 e CRC."""
import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path.cwd() / "VLAB_CODIGO_MAE_R324_COMPLETO.zip")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    parts = manifest["parts"]
    if sum(p["bytes"] for p in parts) != manifest["source_size_bytes"]:
        raise SystemExit("STOP: manifest size inconsistent")
    out = args.output.resolve()
    if not out.parent.is_dir():
        raise SystemExit("STOP: output parent missing")
    digest = hashlib.sha256()
    created = False
    try:
        with out.open("xb") as target:
            created = True
            for part in parts:
                name = part["file"]
                if not re.fullmatch(r"part[0-9]{2}\.bin", name):
                    raise ValueError("unsafe manifest part name")
                src = root / name
                data = src.read_bytes()
                if len(data) != part["bytes"]:
                    raise ValueError("part size mismatch: " + name)
                git_digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
                if git_digest != part["git_blob_sha1"]:
                    raise ValueError("part git-blob SHA mismatch: " + name)
                target.write(data)
                digest.update(data)
        if out.stat().st_size != manifest["source_size_bytes"] or digest.hexdigest() != manifest["source_sha256"]:
            raise ValueError("final SHA256/size mismatch")
        with zipfile.ZipFile(out) as z:
            if len(z.infolist()) != manifest["zip_members"]:
                raise ValueError("ZIP member count mismatch")
            for item in z.infolist():
                n = item.filename.replace("\\", "/")
                if n.startswith("/") or ".." in n.split("/"):
                    raise ValueError("unsafe member")
            if z.testzip() is not None:
                raise ValueError("ZIP CRC invalid")
    except Exception:
        if created:
            out.unlink(missing_ok=True)
        raise
    print(json.dumps({"status": "PASS", "file": str(out), "bytes": manifest["source_size_bytes"], "sha256": digest.hexdigest()}))
    return 0

if __name__ == "__main__":
    sys.exit(main())
