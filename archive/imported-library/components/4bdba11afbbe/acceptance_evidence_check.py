"""Check completeness of submitted enforcement evidence. Never certify GREEN.

Input is untrusted and may be fabricated. This is a pre-audit filter, not a
proof of permission revocation or Notion access controls.
"""
import json
import sys
from pathlib import Path

REQUIRED=[
 'protected_scope_inventory', 'credential_inventory', 'dedicated_gateway_credential',
 'legacy_api_direct_write_denied', 'legacy_notion_ui_edit_denied',
 'legacy_automations_denied', 'legacy_inherited_child_write_denied',
 'old_writer_token_denied', 'concurrent_one_winner',
 'external_failure_unknown_effect_quarantined', 'recovery_readback_verified',
 'independent_auditor_review', 'destination_ack_recorded',
]

def assess(doc):
    if not isinstance(doc,dict) or doc.get('scope')!='OP-VLAB-FUSION-SANDBOX-01:ENGINEERING-DOCS':
        return {'result':'HOLD','missing':['AUTHORIZED_SCOPE']}
    assertions=doc.get('assertions',{})
    missing=[]
    for key in REQUIRED:
        item=assertions.get(key)
        if not isinstance(item,dict) or item.get('observed') is not True or not isinstance(item.get('evidence_ref'),str) or len(item['evidence_ref'])<12:
            missing.append(key)
    return {'result':'HOLD' if missing else 'READY_FOR_INDEPENDENT_REVIEW_NOT_GREEN',
            'missing':missing,'assertions_present':len(REQUIRED)-len(missing),
            'required':len(REQUIRED),'live_notion_fencing':'NOT_CERTIFIED_BY_THIS_TOOL'}

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: acceptance_evidence_check.py evidence.json')
    x=assess(json.loads(Path(sys.argv[1]).read_text()))
    print(json.dumps(x,indent=2,ensure_ascii=False))
    sys.exit(0 if not x['missing'] else 2)
