#!/usr/bin/env python3
"""Execução reproduzível do cenário funcional; os dados Party/Mestre são extratos de leitura datados."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(Path(__file__).resolve().parent))
import pa_r11_adapter as m
import qmc_pa_r05_wire

R09=ROOT/'PA_P0_R09_CORRIGENDA_TEST_20261018.zip'
queries=[
'item isolado com +5 DES permanente',
'somente +20 dano fixo adicional',
'apenas +3 metros permanente',
'apenas +3 em teste de ataque',
'apenas +2 CA mágica comprovada',
'apenas +2 CA estrutural',
'+5 DES permanente e RD20',
'Bota Caminho Veloz',
]
results=[]
for q in queries:
 _,r=m.converse(q)
 results.append({'query':q,'daily_subtotal_pa':r['identified_daily_subtotal_pa'],
                 'daily_total_pa':r['daily_total_pa'],'unresolved':r['unresolved'],
                 'historical_R05':r.get('historical_lookup_R05',{}).get('item'),
                 'status':r['approval_status']})

budget_examples={
'novo_item_25_mais_1_ativacao_5':m.budget(pa_total=100,committed_in_snapshot=20,already_includes_item_daily=False,quoted_item_daily=25,activations=[{'event_id':'A1','pa':5}]),
'item_25_ja_comprometido_no_snapshot':m.budget(pa_total=100,committed_in_snapshot=45,already_includes_item_daily=True,quoted_item_daily=25,activations=[{'event_id':'A1','pa':5}]),
'custo_diario_desconhecido':m.budget(pa_total=100,committed_in_snapshot=20,already_includes_item_daily=False,quoted_item_daily=None),
'ativacao_ja_debitada':m.budget(pa_total=100,committed_in_snapshot=20,already_includes_item_daily=False,quoted_item_daily=25,activations=[{'event_id':'A1','pa':5}],already_debited_activation_ids=['A1'])
}
source_readbacks=json.loads((ROOT/'PA_UNIVERSAL_R05_TEST_20261017'/'BASELINES'/'R04_EXTRAIDO'/'PA_UNIVERSAL_R04_TEST_20261017'/'BASELINE_QMC02'/'qmc02'/'source_readbacks.json').read_text())['sources']
bota=next(x for x in source_readbacks if x['uuid']=='3edc2b324ede8135b199fd0cdbb5463c')
wire=qmc_pa_r05_wire.wrap_qualified_source(bota)
receipt=qmc_pa_r05_wire.strict_local_validation(wire)
native=qmc_pa_r05_wire.native_qmc_probe(wire)

quote=m.estimate({'source_class':'USER_EXPERIMENTAL_SPEC','effects':[
 {'id':'des','kind':'ATRIBUTO_PERMANENTE','magnitude':5,'mode':'PASSIVO_DIARIO','permanent_confirmed':True},
 {'id':'rd','kind':'RD','magnitude':10,'mode':'PASSIVO_DIARIO'}], 'all_effects_documented':True})
proposal=m.craft_handoff(quote)

payload={'contract':'PA-R11-R19-DEMO-TEST-1','baseline':'R09','guard':'R10 READ-ONLY',
         'census_R09':m.r09_census(R09),'conversational_queries':results,
         'budget_scenarios':budget_examples,
         'craft_qmc02_original_bota':{
              'historical_daily_pa':wire['message']['daily_pa'],
              'historical_activation_pa_values':wire['message']['activation_pa_values'],
              'qualified_excerpt_sha256':wire['message']['qualified_excerpt_sha256'],
              'qualified_observed_at':wire['message']['qualified_observed_at'],
              'local_receipt':receipt,'native_original_return':native},
         'craft_proposed_r11_handoff':proposal,
         'all_source_signatures':False,'notion_writes':0,'party_writes':0,'master_mirror_writes':0,
         'official_rank_promotions':0,'production_hold':True}
print(json.dumps(payload,ensure_ascii=False,indent=2))
