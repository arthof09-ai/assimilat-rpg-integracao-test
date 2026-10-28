"""Read-only AST static inspection of physically recovered historical native v0.8.1."""
import ast,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
source=R.parent/'r61_extracted'/'work'/'working'/'historical_v081_verified_original'/'comestre_vlab'/'vlab_effects_v08.py'
if not source.exists():
    source=R.parent/'historical_requirements'/'vlab_effects_v08.py'
raw=source.read_bytes()
tree=ast.parse(raw)
fns=[x for x in tree.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef)) and x.name=='cast_source_specified_spell']
assert len(fns)==1
fn=fns[0]
rejected=[]
for x in ast.walk(fn):
 if isinstance(x,ast.Raise) and isinstance(x.exc,ast.Call):
  ca=x.exc
  if isinstance(ca.func,ast.Name) and ca.func.id=='EffectBlocked':
   texts=[v.value for v in ca.args if isinstance(v,ast.Constant) and isinstance(v.value,str)]
   if any('rounding of half damage needs source convention' in txt for txt in texts):
    rejected.append({'line':x.lineno,'source':texts[0]})
assert len(rejected)==1
# Show the conditional guard is SAVE-HALF, not another unrelated exception.
parent_lines=source.read_text().splitlines()
line=rejected[0]['line']
assert 'SAVE-HALF' in parent_lines[line-1] or 'SAVE-HALF' in parent_lines[line-2]
result={'status':'PASS_STATIC_NATIVE_GATE_DEMONSTRATED','source_sha256':hashlib.sha256(raw).hexdigest(),'file_label':'original recoverable historical v0.8.1; no file altered','function':'cast_source_specified_spell','blockers':rejected,'conclusion':'Native source rejects SAVE-HALF. R103 is additive narrow transactional proof, NOT native integrated effect proof. No new native spell was executed.','native_tests_executed':0}
(R/'R106_NATIVE_EFFECT_SAVE_HALF_BLOCKER.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
