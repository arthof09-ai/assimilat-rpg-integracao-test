#!/usr/bin/env python3
"""R04: camada científica conservadora SOBRE o motor R03, sem substituir o original.
EVIDENCE != PRICE LAW. Nada escreve em Notion, CRAFT canônico ou Party.
"""
from __future__ import annotations
import json,math,sys,statistics
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parent
R03=ROOT/'BASELINE_PA_R03'
sys.path.insert(0,str(R03))
import pa_engine_v3 as r03
MASTER='MESTRE-SIDE'

ANCHORS={
 'amplificador':{'url':'https://app.notion.com/p/3c6c2b324ede82baa4a801de533a5975','surface':'PARTY_MESTRE_ESPELHO','literal':'+3 em um Atributo. 15 PA por dia.','family':'atributo_puro_observado','magnitude':3,'daily_pa':15},
 'sabedoria_ancestral':{'url':'https://app.notion.com/p/3edc2b324ede815699adc0412e96ea2b','surface':'RPG_ITENS','literal':'+10 Sabedoria, outros efeitos; 20 PA isolados ao final da descrição, regra R-PA-DIA sob análise','family':'atributo_misto','magnitude':10,'daily_pa':20,'daily_status':'REGRA_R_PA_DIA_SENSIVEL'},
 'amuleto_inteligencia':{'url':'https://app.notion.com/p/0c4c2b324ede83dd8e1881b52a79e326','surface':'FICHA_ANTIGA_ORIGEM_A_AUDITAR','literal':'+10 INT, +20 dano mágico ou +20 resistência; 30 PA isolados','family':'atributo_misto','magnitude':10,'daily_pa':30,'daily_status':'REGRA_R_PA_DIA_SENSIVEL'},
 'mobilidade':{'url':'https://app.notion.com/p/383c2b324ede820ab38881abbe91ac60','surface':'PARTY_MESTRE_ESPELHO','literal':'+2 CA quando faz movimento, armadura pesada com restrição; 7 PA por dia','family':'ca_condicional','magnitude':2,'daily_pa':7},
 'armadura_ana':{'url':'https://app.notion.com/p/5f7c2b324ede83de9c7a81fcb19b0195','surface':'PARTY_MESTRE_ESPELHO','literal':'+2 CA, -2m, reação anti-empurrão; 6 PA/dia','family':'ca_misto','magnitude':2,'daily_pa':6},
 'zephyr':{'url':'https://app.notion.com/p/a23c2b324ede829bb8168165991577ff','surface':'PARTY_MESTRE_ESPELHO','literal':'+11 CA, +15 DES, +15m, +25 ataque, +50 vento/turno; 90 PA/dia já somado','family':'dano_misto','magnitude':50,'daily_pa':90},
 'bota':{'url':'https://app.notion.com/p/3edc2b324ede8135b199fd0cdbb5463c','surface':'RPG_ITENS','literal':'18 PA/dia e 5 PA pela habilidade Velocidade Sobrenatural','family':'misto_mobilidade','daily_pa':18,'activation_pa':5},
 'arco_elemental':{'url':'https://app.notion.com/p/3edc2b324ede8156849bf1aae0ce9fb5','surface':'RPG_ITENS','literal':'64 PA/dia com 8d8+25, +8d12+10 contra elementais, +15 percepção para rastrear elementais','family':'dano_misto_condicional','daily_pa':64},
 'armadura_elemental':{'url':'https://app.notion.com/p/3edc2b324ede8127a576ee01c44bd1d4','surface':'RPG_ITENS','literal':'55 PA/dia com defesa específica elemental','family':'defesa_mista_condicional','daily_pa':55}
}

