"""R141 source-bound actor/spirit/beast relationship check. Does not infer identity from parent name.
A precedent is an observation, NOT a certificate of current assimilation/activation.
"""
from dataclasses import dataclass
from fractions import Fraction
import json
class BindingHold(ValueError):pass
@dataclass(frozen=True)
class BeastEvidence:
 page_id:str; version:str; root_title:str; physical_name:str; bpa_per_level:int|None; actual_rank:str|None
@dataclass(frozen=True)
class SpiritEvidence:
 actor_id:str|None;spirit_id:str|None;beast_page_id:str|None;source_version:str|None;assimilation_receipt:str|None
 cap_ordinal:int|None; distributed_overlay:dict|None; actor_level:int|None

def bind(beast:BeastEvidence,spirit:SpiritEvidence):
 missing=[]
 if not beast.page_id or not beast.version:missing.append('BEAST_SOURCE_ID_VERSION')
 if not beast.physical_name or beast.physical_name!=beast.root_title:missing.append('ROOT_CHILD_NAME_COLLISION_REQUIRES_ADJUDICATION')
 if beast.bpa_per_level is None:missing.append('BEAST_BAP_NOT_READ')
 if spirit.beast_page_id!=beast.page_id or spirit.source_version!=beast.version:missing.append('SPIRIT_TO_BEAST_PROVENANCE')
 if not spirit.actor_id or not spirit.spirit_id or not spirit.assimilation_receipt:missing.append('ACTOR_SPIRIT_ASSIMILATION')
 if spirit.cap_ordinal is None or spirit.actor_level is None:missing.append('CAP_OR_ACTOR_LEVEL')
 if spirit.distributed_overlay is None:missing.append('DISTRIBUTION')
 expected=Fraction(beast.bpa_per_level,2) if beast.bpa_per_level is not None else None
 if not missing and spirit.distributed_overlay is not None:
  total=int(expected*min(spirit.actor_level,spirit.cap_ordinal))
  if sum(spirit.distributed_overlay.values())!=total:missing.append('T4_DISTRIBUTION_CHECKSUM')
 return {'status':'VERIFIED_BINDING' if not missing else 'HOLD_SOURCE_BOUND','beast_id':beast.page_id,
 'actual_beast_name':beast.physical_name,'source_root_title':beast.root_title,
 'source_version':beast.version,'BAP':beast.bpa_per_level,'TAP':str(expected) if expected else None,
 'unproven_fields':missing,'production_write':False}

def main():
 beast=BeastEvidence('230c2b324ede824d89a4815f1f4391d3','2026-10-01T18:00:58.871Z','Espectro da Morte','Draconis Infernum',30,'Lendário 2')
 spirit=SpiritEvidence(None,None,None,None,None,None,None,None)
 r=bind(beast,spirit)
 assert r['TAP']=='15' and r['status']=='HOLD_SOURCE_BOUND'
 assert 'ROOT_CHILD_NAME_COLLISION_REQUIRES_ADJUDICATION' in r['unproven_fields']
 assert 'ACTOR_SPIRIT_ASSIMILATION' in r['unproven_fields']
 same=BeastEvidence('B','v','Besta TEST','Besta TEST',2,'Prata 1')
 ss=SpiritEvidence('ActorTEST','SpiritTEST','B','v','TEST_ONLY_SIMULATED',6,{'SAB':6},6)
 assert bind(same,ss)['status']=='VERIFIED_BINDING'
 bad=SpiritEvidence('ActorTEST','SpiritTEST','B','v','TEST_ONLY_SIMULATED',6,{'SAB':5},6)
 assert 'T4_DISTRIBUTION_CHECKSUM' in bind(same,bad)['unproven_fields']
 return {'official_research':r,'synthetic_schema_contract':'PASS TEST ONLY','checks':4}
if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False,indent=2))
