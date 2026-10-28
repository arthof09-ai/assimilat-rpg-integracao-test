"""R221 native R18 battle, stable E ability-occurrence RNG streams, rolled initiative arms.
No historical runners/SQLite reused.
"""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'code'),str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import r221_stable_action_rng_reducer as src
import vlab_r18_interactive as j
PRB=(ROOT/'sources/R221_PREREG_BEFORE_NEW_COMBATS.json').read_bytes();PR=json.loads(PRB);PH=hashlib.sha256(PRB).hexdigest();BON={'V':29,'R':25,'E':30}

def roll(seed,arm):
 dice={k:src.old.dice(seed,f'R221-INIT-{arm}-{k}',4,6) for k in BON};receipts={k:{'dice':list(dice[k]),'bonus':BON[k],'total':sum(dice[k])+BON[k]} for k in BON}
 if len({r['total'] for r in receipts.values()})<3:raise ValueError('BLOCKED_TIE_PRECOMMIT')
 return receipts,sorted(BON,key=lambda k:-receipts[k]['total'])

def execute(seed,arm):
 db=ROOT/'evidence/db'/f'R221_STABLE_{arm}_S{seed}.sqlite';q=ROOT/'evidence/quarantine'/db.name
 if db.exists() or q.exists():raise FileExistsError('R221_ID_COLLISION')
 rolls,order=roll(seed,arm)
 src.init(db,seed,'PROTECTIVE','TEAM_A')
 st,_,rev=j.load(db);assert rev==0
 st['actors']['E']['position']='(0, 4)';st['order']=order;st['active']=order[0]
 st['scene']=f'R221-ACTION-INDEX-CRN-{seed}-{arm}'
 st['r221']={'prereg_sha256':PH,'arm':arm,'rolls':rolls,'order':order,'guard_policy':'VAROK_NO_GUARD_R1','E_position':'(0, 4)','spell_tape':'ABILITY_OCCURRENCE_INDEX','source':'TEST_CONDITIONAL'}
 con=j.connect(str(db));head=j.sha({'seed':seed,'r221_prereg':PH,'rolls':rolls,'order':order,'E_position':'(0,4)','action_rng':'ability_index'})
 with con:
  for k,v in [('state',j.canonical(st)),('scene',st['scene']),('genesis',head),('head',head)]:con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 con.close()
 try:
  for i in range(12):
   st,_,_=j.load(db)
   if st['phase']!='ACTIVE':break
   j.event_commit(str(db),f'LAB-CMD-R216-R221-{seed}-{arm}-{i+1}','R216_INTEGRATED_TURN',{'seed':seed,'pre':src.PH,'actor':st['active']},src.turn)
  st,head,rev=j.load(db)
  return {'seed':seed,'arm':arm,'order':order,'rolls':rolls,'db':db.name,'phase':st['phase'],'commits':rev,'events':len(st['native_events']),'HP':{k:v['hp'] for k,v in st['actors'].items()},'PA':{k:v['pa'] for k,v in st['actors'].items()},'stats':st['r216']['stats'],'decisions':st['r216']['decisions']}
 except Exception:db.rename(q);raise

def main():
 accepted=[];blocked=[]
 for seed in PR['seeds']:
  for arm in PR['arms']:
   try:accepted.append(execute(seed,arm))
   except Exception as e:blocked.append({'seed':seed,'arm':arm,'error':str(e),'class':type(e).__name__})
 pairs=[]
 for seed in PR['seeds']:
  a=[v for v in accepted if v['seed']==seed]
  if len(a)!=2:continue
  x=next(v for v in a if v['arm']=='INIT_A');y=next(v for v in a if v['arm']=='INIT_B')
  pairs.append({'seed':seed,'order_changed':x['order']!=y['order'],'HPdiff_A_minus_B':{k:x['HP'][k]-y['HP'][k] for k in x['HP']},'E_choices_A':[e['chosen'] for e in x['decisions']],'E_choices_B':[e['chosen'] for e in y['decisions']]})
 (ROOT/'evidence/reports/R221_STABLE_ACTION_RNG_EXECUTIONS.json').write_text(json.dumps({'admitted':accepted,'blocked':blocked,'pairs':pairs,'historical_replays':0},indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({'attempts':len(PR['seeds'])*2,'admitted':len(accepted),'blocked':len(blocked),'pairs':len(pairs),'changed_order':sum(x['order_changed'] for x in pairs),'HP_different_pairs':sum(any(x['HPdiff_A_minus_B'].values()) for x in pairs),'choice_different_pairs':sum(x['E_choices_A']!=x['E_choices_B'] for x in pairs)},indent=2))
if __name__=='__main__':main()
