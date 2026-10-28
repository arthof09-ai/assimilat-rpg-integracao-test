"""R200: Read-only cold integrity and semantic replay of already stored SQLite fights.
Usage: python R200_COLD_PORTABLE_RECOVERY.py EXTRACTED_ZIP_ROOT [RECEIPT_OUT]
Never runs the fight runner, writes to existing fight databases, or reuses RUN-IDs.
"""
from __future__ import annotations
import json,sys,pathlib,hashlib,subprocess,os,sqlite3

def H(p):
    z=hashlib.sha256()
    with open(p,'rb') as f:
        for block in iter(lambda:f.read(1048576),b''):z.update(block)
    return z.hexdigest()
def check(c,msg):
    if not c:raise AssertionError(msg)
def cold(root,receipt_out=None):
    root=pathlib.Path(root).resolve()
    data=json.loads((root/'R200_SHA256_MANIFEST.json').read_text())
    listed=data['files']
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name!='R200_SHA256_MANIFEST.json' and '__pycache__' not in p.parts}
    check(set(listed)==actual,'MANIFEST_MISSING_OR_ADDITIONAL_FILES')
    for name,item in listed.items():
        p=root/name
        check(p.stat().st_size==item['size'],'SIZE_MISMATCH:'+name)
        check(H(p)==item['sha256'],'HASH_MISMATCH:'+name)
    prev=root/'baseline/VLAB_R199_MAGIC_TRANSFORM_BEAST_COMBAT_MESTRE_ONLY.zip'
    check(H(prev)=='533782992f7c16dfd79c06a7113b38d49d4e487cede9f42c1a19d073de0fd015','R199_BASELINE_BYTE_DRIFT')
    code=root/'new/code'
    sys.path.insert(0,str(code))
    from r200_read_only_audit import audit_one
    report=json.loads((root/'new/evidence/R200_AUDIT.json').read_text())
    runs=json.loads((root/'new/evidence/R200_EXECUTED_FIGHTS.json').read_text())
    dbs=sorted((root/'new/evidence/db').glob('*.sqlite'))
    check(len(runs)==32 and len(dbs)==30,'RUN_OR_DB_DENOMINATOR_DRIFT')
    check(len({r['id'] for r in runs})==32,'RUN_ID_COLLISION')
    check(sum(r['status']=='PRECOMMIT_TIE_HOLD' for r in runs)==2,'INIT_HOLD_DRIFT')
    chk=[audit_one(p) for p in dbs]
    assert len(chk)==report['battles']
    for key,new in [('commits',sum(x['commits'] for x in chk)),('native_events',sum(x['native_events'] for x in chk)),('attacks',sum(x['attacks'] for x in chk)),('KO',sum(x['status']=='FINISHED' for x in chk)),('censored',sum(x['status']=='CENSORED_HORIZON' for x in chk))]:
        check(report[key]==new,'R200_AGGREGATE_DRIFT:'+key)
    tamper=json.loads((root/'new/evidence/adversarial/R200_ADVERSARIAL.json').read_text())
    check(tamper['rejected']==4,'FORGERY_COUNT_DRIFT')
    for x in tamper['clones']:
        db=root/'new/evidence/adversarial'/('R200_FORGERY_'+x['forgery']+'.sqlite')
        try:audit_one(db)
        except AssertionError as err:check(str(err)==x['reason'],'ADVERSARIAL_REASON_DRIFT')
        else:raise AssertionError('SEMANTIC_FORGERY_PASSED:'+x['forgery'])
    env=os.environ.copy();env['PYTHONPATH']=str(code)
    unittest=subprocess.run([sys.executable,'-m','unittest','-q','test_r200_geometry','test_r200_equipment'],cwd=code,env=env,capture_output=True,text=True)
    check(unittest.returncode==0,'SPATIAL_OR_PHYSICAL_UNIT_REGRESSION:'+unittest.stderr[-500:])
    check('Ran 20 tests' in unittest.stderr,'NOT_ALL_20_TESTS')
    html=(root/'new/ui/VLAB_R200_BANCADA_COMBATES_E_EQUIPAMENTOS_OFFLINE.html').read_text()
    check(all(f'data-tab="{x}"' in html for x in ['rapido','padrao','detalhado','combates','r199','r200']),'DASHBOARD_TAB_LOST')
    check('"source_rank":"UNPUBLISHED"' in html or 'NOT_PUBLISHED' in html,'RING_RANK_EVIDENCE_MISSING')
    summary={'result':'PASS_R200_COLD_PORTABLE_RECOVERY','hashes':len(listed),'baseline_r199_sha256':H(prev),'r200_battles':len(chk),'r200_ko':report['KO'],'r200_censored':report['censored'],'r200_precommit_ties':report['precommit_ties'],'commits':report['commits'],'events':report['native_events'],'attacks':report['attacks'],'adversarial_rejected':4,'spatial_and_equipment_regressions':20,'ui_modes':6,'legacy_fights_replayed':0,'new_fights_replayed':0,'magic_ring_rank_certified':False,'terminal_contracts':0,'official_benchmark_cells':0,'production':'HOLD'}
    if receipt_out:pathlib.Path(receipt_out).write_text(json.dumps(summary,indent=2,ensure_ascii=False))
    print(json.dumps(summary,indent=2,ensure_ascii=False))
    return summary
if __name__=='__main__':cold(sys.argv[1] if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parents[2],sys.argv[2] if len(sys.argv)>2 else None)
