"""Calls the original R48/R44/R46/R47 code in an authenticated *patched copy*.
Synthetic only; simulated R47 root keys are public and NOT real attestation.
"""
from __future__ import annotations
import copy,json,sys,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE/'native_lab/R48_TEST_EXTENDED'
sys.path.insert(0,str(ROOT))
from r48_factory import IntegratedFactory,FactoryError,HISTORICAL_RECIPES,ALLOWED_RECIPES,digest
from r48_fixtures import lots,order,REVIEW
from r47_fixtures import recipes_and_sources,policy,make_pair,make_attestation
from r46_fixtures import artifact,make_report

KEY='SBX-VIGILIA-BOREAL-R48-TEST-v1'
CASE='LAB-CRAFT-VIGILIA-BOREAL-20261020-001'
LAB='3fbc2b324ede811db848d35d4739eb00'
URL='https://app.notion.com/p/'+LAB
PA_SHA='1d4e43e1f8b21106e0c8fee25bab53a81528e4a903f3184852b768dade48c4ea' # authenticated R39 envelope bytes; NO tariff math in CRAFT.
CRYSTAL='3edc2b324ede818b9d7ad75d42f2afa2'
HERB='3edc2b324ede81deb8cec70bf5ca7150'
FIBER='3f3c2b324ede815ab04ace5bd1074e79'
LOTS=('SBX-VIGILIA-CRISTAL-01','SBX-VIGILIA-ERVA-01','SBX-VIGILIA-FIBRA-01')

RECIPE={
 'namespace':'SBX-CRAFT-R44-I0016','key':KEY,'status':'EXPERIMENTAL_DESIGN_ONLY',
 'official_rec_id':None,'official_product_id':None,'mechanical_bonus':0,
 'source_page_id':LAB,'source_crn_id':CASE,'source_status':'LAB_E3_NOT_STOCK','source_url':URL,
 'prior_dossier_id':CASE,'design_id':'SBX-VIGILIA-BOREAL-STRUCTURAL',
 'name':'Pingente da Vigília Boreal — montagem estrutural TEST',
 'family':'Acessório — montagem estrutural, SEM eficácia mágica',
 'inputs':[{'source_page_id':CRYSTAL,'unit':'un','quantity':1},
           {'source_page_id':HERB,'unit':'un','quantity':1},
           {'source_page_id':FIBER,'unit':'cm','quantity':45}],
 'auxiliary_materials':'Nenhum insumo adicional admitido sem fonte; ferramental hipotético só fixture.',
 'tools':['SBX-FERRAMENTA-TRANCAR-HIPOTETICA','SBX-GABARITO-QA-HIPOTETICO'],
 'skills':['SBX-HABILIDADE-MONTAGEM-HIPOTETICA','SBX-OPERADOR-QA-TEST'],
 'steps':[
  {'seq':1,'name':'preparar_fibra_simulado','minutes_proposed':15},
  {'seq':2,'name':'preparar_erva_simulado','minutes_proposed':10},
  {'seq':3,'name':'acoplar_cristal_simulado','minutes_proposed':15},
  {'seq':4,'name':'revisar_montagem_sem_magia_simulado','minutes_proposed':15}],
 'proposed_active_minutes':55,'setup_wait_transport_rework_minutes':'PENDENTE_NAO_MEDIDO',
 'design_assumption_R44':'45 cm e 55 min são dimensionamento TEST, não fato do mundo.',
 'output':{'name':'Amostra estrutural sintética sem efeito mágico (NÃO PINGENTE FUNCIONAL)',
           'unit':'amostra_sintetica','quantity':1,'function':'QA geométrico em fixture; eficácia mágica NÃO demonstrada'},
 'qa_rules':[{'field':'piece_count','kind':'range','min':1,'max':1},
             {'field':'fiber_length_mm','kind':'range','min':440,'max':460},
             {'field':'crystal_mounted','kind':'bool_eq','value':True},
             {'field':'herb_mounted','kind':'bool_eq','value':True},
             {'field':'cord_intact','kind':'bool_eq','value':True},
             {'field':'magic_transfer_proven','kind':'bool_eq','value':False}],
 'comparators':['materiais_soltos','suporte_sem_cristal','suporte_sem_erva'],
 'differentiation_proof':'NENHUMA_TRANSFERENCIA_MAGICA_OBSERVADA',
 'risks':['liberacao_de_componente','deterioracao_de_erva','perda_de_luz','transferencia_magic_nao_comprovada'],
 'cost_expression':'UTE_CTE_MED_DESCONHECIDO; NAO_ESTIMAR_PRECO',
 'cost_med_status':'PENDENTE_UTE_CTE',
 'uncertainties':['fibra PS sem rendimento','ferramental e especialista não observados',
                  'QA só sintético','magia e retenção não demonstradas','nenhuma amostra física'],
 'testable_only_in_sandbox':True
}
MEASUREMENTS={'piece_count':1,'fiber_length_mm':450,'crystal_mounted':True,
              'herb_mounted':True,'cord_intact':True,'magic_transfer_proven':False}

