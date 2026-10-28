#!/usr/bin/env python3
"""Parallel reproducible independent runs; each one creates unique SQLite and own audited receipts."""
import concurrent.futures,hashlib,json,sys,time,traceback,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'work'/'fusion_stage12'))
import vlab_r27_scientific_baseline as v
ROOT=Path(__file__).parent/'scientific_runs'
ROOT.mkdir(exist_ok=True)

def task(row):
 seed,left,right=row
 ident=('ORIGINAL_R26' if left is None else left+'__'+right)+'__SEED_'+str(seed)
 target=ROOT/'receipts'/f'{ident}.json';target.parent.mkdir(exist_ok=True)
 if target.exists():
  old=json.loads(target.read_text());return {'status':'CACHED','id':ident,'science_status':old['status']}
 try:
  out=v.run(ROOT/'sqlite',seed,left,right)
  target.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
  return {'status':'DONE','id':ident,'science_status':out['status'],'attacks':out['summary']['attacks'],'round':out['round_reached']}
 except Exception as e:
  target.with_suffix('.failure.json').write_text(json.dumps({'error':str(e),'traceback':traceback.format_exc()},indent=2))
  return {'status':'ERROR','id':ident,'error':str(e)}

def run(rows,jobs=4):
 t=time.monotonic();counts={};completed=0
 with concurrent.futures.ProcessPoolExecutor(max_workers=jobs) as pool:
  fs={pool.submit(task,x):x for x in rows}
  for f in concurrent.futures.as_completed(fs):
   r=f.result();completed+=1;counts[r['status']]=counts.get(r['status'],0)+1
   if r['status']=='ERROR' or completed%10==0 or completed==len(rows):
    print(json.dumps({'done':completed,'planned':len(rows),'elapsed_sec':round(time.monotonic()-t,1),'counts':counts,'last':r},ensure_ascii=False),flush=True)
 return counts
if __name__=='__main__':
 mode=sys.argv[1] if len(sys.argv)>1 else 'original'
 if mode=='original': rows=[(s,None,None) for s in v.r25.DEFAULT_SEEDS]
 elif mode=='pilot':rows=[(s,a,b) for a in v.PROFILES for b in v.PROFILES for s in v.SEEDS[:4]]
 elif mode=='matrix':rows=[(s,a,b) for a in v.PROFILES for b in v.PROFILES for s in v.SEEDS]
 else:raise ValueError('invalid run mode')
 print('START',mode,len(rows),flush=True)
 run(rows)
