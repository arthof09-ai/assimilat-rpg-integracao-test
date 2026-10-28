"""Cold recovery: ZIP CRC + full manifest + independent sqlite audit. No battle execution."""
import argparse,zipfile,tempfile,json,hashlib,subprocess,sys
from pathlib import Path

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(root):
    root=Path(root)
    man=json.loads((root/'SHA256_MANIFEST.json').read_text())
    actual={x.relative_to(root).as_posix() for x in root.rglob('*') if x.is_file() and x.name!='SHA256_MANIFEST.json'}
    if set(man)!=actual:raise AssertionError('MANIFEST_COVERAGE')
    for name,h in man.items():
        if digest(root/name)!=h:raise AssertionError('HASH_FAIL:'+name)
    script=root/'code/r225_independent_readonly_audit.py'
    body=script.read_text()
    if 'import vlab_effects' in body or 'event_commit(' in body:raise AssertionError('AUDITOR_NOT_INDEPENDENT')
    result=subprocess.run([sys.executable,str(script)],cwd=root,env={'PATH':'/usr/bin:/bin'},capture_output=True,text=True,timeout=80)
    if result.returncode:raise AssertionError('SQL_AUDIT:'+result.stdout+' '+result.stderr)
    o=json.loads(result.stdout)
    if o['admitted']!=3 or o['quarantined_preliminary']!=3 or o['odd_half_spells']!=2:raise AssertionError('METRIC_DRIFT')
    return {'status':'PASS_R225_CONFIRMED_DAMAGE_FLOOR_COLD_PORTABLE_TEST_ONLY','manifest_hashes':len(man),**{k:o[k] for k in ('admitted','quarantined_preliminary','commits','odd_half_spells','historical_replays')}}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--archive');p.add_argument('--root');arg=p.parse_args()
    if arg.archive:
        with tempfile.TemporaryDirectory(prefix='R225_COLD_') as d:
            with zipfile.ZipFile(arg.archive) as z:
                if z.testzip() is not None:raise AssertionError('CRC_FAIL')
                z.extractall(d)
            print(json.dumps(verify(d),ensure_ascii=False,indent=2))
    else:print(json.dumps(verify(arg.root),ensure_ascii=False,indent=2))
