"""R169 adversarial controlled DB copies with SHA chain repaired; do NOT touch originals."""
from pathlib import Path
import sqlite3,json,hashlib,shutil,sys
HERE=Path(__file__).parent
sys.path.insert(0,str(HERE))
from r166_cold_concurrent_independent import verify as audit166,sha as SHA
from r165_cold_temporal_independent import audit as audit165
D=HERE/'adversarial_copies';D.mkdir(exist_ok=True)
SRC166=next(p for p in (HERE/'runs').glob('R166_V2_CASULO_AOO_KO_DEV_*.sqlite') if '.checkpoint.' not in p.name)
SRC165=next(p for p in (HERE/'runs').glob('R165_FLECHA_TURN_EXPLICIT_V3_DEV_*.sqlite') if '.checkpoint.' not in p.name)
R=[]
for source,kind in [(SRC166,'FAKE_HP_LOSS'),(SRC165,'FAKE_EXPIRY')]:
 target=D/f'R169_V2_{kind}_{source.stem}.sqlite'
 assert not target.exists(),'NO_REPEAT: redteam snapshot already exists'
 shutil.copy2(source,target)
 shutil.copy2(source.with_suffix('.genesis.json'),target.with_suffix('.genesis.json'))
 with sqlite3.connect(target) as c:
  seq=c.execute('select max(seq) from events').fetchone()[0]
  before=c.execute('select row_json,row_sha from events where seq=?',(seq,)).fetchone()
  obj=json.loads(before[0]);actions=obj['detail']['native_actions']
  if kind=='FAKE_HP_LOSS':
   assert actions[0]['hp_loss_actual']==60 and actions[0]['net']==114
   actions[0]['hp_loss_actual']=114;actions[0]['overkill']=0
  else:
   matches=[x for x in actions if x['action']=='FLECHA_TRAVA_EXPIRES'];assert len(matches)==1
   assert matches[0]['speed_after']=='16';matches[0]['speed_after']='15'
  revised=json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False)
  digest=SHA(obj)
  c.execute('update events set row_json=?,row_sha=? where seq=?',(revised,digest,seq))
  c.execute('update meta set value=? where key="head"',(digest,))
  c.commit()
  c.execute('pragma wal_checkpoint(TRUNCATE)')
  actual=c.execute('select row_json,row_sha from events where seq=?',(seq,)).fetchone()
  assert SHA(json.loads(actual[0]))==actual[1]==digest
  assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
 assert SHA(obj)==digest and digest!=before[1] and hashlib.sha256(target.read_bytes()).hexdigest()!=hashlib.sha256(source.read_bytes()).hexdigest()
 try:
  if kind=='FAKE_HP_LOSS': audit166(target)
  else:audit165(target)
  raise AssertionError('ADVERSARIAL_REWRITE_NOT_DETECTED')
 except (AssertionError,ValueError) as e:
  assert 'ADVERSARIAL_REWRITE_NOT_DETECTED' not in str(e)
  R.append({'type':kind,'copied_db':target.name,'original_db':source.name,'original_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'redteam_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'sqlite_integrity':'ok','R18_row_SHA_recalculated':True,'independent_cold_auditor':'REJECTED_SEMANTIC_TAMPER','error_excerpt':str(e)[:220]})
result={'status':'PASS_2_OF_2_STRUCTURALLY_VALID_TAMPERS_REJECTED','adversarial_copies':R,'originals_modified':False,'contracts':['RNG_REPLAY_STATISTICS','TURN_SCHEDULER_EVENT_SOURCING','BLEED_AND_HEAL_RESTRICTIONS']}
(HERE/'R169_V2_ADVERSARIAL_SEMANTIC_RESULTS.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
