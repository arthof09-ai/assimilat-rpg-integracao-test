"""Read-only multi-recipe evidence crosswalk; adapter to existing CRAFT H2 QA.

Sources: verified Notion Mestre P2/Selamento/Sombras/Oleo recipes (2026-10-21).
Does not edit recipes, reserve lots, invoke R48, supply magic or set PA.
Recipe entries are faithful quotations of ingredient names and quantities, not
an assertion of material stock or ingredient equivalence.
"""
from __future__ import annotations
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
P2_URL='https://app.notion.com/p/3edc2b324ede811783dfce62058ca6b8'
OIL_URL='https://app.notion.com/p/3edc2b324ede81f1a88ec69980ab6cfd'
SEL_URL='https://app.notion.com/p/3edc2b324ede8167aa41f8d6a5aa9671'
SHADOW_URL='https://app.notion.com/p/3edc2b324ede813ca572c8b98443d53f'
ARCTIC_URL='https://app.notion.com/p/3edc2b324ede819e850de7e272c1032e'
REFLEXO_URL='https://app.notion.com/p/3edc2b324ede816bac13cb656a31677a'
CANONICAL_LOT_EVIDENCE_AVAILABLE=False


def _old(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'baseline'/f'{name}.py')
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_SOURCE_GUARD=_old('craft_p2_source_guard')
# Stable human-visible label and BOM; the amounts are directly specified by recipes.
RECIPES={
 'P2':{
  'recipe_url':P2_URL,'pattern':'Inscrição de Vedação (P)','rank':'Prata',
  'bom':{'Argila de Elemental da Terra':3,'Água Benta de Santuário':1,
         'Sal de Geodo Santo':2,'Pó de Ferro de Meteoro':3,
         'Essência de Barreira Mística':1,'Óleo de Vedação':1},
  'energy_options':{'Pedra da Luz':2,'Pote de Essência Mágica':2},
  'specific_identity_conflict':'Passo 3 Sal de Geodo Encantado vs BOM Santo',
  'specific_process_gap':'Nenhum passo contém Pedra da Luz/Pote de Essência Mágica',
  'source_energization_step':'NONE_DOCUMENTED',
  'source_application':'Passo 6 pergaminho OU objeto',
  'source_effect':'Vedar e estabilizar elemento mágico/entidade por um período',
 },
 'SELAMENTO_P':{
  'recipe_url':SEL_URL,'pattern':'Inscrição de Selamento (P) (CG)','rank':'Prata',
  'bom':{'Argila de Barreira':2,'Sal dos Espíritos':3,'Óleo de Vedação':1,
         'Pó de Quartzo de Guardião':2},
  'energy_options':{},
  'specific_identity_conflict':None,
  'specific_process_gap':'Passo 5 exige rituais apropriados sem especificar parâmetros; não confundir com fórmula P2',
  'source_energization_step':'Passo 4 entoação durante aplicação de pó; passo 5 rituais apropriados',
  'source_application':'Passo 5 aplicar pasta no objeto receptor do selo',
  'source_effect':'Receptáculo para espíritos/energias, com resistência a desencantamento',
 },
 'SOMBRAS_O3':{
  'recipe_url':SHADOW_URL,'pattern':'Inscrição Sombras Enganosas (O) (CG)','rank':'Ouro',
  'bom':{'Essência Sangue das Sombras':3,'Pó de Diamante Noturno':3,
         'Tinta de Lula Abissal':2,'Folhas de Camuflagem':5,
         'Orvalho de Lua Nova':5,'Óleo de Vedação':1},
  'energy_options':{},
  'specific_identity_conflict':'Passo 1 Essência de Sombra vs BOM Essência Sangue das Sombras: POSSÍVEL ALIAS NÃO ATESTADO',
  'specific_process_gap':'Passo 6 menciona encantamento de ocultação, sem fornecer parâmetros reproduzíveis',
  'source_energization_step':'Passo 6 entoação durante aplicação no item',
  'source_application':'Passo 6 aplicar pasta no item',
  'source_effect':'Item quase invisível e portador menos detectável',
 },
 'VENTO_ARTICO_B1':{
  'recipe_url':ARCTIC_URL,'pattern':'Inscrição Vento Ártico (B) (CG)','rank':'Bronze',
  'bom':{'Cristais de Gelo Eterno':2,'Essência de Vento Sussurrante':2,
         'Óleo de Vedação':1,'Folhas do Sussurro Congelados':4},
  'energy_options':{},
  'specific_identity_conflict':'Passo 3 Folhas de Mintaur versus Folhas do Sussurro Congelados na BOM; equivalência NÃO documentada',
  'specific_process_gap':'Passo 5 encantamento suave não define teste de eficácia/duração; objeto e arma permitidos na fonte',
  'source_energization_step':'Passo 5 entoação ao aplicar no objeto ou arma',
  'source_application':'Item ou arma desejada, passo 5',
  'source_effect':'Propriedades de gelo, resistência ao frio, agilidade, aura de lentidão; sem bônus numéricos',
 },
}


