"""IBX17 replay of already existing synthetic R213 history for Level Up/Down lengths 1,2,3,5,10.
READONLY local; no Notion writes, no historic Party inference, no new choices/rolls.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LEDGER=ROOT.parent/'delta/R213_HOLDOUT_SYNTHETIC_LEDGER_L0_TO17.json'
data=json.loads(LEDGER.read_text(encoding='utf8'));S={s['level']:s for s in data['history']}
ATTRS=['FOR','DES','CON','INT','SAB','CAR']
D=[1,2,3,5,10]

def replay(start,stop):
 assert start in S and stop in S and start!=stop
 a,b=S[start],S[stop]
 changes={k:b['natural_attrs'][k]-a['natural_attrs'][k] for k in ATTRS}
 amp=1 if stop>start else -1
 rank_changes=[]
 for lvl in range(start+amp,stop+amp,amp):
  if S[lvl]['rank'] != S[lvl-amp]['rank']:
   rank_changes.append({'at_level':lvl,'from':S[lvl-amp]['rank'],'to':S[lvl]['rank'],'kind':'NATURAL_RANK_REBASE_POSSIBLE'})
 expected_sum=2*(stop-start)
 assert sum(changes.values())==expected_sum
 hp=a['hp_current'];pa=a['pa_current'];hpm=b['hp_max'];pam=b['pa_max']
 limit={'HP_CURRENT_EXCEEDS_NEW_MAX':bool(hp is not None and hp>hpm),'PA_CURRENT_EXCEEDS_NEW_MAX':bool(pa is not None and pa>pam)}
 out={'scope':'EXISTING_SYNTHETIC_LEDGER_TEST_ONLY','from_level':start,'to_level':stop,'steps':abs(stop-start),'direction':'UP' if stop>start else 'DOWN','attrs_delta':changes,'natural_points_before':a['natural_sum'],'natural_points_after':b['natural_sum'],'point_budget_delta':expected_sum,'HPmax_before':a['hp_max'],'HPmax_after':hpm,'HPmax_delta':hpm-a['hp_max'],'PAmax_before':a['pa_max'],'PAmax_after':pam,'PAmax_delta':pam-a['pa_max'],'FF_before':a['ff'],'FF_after':b['ff'],'FF_delta':b['ff']-a['ff'],'CA_before':a['ca'],'CA_after':b['ca'],'CD_before':a['magic_cd'],'CD_after':b['magic_cd'],'FF_locks_before':a['locks_active'],'FF_locks_active_after':b['locks_active'],'FF_locks_remain_permanent':True,'rank_crossings':rank_changes,'HP_PA_CURRENT_PRESERVATION_GATES':limit,'current_adjustment_authorized':False,'no_party_write':True,'needs_human_new_choices':False,'reused_prior_synthetic_ledger_not_real_party':True,'rank_rebase_mode':'ALREADY_INCLUDED_IN_VERIFIED_SYNTHETIC_SNAPSHOTS','item_properties_unchanged':True,'history_written_to_party':False}
 return out

if __name__=='__main__':
 import hashlib
 res=[]
 for n in D:
  # 17->17-n, including levels crossing rank boundary
  res.append(replay(17,17-n))
  # 7->7+n; n=10 reaches original 17 fixture and crosses multiple classifications
  res.append(replay(7,7+n))
 # local inverse arithmetic around 7/17, as both boundaries correspond to documented TEST history
 for n in D:
  a=replay(17,17-n)
  rev=replay(17-n,17)
  for f in ['HPmax_delta','PAmax_delta','FF_delta','point_budget_delta']:
   assert a[f]==-rev[f],(n,f)
  assert sum(a['attrs_delta'].values())==-2*n
 assert replay(17,7)['HP_PA_CURRENT_PRESERVATION_GATES']['HP_CURRENT_EXCEEDS_NEW_MAX']
 assert replay(17,7)['HP_PA_CURRENT_PRESERVATION_GATES']['PA_CURRENT_EXCEEDS_NEW_MAX']
 assert len(replay(7,17)['rank_crossings'])==2
 (ROOT/'MATRIZ_10_REPLAY_MULTINIVEL_LEDGER_R213.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'cases':len(res),'forward_7_to_17':replay(7,17),'backward_17_to_7':replay(17,7)},ensure_ascii=False))
