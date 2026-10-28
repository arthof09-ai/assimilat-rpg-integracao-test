"""Independent R221 source initiative, chronology and ability-index common-RNG streams audit.
Engine-free; only imports independent R216 mechanical validator adapted for fixture E=(0,4).
"""
from pathlib import Path
import json,hashlib,random,sys,collections,sqlite3,re
ROOT=Path(__file__).resolve().parents[1]
from r221_independent_mechanical_audit import audit_one as native

def ck(b,message):
 if not b:raise AssertionError(message)
def rd(p):
 c=sqlite3.connect(f'file:{p}?mode=ro&immutable=1',uri=True)
 try:
  meta=dict(c.execute('SELECT key,value FROM meta'));st=json.loads(meta['state']);rows=[json.loads(r[0]) for r in c.execute('SELECT row_json FROM events ORDER BY seq')];pending=c.execute('select count(*) from pending').fetchone()[0];return meta,st,rows,pending
 finally:c.close()
def prf(seed,tag,n,face):
 h=hashlib.sha256(f'R215|{seed}|{tag}|{n}d{face}'.encode()).digest();rand=random.Random(int.from_bytes(h,'big'));return [rand.randint(1,face) for _ in range(n)]
def one(f,sha):
 m=re.fullmatch(r'R221_STABLE_(INIT_[AB])_S(\d{8})\.sqlite',f.name);ck(m,'R221_ID_MISMATCH');arm,seed=m.group(1),int(m.group(2))
 native_result=native(f);meta,st,rows,pending=rd(f);ck(pending==0,'R221_VALID_PENDING')
 x=st['r221'];rolls={k:{'dice':prf(seed,f'R221-INIT-{arm}-{k}',4,6),'bonus':b,'total':sum(prf(seed,f'R221-INIT-{arm}-{k}',4,6))+b} for k,b in [('V',29),('R',25),('E',30)]}
 ck(x['rolls']==rolls and x['prereg_sha256']==sha,'R221_BAD_INIT_RNG_OR_PREREG')
 ck(len({z['total'] for z in rolls.values()})==3,'R221_UNKNOWN_TIE')
 order=sorted(rolls,key=lambda k:-rolls[k]['total']);ck(x['order']==st['order']==order,'R221_ORDER_DRIFT')
 ev=[e for row in rows for e in row['detail']['events_added']]
 start=[e['by'] for e in ev if e['action']=='turn_start'];end=[e['by'] for e in ev if e['action']=='turn_end'];ck(start==end==order*4,'R221_SCHEDULER_CHRONOLOGY')
 first=rows[0]['detail']['events_added'];ck(first[1]['action']=='R221_INITIATIVE_EFFECTIVE_ORDER' and first[1]['roll_receipts']==rolls and first[1]['pre_hash']==sha,'R221_FIRST_INIT_RECEIPT');ck(first[2]['action']=='R221_POSITION_AND_GUARD_POLICY_FIXTURE' and first[2]['position_E']=='(0, 4)','R221_START_SCENE')
 spell_ord=0;heal_ord=0;physical_rng={};round_no=0;start_no=0
 for e in ev:
  action=e['action']
  if action=='turn_start':start_no+=1;round_no=(start_no-1)//3+1
  if action=='R215_POST_RD_GUARD' and e['by']=='V':ck(round_no>1,'R221_V_R1_GUARD_UNAUTHORIZED')
  if action=='PULSO_ESTABILIZACAO':ck(round_no>1,'R221_PULSO_RANGE_R1_INELIGIBLE')
  if action=='R216_GEOMETRY_STATE_DECISION':
   spell_ord+=1;tag=f'R221-SPORES-USE-{spell_ord}'
   ck(e['save_rolls']==prf(seed,tag+'-SPORES-SAVE-R',4,6),'R221_SPORE_SAVE_TAPE_DRIFT')
   # This preflight also confirms gross damage is from the source-required 10d10+10.
   ck(e['spell_gross']==sum(prf(seed,tag+'-SPORES-DMG',10,10))+10,'R221_SPORE_DAMAGE_TAPE_DRIFT')
  if action=='RECONSTITUICAO_SEIVA':
   heal_ord+=1;tag=f'R221-HEAL-USE-{heal_ord}'
   ck(e['healing_rolls']==prf(seed,tag+'-RECONSTITUICAO',8,10),'R221_HEAL_TAPE_DRIFT')
  if action=='R215_OFFENSIVE_RNG':physical_rng[e['stream']]={k:e[k] for k in ('attack_attempts','crit','damage_rolls')}
 ck(native_result['commits']==12 and native_result['phase']=='CENSORED_HORIZON','R221_NATIVE_NOT_COMPLETE')
 return {'seed':seed,'arm':arm,'HP':native_result['HP'],'PA':native_result['PA'],'order':order,'decisions':[e['choice'] for e in ev if e['action']=='R216_SUPPORT_OBSERVED_STATE'],'spell_uses':spell_ord,'direct_heal_uses':heal_ord,'physical_rng':physical_rng, 'native':native_result}

