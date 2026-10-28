"""Independent R218 READ-ONLY auditor. No simulation/engine imports. Verifies source-rolled
initiative RNG, native scheduler chronology, R18+R216 mechanical causal journal, quarantines
and paired experimental denominators, including the negative outcome result.
"""
from pathlib import Path
import random,hashlib,json,sqlite3,re,collections
from r216_independent_readonly_audit import audit_one
ROOT=Path(__file__).resolve().parents[1]
BONUS={'V':29,'R':25,'E':30}
NAME=re.compile(r'^R218_ROLLED_(INIT_A|INIT_B)_S(\d{8})\.sqlite$')

def need(ok,why):
 if not ok:raise AssertionError(why)

def read(p):
 c=sqlite3.connect(f'file:{p}?mode=ro&immutable=1',uri=True)
 try:
  m=dict(c.execute('select key,value from meta'))
  st=json.loads(m['state'])
  seq=[json.loads(r[0]) for r in c.execute('select row_json from events order by seq')]
  return m,st,seq,c.execute('select count(*) from pending').fetchone()[0]
 finally:c.close()

def dice(seed,arm,who):
 text=f'R215|{seed}|R218-INIT-{arm}-{who}|4d6'
 h=hashlib.sha256(text.encode()).digest()
 rng=random.Random(int.from_bytes(h,'big'))
 return [rng.randint(1,6) for _ in range(4)]

def audit_one_rolled(p,ph,fixture_identity=None):
 if fixture_identity is None:
  q=NAME.match(p.name);need(q,'R218_UNKNOWN_RUN_ID')
  arm,seed=q.group(1),int(q.group(2))
 else:
  arm,seed=fixture_identity
  need(arm in ('INIT_A','INIT_B') and isinstance(seed,int),'R218_ADVERSARIAL_IDENTITY_INVALID')
 mechanics=audit_one(p)
 m,st,rows,pending=read(p)
 need(pending==0,'R218_PENDING_IN_ADMITTED')
 need(st['seed']==seed,'R218_SEED_MISMATCH')
 r=st['r218'];need(r['arm']==arm and r['prereg_sha256']==ph,'R218_PRE_HASH_MISMATCH')
 expected={k:{'dice':dice(seed,arm,k),'bonus':BONUS[k],'total':sum(dice(seed,arm,k))+BONUS[k]} for k in BONUS}
 need(r['rolls']==expected,'R218_INITIATIVE_PRF_FORGED')
 totals=[x['total'] for x in expected.values()];need(len(set(totals))==3,'R218_UNRESOLVED_INITIATIVE_TIE')
 order=sorted(BONUS,key=lambda k:-expected[k]['total'])
 need(st['order']==r['order']==order,'R218_WRONG_SCHEDULER_ORDER')
 ev=[e for row in rows for e in row['detail']['events_added']]
 starts=[e['by'] for e in ev if e['action']=='turn_start'];ends=[e['by'] for e in ev if e['action']=='turn_end']
 need(starts==order*4 and ends==order*4,'R218_TURN_CHRONOLOGY')
 need(st['r216']['turns']=={'V':4,'R':4,'E':4},'R218_BAD_TURN_ALLOCATION')
 first=rows[0]['detail']['events_added']
 need(first[0]['action']=='turn_start' and first[1]['action']=='R218_INITIATIVE_EFFECTIVE_ORDER','R218_MISSING_EFFECTIVE_ORDER_EVENT')
 i=first[1]
 need(i['roll_receipts']==expected and i['order']==order and i['branch']==arm and i['by']==order[0] and i['pre_hash']==ph,'R218_ROLL_RECEIPT_NOT_PRE_ACTION')
 need(sum(e['action']=='R218_INITIATIVE_EFFECTIVE_ORDER' for e in ev)==1,'R218_INITIATIVE_EVENT_MULTIPLICITY')
 need(mechanics['commits']==12 and st['phase']=='CENSORED_HORIZON','R218_INCOMPLETE_COMBAT')
 return {'seed':seed,'arm':arm,'initiative_order':order,'HP':mechanics['HP'],'PA':mechanics['PA'], 'events':mechanics['events'],'commits':mechanics['commits'],'moves':mechanics['moves'],'physical_attacks':mechanics['physical_attacks'],'aoo':mechanics['opportunities'],'heals':mechanics['heals'],'spells':mechanics['spells'],'phase':mechanics['phase']}

