"""CRAFT ENC 9/9 official corpus: BOM supplier fanout, static/read-only.

Manual trace of live Notion source pages 2026-10-21. NOT proof of world stock,
procedural equivalence, item production, magic, PA or user knowledge.
"""
from __future__ import annotations
from typing import Any
from collections import Counter

SOURCE_INDEX='https://app.notion.com/p/3edc2b324ede818284e2db7956a28291'
OIL_SOURCE='https://app.notion.com/p/3edc2b324ede81f1a88ec69980ab6cfd'
ENC_MODULE='https://app.notion.com/p/3f1c2b324ede818ab03bc749883906c6'

# Oil quantities and other materials transcribed literally from source recipes.
CATALOG={
 'VENTO_ARTICO_B':{'pattern':'3edc2b324ede814591bbe9b1a9eac5f0','recipe':'3edc2b324ede819e850de7e272c1032e','rank':'Bronze','knowledge':'SIM','surface':'ITEM_OU_ARMA','oil':1,'bom_n':4,'all_quantified':True,'gap':'Folhas do Sussurro Congelados (BOM) / Folhas de Mintaur (processo)'},
 'FLAMEJANTE_SAGRADO_B':{'pattern':'3edc2b324ede81fd8234c99548adf6de','recipe':'3edc2b324ede81b4b912f3f1a8adfd5a','rank':'Bronze','knowledge':'SIM','surface':'ITEM_OU_ARMA','oil':1,'bom_n':4,'all_quantified':True,'gap':'Cinzas Coração Flamejante (BOM) / Cinzas do Coração Flamejante (processo), alias não verificado'},
 'RAIO_POENTE_B':{'pattern':'3edc2b324ede81b590c1ee796ca9cfae','recipe':'3edc2b324ede8173a26cd7c4080b0f88','rank':'Bronze','knowledge':'NAO_INDICADO','surface':'ITEM_OU_ARMA','oil':1,'bom_n':4,'all_quantified':True,'gap':None},
 'CHAMA_RELAMPAGO_P':{'pattern':'3edc2b324ede816c98e1c541bd9011a8','recipe':'3edc2b324ede81cc8ba9f3f82a5cd1bf','rank':'Prata','knowledge':'NAO_INDICADO','surface':'ITEM_OU_ARMA','oil':1,'bom_n':5,'all_quantified':True,'gap':None},
 'TERRA_FERTIL_P':{'pattern':'3edc2b324ede81b9a769d4ede0c4605e','recipe':'3edc2b324ede81fc9893f26f86dabee9','rank':'Prata','knowledge':'NAO_INDICADO','surface':'SOLO','oil':1,'bom_n':5,'all_quantified':True,'gap':None},
 'SOMBRAS_ENGANOSAS_O':{'pattern':'3edc2b324ede81328244cb03c1baf85d','recipe':'3edc2b324ede813ca572c8b98443d53f','rank':'Ouro','knowledge':'SIM','surface':'ITEM','oil':1,'bom_n':6,'all_quantified':True,'gap':'Essência Sangue das Sombras (BOM) / Essência de Sombra (processo)'},
 'SELAMENTO_P':{'pattern':'3edc2b324ede81769f26d68a8a42aab6','recipe':'3edc2b324ede8167aa41f8d6a5aa9671','rank':'Prata','knowledge':'SIM','surface':'OBJETO','oil':1,'bom_n':4,'all_quantified':True,'gap':'Rituais apropriados descritos sem parâmetros de execução e adjudicação'},
 'VEDACAO_P2':{'pattern':'3edc2b324ede81adab3dd3a7f9fe921d','recipe':'3edc2b324ede811783dfce62058ca6b8','rank':'Prata','knowledge':'SIM','surface':'PERGAMINHO_OU_OBJETO','oil':1,'bom_n':7,'all_quantified':True,'gap':'Sal Santo/Encantado e energizador 2 Pedra Luz XOR 2 Pote sem etapa'},
 'REFLEXO_PROFUNDEZAS_P':{'pattern':'3edc2b324ede816bac13cb656a31677a','recipe':'3edc2b324ede816bac13cb656a31677a','rank':'Prata','knowledge':'NAO','surface':'PERGAMINHO_E_ITEM','oil':0,'bom_n':4,'all_quantified':False,'gap':'4/4 quantidades não documentadas, operador sem conhecimento comprovado'},
}


