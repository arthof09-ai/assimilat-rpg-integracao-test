"""R14: durable local-only WAL + crash recovery, integrated with engine_r13 plan.
No Notion API, no native multi-page atomicity claim. The local JSON store is a test
fixture; real Notion use requires independent authority, readback and fencing.
"""
from __future__ import annotations
import copy,json,os,re,tempfile,fcntl
from pathlib import Path
from r10_recovery import digest, Conflict

class SimulatedProcessCrash(BaseException): pass
class LedgerIntegrityError(ValueError): pass


def _atomic_json(path, obj):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(dir=str(path.parent),prefix='.tmp-')
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f:
            json.dump(obj,f,sort_keys=True,ensure_ascii=False,separators=(',',':'))
            f.flush();os.fsync(f.fileno())
        os.replace(name,path)
        try:
            d=os.open(path.parent,os.O_RDONLY)
            try:os.fsync(d)
            finally:os.close(d)
        except OSError:pass
    finally:
        if os.path.exists(name):os.unlink(name)


def _sealed(data):return {'body':data,'sha256':digest(data)}


def _load(path):
    with open(path,encoding='utf-8') as f:env=json.load(f)
    if set(env)!={'body','sha256'} or digest(env['body'])!=env['sha256']:
        raise LedgerIntegrityError('snapshot/journal seal mismatch')
    return env['body']

class DurableStore:
    def __init__(self,root,initial=None):
        self.root=Path(root);self.root.mkdir(parents=True,exist_ok=True)
        self.state_path=self.root/'state.json';self.journal_dir=self.root/'events';self.cas_lock_path=self.root/'cas.lock'
        self.journal_dir.mkdir(exist_ok=True)
        if not self.state_path.exists():
            if initial is None:raise FileNotFoundError('existing state required for reopen')
            self._save({'pages':copy.deepcopy(initial),'versions':{k:0 for k in initial}})
        self._load()
    def _load(self):return _load(self.state_path)
    def _save(self,state):_atomic_json(self.state_path,_sealed(state))
    def read(self,key):
        state=self._load()
        return copy.deepcopy(state['pages'][key]),state['versions'][key]
    def cas(self,key,version,value):
        # Local, cooperating-process CAS. Does not substitute Notion fencing.
        with open(self.cas_lock_path,'a+b') as lock:
            fcntl.flock(lock.fileno(),fcntl.LOCK_EX)
            try:
                state=self._load()
                if state['versions'][key]!=version:raise Conflict('durable CAS version conflict')
                state['pages'][key]=copy.deepcopy(value)
                state['versions'][key]+=1
                self._save(state)
            finally:fcntl.flock(lock.fileno(),fcntl.LOCK_UN)
    def get_all(self):return self._load()['pages']
    def _event_path(self,event_id):
        if not re.fullmatch(r'SIM-[A-Za-z0-9_-]{1,80}',event_id):
            raise ValueError('synthetic event name only')
        return self.journal_dir/(event_id+'.json')
    def event(self,event_id):
        p=self._event_path(event_id)
        return _load(p) if p.exists() else None
    def save_event(self,event):_atomic_json(self._event_path(event['event_id']),_sealed(event))

