#!/usr/bin/env python3
"""Dez cenas A-J; evidência human-readable + JSON, preservando estado nas falas encadeadas."""
from pathlib import Path
import json
from consultor_pa_r05 import initial, interpret
from qmc_pa_r05_wire import wrap_qualified_source,strict_local_validation,native_qmc_probe
from pa_r05 import available_pa_budget
P=Path(__file__).resolve().parent.parent
base=P/'BASELINES'/'R04_EXTRAIDO'/'PA_UNIVERSAL_R04_TEST_20261017'
src=json.loads((base/'BASELINE_QMC02'/'qmc02'/'source_readbacks.json').read_text('utf8'))['sources']
bota=next(x for x in src if x['uuid']=='3edc2b324ede8135b199fd0cdbb5463c')

def run():
 out=[]
 def single(label,prompt):
  state,resp=interpret(initial(),prompt)
  out.append({'case':label,'dialogue':[prompt],'answer':resp['answer'],'result':resp,'mode':resp['mode'],'daily':resp['historical_daily_pa_usable'] if resp['mode']=='HISTORICO' else resp['energy']['daily_total_pa']})
 single('A_HISTORICO_DIARIO','Qual é o PA da Bota Caminho Veloz?')
 single('B_HISTORICO_ATIVACAO','Quanto PA por ativação gasta o Amuleto Tempo Eterno?')
 single('C_COMPOSTO','Quero uma espada com +5 DES, +20 de dano e uma habilidade ativável de movimentação.')
 single('D_ATRIBUTO_ISOLADO','Quanto PA por dia custaria um item que aumenta minha Destreza em +5?')
 single('E_DANO_ISOLADO','Quanto PA custa uma espada que acrescenta +20 dano em cada acerto?')
 single('F_DESCONHECIDO_DEFESA','Quanto PA custa uma armadura com RD 20 contra ataques elementais?')
 single('G_CONFLITO_HISTORICO','Qual PA do Sabedoria Ancestral?')
 single('H_ESPELHO_IDENTIFICADO','Quanto PA custa Amplificador de Atributo?')
 q=['Espada com +20 dano em cada acerto','E se a habilidade for ativada uma vez por dia?','E se a duração for 10 minutos?']
 s=initial();responses=[]
 for x in q:s,z=interpret(s,x);responses.append(z)
 out.append({'case':'I_DURACAO_E_FREQUENCIA','dialogue':q,'answer':responses[-1]['answer'],
             'result':responses[-1],'mode':'PROPOSTA','daily':responses[-1]['energy']['daily_total_pa']})
 q2=['Quero uma espada com +20 dano por acerto','Agora acrescente +5 DES','Esse item pode funcionar com 80 PA livres?','Envie essa avaliação energética ao CRAFT']
 s=initial();responses=[]
 for x in q2:s,z=interpret(s,x);responses.append(z)
 out.append({'case':'J_EXPORT_CRAFT','dialogue':q2,'answer':responses[-1]['answer'],'mode':'PROPOSTA',
             'daily':responses[-1]['energy']['daily_total_pa'],'result':responses[-1],
             'native_accepted':responses[-1]['craft_native_probe']['native_accepted']})
 hist=wrap_qualified_source(bota)
 receipts={'history_test':strict_local_validation(hist),'history_native':native_qmc_probe(hist),
           'candidate_test':responses[-1]['craft_test_receipt'],'candidate_native':responses[-1]['craft_native_probe']}
 (P/'RESULTADOS'/'RECIBOS_QMC_R05.json').write_text(json.dumps({'historical_wire':hist,'receipts':receipts},ensure_ascii=False,indent=2)+'\n','utf8')
 (P/'RESULTADOS'/'CENARIOS_A_J_R05.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n','utf8')
 (P/'RESULTADOS'/'CONSULTOR_DEMONSTRACAO_R05.txt').write_text('\n\n'.join(x['case']+'\n'+' -> '.join(x['dialogue'])+'\n'+x['answer'] for x in out)+'\n','utf8')
 assert len(out)==10 and all('result' in x for x in out)
 print(json.dumps({'scenarios':len(out),'D_ATTR_PA':out[3]['daily'],'C_MIXED_PA':out[2]['daily'],
                 'HISTORICAL_TEST':'RECEBIDO','QMC_NATIVE_ACCEPTED':False,'craft_receipt':receipts['candidate_test']['status']},ensure_ascii=False))
 return out
if __name__=='__main__':run()
