#!/usr/bin/env python3
"""Read-only cold-recovery; never executes fight runners or changes past records."""
from pathlib import Path
import sys,zipfile,json,hashlib,importlib.util
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST_SHA256.json').read_text())
for rel,known_hash in manifest['files'].items():
 p=root/rel
 assert p.exists(),('MISSING',rel)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==known_hash,('SHA',rel)
with zipfile.ZipFile(root/'baseline/R207/VLAB_R207_REACTIVE_HEAL_NATIVE_COLD_AUDITED_MESTRE_ONLY.zip') as z:assert z.testzip() is None
path=root/'new/r208/code/r208_native_pulso_independent_sqlite_audit.py'
spec=importlib.util.spec_from_file_location('r208auditcold',path)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
db=sorted((root/'new/r208/evidence/db').glob('R208_NATIVE_PULSO_GLOVES_TEAM2V1_*.sqlite'))
assert len(db)==4
results=[mod.audit(p) for p in db]
assert all(x['commits']>0 and x['events']>0 for x in results)
a=json.loads((root/'new/r208/evidence/R208_INDEPENDENT_AUDIT.json').read_text())
assert a['audit']=='PASS_R208_INDEPENDENT_NATIVE_R18_PULSO_GLUVES'
assert a['combat_reexecutions_during_audit']==0
print(json.dumps({'result':'PASS_R208_COLD_PORTABLE_RECOVERY','manifest_sha_files':len(manifest['files']),
 'databases':len(db),'commits':sum(x['commits'] for x in results),
 'events':sum(x['events'] for x in results),
 'attacks':sum(x['attacks'] for x in results),'combat_reexecutions':0,
 'production':'HOLD','official_contracts':'0/17','historical_cells':'0/1875'},indent=2))
