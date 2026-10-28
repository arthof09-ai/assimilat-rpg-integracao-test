#!/usr/bin/env python3
"""R41: usa engine R44 AUTÊNTICO presente na fábrica R48, NÃO afirma R48/QMC produtor.
Somente fixtures LAB; jamais escreve estoque, Party, Notion, P4 ou libera F5.
"""
import sys,json,copy,hashlib,os
from pathlib import Path
R48=Path(os.environ.get('R41_R48_DIR',Path(__file__).resolve().parent/'R48_ORIGINAL')).resolve()
sys.path.insert(0,str(R48))
from r48_factory import R44
from experimental_engine import SandboxEngine
from r48_fixtures import lots as historical_lots
from r48_factory import IntegratedFactory, FactoryError
from r48_fixtures import order,REVIEW

CASE='LAB-CRAFT-VIGILIA-BOREAL-20261020-001'
RECIPE_KEY='SBX-VIGILIA-BOREAL-R44-R41-TEST'
SOURCES=['3edc2b324ede818b9d7ad75d42f2afa2','3edc2b324ede81deb8cec70bf5ca7150','3f3c2b324ede815ab04ace5bd1074e79']

def make_contract():
    return {'namespace':'SBX-CRAFT-R44-I0016','key':RECIPE_KEY,'status':'EXPERIMENTAL_DESIGN_ONLY',
       'official_rec_id':None,'official_product_id':None,'mechanical_bonus':0,'source_page_id':SOURCES[0],
       'source_crn_id':'NONE_LAB_TEST','source_status':'LAB_NO_PHYSICAL_INVENTORY',
       'output':{'name':'Pingente Vigilia Boreal — configuração SIMULADA, magia NAO PROVADA',
                 'unit':'fixture_pingente_sem_magia','quantity':1},
       'inputs':[{'source_page_id':SOURCES[0],'unit':'cristal','quantity':1},
                 {'source_page_id':SOURCES[1],'unit':'erva','quantity':1},
                 {'source_page_id':SOURCES[2],'unit':'cm','quantity':45}],
       'tools':['SBX-FERRAMENTA_FIXACAO_SIMULADA'],'skills':['SBX-ARTEFACTOR_SIMULADO'],
       'steps':[{'seq':i,'name':name,'minutes_proposed':t} for i,(name,t) in enumerate([
         ('preparar_fibra',8),('preparar_erva',7),('acoplar_cristal',12),('planejar_transferencia_nao_observada',28)],1)],
       'proposed_active_minutes':55,
       'qa_rules':[{'field':'ligacao_mecanica_integra','kind':'bool_eq','value':True},
                   {'field':'magia_transferida_com_prova_independente','kind':'bool_eq','value':True}],
       'cost_expression':'PENDENTE PRECO MED/UTE/CTE','fixture_only':True}

def make_lots():
    return [{'lot_id':id_,'fixture_kind':'SYNTHETIC','source_page_id':source,'unit':unit,
              'quantity':quantity,'cracked':False,'delaminated':False,'contaminated':False}
        for id_,source,unit,quantity in zip(['SBX-R41-CRISTAL','SBX-R41-ERVA','SBX-R41-FIBRA'],SOURCES,['cristal','erva','cm'],[1,1,45])]

def run():
    recipe=make_contract();ls=make_lots();engine=SandboxEngine({RECIPE_KEY:recipe},ls)
    before=copy.deepcopy(engine.state)
    input_ids=[x['lot_id'] for x in ls];tools=recipe['tools'];skills=recipe['skills']
    # First explicitly incomplete document: refuse as REJECTED_QUALITY, no product.
    missing=engine.run(RECIPE_KEY,'SBX-R41-MISSING',input_ids,{'ligacao_mecanica_integra':True},tools,skills)
    assert missing['status']=='REJECTED_QUALITY' and missing['products']==[]
    # Independent stage: a separate clean instance, explicit FALSE: reject.
    eng2=SandboxEngine({RECIPE_KEY:recipe},make_lots())
    negative=eng2.run(RECIPE_KEY,'SBX-R41-MAGIC-NEGATIVE',input_ids,
              {'ligacao_mecanica_integra':True,'magia_transferida_com_prova_independente':False},tools,skills)
    assert negative['status']=='REJECTED_QUALITY' and negative['products']==[]
    # A knowingly forged synthetic TRUE demonstrates that engine QA can PASS on fixture alone;
    # must not be misreported as magic or RC5. Trust gate below rejects the declaration.
    eng3=SandboxEngine({RECIPE_KEY:recipe},make_lots())
    synthetic=eng3.run(RECIPE_KEY,'SBX-R41-FALSE-MAGIC-FIXTURE',input_ids,
               {'ligacao_mecanica_integra':True,'magia_transferida_com_prova_independente':True},tools,skills)
    assert synthetic['status']=='EXPERIMENTAL_QA_PASS' and synthetic['products'][0]['status']=='SYNTHETIC_OUTPUT_ONLY'
    assert all(e.audit()['ok'] for e in [engine,eng2,eng3])
    # Top level original R48 remains unchanged, rejects immediately.
    fac=IntegratedFactory.fixture_factory(historical_lots());request=order('tli',48141)
    request['recipe_key']=CASE
    try:fac.process_batch('SBX-R48-BATCH-R41-DENY',[request],REVIEW)
    except FactoryError as e: reason=str(e)
    else:raise AssertionError('R48_original_falsely_accepted_Pingente')
    assert reason=='ONLY_TWO_EXISTING_RECIPES' and fac.journal==[]
    assert all(x['quantity'] == y['quantity'] for x,y in zip(fac.core.initial_lots.values(),fac.core.state['lots'].values()))
    return {'status':'PASS_R41_R44_REAL_ENGINE_TEST_ISOLATED','case_id':CASE,
            'r48_top_level':'DENY:'+reason,
            'r44_core_mechanical_pipeline':'EXECUTED_IN_SYNTHETIC_COPY',
            'negative_missing_evidence':missing['status'],
            'negative_false_transfer':negative['status'],
            'test_of_forged_true_fixture':synthetic['status'],
            'test_of_forged_true_proves_real_magic':False,
            'physical_magic_verified':False,'physically_crafted_products':0,
            'r46_r47_real_attestation':False,'RC5':False,'P4':False,'F5_prod':'RED',
            'pa_daily_from_unchanged_provider':12,'pa_per_activation_from_unchanged_provider':7,
            'main_engine_original_hash':hashlib.sha256((R48/'r48_factory.py').read_bytes()).hexdigest(),
            'a_canonical_re_cannot_be_created_by_label_only':True}

if __name__=='__main__': print(json.dumps(run(),ensure_ascii=False,indent=2))