class DurableController:
    def __init__(self,store):self.store=store
    def run(self,prepared,crash_at=None):
        event_id=prepared['event_id'];current=self.store.event(event_id)
        intent_hash=digest(prepared['updates'])
        if current is not None:
            if current['intent_hash']!=intent_hash:raise Conflict('persistent event-ID payload collision')
            return current
        keys=list(prepared['updates'])
        if len(keys)<2:raise ValueError('multipage transaction requires 2+ pages')
        def crash(boundary):
            if crash_at==boundary:raise SimulatedProcessCrash(boundary)
        crash('BEFORE_PREPARE')
        snapshots={}
        for key in keys:
            before,version=self.store.read(key)
            snapshots[key]={'value':before,'version':version,'hash':digest(before)}
        if digest({k:self.store.read(k)[0] for k in keys})!=prepared['before_digest']:
            raise Conflict('stale preflight before WAL')
        event={'schema':1,'event_id':event_id,'state':'PREPARED','intent_hash':intent_hash,
               'snapshots':snapshots,'intended':copy.deepcopy(prepared['updates']),
               'audit':['WAL_PREPARED'], 'keys':keys}
        self.store.save_event(event) # WAL is durably persisted before first write.
        crash('AFTER_PREPARE')
        for key in keys:
            event['state']='WRITING';event['audit'].append('BEFORE_WRITE:'+key)
            self.store.save_event(event)
            crash('BEFORE_WRITE:'+key)
            self.store.cas(key,snapshots[key]['version'],event['intended'][key])
            crash('AFTER_WRITE:'+key) # crash before ACK journal
            if self.store.read(key)[0]!=event['intended'][key]:
                raise Conflict('local readback failed')
            event['audit'].append('AFTER_READBACK:'+key)
            self.store.save_event(event)
            crash('AFTER_READBACK:'+key)
        event['state']='COMMITTED';event['audit'].append('COMMITTED_READBACK_ALL')
        self.store.save_event(event)
        crash('AFTER_COMMIT')
        return event
    def recover(self,event_id,crash_at=None):
        event=self.store.event(event_id)
        if event is None:return 'NOT_APPLIED_NO_WAL'
        if event['state'] in ('COMMITTED','ROLLED_BACK_VERIFIED','HOLD_CONCURRENT_CONFLICT'):
            return event['state']
        snapshots=event['snapshots'];intended=event['intended']
        classification={}
        # Full cross-page preflight: no mutation unless ALL pages are consistent
        # with this event and its expected local version sequence.
        for key in event['keys']:
            value,v=self.store.read(key)
            initial=snapshots[key]
            if value==initial['value'] and v==initial['version']:
                classification[key]='UNTOUCHED'
            elif value==intended[key] and v==initial['version']+1:
                classification[key]='APPLIED'
            elif value==initial['value'] and v==initial['version']+2:
                classification[key]='COMPENSATED'
            else:
                event['state']='HOLD_CONCURRENT_CONFLICT';event['audit'].append('HOLD:'+key)
                self.store.save_event(event);return event['state']
        event['state']='COMPENSATING';event['audit'].append('RECOVER_ABORT_START')
        self.store.save_event(event)
        for key in reversed(event['keys']):
            if classification[key]=='APPLIED':
                crash_name='BEFORE_COMPENSATE:'+key
                if crash_at==crash_name:raise SimulatedProcessCrash(crash_name)
                _,version=self.store.read(key)
                self.store.cas(key,version,snapshots[key]['value'])
                if crash_at=='AFTER_COMPENSATE:'+key:raise SimulatedProcessCrash('AFTER_COMPENSATE:'+key)
                event['audit'].append('COMPENSATE:'+key)
                self.store.save_event(event)
        if any(self.store.read(key)[0]!=snapshots[key]['value'] for key in event['keys']):
            raise Conflict('recovery still not equal to preimage')
        event['state']='ROLLED_BACK_VERIFIED';event['audit'].append('READBACK_ALL_PASS')
        self.store.save_event(event)
        return event['state']
    def explicit_rollback(self,event_id):
        e=self.store.event(event_id)
        if not e or e['state']!='COMMITTED':raise Conflict('requires committed event')
        # Explicit inverse local mutation with a separate idempotent event, no
        # silent deletion of historical receipt. Other modifications MUST HOLD.
        pages=self.store.get_all()
        if any(pages[k]!=e['intended'][k] or self.store.read(k)[1]!=e['snapshots'][k]['version']+1 for k in e['keys']):
            raise Conflict('inverse denied: concurrent modification')
        reverse=copy.deepcopy(e['snapshots'])
        before=copy.deepcopy(pages)
        new_id='SIM-UNDO-'+event_id.removeprefix('SIM-')
        plan={'event_id':new_id,'updates':{k:reverse[k]['value'] for k in e['keys']},
              'before_digest':digest(before)}
        reverse_receipt=self.run(plan)
        e['audit'].append('EXPLICIT_INVERSE_COMMITTED:'+new_id)
        self.store.save_event(e)
        return reverse_receipt
