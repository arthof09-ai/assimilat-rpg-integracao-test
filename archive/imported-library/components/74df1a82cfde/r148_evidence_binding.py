"""R148 source provenance: textual certificates or TEST_ONLY_SIMULATED are never proof.
This does not create a new canon or attribute the catalog child to its root title.
"""
from __future__ import annotations
from fractions import Fraction
from hashlib import sha256
import json

STATES=('SCHEMA_VALID_TEST_ONLY','BEAST_SOURCE_IDENTIFIED','SPIRIT_LINK_DOCUMENTED','ASSIMILATION_EVIDENCED','TRANSFORMATION_ATTRIBUTES_RECONCILED','SOURCE_BOUND_VERIFIED','HOLD_SOURCE_BOUND')

class EvidenceHold(ValueError): pass

def fractional_budget(*,bap,level,cap,previous_distributed=None):
 if type(bap)!=int or type(level)!=int or type(cap)!=int or min(bap,level,cap)<0:raise EvidenceHold('INVALID_NUMERIC_SOURCE')
 tap=Fraction(bap,2); raw=tap*min(level,cap); alloc=raw.numerator//raw.denominator;carry=raw-alloc
 prev=sum(previous_distributed.values()) if previous_distributed else 0
 if prev>alloc:raise EvidenceHold('DISTRIBUTION_EXCEEDS_AVAILABLE')
 result={'tap_numerator':tap.numerator,'tap_denominator':tap.denominator,'raw_numerator':raw.numerator,'raw_denominator':raw.denominator,'distributable':alloc,'carry_numerator':carry.numerator,'carry_denominator':carry.denominator,'already_distributed':prev,'remaining':alloc-prev,'effective_level':min(level,cap)}
 result['checksum']=sha256(json.dumps(result,sort_keys=True).encode()).hexdigest();return result

def classify(*,beast_page_id,beast_version,beast_name,tree_root_name,bap,actor_id,spirit_id,beast_link_id,spirit_source_version,assimilation_evidence,cap,actor_level,distribution,reviewed_source_provenance=False):
 issues=[]
 if not beast_page_id or not beast_version or not beast_name or bap is None:return {'status':'HOLD_SOURCE_BOUND','issues':['BEAST_ID_VERSION_OR_BAP_MISSING'],'certified':False}
 outcome='BEAST_SOURCE_IDENTIFIED'
 if tree_root_name!=beast_name:issues.append('ROOT_CHILD_NAME_COLLISION')
 if not (actor_id and spirit_id and beast_link_id==beast_page_id and spirit_source_version==beast_version):issues.append('PHYSICAL_SPIRIT_LINK_MISSING')
 else:outcome='SPIRIT_LINK_DOCUMENTED'
 artifact=assimilation_evidence
 if not isinstance(artifact,dict) or artifact.get('scope') in ('SYNTHETIC','TEST_ONLY') or not artifact.get('source_page_id') or not artifact.get('source_version') or not artifact.get('verifiable_event_id'):
  issues.append('ASSIMILATION_RECEIPT_NOT_SOURCE_BOUND')
 else:outcome='ASSIMILATION_EVIDENCED'
 if cap is None or actor_level is None or distribution is None:issues.append('CAP_LEVEL_DISTRIBUTION_MISSING')
 else:
  budget=fractional_budget(bap=bap,level=actor_level,cap=cap,previous_distributed=distribution)
  if budget['remaining']!=0:issues.append('DISTRIBUTION_NOT_FULLY_RECONCILED')
  else:outcome='TRANSFORMATION_ATTRIBUTES_RECONCILED'
 if not reviewed_source_provenance:issues.append('INDEPENDENT_SOURCE_PROVENANCE_NOT_ATTESTED')
 if not issues:issues.append('NATIVE_SOURCE_ATTESTATION_UNAVAILABLE_TO_PURE_FUNCTION')
 if issues:return {'status':'SCHEMA_VALID_TEST_ONLY' if isinstance(artifact,str) and artifact.startswith('TEST_') or isinstance(artifact,dict) and artifact.get('scope')=='SYNTHETIC' else 'HOLD_SOURCE_BOUND','last_proven_stage':'SCHEMA_VALID_TEST_ONLY' if isinstance(artifact,str) and artifact.startswith('TEST_') or isinstance(artifact,dict) and artifact.get('scope')=='SYNTHETIC' else outcome,'issues':issues,'certified':False,'budget':locals().get('budget')}
 return {'status':'SOURCE_BOUND_VERIFIED','issues':[],'certified':True,'budget':budget}

def selftest():
 base=dict(beast_page_id='B',beast_version='v',beast_name='B',tree_root_name='B',bap=11,actor_id='A',spirit_id='S',beast_link_id='B',spirit_source_version='v',assimilation_evidence='TEST_ONLY_SIMULATED',cap=2,actor_level=2,distribution={'SAB':11},reviewed_source_provenance=True)
 checks=[]
 def ck(q):assert q;checks.append(1)
 ck(classify(**base)['status']=='SCHEMA_VALID_TEST_ONLY')
 ck(not classify(**base)['certified'])
 ck(not classify(**(base|{'assimilation_evidence':{'scope':'SYNTHETIC','source_page_id':'X','source_version':'1','verifiable_event_id':'FAKE'}}))['certified'])
 ck(classify(**(base|{'tree_root_name':'OTHER'}))['certified'] is False)
 b=fractional_budget(bap=11,level=1,cap=8);ck(b['distributable']==5 and (b['carry_numerator'],b['carry_denominator'])==(1,2))
 b=fractional_budget(bap=11,level=2,cap=8);ck(b['distributable']==11 and b['carry_numerator']==0)
 b=fractional_budget(bap=11,level=6,cap=1);ck(b['distributable']==5 and b['effective_level']==1)
 try:fractional_budget(bap=11,level=1,cap=8,previous_distributed={'SAB':6})
 except EvidenceHold:ck(True)
 else:raise AssertionError('overallocated')
 ck(classify(**(base|{'assimilation_evidence':{'scope':'CANONICAL','source_page_id':'X','source_version':'1','verifiable_event_id':'X'},'reviewed_source_provenance':False}))['certified'] is False)
 return {'checks':len(checks),'synthetic_certificate_prevented':True,'Nie_Li_Espectro':'HOLD_ROOT_CHILD_NAME_CONFLICT'}
if __name__=='__main__':print(json.dumps(selftest()))
