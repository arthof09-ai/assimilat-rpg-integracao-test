"""New R219 source-rolled initiative pairs with pre-existing Varok wound in fixture.
Original source abilities/resolvers R216 remain unchanged. Never execute on historical DBs.
"""
from pathlib import Path
import json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'code'),str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import r219_native_wounded_r216_addonly as src
import vlab_r18_interactive as j
PRB=(ROOT/'sources/R219_PREREG_BEFORE_NEW_COMBATS.json').read_bytes();PR=json.loads(PRB);PH=hashlib.sha256(PRB).hexdigest()
BONUS={'V':29,'R':25,'E':30}

def roll(seed,arm):
 r={k:src.old.dice(seed,f'R219-INIT-{arm}-{k}',4,6) for k in BONUS}
 receipts={k:{'dice':list(r[k]),'bonus':BONUS[k],'total':sum(r[k])+BONUS[k]} for k in BONUS}
 if len({x['total'] for x in receipts.values()})<3:raise ValueError('BLOCKED_TIE_PRECOMMIT')
 return receipts,sorted(BONUS,key=lambda k:-receipts[k]['total'])

def run(seed,arm):
 db=ROOT/'evidence/db'/f'R219_INJURED_{arm}_S{seed}.sqlite'
 quarantine=ROOT/'evidence/quarantine'/db.name
 if db.exists() or quarantine.exists():raise FileExistsError('R219_RUN_ALREADY_CONSUMED')
 rolls,order=roll(seed,arm)
 src.init(db,seed,'PROTECTIVE','TEAM_A')
 st,_,rev=j.load(db);assert rev==0
 st['actors']['V']['hp']=PR['initial_state_TEST']['V_HP']
 st['order']=order;st['active']=order[0]
 st['scene']=f'R219-INJURED-SOURCE-ROLLED-INIT-{seed}-{arm}'
 st['r219']={'prereg_sha256':PH,'arm':arm,'rolls':rolls,'order':order,'starting_V_hp':614,'start_V_max':734,'external_initial_state_fixture':True}
 con=j.connect(str(db));head=j.sha({'seed':seed,'r219_prereg':PH,'rolls':rolls,'order':order,'pre_existing_injury':120})
 with con:
  for k,v in [('state',j.canonical(st)),('scene',st['scene']),('genesis',head),('head',head)]:con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 con.close()
 try:
  for i in range(12):
   st,_,_=j.load(db)
   if st['phase']!='ACTIVE':break
   j.event_commit(str(db),f'LAB-CMD-R216-R219-{seed}-{arm}-{i+1}','R216_INTEGRATED_TURN',{'seed':seed,'pre':src.PH,'actor':st['active']},src.turn)
  st,head,rev=j.load(db)
  return {'seed':seed,'arm':arm,'db':db.name,'order':order,'rolls':rolls,'phase':st['phase'],'commits':rev,'events':len(st['native_events']),'HP':{k:v['hp'] for k,v in st['actors'].items()},'PA':{k:v['pa'] for k,v in st['actors'].items()},'stats':st['r216']['stats'],'decisions':st['r216']['decisions']}
 except Exception:
  db.rename(quarantine)
  raise

def main():
 admitted=[];blocked=[]
 for seed in PR['seeds']:
  for arm in PR['arms']:
   try:admitted.append(run(seed,arm))
   except Exception as e:blocked.append({'seed':seed,'arm':arm,'reason':str(e),'class':type(e).__name__})
 pairs=[]
 for seed in PR['seeds']:
  a=[x for x in admitted if x['seed']==seed]
  if len(a)==2:
   x=next(x for x in a if x['arm']=='INIT_A');y=next(x for x in a if x['arm']=='INIT_B')
   pairs.append({'seed':seed,'orderA':x['order'],'orderB':y['order'],'orderChanged':x['order']!=y['order'],'HPdeltasAminusB':{k:x['HP'][k]-y['HP'][k] for k in x['HP']},'PAdeltasAminusB':{k:x['PA'][k]-y['PA'][k] for k in x['PA']}})
 output={'admitted':admitted,'blocked':blocked,'pairs':pairs,'prior_history_replays':0}
 (ROOT/'evidence/reports/R219_WOUNDED_ROLLED_RESULTS.json').write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({'attempted':len(PR['seeds'])*len(PR['arms']),'admitted':len(admitted),'blocked':len(blocked),'pairs':len(pairs),'changed_order_pairs':sum(x['orderChanged'] for x in pairs),'HP_DIFF_PAIRS':sum(any(y!=0 for y in x['HPdeltasAminusB'].values()) for x in pairs),'PA_DIFF_PAIRS':sum(any(y!=0 for y in x['PAdeltasAminusB'].values()) for x in pairs)},indent=2))
if __name__=='__main__':main()
