"""Independent zero-resolver cap audit + two semantic redteam checks on copied ledger.
No import of native or R18, never writes to actual R138 or R141 success DB.
"""
import hashlib,json,sqlite3,random,shutil
from pathlib import Path
import r139_cold_independent as cold
ROOT=Path(__file__).resolve().parent

def check_cap():
 p=ROOT/'runs'/'R141_HEAL_CAP_S993101.sqlite';st=json.loads(p.with_suffix('.genesis.json').read_text())
 with sqlite3.connect(p) as con:
  meta=dict(con.execute('SELECT key,value FROM meta'))
  rows=[json.loads(x[0]) for x in con.execute('SELECT row_json FROM events ORDER BY seq')]
  pending=con.execute('SELECT count(*) FROM pending').fetchone()[0]
 assert len(rows)==1 and pending==0 and meta['revision']=='1'
 row=rows[0];assert row['kind']=='HEAL' and row['before_sha']==cold.sha(st) and row['prev']==meta['genesis']
 r=st['actors']['E']['resource'];t=st['actors']['F1']['resource'];p0=row['payload']
 assert r['pa']==804 and r['standard']==1 and t['hp']==465 and t['maximum_hp']==479
 die=cold.dice(st['seed'],1,'E','HEAL',8,10)
 assert p0['dice']==die and p0['distance_m']==3
 gross=sum(die)+25+20;actual=min(gross,479-465)
 ev=row['detail']['native_actions'][0]
 assert (gross,actual)==(96,14)
 for name,value in [('gross_heal',gross),('actual_healed',actual),('equipped_gloves_bonus',20),
    ('excess_heal',gross-actual),('hp_before',465),('hp_after',479),('PA_spent',75),('bleeding_removed',False)]:
  assert ev[name]==value,(name,ev[name],value)
 r['pa']-=75;r['standard']=0;t['hp']=479;st['ability_nonce']['E_HEAL']+=1
 assert row['after_sha']==cold.sha(st) and cold.sha(row)==meta['head']
 assert cold.sha(json.loads(meta['state']))==cold.sha(st)
 return {'run_id':p.stem,'independent_heal_cap_audit':'PASS','gross':gross,'effective':actual,'overheal':gross-actual,
 'new_pa_E':r['pa'],'ledger_sha':meta['head'],'imports_resolver':False}

def redteam():
 origin=ROOT/'runs'/'R138_MULTI_SOURCE_FERYN_ERISTAN_DEV_S991402.sqlite'
 results=[]
 for mode,idx in [('FAKE_PA_COST',9),('FAKE_EFFECT_EXPIRY',17)]:
  target=ROOT/'quarantined'/f'R142_REDTEAM_{mode}_REHASHED.sqlite'
  target.parent.mkdir(exist_ok=True)
  if target.exists():
   shutil.copyfile(origin.with_suffix('.genesis.json'),target.with_suffix('.genesis.json'))
   try:cold.cold(target)
   except AssertionError as exc:
    results.append({'mode':mode,'test_copy':target.name,'events':40,'rehashed_chain':'YES_TEST_ONLY',
      'verdict':'INDEPENDENT_SEMANTIC_REJECT','reason':str(exc),'original_unmodified':True,
      'file_sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    continue
   raise AssertionError('EXISTING_REDTEAM_NOT_REJECTED')
  shutil.copyfile(origin,target)
  shutil.copyfile(origin.with_suffix('.genesis.json'),target.with_suffix('.genesis.json'))
  with sqlite3.connect(target) as con:
   evs=[json.loads(r[0]) for r in con.execute('select row_json from events order by seq')]
   assert evs[idx-1]['kind']==('HEAL' if mode=='FAKE_PA_COST' else 'END')
   if mode=='FAKE_PA_COST':
    entry=evs[idx-1]['detail']['native_actions'][0];assert entry['PA_spent']==75;entry['PA_spent']=0
   else:
    e=evs[idx-1]['detail']['native_actions'][-1]
    assert e['action']=='EXPIRE_TURN_EFFECT' and e['bonus_speed_removed_m']==12
    e['bonus_speed_removed_m']=0
   head=dict(con.execute('select key,value from meta'))['genesis']
   for row in evs:
    row['prev']=head
    sha=cold.sha(row)
    con.execute('UPDATE events SET prev=?, row_json=?, row_sha=? WHERE seq=?',
        (head,cold.can(row),sha,row['seq']))
    head=sha
   con.execute('UPDATE meta SET value=? WHERE key=?',(head,'head'))
  with sqlite3.connect(target) as con:
   record_count=con.execute('select count(*) from events').fetchone()[0]
  assert record_count==40
  try:cold.cold(target)
  except AssertionError as exc:verdict='INDEPENDENT_SEMANTIC_REJECT';reason=str(exc)
  else:raise AssertionError('INDEPENDENT_AUDITOR_DID_NOT_CATCH_'+mode)
  results.append({'mode':mode,'test_copy':target.name,'events':record_count,
    'rehashed_chain':'YES_TEST_ONLY','verdict':verdict,'reason':reason,
    'original_unmodified':True,'file_sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
 return results
if __name__=='__main__':
 out={'cap':check_cap(),'redteam':redteam(),'source_status':'MASTER_ONLY_SYNTHETIC_TECHNICAL',
  'auditor_imports_native_or_R18':False}
 (ROOT/'R142_COLD_CAP_AND_REDTEAM.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(out,indent=2,ensure_ascii=False))
