#!/usr/bin/env python3
"""Restore untouched R05 bytes from nested known ZIP for local TEST, not a new motor."""
from pathlib import Path
import hashlib,zipfile
ROOT=Path(__file__).resolve().parent.parent
ARCHIVE=ROOT/'PA_UNIVERSAL_R05_TEST_20261017.zip'
EXPECTED='6f69fd1ef197851e128c2fc7becbad1f2a14a1438e7bf9ac71742b835f99078e'
assert ARCHIVE.is_file() and hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()==EXPECTED,'R05 baseline hash differs'
with zipfile.ZipFile(ARCHIVE) as z:
    assert z.testzip() is None,'CRC failure'
    for entry in z.namelist():
        path=Path(entry)
        assert not path.is_absolute() and '..' not in path.parts and path.parts[0]=='PA_UNIVERSAL_R05_TEST_20261017','bad ZIP path'
    z.extractall(ROOT)
print('R05 original TEST runtime extracted after hash check, historical archive remains untouched')
