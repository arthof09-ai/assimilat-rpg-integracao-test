import json,hashlib,pathlib,sys,concurrent.futures,sqlite3,time
BASE=pathlib.Path(__file__).parent
sys.path.insert(0,str(BASE/'work'/'fusion_stage12'))
import vlab_r27_scientific_baseline as v
RECEIPTS=BASE/'scientific_runs'/'receipts'

def check(case):
 a,b,seed=case;name=f'{a}__{b}__SEED_{seed}'
 j=RECEIPTS/(name+'.json');r=json.loads(j.read_text())
 db=(BASE/'scientific_runs'/'new_sessions_after_hold'/ (name+'.sqlite')) if r.get('separate_new_session_after_earlier_pending_hold') else (BASE/'scientific_runs'/'sqlite'/(name+'.sqlite'))
 bytesha=hashlib.sha256(db.read_bytes()).hexdigest()
 if bytesha!=r['sqlite_sha256']:return {'id':name,'status':'FAIL_SHA'}
 h=v.history(db)
 if (h['head'],h['revision'],h['state']['r21_control']['chain'])!=(r['head'],r['revision'],r['a1_chain']):
  return {'id':name,'status':'FAIL_CHAIN'}
 events=[e for e in h['events'] if e['detail']['action']=='ATTACK']
 if len(events)!=len(r['events']):return {'id':name,'status':'FAIL_COUNT'}
 for x,y in zip(events,r['events']):
  e=x['detail']['inner']['native']['effect'];p=x['detail']['inner']['preview']
  if (e['hit'],e['net'],e['before_hp'],e['after_hp'],p['critical_trigger'])!=(y['native_hit'],y['native_net'],y['before_hp'],y['after_hp'],y['critical']):
   return {'id':name,'status':'FAIL_EVENT'}
 return {'id':name,'status':'PASS','revision':r['revision'],'native_attacks':len(events),'a1':r['a1_events']}

if __name__=='__main__':
 cases=[(a,b,seed) for a in v.PROFILES for b in v.PROFILES for seed in v.SEEDS]
 started=time.monotonic();rows=[]
 with concurrent.futures.ProcessPoolExecutor(max_workers=4) as ex:
  for i,x in enumerate(ex.map(check,cases),1):
   rows.append(x)
   if i%40==0:print('PROGRESS',i,len(cases),round(time.monotonic()-started,1),flush=True)
 out={'schema':'R27_READBACK_320','total':len(rows),'pass':sum(x['status']=='PASS' for x in rows),
  'failures':[x for x in rows if x['status']!='PASS'],
  'attacks':sum(x['native_attacks'] for x in rows if x['status']=='PASS'),
  'A1':sum(x['a1'] for x in rows if x['status']=='PASS'),
  'audit_schema':'read history via R21 A1 + R18 SQLite and compare per-event native V081 receipts',
  'elapsed_sec':round(time.monotonic()-started,1)}
 (BASE/'scientific_report'/'R27_320_READBACK_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(out,ensure_ascii=False,indent=2),flush=True)
