#!/usr/bin/env python3
"""Consultor conversacional dirigido a consultas energéticas do Mestre.
Versão local demonstrativa; o Comestre dialoga normalmente e pode usar este motor
como cálculo auditável. Este parser NÃO é NLP universal; evidência/condições explícitas.
"""
from __future__ import annotations
from pathlib import Path
import re,json,argparse,unicodedata
import pa_r04 as pa
from qmc02_pa_adapter import emit_candidate,qmc_sidecar_receive

def normalise(t):return ''.join(c for c in unicodedata.normalize('NFKD',t.lower()) if not unicodedata.combining(c))

def initial():return {'schema':'PA-DIALOG-STATE-R04-TEST-1','candidate_id':'ESPADA-EXPERIMENTAL-20','item_family':'ARMA','effects':[],
 'daily_semantics':'UNKNOWN','pa_free_declared':None,'history':[]}

def spec(state):
 eff=[]
 for e in state['effects']:
  x={'id':e['id'],'kind':e['kind'],'mode':e['mode'],'magnitude':e['magnitude'],'conditions':e.get('conditions'),'rate':None}
  if e['kind']=='BONUS_DESTREZA':
   x['rate']=5
   x['rate_source']={'source':pa.ANCHORS['amplificador']['url'],'authority':'HIPOTESE_EXPLICITA','scope':'Comparador Party Mestre Espelho; linearidade não validada'}
  eff.append(x)
 return {'candidate_id':state['candidate_id'],'evidence_type':'USER_EXPERIMENTAL_SPEC','name':'Espada mágica proposta','effects':eff,'unknown_synergy':True,'no_new_recipe':True}

def dialogue(state,text):
 t=normalise(text)
 actions=[]
 if ('espada' in t and 'dano' in t) or re.search(r'\+\s*(?:5|10|20)\s*(?:de\s*)?dano',t):
  m=re.search(r'\+\s*(\d+)\s*(?:de\s*)?dano',t)
  if m:
   magnitude=int(m.group(1));found=next((e for e in state['effects'] if e['id']=='DMG_BONUS'),None)
   if found:found['magnitude']=magnitude
   else:state['effects'].append({'id':'DMG_BONUS','kind':'DANO_ADICIONAL_POR_ACERTO','mode':'PASSIVO','magnitude':magnitude,'conditions':'a cada acerto em alvo elegível'})
   actions.append('dano')
 if re.search(r'(?:apenas|so|somente|uma)\s+(?:uma\s+)?vez\s+por\s+dia',t) or ('uma vez por dia' in t):
  e=next((e for e in state['effects'] if e['id']=='DMG_BONUS'),None)
  if e:
   e['mode']='ATIVO';e['conditions']='1x/dia, um acerto elegível após ativação; gatilho exato/duração pendentes'
   actions.append('frequencia_1_dia')
 m=re.search(r'\+\s*(\d+)\s*(?:em|de)?\s*(?:destreza|des)\b',t)
 if m:
  magnitude=int(m.group(1));e=next((e for e in state['effects'] if e['id']=='DES_BONUS'),None)
  if e:e['magnitude']=magnitude
  else:state['effects'].append({'id':'DES_BONUS','kind':'BONUS_DESTREZA','mode':'PASSIVO','magnitude':magnitude,'conditions':'enquanto equipada'})
  actions.append('destreza')
 pfree=re.search(r'\b(\d+)\s*pa\s*livr',t)
 if pfree:state['pa_free_declared']=int(pfree.group(1));actions.append('PA_LIVRE')
 send=bool('craft' in t and ('envi' in t or 'mande' in t or 'pass' in t or 'encaminh' in t))
 if send:actions.append('export_craft')
 if not actions:return state,{'answer':'Consulta não parametrizada: descreva efeito, magnitude, modalidade e custo conhecido; não será inventado custo.','known':False}
 candidate=spec(state);q=pa.proposal(candidate)
 parts=[]
 if 'dano' in actions:
  parts.append('Bônus de dano identificado. Custo PA/dia ou PA/ativação não identificável nos comparadores históricos; não converter dano efetivo automaticamente em PA.')
 if 'frequencia_1_dia' in actions:
  parts.append('Frequência alterada para 1 vez/dia: a parcela de dano passa a ser ATIVA, custo PA/uso desconhecido e manutenção/passivo separado. Limite de uso não determina sozinho o custo.')
 if 'destreza' in actions:
  m=next(e['magnitude'] for e in state['effects'] if e['id']=='DES_BONUS')
  parts.append(f'Adicionado +{m} DES. Pela extrapolação HIPOTÉTICA 5 PA/dia/ponto do Amplificador: subtotal isolado {5*m} PA/dia; não é tarifa canônica, e total da espada permanece indeterminado.')
 if 'PA_LIVRE' in actions:
  parts.append(f'PA Livre informado: {state["pa_free_declared"]}. Sem custo diário total, sem custo de ativação conhecido e sem semântica diária competente, não posso afirmar suficiência. PA Total e comprometido não foram inferidos.')
 if send:
  envelope=emit_candidate(candidate)
  receipt=qmc_sidecar_receive(envelope)
  parts.append('Parecer experimental serializado ao adaptador lateral QMC-02 R04. Recebido somente em TEST, não no validador produtivo nativo, sem receita e sem custo aprovado.')
 else:envelope=None;receipt=None
 state['history'].append({'input':text,'actions':actions})
 return state,{'mode':'PROPOSTA','text':' '.join(parts), 'estimate':q, 'qmc_sidecar_receipt':receipt,'qmc_sidecar_message':envelope,
 'no_new_recipes':True,'interpreter_scope':'PADROES_SINTATICOS_DIRIGIDOS_NAO_NLP_GERAL'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--state',default='consulta_estado.json');p.add_argument('prompt',nargs='+');a=p.parse_args()
 dest=Path(a.state);st=json.loads(dest.read_text('utf8')) if dest.exists() else initial()
 for prompt in a.prompt:
  st,output=dialogue(st,prompt)
  print(json.dumps({'pergunta':prompt,'resposta':output['text'] if 'text' in output else output.get('answer'),'estado_custo':output.get('estimate',{}).get('daily_total_pa'),'craft_receipt':(output.get('qmc_sidecar_receipt') or {}).get('receipt_state')},ensure_ascii=False))
 dest.write_text(json.dumps(st,ensure_ascii=False,indent=2)+'\n','utf8')
