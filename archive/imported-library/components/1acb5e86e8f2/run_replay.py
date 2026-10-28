"""Portable replay in clean directory, does not overwrite any historic store.
Executes PA R27/R26 original, CRAFT v1.2 preflight and 55 new tests,
read-only audits FC04 evidence. No R48 factory fabrication is possible without
verified original binary and legitimate R46/R47 evidence (fail closed).
"""
from __future__ import annotations
import hashlib,json,os,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
HASHES={
 'CRAFT_PA_CORRIGENDA_MESTRE_TEST_20261020.zip':'ab880817ca732743011ee1f8f0269e303f6564e3a98c9a50fdf57ef7cd6320fa',
 'PA_R28_QMC05_NATIVO_INTEGRADO_TEST_20261020.zip':'68acc4405250cbf03a89924fa4df1f3d36586f26a5a903610c6600e8f26a391e',
 'R48_FC04_BASELINE_PRESERVADA.zip':'5756bdf2e6e0550336d483c0c749a411ab345bf39b1168d585d1a883f077bf9b'
}
def dump(p,ob):p.write_text(json.dumps(ob,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
def main():
    result={'baseline_hashes':{},'pa':{},'tests':{},'r48':{},'official_writes':0,'rc5_approved':False}
    for filename,required in HASHES.items():
        p=ROOT/'baselines'/filename;actual=hashlib.sha256(p.read_bytes()).hexdigest()
        result['baseline_hashes'][filename]={'actual':actual,'expected':required,'verified':not required or actual==required}
        if required and required!=actual:raise RuntimeError('BASELINE_HASH_DRIFT:'+filename)
    with tempfile.TemporaryDirectory(prefix='craft_replay_clean_') as tmp:
        temp=Path(tmp)
        with zipfile.ZipFile(ROOT/'baselines/R48_FC04_BASELINE_PRESERVADA.zip') as z:z.extractall(temp/'FC04_UNPACK')
        with zipfile.ZipFile(ROOT/'baselines/PA_R28_QMC05_NATIVO_INTEGRADO_TEST_20261020.zip') as z:
            for m in z.namelist():
                if m.startswith('provider_r27/') and not m.endswith('/'):
                    z.extract(m,temp/'R28')
        provider=temp/'R28/provider_r27';sys.path.insert(0,str(provider))
        from ponte_pa_craft_r27 import consultar_ficha_craft
        request=json.loads((ROOT/'fixtures/pa_r27_request.json').read_text())
        expected=json.loads((ROOT/'fixtures/pa_r27_receipt_fresh_R26_UNCHANGED.json').read_text())
        actual=consultar_ficha_craft(request)
        assert actual==expected,'EXTERNAL_PA_REQUERY_MISMATCH'
        sys.path.insert(0,str(ROOT))
        from pa_nac_preflight import gate
        recipe=json.loads((ROOT/'fixtures/recipe_v1_3_no_false_yield.json').read_text())
        checked=gate(recipe,actual,r48_executable=True,r48_recipe_executed=False)
        assert checked['pa_version_compatible'] is True
        assert checked['pa_provider_reported_total_not_approved']['pa_por_dia']==12
        assert checked['pa_provider_reported_total_not_approved']['pa_ativacoes_no_cenario']==14
        assert 'PA_R26_STALE_ACTIVE_TARIFF' not in checked['non_pa_gates']
        result['pa']={'real_r27_r26_invoked':True,'exact_original_output_reproduced':True,'daily':12,'activation':7,'two_activations':14,'scenario':26,'r48_and_magic_still_blocked':True}
        env={**os.environ,'CRAFT_FC04_ROOT':str(temp/'FC04_UNPACK/CRAFT-R48-B30-22-FC04'),
             'PYTHONPATH':str(ROOT.parent)}
        cmd=[sys.executable,'-m','unittest','-v',
             ROOT.name+'.code.test_pingente_bridge',ROOT.name+'.code.test_maturity_and_readback']
        t=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,cwd=str(ROOT.parent),check=False)
        (ROOT/'outputs/LAST_REPLAY_TESTS.log').write_text(t.stdout)
        assert t.returncode==0,t.stdout[-3000:]
        assert 'Ran 55 tests' in t.stdout
        result['tests']={'current_own_tests':55,'failures':0,'run_in_clean_temp':True}
        from importlib import import_module
        sys.path.insert(0,str(ROOT.parent))
        module=import_module(ROOT.name+'.code.run_pingente_bridge')
        # Crucial: source code is not downloaded from Library: native R48 must fail-closed.
        admission_result=module.main(temp/'MISSING_R48_FACTORY_SOURCE')
        result['r48']={'fc04_archive_readback_reexecuted_by_tests':True,
            'factory_binary_recovered':False,'pingente_r48_real_receipt':False,
            'admission_status':admission_result['r48_gate'],
            'admission_block_count':admission_result['admission_block_count'],
            'control_deck':5,'physical_magic_verified':0}
    dump(ROOT/'outputs/REPLAY_SUMMARY.json',result)
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return result
if __name__=='__main__':main()
