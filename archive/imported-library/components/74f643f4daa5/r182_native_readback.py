"""LEVEL-UP IBX-17 R182: parse native *read-only* Notion tool evidence.

No Notion network calls, no claims of host attestation, no ability to dispatch writes.
The caller must pass a verbatim, fresh connected Notion fetch response. That
input remains untrusted: it is validated for page/parent/marker/journal identity.
Canary already consumed: never issue another write against R177.
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from r173_sqlite_causal_ledger import Ledger, LAB, digest
from r181_host_receipt_ingester import ingest_receipt

CANARY='3fdc2b324ede81a0954cda5efe2fccaa'
TX='IBX17-R177-NATIVE-LEDGER-CANARY-20261018-01'
STAGE='DOC_CANARY'
SOURCE='EXECUTOR_NATIVE_NOTION_TOOL_CAPTURE_SELF_REVIEW'

class NativeReadbackHold(ValueError): pass

@dataclass(frozen=True)
class Readback:
    target:str
    parent:str
    version:str
    phase:str
    journal_verified:bool
    native_attestation:bool=False

def _parse_capture(payload):
    p=payload.get('structuredContent') if isinstance(payload,dict) else None
    if not isinstance(p,dict):raise NativeReadbackHold('NO_NATIVE_STRUCTURED_CONTENT')
    content=p.get('text'); url=p.get('url'); version=p.get('page_last_edited_at')
    if not all(isinstance(t,str) and t for t in (content,url,version)):
        raise NativeReadbackHold('NATIVE_METADATA_INCOMPLETE')
    match=re.search(r'/p/([a-f0-9]{32})(?:\?|$)',url)
    if not match or match.group(1)!=CANARY:raise NativeReadbackHold('WRONG_NATIVE_PAGE')
    tag=re.search(r'<page\s+url="([^"]+)"',content)
    if not tag or '/p/'+CANARY not in tag.group(1):raise NativeReadbackHold('NATIVE_PAGE_BODY_MISMATCH')
    parent=re.search(r'<parent-page\s+url="https://app\.notion\.com/p/([a-f0-9]{32})"',content)
    if not parent or parent.group(1)!=LAB:raise NativeReadbackHold('NATIVE_PARENT_NOT_LAB')
    body=re.search(r'<content>([\s\S]*?)</content>',content)
    if not body:raise NativeReadbackHold('NATIVE_CONTENT_NOT_READABLE')
    return version,body.group(1)

def inspect_native_readback(payload,ledger_path):
    version,body=_parse_capture(payload)
    if body.count('BRIDGE_EVENT: '+TX)!=1:raise NativeReadbackHold('EVENT_NOT_UNIQUE')
    before=body.count('BRIDGE_PHYSICAL: BEFORE');after=body.count('BRIDGE_PHYSICAL: AFTER')
    if (before,after) not in ((1,0),(0,1)):
        raise NativeReadbackHold('PHYSICAL_MARKER_AMBIGUOUS')
    phase='BEFORE' if before==1 else 'AFTER'
    with Ledger(ledger_path) as ledger:
        chain=ledger.verify_chain(TX,STAGE)
        intent=ledger.db.execute('SELECT target,parent,after_sha FROM intent WHERE tx=? AND stage=?',(TX,STAGE)).fetchone()
        if not intent or intent[:2]!=(CANARY,LAB):raise NativeReadbackHold('INTENT_IDENTITY_MISMATCH')
        expected_hash=intent[2]
        journal=(f'BRIDGE_JOURNAL: COMMITTED_AFTER_NATIVE_READBACK; tx={TX}; stage={STAGE}; after_sha={expected_hash};')
        journal_ok=(body.count(journal)==1)
        if phase=='AFTER' and not journal_ok:raise NativeReadbackHold('AFTER_WITHOUT_MATCHING_JOURNAL')
        if phase=='BEFORE' and journal_ok:raise NativeReadbackHold('BEFORE_WITH_COMMITTED_JOURNAL_CONFLICT')
        return {'target':CANARY,'parent':LAB,'phase':phase,'page_version':version,
                'observed_state':{'target':CANARY,'field':'BRIDGE_PHYSICAL: '+phase},
                'journal_verified':journal_ok,'chain_observations':chain['observations'],
                'source_class':SOURCE,'native_attestation':False,'provenance':'CALLER_SUPPLIED_NATIVE_FETCH_SELF_REVIEW',
                'write_allowed':False,'auto_retry':False}

def import_readback_idempotently(payload,ledger_path):
    """Import only new readback-version observations, not any native effects.

    Replay of identical version+phase is NOOP. Local side is append-only.
    It intentionally does not synthesize WRITE_DISPATCHED or native journal.
    """
    readback=inspect_native_readback(payload,ledger_path)
    phase='READBACK_'+readback['phase']
    with Ledger(ledger_path) as ledger:
        previous=ledger.db.execute('SELECT 1 FROM observation WHERE tx=? AND stage=? AND phase=? AND page_version=? LIMIT 1',
                                   (TX,STAGE,phase,readback['page_version'])).fetchone()
        if previous:
            return {'status':'ALREADY_OBSERVED_NOOP','new_rows':0,'write_allowed':False,
                    'native_write_calls':0,'review':'SELF_REVIEW_ONLY'}
    result=ingest_receipt(ledger_path,{
        'tx':TX,'stage':STAGE,'target':CANARY,'phase':phase,
        'page_version':readback['page_version'],'observed_state':readback['observed_state'],
        'auditor':'SELF_REVIEW_ONLY','source_class':SOURCE,'native_attestation':False
    })
    return {'status':'READBACK_IMPORTED_SELF_REVIEW','new_rows':1,
            'ledger_classification':result['ledger_classification']['state'],
            'write_allowed':False,'native_write_calls':0,'native_attestation':False}
