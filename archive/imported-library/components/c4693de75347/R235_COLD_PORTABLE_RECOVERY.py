"""Source/manifest + independent SQLite audit only. Does not run combat runner."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent
def run():
 manifest=json.loads((ROOT/'SHA256_MANIFEST.json').read_text())['files']
 files={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256_MANIFEST.json' and not p.name.endswith(('-wal','-shm'))}
 assert set(manifest)==files,(len(manifest),len(files),sorted(set(manifest)^files)[:10])
 for name,sha in manifest.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,name
 sys.path.insert(0,str(ROOT/'code'));from r235_independent_readonly_audit import audit
 out=audit(ROOT,write=False);assert out['status']=='PASS_R235_FACTORIAL_SOURCE_GRIFFON_SPELL_NATIVE_CONDITIONAL' and out['counts']['commits']==196
 adv=json.loads((ROOT/'evidence/reports/R235_ADVERSARIAL_REHASH.json').read_text());assert adv['status']=='PASS_R235_INDEPENDENT_ADVERSARIAL_5_OF_5' and all(x['rejected'] for x in adv['cases'])
 print('PASS_R235_PORTABLE_COLD_FACTORIAL_AND_SAVE',len(manifest),'SHA',out['counts']['commits'],'COMMITS',out['counts']['events'],'NATIVE_EVENTS','ZERO_HISTORICAL_REPLAY')
if __name__=='__main__':run()
