"""Produce deterministic R19 capability & snapshot admission evidence. NO Notion writes."""
from __future__ import annotations
from pathlib import Path
import sys,json,hashlib,copy
from native_tree_gate_r19 import (
    MCP_OBSERVATION, FIXTURES, tool_gap_report, admission_gate,
    native_differential_proof, native_restoration_proof)


def run(output: str | Path):
    output=Path(output)
    if output.exists() and any(output.iterdir()):
        raise ValueError('Refusing to overwrite old evidence')
    output.mkdir(parents=True,exist_ok=True)
    base=tool_gap_report()
    base['notion_fixture_count']=len(FIXTURES)
    base['target_native_pages']=2
    base['verified_native_pages']=0
    base['source']='tool declaration and live Notion fetch of 5 fixture pages; not block-tree dump'
    state={kind:dict(info) for kind,info in FIXTURES.items()}
    state['CAOSTIK']={'page_id':'3f4c2b32-4ede-814d-90e7-e462b05ecbd2','R09-TRANSFORM-ACTIVE':'ACTIVE_AND_SAVE_4_RENDERED_OCCURRENCES','pre_R09_independent':False}
    state['EMEF']={'page_id':'3f4c2b32-4ede-8140-bdb6-c2a74789d7f1','R09-TRANSFORM-ACTIVE':'ACTIVE_AND_SAVE_4_RENDERED_OCCURRENCES','pre_R09_independent':False}
    state['HISTORICAL_MODEL']={'page_id':'3f4c2b32-4ede-81fc-8ad5-d2010f27d865','native_writes':0,'pre_R09_independent':None}
    blocker=admission_gate(MCP_OBSERVATION)
    for name,data in [('R19_TOOL_CAPABILITIES.json',MCP_OBSERVATION),('R19_STRUCTURAL_MATRIX.json',base),('R19_FIXTURE_READBACK_STATE.json',state),('R19_NATIVE_CANARY_ADMISSION.json',blocker)]:
        (output/name).write_text(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf8')
    return {'preflight':'BLOCKED_WITH_SPECIFIC_OPERATIONS','native_pages':0,'total':2,'report_files':4,
            'blocked_operations':len(base['missing_verified_operations'])}

if __name__=='__main__':
    path=sys.argv[1] if len(sys.argv)>1 else 'R19_PREFLIGHT_OUTPUT'
    print(json.dumps(run(path),indent=2))
