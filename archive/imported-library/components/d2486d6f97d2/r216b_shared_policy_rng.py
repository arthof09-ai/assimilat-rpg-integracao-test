"""R216B new registered arms, common random streams only for matched spell/heal action tags.
The underlying actions and native reducers remain identical to R216; no historical seeds reused.
"""
import json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
import r216_dynamic_multi_actor as b
PB=(ROOT/'sources/R216B_FAIR_POLICY_PREREG.json').read_bytes();P=json.loads(PB)
pre=dict(b.PR);pre['run_seeds']=P['seed_pairs'];pre['registered_substudy']='R216B-COMMON-ACTION-RNG';pre['prereg_document_sha256']=hashlib.sha256(PB).hexdigest()
b.PR=pre;b.PH=hashlib.sha256(json.dumps(pre,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
_original_spores=b.safe_spores
_original_heal=b.standard_heal

def normalized_spores(scene,seed,tag):
 for k in P['policies']:tag=tag.replace('-'+k,'-MATCHED')
 return _original_spores(scene,seed,tag)
def normalized_heal(scene,seed,tag):
 for k in P['policies']:tag=tag.replace('-'+k,'-MATCHED')
 return _original_heal(scene,seed,tag)
b.safe_spores=normalized_spores;b.standard_heal=normalized_heal

def main():
 r=[];hold=[]
 for seed in P['seed_pairs']:
  for policy in P['policies']:
   try:r.append(b.execute(seed,policy,'TEAM_A'))
   except Exception as e:hold.append({'seed':seed,'policy':policy,'error':repr(e)})
 obj={'substudy':'R216B-COMMON-RNG', 'accepted':r,'blocked':hold,'paired_complete_seeds':[seed for seed in P['seed_pairs'] if sum(x['seed']==seed for x in r)==2]}
 (ROOT/'evidence/reports/R216B_FAIR_POLICY_RESULTS.json').write_text(json.dumps(obj,indent=2,ensure_ascii=False))
 print(json.dumps({'admitted':len(r),'holds':hold,'complete_pairs':obj['paired_complete_seeds'],'commits':sum(x['commits'] for x in r)},indent=2))
if __name__=='__main__':main()