def simulated_lot(name,source,unit,amount):
 return {'lot_id':name,'source_page_id':source,'unit':unit,'quantity':amount,
         'fixture_kind':'SYNTHETIC','cracked':False,'delaminated':False,'contaminated':False,
         'scope':'SYNTHETIC_STOCK_NOT_COLLECTED','dimensions_mm':{}}

def build_factory():
 recs,sources=recipes_and_sources()
 assert set(recs)==set(HISTORICAL_RECIPES)
 recs[KEY]=copy.deepcopy(RECIPE)
 sources[LAB]={'title':'LAB CRAFT — caso Pingente Vigília Boreal TEST','source_status':'LAB_E3_PROPOSAL',
  'last_edited_at':'2026-10-20T14:45:34.463Z','url':URL,'inventory':'NO_CANONICAL_STOCK_CLAIM'}
 synthetic=lots()+[simulated_lot(LOTS[0],CRYSTAL,'un',1),simulated_lot(LOTS[1],HERB,'un',1),simulated_lot(LOTS[2],FIBER,'cm',45)]
 return IntegratedFactory(recs,synthetic,sources,policy())

def make_report_for_third(index=48301):
 # Call original R46 fixture creator for the wholly fictional instrument, operator,
 # artifacts and custody, then rebind to the THIRD registry and recompute artifacts.
 report=make_report('SBX-TLI-R44-v1',id=f'SBX-R46-LAUDO-{index:05d}',kind='SYNTHETIC')
 report['recipe_key']=KEY;report['source_page_id']=LAB;report['source_crn_id']=CASE
 report['lot_ids']=list(LOTS)
 report['conditions']['method_id']='SBX-VIGILIA-STRUCTURAL-ONLY'
 old=report['observations']
 obs={}
 for rule in RECIPE['qa_rules']:
  name=rule['field'];value=MEASUREMENTS[name]
  obs[name]={'reading_id':'SBX-R46-OBS-'+str(index)+'-'+name,
         'value':value,'unit':'bool' if rule['kind']=='bool_eq' else 'count' if name.endswith('_count') else 'mm',
         'uncertainty_abs':0 if rule['kind']=='bool_eq' or name.endswith('_count') else 0.05,
         'instrument_id':report['instrument']['instrument_id'],
         'sample_id':report['sample_id'],'observed_at':report['observed_at']}
 report['observations']=obs
 # regenerate all payload bindings per original schema
 inst=report['instrument'];cert={k:v for k,v in inst.items() if k!='certificate_sha256'}
 report['artifacts']['calibration']=artifact(json.dumps(cert,ensure_ascii=False,sort_keys=True))
 inst['certificate_sha256']=report['artifacts']['calibration']['claimed_sha256']
 custody={'sample_id':report['sample_id'],'events':[{k:v for k,v in e.items() if k!='support_sha256'} for e in report['custody']]}
 report['artifacts']['custody']=artifact(json.dumps(custody,ensure_ascii=False,sort_keys=True))
 for e in report['custody']:e['support_sha256']=report['artifacts']['custody']['claimed_sha256']
 op={'sample_id':report['sample_id'],'operator':{k:v for k,v in report['operator'].items() if k!='attestation_ref'}}
 report['artifacts']['operator']=artifact(json.dumps(op,ensure_ascii=False,sort_keys=True))
 report['operator']['attestation_ref']=report['artifacts']['operator']['claimed_sha256']
 doc={'sample_id':report['sample_id'],'source_page_id':LAB,'instrument_id':inst['instrument_id'],
   'observed_at':report['observed_at'],'observations':report['observations']}
 report['artifacts']['measurement']=artifact(json.dumps(doc,ensure_ascii=False,sort_keys=True))
 return report

