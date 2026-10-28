"""R05: consulta dirigida a fontes MESTRE, via fornecedor oficial existente R27→R26.

NAO cria formula, NAO define ranks E0, NAO altera historicos, fichas ou CRAFT.
A camada so coordena entradas, diferencia unidades e impede que piso puro seja
interpretado como habilidade demonstrada (reutiliza consumidor R03 existente).
"""
from __future__ import annotations
import hashlib,json,os,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent


def sha256(data:bytes)->str:return hashlib.sha256(data).hexdigest()

def load_sources(p:Path=HERE/'R05_FONTES_TRANSCRITAS_READONLY.json'):
 data=json.loads(p.read_text());assert data['source_count']==12
 assert len({x['uuid'] for x in data['pages']})==12
 return data

def load_original_provider(path:Path):
 if not (path/'ponte_pa_craft_r27.py').exists() or not (path/'engine_r26/parecer_semicanonico_r26.py').exists():
  raise FileNotFoundError('R27_R26_ORIGINAL_MISSING')
 os.environ['PA_R26_ENGINE_DIR']=str(path/'engine_r26')
 sys.path.insert(0,str(path))
 from ponte_pa_craft_r27 import consultar_ficha_craft, SCHEMA_VERSION
 assert SCHEMA_VERSION=='PA-CRAFT-QMC05-COMPAT-R27/1.0.0-TEST'
 from engine_r26.parecer_semicanonico_r26 import avaliar
 return consultar_ficha_craft,avaliar

def request_for(source:dict,*,legacy=True,rank=None,bonus=None,abilities=None):
 family={'BOTA_CAMINHO_VELOZ':'acessório','LAMINA_ECLIPSE':'arma',
         'TOPAZIO_VELOCIDADE':'artefato','TOQUE_CHOCANTE':'outro',
         'ZEPHYR_A':'armadura','ZEPHYR_B':'armadura',
         'AMPLIFICADOR_A':'acessório','AMPLIFICADOR_B':'acessório',
         'ANEL_ALMA':'acessório','BOTAS_VELOCIDADE':'acessório',
         'CAJADO_ECLIPSE':'arma','BOTAS_VENTO_CORTANTE':'acessório'}[source['id']]
 return {'acao':'CONSULTAR_PA_TEST','item':source['title'],'familia':family,
         'rank_item':rank,'historico':legacy,
         'bonus':list(source['bonuses'] if bonus is None else bonus),
         'habilidades':[a.copy() for a in (source['abilities'] if abilities is None else abilities)],
         'pa_historico':source['historic'].copy()}

def annotate_issue(source:dict,prospective:dict)->list[str]:
 issues=[]
 if source['source_item_rank'] is None:issues.append('RI_NAO_DOCUMENTADO_NO_CORPO_CANONICO_DA_PAGINA')
 if source['surface']=='PESSOAL_MESTRE_PARTY_ESPELHO':issues.append('SUPERFICIE_PESSOAL_ESP_MESTRE_NAO_CATALOGO_ITENS_CANONICO')
 if not source['effect_text_present']:issues.append('MECANICA_APENAS_IMAGEM_NAO_INSPECIONADA')
 if source['id'].startswith('ZEPHYR'):issues.append('CONFLITO_HISTORICO_UNIDADE_PA_ZEPHYR_SEM_FUSAO')
 if source['id'].startswith('AMPLIFICADOR'):issues.append('ATRIBUTO_EH_ESCOLHIDO_NAO_DEFINIDO; VALOR_15_TEST_CONDICIONAL')
 if source['id']=='ANEL_ALMA':issues.append('MAIS_50_PA_E_CAPACIDADE_DO_PORTADOR_NAO_CUSTO_POR_DIA')
 if source['id']=='TOQUE_CHOCANTE':issues.append('OURO_NOMINAL_DA_TECNICA_NAO_RE_E0')
 if source['id']=='TOPAZIO_VELOCIDADE':issues.append('DOBRAR_VELOCIDADE_TEMPORARIA_NAO_DESCREVE_DURACAO_NEM_DISTANCIA_BASE')
 if source['id']=='CAJADO_ECLIPSE':issues.append('MULTIPLAS_ATIVAS_E_PASSIVAS_SEM_RI_RE_E0')
 if source['id']=='BOTAS_VENTO_CORTANTE':issues.append('EQUIPAMENTO_COM_MULTIPLOS_EFEITOS_SEM_RI_RE_E0')
 if prospective.get('gate')!='CONSULTA_TEST_PARCIAL_COM_PENDENCIAS':issues.append('REVISAR_STATUS_NATIVO_NAO_PARCIAL')
 return issues

