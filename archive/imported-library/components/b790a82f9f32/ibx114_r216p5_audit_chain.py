"""IBX-114: deterministic append-only LOCAL evidence transcript for review requests.

An internal digest chain detects local accidental/casual tampering, NOT a secure
remote notarization, identity attestation, CAS, Notion receipt, or authorization.
It never exposes an EXECUTE transition or imports a Notion connector.
"""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
import json
import re
from typing import Any

SCHEMA='IBX114_REVIEW_CHAIN_LOCAL_V1'
PREVIEW_ID='IBX17-R214-PREVIEW-ALT08-DES1-CON1-FIXED7-20261020'
PREVIEW_SEMANTIC_SHA256='4ef33cc4c36033015ba8251be8fc096e280b6a644a74ca3ed4ba2794f58b0c19'
R213_PAGE='3ffc2b324ede81d383e4df1d5a4633ed'
R213_VERSION='2026-10-20T10:45:46.234Z'
_EVENT_SET={'PREVIEW_ISSUED','CANCEL_REQUESTED','SUBMIT_FOR_APPROVAL',
            'PERSONAL_APPROVAL_EVIDENCE_CLAIMED','TRANSACTION_AUTHORITY_EVIDENCE_CLAIMED',
            'HOST_UNCERTAIN_RESULT_REPORTED','SOURCE_STALE_REPORTED'}
_TERMINAL={'CANCEL_REQUESTED','HOST_UNCERTAIN_RESULT_REPORTED','SOURCE_STALE_REPORTED'}

class ChainHold(ValueError): pass

def _canonical(value:Any)->str:
    return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)

def _hash(value:Any)->str:
    return sha256(_canonical(value).encode('utf-8')).hexdigest()

@dataclass(frozen=True)
class ReviewSubject:
    preview_id:str=PREVIEW_ID
    semantic_sha256:str=PREVIEW_SEMANTIC_SHA256
    source_page_id:str=R213_PAGE
    source_version:str=R213_VERSION
    owner_route:str='MESTRE-SIDE'

    def check(self)->None:
        if (self.preview_id,self.semantic_sha256,self.source_page_id,self.source_version,self.owner_route)!= (
            PREVIEW_ID,PREVIEW_SEMANTIC_SHA256,R213_PAGE,R213_VERSION,'MESTRE-SIDE'):
            raise ChainHold('SUBJECT_MUST_MATCH_FROZEN_R214')


def genesis(subject:ReviewSubject=ReviewSubject())->dict:
    subject.check()
    # Re-generate R214's approved-CHOICES preview from retained rules. Merely
    # repeating a copied hash must never mask a source-code/semantic drift.
    from ibx114_r214_selected_preview import generate
    rendered=generate()
    if (rendered.get('preview_id')!=subject.preview_id or
        rendered.get('sha256_payload_semantic')!=subject.semantic_sha256 or
        rendered.get('source',{}).get('page')!=subject.source_page_id or
        rendered.get('source',{}).get('last_edited_at')!=subject.source_version or
        rendered.get('authorization',{}).get('preview_approved') is not False or
        rendered.get('authorization',{}).get('write_authorized') is not False or
        rendered.get('authorization',{}).get('writes')!=0):
        raise ChainHold('FROZEN_R214_GENERATOR_OR_AUTHORIZATION_DRIFT')
    base={'schema':SCHEMA,'preview_id':subject.preview_id,'preview_sha256':subject.semantic_sha256,
          'source_page':subject.source_page_id,'source_version':subject.source_version,
          'route':subject.owner_route,'genesis_kind':'LOCAL_TEST_EVIDENCE_RECORD_NOT_NOTION_PROOF'}
    return {'base':base,'genesis_hash':_hash(base),'events':[]}


