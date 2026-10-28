#!/usr/bin/env python3
"""Verify original recovery bytes without executing any archived program."""
from __future__ import annotations
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_name(name):
    path = PurePosixPath(name.replace('\\', '/'))
    if path.is_absolute() or '..' in path.parts or '\x00' in name:
        raise ValueError('unsafe archive path: ' + name)


def main():
    seen = set()
    counts = {'original_files': 0, 'original_bytes': 0, 'unique_zip_objects': 0,
              'zip_members_crc_verified': 0, 'split_archives': 0, 'existing_bridge_archives': 0}

    def verify_zip(data, depth=0):
        h = digest(data)
        if h in seen:
            return
        seen.add(h)
        if depth > 12:
            raise ValueError('ZIP nesting limit')
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            members = archive.infolist()
            names = [m.filename for m in members]
            if len(names) != len(set(names)):
                raise ValueError('duplicate ZIP member')
            if sum(m.file_size for m in members) > 512 * 1024 * 1024:
                raise ValueError('ZIP expansion limit')
            counts['unique_zip_objects'] += 1
            for member in members:
                safe_name(member.filename)
                if member.is_dir():
                    continue
                if member.file_size > 128 * 1024 * 1024:
                    raise ValueError('ZIP member size limit')
                payload = archive.read(member)  # zipfile validates CRC on complete read.
                counts['zip_members_crc_verified'] += 1
                if member.filename.lower().endswith('.zip'):
                    verify_zip(payload, depth + 1)

    manifest_path = ROOT / 'archive/imported-library/MANIFEST_20261028.json'
    manifest = json.loads(manifest_path.read_text())
    hashes = set()
    for item in manifest['artifacts']:
        rel = item['destination']
        safe_name(rel)
        if not rel.startswith('archive/imported-library/'):
            raise ValueError('unexpected destination')
        data = (ROOT / rel).read_bytes()
        if len(data) != item['bytes'] or digest(data) != item['sha256']:
            raise ValueError('original hash/size mismatch: ' + rel)
        if item['sha256'] in hashes:
            raise ValueError('duplicate original SHA-256 in upload manifest')
        hashes.add(item['sha256'])
        if rel.lower().endswith('.zip'):
            verify_zip(data)
        counts['original_files'] += 1
        counts['original_bytes'] += len(data)

    bridge = json.loads((ROOT / 'archive/vlab/bridge-zip/MANIFEST_20261028.json').read_text())
    for item in bridge['zip_files']:
        data = (ROOT / item['github_path']).read_bytes()
        if len(data) != item['bytes'] or digest(data) != item['sha256']:
            raise ValueError('bridge original hash/size mismatch')
        verify_zip(data)
        counts['existing_bridge_archives'] += 1

    for version in ('R323', 'R324', 'R325', 'R326'):
        folder = ROOT / 'archive/vlab-source' / version
        split = json.loads((folder / 'manifest.json').read_text())
        chunks = []
        for part in split['parts']:
            safe_name(part['file'])
            if Path(part['file']).name != part['file']:
                raise ValueError('part must be a filename')
            data = (folder / part['file']).read_bytes()
            if len(data) != part['bytes']:
                raise ValueError('part size mismatch')
            if 'sha256' in part and digest(data) != part['sha256']:
                raise ValueError('part SHA-256 mismatch')
            if 'git_blob_sha1' in part:
                gh = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
                if gh != part['git_blob_sha1']:
                    raise ValueError('part Git blob mismatch')
            chunks.append(data)
        original = b''.join(chunks)
        if len(original) != split['source_size_bytes'] or digest(original) != split['source_sha256']:
            raise ValueError('reconstructed original mismatch: ' + version)
        with zipfile.ZipFile(io.BytesIO(original)) as archive:
            if len(archive.infolist()) != split['zip_members'] or archive.testzip() is not None:
                raise ValueError('split ZIP integrity mismatch')
        # Historical internal manifest defects are reported separately; never repair source bytes.
        counts['split_archives'] += 1
    print(json.dumps({'status': 'PASS', **counts}, sort_keys=True))


if __name__ == '__main__':
    main()
