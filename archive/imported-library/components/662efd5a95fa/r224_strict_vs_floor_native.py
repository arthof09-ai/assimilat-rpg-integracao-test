"""Source-gated paired new combat experiments R224: STRICT_HOLD vs TENTATIVE_FLOOR, never replay old IDs."""
import sys,json,hashlib,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'code'),str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import r222_round_reducer as strict
import r223_round_reducer as floor
import vlab_r18_interactive as j
PRE=(ROOT/'sources/R224_PREREG_BEFORE_NEW_COMBATS.json').read_bytes();P=json.loads(PRE);PH=hashlib.sha256(PRE).hexdigest();B={'V':29,'R':25,'E':30}

def initiative(seed):
 rec={k:{'dice':list(strict.old.dice(seed,f'R224-INIT-{k}',4,6)),'bonus':b} for k,b in B.items()}
 for k,x in rec.items():x['total']=sum(x['dice'])+x['bonus']
 if len({x['total'] for x in rec.values()})<3:raise ValueError('BLOCKED_INIT_TIE_PRECOMMIT')
 return rec,sorted(rec,key=lambda k:-rec[k]['total'])

def run(seed,arm):
 db=ROOT/'evidence/db'/f'R224_HOLDCOMP_{arm}_S{seed}.sqlite';q=ROOT/'evidence/quarantine'/db.name
 if db.exists() or q.exists():raise FileExistsError('R224_RUN_ID_COLLISION')
 rec,order=initiative(seed);src=strict if arm=='STRICT_HOLD' else floor
 src.init(db,seed,'PROTECTIVE','TEAM_A')
 st,_,rev=j.load(db);assert rev==0
 st['actors']['E']['position']='(0, 4)';st['order']=order;st['active']=order[0];st['scene']=f'R224-{seed}-{arm}'
 st['r222']={'prereg_sha256':PH,'arm':'INIT_A','mode':'ROUND','rolls':rec,'order':order,'E_position':'(0, 4)','guard_policy':'VAROK_NO_GUARD_R1'}
 st['r224']={'prereg_sha256':PH,'arm':arm,'policy':'HOLD' if arm=='STRICT_HOLD' else 'FLOOR_MASTER_TENTATIVE_TEST','source':'USER_MESTRE_UNCERTAIN_2026-10-21','world_canon':False}
 con=j.connect(str(db));head=j.sha({'seed':seed,'pre':PH,'receipts':rec,'order':order,'arm':arm})
 with con:
  for k,v in [('state',j.canonical(st)),('scene',st['scene']),('genesis',head),('head',head)]:con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 con.close()
 failed=None
 for i in range(12):
  st,_,_=j.load(db)
  if st['phase']!='ACTIVE':break
  try:j.event_commit(str(db),f'LAB-CMD-R216-R224-{seed}-{arm}-{i+1}','R216_INTEGRATED_TURN',{'seed':seed,'pre':src.PH,'actor':st['active']},src.turn)
  except Exception as e:failed={'class':type(e).__name__,'reason':str(e),'turn_attempt':i+1};break
 if failed:
  # never auto-replay UNKNOWN. Move entire brand-new sqlite to quarantine with pending metadata intact.
  db.rename(q);path=q
 else:path=db
 # Read frozen state by read-only sqlite, do not call j.load() on pending.
 con=sqlite3.connect(f'file:{path}?mode=ro&immutable=1',uri=True)
 try:
  m=dict(con.execute('select key,value from meta'));state=json.loads(m['state']);pending=con.execute('select count(*) from pending').fetchone()[0]
 finally:con.close()
 if failed and pending!=1:raise AssertionError('EXPECTED_PENDING_INTENT_NOT_PRESERVED')
 if not failed and pending:raise AssertionError('UNEXPECTED_PENDING')
 return {'seed':seed,'arm':arm,'path':path.name,'commits':int(m['revision']),'terminal':state['phase'] if not failed else None,'unknown_intent':bool(pending),'failure':failed,
 'HP':{k:x['hp'] for k,x in state['actors'].items()},'PA':{k:x['pa'] for k,x in state['actors'].items()},'turn_count_committed':state['turn'],'order':order,'initiative':rec,'events':len(state['native_events'])}

def main():
 log=[];block=[]
 for seed in P['seeds']:
  for arm in P['arms']:
   try:log.append(run(seed,arm))
   except ValueError as e:block.append({'seed':seed,'arm':arm,'reason':str(e)})
 pair=[]
 for seed in P['seeds']:
  v=[x for x in log if x['seed']==seed]
  if len(v)<2:continue
  s=next(x for x in v if x['arm']=='STRICT_HOLD');f=next(x for x in v if x['arm']=='TENTATIVE_FLOOR')
  pair.append({'seed':seed,'strict_phase':s['terminal'] or 'UNKNOWN_EFFECT','floor_phase':f['terminal'] or 'UNKNOWN_EFFECT',
   'strict_commits':s['commits'],'floor_commits':f['commits'],'strict_unknown_intent':s['unknown_intent'],
   'strict_interrupted':s['failure'] is not None,'floor_legal_censored':f['terminal']=='CENSORED_HORIZON'})
 obj={'prereg_sha256':PH,'attempts':len(P['seeds'])*2,'runs':log,'blocked_before_db':block,'paired_units':pair,'historical_replays':0}
 (ROOT/'evidence/reports/R224_STRICT_VS_FLOOR_EXECUTIONS.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'attempts':obj['attempts'],'runs_with_db':len(log),'blocked_pre_db':len(block),'pairs':len(pair),
  'strict_unknown':sum(x['strict_interrupted'] for x in pair),'floor_censures':sum(x['floor_legal_censored'] for x in pair),
  'strict_normal_censures':sum(x['strict_phase']=='CENSORED_HORIZON' for x in pair),'committed':sum(x['commits'] for x in log)},indent=2))
if __name__=='__main__':main()
