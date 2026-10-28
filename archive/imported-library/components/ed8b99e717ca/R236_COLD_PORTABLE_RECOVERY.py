"""R236 portable cold verifier with independent read-only SQL, no fight replay."""
from pathlib import Path
import json,hashlib,sys
R=Path(__file__).resolve().parent
def run():
 m=json.loads((R/'SHA256_MANIFEST.json').read_text())['files']
 files={p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256_MANIFEST.json' and not p.name.endswith(('-shm','-wal'))}
 assert set(m)==files,(len(m),len(files),sorted(set(m)^files)[:20])
 for name,h in m.items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==h,name
 sys.path.insert(0,str(R/'code'));from r236_independent_readonly_audit import audit
 v=audit(R,write=False);assert v['status']=='PASS_R236_FRACO_WEAK_HP0_INTERRUPT_NATIVE_CONDITIONAL' and v['counts']['commits']==59 and v['counts']['blocked_future_turns']==121
 q=json.loads((R/'evidence/reports/R236_ADVERSARIAL_REHASH.json').read_text());assert q['status']=='PASS_R236_ADVERSARIAL_REHASH_5_OF_5' and all(z['rejected'] for z in q['cases'])
 print('PASS_R236_PORTABLE_COLD_WEAK_HP0',len(m),'hashes',v['counts']['arms'],'arms',v['counts']['commits'],'commits',v['counts']['native_events'],'native events')
if __name__=='__main__':run()
