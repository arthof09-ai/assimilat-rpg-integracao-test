"""R220 genuine noncommutative source-init order TEST, R18 native. Never history replay."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'code'),str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import r220_noncommutative_source_reducer as src
import vlab_r18_interactive as j
PRB=(ROOT/'sources/R220_PREREG_BEFORE_NEW_COMBATS.json').read_bytes();PR=json.loads(PRB);PH=hashlib.sha256(PRB).hexdigest();B={'V':29,'R':25,'E':30}

def rolled(seed,arm):
 rolls={k:src.old.dice(seed,f'R220-INIT-{arm}-{k}',4,6) for k in B}
 rec={k:{'dice':list(rolls[k]),'bonus':B[k],'total':sum(rolls[k])+B[k]} for k in B}
 if len({x['total'] for x in rec.values()})<3:raise ValueError('BLOCKED_TIE_PRECOMMIT')
 return rec,sorted(B,key=lambda k:-rec[k]['total'])

def run(seed,arm):
 db=ROOT/'evidence/db'/f'R220_GUARD_CHOICE_{arm}_S{seed}.sqlite';q=ROOT/'evidence/quarantine'/db.name
 if db.exists() or q.exists():raise FileExistsError('RUN_ID_ALREADY_CONSUMED')
 rec,order=rolled(seed,arm)
 src.init(db,seed,'PROTECTIVE','TEAM_A')
 st,_,rev=j.load(db);assert rev==0
 st['actors']['E']['position']='(0, 4)'
 st['order']=order;st['active']=order[0]
 st['scene']=f'R220-SOURCE-ORDER-REACTION-HEAL-{seed}-{arm}'
 st['r220']={'prereg_sha256':PH,'arm':arm,'rolls':rec,'order':order,'guard_policy':'VAROK_NO_GUARD_R1','E_position':'(0, 4)','source_status':'TEST_CONDITIONAL'}
 con=j.connect(str(db));head=j.sha({'seed':seed,'r220_prereg':PH,'order':order,'rolls':rec,'Epos':'(0, 4)','V_R1_guard':False})
 with con:
  for k,v in [('state',j.canonical(st)),('scene',st['scene']),('genesis',head),('head',head)]:con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 con.close()
 try:
  for i in range(12):
   st,_,_=j.load(db)
   if st['phase']!='ACTIVE':break
   j.event_commit(str(db),f'LAB-CMD-R216-R220-{seed}-{arm}-{i+1}','R216_INTEGRATED_TURN',{'seed':seed,'pre':src.PH,'actor':st['active']},src.turn)
  st,head,rev=j.load(db)
  return {'seed':seed,'arm':arm,'order':order,'rolls':rec,'db':db.name,'commits':rev,'events':len(st['native_events']),'phase':st['phase'],'HP':{k:v['hp'] for k,v in st['actors'].items()},'PA':{k:v['pa'] for k,v in st['actors'].items()},'decisions':st['r216']['decisions'],'stats':st['r216']['stats']}
 except Exception:
  db.rename(q);raise

def main():
 admitted=[];blocked=[]
 for seed in PR['new_seeds']:
  for arm in PR['arms']:
   try:admitted.append(run(seed,arm))
   except Exception as e:blocked.append({'seed':seed,'arm':arm,'reason':str(e),'class':type(e).__name__})
 pairs=[]
 for seed in PR['new_seeds']:
  x=[a for a in admitted if a['seed']==seed]
  if len(x)!=2:continue
  a=next(v for v in x if v['arm']=='INIT_A');b=next(v for v in x if v['arm']=='INIT_B')
  pairs.append({'seed':seed,'order_A':a['order'],'order_B':b['order'],'order_changed':a['order']!=b['order'],'terminal_deltaHP_AminusB':{k:a['HP'][k]-b['HP'][k] for k in a['HP']},'terminal_deltaPA_AminusB':{k:a['PA'][k]-b['PA'][k] for k in a['PA']},'E_decisions_A':[v['chosen'] for v in a['decisions']],'E_decisions_B':[v['chosen'] for v in b['decisions']]})
 output={'admitted':admitted,'blocked':blocked,'pairs':pairs,'prior_combat_replays':0};(ROOT/'evidence/reports/R220_NONCOMMUTATIVE_EXECUTIONS.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'admitted':len(admitted),'blocked':len(blocked),'pairs':len(pairs),'changed_order':sum(x['order_changed'] for x in pairs),'HP_differences':sum(any(d for d in x['terminal_deltaHP_AminusB'].values()) for x in pairs),'E_decision_differences':sum(x['E_decisions_A']!=x['E_decisions_B'] for x in pairs)},indent=2))
if __name__=='__main__':main()
