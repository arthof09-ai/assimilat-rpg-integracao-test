"""R148: source-bound independent spatial audit and frozen-prefix readback.
Never reruns earlier commands. Input R146 immutable. No network or official sheets.
"""
import copy,hashlib,json,sqlite3,shutil
from pathlib import Path
import r147_cold_metric_independent as cold
import r146_native_metric_corrected as native
ROOT=Path(__file__).resolve().parent
DB=ROOT/'runs'/'R146_MULTI_SOURCE_FERYN_ERISTAN_DEV_S995401.sqlite'
PREFIX=ROOT/'runs'/'R148_R146_COLD_RECONSTRUCTED_PREFIX_REV20.sqlite'

def run():
 if PREFIX.exists():raise RuntimeError('NO_OVERWRITE_RECONSTRUCTED_PREFIX')
 pre=json.loads((ROOT/'R146_PREREG.json').read_text())
 assert pre['experimental_distance_m']['F-E_before_move']==3
 assert pre['experimental_distance_m']['F-E_after_move']==2
 assert pre['source_abilities']['PULSO'].find('<=3m')>=0
 metrics=cold.cold(DB,capture_at=20)
 assert metrics['metrics']['commits']==40 and metrics['metrics']['native_events']==43
 assert metrics['phase']=='CENSORED_HORIZON' and metrics['end_hp']['F1']==191
 prefix_state=metrics['captured_prefix_state']
 assert prefix_state and prefix_state['round']==3 and prefix_state['turn_index']==6
 with sqlite3.connect(DB) as c:
  rows=[json.loads(z[0]) for z in c.execute('SELECT row_json FROM events ORDER BY seq')]
  aoos=[r for r in rows if r['kind']=='MOVE_F_AOO_PULSO']
  assert len(aoos)==1
  aoo=aoos[0]; events=aoo['detail']['native_actions']
  assert aoo['payload']['pulse_distance_m']==pre['experimental_distance_m']['F-E_before_move']
  assert [x['action'] for x in events]==['weapon_attack','PULSO_ESTABILIZACAO','move']
  assert events[-1]['from']=='B1' and events[-1]['to']=='B2'
  end_state=json.loads(c.execute('SELECT value FROM meta WHERE key=?',('state',)).fetchone()[0])
  assert end_state['actors']['F1']['resource']['position']=='B2'
  row20=c.execute('SELECT row_sha,after_sha FROM events WHERE seq=20').fetchone()
  assert row20[1]==cold.sha(prefix_state)
 shutil.copyfile(DB,PREFIX)
 with sqlite3.connect(PREFIX) as c:
  c.execute('DELETE FROM events WHERE seq>20')
  c.execute('UPDATE meta SET value=? WHERE key=?',(row20[0],'head'))
  c.execute('UPDATE meta SET value=? WHERE key=?',(cold.can(prefix_state),'state'))
  c.execute('UPDATE meta SET value=? WHERE key=?',('20','revision'))
 state,head,revision=native.core.load(PREFIX)
 assert revision==20 and head==row20[0] and state==prefix_state
 # Confirm source full 40 commits unaffected by making independent prefix copy.
 assert cold.cold(DB)['head']==metrics['head']
 result={
 'status':'PASS_SOURCE_SPATIAL_BINDING_AND_COLD_PREFIX',
 'run_id':DB.stem,'seed':995401,'source_prereg_before_m':3,'source_prereg_after_m':2,
 'ledger_pulse_pre_m':aoo['payload']['pulse_distance_m'],
 'causal_action_order':[v['action'] for v in events],
 'B0_B3_topology_not_meters':True,
 'prefix_reconstruction':'COLD_RECONSTRUCTED_NOT_CONTEMPORANEOUS',
 'prefix_rev':revision,'full_rev':40,'prefix_sha256':None,
 'source_db_sha256':hashlib.sha256(DB.read_bytes()).hexdigest(),
 'prefix_R18_core_load':'PASS','original_action_commands_reexecuted':False,
 'full_head_unchanged':metrics['head'],
 'technical_horizon':'CENSORED_HORIZON','winner':None,
 'official_power_cell_credits':0,'terminal_certifications':0}
 # SQLite may defer WAL checkpoint to connection release; hash only after all checks/reopens.
 with sqlite3.connect(PREFIX) as c: c.execute('PRAGMA wal_checkpoint(TRUNCATE)')
 result['prefix_sha256']=hashlib.sha256(PREFIX.read_bytes()).hexdigest()
 assert result['prefix_sha256']!=result['source_db_sha256'], 'prefix bytes should differ from full DB'
 (ROOT/'R148_SOURCE_BINDING_AND_PREFIX.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 return result
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
