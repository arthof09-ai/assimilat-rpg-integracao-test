"""R222 pre-registered factorial: real initiative A/B x identical random bank assigned by ROUND/ABILITY.
Uses R216 source-native R18 event_commit, full combat and read-only later audits. No replay.
"""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'code'),str(ROOT/'runtime/native'),str(ROOT/'runtime/fusion_stage12')]
import r222_round_reducer as rd
import r222_ability_reducer as ability
import vlab_r18_interactive as j
PRE=(ROOT/'sources/R222_PREREG_BEFORE_NEW_COMBATS.json').read_bytes();P=json.loads(PRE);PH=hashlib.sha256(PRE).hexdigest();B={'V':29,'R':25,'E':30}

def source_init(seed,arm):
 tapes={k:rd.old.dice(seed,f'R222-INIT-{arm}-{k}',4,6) for k in B}
 receipt={k:{'dice':list(tapes[k]),'bonus':B[k],'total':sum(tapes[k])+B[k]} for k in B}
 if len({x['total'] for x in receipt.values()})<3:raise ValueError('BLOCKED_TIE_PRECOMMIT')
 return receipt,sorted(B,key=lambda k:-receipt[k]['total'])

def run(seed,arm,mode):
 path=ROOT/'evidence/db'/f'R222_FACTOR_{arm}_{mode}_S{seed}.sqlite';q=ROOT/'evidence/quarantine'/path.name
 if path.exists() or q.exists():raise FileExistsError('R222_ID_REUSE')
 receipt,order=source_init(seed,arm);src=rd if mode=='ROUND' else ability
 src.init(path,seed,'PROTECTIVE','TEAM_A')
 st,_,rev=j.load(path);assert rev==0
 st['actors']['E']['position']='(0, 4)';st['order']=order;st['active']=order[0];st['scene']=f'R222-{seed}-{arm}-{mode}'
 st['r222']={'prereg_sha256':PH,'arm':arm,'mode':mode,'rolls':receipt,'order':order,'E_position':'(0, 4)','guard_policy':'VAROK_NO_GUARD_R1'}
 con=j.connect(str(path));head=j.sha({'seed':seed,'initiative':receipt,'order':order,'arm':arm,'mode':mode,'pre':PH})
 with con:
  for k,v in [('state',j.canonical(st)),('scene',st['scene']),('genesis',head),('head',head)]:con.execute('UPDATE meta SET value=? WHERE key=?',(v,k))
 con.close()
 try:
  for i in range(12):
   st,_,_=j.load(path)
   if st['phase']!='ACTIVE':break
   j.event_commit(str(path),f'LAB-CMD-R216-R222-{seed}-{arm}-{mode}-{i+1}', 'R216_INTEGRATED_TURN',{'seed':seed,'pre':src.PH,'actor':st['active']},src.turn)
  st,head,rev=j.load(path)
  return {'seed':seed,'arm':arm,'mode':mode,'db':path.name,'order':order,'initiative_receipts':receipt,'commits':rev,'phase':st['phase'],'HP':{k:v['hp'] for k,v in st['actors'].items()},'PA':{k:v['pa'] for k,v in st['actors'].items()},'decisions':st['r216']['decisions'],'stats':st['r216']['stats'],'events':len(st['native_events'])}
 except Exception:path.rename(q);raise

def main():
 valid=[];bad=[]
 for seed in P['seeds']:
  for arm in P['arm_initiative']:
   for mode in P['arm_rng_mapping']:
    try:valid.append(run(seed,arm,mode))
    except Exception as e:bad.append({'seed':seed,'arm':arm,'mode':mode,'class':type(e).__name__,'reason':str(e)})
 full=[]
 for seed in P['seeds']:
  a=[x for x in valid if x['seed']==seed]
  if len(a)<4:continue
  by={(x['arm'],x['mode']):x for x in a}
  vround=by['INIT_A','ROUND'];vability=by['INIT_A','ABILITY'];bround=by['INIT_B','ROUND'];bability=by['INIT_B','ABILITY']
  full.append({'seed':seed,'orderA':vround['order'],'orderB':bround['order'],
   'dHP_initiative_ROUND':{k:vround['HP'][k]-bround['HP'][k] for k in vround['HP']},
   'dHP_initiative_ABILITY':{k:vability['HP'][k]-bability['HP'][k] for k in vability['HP']},
   'dHP_mapping_in_INIT_A':{k:vround['HP'][k]-vability['HP'][k] for k in vround['HP']},
   'dHP_mapping_in_INIT_B':{k:bround['HP'][k]-bability['HP'][k] for k in vround['HP']},
   'E_choices':{f'{x["arm"]}_{x["mode"]}':[z['chosen'] for z in x['decisions']] for x in a}})
 report={'admitted':valid,'blocked':bad,'complete_factorial_seeds':full,'historical_replays':0}
 (ROOT/'evidence/reports/R222_FACTORIAL_EXECUTIONS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'attempts':len(P['seeds'])*4,'admitted':len(valid),'blocked':len(bad),'complete_factorial_seeds':len(full),
 'initiave_diff_round':sum(any(z for z in x['dHP_initiative_ROUND'].values()) for x in full),
 'initiative_diff_ability':sum(any(z for z in x['dHP_initiative_ABILITY'].values()) for x in full),
 'rng_mapping_diff_A':sum(any(z for z in x['dHP_mapping_in_INIT_A'].values()) for x in full),
 'rng_mapping_diff_B':sum(any(z for z in x['dHP_mapping_in_INIT_B'].values()) for x in full)},indent=2))
if __name__=='__main__':main()