class AuditInputError(ValueError):pass


def plan_shared_supplier(demand:dict[str,int], synthetic_finished_oil_qty:int|None=None)->dict[str,Any]:
    """Static BOM demand + bottleneck, not stock or R48 planning authority."""
    if not isinstance(demand,dict) or not demand:
        raise AuditInputError('BATCH_DEMAND_EMPTY')
    for key,count in demand.items():
        if key not in RECIPES:raise AuditInputError('UNKNOWN_RECIPE:'+str(key))
        if type(count) is not int or count<=0:raise AuditInputError('INVALID_POSITIVE_INTEGER_QUANTITY:'+str(key))
    if synthetic_finished_oil_qty is not None and (type(synthetic_finished_oil_qty) is not int or synthetic_finished_oil_qty<0):
        raise AuditInputError('INVALID_SYNTHETIC_STOCK')
    supplier=Counter()
    for key,amount in demand.items():
        for item,q in RECIPES[key]['bom'].items(): supplier[item]+=q*amount
    required_oil=supplier['Óleo de Vedação']
    # A supplied synthetic quantity can show arithmetic insufficiency but never certify custody.
    synthetic_shortfall=None if synthetic_finished_oil_qty is None else max(0,required_oil-synthetic_finished_oil_qty)
    selected={key:{'count':amount,'recipe_url':RECIPES[key]['recipe_url'],
                   'unresolved_recipe_issues':_issues(key),
                   'operator_and_physical_lot_validated':False,
                   'auto_installed':False} for key,amount in demand.items()}
    return {
       'type':'READONLY_REC_EXEC_DEPENDENCY_ADAPTER',
       'case':'OP-ARQ-RIN-REC-01/CM-000002-WS0001',
       'selected':selected,
       'oil_dependency_recipe_count':sum('Óleo de Vedação' in RECIPES[x]['bom'] for x in demand),
       'oil_units_required':required_oil,
       'oil_official_recipe_url':OIL_URL,
       'oil_official_iron_units':3,
       'oil_historical_iron_units_comparison_only':2,
       'sum_bom_excluding_energy':dict(sorted(supplier.items())),
       'p2_energy_exclusive_branch_required':'P2' in demand,
       'p2_energy_branch_chosen':False,
       'synthetic_oil_quantity':synthetic_finished_oil_qty,
       'synthetic_shortfall_units':synthetic_shortfall,
       'qualified_finished_oil_available':'UNVERIFIED',
       'physical_stock_changed':False,
       'stock_reservations':0,'craft_r48_orders_created':0,
       'all_three_receipts_magic_observed':False,
       'next_gate':'LIVE_LOT_CUSTODY_QA_AND_P2_DECISIONS_AND_OPERATOR',
       'material_and_magic_execution':'HOLD',
       'party_or_prime_writes':0,
    }


def _issues(key):
    base=RECIPES[key]
    issues=[]
    if base['specific_identity_conflict']:issues.append('BOM_PROCESS_NAME_UNRECONCILED')
    if base['specific_process_gap']:issues.append('APPLICATION_PROCESS_NEEDS_COMPETENT_SPECIFICATION')
    if key=='P2':issues.append('P2_ENERGIZER_STAGING_UNDEFINED')
    issues.append('OLEO_FINISHED_LOT_OR_MANUFACTURE_NOT_PROVEN')
    issues.extend(['RAW_INPUT_LOTS_UNVERIFIED','OPERATOR_UNASSIGNED','MAGIC_WITNESS_ABSENT'])
    return issues


