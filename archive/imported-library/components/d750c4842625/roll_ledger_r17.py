"""R17 local-only, crash-resilient roll receipts. Never sends messages or edits Notion.

Two phases: (1) commit unrevealed OS entropy + specification durably; (2) derive
unbiased dice deterministically, reveal a reproducible receipt durably. Reuses
roll_id on retry; mismatch fails closed. SHA256 proves internal consistency, NOT
fairness or resistance to an operator who can rewrite all local records; real
certification needs independent witness/anchor + authorized runtime entropy.
"""
from __future__ import annotations
import hashlib, json, os, re, secrets, fcntl, copy
from pathlib import Path
from durable_r14 import _atomic_json, _sealed, _load, LedgerIntegrityError
from r10_recovery import digest, Conflict

class RollHold(ValueError):pass


def _canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()

def derive(seed_hex: str, spec: dict):
    seed=bytes.fromhex(seed_hex)
    if len(seed)!=32:raise RollHold('invalid entropy length')
    sides=spec['sides'];count=spec['count']
    if type(sides) is not int or type(count) is not int or not (2<=sides<=60 and 1<=count<=25):
        raise RollHold('unsupported dice contract')
    bound=(1<<256)-((1<<256)%sides)
    out=[];counter=0
    while len(out)<count:
        payload=b'LEVELUP-R17-DICE-V1\x00'+seed+_canonical(spec)+counter.to_bytes(8,'big')
        k=int.from_bytes(hashlib.sha256(payload).digest(),'big')
        if k<bound:out.append(k%sides+1)
        counter+=1
    return out,counter

class RollLedger:
    def __init__(self,root):
        self.root=Path(root);self.root.mkdir(parents=True,exist_ok=True)
        self.lock=self.root/'.exclusive.lock'
    def _path(self,roll_id):
        if not isinstance(roll_id,str) or not re.fullmatch(r'SIM-[A-Za-z0-9_-]{1,100}',roll_id):
            raise RollHold('synthetic roll IDs only')
        return self.root/(roll_id+'.json')
    def _transaction(self,fn):
        with open(self.lock,'a+b') as f:
            fcntl.flock(f.fileno(),fcntl.LOCK_EX)
            try:return fn()
            finally:fcntl.flock(f.fileno(),fcntl.LOCK_UN)
    @staticmethod
    def spec(roll_id,event_id,purpose,sides,count,authority='SYNTHETIC_RULE_SELECTED'):
        if not isinstance(event_id,str) or not re.fullmatch('SIM-[A-Za-z0-9_-]{1,80}',event_id):
            raise RollHold('event not synthetic')
        if not isinstance(purpose,str) or not re.fullmatch('[A-Z0-9_-]{2,100}',purpose):
            raise RollHold('invalid purpose')
        v={'schema':'R17-ROLL-V1','roll_id':roll_id,'event_id':event_id,'purpose':purpose,
           'sides':sides,'count':count,'authority':authority}
        # Same constraints whether it is new or already present.
        derive('00'*32,v)
        return v
    def commit(self,roll_id,event_id,purpose,sides,count):
        spec=self.spec(roll_id,event_id,purpose,sides,count)
        path=self._path(roll_id)
        def op():
            if path.exists():
                body=_load(path)
                if body['spec']!=spec:raise Conflict('roll id collision: mismatched terms')
            else:
                entropy=secrets.token_bytes(32).hex()
                commitment=hashlib.sha256(b'LEVELUP-R17-COMMIT-V1\x00'+bytes.fromhex(entropy)+_canonical(spec)).hexdigest()
                body={'spec':spec,'state':'COMMITTED_HIDDEN','private_seed_hex':entropy,
                      'commitment':commitment,'receipt':None,
                      'audit':['ENTROPY_COMMIT_DURABLE_BEFORE_RESULT']}
                _atomic_json(path,_sealed(body))
            return {'roll_id':roll_id,'commitment':body['commitment'],
                    'state':body['state'],'contract_digest':digest(spec)}
        return self._transaction(op)
    def reveal(self,roll_id,event_id,purpose,sides,count):
        spec=self.spec(roll_id,event_id,purpose,sides,count)
        path=self._path(roll_id)
        def op():
            if not path.exists():raise RollHold('cannot reveal without prior durable commitment')
            body=_load(path)
            if body['spec']!=spec:raise Conflict('roll id collision')
            receipt=body['receipt']
            if receipt is not None:
                self.verify(receipt)
                return copy.deepcopy(receipt)
            values,counters=derive(body['private_seed_hex'],spec)
            receipt={'schema':'R17-ROLL-RECEIPT-V1','spec':spec,'commitment':body['commitment'],
                     'seed_reveal_hex':body['private_seed_hex'],'rolls':values,'sum':sum(values),
                     'sha256_domain':'LEVELUP-R17','draws_consumed':counters,
                     'source':'OS_ENTROPY_LOCAL_SIMULATION',
                     'limits':'NOT_EXTERNAL_ENTROPY_PROOF_OR_PARTY_AUTHORITY'}
            receipt['receipt_sha256']=digest(receipt)
            self.verify(receipt)
            body.update(state='REVEALED_DURABLE',receipt=receipt)
            body['audit'].append('RESULT_REVEALED_DURABLE')
            _atomic_json(path,_sealed(body))
            return copy.deepcopy(receipt)
        return self._transaction(op)
    def draw(self,roll_id,event_id,purpose,sides,count):
        c=self.commit(roll_id,event_id,purpose,sides,count)
        return c,self.reveal(roll_id,event_id,purpose,sides,count)
    def read(self,roll_id):
        path=self._path(roll_id)
        return _load(path) if path.exists() else None
    def all_receipts(self):
        return [self.read(p.stem)['receipt'] for p in sorted(self.root.glob('SIM-*.json'))
                if self.read(p.stem)['receipt'] is not None]
    @staticmethod
    def verify(r):
        if not isinstance(r,dict):raise LedgerIntegrityError('invalid receipt')
        proof=copy.deepcopy(r);hd=proof.pop('receipt_sha256',None)
        if digest(proof)!=hd:raise LedgerIntegrityError('receipt hash mismatch')
        spec=r['spec'];expected=RollLedger.spec(spec['roll_id'],spec['event_id'],spec['purpose'],
                                                 spec['sides'],spec['count'],spec['authority'])
        if expected!=spec:raise LedgerIntegrityError('invalid roll specification')
        calc=hashlib.sha256(b'LEVELUP-R17-COMMIT-V1\x00'+bytes.fromhex(r['seed_reveal_hex'])+_canonical(spec)).hexdigest()
        if calc!=r['commitment']:raise LedgerIntegrityError('commitment mismatch')
        vals,counters=derive(r['seed_reveal_hex'],spec)
        if vals!=r['rolls'] or sum(vals)!=r['sum'] or counters!=r['draws_consumed']:
            raise LedgerIntegrityError('replay mismatch')
        return True
