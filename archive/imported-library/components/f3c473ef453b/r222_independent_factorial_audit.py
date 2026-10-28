"""Independent R222 2x2 factorial science audit. No battle engine/runner imports.
Verifies R18+R216 native mechanics; 4d6 source-rolled initiative; identical initiative between
RNG mapping arms; common PRF bank used by nth round vs nth ability; chronology; factual outcome.
"""
from pathlib import Path
import hashlib,json,random,sqlite3,collections,re
from r222_independent_mechanical_audit import audit_one
ROOT=Path(__file__).resolve().parents[1]
BONUS={'V':29,'R':25,'E':30}
REGEX=re.compile(r'^R222_FACTOR_(INIT_[AB])_(ROUND|ABILITY)_S(\d{8})\.sqlite$')

def ck(ok,message):
 if not ok:raise AssertionError(message)
def dbread(p):
 con=sqlite3.connect(f'file:{p}?mode=ro&immutable=1',uri=True)
 try:
  m=dict(con.execute('select key,value from meta'));st=json.loads(m['state']);rows=[json.loads(r[0]) for r in con.execute('select row_json from events order by seq')];pending=con.execute('select count(*) from pending').fetchone()[0];return m,st,rows,pending
 finally:con.close()
def dice(seed,tag,n,faces):
 h=hashlib.sha256(f'R215|{seed}|{tag}|{n}d{faces}'.encode()).digest()
 rng=random.Random(int.from_bytes(h,'big'));return [rng.randint(1,faces) for _ in range(n)]
def audit_fight(p,ph,known_identity=None):
 if known_identity is None:
  match=REGEX.fullmatch(p.name);ck(match,'R222_RUN_ID_UNRECOGNIZED');arm,mode,seed=match.group(1),match.group(2),int(match.group(3))
 else:arm,mode,seed=known_identity
 native=audit_one(p);m,st,rows,pending=dbread(p);ck(pending==0,'R222_VALID_HAS_PENDING')
 meta=st['r222'];ck(meta['mode']==mode and meta['arm']==arm and meta['prereg_sha256']==ph,'R222_PREREG_OR_MODE_MISMATCH')
 receipts={k:{'dice':dice(seed,f'R222-INIT-{arm}-{k}',4,6),'bonus':b,'total':sum(dice(seed,f'R222-INIT-{arm}-{k}',4,6))+b} for k,b in BONUS.items()}
 ck(meta['rolls']==receipts,'R222_INIT_PRF_FORGED')
 ck(len({x['total'] for x in receipts.values()})==3,'R222_INIT_TIE_NOT_ADMISSIBLE')
 order=sorted(receipts,key=lambda k:-receipts[k]['total']);ck(meta['order']==st['order']==order,'R222_TURN_ORDER_NOT_ROLLED')
 ev=[x for row in rows for x in row['detail']['events_added']]
 starts=[x['by'] for x in ev if x['action']=='turn_start'];ends=[x['by'] for x in ev if x['action']=='turn_end']
 ck(starts==ends==order*4 and st['r216']['turns']=={'V':4,'R':4,'E':4},'R222_INVALID_TURN_CHRONOLOGY')
 first=rows[0]['detail']['events_added'];ck(len(first)>3 and first[0]['action']=='turn_start' and first[1]['action']=='R222_INITIATIVE_EFFECTIVE_ORDER','R222_FIRST_TURN_INITIATIVE_MISSING')
 ck(first[1]['roll_receipts']==receipts and first[1]['order']==order and first[1]['branch']==arm and first[1]['pre_hash']==ph,'R222_INIT_PROVENANCE_MISMATCH')
 ck(first[2]['action']=='R222_POSITION_AND_GUARD_POLICY_FIXTURE' and first[2]['position_E']=='(0, 4)' and first[2]['stream_map_mode']==mode,'R222_INITIAL_SCENE_OR_MAPPING_MISMATCH')
 round_no=0;turns=0;spells=0;heals=0;physics={};spore_tape=[];heal_tape=[]
 for e in ev:
  a=e['action']
  if a=='turn_start':turns+=1;round_no=(turns-1)//3+1
  if a=='R215_POST_RD_GUARD' and e['by']=='V':ck(round_no>1,'R222_VAROK_GUARD_R1_UNAUTHORIZED')
  if a=='PULSO_ESTABILIZACAO':ck(round_no>1,'R222_PULSO_RANGE_NOT_MET_R1')
  if a=='R216_GEOMETRY_STATE_DECISION':
   spells+=1;slot=round_no if mode=='ROUND' else spells
   tag=f'R222-SPORE-BANK-{slot}'
   want_save=dice(seed,tag+'-SPORES-SAVE-R',4,6);want_damage=dice(seed,tag+'-SPORES-DMG',10,10)
   ck(e['save_rolls']==want_save and e['spell_gross']==sum(want_damage)+10,'R222_SPORE_BANK_TAPE_INVALID')
   spore_tape.append({'round':round_no,'slot':slot,'save':want_save,'damage':want_damage})
  if a=='RECONSTITUICAO_SEIVA':
   heals+=1;slot=round_no if mode=='ROUND' else heals
   tag=f'R222-HEAL-BANK-{slot}';want=dice(seed,tag+'-RECONSTITUICAO',8,10)
   ck(e['healing_rolls']==want,'R222_HEAL_BANK_TAPE_INVALID');heal_tape.append({'round':round_no,'slot':slot,'healing_rolls':want})
  if a=='R215_OFFENSIVE_RNG':physics[e['stream']]={k:e[k] for k in ['attack_attempts','crit','damage_rolls']}
 ck(native['commits']==12 and native['phase']=='CENSORED_HORIZON','R222_NATIVE_INCOMPLETE')
 return {'seed':seed,'arm':arm,'mode':mode,'order':order,'rolls':receipts,'native':native,'HP':native['HP'],'PA':native['PA'],'E_decisions':[e['choice'] for e in ev if e['action']=='R216_SUPPORT_OBSERVED_STATE'],'physical_tapes':physics,'spores_tapes':spore_tape,'heals_tapes':heal_tape}

