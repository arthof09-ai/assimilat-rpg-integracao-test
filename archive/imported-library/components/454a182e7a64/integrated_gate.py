"""MESTRE-SIDE TEST: integrated source-authority gate ahead of existing H2-3 preflight.
Never enables application. Frozen upstream ZIPs rehydrated and hash checked.
"""
from __future__ import annotations
import zipfile,tempfile,hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P2='https://app.notion.com/p/3edc2b324ede811783dfce62058ca6b8'
MIRROR_O='https://app.notion.com/p/7cac2b324ede8294bb7a8169d7a51ad7'
MIRROR_P='https://app.notion.com/p/2d5c2b324ede839895e0815fb2e4fc92'
UPSTREAM={"CRAFT_H23_READINESS_P0_20261021.zip":"f66c91579421120808659ba2850dd8409d83251c33362bad208e1842d8f208bd",
"CRAFT_P2_VARIANT_CHAIN_TEST_20261021.zip":"94e753d82a8515a3c210b3d5d10dbbbb84400879165a04f16c743b64dde69a7e"}

def _import(f,name):
    spec=importlib.util.spec_from_file_location(name,str(f))
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def checked_sources():
    for name,expected in UPSTREAM.items():
        p=ROOT/'upstream'/name
        if hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
            raise ValueError('UPSTREAM_SHA_MISMATCH:'+name)
        with zipfile.ZipFile(p) as z:
            if z.testzip() is not None: raise ValueError('UPSTREAM_ZIP_CRC_FAIL')
    return dict(UPSTREAM)

def integrated_preflight(source_url=P2,source_role='MASTER_CANON_SOURCE',additional_flags=None):
    checked_sources()
    flags=additional_flags or {}
    with tempfile.TemporaryDirectory() as d:
        d=Path(d)
        for name in UPSTREAM:
            with zipfile.ZipFile(ROOT/'upstream'/name) as z:z.extractall(d)
        hroot=d/'CRAFT_H23_READINESS_P0_20261021'
        vroot=d/'CRAFT_P2_VARIANT_CHAIN_TEST_20261021'
        mod1=_import(hroot/'code'/'readiness_delta.py','h23_upstream')
        mod2=_import(vroot/'code'/'variant_gate.py','p2_variant_upstream')
        source=json.loads((vroot/'data'/'source_transcription.json').read_text())['sources']
        master=source['P2_MASTER']
        candidate={'authority':source_role,'surface':'MESTRE_ONLY'}
        valid=(source_url==master['source_url'] and
            mod2.admissible_authority(candidate,'master_recipe_decision'))
        if not valid:
            return {'status':'SOURCE_AUTHORITY_REJECTED','candidate_url':source_url,
                 'candidate_role':source_role,'master_url':P2,'h23a':'HOLD_NO_APPLICATION',
                 'application_authorized':False,'magic_observed':False,
                 'r48_replayed':False,'party_writes':0,'reason':'MASTER_P2_MUST_MATCH_SOURCE_AND_AUTHORITY'}
        master_result=mod1.run_actual_readonly()
        p2=mod2.report(source)
        assert master_result['h23']['h23a']=='HOLD_NO_APPLICATION'
        assert master_result['R48_replayed'] is False
        assert master_result['party_writes']==0
        assert p2['decision']=='HOLD_NO_APPLICATION'
        assert p2['gate']['mirrors_not_authorities']
        return {'status':'HOLD_NO_APPLICATION',
            'candidate_url':source_url,'candidate_role':source_role,
            'h23_documented_fields':master_result['h23']['field_count'],
            'causal_controls_proposed_not_executed':master_result['causal_controls']['count'],
            'p2_salt_pending':p2['gate']['salt_equivalence_unapproved'],
            'p2_energy_stage_pending':p2['gate']['missing_energy_stage'],
            'oil_lot_verified':False,'operator_p2_assigned':False,
            'h23a':master_result['h23']['h23a'],
            'h23b':master_result['h23']['h23b'],
            'source_stabilized':master_result['h23']['source_stabilized'],
            'item_integrated':master_result['h23']['item_integrated'],
            'application_authorized':False,'magic_observed':False,
            'r48_replayed':False,'r48_prior_order':master_result['R48_prior_order'],
            'f5':master_result['f5'],'c19':master_result['c19'],'party_writes':0,
            'flags_not_authority':list(sorted(flags)),'baseline_hashes_valid':True}

if __name__=='__main__':
    print(json.dumps(integrated_preflight(),ensure_ascii=False,indent=2))
