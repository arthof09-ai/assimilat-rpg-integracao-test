"""Independent R219/R220 chronology+source RNG audit, engine-free; imports ONLY READ-ONLY
R216 mechanical auditors for respective scene initial states. No combat runner imports.
"""
from pathlib import Path
import hashlib,json,sqlite3,random,collections,re,sys
ROOT=Path(__file__).resolve().parents[1]

def ck(cond,msg):
 if not cond:raise AssertionError(msg)

def sqlread(p):
 c=sqlite3.connect(f'file:{p}?mode=ro&immutable=1',uri=True)
 try:
  meta=dict(c.execute('select key,value from meta'));st=json.loads(meta['state']);rows=[json.loads(r[0]) for r in c.execute('select row_json from events order by seq')];pending=c.execute('select count(*) from pending').fetchone()[0];return meta,st,rows,pending
 finally:c.close()

def initiative(seed,arm,actor,version):
 bonus={'V':29,'R':25,'E':30}[actor]
 h=hashlib.sha256(f'R215|{seed}|R{version}-INIT-{arm}-{actor}|4d6'.encode()).digest();g=random.Random(int.from_bytes(h,'big'));dice=[g.randint(1,6) for _ in range(4)]
 return {'dice':dice,'bonus':bonus,'total':sum(dice)+bonus}

def audit_one_special(p,version,prereg_sha,mechanic):
 match=re.fullmatch(rf'R{version}_(?:INJURED|GUARD_CHOICE)_(INIT_[AB])_S(\d{{8}})\.sqlite',p.name);ck(match,'WRONG_R219_R220_ID')
 arm,seed=match.group(1),int(match.group(2))
 native=mechanic(p)
 meta,st,rows,pending=sqlread(p);ck(pending==0,'VALID_HAS_PENDING')
 info=st['r'+version];ck(info['arm']==arm and info['prereg_sha256']==prereg_sha,'PRE_HASH_INVALID')
 rolls={a:initiative(seed,arm,a,version) for a in ('V','R','E')};ck(info['rolls']==rolls,'INITIATIVE_RNG_DRIFT')
 ck(len({r['total'] for r in rolls.values()})==3,'INIT_TIE_NOT_ALLOWED')
 order=sorted(rolls,key=lambda x:-rolls[x]['total']);ck(st['order']==info['order']==order,'NATIVE_ROLLED_ORDER_WRONG')
 events=[e for row in rows for e in row['detail']['events_added']];starts=[e['by'] for e in events if e['action']=='turn_start'];ends=[e['by'] for e in events if e['action']=='turn_end']
 ck(starts==ends==order*4 and st['r216']['turns']=={'V':4,'R':4,'E':4},'TURN_SCHEDULER_CHRONOLOGY')
 first=rows[0]['detail']['events_added'];ck(first[0]['action']=='turn_start' and first[1]['action']==f'R{version}_INITIATIVE_EFFECTIVE_ORDER','MISSING_INITIATIVE_FIRST_EVENT')
 ck(first[1]['roll_receipts']==rolls and first[1]['order']==order and first[1]['pre_hash']==prereg_sha,'INIT_FIRST_RECEIPT_DRIFT')
 if version=='219':
  ck(first[2]['action']=='R219_PREEXISTING_WOUND_FIXTURE' and first[2]['initial_hp']==614 and first[2]['precombat_wound']==120 and first[2]['no_simulated_prior_attack'],'INITIAL_WOUND_SOURCE_DRIFT')
  ck(info['starting_V_hp']==614 and info['start_V_max']==734,'INITIAL_WOUND_STORED_DRIFT')
 else:
  ck(first[2]['action']=='R220_POSITION_AND_GUARD_POLICY_FIXTURE' and first[2]['position_E']=='(0, 4)' and first[2]['V_precombat_hp']==734,'R220_FIXTURE_DECLARATION_DRIFT')
  ck(info['E_position']=='(0, 4)' and info['guard_policy']=='VAROK_NO_GUARD_R1','GUARD_POLICY_STATE_DRIFT')
  # Varok consciously declined reaction defense in first round; no fake use or PA debit allowed.
  active_round=0;counter=0
  for e in events:
   if e['action']=='turn_start':counter+=1;active_round=(counter-1)//3+1
   if e['action']=='R215_POST_RD_GUARD' and e['by']=='V':ck(active_round>1,'VAROK_DEFENSE_USED_DURING_PROTECTED_FIRST_ROUND')
   if e['action']=='PULSO_ESTABILIZACAO':ck(active_round>1,'ILLEGAL_FIRST_ROUND_PULSO_AT_DISTANCE_GT3')
 ck(native['commits']==12 and native['phase']=='CENSORED_HORIZON','INCOMPLETE_NATIVE_FIGHT')
 return {'arm':arm,'seed':seed,'order':order,'HP':native['HP'],'PA':native['PA'],'commits':native['commits'],'events':native['events'],'moves':native['moves'],'physical_attacks':native['physical_attacks'],'opportunities':native['opportunities'],'heals':native['heals'],'spells':native['spells'], 'E_decisions':[e['choice'] for e in events if e['action']=='R216_SUPPORT_OBSERVED_STATE'], 'physical_rng':{e['stream']:e for e in events if e['action']=='R215_OFFENSIVE_RNG'}}