# Structural identifiability criterion: mixed-feature total != isolated marginal coefficient.
def coefficients()->dict:
 return {
  'attr_any':{'unit':'PA/dia por ponto de atributo','status':'NAO_IDENTIFICAVEL_UNIVERSALMENTE','point_estimate':None,'generalizable_interval':None,'observations':['amplificador','sabedoria_ancestral','amuleto_inteligencia'],
    'proof':'Para cenário aditivo linear de 5 PA/ponto, 10 SAB requer >=50 PA/dia antes de outros efeitos, versus total de 20 PA/dia interpretado; 10 INT exige >=50 versus 30; contradição condicional às interpretações e não negatividade. Fontes de espelho/ambíguas não comprovam tarifa canônica universal.'},
  'attr_pure_amplificador':{'unit':'PA/dia por ponto (mesma condição do Amplificador)','status':'RAZAO_HISTORICA_LOCAL_UMA_OBSERVACAO','value':5,'sample_independent_groups':1,'source':ANCHORS['amplificador']['url'],'surface':ANCHORS['amplificador']['surface'],'generalize':False},
  'ca_conditional_movement':{'unit':'PA/dia por +1 CA após ação de movimento','status':'RAZAO_HISTORICA_LOCAL_UMA_OBSERVACAO','value':3.5,'sample_independent_groups':1,'source':ANCHORS['mobilidade']['url'],'surface':ANCHORS['mobilidade']['surface'],'generalize':False},
  'ca_unconditional':{'unit':'PA/dia por +1 CA universal','status':'NAO_IDENTIFICAVEL','value':None,'confounding':'Armadura Anã inclui desvantagem de movimento e reação; Mobilidade é condicional.'},
  'rd':{'unit':'PA/dia por +1 RD','status':'NAO_IDENTIFICAVEL','value':None},
  'rdm':{'unit':'PA/dia por +1 RDM','status':'NAO_IDENTIFICAVEL','value':None},
  'damage_bonus_passive':{'unit':'PA/dia por +1 dano/ataque','status':'NAO_IDENTIFICAVEL','value':None,'confounding':'Itens históricos possuem dano base, efeitos extras, alvos, duração e modalidade diferentes.'},
  'damage_bonus_active':{'unit':'PA/ativação por +1 dano','status':'NAO_IDENTIFICAVEL','value':None},
  'passive_vs_active_premium':{'unit':'multiplicador por modalidade','status':'NAO_IDENTIFICAVEL','value':None},
  'healing':{'unit':'PA por unidade de cura / duração','status':'NAO_IDENTIFICAVEL','value':None},
  'movement':{'unit':'PA/dia por metro ou PA/ativação por metro','status':'NAO_IDENTIFICAVEL','value':None},
  'protection_elemental':{'unit':'PA/dia por unidade condicional','status':'NAO_IDENTIFICAVEL','value':None},
  'perception':{'unit':'PA/dia por ponto sob alvo condicionado','status':'NAO_IDENTIFICAVEL','value':None},
  'saves':{'unit':'PA/dia por salvaguarda','status':'NAO_IDENTIFICAVEL','value':None},
  'control':{'unit':'PA/uso por severidade, alcance, duração','status':'NAO_IDENTIFICAVEL','value':None}
 }

def identified_bounds()->dict:
 """Bounds are explicitly conditional to strict linear nonnegative component model.
 Crucial: if daily interpreted is invalid or interaction/discount exists, bounds also invalid.
 """
 return {'assumptions':['PA/dia interpretado verdadeiro','todas parcelas nao negativas','contribuicao linear do atributo','sem descontos/interacoes/creditos','mesma modalidade e unidade'],
 'sabedoria_misto':{'conditional_upper_bound_per_point':2,'source':ANCHORS['sabedoria_ancestral']['url'],'status':'BOUND_CONDICIONAL_NAO_CANONICO'},
 'inteligencia_misto':{'conditional_upper_bound_per_point':3,'source':ANCHORS['amuleto_inteligencia']['url'],'status':'BOUND_CONDICIONAL_NAO_CANONICO'},
 'atributo_puro':{'observed_ratio':5,'source':ANCHORS['amplificador']['url'],'status':'RAZAO_LOCAL'},
 'intersection_with_single_beta_5':'VAZIA_SOB_HIPOTESES', 'scientific_conclusion':'NAO_IDENTIFICABILIDADE OU FALHA DAS HIPOTESES; NAO CALIBRAR TARIFA GLOBAL'}

