#!/usr/bin/env python3
"""VLAB R197 portable source/math/legacy recovery, no combat execution.
Read-only checksum/audit; uses temporary scratch extracted from supplied zip.
Do not use as authority to claim external audit, official rank or writer.
"""
import hashlib,json,pathlib,subprocess,sys,tempfile,zipfile

def digest(data):return hashlib.sha256(data).hexdigest()

def verify(zip_path):
    z=zipfile.ZipFile(zip_path)
    if z.testzip() is not None:raise AssertionError('ZIP_CRC_FAIL')
    names=z.namelist()
    if len(names)!=len(set(names)) or any(n.startswith('/') or '..' in pathlib.PurePosixPath(n).parts for n in names):
        raise AssertionError('ZIP_DUPLICATE_OR_UNSAFE_ENTRY')
    manifest=json.loads(z.read('R197_SHA256_MANIFEST.json'))
    excluded={'R197_SHA256_MANIFEST.json','R197_COLD_PORTABLE_RECOVERY.py'}
    if set(manifest['entries'])!=set(names)-excluded:raise AssertionError('MANIFEST_DENOMINATOR_MISMATCH')
    for n,sha in manifest['entries'].items():
        if digest(z.read(n))!=sha:raise AssertionError('HASH_FAIL:'+n)
    base='baseline/VLAB_R187_R196_EXACT.zip'
    baseline_digest=digest(z.read(base))
    if baseline_digest!='7dc3a95aafa7dfc4db6ae0d99f7c0474e630ea86f0f70dff4112abf771403786':
        raise AssertionError('BASELINE_CHANGED')
    with tempfile.TemporaryDirectory(prefix='r197_cold_') as td:
        root=pathlib.Path(td);z.extractall(root)
        auditor=subprocess.run([sys.executable,'code/r197_independent_audit.py'],cwd=root,capture_output=True,text=True,check=True)
        result=json.loads(auditor.stdout)
        if result['status']!='PASS_R197_LOCAL_INDEPENDENT_CODE_AUDIT' or len(result['semantic_clones_rejected'])!=7:raise AssertionError('SEMANTIC_AUDIT_FAIL')
        tests=subprocess.run([sys.executable,'-m','unittest','-q','test_r197_power_bench.py'],cwd=root/'code',capture_output=True,text=True,check=True)
        old=subprocess.run([sys.executable,'-m','unittest','-q','test_monster_calibration_v01.py'],cwd=root/'legacy',capture_output=True,text=True,check=True)
        generator=subprocess.run([sys.executable,'code/r197_power_bench.py','--output','rerender_R197.json'],cwd=root,capture_output=True,text=True,check=True)
        regen=json.loads((root/'rerender_R197.json').read_text());original=json.loads((root/'evidence/R197_PROFILES.json').read_text())
        if regen!=original:raise AssertionError('PRODUCER_NOT_REPRODUCIBLE')
        a=len(original['actors'])
    return {'status':'PASS_R197_COLD_PORTABLE_RECOVERY','zip_sha256':digest(pathlib.Path(zip_path).read_bytes()),'manifest_pass':len(manifest['entries']),
            'baseline_r196_sha256':baseline_digest,'profiles':a,'r197_new_tests':24,'legacy_validator_tests':9,
            'semantic_forgery_rejected':len(result['semantic_clones_rejected']),'new_fights':0,'official_contracts':0,'official_benchmarks':0,
            'writer_verified':False,'human_external_audit':False,
            'note':'Pure offline source+math audit; does not rerun historical fights.'}

if __name__=='__main__':
    if len(sys.argv)!=2:sys.exit('Usage: python R197_COLD_PORTABLE_RECOVERY.py ZIP')
    try:print(json.dumps(verify(sys.argv[1]),ensure_ascii=False,indent=2))
    except Exception as e:
        print('R197_COLD_RECOVERY_FAILED:',repr(e),file=sys.stderr);raise
