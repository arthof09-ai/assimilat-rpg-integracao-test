"""CRAFT LAB extension: evidence qualification for existing H2-3.
Not an engine, not a recipe creator, not a PA calculator, not a magic witness.
No physical stock mutability and no successful in-game execution can be inferred.
"""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
BASE_SHA='a0a2ed07a504edc67014d80bb63d6787afb9a0b4c2d53ca52371f7909a20d030'
def read_evidence():
    return json.loads((ROOT/'inputs/CANONICAL_SOURCE_EVIDENCE_POSTH2P2.json').read_text(encoding='utf-8'))
def qualify_finished_oil(evidence):
    """A catalogue, formula or price never becomes a stock batch.
    A hypothetical future batch with documentation is STILL pending external physical
    or in-game authority; this function only determines documentary candidacy.
    """
    candidates=[]
    for row in evidence['oil_inventory_evidence']:
        missing=[k for k in ('lot_id','quantity_available','quality_record','custody') if row.get(k) is None]
        product_only=row['kind'] in ('CANONICAL_RECIPE_PAGE','HISTORICAL_RECIPE_COPY','HISTORICAL_PRICE_RECORD')
        candidates.append({'id':row['id'],'source':row['url'],'kind':row['kind'],
                           'status':'DOCUMENT_ONLY_NOT_STOCK' if product_only else 'BATCH_EVIDENCE_INCOMPLETE',
                           'missing':missing,'finished_oil_usable':False,'quantity_consumed':0})
    return {'sources_examined':len(candidates),'usable_lots':0,'oil_preparation_performed':False,
            'candidate_rows':candidates,'search_scope_non_exhaustive':True,
            'canonical_item_fiche_exists':True,'stock_exists_somewhere':None}
def qualify_operator(evidence):
    return {'operator_candidates_documented':len(evidence['operator_candidates']),
            'assigned_authorized_operator':None,
            'operator_knowledge_of_p2':None,
            'source_confidence':'MESTRE_MIRROR_OR_PROPOSED_NPC_ONLY',
            'operator_competence_gate':'CANDIDATES_IDENTIFIED_BUT_NOT_CERTIFIED_FOR_THIS_ATTEMPT',
            'roll_authorized':False}
def p2_materials(evidence):
    p2=evidence['P2']; out=[]
    for itm in p2['items']:
        out.append({'material_id':itm['slug'],'quantity_from_canon':itm['qty'],
                    'physical_unit':None,'lot_id':None,'lot_qty_confirmed':None,
                    'step_match':itm['used_in_text'],
                    'identity_resolved':itm['slug']!='sal_geodo_santo',
                    'energy_step_resolved':False if itm['slug']=='energy_choice_xor' else None,
                    'source_provenance':'P2_CANONICAL_BOM','used':0})
    return out

def h2_3_admission(evidence):
    # Use authoritatively restored source data: no free-form success flag/fiction can qualify.
    p2=evidence['P2'];oil=qualify_finished_oil(evidence);op=qualify_operator(evidence)
    blockers={
      'P2_SALT':p2['salt_decision'] is None,
      'P2_ENERGIZATION':p2['energy_step_authorized'] is None,
      'P2_PATTERN_SPEC':not p2['pattern_geometry_validated'],
      'OIL_VERIFIED_LOT':oil['usable_lots']!=1,
      'NON_OIL_INPUT_LOTS':True, # no production lot evidence for other 6 ingredients
      'PARCHMENT_PHYSICAL_LOT':True,
      'OPERATOR_ASSIGNED_AND_FORMULA_KNOWN':op['assigned_authorized_operator'] is None,
      'ENERGIZER_LOT_AND_BRANCHED_METHOD':True,
      'SCENE_ADJUDICATOR_AND_OBSERVABLE_TARGET':True,
      'ACTION_AUTHORIZATION_AND_CUSTODY':True,
    }
    assert all(blockers.values()),'This snapshot only contains unresolved source/lot evidence'
    return {'experiment':'H2-3 P2 isolada em pergaminho',
            'substrate_category_authorized':True,
            'substrate_specific_lot_verified':False,
            'bom_lines':p2_materials(evidence),
            'stage_A':'HOLD_NO_APPLICATION',
            'stage_B':'NOT_REACHABLE_WITHOUT_STAGE_A_AND_VALID_EFFECT_TARGET',
            'blocking_dimensions':blockers,'blocker_count':len(blockers),
            'finished_oil':oil,'operator':op,
            'controlled_actor_actions':0,'consumed_units':0,'new_R48_orders':0,
            'in_game_magic_observations':0,
            'magical_effect_claim':False,
            'certified_attestation':None,
            'item_integrated':False,'source_stabilized':False,
            'first_legal_unblocked_step':'READ_P2_AND_PREPARE_DOCUMENTARY_TICKET_ONLY',
            'needs_master_decisions':['P2-SALT-01','P2-ENERGY-02'],
            'cross_effect_confounds':['P2_OWN_ENERGIZER','P2_INSCRIPTION_ONLY_CONTROL','SOURCE_REMOVE_COMPARE']}