def damage_increment(base_damage:float,extra:float,rd:float,attempts:float=1,p_hit:float=1,eligible:float=1,targets:float=1)->dict:
 for a in (base_damage,extra,rd,attempts,p_hit,eligible,targets):
  if not isinstance(a,(float,int)) or isinstance(a,bool) or not math.isfinite(a) or a<0:raise ValueError('Parâmetros finitos e nao negativos')
 if p_hit>1 or eligible>1:raise ValueError('Probabilidade entre 0 e 1')
 delta=max(0,base_damage+extra-rd)-max(0,base_damage-rd)
 return {'increment_effective_per_eligible_hit':delta,'expected_increment':delta*attempts*p_hit*eligible*targets,
 'units':'dano efetivo, NAO PA','assumptions':{'base_damage':base_damage,'extra':extra,'RD':rd,'attempts':attempts,'p_hit':p_hit,'eligible':eligible,'targets':targets},'energy_cost_pa':None,'model_status':'PA_NAO_IDENTIFICAVEL'}

def _nonnegative(x,field):
 if not isinstance(x,(int,float)) or isinstance(x,bool) or not math.isfinite(x) or x<0:raise ValueError(field+' precisa ser numero finito nao negativo')
 return x

def proposal(spec:dict)->dict:
 """A proposed item can have several effects; each rate must carry approved scope and provenance.
 Nonidentifiable dimensions keep total None, never silently 0.
 """
 effects=spec.get('effects',[])
 if not isinstance(effects,list):raise ValueError('effects list')
 seen=set();parts=[];daily=0;active=0;missing_daily=[];missing_active=[]
 for e in effects:
  eid=e.get('id');typ=e.get('mode');mag=_nonnegative(e.get('magnitude'),str(eid))
  if not eid or eid in seen:raise ValueError('efeito duplicado ou sem ID')
  if typ not in ('PASSIVO','ATIVO'):raise ValueError('modo nao definido')
  seen.add(eid)
  rate=e.get('rate');r=e.get('rate_source');unit='PA/dia' if typ=='PASSIVO' else 'PA/uso'
  valid=bool(isinstance(rate,(int,float)) and not isinstance(rate,bool) and math.isfinite(rate) and rate>=0 and isinstance(r,dict)
             and r.get('source') and r.get('authority') in ('HIPOTESE_EXPLICITA','MODELO_ANALITICO_VALIDADO'))
  # Never treat local historical ratio as validated coefficient if extrapolated.
  if valid: val=mag*rate; (lambda:None)();daily+=val if typ=='PASSIVO' else 0;active+=val if typ=='ATIVO' else 0
  else:val=None;(missing_daily if typ=='PASSIVO' else missing_active).append(eid)
  parts.append({'id':eid,'kind':e.get('kind'),'mode':typ,'magnitude':mag,'unit':unit,'rate':rate if valid else None,
   'value':val,'source':r if valid else None,'effect_conditions':e.get('conditions'),'status':'CENARIO_PARAMETRICO' if valid else 'ENERGIA_NAO_IDENTIFICADA'})
 base=spec.get('documented_base_pa_daily')
 if base is not None:_nonnegative(base,'base PA')
 if spec.get('daily_base_includes_effects') and base is not None:
  # If historical aggregate already includes component effects, report base as historical total, do not add them again.
  cost=base
  accounting='CUSTO_AGREGADO_HISTORICO_INCLUI_COMPONENTES; DELTAS NAO ADITIVOS'
 elif spec.get('daily_base_includes_effects'):
  cost=None;accounting='AGREGADO_NAO_DOCUMENTADO'
 else:
  cost=None if missing_daily else daily+(base or 0)
  accounting='SOMATORIO_HIPOTETICO_INDEPENDENTE; SINERGIAS_NAO_CALIBRADAS' if effects else 'SEM_COMPONENTES'
 if spec.get('unknown_synergy',True) and not spec.get('daily_base_includes_effects') and cost is not None:
  cost=None;accounting='SINERGIA_DESCONHECIDA; SUBTOTAL_PROPOSTO_NAO_TOTAL'
 return {'mode':'PROPOSTA','name':spec.get('name','candidato TEST'),'components':parts,'daily_component_subtotal_scenario':daily,
 'daily_total_pa':cost,'per_use_component_subtotal_scenario':active,'per_use_total_pa':None if missing_active else active,
 'missing_daily_components':missing_daily,'missing_active_components':missing_active,
 'accounting':accounting,'experimental_not_approved':True,'historical_sources_unchanged':True,'craft_released':False,'new_recipes_permitted':False}