def run_native_roster(data:dict,provider):
 report=[]
 for source in data['pages']:
  historic=provider(request_for(source,legacy=True))
  prospective=provider(request_for(source,legacy=False))
  assert historic['gate']=='DIAGNOSTICO_HISTORICO_SEM_REPRECIFICACAO',(source['id'],historic['gate'])
  assert historic['custo_pa']['pa_por_dia'] is None
  assert historic['custo_pa']['pa_total_no_cenario'] is None
  assert historic['custo_pa']['pa_historico_preservado']==(source['historic'] or None)
  assert prospective['custo_pa']['pa_total_no_cenario'] is None,(source['id'],prospective['gate'])
  assert historic['governanca']['party_write'] is False and prospective['governanca']['party_write'] is False
  assert not historic['governanca']['historico_reprecificado']
  report.append({'id':source['id'],'uuid':source['uuid'],'surface':source['surface'],
          'source_last_edited':source['last_edited'], 'original_cost_typed':source['historic'],
          'retained_original_pa':historic['custo_pa']['pa_historico_preservado'],
          'diagnostic_prospective_cost':None, 'provider_legacy_gate':historic['gate'],
          'provider_prospective_gate':prospective['gate'],
          'native_provider_issue_count':len(prospective['pendencias']),
          'gaps':annotate_issue(source,prospective),
          'official_PA_updated':False,'RE_E0_claimed':False,'Party_write':False})
 return report

def parametric_amplifier_test(data:dict,provider):
 # DESCRICAO ORIGINAL não especifica QUAL atributo.
 # 6 COPIAS DE LAB mostram invariância da tarifa de +3 para qualquer 1 atributo;
 # pressupõe BRONZE somente conforme decisão textual Mestre, não deduzido do Notion.
 source=next(x for x in data['pages'] if x['id']=='AMPLIFICADOR_A')
 variants={'FOR':'Força','DES':'Destreza','CON':'Constituição',
           'INT':'Inteligência','SAB':'Sabedoria','CAR':'Carisma'}
 examples=[]
 for key,attribute in variants.items():
  candidate=request_for(source,legacy=False,rank='Bronze',bonus=[f'+3 de {attribute}'])
  o=provider(candidate)
  c=o['custo_pa'];assert (c['pa_por_dia'],c['pa_ativacoes_no_cenario'],c['pa_total_no_cenario'])==(15,0,15),(key,c,o['pendencias'])
  assert o['gate']=='CONSULTA_TEST_COMPLETA_COM_REVISAO_JIT'
  examples.append({'attribute_variant':key,'result_native_R27':c['pa_total_no_cenario'],
       'rank_Bronze_source':'MESTRE_EXPLICITO_EM_CONVERSA; NAO_PROVADO_PELO_CORPO_NOTION_DA_FICHA',
       'official_cost_changed':False})
 assert len(examples)==6
 return {'source_uuid':source['uuid'], 'source_excerpt':source['excerpt'],
         'historic_pa_day':15,'variants':examples,'invariant_test_total':15,
         'guard':'RESULTADO_CONDICIONAL_E3_TEST_SEM_MODIFICAR_HISTORICO',
         'source_note':'Nao escolher atributo arbitrariamente; variacoes simuladas separadas do item historico.'}

