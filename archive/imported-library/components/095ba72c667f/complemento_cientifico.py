import csv,json,pathlib,collections,itertools,math,hashlib
r=pathlib.Path(__file__).parent
S={x['source_key']:x for x in csv.DictReader(open(r/'01_FONTES_FISICAS.csv',encoding='utf-8'))}
E={x['definition_id']:x for x in csv.DictReader(open(r/'02_DEFINICOES_EFEITOS.csv',encoding='utf-8'))}
def jwrite(name,x):(r/name).write_text(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
PREFLIGHT={
 'schema':'DMG-F0-F6-LOTE002-PREFLIGHT-B1-v1','operation':'OP-DMG-CORPUS-EMP-01','mode':'DOCUMENTARY_PROPOSAL_NO_DISPATCH',
 'target_consumer':'VLAB R23 BENCHMARK_AUTO; native adapter confirmation PENDING',
 'pilot_id':'DMG-GALIDEMUS-BRONZE1-001',
 'scene_id':None,'source_id':S['galidemus']['page_id'],'source_url':S['galidemus']['url'],
 'source_document_last_edited_at':S['galidemus']['notion_edited_at'],'source_digest':None,
 'source_excerpt_hash_only':S['galidemus']['excerpt_sha256'],'source_freeze_status':'SOURCE_EXCERPT_ONLY_NOT_NATIVE_SOURCE_DIGEST',
 'actor_id':'GaliDemus physical source; runtime actor UUID missing','form_id':'documentary-Bronze1-not-scene','actor_snapshot':None,
 'actor_rank':'Bronze 1','actor_type':'Besta Demoníaca','action_id':'GAL_PATADA','action_source_literal':'Patada: 1d4 + destreza cortante',
 'damage_components':[{'dice':'1d4','intrinsic_dme':2.5,'external_attribute':'DES','printed_value':13,'conditional_math_only_bruto_dme':15.5,'damage_tag':'cortante','mitigated':False}],
 'known_actor_fields':{'vida_display':32,'alma_display':32,'ca_display':21,'DES_display':13},
 'missing':['scene_epoch_actor_instance','current_equipment_status','action_economy_specific','cost_or_authoritative_omission_rule','range_or_adjacent_geometry','Luta proficiency','hit_roll_and_defense_reaction','target_RD_resistance','native_vlab_specific_action_adapter','official_snapshot_digest','transactional_acceptance_receipt'],
 'five_gates':{'declaration':'PENDING_SCENE','mechanical_completeness':'INCOMPLETE','native_resolver':'UNSUPPORTED_UNVERIFIED','transactional_security':'NOT_EVALUATED_BY_DMG','source_authority':'DOCUMENTARY_MATH_ONLY'},
 'action_dispatch':'DENY','allowed_for_full_fight':False,'allowed_for_intrinsic_math':True,
 'no_fake_evidence':'Not a combat; native VLAB R23 baseline attack is fictional 1d6 and cannot silently stand for 1d4+DES',
 'ibx':'IBX-90 pre-existing; no ACK, not sent this run'
}
jwrite('VLAB_PREFLIGHT_GALIDEMUS_B1_NO_DISPATCH.json',PREFLIGHT)

# Source-defined sampling support, NOT SCIENTIFIC RUNS: only an audit of which
authoritative={
 'cabra':('BE','Bronze',1),'galidemus':('BE','Bronze',1),'raposa':('BE','Bronze',2),
 'demonio_vermelho':('BE','Prata',1),'felpudo':('BE','Bronze',1),'rato':('BE','Bronze',1),
 'macaco':('BE','Prata',5),'behemoth':('BE','Ouro',1),'ignisaurus':('BE','Ouro',1),'dragon_a':('BE','Ouro',1),
 # dragon B conflict title/body, Guardiao and Wyvern lack verified matching star; omit
 'liu':('ED','Prata',5),
 # Ziha P2 is toggle only, rank not scene-confirmed; omit from frozen rank cells
}
RANKS=['Bronze','Prata','Ouro','Ouro Negro','Lendário']
with open(r/'14_COBERTURA_POSICOES_RN_25_ED_BE.csv','w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['actor_type','rank','star','source_pages_with_explicit_doc_rn','source_keys','full_scene_eligible','rank_position_provisional'])
 w.writeheader()
 for typ in ['ED','BE']:
  for rank in RANKS:
   for star in range(1,6):
    keys=sorted(k for k,v in authoritative.items() if v==(typ,rank,star))
    w.writerow({'actor_type':typ,'rank':rank,'star':star,'source_pages_with_explicit_doc_rn':len(keys),'source_keys':';'.join(keys),'full_scene_eligible':0,'rank_position_provisional':True})

# Exact PMF after adding a printed attribute, not conditional on hit.
EXACT=[]
for did,faces,attr in [('GAL_PATADA',4,13),('CABRA_INVESTIDA',6,13),('FELPUDO_ESPINHOS',4,8)]:
  e=E[did]
  pmf=[{'gross_outcome':r+attr,'probability_numerator':1,'denominator':faces} for r in range(1,faces+1)]
  exactmean=sum(x['gross_outcome'] for x in pmf)/faces
  assert math.isclose(exactmean,float(e['conditional_dme_with_printed_attribute']))
  EXACT.append({'effect_id':did,'source_url':e['source_url'],'model':'one independent uniform die per declared roll; attribute fixed as printed','conditional_on_damage_component_only':True,'no_hit_or_defense_model':True,'pmf':pmf,'min':min(x['gross_outcome'] for x in pmf),'max':max(x['gross_outcome'] for x in pmf),'mean':exactmean})
jwrite('15_PMF_EXATAS_EXEMPLOS.json',EXACT)
COMPARISONS={
 'disclaimer':'Comparação aritmética de efeitos documentados, não emparelhamento F9, não equilíbrio nem efeito em HP',
 'within_behemoth':{'source_url':S['behemoth']['url'],'Estilhacos_intrinseco':7,'Mordida_intrinseco':10.5,'Estilhacos_condicional_DES52':59,'Mordida_condicional_FOR18':28.5,'intrinsic_gap_Mordida_minus_Estilhacos':3.5,'conditional_gap_Estilhacos_minus_Mordida':30.5,'unsupported':['accuracy','RD','mitigation','turn windows','PA','hit']},
 'galidemus_versus_felpudo':{'source_urls':[S['galidemus']['url'],S['felpudo']['url']],'shared_intrinsic_dice':'1d4','intrinsic_dme_each':2.5,'GAL_attribute_DES13':13,'FEL_attribute_DES8':8,'gross_DME_gap_if_both_attack_hit':5,'why_not_matched_pair':'different source families/attack tags, no scene or defense'},
 'internal_conflicts':[{'effect':'FRIO_V3_MAIN','options_dme':[26,11],'accepted_option':None},{'effect':'COLUNA_V2_DOT','options_dme':[10.5,7],'accepted_option':None}],
}
jwrite('16_COMPARACOES_ARITMETICAS_NAO_F9.json',COMPARISONS)
print('ADDITIONAL',len(authoritative),'rank pages',len(EXACT),'pmf fixtures')