def budget(pa_total:float,other_commitments:float,documented_daily:float|None=None,activation_cost:float|None=None,requests:int=1, daily_semantics:str='UNKNOWN')->dict:
 pa_total=_nonnegative(pa_total,'PA total');other_commitments=_nonnegative(other_commitments,'outros compromissos')
 if other_commitments>pa_total:raise ValueError('compromisso > total')
 if daily_semantics not in ('UNKNOWN','COMMIT','DEBIT'):raise ValueError('semantica diaria')
 if not isinstance(requests,int) or isinstance(requests,bool) or requests<0:raise ValueError('usos')
 if documented_daily is not None:_nonnegative(documented_daily,'diario')
 if activation_cost is not None:_nonnegative(activation_cost,'ativacao')
 free=pa_total-other_commitments
 ans={'pa_total':pa_total,'pa_comprometido_comprovado':other_commitments,'pa_livre_antes':free,
   'manutencao_documentada_pa_dia':documented_daily,'custo_por_ativacao_pa':activation_cost,
   'solicitacoes_uso':requests,'semantica_manutencao':daily_semantics,'item_spell_exhaustion':'NAO_INFERIDA',
   'can_authorize_use':False,'operation':'CONSULTA_SEM_MUTACAO'}
 if daily_semantics=='UNKNOWN':ans['verdict']='INDETERMINADO_SEMANTICA_DIA';return ans
 if documented_daily is None:ans['verdict']='INDETERMINADO_CUSTO_DIA';return ans
 if activation_cost is None and requests:ans['verdict']='INDETERMINADO_CUSTO_ATIVACAO';return ans
 if daily_semantics=='COMMIT':
  available=free-documented_daily
  ans['pa_livre_cenario_apos_comprometimento_diario']=available if available>=0 else None
  need=(activation_cost or 0)*requests
  ans['verdict']='COBERTURA_NUMERICA_CONDICIONAL' if available>=need else 'INSUFICIENTE_NO_CENARIO'
 else:
  if documented_daily>free:ans['verdict']='INSUFICIENTE_NO_CENARIO';return ans
  need=documented_daily+(activation_cost or 0)*requests
  ans['verdict']='COBERTURA_NUMERICA_CONDICIONAL' if free>=need else 'INSUFICIENTE_NO_CENARIO'
 ans['can_authorize_use']=False
 ans['authorization_reason']='Semântica diaria escolhida como cenário não é canonização de débito/compromisso; contexto de PA corrente e outras reservas precisa ser confirmado'
 return ans

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['coefficients','bounds','historical','proposal','budget','damage20']);p.add_argument('argument',nargs='?');a=p.parse_args()
 if a.mode=='coefficients':o=coefficients()
 elif a.mode=='bounds':o=identified_bounds()
 elif a.mode=='historical':o=r03.historical(a.argument)
 elif a.mode=='proposal':o=proposal(json.loads(Path(a.argument).read_text('utf8')))
 elif a.mode=='budget':o=budget(**json.loads(Path(a.argument).read_text('utf8')))
 else:o=[damage_increment(15,n,25,attempts=a, p_hit=.6) for n in [5,10,20] for a in [1,2,3]]
 print(json.dumps(o,ensure_ascii=False,indent=2))
