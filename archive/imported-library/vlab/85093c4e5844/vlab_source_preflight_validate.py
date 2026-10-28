import json
from pathlib import Path
p=Path(__file__).with_name('vlab_source_preflight_readonly_v01.json')
d=json.loads(p.read_text(encoding='utf-8'))
ss=d['sources']
checks={
 'unique_provisional_ids':len(set(x['provisional_action_id'] for x in ss))==len(ss),
 'unique_source_id_pairs':len(set((x['source_page_id'],x['name']) for x in ss))==len(ss),
 'none_full_fight':all(x['eligibility']!='FULL-FIGHT' for x in ss),
 'none_frozen':all(x['source_fingerprint'] is None for x in ss),
 'none_adapter':all(x['effect_adapter'] is None for x in ss),
 'binary_unavailable':d['code_binary_status']=='BINARY-UNAVAILABLE',
 'no_claim_writer':d['writer'] is None and d['instance_id'] is None,
 'all_have_blockers':all(x['blockers'] for x in ss),
 'all_source_urls':all(x['source_url'].startswith('https://app.notion.com/p/') for x in ss),
 'math_damage_example':next(x for x in ss if x['name'].startswith('Bola de Fogo'))['damage_mean']==7.5
}
for k,v in checks.items(): print(f'{k}: {"PASS" if v else "FAIL"}')
print(f'PREFLIGHT TESTS: {sum(checks.values())}/{len(checks)} PASS; SOURCES: {len(ss)}; FULL-FIGHT ELIGIBLE: {sum(x["eligibility"]=="FULL-FIGHT" for x in ss)}')
if not all(checks.values()): raise SystemExit(1)
