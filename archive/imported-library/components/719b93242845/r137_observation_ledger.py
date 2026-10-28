"""R137 incremental evidence ledger: preserve contradictory originals and append errata.
NO client/Notion network. Authority lives outside this pure module.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from hashlib import sha256
import json,re
from typing import Any

class DocumentaryHold(ValueError): pass

def h(v:Any)->str:
    return sha256((v if isinstance(v,str) else json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'))).encode('utf-8')).hexdigest()

@dataclass(frozen=True)
class EvidenceKey:
    tx:str
    stage:str
    kind:str
    sequence:int
    def validate(self):
        if not all((self.tx,self.stage,self.kind)) or self.sequence<1:raise DocumentaryHold('BAD_COMPOUND_ID')
        return True

@dataclass(frozen=True)
class Observation:
    key:EvidenceKey
    source_page:str
    observed_version:str
    raw_value:str
    operator:str
    evidence_role:str
    def __post_init__(self):
        self.key.validate()
        if not all((self.source_page,self.observed_version,self.operator,self.evidence_role)):
            raise DocumentaryHold('MISSING_PROVENANCE')

class Ledger:
    def __init__(self):self.items={}
    def append(self,o:Observation):
        k=(o.key.tx,o.key.stage,o.key.kind,o.key.sequence)
        if k in self.items:raise DocumentaryHold('DUPLICATE_COMPOUND_EVIDENCE_ID')
        self.items[k]=o
    def append_sequential(self,tx,stage,kind,source_page,observed_version,raw_value,operator,evidence_role):
        seq=1+max([i[3] for i in self.items if i[:3]==(tx,stage,kind)] or [0])
        o=Observation(EvidenceKey(tx,stage,kind,seq),source_page,observed_version,raw_value,operator,evidence_role)
        self.append(o);return o
    def readings(self,tx,stage,kind):return [o for k,o in sorted(self.items.items()) if k[:3]==(tx,stage,kind)]
    def classify(self,tx,stage,kind):
        obs=self.readings(tx,stage,kind)
        if not obs:return 'NO_EVIDENCE'
        return 'DOCUMENTARY_CONFLICT' if len({i.raw_value for i in obs})>1 else 'CONSISTENT_DUPLICATE' if len(obs)>1 else 'SINGLE_OBSERVATION'
    def original_values(self,tx,stage,kind):return [asdict(x) for x in self.readings(tx,stage,kind)]

def scan_occurrences(body,key):
    rows=[]
    for n,line in enumerate(body.splitlines(),1):
        if line.startswith(key+':'):
            rows.append({'line_hint_not_block_id':n,'exact_line':line,'raw_value':line.split(':',1)[1].strip(),'line_sha256':h(line)})
    return rows

def documentary_gate(observed, *,expected_single=False):
    values={x['raw_value'] for x in observed}
    if len(values)>1:return 'DOCUMENTARY_CONFLICT'
    if not observed:return 'EVIDENCE_MISSING'
    if expected_single and len(observed)>1:return 'DUPLICATE_SAME_VALUE_REVIEW'
    return 'CONSISTENT'

def errata_append(*,target_page,version,tx,stage,original_occurrences,explanation,authority):
    if not target_page or not version or authority!='MESTRE_SIDE_TEST_DOCUMENTARY':raise DocumentaryHold('AUTHORITY_MISSING')
    if documentary_gate(original_occurrences)!='DOCUMENTARY_CONFLICT':raise DocumentaryHold('NO_CONFLICT_TO_RECONCILE')
    if not explanation:raise DocumentaryHold('ERRATA_REQUIRES_EXPLANATION')
    return {'tx_id':tx,'stage':stage,'kind':'DOCUMENTARY_ERRATA','sequence':1,
            'target_page':target_page,'pre_version':version,'originals_sha256':[x['line_sha256'] for x in original_occurrences],
            'originals_literal':[x['exact_line'] for x in original_occurrences],
            'explanation':explanation,'operator_scope':authority,'preserve_originals':True}

def main():
    L=Ledger();a=L.append_sequential('TX','NORMAL','NATIVE_RESPONSE','PAGE','v0','NOT_OBSERVED','executor','initial placeholder')
    b=L.append_sequential('TX','NORMAL','NATIVE_RESPONSE','PAGE','v1','{page_id: P}','executor','observed write')
    assert a.key.sequence==1 and b.key.sequence==2
    assert L.classify('TX','NORMAL','NATIVE_RESPONSE')=='DOCUMENTARY_CONFLICT'
    assert L.original_values('TX','NORMAL','NATIVE_RESPONSE')[0]['raw_value']=='NOT_OBSERVED'
    assert L.classify('TX','NORMAL','JOURNAL')=='NO_EVIDENCE'
    c=L.append_sequential('TX','NORMAL','JOURNAL','PAGE','v2','COMMITTED','executor','readback')
    assert c.key.sequence==1 and L.classify('TX','NORMAL','JOURNAL')=='SINGLE_OBSERVATION'
    try:L.append(b)
    except DocumentaryHold:pass
    else:raise AssertionError('same compound ID accepted twice')
    o=scan_occurrences('R131_CAUSAL_TOOL_RESPONSE: A\nR131_CAUSAL_TOOL_RESPONSE: B','R131_CAUSAL_TOOL_RESPONSE')
    assert len(o)==2 and documentary_gate(o)=='DOCUMENTARY_CONFLICT'
    e=errata_append(target_page='P',version='v1',tx='TX',stage='NORMAL',original_occurrences=o,explanation='retain both',authority='MESTRE_SIDE_TEST_DOCUMENTARY')
    assert e['preserve_originals'] and len(e['originals_literal'])==2
    assert documentary_gate(scan_occurrences('R131_CAUSAL_TOOL_RESPONSE: A','R131_CAUSAL_TOOL_RESPONSE'))=='CONSISTENT'
    try:errata_append(target_page='P',version='v1',tx='TX',stage='NORMAL',original_occurrences=o,explanation='',authority='MESTRE_SIDE_TEST_DOCUMENTARY')
    except DocumentaryHold:pass
    else:raise AssertionError('missing explanation accepted')
    return {'status':'PASS','assertions':10,'compound_keys':len(L.items),'conflict_detection':True,'history_preserved':True}
if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False))
