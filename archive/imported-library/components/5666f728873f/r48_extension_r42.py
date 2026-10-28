"""Additive lab-only extension of authentic R48/R46 schema gates.
Patch is applied to an isolated COPY of historical modules and NEVER to official runtime.
The original factory and its original regression are left byte-for-byte intact.
"""
from pathlib import Path
import tempfile, shutil, sys, json, hashlib, copy, os
ORIG=Path(os.environ.get('R42_R48_ORIG',str(Path(__file__).parent/'parents'/'r48_original')))
KEY='SBX-VIGILIA-BOREAL-R44-R41-TEST'
SOURCE='3edc2b324ede818b9d7ad75d42f2afa2'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    before={p:sha(ORIG/p) for p in ['r48_factory.py','r48_store.py','legacy/CRAFT-R47-SANDBOX-I0016/baseline/CRAFT-R46-SANDBOX-I0016/r46_evidence.py']}
    with tempfile.TemporaryDirectory(prefix='r42_r48_shadow_') as tmp:
        root=Path(tmp)/'SHADOW_COPY';shutil.copytree(ORIG,root,ignore=shutil.ignore_patterns('__pycache__'))
        factory=root/'r48_factory.py'
        data=factory.read_text(encoding='utf8')
        old="ALLOWED_RECIPES=('SBX-TLI-R44-v1','SBX-MICA-R44-v1')"
        assert data.count(old)==1
        data=data.replace(old,"ALLOWED_RECIPES=('SBX-TLI-R44-v1','SBX-MICA-R44-v1','%s')"%KEY)
        factory.write_text(data,encoding='utf8')
        evidence=root/'legacy/CRAFT-R47-SANDBOX-I0016/baseline/CRAFT-R46-SANDBOX-I0016/r46_evidence.py'
        data=evidence.read_text(encoding='utf8')
        old="len(self.recipes)!=2 or set(self.recipes)!={'SBX-TLI-R44-v1','SBX-MICA-R44-v1'}"
        assert data.count(old)==1
        data=data.replace(old,"len(self.recipes)!=3 or set(self.recipes)!={'SBX-TLI-R44-v1','SBX-MICA-R44-v1','%s'}"%KEY)
        evidence.write_text(data,encoding='utf8')
        sys.path.insert(0,str(root))
        from r48_factory import IntegratedFactory,FactoryError
        from r47_fixtures import recipes_and_sources,make_pair,policy
        from r48_fixtures import lots,order,REVIEW
        sys.path.insert(0,str(Path(__file__).resolve().parent))
        os.environ['R41_R48_DIR']=str(root)
        from r41_pingente_r44_controlado import make_contract,make_lots
        recipes,sources=recipes_and_sources();recipes[KEY]=make_contract()
        sources[SOURCE]={'title':'Cristal de Aurora Boreal','source_status':'LAB_UNVALIDATED_FOR_TRANSFER',
                          'last_edited_at':'2026-10-20T13:00:00Z','url':'https://app.notion.com/p/'+SOURCE,
                          'inventory':'NO_CANONICAL_STOCK_CLAIM'}
        all_lots=lots()+make_lots()
        fac=IntegratedFactory(recipes,all_lots,sources,policy())
        audit0=fac.audit();assert audit0['ok'],audit0
        test=order('tli',4242)
        test['order_id']='SBX-R48-ORDER-R42-PINGENTE'
        test['recipe_key']=KEY
        test['lot_ids']=[x['lot_id'] for x in make_lots()]
        test['measurements']={'ligacao_mecanica_integra':True,'magia_transferida_com_prova_independente':True}
        test['tools']=recipes[KEY]['tools'];test['skills']=recipes[KEY]['skills']
        # Rebinding report identifiers doesn't make its historical signature valid.
        test['report']['recipe_key']=KEY
        test['report']['source_page_id']=SOURCE
        test['report']['source_crn_id']='NONE_LAB_TEST'
        test['report']['lot_ids']=test['lot_ids']
        test['report']['report_id']='SBX-R46-LAUDO-R42-PINGENTE-UNTRUSTED'
        test['attestation']['report_id']=test['report']['report_id']
        beforestock=fac.quantities.copy()
        out=fac.process_batch('SBX-R48-BATCH-R42-PINGENTE',[test],REVIEW)
        assert out['status']=='COMPLETED_WITH_REJECTIONS',out
        one=out['orders'][0]
        assert one['status'].startswith('QUARANTINE'),one
        assert fac.quantities==beforestock
        assert out['physical_products']==0 and out['official_stock_effect']==0
        assert fac.audit()['ok']
        replay=fac.process_batch('SBX-R48-BATCH-R42-PINGENTE',[test],REVIEW)
        assert replay['idempotent_replay'] is True
        tampered=copy.deepcopy(test);tampered['measurements']['magia_transferida_com_prova_independente']=False
        try:fac.process_batch('SBX-R48-BATCH-R42-PINGENTE',[tampered],REVIEW)
        except FactoryError as e:tamper=str(e)
        else:raise AssertionError('tampered idempotent request accepted')
        assert 'IDEMPOTENCY_CONFLICT' in tamper
        output={'state':'PASS_R42_SHADOW_R48_THIRD_RECIPE_ADMISSION','case':KEY,
                'original_factory_source_sha256_before_after_equal':True,
                'original_r48_core_unchanged':True,'shadow_patch_n_modules':2,
                'admission_passes_whitelist_in_SHADOW_only':True,
                'order_status':one['status'],'factory_status':out['status'],
                'native_r47_evidence_status':one['authenticity']['status'],
                'magic_observed':False,'physical_products':0,'official_stock_effect':0,
                'synthetic_lot_stock_preserved':True,'idempotent_identical_request':True,
                'idempotent_tamper_blocked':tamper,'can_install_on_production':False,
                'note':'Only isolated prototype of native code expansion; R46/R47 roots are fixture keys and do NOT attest real-world magic.'}
    assert before=={p:sha(ORIG/p) for p in before}
    return output
if __name__=='__main__':print(json.dumps(run(),indent=2,ensure_ascii=False))
