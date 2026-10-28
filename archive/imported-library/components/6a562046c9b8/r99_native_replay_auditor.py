#!/usr/bin/env python3
"""Portable verifier for IBX17 R99. Does not write Notion.
Use a genuine Notion attachment IBX17_R99_NATIVE_AFTER_AUDIT_20261016.json
exported from original operation. In absence of audit, prints HOLD (not a fake PASS).
"""
import argparse, hashlib, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
SOURCE=HERE/'IBX17_R75_UP_PAYLOAD_COMPACT_20261016.json'

def canon(x): return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def sha(x): return hashlib.sha256(x).hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--audit',type=Path,help='The original R99 native JSON audit attachment downloaded from Notion')
    a=p.parse_args()
    d=json.loads(SOURCE.read_text(encoding='utf8'))
    source_checks={'source_sha256':sha(SOURCE.read_bytes()),'fixture_synthetic':d['fixture_label']=='SYNTHETIC_EXPLICIT_ONLY',
                   'mechanical_event':d['event_id'],'engine':d['engine'],'before_sha256':sha(canon(d['before'])),'after_sha256':sha(canon(d['after']))}
    if a.audit is None:
        print(json.dumps({'contract':'R99','state':'HOLD_NEEDS_PHYSICAL_NOTION_AUDIT','source_checks':source_checks,'notion_write_replayed':False},indent=2,ensure_ascii=False))
        return 2
    q=json.loads(a.audit.read_text(encoding='utf8'))
    checks={
        'audit_has_provider_target':q.get('meta',{}).get('url')=='https://app.notion.com/p/3fbc2b324ede8191a5cdc34c720f2c29',
        'txn_id':q.get('meta',{}).get('tx')=='IBX17-R99-NATIVE-UP-20261016-01',
        'native_state_committed':q.get('meta',{}).get('status')=='COMMITTED_NATIVE_R99_FIELDS_VERIFIED_3_OF_3',
        'native_pre_matches_source':q.get('historical_pre')==d['before'],
        'normal_matches_source':q.get('current_states',{}).get('NORMAL')==d['after']['NORMAL'],
        'transform_matches_source':q.get('current_states',{}).get('TRANSFORM')==d['after']['TRANSFORM'],
        'locks_matches_source':q.get('current_states',{}).get('LOCKS')==d['after']['LOCKS'],
        '20_children_reported':q.get('checks',{}).get('has_20_native_children') is True,
        'test_gate_recorded':q.get('checks',{}).get('test_gate_recorded') is True,
        'production_not_claimed':q.get('limits',{}).get('production_writer') is False,
        'source_bound_not_claimed':q.get('limits',{}).get('real_player_confirmation') is False,
    }
    ok=all(checks.values())
    print(json.dumps({'contract':'R99','state':'PASS_PORTABLE_EVIDENCE_CONSISTENCY' if ok else 'FAIL',
                      'checks':checks,'source_checks':source_checks,'audit_file_sha256':sha(a.audit.read_bytes()),
                      'limitations':'Revalidates exported audit content, not a fresh live Notion state; requires separate live fetch for freshness.'},ensure_ascii=False,indent=2))
    return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
