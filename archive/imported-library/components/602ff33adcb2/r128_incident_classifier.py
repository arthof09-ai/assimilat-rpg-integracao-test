"""R128: causal disposition of historical partial effects. Safety-biased.
This module DOES NOT reconstruct a native write receipt from state equivalence.
"""
from __future__ import annotations
from dataclasses import dataclass
import json
@dataclass
class Incident:
 name:str;target:str;version:str;group:str;physical:str;journal:str
 expected_receipt_matches:bool;native_causal_response_present:bool
 immutable_source_present:bool;pre_version_authentic:bool
 independent_audit_object_present:bool;write_source_identity_bound:bool
 def decide(self):
  if self.physical not in ('BEFORE','AFTER') or self.journal not in ('PREPARED','COMMITTED'):
   return {'status':'UNKNOWN_EFFECT','writeset':[],'reason':'unclassified native state'}
  if self.journal=='COMMITTED' and self.physical=='BEFORE':return {'status':'HOLD_JOURNAL_AHEAD','writeset':[]}
  if self.physical=='AFTER' and self.journal=='COMMITTED':return {'status':'GROUP_CONSUMED_NOOP','writeset':[]}
  if self.physical=='BEFORE' and self.journal=='PREPARED':return {'status':'PRE_NOT_APPLIED_NOOP','writeset':[]}
  missing=[]
  for field in ('expected_receipt_matches','native_causal_response_present','immutable_source_present','pre_version_authentic','independent_audit_object_present','write_source_identity_bound'):
   if not getattr(self,field):missing.append(field)
  if missing:return {'status':'HOLD_CAUSAL_REPAIR_NOT_AUTHORIZED','writeset':[],'missing_evidence':missing,'reason':'AFTER != causal proof; no journal repair'}
  return {'status':'REVIEWABLE_JOURNAL_REPAIR_CANDIDATE_NOT_AUTOMATIC','writeset':['JOURNAL_'+self.group],'reason':'pending fresh version/authority and external reviewer certification'}

def cases():
 return [Incident('R110_TRANSFORM','3fcc2b324ede81aab6d5df4f337ce936','2026-10-17T01:32:19.191Z','TRANSFORM','AFTER','PREPARED',True,False,True,False,False,False),
 Incident('R121_F_EQUIP_OFF','3fcc2b324ede81eba833c01224eda5fb','2026-10-17T11:16:09.900Z','F','AFTER','PREPARED',True,False,True,False,False,False)]

def tests():
 out={i.name:i.decide() for i in cases()}
 assert all(v['status']=='HOLD_CAUSAL_REPAIR_NOT_AUTHORIZED' and v['writeset']==[] for v in out.values())
 assert 'native_causal_response_present' in out['R110_TRANSFORM']['missing_evidence']
 assert 'pre_version_authentic' in out['R121_F_EQUIP_OFF']['missing_evidence']
 assert Incident('positive','ID','v','NORMAL','AFTER','COMMITTED',True,True,True,True,True,True).decide()['status']=='GROUP_CONSUMED_NOOP'
 assert Incident('unknown','ID','v','NORMAL','OTHER','PREPARED',True,False,True,True,False,False).decide()['status']=='UNKNOWN_EFFECT'
 assert Incident('ahead','ID','v','NORMAL','BEFORE','COMMITTED',True,True,True,True,True,True).decide()['status']=='HOLD_JOURNAL_AHEAD'
 return out
if __name__=='__main__':
 from pathlib import Path
 r=tests();dst=Path(__file__).parent.parent/'evidence'/'R128_CAUSAL_DISPOSITIONS.json'
 dst.write_text(json.dumps({'scope':'MASTER_SIDE_TEST','classification':r,'no_retries':True,'other_sources':'Historical tool response was not durably saved on the target before refusal; summary notes are not independent native causal proof.'},ensure_ascii=False,indent=2))
 print('R128 2/2 actual incidents HOLD with precise reasons, local classifier 6 directed checks',dst)
