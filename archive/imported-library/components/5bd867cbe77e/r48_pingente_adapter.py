"""Minimal additive input adapter to ORIGINAL R48 schema, MESTRE-SIDE TEST.
No simulation of R48, no cert issuance, no magical efficacy claim, no inventory write.
Can produce a candidate recipe contract and a strict FAIL-CLOSED admission report.
Requires ORIGINAL verified R48 engine and external R46/47 evidence to run factory.
"""
from __future__ import annotations
import copy, hashlib, json
from pathlib import Path

CASE='LAB-CRAFT-VIGILIA-BOREAL-20261020-001'
KEY='SBX-VIGILIA-BOREAL-R48-TEST-v1' # sandbox key, NOT REC-ID
CORE='3edc2b324ede818b9d7ad75d42f2afa2'
HERB='3edc2b324ede81deb8cec70bf5ca7150'
FIBER='3f3c2b324ede815ab04ace5bd1074e79'
EXPECTED_R48_SHA256='872dc5bf1e588a9ba6f4c45421a4dddbbe7d261842a4e951fd684bfc374c6801'
EXPECTED_STORE_SHA256='e6f684e80e0d5c95dff8ea94cbae985b0a8e046b48886d593d6e49534f046bd1'
EXPECTED_R46_SHA256='c869d80f243b349d817c63bd0c40fc08d7b43c98ce54ec9c91d62cd42c73c85e'
HISTORIC_KEYS={'SBX-TLI-R44-v1','SBX-MICA-R44-v1'}

class AdapterBlocked(RuntimeError): pass

