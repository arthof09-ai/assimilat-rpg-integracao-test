"""Patch strictly selected predicate guards in COPY of the authenticated R48/R46.
Does not touch source R40 tree. Fail closed when source drifts.
"""
from pathlib import Path
import hashlib,json,difflib
root=Path(__file__).parent
original=root/'baseline_extracted/R40/R48_ORIGINAL'
lab=root/'native_lab/R48_TEST_EXTENDED'
F='r48_factory.py'
R46='legacy/CRAFT-R47-SANDBOX-I0016/baseline/CRAFT-R46-SANDBOX-I0016/r46_evidence.py'
expected={F:'872dc5bf1e588a9ba6f4c45421a4dddbbe7d261842a4e951fd684bfc374c6801',R46:'c869d80f243b349d817c63bd0c40fc08d7b43c98ce54ec9c91d62cd42c73c85e'}
for name,h in expected.items():
 data=(original/name).read_bytes()
 if hashlib.sha256(data).hexdigest()!=h or (lab/name).read_bytes()!=data:raise AssertionError('UNVERIFIED_OR_CHANGED_SOURCE:'+name)

p=lab/F;s=p.read_text('utf8');old=s
pairs=[
 ("ALLOWED_RECIPES=('SBX-TLI-R44-v1','SBX-MICA-R44-v1')", "HISTORICAL_RECIPES=('SBX-TLI-R44-v1','SBX-MICA-R44-v1')\nALLOWED_RECIPES=HISTORICAL_RECIPES  # original R48 historical set remains unchanged\nPINGENTE_TEST='SBX-VIGILIA-BOREAL-R48-TEST-v1'\nPINGENTE_CASE='LAB-CRAFT-VIGILIA-BOREAL-20261020-001'"),
 ("    if type(item) is not dict or set(item)!={'order_id','recipe_key','lot_ids','measurements','tools','skills','report','attestation'}:\n        raise FactoryError('ORDER_CONTRACT_INVALID')", "    baseline={'order_id','recipe_key','lot_ids','measurements','tools','skills','report','attestation'}\n    is_pingente=type(item) is dict and item.get('recipe_key')=='SBX-VIGILIA-BOREAL-R48-TEST-v1'\n    needed=baseline|({'experimental_phase','case_id','pa_envelope_sha256','pa_livre_fixture'} if is_pingente else set())\n    if type(item) is not dict or set(item)!=needed:\n        raise FactoryError('ORDER_CONTRACT_INVALID')\n    if is_pingente:\n        if item['case_id']!=PINGENTE_CASE or item['experimental_phase'] not in ('STRUCTURAL_TEST','MAGIC_TEST'):\n            raise FactoryError('PINGENTE_CASE_OR_PHASE_INVALID')\n        h=item['pa_envelope_sha256']\n        if type(h) is not str or len(h)!=64 or any(ch not in '0123456789abcdef' for ch in h):\n            raise FactoryError('PINGENTE_PA_ENVELOPE_INVALID')\n        from r48_pa_gate import validate_envelope\n        try:verified_pa=validate_envelope(h)\n        except ValueError as exc:raise FactoryError(str(exc)) from exc\n        if type(item['pa_livre_fixture']) is not int or item['pa_livre_fixture']<0:\n            raise FactoryError('PA_LIVRE_FIXTURE_INVALID')\n        if item['experimental_phase']=='MAGIC_TEST' and item['pa_livre_fixture']<verified_pa['pa_por_ativacao']:\n            raise FactoryError('PA_LIVRE_INSUFICIENTE_TEST')"),
 ("        if set(recipes)!=set(ALLOWED_RECIPES):raise FactoryError('EXACTLY_TWO_EXISTING_RECIPES')", "        if set(recipes) not in (set(HISTORICAL_RECIPES),set(HISTORICAL_RECIPES)|{PINGENTE_TEST}):\n            raise FactoryError('HISTORICAL_RECIPES_OR_EXACTLY_ONE_TEST_EXTENSION_REQUIRED')"),
 ("    if item['recipe_key'] not in ALLOWED_RECIPES:\n        raise FactoryError('ONLY_TWO_EXISTING_RECIPES')", "    if item['recipe_key'] not in ALLOWED_RECIPES and item['recipe_key']!=PINGENTE_TEST:\n        raise FactoryError('ONLY_TWO_EXISTING_RECIPES')"),
 ("        for row in orders:_validate_request(row)\n        evidence_ids", "        for row in orders:_validate_request(row)\n        for row in orders:\n            if row['recipe_key']=='SBX-VIGILIA-BOREAL-R48-TEST-v1' and row['experimental_phase']=='MAGIC_TEST':\n                # Native R48 entrypoint, not an external simulation. No magical witness exists.\n                # The original R44 ledger is never allowed to declare magical efficacy.\n                raise FactoryError('MAGIC_TRANSFER_NOT_DEMONSTRATED')\n        evidence_ids")]
for a,b in pairs:
 if s.count(a)!=1:raise AssertionError('PATCH_F48_PREDICATE_MATCH_'+str(s.count(a))+':'+a[:50])
 s=s.replace(a,b)
p.write_text(s,'utf8')
import shutil
shutil.copy2(root/'r48_pa_gate.py', lab/'r48_pa_gate.py')
shutil.copy2(root/'R39_PINGENTE_ENVELOPE_NATIVE.json', lab/'R39_PINGENTE_ENVELOPE_NATIVE.json')

p=lab/R46;s=p.read_text('utf8');old46=s
pairs2=[
 ("        if len(self.recipes)!=2 or set(self.recipes)!={'SBX-TLI-R44-v1','SBX-MICA-R44-v1'}:\n            raise EvidenceError('ONLY_TWO_HISTORICAL_RECIPES')", "        historical={'SBX-TLI-R44-v1','SBX-MICA-R44-v1'}\n        allowed=historical|{'SBX-VIGILIA-BOREAL-R48-TEST-v1'}\n        if set(self.recipes) not in (historical,allowed):\n            raise EvidenceError('HISTORICAL_OR_SINGLE_TEST_RECIPE_ONLY')"),
 ("'RECIPE_NOT_IN_TWO_MODELS'", "'RECIPE_NOT_REGISTERED_IN_TEST_VAULT'")]
for a,b in pairs2:
 if s.count(a)!=1:raise AssertionError('PATCH_R46_PREDICATE_MATCH_'+str(s.count(a)))
 s=s.replace(a,b)
p.write_text(s,'utf8')
(root/'R48_TEST_DIFF.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True), (lab/F).read_text().splitlines(True),fromfile='R48_ORIGINAL/r48_factory.py',tofile='R48_TEST_EXTENDED/r48_factory.py'))+'\n'+''.join(difflib.unified_diff(old46.splitlines(True), (lab/R46).read_text().splitlines(True),fromfile='R48_ORIGINAL/'+R46,tofile='R48_TEST_EXTENDED/'+R46)),encoding='utf8')
print(json.dumps({'patched_files':2,'original_sha':expected,'new_sha':{x:hashlib.sha256((lab/x).read_bytes()).hexdigest() for x in expected},'diff':str(root/'R48_TEST_DIFF.patch')},indent=2))
