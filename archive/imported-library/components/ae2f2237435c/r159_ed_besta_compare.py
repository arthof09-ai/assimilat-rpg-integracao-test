"""Source-conditional ED x Beast contrast (NOT official): uses historical v0.8.1 native attack/spell + R18.
Only factor = Grifo uses one Descarga Curta opening or not. Grifo initiative remains unproven;
exogenous beast opening only, not natural initiative. Limits source page line length and Lightning RD Auren unknown.
"""
from pathlib import Path
import json,sqlite3,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import r159_ed_besta_native as b

PREREG={'stage':'R159_ED_BE','source_grifo':b.AUTH['Grifo'],'source_auren':b.AUTH['Auren'],
 'seed':998801,'sides':['BE_SPECIAL','BE_BASIC'],'exogenous_opening':'GRIFO_FIRST_ONLY_NO_INITIATIVE_AUTH',
 'single_factor':'Grifo first own action 55PA Descarga Curta (save half on even only), else Talon basic',
 'horizon_actor_turns':70,'test_family':'DEVELOPMENT_PAIRED_NOT_BLIND',
 'rd_lightning_Auren':'UNREPORTED; conditional LAB0 ONLY, NOT official',
 'geometry':'short straight unobstructed near1.5m LAB ONLY; precise source maximum unknown',
 'policy':'Auren physical lance each own turn, Grifo talon thereafter. No deliberate foregoing.',
 'source_and_unit_limits':['Grifo natural INIT bonus unknown; exogenous','No reaction against Reflex save','No 2ED team','No canon benchmark cell'],
 'no_repeat':['R93/R95 flawed historic','R112 former 915133/920801','R01–R150']}

def run(variant):
 seed=PREREG['seed'];db=ROOT/'runs'/f'R159_ED_GRIFO_AUREN_{variant}_DEV_S{seed}.sqlite'
 db.parent.mkdir(parents=True,exist_ok=True)
 b.init_db(db,'G_FULL',seed,variant)
 turns=0;stop=None
 while turns<PREREG['horizon_actor_turns']:
  s,h,rev=b.core.load(db)
  if s['phase']!='ACTIVE':break
  actor=s['active'];tar='E' if actor=='B' else 'B'
  b.commit(db,'TURN_START',{'actor':actor})
  s,_,_=b.core.load(db)
  if actor=='B' and variant=='BE_SPECIAL' and s['special_used_count']==0:
   data=b.special_inputs(s)
   if data['raw']%2:stop='ODD_HALF_NORMATIVE_HOLD';break
   b.commit(db,'NATIVE_SPECIAL',data)
  else:
   data=b.attack_inputs(s,actor,tar)
   b.commit(db,'NATIVE_ATTACK',data)
  b.commit(db,'TURN_END',{'actor':actor})
  turns+=1
 s,head,rev=b.core.load(db)
 with sqlite3.connect(db) as con:
  rows=[json.loads(x[0]) for x in con.execute('select row_json from events order by seq')]
  pending=con.execute('select count(*) from pending').fetchone()[0]
 with sqlite3.connect(db) as src,sqlite3.connect(db.with_suffix('.checkpoint.sqlite')) as dst:src.backup(dst)
 assert b.core.load(db)==b.core.load(db.with_suffix('.checkpoint.sqlite'))
 A=[r['detail']['native_action'] for r in rows if r['kind']=='NATIVE_ATTACK'];S=[r['detail']['native_action'] for r in rows if r['kind']=='NATIVE_SPECIAL']
 return {'run_id':db.stem,'seed':seed,'phase':s['phase'],'winner':s['winner'],'events':rev,'actor_turns':turns,
  'tactical_beast_special':variant=='BE_SPECIAL','critical_negative_lab':sum(e.get('critical')=='NEGATIVE' for e in A),
  'critical_positive':sum(e.get('critical')=='POSITIVE' for e in A),
  'attacks':len(A),'specials':len(S),'PA_spent':sum(e.get('PA_spent',0) for e in S),
  'hp_final':{k:v['resource']['hp'] for k,v in s['actors'].items()},
  'damage_auren_by_grifo':sum(e['hp_loss_actual'] for e in A if e['from']=='B')+sum(e['hp_before']-e['hp_after'] for e in S if e['by']=='B'),
  'damage_grifo_by_auren':sum(e['hp_loss_actual'] for e in A if e['from']=='E'),
  'conditional_rd0_and_initiative':True,'stop':stop,'pending':pending,'head':head}

if __name__=='__main__':
 p=ROOT/'R159_ED_BE_PREREG.json';p.write_text(json.dumps(PREREG,ensure_ascii=False,indent=2)+'\n')
 out=[]
 for variant in PREREG['sides']:
  v=run(variant);out.append(v);print({k:v[k] for k in ['run_id','events','phase','winner','actor_turns','hp_final','critical_negative_lab','PA_spent','stop']},flush=True)
 (ROOT/'R159_ED_BE_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