def verify(root=ROOT):
 prereg=root/'sources/R222_PREREG_BEFORE_NEW_COMBATS.json';spec=json.loads(prereg.read_text());ph=hashlib.sha256(prereg.read_bytes()).hexdigest()
 results=json.loads((root/'evidence/reports/R222_FACTORIAL_EXECUTIONS.json').read_text())
 files=sorted((root/'evidence/db').glob('R222_FACTOR_*.sqlite'));blocked=sorted((root/'evidence/quarantine').glob('R222_FACTOR_*.sqlite'))
 ck(len(files)==76 and len(results['admitted'])==76,'R222_VALID_ROSTER')
 ck(len(results['blocked'])==20 and len(blocked)==2,'R222_BLOCKED_ROSTER')
 ck(len(spec['seeds'])==24 and len(spec['arm_initiative'])==2 and len(spec['arm_rng_mapping'])==2,'R222_PRE_REG_FACTORIAL')
 for q in blocked:
  m,st,rows,pending=dbread(q);ck(pending==1 and st['phase']=='ACTIVE','R222_QUARANTINE_PENDING')
 passed=[audit_fight(p,ph) for p in files];by=collections.defaultdict(dict)
 for row in passed:by[row['seed']][row['arm'],row['mode']]=row
 log={(x['seed'],x['arm'],x['mode']):x for x in results['admitted']}
 for x in passed:
  v=log[x['seed'],x['arm'],x['mode']];ck(v['HP']==x['HP'] and v['PA']==x['PA'] and v['order']==x['order'],'R222_FINAL_REPORT_NOT_SOURCE_ALIGNED')
 for seed,cases in by.items():
  for arm in ('INIT_A','INIT_B'):
   if (arm,'ROUND') not in cases or (arm,'ABILITY') not in cases:continue
   a=cases[arm,'ROUND'];b=cases[arm,'ABILITY'];ck(a['order']==b['order'] and a['rolls']==b['rolls'],'R222_SAME_INIT_DIFFERENT_MODE_CHANGED_ORDER')
   for k in set(a['physical_tapes'])&set(b['physical_tapes']):ck(a['physical_tapes'][k]==b['physical_tapes'][k],'R222_PHYSICAL_TAPE_DIVERGED_WITH_MAPPING')
 full=[]
 for seed in spec['seeds']:
  if len(by[seed])<4:continue
  x=by[seed];ar=x['INIT_A','ROUND'];aa=x['INIT_A','ABILITY'];br=x['INIT_B','ROUND'];ba=x['INIT_B','ABILITY']
  ck(ar['order']==aa['order'] and br['order']==ba['order'],'R222_FACTORIAL_INIT_CONFUSION')
  d=lambda a,b:{k:a['HP'][k]-b['HP'][k] for k in a['HP']}
  full.append({'seed':seed,'orderA':ar['order'],'orderB':br['order'],'init_diff_round':d(ar,br),'init_diff_ability':d(aa,ba),'mapping_diff_A':d(ar,aa),'mapping_diff_B':d(br,ba),'choices':{f'{z["arm"]}_{z["mode"]}':z['E_decisions'] for z in x.values()}})
 ck(len(full)==14,'R222_COMPLETE_QUADRUPLES')
 discr=next(v for v in full if v['seed']==22288014)
 ck(discr['init_diff_round']['R']==-69 and discr['init_diff_ability']['R']==-69 and discr['init_diff_round']['V']==-35 and discr['init_diff_ability']['V']==-35,'R222_NONCOMMUTATIVE_NOT_REPRODUCED')
 cnt={k:sum(v['native'][k] for v in passed) for k in ['commits','events','moves','physical_attacks','opportunities','heals','spells']}
 return {'status':'PASS_R222_INDEPENDENT_FACTORIAL_ROLLED_INITIATIVE_RNG_ASSIGNMENT','attempted':96,'valid':len(passed),'blocked':len(results['blocked']),'blocked_unknown_banks':len(blocked),'full_factorial_seed_units':len(full),'changed_order_quadruples':sum(v['orderA']!=v['orderB'] for v in full),
 'round_tag_initiative_HP_diff':sum(any(v['init_diff_round'].values()) for v in full),'ability_tag_initiative_HP_diff':sum(any(v['init_diff_ability'].values()) for v in full),'mapping_change_HP_diff_A':sum(any(v['mapping_diff_A'].values()) for v in full),'mapping_change_HP_diff_B':sum(any(v['mapping_diff_B'].values()) for v in full),**cnt,'censures':len(passed),'KO':0,'history_replays':0,'full_seeds':full}
if __name__=='__main__':
 r=verify()
 (ROOT/'evidence/reports/R222_INDEPENDENT_FACTORIAL_AUDIT.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({k:v for k,v in r.items() if k!='full_seeds'},indent=2,ensure_ascii=False))
