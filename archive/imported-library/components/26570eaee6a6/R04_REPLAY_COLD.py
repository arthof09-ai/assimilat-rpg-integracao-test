"""Offline read-only cold replay of the ORIGINAL R39->R28->R27->R26+CRAFT chain.

Usage: Python 3.11+ stdlib, `python R04_REPLAY_COLD.py` from unpacked R04.
Creates a temporary sandbox; fixture legacy path is created only if absent,
removed in finally. Does NOT modify or install the native official RPG system.
"""
from __future__ import annotations
import hashlib,json,os,re,subprocess,sys,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SRC=ROOT/'SOURCE_R39_FROZEN.zip'
KNOWN={
 'SOURCE_R39_FROZEN.zip':'daf7d6d5058fca308df62bc593795868df080cded1107edb2f80cf8a11a71b32',
 'CRAFT_PA_CORRIGENDA_MESTRE_TEST_20261020.zip':'ab880817ca732743011ee1f8f0269e303f6564e3a98c9a50fdf57ef7cd6320fa',
 'PA_R28_QMC05_NATIVO_INTEGRADO_TEST_20261020.zip':'68acc4405250cbf03a89924fa4df1f3d36586f26a5a903610c6600e8f26a391e',
}
def sha(raw):return hashlib.sha256(raw).hexdigest()

def safe_extract_zip(p:Path,out:Path):
    out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None,'CRC_FAIL:'+p.name
        for n in z.namelist():
            path=(out/n).resolve()
            assert path.is_relative_to(out.resolve()),'ZIP_TRAVERSAL'
        z.extractall(out)

def run(cmd,cwd,env=None):
    p=subprocess.run(cmd,cwd=cwd,env=env or os.environ.copy(),capture_output=True,text=True,timeout=100)
    return p,p.stdout+'\n'+p.stderr

def verify_manifest():
    mf=ROOT/'MANIFEST_SHA256.json'
    if not mf.is_file():return 'UNSEALED_STAGING'
    data=json.loads(mf.read_text())
    for name,info in data['files'].items():
        raw=(ROOT/name).read_bytes()
        assert len(raw)==info['bytes'] and sha(raw)==info['sha256'],'MANIFEST_MISMATCH:'+name
    return str(len(data['files']))+'/'+str(len(data['files']))+'_PASS'

