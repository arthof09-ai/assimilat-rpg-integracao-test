"""Engine-free independent READ-ONLY audit of physical initiative-permutation R217.
Read each native R18 journal, source R216 mech-audit and frozen pre-reg, then
assert true chronological turn order; compare actor-identical outcomes, not labels.
"""
from pathlib import Path
import hashlib,json,sqlite3
from collections import Counter
from r216_independent_readonly_audit import audit_one
BASE=Path(__file__).resolve().parents[1]

def ck(b,s):
 if not b:raise AssertionError(s)
def read(p):
 c=sqlite3.connect(f'file:{p}?mode=ro&immutable=1',uri=True)
 try:
  m=dict(c.execute('SELECT key,value FROM meta'));st=json.loads(m['state'])
  events=[]
  for (s,) in c.execute('SELECT row_json FROM events ORDER BY seq'):
   row=json.loads(s);events.extend(row['detail']['events_added'])
  return st,events,m
 finally:c.close()

def audit_single_order(p, expected_prereg_sha):
 mechanical=audit_one(p)
 st,ev,m=read(p)
 order=st['r217']['order']
 ck(order==st['order'],'DECLARED_ORDER_DIFFERS_FROM_CURRENT_STATE')
 ck(order in (['V','R','E'],['R','V','E']),'UNSUPPORTED_ORDER')
 starts=[e['by'] for e in ev if e['action']=='turn_start']
 ck(starts==order*4,'INITIATIVE_TURN_CHRONOLOGY')
 ck(st['r216']['turns']=={'V':4,'R':4,'E':4},'INITIATIVE_RESOURCE_TURN_ALLOCATION')
 ck(st['r217']['preregister_sha256']==expected_prereg_sha,'FROZEN_INITIATIVE_PREREG')
 return mechanical

def verify(root=BASE):
 prereg=root/'sources/R217_ORDER_PREFLIGHT_PREREG.json';pr=json.loads(prereg.read_text());ph=hashlib.sha256(prereg.read_bytes()).hexdigest()
 allresults=[];bad=[];pairs=[];counts=Counter()
 p=(root/'evidence/db');q=(root/'evidence/quarantine')
 accepted=sorted(p.glob('R217_ORDER_*.sqlite'));blocked=sorted(q.glob('R217_ORDER_*.sqlite'))
 ck(len(accepted)==10 and len(blocked)==14,'DENOMINATORS_10_AND_14')
 for f in accepted:
  mechanical=audit_single_order(f,ph)
  st,ev,m=read(f)
  order=st['r217']['order'];seed=st['seed'];arm='V_FIRST' if order==['V','R','E'] else 'R_FIRST' if order==['R','V','E'] else None
  ck(arm is not None and f.name==f'R217_ORDER_{arm}_S{seed}.sqlite','ORDER_ID_CORRESPONDENCE')
  ck(st['r217']['preregister_sha256']==ph,'PRE_REG_HASH')
  ck(st['r217']['previous_R216_SHA256']=='2b2f3a398e6ed9886133ae531e8f603caa4e4ee509317d640c947a38b528af0e','UPSTREAM_SNAPSHOT_ID')
  starts=[e['by'] for e in ev if e['action']=='turn_start'];ends=[e['by'] for e in ev if e['action']=='turn_end']
  ck(starts==order*4 and ends==order*4,'NATIVE_TURN_CHRONOLOGY')
  ck(st['order']==order and st['phase']=='CENSORED_HORIZON','SCHEDULER_ORDER_PHASE')
  ck(st['r216']['turns']=={'V':4,'R':4,'E':4},'FAIR_ACTION_ALLOCATION')
  ck(mechanical['commits']==12 and mechanical['phase']=='CENSORED_HORIZON','NATIVE_MECH_GATE')
  ck(m['scene']==st['scene'] and st['synthetic'] is True,'SCENE_STATE_SOURCE')
  counts['commits']+=mechanical['commits'];counts['events']+=mechanical['events'];counts['attacks']+=mechanical['physical_attacks'];counts['heals']+=mechanical['heals'];counts['spells']+=mechanical['spells']
  allresults.append({'seed':seed,'order':arm,'native_events':mechanical['events'],'HP':mechanical['HP'],'PA':mechanical['PA'],'attacks':mechanical['physical_attacks'],'opportunity_attacks':mechanical['opportunities'],'turn_order':starts})
 for f in blocked:
  st,ev,m=read(f)
  # Zero-effect preflight or genuine UNKNOWN-ODD intent; no replays nor success claim.
  c=sqlite3.connect(f'file:{f}?mode=ro&immutable=1',uri=True)
  try:pend=c.execute('SELECT count(*) FROM pending').fetchone()[0];rev=int(m['revision'])
  finally:c.close()
  if '217810' in f.name:ck(rev==0 and pend==0,'INITIAL_BAD_SCENE_QUARANTINE')
  elif '21782003' in f.name:ck(rev>0 and pend==1,'UNKNOWN_EFFECT_QUARANTINE')
  else:raise AssertionError('UNKNOWN_QUARANTINE_CLASS')
  bad.append({'name':f.name,'revision':rev,'pending':pend,'class':'INITIAL_PREFLIGHT_REJECT' if '217810' in f.name else 'UNKNOWN_ODD'})
 for seed in pr['seeds']:
  cases=[r for r in allresults if r['seed']==seed]
  if not cases:ck(seed==21782003,'UNEXPECTED_MISSING_PAIR');continue
  ck(len(cases)==2 and {r['order'] for r in cases}=={'V_FIRST','R_FIRST'},'PAIR_INCOMPLETE')
  a,b=cases
  ck(a['HP']==b['HP'] and a['PA']==b['PA'],'IDENTITY_OUTCOMES_DIFFER_FROZEN_FIXTURE')
  ck(a['turn_order']!=b['turn_order'],'DID_NOT_ACTUALLY_SWAP_ORDER')
  pairs.append({'seed':seed,'HP':a['HP'],'PA':a['PA'],'diff_HP':{k:0 for k in a['HP']},'chronology_is_different':True})
 ck(len(pairs)==5 and counts['commits']==120,'PAIRS_OR_COMMITS')
 return {'status':'PASS_R217_ENGINE_INDEPENDENT_INITIATIVE_ORDER_TEST','scope':'TEST_SOURCE_CONDITIONAL_NOT_UNIVERSAL_FAIRNESS','pairs':pairs,'valid_runs':len(accepted),'independent_seed_pairs':len(pairs),'commits':counts['commits'],'events':counts['events'],'attacks':counts['attacks'],'heals':counts['heals'],'spells':counts['spells'],'KO':0,'censored':len(accepted),'quarantine':len(blocked),'quarantine_classes':Counter(v['class'] for v in bad),'prior_historical_runs_reexecuted':0}
if __name__=='__main__':
 r=verify();(BASE/'evidence/reports/R217_INDEPENDENT_ORDER_AUDIT.json').write_text(json.dumps(r,indent=2,ensure_ascii=False))
 print(json.dumps({k:v for k,v in r.items() if k!='pairs'},indent=2,ensure_ascii=False))