def verify(root=ROOT):
 p=root/'sources/R221_PREREG_BEFORE_NEW_COMBATS.json';spec=json.loads(p.read_text());sha=hashlib.sha256(p.read_bytes()).hexdigest();report=json.loads((root/'evidence/reports/R221_STABLE_ACTION_RNG_EXECUTIONS.json').read_text())
 admitted=sorted((root/'evidence/db').glob('R221_STABLE_*.sqlite'));blocked=sorted((root/'evidence/quarantine').glob('R221_STABLE_*.sqlite'))
 ck(len(admitted)==33 and len(report['admitted'])==33 and len(report['blocked'])==15,'R221_ADMISSION_DENOMINATOR')
 ck(len(blocked)==4,'R221_UNKNOWN_HALF_BANK_COUNT')
 for q in blocked:
  m,st,r,pending=rd(q);ck(pending==1 and st['phase']=='ACTIVE','R221_UNKNOWN_EFFECT_PENDING')
 results=[one(x,sha) for x in admitted]
 by=collections.defaultdict(dict)
 for x in results:by[x['seed']][x['arm']]=x
 paired=[]
 for seed in spec['seeds']:
  if len(by[seed])!=2:continue
  a,b=by[seed]['INIT_A'],by[seed]['INIT_B']
  for k in set(a['physical_rng'])&set(b['physical_rng']):ck(a['physical_rng'][k]==b['physical_rng'][k],'R221_ATTACK_STREAM_MISMATCH')
  ck(a['spell_uses']==b['spell_uses'] and a['direct_heal_uses']==b['direct_heal_uses'],'R221_ACTION_INDEX_UNPAIRED')
  paired.append({'seed':seed,'order_changed':a['order']!=b['order'],'HP_diff':{k:a['HP'][k]-b['HP'][k] for k in a['HP']},'E_decisions_changed':a['decisions']!=b['decisions'],'spell_uses':a['spell_uses'],'direct_heal_uses':a['direct_heal_uses']})
 ck(len(paired)==13 and sum(x['order_changed'] for x in paired)==9,'R221_PAIRS_ORDER_COUNT')
 ck(sum(x['E_decisions_changed'] for x in paired)==3 and sum(any(x['HP_diff'].values()) for x in paired)==0,'R221_NEGATIVE_HP_RESULT')
 totals={k:sum(x['native'][k] for x in results) for k in ['commits','events','moves','physical_attacks','opportunities','heals','spells']}
 return {'status':'PASS_R221_INDEPENDENT_ROLLED_INITIATIVE_ABILITY_INDEX_CRN','admitted':len(results),'blocked':len(report['blocked']),'complete_seed_pairs':len(paired),'order_changes':sum(x['order_changed'] for x in paired),'support_choice_diff_pairs':sum(x['E_decisions_changed'] for x in paired),'terminal_hp_diff_pairs':0,'blocked_unknown_banks':len(blocked),**totals,'censures':len(results),'KO':0,'historical_replays':0,'paired_results':paired}
if __name__=='__main__':
 r=verify();(ROOT/'evidence/reports/R221_INDEPENDENT_STABLE_TAPE_AUDIT.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='paired_results'},indent=2,ensure_ascii=False))
