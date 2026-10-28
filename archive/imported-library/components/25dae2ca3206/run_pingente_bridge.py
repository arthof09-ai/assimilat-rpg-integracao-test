"""Read-only command: serialize adapter + discriminators + original-binary gate.
Exact inputs are QA-approved v1.2 and genesis R48 recipe schema recovered in FC04.
No R48 fabrication command is called if original engine cannot be verified.
"""
import json,os
from pathlib import Path
from .r48_pingente_adapter import admission
from .magic_controls import run_deck
BASE=Path(__file__).resolve().parents[1]
FIX=BASE/'fixtures'
OUT=BASE/'outputs'

def main(engine_root:Path):
    recipe=json.loads((FIX/'recipe.json').read_text());pa=json.loads((FIX/'pa_gate.json').read_text());arc=json.loads((FIX/'r48_archived_contract.json').read_text())
    a=admission(recipe,pa,arc,engine_root)
    d=run_deck()
    assert a['status']=='BLOCKED_BEFORE_R48_ORDER' and a['r48_receipt'] is None
    assert d['physical_magic_verified']==0
    OUT.mkdir(exist_ok=True)
    (OUT/'R48_ADMISSION_REPORT.json').write_text(json.dumps(a,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    (OUT/'MAGIC_DISCRIMINATORS.json').write_text(json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    return {'r48_gate':a['status'],'engine_present':a['engine_evidence']['ok'],'admission_block_count':len(a['blocks']),'discriminators':d['count'],'magical_fabrication_proven':False,'receipt_produced':False}
if __name__=='__main__':
    print(json.dumps(main(Path(os.environ.get('CRAFT_R48_ENGINE_ROOT',str(BASE/'baselines/NO_R48_ORIGINAL_BYTES'))) ),indent=2))
