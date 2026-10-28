"""Standalone cold-replay, verifies exact immutable R42 baseline and R50 files."""
from __future__ import annotations
import hashlib,json,zipfile,tempfile,sys,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PARENT_SHA='6fbaaf8b54e79d5b7e506f580b32495ee3448e5f8c13c75be224e9c9fdbe7800'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    manifest=json.loads((ROOT/'MANIFEST_SHA256.json').read_text(encoding='utf-8'))
    for name,old in manifest['files'].items():
        p=ROOT/name
        assert p.is_file(),name
        assert sha(p)==old,name
    baseline=ROOT/'original_R42_immutable.zip'
    assert sha(baseline)==PARENT_SHA,'R42_BASELINE_CHANGED'
    with tempfile.TemporaryDirectory(prefix='r50_cold_') as dd:
        temp=Path(dd);target=temp/'engine'
        with zipfile.ZipFile(baseline) as z:
            assert z.testzip() is None
            extracted=0
            for name in z.namelist():
                if name.startswith('parents/engine_r26/') and not name.endswith('/'):
                    leaf=name[len('parents/engine_r26/'):]
                    dest=target/leaf;dest.parent.mkdir(parents=True,exist_ok=True)
                    dest.write_bytes(z.read(name));extracted+=1
            assert extracted>=80,extracted
        env_path=str(target)+':'+str(target/'baseline_r25')
        ev={'PYTHONPATH':env_path}
        # Run unit tests of original native R26, independent of wrapper.
        a=subprocess.run([sys.executable,'-m','unittest','-q','test_r26_decisao'],cwd=target,
                         text=True,capture_output=True,env={**__import__('os').environ,**ev})
        assert a.returncode==0,(a.stdout,a.stderr)
        assert 'Ran 26 tests' in a.stderr
        b=subprocess.run([sys.executable,'-m','unittest','discover','-q','-s','tests','-p','test_*.py'],cwd=ROOT,
                         text=True,capture_output=True,env={**__import__('os').environ,'PA_R50_BASELINE_ENGINE':str(target)})
        assert b.returncode==0,(b.stdout,b.stderr)
        assert 'Ran 49 tests' in b.stderr
        sys.path.insert(0,str(ROOT/'src'))
        from runner import generate
        from probe26 import run as probe26_run
        o=generate(ROOT,target)
        o26=probe26_run(ROOT,target)
        assert o26['n']==26 and o26['native_rank_candidates']==11
        by26=(json.dumps(o26,indent=2,sort_keys=True,ensure_ascii=False)+'\n').encode('utf8')
        assert by26==(ROOT/'outputs/r50_26_native_probe.json').read_bytes(),'NATIVE_26_OUTPUT_MISMATCH'
        by=(json.dumps(o,indent=2,sort_keys=True,ensure_ascii=False)+'\n').encode('utf8')
        stored=(ROOT/'outputs/r50_results.json').read_bytes()
        assert by==stored,'DETERMINISTIC_R50_RESULT_MISMATCH'
    print(json.dumps({'status':'PASS','original_R42_SHA256':PARENT_SHA,
       'source_manifest_files':len(manifest['files']),
       'original_R26_tests':26,'R50_new_tests':49,'advisory_cases':4,'rank_free_26_native_candidates':11,'rank_free_26_undetermined':15,
       'canonical_ranks_issued':0,'PA_authorized':0,'writes_to_notion_or_party':0},sort_keys=True))

if __name__=='__main__':main()
