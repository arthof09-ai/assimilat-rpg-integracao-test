#!/usr/bin/env python3
"""IBX-17: verify the complete R30 distribution, retaining legacy manifests.

No changes to the R17/V05 motor or to prior manifest files.  The R30
manifest supersedes the legacy R29 manifest *for this R30 distribution*.
Optional --v05-zip validates the external historical dependency if mounted.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R30_MANIFEST = 'MANIFESTO_SHA256_LEVELDOWN_R30.json'
LEGACY_MANIFEST = 'MANIFESTO_SHA256.json'
V05_SHA256 = 'bf62fb0eb77bfc29af8b3d0a476b034954275065472bbfccbce519b4f6dbd8d1'


def file_sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root=HERE, v05_zip=None):
    root = Path(root).resolve()
    new_path = root / R30_MANIFEST
    if not new_path.is_file():
        raise AssertionError(f'Manifesto R30 ausente: {new_path.name}')
    if not (root / LEGACY_MANIFEST).is_file():
        raise AssertionError('Manifesto histórico não preservado')
    r30 = json.loads(new_path.read_text(encoding='utf-8'))
    if r30.get('schema') != 'IBX17_LEVELDOWN_MANIFEST_V1':
        raise AssertionError('Schema de manifesto R30 incompatível')
    expected = r30.get('files')
    if not isinstance(expected, dict) or len(expected) != 57:
        raise AssertionError('Denominador R30 inesperado')
    if any(not isinstance(v, str) or len(v) != 64 for v in expected.values()):
        raise AssertionError('Hash listado inválido')
    forbidden = {'', '.', '..', R30_MANIFEST}
    for rel in expected:
        path = Path(rel)
        if (path.is_absolute() or any(part in ('..', '.') for part in path.parts)
                or rel in forbidden or not (root / path).resolve().is_relative_to(root)):
            raise AssertionError(f'Caminho inseguro ou auto-referencial: {rel}')
    found = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.name != R30_MANIFEST}
    expected_keys = set(expected)
    missing = expected_keys - found
    extra = found - expected_keys
    if missing or extra:
        raise AssertionError(f'Arquivos R30 divergentes: ausentes={sorted(missing)} extras={sorted(extra)}')
    bad = [rel for rel, declared in sorted(expected.items()) if file_sha256(root / rel) != declared]
    if bad:
        raise AssertionError(f'SHA-256 divergente: {bad}')
    result = {'r30_files_pass': len(expected), 'missing': 0, 'extra': 0,
              'legacy_manifest_retained': True, 'v05_zip_verified': None}
    if v05_zip is not None:
        v05_zip = Path(v05_zip)
        if not v05_zip.is_file() or file_sha256(v05_zip) != V05_SHA256 or r30['v05_zip_sha256'] != V05_SHA256:
            raise AssertionError('Dependência V05 inexistente ou SHA-256 divergente')
        result['v05_zip_verified'] = True
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Verifica 57 arquivos do R30 e, opcionalmente, o V05')
    parser.add_argument('--v05-zip', type=Path, help='ZIP histórico V05, externo ao pacote R30')
    options = parser.parse_args()
    status = verify(v05_zip=options.v05_zip)
    print('PASS R30: 57/57 hashes; 0 extras, 0 ausentes; manifesto legado preservado.' +
          (' V05 SHA-256 PASS.' if status['v05_zip_verified'] else ' V05 não fornecido (verificação opcional).'))
