"""Verify archived VLAB Stage10/Stage12 SOURCE documents without claiming 17/17.

Original 2.57/2.67 MB ZIPs and 688/718 member hashes were checked locally;
only two exact JSON source snapshots are copied into GitHub for lightweight CI.
This verifier does NOT re-run all historical Stage10/Stage12 engines.
"""
from pathlib import Path
import base64
import hashlib
import json
import lzma
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]/'experiments/vlab_historical_provenance'
PINS={
 10:('stage10_source.json.xz.b64','e74a45cdd2f7d2b70d0e576f3a519a3c311dccf097a6944b04cd61898e70d1fb'),
 12:('stage12_matrix.json.xz.b64','1c1f02e0de5393a81401752757276237b93ed8b32239024c59eccd62991d0c8f'),
}
ARCHIVE_LOCAL_RECEIPTS={
 'stage10':{'sha256':'77b1d2e973f4c2cddf5741c74f9263a0c652885201571d645a5b799095a26979',
            'zip_members':689,'member_sha256_checked':688},
 'stage12':{'sha256':'17342b3377ac6f04c961388d87188fa48029c2e713e9eb9a9aae101ebf170772',
            'zip_members':719,'member_sha256_checked':718},
 'stage10_members_preserved_in_stage12':689,'new_members_stage12':30,
 'full_archive_sha256_recomputed_in_github':False,
}


def source(stage):
    name,pin=PINS[stage]
    original=lzma.decompress(base64.b64decode((ROOT/name).read_text().strip(),validate=True))
    if hashlib.sha256(original).hexdigest()!=pin:
        raise AssertionError('STAGE_SOURCE_SHA256_MISMATCH:'+str(stage))
    return json.loads(original)


def validate_docs(stage10,stage12):
    if stage10['id']!='OP-VLAB-FUSION-SANDBOX-01/STAGE10/C1-SOURCE-MATRIX':
        raise AssertionError('STAGE10_ID_MISMATCH')
    if (len(stage10['conflicts'])!=8 or stage10['strict_eligible'] is not False
        or stage10['all_fields_in_claims_are_documentary_only'] is not True
        or stage10['official_duels']!=0 or stage10['canonical_credits']!=0
        or stage10['global_progress']!='NOT_DETERMINABLE'):
        raise AssertionError('STAGE10_SOURCE_AUTHORITY_HOLD_CHANGED')
    if (stage12['id']!='STAGE12_FUSION_FUNCTIONAL_ACCEPTANCE_MATRIX'
        or stage12['contracts_total']!=17 or len(stage12['rows'])!=17
        or stage12['terminal_acceptance']!=0
        or stage12['incomplete_or_blocked']!=14
        or stage12['nac_pass_02']!='HOLD'
        or stage12['single_canonical_fight_engine'] is not False
        or stage12['technical_full_fusion_complete'] is not False
        or stage12['bushi_wang_current_source_freeze'] is not False
        or stage12['v09_historical_binary_available'] is not False
        or stage12['canonical_duels']!=0
        or any(r.get('terminal_certified') is not False for r in stage12['rows'])):
        raise AssertionError('STAGE12_17_CONTRACTS_NOT_CERTIFIED_GATE_CHANGED')
    statuses=Counter(r['candidate_capability'] for r in stage12['rows'])
    if statuses!={'BLOCKED':3,'PARTIAL':11,'REBUILT_TEST_ONLY':3}:
        raise AssertionError('STAGE12_CANDIDATE_CLASSES_CHANGED')
    return {'stage10_source_conflicts':8,'stage12_contracts':17,
      'stage12_terminal_approved':0,'stage12_blocked':3,'stage12_partial':11,
      'stage12_bounded_rebuilt_test_only':3,'strict_execution':'HOLD'}


def main():
    values=validate_docs(source(10),source(12))
    result={'status':'PASS_ORIGINAL_SOURCE_PROVENANCE_DOCUMENTARY_TEST_ONLY',
            'stage10_source_sha256':PINS[10][1],
            'stage12_matrix_sha256':PINS[12][1],
            'archive_integrity_evidence':ARCHIVE_LOCAL_RECEIPTS,
            'full_stage10_stage12_runtime_in_github':'NOT_EXECUTED',
            'writer':'DENY','canon':'HOLD','party_writes':0}
    result.update(values)
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