def corpus_report(cases:dict[str,int]|None=None)->dict[str,Any]:
    if cases is None:cases={k:1 for k in CATALOG}
    if not isinstance(cases,dict):raise ValueError('INVALID_CASES')
    if any(k not in CATALOG for k in cases):raise ValueError('UNKNOWN_INSCRIPTION')
    if any(type(v) is not int or v<=0 for v in cases.values()):raise ValueError('INVALID_QUANTITY')
    rank_counts=dict(Counter(x['rank'] for x in CATALOG.values()))
    knowledge_counts=dict(Counter(x['knowledge'] for x in CATALOG.values()))
    oil_dependent=[k for k,x in CATALOG.items() if x['oil']==1]
    oil_independent=[k for k,x in CATALOG.items() if x['oil']==0]
    portfolio_oil=sum(CATALOG[k]['oil']*v for k,v in cases.items())
    return {'source_index':SOURCE_INDEX,'official_enc_corpus_denominator':len(CATALOG),
        'inscription_source_pages':len({x['pattern'] for x in CATALOG.values()}),
        'recipe_source_pages':len({x['recipe'] for x in CATALOG.values()}),
        'oil_dependency_count':len(oil_dependent),
        'oil_dependency_names':oil_dependent,
        'oil_independent_count':len(oil_independent),
        'oil_independent_names':oil_independent,
        'oil_requirements_for_selected_cases':portfolio_oil,
        'rank_counts':rank_counts,'knowledge_counts':knowledge_counts,
        'source_knowledge_is_operator_competence':False,
        'uses_oil_not_equal_to_fabricated_oil':True,
        'oil_finished_lot_qualified_in_current_case':False,
        'oil_world_stock_conclusion':'UNKNOWN',
        'oil_recipe_current_iron_units':3,
        'oil_ingredient_process_conflicts':['OIL-DROPS-03','OIL-ESSENCE-04','OIL-IRON-05'],
        'cross_family_weapon_inscriptions':[k for k,x in CATALOG.items() if x['surface']=='ITEM_OU_ARMA'],
        'soil_is_accessory':False,
        'source_evidence':{k:{'pattern_url':'https://app.notion.com/p/'+x['pattern'],
                              'recipe_url':'https://app.notion.com/p/'+x['recipe'],
                              'rank':x['rank'],'knowledge':x['knowledge'],
                              'oil_units_by_bom':x['oil'],
                              'materials_quantified':x['all_quantified'],
                              'ingredient_line_count':x['bom_n'],
                              'surface':x['surface'],'gap':x['gap'],
                              'magic_ever_observed_by_this_audit':False}
                           for k,x in CATALOG.items()},
        'operation':'OP-ARQ-RIN-REC-01','workstream':'CM-000002-WS0001',
        'production':'HOLD','f5':'RED','c19':'UNKNOWN-EFFECT',
        'p2_recipe_edited':False,'r48_orders_created':0,
        'pa_debits':0,'real_magic_acts':0,'party_writes':0,'o_primeiro_writes':0}


def route_decision(requested:list[str]):
    """Prioritizes research paths without authorizing actual application."""
    if not isinstance(requested,list) or not requested:raise ValueError('EMPTY_ROUTE')
    if len(set(requested))!=len(requested):raise ValueError('DUPLICATE_CANDIDATE')
    data=corpus_report({k:1 for k in requested})
    oil_users=[k for k in requested if CATALOG[k]['oil']]
    no_oil=[k for k in requested if not CATALOG[k]['oil']]
    return {'shared_oil_users':oil_users,
       'oil_units_minimum_for_one_of_each':len(oil_users),
       'independent_research_paths':[{
           'inscription':k,'known_general':CATALOG[k]['knowledge'],
           'fully_quantified':CATALOG[k]['all_quantified'],
           'unblocked_for_real_application':False,
           'reason':'NON_OIL_RECIPE_STILL_LACKS_REQUIRED_QUANTITIES_KNOWLEDGE_LOTS_OPERATOR'
       } for k in no_oil],
       'ability_to_apply_now':False,
       'has_any_authorized_recipe_at_application_gate':False,
       'value':'BOM_DEPENDENCY_MAP_ONLY'}


def stress(n=12):
    total=0
    for i in range(1,n+1):
     for j in range(1,n+1):
      for k in range(1,n+1):
       a=corpus_report({'VEDACAO_P2':i,'VENTO_ARTICO_B':j,'TERRA_FERTIL_P':k})
       assert a['oil_requirements_for_selected_cases']==i+j+k
       assert a['production']=='HOLD' and a['r48_orders_created']==0
       total+=1
    return {'synthetic_test_vectors':total,'material_receipts':0,'result':'PASS'}

if __name__=='__main__':
 import json
 print(json.dumps(corpus_report(),indent=2,ensure_ascii=False))