def oil_recipe_incoherence():
    return {
       'source':OIL_URL,
       'bom_current':dict(_SOURCE_GUARD.OIL_OFFICIAL_BOM),
       'mismatch_drops':{'bom':'Gota do Orvalho do Amanhecer','process':'Orvalho de Dragão'},
       'mismatch_essence':{'bom':'Essência de Lua Minguante','process':'Essência de Vórtice'},
       'iron_unplaced':{'bom_units':3,'historical_units':2,'explicit_process_incorporation':False},
       'truncated_step':2,
       'salt_resolution_from_older_variants':False,
       'processable':False,
       'official_recipe_modified':False,
    }


def concrete_source_comparison():
    return {
      'purpose':'Adjudication packet for energy-step authority; precedent not binding P2',
      'recipescanned':list(RECIPES),
      'P2_energy':'2 Pedra da Luz XOR 2 Pote de Essência Mágica explicitly in BOM; no insertion step',
      'SELAMENTO_P_activation':'Ritual de proteção no passo 4 e ritual apropriado no passo 5; lacks the P2 energizer',
      'SOMBRAS_O3_activation':'Entoação de ocultação during application no passo 6; no P2 energizer',
      'VENTO_ARTICO_B1_activation':'Passo 5 entoação durante aplicação em item ou arma, sem autorizar P2',
      'not_sufficient_to_infer_P2_step':True,
      'minimal_authority_decision':{
        'salt_choice':'SANTO_or_ENCANTADO explicitly adjudicated',
        'energy_branch':'PEDRA_LUZ_or_POTE_ESSENCIA or decide whether original branch needs normative correction',
        'insertion_stage':'By recipe authority, NOT inferred from comparators',
        'method':'Material handling and activation determined by authority',
        'expenditure':'Conservation/consumption determined by authority',
        'duration':'Effect timeline or limit determined by authority',
        'observation':'Effect validation criterion and independent witness',
        'operator':'Competency and procedure authorization',
      },
      'source_recipe_modified':False,
      'pattern_created':False,
    }



# Literal process mention inventory from four Mestre-side pages. Deliberately no
# fuzzy matching or implied aliases; this is a traceable manual crosswalk, not
# a claim of natural language completeness.
PROCESS_LITERAL_MENTIONS={
 'P2':('Argila de Elemental da Terra','Água Benta de Santuário',
       'Sal de Geodo Encantado','Pó de Ferro de Meteoro',
       'Óleo de Vedação','Essência de Barreira Mística'),
 'SELAMENTO_P':('Argila de Barreira','Sal dos Espíritos','Óleo de Vedação',
                'Pó de Quartzo de Guardião'),
 'SOMBRAS_O3':('Essência de Sombra','Pó de Diamante Noturno',
               'Tinta de Lula Abissal','Folhas de Camuflagem',
               'Óleo de Vedação','Orvalho de Lua Nova'),
 'VENTO_ARTICO_B1':('Cristais de Gelo Eterno','Essência de Vento Sussurrante',
                   'Folhas de Mintaur','Óleo de Vedação'),
 'OLEO':('Raiz de Mandrágora','Orvalho de Dragão','Essência de Vórtice'),
}

