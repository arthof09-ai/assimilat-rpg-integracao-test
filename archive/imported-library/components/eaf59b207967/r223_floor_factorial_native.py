"""R223: new source-gated TEST odd-half floor integrated native R18 combats. No historical replay."""
import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'code'),str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import r223_round_reducer as rd
import r223_ability_reducer as ability
import vlab_r18_interactive as j
PRE=(ROOT/'sources/R223_PREREG_BEFORE_NEW_COMBATS.json').read_bytes();P=json.loads(PRE);PH=hashlib.sha256(PRE).hexdigest();B={'V':29,'R':25,'E':30}

def source_init(seed,arm):
 tapes={k:rd.old.dice(seed,f'R223-INIT-{arm}-{k}',4,6) for k in B}
 rec={k:{'dice':list(tapes[k]),'bonus':B[k],'total':sum(tapes[k])+B[k]} for k in B}
 if len({x['total'] for x in rec.values()})<3:raise ValueError('BLOCKED_INITIATIVE_TIE_PRECOMMIT')
 return rec,sorted(B,key=lambda k:-rec[k]['total'])

def run(seed,arm,mode):
 path=ROOT/'evidence/db'/f'R223_ODD_FLOOR_{arm}_{mode}_S{seed}.sqlite';quarantine=ROOT/'evidence/quarantine'/path.name
 if path.exists() or quarantine.exists():raise FileExistsError('R223_RUN_ID_COLLISION')
 receipt,order=source_init(seed,arm);src=rd if mode=='ROUND' else ability
 src.init(path,seed,'PROTECTIVE','TEAM_A')
 st,_,rev=j.load(path);assert rev==0
 st['actors']['E']['position']='(0, 4)';st['order']=order;st['active']=order[0]
 st['scene']=f'R223-{seed}-{arm}-{mode}-FLOOR-TENTATIVE'
 st['r222']={'prereg_sha256':PH,'arm':arm,'mode':mode,'rolls':receipt,'order':order,'E_position':'(0, 4)','guard_policy':'VAROK_NO_GUARD_R1'}
 st['r223']={'prereg_sha256':PH,'policy':'FLOOR_MASTER_TENTATIVE_TEST','decision_status':'NON_CANON_MASTER_UNCERTAIN','source':'USER_MESTRE_2026-10-21','historical_replays':0}
 con=j.connect(str(path));head=j.sha({'seed':seed,'initiative':receipt,'order':order,'arm':arm,'mode':mode,'pre':PH,'r223_floor':'MASTER_TENTATIVE_TEST_ONLY'})
 with con:
  for k,v in [('state',j.canonical(st)),('scene',st['scene']),('genesis',head),('head',head)]:con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 con.close()
 try:
  for i in range(12):
   st,_,_=j.load(path)
   if st['phase']!='ACTIVE':break
   j.event_commit(str(path),f'LAB-CMD-R216-R223-{seed}-{arm}-{mode}-{i+1}','R216_INTEGRATED_TURN',{'seed':seed,'pre':src.PH,'actor':st['active']},src.turn)
  st,head,rev=j.load(path)
  ev=st['native_events'];odd=[e for e in ev if e.get('action')=='spell' and e.get('r223_odd_half_policy')=='FLOOR_MASTER_TENTATIVE_TEST']
  return {'seed':seed,'arm':arm,'mode':mode,'db':path.name,'order':order,'rolls':receipt,'commits':rev,'phase':st['phase'],'HP':{k:v['hp'] for k,v in st['actors'].items()},'PA':{k:v['pa'] for k,v in st['actors'].items()},'decisions':st['r216']['decisions'],'stats':st['r216']['stats'],'events':len(ev),'odd_half_floor_exercised':len(odd)}
 except Exception as e:
  if path.exists():path.rename(quarantine)
  raise

def main():
 valid=[];bad=[]
 for seed in P['seeds']:
  for arm in P['arm_initiative']:
   for mode in P['arm_rng_mapping']:
    try:valid.append(run(seed,arm,mode))
    except Exception as e:bad.append({'seed':seed,'arm':arm,'mode':mode,'class':type(e).__name__,'reason':str(e)})
 complete=[]
 for seed in P['seeds']:
  a=[x for x in valid if x['seed']==seed]
  if len(a)!=4:continue
  by={(x['arm'],x['mode']):x for x in a}
  vround=by['INIT_A','ROUND'];vability=by['INIT_A','ABILITY'];bround=by['INIT_B','ROUND'];bability=by['INIT_B','ABILITY']
  complete.append({'seed':seed,'orders':{'A':vround['order'],'B':bround['order']},
    'delta_hp_round':{k:vround['HP'][k]-bround['HP'][k] for k in vround['HP']},
    'delta_hp_ability':{k:vability['HP'][k]-bability['HP'][k] for k in vability['HP']},
    'odd_half_exercised':sum(x['odd_half_floor_exercised'] for x in a),
    'choices':{f'{x["arm"]}_{x["mode"]}':[v['chosen'] for v in x['decisions']] for x in a}})
 report={'prereg_sha256':PH,'admitted':valid,'blocked':bad,'complete_factorial_seeds':complete,'historical_replays':0}
 (ROOT/'evidence/reports/R223_FLOOR_EXECUTIONS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'attempts':len(P['seeds'])*4,'admitted':len(valid),'blocked':len(bad),'complete_factorial_seeds':len(complete),'odd_half_floor_spells':sum(x['odd_half_floor_exercised'] for x in valid),'commits':sum(x['commits'] for x in valid),'events':sum(x['events'] for x in valid)},indent=2))
if __name__=='__main__':main()
