"""R140: independent COLD prefix reconstruction, not a contemporaneous original checkpoint.
Committed original events are not re-executed. Source full DB remains unchanged.
"""
import json,sqlite3,hashlib,shutil
from pathlib import Path
import r139_cold_independent as auditor
ROOT=Path(__file__).resolve().parent
FULL=ROOT/'runs'/'R138_MULTI_SOURCE_FERYN_ERISTAN_DEV_S991402.sqlite'
TARGET=ROOT/'runs'/'R140_COLD_RECONSTRUCTED_PREFIX_ROUND2_REV20.sqlite'
def reconstruct():
 if TARGET.exists():raise ValueError('NO_OVERWRITE_EXISTING_CHECKPOINT')
 a=auditor.cold(FULL,capture_at=20)
 st=a['captured_prefix_state'];assert st and st['round']==3 and st['turn_index']==6
 shutil.copyfile(FULL,TARGET)
 with sqlite3.connect(TARGET) as con:
  row=con.execute('SELECT row_sha,after_sha FROM events WHERE seq=20').fetchone()
  assert row and row[1]==auditor.sha(st)
  con.execute('DELETE FROM events WHERE seq>20')
  con.execute('UPDATE meta SET value=? WHERE key=?',(row[0],'head'))
  con.execute('UPDATE meta SET value=? WHERE key=?',(auditor.can(st),'state'))
  con.execute('UPDATE meta SET value=? WHERE key=?',('20','revision'))
 # Authenticated by original R18 checker (not audit oracle)
 import r138_multiround_native as runner
 recovered,head,revision=runner.core.load(TARGET)
 assert revision==20 and recovered==st and head==row[0]
 # independent verified prefix 20 events; no writer promotion
 output={'checkpoint':TARGET.name,'classification':'COLD_RECONSTRUCTED_PREFIX_NOT_LIVE_SAVE',
 'original_run':FULL.stem,'source_revision':40,'prefix_revision':revision,'original_events_reexecuted':False,
 'last_event_row_sha':head,'prefix_state_sha256':auditor.sha(st),
 'checkpoint_file_sha256':hashlib.sha256(TARGET.read_bytes()).hexdigest(),
 'open_by_original_R18':'PASS','source_head_is_untouched':auditor.cold(FULL)['head']==a['head'],
 'round_after_prefix':st['round'],'active_next':st['active'],
 'HP':{k:v['resource']['hp'] for k,v in st['actors'].items()},
 'PA':{k:v['resource']['pa'] for k,v in st['actors'].items()}}
 (ROOT/'R140_COLD_PREFIX_CHECKPOINT.json').write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
 return output
if __name__=='__main__':print(json.dumps(reconstruct(),indent=2,ensure_ascii=False))
