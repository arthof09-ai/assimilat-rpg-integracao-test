from pathlib import Path
import json,statistics
import pa_r04 as pa
P=Path(__file__).resolve().parent
r03=json.loads((P/'BASELINE_PA_R03/corpus_pa_v3.json').read_text('utf8'))['items']
p=json.loads((P/'CORPUS_ORIGEM_AUDITADA_R04.json').read_text('utf8'))
master=[x for x in p['rows'] if x['surface']=='CATALOGO_MESTRE_INDEXADO' and x['pa_daily'] is not None]
strict=[x for x in master if x['classification']=='EXPLICITA']
coeff=pa.coefficients();bounds=pa.identified_bounds()
(P/'COEFICIENTES_R04_PROVENIENCIA.json').write_text(json.dumps({'coefficients':coeff,'conditional_partial_bounds':bounds,'status':'TEST_CIENTIFICO_NAO_HOMOLOGADO','source_contrast':'2 APRIMORAMENTOS da Party-Espelho não devem compor dataset Mestre','canonical_coefficients_demonstrated':0},ensure_ascii=False,indent=2)+'\n','utf8')
model={'data_assessment':{'R03_total_daily_n':30,'R03_total_pages_n':108,'MASTER_items_and_patterns_n':88,'MASTER_daily_numeric_including_R_PA_DIA':len(master),'MASTER_daily_explicit':len(strict),
'MASTER_daily_inferred_R_PA_DIA':len(master)-len(strict),'MASTER_independent_lineages_max_provisional':87,
'MASTER_median_daily_with_RPA':statistics.median(x['pa_daily'] for x in master),'MASTER_median_daily_explicit_only':statistics.median(x['pa_daily'] for x in strict),
'global_population_unknown':True},
 'model_comparison':[
  {'model':'A0_CONSTANTE_R03_MEDIANA','training_n':30,'input':'all R03 daily numeric regardless of source','forecast_constant':statistics.median(x['pa_daily']['value'] for x in r03 if x['pa_daily']['value'] is not None),'scientific_status':'VIES_FONTE_PARTY; NÃO USAR CANONIZACAO'},
  {'model':'A1_CONSTANTE_APENAS_MESTRE','training_n':len(master),'predicted_opaque_pa_day':statistics.median(x['pa_daily'] for x in master),'scientific_status':'BASELINE_DESCRITIVO_SEM_PODER_DE_RESOLVER_EFEITOS; NAO_ESTIMADOR_APROVADO'},
  {'model':'B_GLOBAL_LIN_ATTR_5','training_n_pure_independent':1,'applicability':'Somente fonte em Party Espelho','scientific_status':'CONTRADICAO_CONDICIONAL_COM_MISTOS; NAO_IDENTIFICAVEL'},
  {'model':'C_SOMA_NAO_NEGATIVA_COMPONENTES','potential_parameters_min':17,'master_cost_observations_max':len(master),'linear_rank_upper_bound':len(master),'nullspace_dimension_lower_bound':3,'scientific_status':'SUBDETERMINADO MESMO SE X FOSSE COMPLETA; SERIA MENOR COM LINHAGENS RELACIONADAS'},
  {'model':'D_IDENTIFICACAO_PARCIAL_ESTERIL','training_n':len(master),'cost_new_item':None,'scientific_status':'SEGURANCA EPISTEMICA: CUSTO DESCONHECIDO FORA DE EFEITOS ISOLADOS; MODELO MAIS SIMPLES ACEITO PARA R04'}],
 'holdout':{'in_domain_eligible_new_validation_count':0,'out_of_domain_new_test_count':6,'out_of_domain_lineage_groups':4,'outcome':'NÃO HÁ DESEMPENHO PREDITIVO UNIVERSAL COMPROVADO'},
 'conclusions':['Estes coeficientes não podem ser ajustados com identificação causal por patamar, rank, MED ou FIP genérica.',
 'A adaga 35 de PA tem leitura divergente entre R03 e QMC02; sensibilidade n=12 explícitos vs 14 incluindo R-PA-DIA.',
 'Desempenho no espelho Party não é holdout Mestre.',
 'Uma solução científica completa exige novos itens de fonte Mestre com efeito isolado e preço declarado, preferencialmente pares por versão.']}
(P/'COMPARATIVO_MODELOS_R04.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n','utf8')
scenarios={'technical_examples_only':True,'not_pa_tariff':True,
 'bonus_grid':[pa.damage_increment(15,n,25,attempts=k,p_hit=.6,eligible=1,targets=1) for n in [5,10,20] for k in [1,2,3]],
 'bonus_20_condition_half_eligible':pa.damage_increment(15,20,25,attempts=3,p_hit=.6,eligible=.5),
 'bonus_20_two_targets':pa.damage_increment(15,20,25,attempts=3,p_hit=.6,targets=2),
 'daily_budget_examples':{'unknown':pa.budget(100,20,18,5,daily_semantics='UNKNOWN'),'commit_hypothetical':pa.budget(100,20,18,5,daily_semantics='COMMIT'),'debit_hypothetical':pa.budget(100,20,18,5,daily_semantics='DEBIT'),'insufficient_hypothetical':pa.budget(40,20,18,5,daily_semantics='COMMIT')},
 'candidate_reference':'CANDIDATO_EXPERIMENTAL_ESPADA.json','candidate_result':pa.proposal(json.loads((P/'CANDIDATO_EXPERIMENTAL_ESPADA.json').read_text('utf8')))}
(P/'CENARIOS_ENERGETICOS_R04.json').write_text(json.dumps(scenarios,ensure_ascii=False,indent=2)+'\n','utf8')
print('model written',len(master),len(strict),model['data_assessment']['MASTER_median_daily_with_RPA'])
