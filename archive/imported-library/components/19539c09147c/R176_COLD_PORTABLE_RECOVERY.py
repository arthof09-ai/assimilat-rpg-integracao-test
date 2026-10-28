"""Portable read-only R176 recovery: verifies manifest, pins, bank and adversarial clones.
No simulation commands, no replay of historical effects, no Notion/Party writes.
Usage: python R176_COLD_PORTABLE_RECOVERY.py EXTRACTED_R176_DIRECTORY [OUTPUT_RECEIPT.json]
"""
import pathlib,hashlib,json,sys,subprocess

def digest(path):return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
def verify(root,receipt=None):
 root=pathlib.Path(root).resolve()
 manifest=json.loads((root/'R176_SHA256_MANIFEST.json').read_text())
 files=manifest['files'];assert len(files)>12
 for f in files:
  q=root/f['path'];assert q.is_file() and q.stat().st_size==f['size'] and digest(q)==f['sha256'],f['path']
 assert digest(root/'baseline/R175_BASELINE_EXACT.zip')=='661949d6b896051d580df62dd32f94461d7ca415b820a1b2d65e41e25622207f'
 pins=json.loads((root/'R176_RUNTIME_PINS.json').read_text())
 for pin in pins['pins']:assert digest(root/pin['path'])==pin['sha256']
 prereg=json.loads((root/'R176_PREREGISTRATION.json').read_text())
 assert prereg['seed']==1760101 and prereg['experiment']=='R176-AUREN-GRIFFIN-INIT_RANGE_CONTACT'
 src=json.loads((root/'sources/R176_SOURCE_ADMISSIBILITY.json').read_text())
 assert src['admissibility']['full_source_admission']=='HOLD'
 cross=json.loads((root/'R176_17_CONTRACT_CROSSWALK.json').read_text())
 assert len(cross['rows'])==17 and cross['R176_terminals']==0 and cross['official_cells']['after']==0
 local=root/'evidence/R176_AUREN_GRIFFIN_INIT_BOUNDED_DEV1760101.sqlite'
 script=root/'code/r176_independent_scientific_audit.py'
 out=subprocess.run([sys.executable,str(script),str(local)],capture_output=True,text=True,check=True,timeout=25)
 data=json.loads(out.stdout)
 assert data['result']=='PASS_R176_SOURCE_BOUNDED_CAUSAL_REPLAY'
 assert data['commits']==52 and data['native_events']==153 and data['metric']['attempts']==51
 assert data['metric']['hp_loss']==4315 and data['metric']['overkill']==143
 bad=[]
 for path in sorted((root/'evidence/negative_cases').glob('*.sqlite')):
  proc=subprocess.run([sys.executable,str(script),str(path)],capture_output=True,text=True,timeout=25)
  assert proc.returncode!=0,'TAMPER_BYPASSED:'+path.name
  bad.append(path.name)
 assert len(bad)==5
 report={'verdict':'PASS_R176_COLD_PORTABLE_RECOVERY','file_hashes':len(files),'baseline_R175_untouched':True,'runtime_pins':len(pins['pins']),
         'legit_db':1,'commits':data['commits'],'native_events':data['native_events'],'attacks':data['metric']['attempts'],
         'hp_removed':data['metric']['hp_loss'],'overkill':data['metric']['overkill'],'initiative':data['initiative'],
         'rejected_tampered_sql_clones':bad,'source_full_admissibility':'HOLD','terminal_contracts':'0/17','official_benchmarks':'0/1875',
         'does_not_rerun_battles':True,'writer_not_claimed':True}
 if receipt:pathlib.Path(receipt).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 return report
if __name__=='__main__':
 print(json.dumps(verify(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else None),ensure_ascii=False,indent=2))
