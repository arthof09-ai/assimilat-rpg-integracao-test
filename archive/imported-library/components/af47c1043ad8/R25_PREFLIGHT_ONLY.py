"""Evidence-only preflight for CM-000001 R25. NOT a combat engine."""
import json
from pathlib import Path

def blockers(contract):
    return [key for key,value in contract["missing_authorized_scene_fields"].items() if value is None]

def gate(contract):
    failures=blockers(contract)
    return {"admissible_for_operator_review":len(failures)==0,"missing_fields":failures,"real_events":contract["synthetic_arithmetic_only"]["real_events"],"is_combat_engine":False}

if __name__=='__main__':
    p=Path(__file__).resolve().parent/'R25_CONTRATO_PREFLIGHT.json'
    print(json.dumps(gate(json.loads(p.read_text(encoding='utf8'))),indent=2))
