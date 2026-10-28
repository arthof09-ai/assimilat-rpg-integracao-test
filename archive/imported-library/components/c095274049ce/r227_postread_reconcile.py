#!/usr/bin/env python3
"""Read-only post-publication row-level aggregate. No engine imports. Historical batches not reexecuted."""
import pathlib,json,hashlib
p=pathlib.Path(__file__).with_name('R227_EXECUTION_RESULTS_FROZEN.json')
r=json.loads(p.read_text(encoding='utf-8'))
rows=r['runs'];pairs=r['pairs']
assert len(rows)==12 and len(pairs)==6
assert len(set((r['seed'],r['arm']) for r in rows))==len(rows)
assert len({r['seed'] for r in rows})==6
assert sum(x['commits'] for x in rows)==24
assert sum(x['events'] for x in rows)==132
assert all(x['source_window_censored'] for x in rows)
assert sum(x['item_pa_spent'] for x in rows)==176
assert sum(int(x['hit']) for x in pairs)==4
assert sum(x['magic_net_RD0'] for x in pairs)==100
assert sum(x['magic_net_RD100'] for x in pairs)==0
assert sum(int(x['slow_RD0']) for x in pairs)==4
assert sum(int(x['slow_RD100']) for x in pairs)==0
assert all(x['item_PA_spent'] in (0,22) for x in pairs)
# Exposes reporting-only typo in original R227 runner's final print: x['item_pa_spent_each_arm'] vs x['item_PA_spent']
summary={'status':'PASS_R227_POSTREAD_COUNTS_UNCHANGED','runs':len(rows),'paired_seeds':len(pairs),'commits':24,'events':132,
  'physical_hits_across_pairs':4,'magic_effective_rd0':100,'magic_effective_rd100':0,
  'total_item_pa_both_arms':176,'slow_rd0':4,'slow_rd100':0,
  'runner_print_typo':'item_pa_spent_each_arm -> item_PA_spent, reporting stage only, executed evidence already frozen',
  'replayed_combats':0,'frozen_report_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
print(json.dumps(summary,indent=2,ensure_ascii=False))
