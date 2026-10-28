"""Rehash structurally valid copied ledgers with falsified semantic fields; cold auditor must reject."""
import json,sqlite3,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT));import r120_cold_integrated_audit as cold
from r119_integrated_three_actor import core
ORIGINAL=ROOT/'runs/R119_THREE_ACTOR_DEV_918201.sqlite'
OUT=ROOT/'adversarial_copies';OUT.mkdir(exist_ok=True)
results=[]
for case in ('ALTER_NORMAL_NET','ALTER_COUNTER_ADVANTAGE'):
 p=OUT/f'R125_{case}_COPY.sqlite'
 with sqlite3.connect(ORIGINAL) as a,sqlite3.connect(p) as b:a.backup(b)
 shutil.copy2(ORIGINAL.with_suffix('.genesis.json'),p.with_suffix('.genesis.json'))
 with sqlite3.connect(p) as con:
  evs=[json.loads(x[0]) for x in con.execute('select row_json from events order by seq')]
  mutated=False
  for e in evs:
   for a in e['detail']['native_actions']:
    if case=='ALTER_NORMAL_NET' and a['action']=='weapon_attack' and a['hit'] and not mutated:
     a['net']+=1;mutated=True;break
    elif case=='ALTER_COUNTER_ADVANTAGE' and a['action']=='COUNTER_RESPONSE' and not mutated:
     a['advantage_bonus']+=1;mutated=True;break
   if mutated:break
  assert mutated
  genesis=dict(con.execute('select key,value from meta'))['genesis'];prev=genesis
  for e in evs:
   e['prev']=prev;digest=cold.sha(e)
   con.execute('UPDATE events SET prev=?,row_json=?,row_sha=? WHERE seq=?',(prev,cold.canon(e),digest,e['seq']))
   prev=digest
  con.execute("UPDATE meta SET value=? WHERE key='head'",(prev,))
 assert core.load(p)  # passes cryptographic/replay structural chain, since each semantic field rehashed
 reject=None
 try:cold.cold(p)
 except Exception as ex:reject=type(ex).__name__+' '+str(ex)
 assert reject is not None,case
 results.append({'case':case,'source_DB':ORIGINAL.name,'copied_file':p.name,'syntactic_sha_chain':'PASS',
  'semantic_cold_audit':'REJECT','cause':reject,'no_original_mutation':True})
(ROOT/'R125_COLD_REDTEAM_2.json').write_text(json.dumps({'cases':results,'accepted':0,'rejected':2},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