def literal_process_coverage():
    sets={x:dict(RECIPES[x]['bom']) for x in RECIPES}
    sets['OLEO']=dict(_SOURCE_GUARD.OIL_OFFICIAL_BOM)
    details={}
    total_bom=matched=0
    for key,bom in sets.items():
        mentions=set(PROCESS_LITERAL_MENTIONS[key])
        matched_names=sorted(k for k in bom if k in mentions)
        missing=sorted(k for k in bom if k not in mentions)
        unmatched_process=sorted(k for k in mentions if k not in bom)
        details[key]={'source':OIL_URL if key=='OLEO' else RECIPES[key]['recipe_url'],
                      'bom_entries':len(bom),'exactly_mentioned':len(matched_names),
                      'names_exact':matched_names,
                      'not_exact_in_process':missing,
                      'process_mentions_without_literal_bom_match':unmatched_process,
                      'energy_staging_missing':'P2'==key,
                      'method':'MANUAL_LITERAL_NAME_MATCH_ONLY',
                      'equivalence_granted':False}
        total_bom+=len(bom)
        matched+=len(matched_names)
    return {'corpus_scope':list(sets),'scoped_recipe_count':len(sets),
            'aggregate_exact_matches':matched,
            'aggregate_bom_items':total_bom,
            'not_exactly_covered':total_bom-matched,
            'p2_energy_extra_branch_not_in_base_denominator':2,
            'details':details,
            'silent_reconciliation':False,
            'authoritative_recipe_modified':False,
            'readback_live_stock_verified':False}


def test_linear_demand_properties(max_quantity:int=15):
    """Pure arithmetic adversarial vectors on synthetic order counts only."""
    checked=0
    for a in range(1,max_quantity+1):
        for b in range(1,max_quantity+1):
            for c in range(1,max_quantity+1):
                inputs={'P2':a,'SELAMENTO_P':b,'SOMBRAS_O3':c}
                state=plan_shared_supplier(inputs,a+b+c-1)
                assert state['oil_units_required']==a+b+c
                assert state['synthetic_shortfall_units']==1
                assert state['material_and_magic_execution']=='HOLD'
                assert state['qualified_finished_oil_available']=='UNVERIFIED'
                assert state['stock_reservations']==0
                checked+=1
    return {'synthetic_vectors':checked,'range_per_family':max_quantity,
            'ledger_changed':False,'live_lots_examined':0,'result':'PASS'}

def reflexo_independent_route():
    """Specific NON-oil inscription route; no fictional ingredient amounts."""
    return {
      'source':REFLEXO_URL,
      'pattern':'Reflexo das Profundezas','rank':'Prata',
      'knowledge_general':'NAO',
      'oil_listed_in_ingredients':False,
      'ingredients_in_source':['Núcleo de vida de um Kraken Ancião',
                              'Sangue de Sereia Abissal','Pó de Coral Negro',
                              'Essência de Alga da Noite Eterna'],
      'quantities_documented_for_these_ingredients':0,
      'quantity_required_to_make_executable':'COMPETENT_RECIPE_AUTHORITY',
      'operator_license_and_known_pattern':'PENDENTE',
      'actual_material_lots_verified':0,
      'procedure':'Moa núcleo → combine sangue/pó → aqueça essência → trace símbolo e entoe',
      'substrate_note':'Desenho em pergaminho na fonte; aplicação em item referenciada',
      'independent_of_oil_in_current_text':True,
      'authorization_to_apply':False,
      'effect_observed':False,
      'magic_powers_copied_to_new_item':False,
      'next_stage':'RECONCILE_QUANTITIES_AND_KNOWLEDGE_BEFORE_LOT_REVIEW',
    }


def full_report():
    return {'source_comparison':concrete_source_comparison(),
            'oil_incoherence':oil_recipe_incoherence(),
            'literal_qa':literal_process_coverage(),
            'reflexo_without_oil':reflexo_independent_route(),
            'portfolio_four_oil_uses':plan_shared_supplier({k:1 for k in RECIPES}),
            'portfolio':plan_shared_supplier({'P2':1,'SELAMENTO_P':1,'SOMBRAS_O3':1}),
            'synthetic_1_unit':plan_shared_supplier({'P2':1,'SELAMENTO_P':1,'SOMBRAS_O3':1},1),
            'synthetic_3_units':plan_shared_supplier({'P2':1,'SELAMENTO_P':1,'SOMBRAS_O3':1},3),
            'p2_guard':_SOURCE_GUARD.evaluate({}),
            'r48_new_actions':0,'notion_writes':0,'production':'HOLD'}

if __name__=='__main__':print(json.dumps(full_report(),ensure_ascii=False,indent=2))