def digest(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def verify_orig_engine(root:Path) -> dict:
    """Authenticate three original file hashes before any engine import or in-memory patch.
    Does NOT claim anything about original files if they are absent.
    """
    root=Path(root)
    check=[(root/'r48_factory.py',EXPECTED_R48_SHA256),
           (root/'r48_store.py',EXPECTED_STORE_SHA256),
           (root/'legacy/CRAFT-R47-SANDBOX-I0016/baseline/CRAFT-R46-SANDBOX-I0016/r46_evidence.py',EXPECTED_R46_SHA256)]
    defects=[];checks=[]
    for p,expect in check:
        got=hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
        good=got==expect
        checks.append({'path':str(p),'expected_sha256':expect,'observed_sha256':got,'matched':good})
        if not good:defects.append(('HASH_MISMATCH' if got else 'ORIGINAL_BINARY_NOT_MATERIALIZED')+':'+p.name)
    return {'ok':not defects,'checks':checks,'defects':defects,'engine_executed':False}

def map_recipe(recipe:dict, pa:dict, archived_recipe_contract:dict) -> dict:
    """Wire candidate for R48; no order, measured report, attestation or product.
    'archived_recipe_contract' is a READ-ONLY R48 checkpoint (schema evidence).
    """
    if recipe.get('case_id') != CASE or not recipe.get('fixture_only'):
        raise AdapterBlocked('WRONG_OR_NON_TEST_CASE')
    if any(recipe.get(x) for x in ('request_publish','request_fabricate','request_write')):
        raise AdapterBlocked('OFFICIAL_WRITE_FORBIDDEN')
    bom=recipe.get('bom',[])
    links=[{'source_page_id':str(x['source_ref']).split('/p/')[-1],
            'quantity':x['qty'], 'unit':x['unit'], 'role':x['role'],
            'evidence_kind':x['classification'], 'id':x['id']} for x in bom]
    if {x['source_page_id'] for x in links}!={CORE,HERB,FIBER}:
        raise AdapterBlocked('SOURCE_SET_CHANGED')
    if not all(x['quantity']>0 for x in links):raise AdapterBlocked('NONPOSITIVE_BOM')
    ops=recipe.get('operations',[])
    if len(ops)!=4:raise AdapterBlocked('OPERATIONS_CHANGED')
    available={x['id'] for x in bom}
    for op in ops:
        for x in op['inputs']:
            if x not in available:raise AdapterBlocked('PROCESS_INPUT_NOT_PRODUCED:'+x)
        available.update(op['outputs'])
    if recipe['final_node'] not in available:raise AdapterBlocked('FINAL_NODE_UNREACHABLE')
    if any(not isinstance(x.get('source_page_id'),str) for x in links):raise AdapterBlocked('NO_SOURCE_ID')
    if not pa.get('pa_version_compatible'):raise AdapterBlocked('PA_PREVALIDATOR_NOT_COMPATIBLE')
    if pa.get('pa_provider_reported_total_not_approved',{}).get('pa_por_dia')!=12:
        raise AdapterBlocked('PA_PROVIDER_RECEIPT_CHANGED')
    if pa.get('pa_provider_reported_total_not_approved',{}).get('pa_ativacoes_no_cenario')!=14:
        raise AdapterBlocked('PA_ACTIVATION_SCENARIO_CHANGED')
    if not {a['key'] for a in archived_recipe_contract.values()}>=HISTORIC_KEYS:
        raise AdapterBlocked('ORIGINAL_R48_RECIPE_CONTRACT_UNVERIFIED')
    example=archived_recipe_contract['SBX-CHITINCASE-CRAFT-FC03-v1']
    # Adapts only the R48 field names observable in an authenticated historical snapshot.
    # R46 supports mm,count,bool in the original; magic observables NOT a known R46 type.
    proposed={
     'key':KEY, 'namespace':'SBX-CRAFT-R44-I0016',
     'design_id':CASE,'name':'Pingente da Vigília Boreal — LAB TEST',
     'family':'acessório mágico / luz pessoal / efeito ativo proposto',
     'status':'EXPERIMENTAL_DESIGN_ONLY','source_status':'FONTE_MESTRE + PS_NAO_P4',
     'source_page_id':CORE,'source_crn_id':'LAB_ONLY_NOT_CRN_NOT_REC_ID',
     'inputs':[{'source_page_id':x['source_page_id'],'quantity':x['quantity'],'unit':x['unit']} for x in links],
     'output':{'name':'Pingente da Vigília Boreal TEST','quantity':1,'unit':'pingente_TEST',
               'function':'luz passiva 1m + percepção visual local sob escuridão mágica PROPOSTA NÃO OBSERVADA'},
     'steps':[{'seq':i+1,'name':op['id'],'minutes_proposed':None} for i,op in enumerate(ops)],
     'tools':[x['id'] for x in recipe['manufacture']['equipment']],
     'skills':[recipe['manufacture']['specialist']['competence']],
     'qa_rules':[], # fail-closed: no magical R46 observed field is defined by original
     'knowledge':'LAB_ONLY_NOT_PLAYER_KNOWLEDGE',
     'official_rec_id':None,'official_product_id':None,
     'mechanical_bonus':0,'testable_only_in_sandbox':True,
     'source_qa_status':'NO_R46_OBSERVED_MAGIC_OR_PHYSICAL_LAUDO',
     'pa_contract':'PA-CRAFT-QMC05-COMPAT-R27/1.0.0-TEST',
     'pa_receipt_input_sha256':pa['pa_receipt_id'],
     'pa_day':12,'pa_activation':7,'activation_count':2,
     'critical_unknowns':[
        'SOURCE_FIBER_PS_NOT_P4', 'MATERIAL_LOTS_AND_MASS_NOT_OBSERVED',
        'LUMINANCE_RETENTION_NOT_OBSERVED','DARKNESS_DISRUPTION_NOT_OBSERVED',
        'R46_MAGIC_SENSOR_CONTRACT_ABSENT','R47_INDEPENDENT_CUSTODY_ABSENT',
        'SPECIALIST_AND_CTE_NOT_VERIFIED','ALLOWLIST_REQUIRES_SCOPED_TEST_ADAPTER'],
     'reference_schema_from_fc04':list(example.keys()),
    }
    return {'schema':'CRAFT-PINGENTE-TO-R48-CANDIDATE-v1',
     'kind':'INPUT_ADAPTER_ONLY_NOT_FACTORY_OUTPUT',
     'case_id':CASE,'recipe_candidate':proposed,
     'trace_bom':links,'trace_steps':ops,
     'r48_expected_order_fields': ['order_id','recipe_key','lot_ids','measurements','tools','skills','report','attestation'],
     'r46_report_expected_schema':'R46-LAUDO-v1',
     'r47_attestation_expected_schema':'R47-AUTHENTICITY-v1',
     'factory_reception':'NOT_ATTEMPTED_WITHOUT_VERIFIED_BINARY_AND_LAUDOS',
     'official_writes':0,'physical_magic_proven':False}

def admission(recipe:dict, pa:dict, archived_recipes:dict, root:Path) -> dict:
    candidate=map_recipe(recipe,pa,archived_recipes)
    binary=verify_orig_engine(root)
    orig_types=['SBX-TLI-R44-v1','SBX-MICA-R44-v1']
    blocker_codes=[]
    if not binary['ok']:blocker_codes+=binary['defects']
    # Actual original runtime recognizes just two keys. Extension REQUIRES scoped review.
    if KEY not in orig_types:blocker_codes.append('R48_ORIGINAL_ALLOWLIST_REJECTS_PINGENTE')
    blocker_codes += ['R46_MAGIC_QA_SCHEMA_UNSUPPORTED', 'R47_SIGNED_REPORT_NOT_PROVIDED',
                      'R48_PRODUCTION_REQUEST_NOT_AUTHORIZED', 'MAGICAL_TRANSFER_NOT_OBSERVED']
    return {'case_id':CASE,'schema':'CRAFT-R48-ADMISSION/1.0-TEST',
        'adapter_contract_sha256':digest(candidate), 'status':'BLOCKED_BEFORE_R48_ORDER',
        'engine_evidence':binary,'r48_stored_recipes':orig_types,
        'blocks':blocker_codes,'missing_order_inputs':['lot_ids_synthetic_only','R46_measured_report','R47_attestation'],
        'original_engine_invoked':False,'r48_receipt':None,
        'candidate':candidate,'official_inventory_consumed':0,'RC5':False}
