"""Hash-rebuilt illegal clones for R227, preserving every original. Auditor must reject mechanics not only hash tamper."""
import sqlite3,json,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'code'))
import r227_independent_magic_rd_audit as checker
import r227_magic_rd_sensitivity_native as sim
p0=ROOT/'evidence/db/R227_MANOPLA_LIGHTNING_RD100_S22762002.sqlite'
def mutate(p,kind):
 c=sqlite3.connect(p);m=dict(c.execute('select key,value from meta'));st=json.loads(m['state']);last=json.loads(c.execute('select row_json from events where seq=2').fetchone()[0])
 if kind=='FORGED_ASSUMED_RD':st['r227']['magical_rd_assumption']=0
 elif kind=='FORGED_ITEM_PA':st['actors']['R']['pa']+=22
 elif kind=='FALSE_SLOW':
  e=next(x for x in st['native_events'] if x['action']=='R227_ITEM_LIGHTNING_AND_CONDITION');e['slow_applied']=True;e['slow_m']=3
 elif kind=='FALSE_LIGHTNING_DAMAGE':
  e=next(x for x in st['native_events'] if x['action']=='R227_ITEM_LIGHTNING_AND_CONDITION');e['magic_effective']=20
 else:raise AssertionError('UNKNOWN_MUTATION')
 if kind in ('FALSE_SLOW','FALSE_LIGHTNING_DAMAGE'):
  # report first row's detail changed as well; rebuild row 1 then row 2 link
  first=json.loads(c.execute('select row_json from events where seq=1').fetchone()[0]); e=next(x for x in first['detail']['events_added'] if x['action']=='R227_ITEM_LIGHTNING_AND_CONDITION')
  if kind=='FALSE_SLOW':e['slow_applied']=True;e['slow_m']=3
  else:e['magic_effective']=20
  first['after_sha']=checker.dig({**st,'native_events':first['detail']['events_added']}) if False else first['after_sha']
  # This adversarial probe intentionally repairs the row hash and next prev but leaves published before/after state projection;
  # SQL audit should reject via source semantics even after receipt reconstruction.
  firstjson=json.dumps(first,sort_keys=True,separators=(',',':'),ensure_ascii=False);firstsha=checker.dig(first)
  c.execute('update events set row_json=?,row_sha=? where seq=1',(firstjson,firstsha))
  last['prev']=firstsha
  last['before_sha']=first['after_sha']
 # rebuild final-row state hash and head
 last['after_sha']=checker.dig(st)
 lastjson=json.dumps(last,sort_keys=True,separators=(',',':'),ensure_ascii=False)
 c.execute('update events set row_json=?,row_sha=?,prev=?,after_sha=? where seq=2',(lastjson,checker.dig(last),last['prev'],last['after_sha']))
 c.execute('update meta set value=? where key="state"',(json.dumps(st,sort_keys=True,separators=(',',':'),ensure_ascii=False),))
 c.execute('update meta set value=? where key="head"',(checker.dig(last),))
 c.commit();c.close()

def main():
 folder=ROOT/'evidence/adversarial';folder.mkdir(exist_ok=True);out=[]
 for kind in ['FORGED_ASSUMED_RD','FORGED_ITEM_PA','FALSE_SLOW','FALSE_LIGHTNING_DAMAGE']:
  p=folder/f'R227_FORGED_{kind}.sqlite'
  if p.exists():raise FileExistsError('R227_ATTACK_COLLISION')
  shutil.copy2(p0,p);mutate(p,kind)
  try:checker.audit_one(p,sim.P,sim.IH,sim.PH,'LIGHTNING_RD100',22762002);raise AssertionError('ACCEPTED_ILLEGAL_MUTATION')
  except AssertionError as e:
   if str(e)=='ACCEPTED_ILLEGAL_MUTATION':raise
   out.append({'case':kind,'rejected':True,'reason':str(e)})
 (ROOT/'evidence/reports/R227_ADVERSARIAL_RESULT.json').write_text(json.dumps({'attacks':out},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'status':'PASS_R227_FORGED_SCIENCE_PARAMETERS_REJECTED','attack_clones':len(out)},indent=2))
if __name__=='__main__':main()
