#!/usr/bin/env python3
"""R210 read-only cold recovery; does not load combat motor or reexecute any fight."""
from pathlib import Path
import json,hashlib,sys,zipfile,importlib.util
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST_SHA256.json').read_text())
for rel,hash_expected in manifest['files'].items():
 p=root/rel
 assert p.exists() and p.is_file(),('MISSING',rel)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==hash_expected,('BAD_SHA',rel)
with zipfile.ZipFile(root/'baseline/R209/VLAB_R209_SPORES_MULTITARGET_COLD_AUDITED_MESTRE_ONLY.zip') as z:assert z.testzip() is None
spec=importlib.util.spec_from_file_location('r210independent',root/'new/r210/code/r210_independent_sqlite_readonly_audit.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
files=sorted((root/'new/r210/evidence/db').glob('R210_CENTER_SPORES_S*.sqlite'))
assert len(files)==10
found=[mod.audit(p) for p in files]
expected={'commits':448,'events':1566,'attacks':292,'casts':98,'target_events':244,'PA_spent':7840,'magic_effective':15036,'self_damage':2950,'beast_damage':12086}
for k,v in expected.items():assert sum(x[k] for x in found)==v,(k,v)
r=json.loads((root/'new/r210/evidence/R210_INDEPENDENT_AUDIT.json').read_text())
assert r['audit']=='PASS_R210_INDEPENDENT_R18_TWO_CENTERS_GEOMETRY_CAUSAL_PAIRING' and r['totals']==expected
assert len({x['seed'] for x in found})==5 and r['blocked_precommit_arms']==2
print(json.dumps({'result':'PASS_R210_COLD_PORTABLE_RECOVERY','manifest_sha_files':len(manifest['files']),'db':len(files),'commits':448,'events':1566,'casts':98,'targets':244,'fight_reexecutions':0,'production':'HOLD'},indent=2))