def rank_only_negative_canary(consult, native_avaliar):
 # Representa técnica cuja descrição mecânica está somente em IMAGEM.
 # Propositalmente modelado como item Ouro incorreto para demonstrar
 # por que rank sozinho não libera custo: R27 gera 21 do piso.
 q={'acao':'CONSULTAR_PA_TEST','item':'Toque Chocante (O) CANARIO','familia':'outro',
       'rank_item':'Ouro','habilidades':[],'bonus':[], 'historico':False}
 raw=consult(q)
 assert raw['gate']=='CONSULTA_TEST_COMPLETA_COM_REVISAO_JIT'
 assert raw['custo_pa']['pa_por_dia']==21
 from R03_CONSUMIDOR_READONLY_TEST import consumir_consulta
 safe=consumir_consulta('Item: Toque Chocante (O) CANARIO\nRank do item: Ouro',avaliar_nativo=native_avaliar)
 assert safe['state']=='HOLD_ITEM_SEM_EFEITO_DESCRITO'
 assert safe['scenario_pa'] is None and safe['production']=='HOLD'
 return {'source_uuid':'3edc2b324ede81f79aaaeb6c8c10729e','artificial_rank_input':True,
         'raw_native_daily_floor':21, 'safe_existing_R03_state':safe['state'],
         'safe_scenario_total':safe['scenario_pa'], 'official_P_A':None,
         'not_a_native_tariff_bug':'Custo matematico valido de piso, mas foi usado indevidamente como prova de efeito. Falha de gate consumidor.',
         'production':'HOLD'}

def main(provider_dir:Path, consumer_dir:Path):
 data=load_sources()
 provider,native=load_original_provider(provider_dir)
 sys.path.insert(0,str(consumer_dir))
 results=run_native_roster(data,provider)
 amp=parametric_amplifier_test(data,provider)
 floor=rank_only_negative_canary(provider,native)
 assert next(x for x in results if x['id']=='ZEPHYR_A')['original_cost_typed']=={'daily_pa':90}
 assert next(x for x in results if x['id']=='ZEPHYR_B')['original_cost_typed']=={'per_turn_pa':90}
 assert next(x for x in results if x['id']=='ANEL_ALMA')['original_cost_typed']=={'capacity_bonus_pa':50}
 assert sum(x['surface']=='ITENS_MESTRE_CATALOGO' for x in results)==4
 assert sum(x['surface']=='PESSOAL_MESTRE_PARTY_ESPELHO' for x in results)==8
 result={'contract':'PA_R05_CATALOGO_MASTER_ONLY_READONLY_TEST/1.0',
         'source_count':len(results),'canonical_item_pages':4,'personal_mirror_pages':8,
         'native_historical_consultations':len(results),'native_prospective_incomplete_consultations':len(results),
         'conditional_variants':6,'negative_rank_only_canary':1,
         'original_provider':'R27→R26 ORIGINAL PINNED','source_snapshot_sha256':sha256((HERE/'R05_FONTES_TRANSCRITAS_READONLY.json').read_bytes()),
         'results':results,'conditional_amplifier':amp,'rank_only_canary':floor,
         'native_source_page_changes':0,'notion_writes':0,'party_writes':0,
         'production_status':'HOLD','E0_decisions_issued':0,
         'scope':'MESTRE_ONLY_TEST'}
 p=HERE/'R05_RESULTS_REPRODUCIBLE.json';p.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ('source_count','canonical_item_pages','personal_mirror_pages','native_historical_consultations','native_prospective_incomplete_consultations','conditional_variants','negative_rank_only_canary','production_status')},ensure_ascii=False,indent=2))
 return result

if __name__=='__main__':
 if len(sys.argv)!=3:raise SystemExit('Usage: python R05_CONSULTA_CATALOGO_READONLY.py [provider_dir] [consumer_dir]')
 main(Path(sys.argv[1]),Path(sys.argv[2]))
