"""R219: portable COLD readback. Validates hashes, original historical R218 baseline,
all admitted new source-native SQLite and quarantine; never invokes any combat runner."""
from pathlib import Path
import sys,hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'code'))
from r219_r220_independent_chronology import verify

def main():
 manifest=json.loads((ROOT/'MANIFEST_SHA256.json').read_text())
 if not manifest:raise AssertionError('EMPTY_MANIFEST')
 for rel,want in manifest.items():
  p=ROOT/rel
  if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=want:raise AssertionError('R219_SHA_MISMATCH:'+rel)
 baseline=ROOT/'baseline/VLAB_R218_ORIGINAL_READ_ONLY.zip'
 if hashlib.sha256(baseline.read_bytes()).hexdigest()!='19a1223fd1a92451a5e92adee1eb87aa0965c68a3a3b4b16f2946a915190d40b':raise AssertionError('HISTORIC_R218_SHA_DRIFT')
 with zipfile.ZipFile(baseline) as z:
  if z.testzip() is not None:raise AssertionError('HISTORIC_R218_CRC')
 result=verify(ROOT,version="219")
 print('PASS_R219_COLD_PORTABLE_NATIVE_SOURCE_SCIENCE')
 print(json.dumps({'manifest_files':len(manifest),'admitted':result.get('admitted',result.get('valid')),'blocked':result['blocked'],'commits':result['commits'],'events':result['events'],'historical_replays':0,'production':'HOLD'},ensure_ascii=False,indent=2))
 return result
if __name__=='__main__':main()
