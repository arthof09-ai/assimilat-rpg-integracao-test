from pathlib import Path
import json,sqlite3,hashlib
H=Path(__file__).parent
old=Path('/mnt/data/vlab_r161_work/baseline_r160/r151_r160/R160_QUARANTINE_UNKNOWN_EFFECT_NO_REPEAT.json')
b=json.loads(old.read_text());run=H/'runs'
ids=['R163_AFTER_INTENT_S1163101','R163_FRESH_AFTER_INTENT_S1163103','R163_FRESH_AFTER_COMMIT_S1163104','R165_FLECHA_TURN_EXPLICIT_DEV_S1185001','R165_FLECHA_TURN_EXPLICIT_V2_DEV_S1185088','R165_FLECHA_TURN_EXPLICIT_V3_DEV_S1185114','R166_CASULO_AOO_NEGATIVE_DEV_S1195392','R166_V2_CASULO_AOO_NEGATIVE_DEV_S1195557','R166_V2_CASULO_AOO_KO_DEV_S1205088','R168_ED_AUREN_VS_CROC_BASIC_DEV_S1168001','R168_ED_AUREN_VS_CROC_BASIC_RESERVED_NONBLIND_S1169001']
per={}
for name in ids:
 file=run/f'{name}.sqlite';assert file.exists(),file
 with sqlite3.connect(f'file:{file}?mode=ro',uri=True) as c:
  assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
  pending=c.execute('select count(*) from pending').fetchone()[0]
  ev=c.execute('select count(*) from events').fetchone()[0]
 state='SELECTED_COLD_PASS' if name in ids[5:6]+ids[7:] else 'DIAGNOSTIC_QUARANTINE'
 if pending:state='UNKNOWN_EFFECT_HOLD_NO_RETRY'
 per[name]={'DB_SHA256':hashlib.sha256(file.read_bytes()).hexdigest(),'commits':ev,'pending':pending,'status':state}
new={'operation':b['operation'],'baseline':'R01–R160 intact archived','prior_R160_quarantine_verbatim':b,'r161_to_r170_seen_banks':per,
 'R169_semantic_redteam_V1':'DIAGNOSTIC_WAL_ONLY_NOT_PERSISTED_IN_BASE_DB, excluded; V2 uses checkpointed actual modified copies, 2/2 rejected',
 'accepted_selected_new_runs':[k for k,v in per.items() if v['status']=='SELECTED_COLD_PASS'],
 'preserved_incidents':['R123_UNKNOWN_EFFECT','R130_QA_FAIL','R134_UNKNOWN_EFFECT','R138_SPATIAL_PARITY_HOLD','R143_UNKNOWN_EFFECT','R124_CENSORED','R156_UNKNOWN_EFFECT','R159_ODD_HALF_BLOCKED'],
 'no_repeat':'No R01–R160 historical event repeated; new diagnostics with pending remain locked. No random or ID reuse.',
 'authority':'CM-000006 PAUSED; no writer lease epoch fencing ID/IBX101-ACK; sandbox development and read-only Notion/Library only'}
(H/'R170_QUARANTINE_NO_REPEAT.json').write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v['status'] for k,v in per.items()},ensure_ascii=False,indent=2))
