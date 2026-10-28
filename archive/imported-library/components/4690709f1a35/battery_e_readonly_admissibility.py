#!/usr/bin/env python3
"""R227 Bateria E source-status admission audit (no combat imports, no writes to source)."""
import json, hashlib, pathlib, copy
p=pathlib.Path(__file__).with_name('BATERIA_E_CANDIDATES_SOURCE_GATE.json')
s=json.loads(p.read_text(encoding='utf-8'))
assert s['ready_for_official_cell_count']==0
assert s['official_matrix_homologated']==0
assert s['terminal_contracts_homologated']==0
assert len(s['source_candidates'])==3

def admit(c):
    return (c['canonical_item_status_verified'] is True
            and c['physical_chassis_separable'] is True
            and c['magic_component_separable'] is True
            and c['source_complete_equipped_user_geometry'] is True
            and c['party_side_source'] is False
            and c['mechanical_test_audited'] is True)

assert all(not admit(c) for c in s['source_candidates'])
# In the frozen evidence, deliberately false attempted promotion of just one field never passes.
for i,c in enumerate(s['source_candidates']):
    for field in ['canonical_item_status_verified','physical_chassis_separable',
                  'magic_component_separable','source_complete_equipped_user_geometry',
                  'party_side_source','mechanical_test_audited']:
        bad=copy.deepcopy(c)
        bad[field]=False if field=='party_side_source' else True
        if bad!=c:
            assert not admit(bad), (i,field)

sha=hashlib.sha256(p.read_bytes()).hexdigest()
result={"status":"PASS_R227_BATTERY_E_READONLY_SOURCE_ELIGIBILITY_GATES",
        "source_rows":3,"official_admitted":0,"test_only":1,
        "not_test_admissible":2,"no_canon_promotions":True,
        "classification":"mechanical sourced candidates; not complete canonical item acceptance",
        "source_gate_sha256":sha}
print(json.dumps(result,indent=2,ensure_ascii=False))