def main():
    manifest=verify_manifest()
    assert sha(SRC.read_bytes())==KNOWN[SRC.name],'WRONG_R39_SOURCE'
    with tempfile.TemporaryDirectory(prefix='pa_r04_cold_') as td:
        tmp=Path(td)
        r39=tmp/'r39';safe_extract_zip(SRC,r39)
        craftzip=r39/'CRAFT_PA_CORRIGENDA_MESTRE_TEST_20261020.zip'
        assert sha(craftzip.read_bytes())==KNOWN[craftzip.name]
        r29zip=r39/'PA_R29_R38_CONSULTOR_OPERACIONAL_TEST_20261020.zip'
        r29=tmp/'r29';safe_extract_zip(r29zip,r29)
        r28zip=r29/'PA_R28_QMC05_NATIVO_INTEGRADO_TEST_20261020.zip'
        assert sha(r28zip.read_bytes())==KNOWN[r28zip.name]
        r28=tmp/'pa_r28';safe_extract_zip(r28zip,r28)
        craftroot=tmp/'craft_v12';safe_extract_zip(craftzip,craftroot)
        craft=craftroot/'CRAFT_RECIPE_PA_LAB_v1_2_CORRIGIDO'
        provider=r28/'provider_r27'
        # The historical R22 test expects a local absolute fixture. The actual
        # fixture bytes are taken from the previously frozen R23 archive.
        fixturezip=provider/'engine_r26/baseline_r25/BASELINE_R23_IMUTAVEL.zip'
        legacy=Path('/mnt/data/pa_r21_work/ATIVACOES_HISTORICAS_R21.csv')
        assert not legacy.parent.exists(),'HISTORICAL_PATH_IN_USE_REFUSE_OVERWRITE'
        with zipfile.ZipFile(fixturezip) as z:
            assert z.testzip() is None
            original_csv=z.read('compat_r21/ATIVACOES_HISTORICAS_R21.csv')
        fixture_sha=sha(original_csv)
        legacy.parent.mkdir(parents=True)
        try:
            legacy.write_bytes(original_csv)
            assert sha(legacy.read_bytes())==fixture_sha
            native,native_log=run([sys.executable,'RUN_ALL_R28.py'],r28)
            report=json.loads((r28/'RUN_ALL_R28_RESULT.json').read_text())
        finally:
            legacy.unlink(missing_ok=True)
            legacy.parent.rmdir()
            assert not legacy.exists(),'FIXTURE_CLEANUP_FAILED'
        assert native.returncode==0 and report['all_pass'] and report['tests_total']==448, native_log[-1700:]
        previous,prev_log=run([sys.executable,'run_lab.py'],craft)
        assert previous.returncode==0,'CRAFT_V12_TESTS_FAILED:'+prev_log[-1100:]
        craftrep=json.loads(previous.stdout)
        assert craftrep['current']=={'tests':56,'failures':0,'errors':0,'success':True}
        assert craftrep['legacy']=={'tests':26,'failures':0,'errors':0,'success':True}
        env=os.environ.copy();env['R04_R27_DIR']=str(provider);env['R04_CRAFT_DIR']=str(craft)
        boundary,boundary_log=run([sys.executable,'-m','unittest','-q','test_r04_native_binding'],ROOT,env)
        assert boundary.returncode==0 and 'Ran 30 tests' in boundary_log and 'OK' in boundary_log and 'skipped=' not in boundary_log,'R04_NEW_TESTS_FAILED:'+boundary_log[-1500:]
        qmc=r28/'CRAFT-QMC04'
        stem='https://app.notion.com/p/3edc2b324ede816f98a1fa7babd3c0d3'
        cmd=[sys.executable,'QMC-05/qmc05.py','--url',stem,'--readback','QMC-05/holdout/lamina.txt','--pa-r28']
        legacy_cli,log_hist=run(cmd,qmc);assert legacy_cli.returncode==0,log_hist[-500:]
        hist=json.loads(legacy_cli.stdout)
        proposed_cli,log_prop=run(cmd+['--pa-projeto-json','../PROJETO_COMPATIVO_LAMINA_E3.json'],qmc)
        assert proposed_cli.returncode==0,log_prop[-500:]
        prop=json.loads(proposed_cli.stdout)
        assert hist['historico']['projecao_energetica'] is None
        assert hist['cenario_novo'] is None
        assert hist['governanca']['notion_write'] is False
        assert prop['cenario_novo']['r27_result']['custo_pa']['pa_total_no_cenario'] is None
        assert prop['cenario_novo']['r27_result']['gate']=='CONSULTA_TEST_PARCIAL_COM_PENDENCIAS'
        # Compare original native CLI outputs against this release's pinned ones.
        assert hist==json.loads((ROOT/'R04_QMC05_HISTORIC_NATIVE.json').read_text())
        assert prop==json.loads((ROOT/'R04_QMC05_E3_NATIVE.json').read_text())
        return {'stage':'R04_TEST_COLD_REPLAY','status':'PASS',
                'native_r28_tests':448,'craft_v12_current_tests':56,
                'craft_v12_legacy_tests':26,'new_r04_binding_tests':30,
                'unique_methods_this_run':560,'qmc05_cli_scenarios':2,
                'manifest':manifest,
                'source_sha256':KNOWN[SRC.name],
                'r28_original_sha256':KNOWN[r28zip.name],
                'craft_original_sha256':KNOWN[craftzip.name],
                'legacy_r21_fixture_sha256':fixture_sha,
                'legacy_fixture_deleted':not legacy.exists(),
                'qmc05_historical_pa':None,'qmc05_proposed_incomplete_total':None,
                'r04_binding_installed_in_craft':False,
                'notion_write':False,'party_write':False,'official_item_changes':0,
                'production':'HOLD'}

if __name__=='__main__':
    report=main()
    print(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2))
