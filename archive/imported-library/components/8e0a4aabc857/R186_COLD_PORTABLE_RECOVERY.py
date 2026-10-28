"""R186 portable READ-ONLY cold verifier. NO combat production / no historical replay."""
import sys,pathlib,json,hashlib,zipfile,sqlite3,csv
ROOT=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'code'))
import r183_independent_auditor as audit
CAN=audit.CAN;SHA=audit.SHA
BASE_SHA='e8da2752ebcd5c7d99c4d5cee010be396462e765f44b29c94e4084194d89f19e'
MAN=ROOT/'R186_SHA256_MANIFEST.json'
def verify():
 manifest=json.loads(MAN.read_text());assert manifest['manifest_version']=='R186_VLAB_MESTRE_ONLY_SOURCE_SCOPE_SHA256'
 for rel,expect in manifest['files'].items():
  path=ROOT/rel;assert path.is_file(),('FILE_ABSENT',rel)
  assert hashlib.sha256(path.read_bytes()).hexdigest()==expect,('FILE_SHA_DRIFT',rel)
 expected=set(manifest['files'])|{'R186_SHA256_MANIFEST.json'}
 existing={str(x.relative_to(ROOT)) for x in ROOT.rglob('*') if x.is_file() and '__pycache__' not in x.parts and x.suffix != '.pyc' and not x.name.endswith(('-wal','-shm'))}
 assert expected==existing,('MISSING_OR_EXTRA',list(existing-expected)[:8],list(expected-existing)[:8])
 base=ROOT/'baseline'/'R176_BASELINE_EXACT.zip'
 assert hashlib.sha256(base.read_bytes()).hexdigest()==BASE_SHA
 with zipfile.ZipFile(base) as z:assert len(z.namelist())==298 and z.testzip() is None
 pre=ROOT/'R184_PRE_REGISTRATION_BEFORE_EXECUTION.json'
 assert hashlib.sha256(pre.read_bytes()).hexdigest()==audit.PRE_SHA
 cross=json.loads((ROOT/'R185_17_CONTRACT_CROSSWALK.json').read_text())
 ids=cross['original_id_sequence'];assert len(ids)==len(set(ids))==17
 assert {x['id'] for x in cross['rows']}==set(ids)
 assert all(x['terminal_certified'] is False for x in cross['rows'])
 assert cross['R177_to_R186_terminals']==0 and cross['official_cells']=={'before':0,'after':0,'denominator':1875}
 summ=json.loads((ROOT/'evidence'/'R184_PAIRED_RESULTS.json').read_text());results=summ['runs']
 assert len(results)==10 and summ['cohort']=={'dev':[17718001],'validation':[17718002],'holdout':[17718011,17718012,17718013]}
 verified=[]
 for row in results:
  db=ROOT/'evidence'/row['db'];r=audit.audit(db)
  assert r['seed']==row['seed'] and r['policy']==row['policy'] and r['commits']==row['commits'] and r['attacks']==row['attacks']
  assert r['HP_final']==row['HP_final'] and r['PA_final']==row['PA_final']
  verified.append(r)
 assert sum(x['commits'] for x in verified)==212
 assert sum(x['native_events'] for x in verified)==616
 assert sum(x['attacks'] for x in verified)==202
 assert all(x['winner']=='LEVIATHAN' for x in verified)
 assert len({(r['seed'],r['policy']) for r in verified})==10
 assert len({r['seed'] for r in verified})==5
 csv_path=ROOT/'evidence'/'R185_DMG_TRANSFERRABLE_OFFENSIVE_RECEIPTS.csv'
 with csv_path.open(newline='') as f:csv_rows=list(csv.DictReader(f))
 assert len(csv_rows)==202 and len({(x['run_db'],x['tx_seq']) for x in csv_rows})==202
 summary=json.loads((ROOT/'evidence'/'R184_RESEARCH_SUMMARY.json').read_text())
 assert summary['holdout_summary']['n']==3 and summary['holdout_summary']['rounds_extended']==2 and summary['holdout_summary']['winners_changed']==0
 assert summary['holdout_summary']['observed_extra_damage_from_additional_turns']==[34,26,42]
 numeric=json.loads((ROOT/'evidence'/'R178_NUMERIC_RANGE_TESTS.json').read_text())
 assert len(numeric['admitted_preflight'])==2 and len(numeric['rejected_preflight'])==4
 assert [x['source_max_m'] for x in numeric['admitted_preflight']]==[80,30]
 assert [x['experiment_distance_m'] for x in numeric['rejected_preflight']]==[81,31,20,20]
 range_db=ROOT/'evidence'/'R178_NUMERIC_SOURCE_RANGE_PREFLIGHT_ONLY.sqlite';conn=sqlite3.connect(range_db)
 rr=dict(conn.execute('SELECT key,value FROM meta'));rangestate=json.loads(rr['state']);event=list(conn.execute('SELECT row_json,row_sha FROM events'));pend=list(conn.execute('SELECT * FROM pending'));conn.close()
 assert len(event)==1 and not pend and int(rr['revision'])==1
 assert rangestate['range_preflight']['sample_m']==60 and rangestate['range_preflight']['admitted_action']==False
 assert SHA(json.loads(event[0][0]))==event[0][1]
 negs=list((ROOT/'negative_cases').glob('R183_FORGERY_*.sqlite'));assert len(negs)==10
 excluded=[]
 for db in negs:
  try:audit.audit(db)
  except (AssertionError,ValueError,TypeError,KeyError,sqlite3.Error):excluded.append(db.name)
  else:raise AssertionError('SEMANTIC_SQL_FORGERY_ACCEPTED:'+db.name)
 assert len(excluded)==10
 adv=json.loads((ROOT/'evidence'/'R183_ADVERSARIAL.json').read_text());assert len(adv['clones'])==10
 faults=json.loads((ROOT/'evidence'/'R183_CRASH_ISOLATION.json').read_text());assert len(faults['records'])==2
 banks=[]
 for name,pending_expected,revision in [('AFTER_INTENT',1,0),('AFTER_COMMIT',0,1)]:
  conn=sqlite3.connect(ROOT/'evidence'/f'R183_FAULT_NEW_{name}.sqlite');md=dict(conn.execute('SELECT key,value FROM meta'));n=conn.execute('SELECT COUNT(*) FROM pending').fetchone()[0];rows=conn.execute('SELECT COUNT(*) FROM events').fetchone()[0];conn.close()
  assert n==pending_expected and int(md['revision'])==revision and rows==revision
  assert json.loads(md['state'])['phase']==('INIT' if name=='AFTER_INTENT' else 'ACTIVE')
  banks.append({'failure':name,'pending':n,'commits':revision})
 source=json.loads((ROOT/'source'/'R177_INITIATIVE_SOURCE_MATRIX.json').read_text());assert len(source['R177_initiative_matrix'])==8 and source['exact_named_bestial_initiative_from_six_consulted']==0
 out={'result':'PASS_R186_COLD_PORTABLE_RECOVERY','files_sha256_ok':len(manifest['files']),'r176_baseline_sha':BASE_SHA,'r176_zip_entries':298,'source_beast_initiative_named':0,'source_beast_denominator':6,'combat_databases':len(verified),'combat_sql_commits':212,'native_events':616,'offensive_receipts':202,'preflight_range_admitted':2,'preflight_range_rejected':4,'preflight_R18_commits':1,'semantic_forged_clones_rejected':len(excluded),'fault_banks':banks,'holdout_seeds':3,'official_benchmarks':0,'original_contracts_terminal':0,'original_contracts_denominator':17,'no_rerun_of_attacks':True,'no_production_writer':True}
 return out
if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
