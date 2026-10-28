"""LEVEL-UP-ENGINE R10 complementary read-only/simulation components.
Not a Notion writer; no production/Party authority. Preserve prior R06–R09 engine.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from html.parser import HTMLParser
from hashlib import sha256
import copy, json
from typing import Any

class StructuralError(ValueError): pass

class _TableParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables=[]; self.stack=[]; self.current=None; self.cell=None
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='table':
            if self.current is not None: raise StructuralError('nested table unsupported')
            self.current={'attrs':tuple(sorted(attrs.items())),'rows':[]}
            self.stack.append(tag)
        elif self.current is not None:
            if tag=='tr' and self.stack[-1]=='table':
                self.current['rows'].append([]); self.stack.append(tag)
            elif tag in ('td','th') and self.stack[-1]=='tr':
                self.cell={'type':tag,'attrs':tuple(sorted(attrs.items())),'text':''}
                self.stack.append(tag)
            else: raise StructuralError('unknown table structure or nesting: '+tag)
    def handle_endtag(self,tag):
        if self.current is not None:
            if not self.stack or self.stack[-1]!=tag: raise StructuralError('bad closing tag')
            self.stack.pop()
            if tag in ('td','th'):
                self.current['rows'][-1].append(self.cell);self.cell=None
            if tag=='table':
                self.tables.append(self.current);self.current=None
    def handle_data(self,data):
        if self.cell is not None: self.cell['text']+=data
        elif self.current is not None and data.strip():
            raise StructuralError('unmodeled text between table cells')
    def close(self):
        super().close()
        if self.stack or self.current is not None: raise StructuralError('incomplete table')

def table_ast(markdown):
    """Extract lossless table matrix; ignore only indentation OUTSIDE cells.
    An unrecognized nested/complex table is rejected, never silently normalized.
    """
    p=_TableParser();p.feed(markdown);p.close()
    if not p.tables:raise StructuralError('no table found')
    return p.tables

def compare_tables(before,after):
    a,b=table_ast(before),table_ast(after)
    return {'equal':a==b,'before_tables':len(a),'after_tables':len(b),
            'before_digest':digest(a),'after_digest':digest(b)}

def digest(value):
    return sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def media_evidence(*, source_block_id=None, clone_block_id=None, source_url=None,
                   clone_url=None, source_bytes=None, clone_bytes=None,
                   delete_restore_verified=False, independent_object_ids=False):
    """Do NOT infer independent backup from block identifiers, URLs or matching bytes.
    A separate media object AND tested restoration after source deletion are required.
    """
    same_bytes=(source_bytes is not None and clone_bytes is not None and source_bytes==clone_bytes)
    verified=bool(independent_object_ids and same_bytes and delete_restore_verified)
    return {'state':'VERIFIED' if verified else 'PENDING',
            'byte_comparison':'MATCH' if same_bytes else 'PENDING' if source_bytes is None or clone_bytes is None else 'MISMATCH',
            'distinct_block_ids':bool(source_block_id and clone_block_id and source_block_id!=clone_block_id),
            'distinct_urls':bool(source_url and clone_url and source_url!=clone_url),
            'independent_media_objects':bool(independent_object_ids),
            'restoration_proven':bool(delete_restore_verified)}

class Crash(BaseException): pass
class Conflict(Exception): pass

@dataclass
class FakeStore:
    pages: dict[str,Any]
    versions: dict[str,int]=field(default_factory=dict)
    journals:dict[str,Journal]=field(default_factory=dict)
    def __post_init__(self):
        self.pages=copy.deepcopy(self.pages)
        for key in self.pages:self.versions.setdefault(key,0)
    def read(self,key):return copy.deepcopy(self.pages[key]),self.versions[key]
    def cas(self,key,old_version,value):
        if self.versions[key]!=old_version:raise Conflict(key)
        self.pages[key]=copy.deepcopy(value);self.versions[key]+=1

@dataclass
class Journal:
    event_id:str
    state:str='NEW'
    snapshots:dict=field(default_factory=dict)
    intended:dict=field(default_factory=dict)
    applied:list=field(default_factory=list)
    audit:list=field(default_factory=list)
    def log(self,event,**kwargs):self.audit.append({'event':event,**kwargs})

class RecoveryController:
    """Simulated compensation protocol. No Notion atomic transaction claimed.
    Crash at an injected boundary is reconciled by comparing physical readback.
    """
    def __init__(self,store):self.store=store
    def run(self,event_id,updates,crash_at=None):
        if len(updates)<2:raise ValueError('require 2+ pages')
        if event_id in self.store.journals:
            existing=self.store.journals[event_id]
            if existing.intended != updates: raise Conflict('event-ID payload collision')
            return existing
        j=Journal(event_id=event_id,intended=copy.deepcopy(updates))
        self.store.journals[event_id]=j
        def boundary(name):
            j.log(name)
            if name==crash_at:raise Crash(name)
        try:
            boundary('BEFORE_PREFLIGHT')
            for k in updates:
                snapshot,version=self.store.read(k)
                j.snapshots[k]={'value':snapshot,'version':version,'hash':digest(snapshot)}
            j.state='SNAPSHOT_READY';boundary('AFTER_PREFLIGHT')
            for k in updates:
                if digest(self.store.read(k)[0])!=j.snapshots[k]['hash']:raise Conflict(k)
            j.state='APPLYING'
            for k,v in updates.items():
                boundary('BEFORE_WRITE:'+k)
                self.store.cas(k,j.snapshots[k]['version'],v)
                j.applied.append(k)
                boundary('AFTER_WRITE:'+k)
                if self.store.read(k)[0]!=v:raise Conflict('readback '+k)
                boundary('AFTER_READBACK:'+k)
            j.state='COMMITTED';boundary('AFTER_COMMIT')
            return j
        except (Crash,Conflict):
            j.state='UNKNOWN_EFFECT' # caller must physically reconcile; no blind retry
            return j
    def reconcile(self,j):
        """Only compensate if current state is exactly snapshot or intended value.
        Unknown concurrent edits require HOLD; never overwrite them.
        """
        if j.state=='COMMITTED':return j
        if not j.snapshots:
            j.state='NOT_APPLIED';j.log('NO_SNAPSHOT');return j
        physical={k:self.store.read(k) for k in j.snapshots}
        for k,(value,version) in physical.items():
            # Detect ABA or concurrent writes even if the final value looks identical.
            expected_version=j.snapshots[k]['version']+(1 if k in j.applied else 0)
            if version!=expected_version or (value!=j.snapshots[k]['value'] and value!=j.intended[k]):
                j.state='HOLD_CONCURRENT_CONFLICT';j.log('HOLD',page=k);return j
        # Preflight crosscheck completed before writing to avoid partial unsafe undo.
        for k in reversed(list(j.snapshots)):
            current,version=self.store.read(k)
            if current==j.intended[k] and current!=j.snapshots[k]['value']:
                self.store.cas(k,version,j.snapshots[k]['value'])
                j.log('COMPENSATE',page=k)
        if all(self.store.read(k)[0]==j.snapshots[k]['value'] for k in j.snapshots):
            j.state='ROLLED_BACK_VERIFIED';j.log('READBACK_ALL_PASS')
        else:j.state='HOLD_READBACK_FAILURE'
        return j

JOURNAL_SCHEMA_VERSION=1

def export_journal(j):
    """Pure JSON checkpoint ready to persist by a separately authorized writer.
    Caller must durably persist and reopen BEFORE proceeding with mutations.
    """
    body={'schema_version':JOURNAL_SCHEMA_VERSION,'event_id':j.event_id,
          'state':j.state,'snapshots':copy.deepcopy(j.snapshots),
          'intended':copy.deepcopy(j.intended),'applied':list(j.applied),
          'audit':copy.deepcopy(j.audit)}
    return json.dumps({'body':body,'sha256':digest(body)},ensure_ascii=False,sort_keys=True)

def import_journal(payload):
    envelope=json.loads(payload)
    body=envelope['body']
    if body.get('schema_version')!=JOURNAL_SCHEMA_VERSION:raise StructuralError('journal schema mismatch')
    if envelope['sha256']!=digest(body):raise StructuralError('journal integrity failure')
    return Journal(event_id=body['event_id'],state=body['state'],snapshots=body['snapshots'],
                   intended=body['intended'],applied=body['applied'],audit=body['audit'])
