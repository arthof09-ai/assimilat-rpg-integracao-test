"""Cold-run the pinned, self-contained CRAFT/PA package using standard Python."""
import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
EXPECTED_SHA = '215c895a9e4bd3da99172cca429ca6b986ee2b6b895c13c53559657576832cc1'

def main():
    source = HERE / 'CRAFT_PA_NATIVE_20261029.zip'
    if hashlib.sha256(source.read_bytes()).hexdigest() != EXPECTED_SHA:
        raise ValueError('ARCHIVE_SHA_MISMATCH')
    with tempfile.TemporaryDirectory(prefix='craft-pa-native-') as directory:
        with zipfile.ZipFile(source) as archive:
            if archive.testzip() is not None:
                raise ValueError('ZIP_CRC_FAILED')
            if sum(item.file_size for item in archive.infolist()) > 25_000_000:
                raise ValueError('ARCHIVE_SIZE_LIMIT')
            for item in archive.infolist():
                path = PurePosixPath(item.filename)
                if path.is_absolute() or '..' in path.parts:
                    raise ValueError('ZIP_PATH_TRAVERSAL')
                if (item.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('ZIP_SYMLINK_REJECTED')
            archive.extractall(directory)
        run = subprocess.run([sys.executable, '-B', 'verify_release.py'],
            cwd=directory, capture_output=True, text=True, timeout=120)
        print(run.stdout)
        if run.returncode:
            raise RuntimeError(run.stderr)
        result = json.loads(run.stdout.strip().splitlines()[-1])
        if result.get('tests') != 149 or result.get('status') != 'LOCAL-TEST-PASS':
            raise ValueError('INCOMPLETE_ACCEPTANCE')
        print('CRAFT_PA_NATIVE_COLD_PASS: 149 tests, 248 hashed files, zero remote writes')

if __name__ == '__main__':
    main()
