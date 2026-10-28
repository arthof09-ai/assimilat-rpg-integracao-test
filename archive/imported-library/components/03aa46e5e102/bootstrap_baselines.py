from pathlib import Path
import zipfile,hashlib,json
ROOT=Path(__file__).resolve().parent.parent
Z=ROOT/'BASELINES'/'PA_UNIVERSAL_R04_TEST_20261017.zip'
EXPECTED='2c64788b33b6e486f3edc45334b462f88fce8fb2db02fc742aa6b0b2e954cc46'
sha=hashlib.sha256(Z.read_bytes()).hexdigest()
assert sha==EXPECTED,(sha,EXPECTED)
dest=ROOT/'BASELINES'/'R04_EXTRAIDO'
with zipfile.ZipFile(Z) as z:
 assert z.testzip() is None
 z.extractall(dest)
print(json.dumps({'baseline':'R04','verified_sha256':sha,'zip_files':49,'extracted':str(dest),'status':'PASS'},ensure_ascii=False))