def replay(transcript:dict)->dict:
    """Validate every event and recover cautious status from untrusted local JSON.

    Even event names that say 'evidence' are claims until separately authenticated.
    They cannot move this module into AUTHORIZED or READY_TO_WRITE states.
    """
    if not isinstance(transcript,dict) or set(transcript)!={'base','genesis_hash','events'}:
        raise ChainHold('INVALID_CHAIN_ENVELOPE')
    base=genesis()['base']
    if transcript['base']!=base or transcript['genesis_hash']!=_hash(base):
        raise ChainHold('GENESIS_MISMATCH_OR_SUBJECT_DRIFT')
    events=transcript['events']
    if not isinstance(events,list) or len(events)>10000:raise ChainHold('EVENT_COUNT_INVALID')
    latest=transcript['genesis_hash'];last_type=None;ids=set();phase='UNISSUED'
    for seq,ev in enumerate(events,1):
        if not isinstance(ev,dict) or set(ev)!={'seq','type','id','payload','prior_sha256','entry_sha256'}:
            raise ChainHold('EVENT_SCHEMA_INVALID')
        if type(ev['seq']) is not int or ev['seq']!=seq:raise ChainHold('SEQUENCE_GAP_OR_REORDER')
        if ev['prior_sha256']!=latest:raise ChainHold('CHAIN_LINK_TAMPERED')
        typ=ev['type'];key=ev['id'];p=ev['payload']
        if typ not in _EVENT_SET or not isinstance(key,str) or not re.fullmatch(r'[A-Za-z0-9_.:-]{1,80}',key):
            raise ChainHold('INVALID_EVENT_TYPE_OR_ID')
        if key in ids:raise ChainHold('DUPLICATE_EVENT_ID')
        ids.add(key)
        if not isinstance(p,dict) or len(_canonical(p))>4096:raise ChainHold('INVALID_EVENT_PAYLOAD')
        required={'preview_id':PREVIEW_ID,'semantic_sha256':PREVIEW_SEMANTIC_SHA256,
                  'source_page':R213_PAGE,'source_version':R213_VERSION}
        if any(p.get(k)!=v for k,v in required.items()):raise ChainHold('EVENT_SUBJECT_MISMATCH')
        for k in ('write_authorized','host_transaction_success','cas_proven','physical_receipt_verified'):
            if p.get(k) is True:raise ChainHold('LOCAL_CHAIN_CANNOT_SELF_GRANT_AUTHORITY')
        if phase=='UNISSUED':
            if typ!='PREVIEW_ISSUED':raise ChainHold('PREVIEW_MUST_START_CHAIN')
            phase='PREVIEW_OPEN'
        elif typ in _TERMINAL:
            if phase not in ('PREVIEW_OPEN','SUBMITTED_PENDING_HUMAN'):
                raise ChainHold('CANNOT_TERMINATE_THIS_PHASE')
            phase='CANCELED' if typ=='CANCEL_REQUESTED' else 'FROZEN_HOLD'
        elif typ=='SUBMIT_FOR_APPROVAL':
            if phase!='PREVIEW_OPEN':raise ChainHold('SUBMISSION_OUT_OF_ORDER')
            phase='SUBMITTED_PENDING_HUMAN'
        elif typ in ('PERSONAL_APPROVAL_EVIDENCE_CLAIMED','TRANSACTION_AUTHORITY_EVIDENCE_CLAIMED'):
            if phase!='SUBMITTED_PENDING_HUMAN':raise ChainHold('CLAIM_WITHOUT_PENDING_SUBMISSION')
            # A claimed receipt does not authenticate itself, nor authorize mutation.
        else:raise ChainHold('PHASE_DOES_NOT_ADMIT_EVENT')
        unsigned={k:ev[k] for k in ('seq','type','id','payload','prior_sha256')}
        if ev['entry_sha256']!=_hash(unsigned):raise ChainHold('EVENT_HASH_MISMATCH')
        latest=ev['entry_sha256'];last_type=typ
    return {'schema':SCHEMA,'phase':phase,'events_verified_locally':len(events),
            'last_event':last_type,'chain_tip_sha256':latest,
            'human_preview_approval_physically_verified':False,
            'transaction_authorized':False,'host_writer_permission':False,
            'host_transactions_dispatched':0,'production':'HOLD',
            'evidence_quality':'LOCAL_SELF_CONSISTENCY_NOT_AN_EXTERNAL_ATTESTATION'}


def append(transcript:dict,typ:str,event_id:str,*,details:dict|None=None)->dict:
    replay(transcript)  # Reject even historical manipulation before extending.
    if typ not in _EVENT_SET:raise ChainHold('UNKNOWN_EVENT_TYPE')
    details={} if details is None else details
    if not isinstance(details,dict):raise ChainHold('DETAILS_NOT_OBJECT')
    mandatory={'preview_id':PREVIEW_ID,'semantic_sha256':PREVIEW_SEMANTIC_SHA256,
              'source_page':R213_PAGE,'source_version':R213_VERSION}
    if set(details)&set(mandatory):raise ChainHold('IMMUTABLE_SUBJECT_OVERWRITE')
    payload=mandatory|details
    # JSON round trip prevents sharing mutable caller dictionaries across events.
    payload=json.loads(_canonical(payload))
    current=transcript['events']
    rec={'seq':len(current)+1,'type':typ,'id':event_id,'payload':payload,
         'prior_sha256':current[-1]['entry_sha256'] if current else transcript['genesis_hash']}
    rec['entry_sha256']=_hash(rec)
    out=json.loads(_canonical(transcript));out['events'].append(rec)
    replay(out)
    return out


def demo_readonly()->dict:
    p=genesis();p=append(p,'PREVIEW_ISSUED','r214.preview.demo')
    canceled=append(p,'CANCEL_REQUESTED','r214.cancel.demo')
    submitted=append(p,'SUBMIT_FOR_APPROVAL','r214.submit.demo')
    return {'canceled':replay(canceled),'submitted':replay(submitted),
            'same_source_preview':True,'notion_writes':0}
