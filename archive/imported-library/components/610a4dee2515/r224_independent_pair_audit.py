"""R224 independent SQL read-only paired audit. No battle engine or executor imports."""
from pathlib import Path
import hashlib,json,re,sqlite3,random,collections
from r222_independent_mechanical_audit import audit_one as old_audit
from r223_independent_mechanical_audit import audit_one as floor_audit
ROOT=Path(__file__).resolve().parents[1]
REGEX=re.compile(r'R224_HOLDCOMP_(STRICT_HOLD|TENTATIVE_FLOOR)_S(\d{8})\.sqlite')
B={'V':29,'R':25,'E':30}
def ck(flag,message):
 if not flag:raise AssertionError(message)
def dig(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def dice(seed,k):
 tag=f'R224-INIT-{k}';h=hashlib.sha256(f'R215|{seed}|{tag}|4d6'.encode()).digest();rng=random.Random(int.from_bytes(h,'big'));return [rng.randint(1,6) for _ in range(4)]
def state_db(p):
 c=sqlite3.connect(f'file:{p}?mode=ro&immutable=1',uri=True)
 try:
  m=dict(c.execute('select key,value from meta'));st=json.loads(m['state']);rows=[json.loads(a[0]) for a in c.execute('select row_json from events order by seq')];pending=list(c.execute('select cmd_id,base_head,kind,payload_json from pending'));return m,st,rows,pending
 finally:c.close()
def audit_one(path,ph):
 match=REGEX.fullmatch(path.name);ck(match,'RUN_ID_FORMAT');arm,seed=match.group(1),int(match.group(2))
 meta,st,rows,pending=state_db(path)
 ck(st['seed']==seed and st['r224']['prereg_sha256']==ph and st['r224']['arm']==arm,'R224_META_SOURCE')
 ck(st['r224']['world_canon'] is False,'CANON_UNAUTHORIZED')
 receipts={k:{'dice':dice(seed,k),'bonus':v,'total':sum(dice(seed,k))+v} for k,v in B.items()}
 ck(st['r222']['rolls']==receipts,'INIT_DICE_WRONG')
 ck(len({v['total'] for v in receipts.values()})==3,'INIT_TIE_SHOULD_HAVE_BLOCKED')
 order=sorted(B,key=lambda k:-receipts[k]['total']);ck(st['order']==st['r222']['order']==order,'INIT_ORDER')
 ck(len(rows)==int(meta['revision']),'REVISION_MISMATCH')
 c=sqlite3.connect(f'file:{path}?mode=ro&immutable=1',uri=True)
 try: receipts=list(c.execute('select row_sha,prev,before_sha,after_sha from events order by seq'))
 finally:c.close()
 ck(len(receipts)==len(rows),'ROW_RECEIPT_DENOMINATOR')
 for row,(rh,pr,bs,af) in zip(rows,receipts):
  ck(dig(row)==rh and row['prev']==pr and row['before_sha']==bs and row['after_sha']==af,'ROW_SHA_OR_COL_MISMATCH')
 prior=meta['genesis'];bef=None;all_events=[]
 for index,row in enumerate(rows,1):
  ck(row['seq']==index and row['prev']==prior,'HASH_CHAIN_SEQUENCE')
  ck(row['after_sha'] and row['before_sha'] and len(row['detail']['events_added'])>0,'STATE_RECEIPT')
  if bef is not None:ck(row['before_sha']==bef,'BEFORE_AFTER_CONTIGUITY')
  ck(row['cmd_id'].startswith(f'LAB-CMD-R216-R224-{seed}-{arm}-'),'WRONG_RUN_ID')
  prior=dig(row);bef=row['after_sha'];all_events+=row['detail']['events_added']
 ck(prior==meta['head'],'HEAD_ROW_MISMATCH')
 if rows:ck(rows[-1]['after_sha']==dig(st),'FINAL_STATE_SHA')
 ck(all_events==st['native_events'],'NATIVE_EVENT_CONTINUITY')
 for i,e in enumerate(all_events,1):ck(e['seq']==i,'EVENT_SEQUENCE')
 if arm=='STRICT_HOLD':
  ck(st['r224']['policy']=='HOLD','STRICT_POLICY_TAMPER')
  if pending:
   ck(len(pending)==1 and st['phase']=='ACTIVE','UNKNOWN_PENDING_SHAPE')
   ck(pending[0][0].startswith(f'LAB-CMD-R216-R224-{seed}-{arm}-'),'UNKNOWN_PENDING_NOT_THIS_RUN')
   ck(pending[0][1]==meta['head'] and pending[0][2]=='R216_INTEGRATED_TURN','UNKNOWN_PENDING_HEAD_OR_KIND')
   payload=json.loads(pending[0][3]);ck(payload['seed']==seed and payload['actor']==st['active'],'UNKNOWN_PENDING_PAYLOAD')
   ck(int(meta['revision'])<12,'UNKNOWN_PREMATURE_TERMINAL')
   return {'seed':seed,'arm':arm,'kind':'UNKNOWN_EFFECT','rows':rows,'events':all_events,'commits':len(rows),'pending':1,'state':st}
  else:
   old_audit(path)
 else:
  ck(st['r224']['policy']=='FLOOR_MASTER_TENTATIVE_TEST','FLOOR_POLICY_TAMPER')
  ck(not pending,'FLOOR_PENDING_NOT_ALLOWED');floor_audit(path)
 ck(st['phase']=='CENSORED_HORIZON' and len(rows)==12,'COMPLETE_BATTLE_EXPECTED')
 return {'seed':seed,'arm':arm,'kind':'CENSORED_HORIZON','rows':rows,'events':all_events,'commits':len(rows),'pending':0,'state':st}

def verify(root=ROOT):
 root=Path(root);pre=root/'sources/R224_PREREG_BEFORE_NEW_COMBATS.json';s=json.loads(pre.read_text());ph=hashlib.sha256(pre.read_bytes()).hexdigest()
 res=json.loads((root/'evidence/reports/R224_STRICT_VS_FLOOR_EXECUTIONS.json').read_text())
 files=sorted((root/'evidence/db').glob('R224_HOLDCOMP_*.sqlite'))+sorted((root/'evidence/quarantine').glob('R224_HOLDCOMP_*.sqlite'))
 ck(len(files)==40 and len(res['runs'])==40,'ROSTER_MISMATCH')
 ck(len(res['blocked_before_db'])==8,'PREFLIGHT_DENOMINATOR')
 x=[audit_one(p,ph) for p in files];by=collections.defaultdict(dict)
 for v in x:by[v['seed']][v['arm']]=v
 ck(len(by)==20 and all(len(v)==2 for v in by.values()),'PAIRED_VALID_SEEDS')
 truncated=[];odd=0;floor_meta=[]
 for seed,v in by.items():
  strict=v['STRICT_HOLD'];fl=v['TENTATIVE_FLOOR'];ck(strict['commits']<=fl['commits'],'STRICT_MORE_COMMITS_THAN_FLOOR')
  for i in range(strict['commits']):
   a=strict['rows'][i]['detail']['events_added'];b=fl['rows'][i]['detail']['events_added'];ck(a==b,'COMMON_PREFIX_DIVERGENCE')
  ck(strict['state']['r222']['rolls']==fl['state']['r222']['rolls'] and strict['state']['order']==fl['state']['order'],'SOURCE_INIT_DIFFERED')
  future=[e for e in fl['events'][len(strict['events']):] if e['action']=='R223_TENTATIVE_ROUNDING_EVIDENCE']
  if strict['kind']=='UNKNOWN_EFFECT':
   ck(len(future)>0,'UNKNOWN_NOT_ODD_EFFECT')
   truncated.append({'seed':seed,'committed_prefix':strict['commits'],'floor_odd_evidence':future[0]['rounded_down']})
  n=sum(e['action']=='spell' and e.get('r223_odd_half_policy')=='FLOOR_MASTER_TENTATIVE_TEST' for e in fl['events']);odd+=n
  floor_meta.append({'seed':seed,'strict':strict['kind'],'floor':fl['kind'],'prefix_commits':strict['commits'],'floor_odd_count':n})
 cnt={'attempts':48,'precommit_blocks':8,'paired_seed_units':20,'strict_unknown_intents':len(truncated),'floor_censures':sum(v['TENTATIVE_FLOOR']['kind']=='CENSORED_HORIZON' for v in by.values()),'strict_censures':sum(v['STRICT_HOLD']['kind']=='CENSORED_HORIZON' for v in by.values()),'floor_odd_half_spells':odd,'valid_terminal_sqlite':sum(v['kind']=='CENSORED_HORIZON' for v in x),'unknown_quarantine_sqlite':sum(v['kind']=='UNKNOWN_EFFECT' for v in x),'commits':sum(v['commits'] for v in x),'events':sum(len(v['events']) for v in x),'historical_replays':0}
 ck(cnt['strict_unknown_intents']==2 and cnt['floor_censures']==20 and cnt['valid_terminal_sqlite']==38,'EXPECTED_COHORT_OUTCOME')
 return {'status':'PASS_R224_INDEPENDENT_SQLITE_STRICT_VS_FLOOR_SOURCE_CENSURE','metrics':cnt,'interrupted_pairs':truncated,'pairs':floor_meta}
if __name__=='__main__':
 r=verify();(ROOT/'evidence/reports/R224_INDEPENDENT_PAIR_AUDIT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'status':r['status'],'metrics':r['metrics'],'interrupted_pairs':r['interrupted_pairs']},ensure_ascii=False,indent=2))
