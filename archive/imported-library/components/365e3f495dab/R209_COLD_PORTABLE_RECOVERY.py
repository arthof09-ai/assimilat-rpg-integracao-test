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
with zipfile.ZipFile(root/'baseline/R208/VLAB_R208_NATIVE_PULSO_GLOVES_COLD_AUDITED_MESTRE_ONLY.zip') as z:assert z.testzip() is None
path=root/'new/r209/code/r209_spores_independent_sqlite_readonly_audit.py'
spec=importlib.util.spec_from_file_location('r209auditcold',path)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
db=sorted((root/'new/r209/evidence/db').glob('R209_AREA_SPORES_S*.sqlite'))
assert len(db)==6
results=[mod.audit(p) for p in db]
assert all(x['commits']>0 and x['events']>0 for x in results)
a=json.loads((root/'new/r209/evidence/R209_INDEPENDENT_AUDIT.json').read_text())
assert a['audit']=='PASS_R209_INDEPENDENT_R18_MULTITARGET_GEOMETRY_AREA_WITH_CASTER'
assert a['combat_reexecutions_during_audit']==0
print(json.dumps({'result':'PASS_R209_COLD_PORTABLE_RECOVERY','manifest_sha_files':len(manifest['files']),
 'databases':len(db),'commits':sum(x['commits'] for x in results),
 'events':sum(x['events'] for x in results),
 'attacks':sum(x['attacks'] for x in results),'combat_reexecutions':0,
 'production':'HOLD','official_contracts':'0/17','historical_cells':'0/1875'},indent=2))
