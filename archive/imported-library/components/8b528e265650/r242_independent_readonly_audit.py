"""Independent data-level exhaustive 3d6 ordered critical stress verifier; no motor import."""
import json,hashlib,itertools,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def req(v,t):
 if not v:raise AssertionError(t)
def audit(root=ROOT,write=True,mod=None):
 root=Path(root)
 P_bytes=(root/'sources/R242_PREREG.json').read_bytes();P=json.loads(P_bytes);p_sha=hashlib.sha256(P_bytes).hexdigest()
 beast_bytes=(root/'sources/R234_BEAST_FROZEN_EXCERPTS.json').read_bytes();b_sha=hashlib.sha256(beast_bytes).hexdigest()
 report=json.loads((root/'reports/R242_RUN_RAW.json').read_text()) if mod is None else copy.deepcopy(mod)
 req(report['prereg_sha']==p_sha and report['source_beast_sha']==b_sha,'FROZEN_ORACLE_SHA')
 req(P['official_cells']==0 and P['certified_terminals']==0 and report['official_cells']==0 and report['terminal_contracts']==0 and report['source_status']=='PRECREATE-NONP4','NO_OFFICIAL_PROMOTION')
 details=report['details'];req(len(details)==432 and report['total_probes']==432,'FULL_432_DENOMINATOR')
 counts={'75':{'rejected':0,'positive':0,'miss':0,'hit':0,'hp_total':0},'1000':{'rejected':0,'positive':0,'miss':0,'hit':0,'hp_total':0}}
 seen=set()
 for x in details:
  t=tuple(x['tape']);k=x['rd'];req(k in [75,1000] and len(t)==3 and all(type(v)==int and 1<=v<=6 for v in t),'LEGAL_CRIT_TAPE')
  req((k,t) not in seen,'DUPLICATE_TAPE');seen.add((k,t))
  neg=t[:2]==(1,1) and t[2] in [1,2]
  pos=t[:2]==(6,6) and t[2] in [5,6]
  q=counts[str(k)]
  if neg:
   req(x['status']=='REJECTED' and 'critical failure consequence unresolved' in x['reason'] and x['pre_effect_unchanged'] is True and x['events_after']==1,'NEG_FAILS_BEFORE_EFFECT')
   q['rejected']+=1
  else:
   req(x['status']=='ADMITTED' and x['attacker_standard_after']==0 and x['events_after']==2,'ADMITTED_ATOMIC_STANDARD')
   raw=220 if pos else 0;rd=k if pos else 0;hp=max(0,raw-rd)
   req(x['critical']==('POSITIVE' if pos else 'NONE') and x['hit']==pos and x['raw']==raw and x['rd_applied']==rd and x['hp_loss_actual']==hp,'ORDERED_CRIT_AND_RD')
   req(x['target_hp_after']==4315-hp,'TARGET_HP_CONSERVATION')
   q['positive']+=int(pos);q['hit']+=int(pos);q['miss']+=int(not pos);q['hp_total']+=hp
 req(seen=={(k,t) for k in (75,1000) for t in itertools.product(range(1,7),repeat=3)},'COMPLETE_TAPE_DOMAIN')
 req(counts==report['counts'],'AGGREGATE_REPORT_AGREEMENT')
 req(counts['75']=={'rejected':2,'positive':2,'miss':212,'hit':2,'hp_total':290},'RD75_COUNTS')
 req(counts['1000']=={'rejected':2,'positive':2,'miss':212,'hit':2,'hp_total':0},'RD1000_COUNTS')
 # Engine identity safety: verify precise original adapter bytes recovered from R237.
 v=(root/'runtime/native/vlab_effects_v08.py');req(v.exists() and hashlib.sha256(v.read_bytes()).hexdigest()=='9b42a9f6d6197f7a07ba900c955c046d4cad061a3d75cf1d6f923aaa6cb324a6','NATIVE_BASELINE_DRIFT')
 out={'gate':'PASS_R242_CRITICAL_SEQUENCE_LOCAL_INDEPENDENT_READONLY','total_ordered_cases':432,'actual_positive_auto_hit':4,
 'negative_fails_closed':4,'all_noncrit_misses':424,'RD75_HP_total':290,'RD1000_HP_total':0,'native_adapter_sha256':hashlib.sha256(v.read_bytes()).hexdigest(),
 'canonical_negative_critical_consequence':'UNRESOLVED_HOLD','official_cells':0,'terminal_contracts':0,'source_status':'PRECREATE-VZ-NONP4'}
 if write:(root/'reports/R242_INDEPENDENT_READONLY_AUDIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 return out
if __name__=='__main__':print(json.dumps(audit(),ensure_ascii=False,indent=2))