def make_order(index=48301,phase='STRUCTURAL_TEST',pa_sha=PA_SHA):
 report=make_report_for_third(index)
 return {'order_id':f'SBX-R48-ORDER-{index:05d}','recipe_key':KEY,
   'lot_ids':list(LOTS),'measurements':copy.deepcopy(MEASUREMENTS),
   'tools':copy.deepcopy(RECIPE['tools']),'skills':copy.deepcopy(RECIPE['skills']),
   'report':report,'attestation':make_attestation(report),
   'experimental_phase':phase,'case_id':CASE,'pa_envelope_sha256':pa_sha,'pa_livre_fixture':20}

def demo(outdir=HERE/'results'):
 outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
 factory=build_factory();before=factory.snapshot();old_head=factory.head
 bad=make_order(48301,phase='MAGIC_TEST')
 error=None
 try:factory.process_batch('SBX-R48-BATCH-VIGILIA-MAGIC-NEG',[bad],REVIEW)
 except FactoryError as e:error=str(e)
 assert error=='MAGIC_TRANSFER_NOT_DEMONSTRATED',error
 assert factory.snapshot()==before and factory.head==old_head
 fake_recipe=order('tli',48302)
 fake_recipe['recipe_key']='SBX-UNKNOWN-EXPERIMENT'
 try:factory.process_batch('SBX-R48-BATCH-FAKE-RECIPE',[fake_recipe],REVIEW)
 except FactoryError as e:unknown=str(e)
 else:raise AssertionError('UNKNOWN_RECIPE_WAS_ACCEPTED')
 assert unknown=='ONLY_TWO_EXISTING_RECIPES',unknown
 valid=make_order(48303)
 receipt=factory.process_batch('SBX-R48-BATCH-VIGILIA-STRUCTURAL',[valid],REVIEW)
 after=factory.snapshot()
 replay=factory.process_batch('SBX-R48-BATCH-VIGILIA-STRUCTURAL',[valid],REVIEW)
 assert replay['idempotent_replay'] is True and factory.snapshot()==after
 assert factory.audit()['ok']
 report={'negative_magic':error,'unknown_recipe':unknown,
     'receipt':receipt,'replay':{'idempotent_replay':replay['idempotent_replay'],'unchanged_after_replay':factory.snapshot()==after},
     'before':before,'after':after,'audit':factory.audit(),
     'r48_original_dispatch':'IntegratedFactory.process_batch','r44_engine_used':True,
     'r46_r47_original_dispatch':True,'quality_fixture_only':True,
     'physically_made':False,'magic_observed':False,'official_production':False}
 (outdir/'native_pingente_result.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf8')
 print(json.dumps({'magic':error,'unknown':unknown,'order_status':receipt['orders'][0]['status'],
                   'receipt':receipt['batch_id'],'journal_events':len(factory.journal),'r44_events':len(factory.core.state['events']),
                   'r47_events':len(factory.vault.events),'product_count_synthetic':receipt['experimental_product_count'],
                   'physical_products':receipt['physical_products'],'status':receipt['status'],
                   'audit':factory.audit()['ok'],'idempotent':replay['idempotent_replay']},indent=2))
 return report
if __name__=='__main__':demo()
