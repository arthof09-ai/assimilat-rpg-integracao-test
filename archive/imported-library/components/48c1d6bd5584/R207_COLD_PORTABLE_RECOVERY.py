#!/usr/bin/env python3
"""Read-only portable R207 cold recovery. Never runs any combat executor.
Usage: python R207_COLD_PORTABLE_RECOVERY.py [EXTRACTED_PACKAGE_DIR]
"""
from pathlib import Path
import json,hashlib,zipfile,sqlite3,importlib.util,sys
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST_SHA256.json').read_text())
for relative,expected in manifest['files'].items():
 p=root/relative
 assert p.is_file(),f'MISSING_FILE:{relative}'
 actual=hashlib.sha256(p.read_bytes()).hexdigest()
 assert actual==expected,f'HASH_CONFLICT:{relative}'
for a in [root/'baseline/R206B/VLAB_R206B_TATICA_ADAPTATIVA_COLD_AUDITED_MESTRE_ONLY.zip']:
 with zipfile.ZipFile(a) as z:assert z.testzip() is None
p=root/'new/r207/code/r207_independent_sqlite_readonly_audit.py'
spec=importlib.util.spec_from_file_location('r207_independent_audit_portable',p)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
dbs=sorted((root/'new/r207/evidence/db').glob('R207_TEAM_HEAL_2V1_*.sqlite'))
results=[mod.audit(p) for p in dbs]
assert len(results)==8 and len({x['run_id'] for x in results})==8
base=json.loads((root/'new/r207/evidence/R207_INDEPENDENT_AUDIT.json').read_text())
checks={'commits':sum(x['commits'] for x in results),'events':sum(x['events'] for x in results),'attacks':sum(x['attacks'] for x in results),'heals':sum(x['heals'] for x in results),'heal_pa':sum(x['heal_pa'] for x in results),'heal_effective':sum(x['healing_effective'] for x in results),'KO':sum(x['status']=='KO' for x in results),'censored':sum(x['status']=='CENSORED_HORIZON' for x in results)}
for k,v in checks.items():assert base[k]==v,(k,base[k],v)
expected={'commits':384,'events':1165,'attacks':126,'heals':30,'heal_pa':1350,'heal_effective':750,'KO':1,'censored':7}
assert checks==expected
probe=json.loads((root/'new/r207/evidence/R207_ORC_IBX17_NATIVE_PREVIEW_DIAGNOSTIC.json').read_text())
assert probe['writes']==0 and probe['results'][0]['preview_after']['hp']==37 and probe['results'][0]['target_historical']['hp']==39
assert probe['results'][1]['preview_after'] is None
assert base['combat_reexecutions_during_audit']==0
print(json.dumps({'result':'PASS_R207_COLD_PORTABLE_RECOVERY','hashes':len(manifest['files']),
'databases':len(dbs),**checks,'native_levelup_parity':'HOLD','combat_reexecutions':0},indent=2))
