"""R218 source-rolled initiative, native R18, minimal R216 compatibility adapter, never R217 replay.
Each arm uses independent INIT_A/B initiative RNG; combat RNG remains R216 actor/action/seed-bound.
"""
from pathlib import Path
import sys,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'code'),str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import r218_dynamic_multi_actor_r216_addonly as src
import vlab_r18_interactive as j
PRB=(ROOT/'sources/R218_PREREG_BEFORE_NEW_COMBATS.json').read_bytes();PR=json.loads(PRB);PH=hashlib.sha256(PRB).hexdigest()
INIT_BONUS={'V':29,'R':25,'E':30}

def rolled(seed,arm):
 rr={}
 for who in ('V','R','E'):
  die=src.old.dice(seed,f'R218-INIT-{arm}-{who}',4,6)
  rr[who]={'dice':list(die),'bonus':INIT_BONUS[who],'total':sum(die)+INIT_BONUS[who]}
 if len(set(x['total'] for x in rr.values()))<3:raise ValueError('BLOCKED_TIE_PRECOMMIT')
 return rr,sorted(rr,key=lambda k:-rr[k]['total'])

def run(seed,arm):
 db=ROOT/'evidence/db'/f'R218_ROLLED_{arm}_S{seed}.sqlite'
 quarantine=ROOT/'evidence/quarantine'/db.name
 if db.exists() or quarantine.exists():raise FileExistsError('R218_ID_CONSUMED')
 receipts,order=rolled(seed,arm)
 src.init(db,seed,'PROTECTIVE','TEAM_A')
 st,_,rev=j.load(db);assert rev==0 and not st['native_events']
 st['order']=order;st['active']=order[0]
 st['scene']=f'R218-SOURCE-ROLLED-INIT-{seed}-{arm}'
 st['r218']={'prereg_sha256':PH,'arm':arm,'rolls':receipts,'order':order,'confidence':'NOTION_SOURCE_ROLLED_ON5_TIE_PRECOMMIT_BLOCK'}
 con=j.connect(str(db));head=j.sha({'seed':seed,'R218_PREREG':PH,'initiative':receipts,'order':order,'arm':arm,'native_R216_PH':src.PH})
 with con:
  for k,v in [('state',j.canonical(st)),('scene',st['scene']),('genesis',head),('head',head)]:con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 con.close()
 try:
  for i in range(12):
   st,_,_=j.load(db)
   if st['phase']!='ACTIVE':break
   j.event_commit(str(db),f'LAB-CMD-R216-R218-{seed}-{arm}-{i+1}', 'R216_INTEGRATED_TURN', {'seed':seed,'pre':src.PH,'actor':st['active']},src.turn)
  st,head,rev=j.load(db)
  return {'seed':seed,'arm':arm,'db':db.name,'order':order,'initiatives':receipts,'revision':rev,'events':len(st['native_events']),'phase':st['phase'],'HP':{k:v['hp'] for k,v in st['actors'].items()},'PA':{k:v['pa'] for k,v in st['actors'].items()},'stats':st['r216']['stats']}
 except Exception:
  db.rename(quarantine)
  raise

def main():
 valid=[];blocked=[]
 for seed in PR['seeds']:
  for arm in PR['arms']:
   try:valid.append(run(seed,arm))
   except Exception as e:blocked.append({'seed':seed,'arm':arm,'class':type(e).__name__,'reason':str(e)})
 r={'results':valid,'blocked':blocked,'runs':len(valid),'unique_seeds_admitted':len({x['seed'] for x in valid}),'matched_seed_pairs':len([x for x in PR['seeds'] if len([v for v in valid if v['seed']==x])==2]),'historical_replays':0}
 (ROOT/'evidence/reports/R218_INITIATIVE_RUNS.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'admitted':len(valid),'blocked':len(blocked),'paired':r['matched_seed_pairs'],'phases':{p:sum(x['phase']==p for x in valid) for p in {x['phase'] for x in valid}}},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
