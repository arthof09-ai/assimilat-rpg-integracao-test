"""R217 add-only scheduler initiative-permutation test. Source/engine: R216 native R18 unchanged.
Two declared ON5 initiative orders, same actors and TEST fixture, NEW seeds only.
No R216 historical runners nor historical SQLite are invoked.
"""
from pathlib import Path
import sys,sqlite3,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'code'),str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import r216_dynamic_multi_actor as src
import vlab_r18_interactive as j
PR=json.loads((ROOT/'sources/R217_ORDER_PREFLIGHT_PREREG.json').read_text())
PRE_SHA=hashlib.sha256((ROOT/'sources/R217_ORDER_PREFLIGHT_PREREG.json').read_bytes()).hexdigest()

def run(seed,ordern):
 order=['V','R','E'] if ordern=='V_FIRST' else ['R','V','E']
 db=ROOT/'evidence/db'/f'R217_ORDER_{ordern}_S{seed}.sqlite'
 if db.exists():raise FileExistsError('NO_REUSE_R217_RUN_ID:'+str(db))
 src.init(db,seed,'PROTECTIVE','TEAM_A') # initialize a new TEST bank, never historical
 # BEFORE first commit customize the declared combat-order source/initial state and genesis.
 st,_,rev=j.load(db)
 assert rev==0 and st['turn']==0 and not st['native_events']
 st['order']=order;st['active']=order[0];st['scene']=f'R217-SCHEDULER-INITIATIVE-{seed}-{ordern}'
 st['r217']={'order':order,'preregister_sha256':PRE_SHA,'initiative_source':'TEST_ON5_COMPARATOR_ORDER_FROZEN_NOT_GAME_INITIATIVE_RULE','previous_R216_SHA256':'2b2f3a398e6ed9886133ae531e8f603caa4e4ee509317d640c947a38b528af0e'}
 head=j.sha({'seed':seed,'r217_prereg':PRE_SHA,'order':order,'original_R216_pre_hash':src.PH})
 con=j.connect(str(db))
 with con:
  for k,v in [('state',j.canonical(st)),('genesis',head),('head',head),('scene',f'R217-SCHEDULER-INITIATIVE-{seed}-{ordern}')]:con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 con.close()
 for i in range(12):
  state,_,_=j.load(db)
  if state['phase']!='ACTIVE':break
  j.event_commit(str(db),f'LAB-CMD-R216-R217-{seed}-{ordern}-{i+1}','R216_INTEGRATED_TURN',{'seed':seed,'pre':src.PH,'actor':state['active']},src.turn)
 st,head,rev=j.load(db)
 return {'seed':seed,'order':ordern,'db':db.name,'commits':rev,'status':st['phase'],'actor_turn_order':[e['by'] for e in st['native_events'] if e['action']=='turn_start'],'HP':{k:a['hp'] for k,a in st['actors'].items()},'PA':{k:a['pa'] for k,a in st['actors'].items()},'events':len(st['native_events'])}

if __name__=='__main__':
 ok=[];blocked=[]
 for seed in PR['seeds']:
  for order in PR['arms']:
   try:ok.append(run(seed,order))
   except Exception as e:blocked.append({'seed':seed,'order':order,'error':repr(e),'bank':f'R217_ORDER_{order}_S{seed}.sqlite'})
 res={'new_results':ok,'blocked':blocked,'historical_reexecutions':0,'source_admissibility':'TEST_CONDITIONAL','initiative_order':'declared experimental comparator, NOT canonical roll-based initiative'}
 (ROOT/'evidence/reports/R217_INITIATIVE_ORDER_EXECUTIONS.json').write_text(json.dumps(res,indent=2,ensure_ascii=False))
 print(json.dumps({'admitted':len(ok),'blocked':len(blocked),'commits':sum(x['commits'] for x in ok),'valid_paired_seeds':[s for s in PR['seeds'] if sum(x['seed']==s for x in ok)==2]},indent=2))