def verify(root=ROOT,version='220'):
 code=root/'code';sys.path.insert(0,str(code))
 if version=='220':
  from r220_independent_mechanical_audit import audit_one as mechanic
  pre=root/'sources/R220_PREREG_BEFORE_NEW_COMBATS.json';f=root/'evidence/reports/R220_NONCOMMUTATIVE_EXECUTIONS.json';admitted_expected=33;blocked_expected=15;pending_expected=6;seeds_key='new_seeds'
 else:
  from r219_independent_mechanical_core_audit import audit_one as mechanic
  pre=root/'sources/R219_PREREG_BEFORE_NEW_COMBATS.json';f=root/'evidence/reports/R219_WOUNDED_ROLLED_RESULTS.json';admitted_expected=36;blocked_expected=12;pending_expected=5;seeds_key='seeds'
 prereg=json.loads(pre.read_text());ph=hashlib.sha256(pre.read_bytes()).hexdigest();report=json.loads(f.read_text())
 globstr=f'R{version}_*.sqlite';files=sorted((root/'evidence/db').glob(globstr));bad=sorted((root/'evidence/quarantine').glob(globstr))
 ck(len(files)==admitted_expected and len(report['admitted'])==admitted_expected,'ADMISSION_COUNT_WRONG')
 ck(len(report['blocked'])==blocked_expected and len(bad)==pending_expected,'BLOCK_DENOMINATOR_DRIFT')
 for p in bad:
  meta,st,rows,pending=sqlread(p);ck(pending==1 and int(meta['revision'])>=0 and st['phase']=='ACTIVE','UNKNOWN_QUARANTINE_CONTRACT')
 results=[audit_one_special(p,version,ph,mechanic) for p in files]
 source={(r['seed'],r['arm']):r for r in report['admitted']}
 for r in results:
  x=source[(r['seed'],r['arm'])];ck(r['HP']==x['HP'] and r['PA']==x['PA'] and r['order']==x['order'],'RESULT_REPORT_MISMATCH')
 by=collections.defaultdict(dict)
 for r in results:by[r['seed']][r['arm']]=r
 pairs=[]
 for seed in prereg[seeds_key]:
  if len(by[seed])!=2:continue
  a,b=by[seed]['INIT_A'],by[seed]['INIT_B']
  aligned=set(a['physical_rng']).intersection(b['physical_rng'])
  ck(all(a['physical_rng'][k]['attack_attempts']==b['physical_rng'][k]['attack_attempts'] and a['physical_rng'][k]['crit']==b['physical_rng'][k]['crit'] and a['physical_rng'][k]['damage_rolls']==b['physical_rng'][k]['damage_rolls'] for k in aligned),'PAIR_PHYSICAL_TAPE_DRIFT')
  pairs.append({'seed':seed,'order_A':a['order'],'order_B':b['order'],'order_changed':a['order']!=b['order'],'HPdiff':{k:a['HP'][k]-b['HP'][k] for k in a['HP']},'PAdiff':{k:a['PA'][k]-b['PA'][k] for k in a['PA']},'E_decisions_changed':a['E_decisions']!=b['E_decisions'],'identical_matching_physical_streams':len(aligned)})
 if version=='220':
  ck(len(pairs)==13 and sum(x['E_decisions_changed'] for x in pairs)==2 and sum(any(x['HPdiff'].values()) for x in pairs)==1,'R220_NONCOMMUTATIVE_RESULT_NOT_REPRODUCED')
  ck(next(x for x in pairs if x['seed']==22045003)['HPdiff']['R']==-34,'R220_DISCRIMINANT_SEED_BAD')
 else:ck(len(pairs)==16 and all(not any(x['HPdiff'].values()) for x in pairs),'R219_NEGATIVE_RESULT_NOT_REPRODUCED')
 cnt={k:sum(x[k] for x in results) for k in ('commits','events','moves','physical_attacks','opportunities','heals','spells')}
 return {'status':f'PASS_R{version}_INDEPENDENT_SOURCE_ROLLED_INITIATIVE_NATIVE_FIGHT','scope':'TEST_ONLY_PROPOSED_NPC_FROZEN_FIXTURE','attempted':len(prereg[seeds_key])*2,'admitted':len(results),'blocked':len(report['blocked']),'unknown_half_sqlite':len(bad),'complete_pairs':len(pairs),'order_changed_pairs':sum(x['order_changed'] for x in pairs),'E_decision_diff_pairs':sum(x['E_decisions_changed'] for x in pairs),'HP_difference_pairs':sum(any(x['HPdiff'].values()) for x in pairs),**cnt,'censures':len(results),'KO':0,'historical_replays':0,'pairs':pairs}

if __name__=='__main__':
 ver=sys.argv[1] if len(sys.argv)>1 else '220'
 result=verify(version=ver)
 (ROOT/'evidence/reports'/f'R{ver}_INDEPENDENT_CHRONOLOGY_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='pairs'},ensure_ascii=False,indent=2))