def evaluate_fixture(batch):
    # A synthetic batch can test the record schema, not prove that a bottle exists.
    if batch.get('simulated') is True:
        return {'stock_admitted':False,'reason':'LAB_FIXTURE_IS_NOT_MATERIAL_LOT',
                'quantity_consumed':0}
    essential=('lot_id','product_page','origin','quantity','custody','quality','use_authorized')
    if any(batch.get(k) in (None,'') for k in essential):
        return {'stock_admitted':False,'reason':'CUSTODY_OR_QUALITY_MISSING','quantity_consumed':0}
    # No source-verification mechanism is present in this offline code. Even if
    # well formed, independent Notion + laboratory readback must occur.
    return {'stock_admitted':False,'reason':'REQUIRES_INDEPENDENT_AUTHORITY_SOURCE_READBACK',
            'quantity_consumed':0}

def material_status(evidence):
    m=evidence['material']
    return {'source_roles':['FIBRA_STRUCTURE_PS','HERB_LIGHT_SOURCE','CRYSTAL_LIGHT_SOURCE',
                            'PERGAMINHO_P2_BENCH_ONLY','SLATE_CANDIDATE_PS'],
            'proposed_fiber_cm':m['fiber_length_proposed_cm'],
            'measured_fiber_cm':m['fiber_length_measured_cm'],
            'physical_acceptance':'HOLD_MEASUREMENTS_AND_SAMPLE',
            'geometry_constraints_generated':True,
            'new_bom_changes':0,'physical_units_built':0}

def read_only_baseline_status():
    p=ROOT/'baselines/CRAFT_H2P2_EVOLUCAO_TEST_20261020.zip'
    assert hashlib.sha256(p.read_bytes()).hexdigest()==BASE_SHA
    with zipfile.ZipFile(p) as z:assert z.testzip() is None
    return {'baseline_sha256':BASE_SHA,'baseline_bytes':p.stat().st_size,
            'historical_r48_seq':1,'historical_r48_order':'SBX-R48-ORDER-48322',
            'executed_r48_factory':False}

def compile_docket():
    e=read_evidence()
    return {'trace':'CRAFT-POSTH2P2-20261020-001','case':e['case'],
            'p2':h2_3_admission(e),'oil_stock_search':qualify_finished_oil(e),
            'inventory_database_rows_scanned':10,
            'inference_scope':'NO_QUALIFIED_OIL_LOT_FOUND_IN_QUERIED_SOURCES_NOT_GLOBAL_ABSENCE',
            'material':material_status(e),
            'operator':qualify_operator(e),
            'vector_route':'EXISTING_ESSENCE_EXTRACTION_AND_AURORA_ESSENCE_COMPARATORS_ONLY',
            'H2_4':'HOLD_P2_PLUS_ITEM_SPECIFIC_PATTERN',
            'H2_5':'HOLD_H2_4_AND_SOURCE_SEPARATION',
            'PA_H1':None,'PA_inquiry':'CRAFT-PA-QUERY-POS-E50-20261020-001',
            'baseline':read_only_baseline_status(),
            'magic_success_claimed':False,'party_or_primeiro_writes':0,
            'RC5':'HOLD','F5':'RED','C19_021':'UNKNOWN-EFFECT'}

if __name__=='__main__':
    data=compile_docket()
    (ROOT/'outputs'/'H2_3_ACTUAL_READONLY_PRECHECK.json').write_text(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('READONLY_ADMISSION',data['p2']['stage_A'],'BLOCKERS',data['p2']['blocker_count'],
          'OIL_USABLE_LOTS',data['oil_stock_search']['usable_lots'],
          'OPERATOR_ASSIGNED',data['operator']['assigned_authorized_operator'])