def verify(root=ROOT):
 prep=root/'sources/R218_PREREG_BEFORE_NEW_COMBATS.json'
 pre=json.loads(prep.read_text());ph=hashlib.sha256(prep.read_bytes()).hexdigest()
 accepted=sorted((root/'evidence/db').glob('R218_ROLLED_*.sqlite'))
 blocked=sorted((root/'evidence/quarantine').glob('R218_ROLLED_*.sqlite'))
 log=json.loads((root/'evidence/reports/R218_INITIATIVE_RUNS.json').read_text())
 need(len(accepted)==33 and len(blocked)==6 and len(log['blocked'])==15,'R218_DENOMINATOR_CONFLICT')
 need(len(pre['seeds'])==24 and len(pre['arms'])==2,'R218_PREREG_DENOMINATOR')
 results=[audit_one_rolled(f,ph) for f in accepted]
 for f in blocked:
  m,st,rows,pend=read(f)
  need(pend==1 and int(m['revision'])>=1,'R218_UNKNOWN_HALF_QUARANTINE_NO_PENDING')
  need(st['phase']=='ACTIVE','R218_QUARANTINE_INVALID_STATE')
  need(f.name not in [x.name for x in accepted],'R218_QUARANTINE_ID_COLLISION')
 counts=collections.Counter(x['reason'] for x in log['blocked'])
 need(counts=={'BLOCKED_TIE_PRECOMMIT':9,'UNKNOWN_EFFECT_PENDENTE: UNKNOWN_HALF_ODD_ROUNDING_SOURCE_HOLD':6},'R218_QUARANTINE_CLASS_DRIFT')
 need(len(results)==len(log['results']) and {x['arm']+str(x['seed']) for x in results}=={x['arm']+str(x['seed']) for x in log['results']},'R218_RESULT_ROSTER_MISMATCH')
 for r in log['results']:
  x=next(x for x in results if x['seed']==r['seed'] and x['arm']==r['arm'])
  need(x['HP']==r['HP'] and x['PA']==r['PA'] and x['initiative_order']==r['order'],'R218_LOG_RESULT_DRIFT')
 by=collections.defaultdict(dict)
 for x in results:by[x['seed']][x['arm']]=x
 pairs=[]
 for seed,arms in sorted(by.items()):
  if len(arms)!=2:continue
  a,b=arms['INIT_A'],arms['INIT_B']
  pairs.append({'seed':seed,'order_A':a['initiative_order'],'order_B':b['initiative_order'],'order_changed':a['initiative_order']!=b['initiative_order'], 'terminal_HP_different':a['HP']!=b['HP'], 'terminal_PA_different':a['PA']!=b['PA'], 'HP_A':a['HP'],'HP_B':b['HP']})
 need(len(pairs)==13,'R218_INDEPENDENT_PAIRS_DENOMINATOR')
 totals={field:sum(x[field] for x in results) for field in ('events','commits','moves','physical_attacks','aoo','heals','spells')}
 need(totals=={'events':2452,'commits':396,'moves':99,'physical_attacks':297,'aoo':33,'heals':43,'spells':132},'R218_NATIVE_TOTALS_CONFLICT')
 changed=sum(p['order_changed'] for p in pairs)
 need(changed>0,'R218_NO_ACTUAL_ORDER_PERMUTATION')
 return {'status':'PASS_R218_INDEPENDENT_NATIVE_ROLLED_INITIATIVE_SOURCE_GATED','scope':'TEST_PROPOSED_NPCS_TIES_BLOCKED_NO_CANONIC_FAIRNESS', 'attempted_arms':48,'admitted':len(results),'blocked':len(log['blocked']),'blocked_ties_precommit':9,'blocked_half_odd_unknown':6,'unknown_pending_sqlite':len(blocked),'paired_independent_seeds':len(pairs),'pairs_order_changed':changed,'pairs_terminal_HP_different':sum(p['terminal_HP_different'] for p in pairs),'pairs_terminal_PA_different':sum(p['terminal_PA_different'] for p in pairs),**totals,'censures':len(results),'KO':0,'historical_replays':0,'pairs':pairs}

if __name__=='__main__':
 x=verify()
 (ROOT/'evidence/reports/R218_INDEPENDENT_ROLLED_AUDIT.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in x.items() if k!='pairs'},indent=2,ensure_ascii=False))
