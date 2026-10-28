"""VLAB R04 reference gateway: serializable local allocation, fencing, journal.

Scope: an ISOLATED demonstration DB and simulated sink only. A production Notion
adapter is deliberately absent. External writes are never automatically retried
when their effect is unknown. No live instance is allocated by this package.

SQLite/WAL needs ONE machine's durable local block filesystem. Never share a
SQLite file over NFS or assume multiple chat containers access the same DB.
The DB and its audit history are part of the protected trust boundary.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import secrets
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path

DOMAIN = 'OP-VLAB-FUSION-SANDBOX-01:ENGINEERING-DOCS'
IDENTITY = 'CM-000006'

class Rejected(Exception):
    """An authorization, state, idempotency or scope condition was rejected."""
    def __init__(self, code):
        self.code = code
        super().__init__(code)

class UncertainEffect(Rejected):
    """External effect cannot be safely inferred; manual reconciliation required."""

class Gateway:
    def __init__(self, database: str | Path, master_key: bytes):
        if not isinstance(master_key, bytes) or len(master_key) < 32:
            raise ValueError('MASTER_KEY_MUST_BE_AT_LEAST_32_BYTES')
        self.database = str(database)
        self.master_key = master_key
        Path(self.database).parent.mkdir(parents=True, exist_ok=True)
        # Demo DB still contains bearer digests; never leave world-readable.
        if not Path(self.database).exists():
            fd=os.open(self.database, os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0o600)
            os.close(fd)
        os.chmod(self.database, 0o600)
        self._init()

    @classmethod
    def from_env(cls, database):
        key = os.getenv('VLAB_GATE_MASTER_KEY_HEX', '')
        if len(key) < 64:
            raise Rejected('MISSING_MASTER_KEY_FAIL_CLOSED')
        try:
            return cls(database, bytes.fromhex(key))
        except ValueError:
            raise Rejected('INVALID_MASTER_KEY_FAIL_CLOSED')

    def _conn(self):
        db = sqlite3.connect(self.database, timeout=30, isolation_level=None)
        db.execute('PRAGMA busy_timeout=30000')
        db.execute('PRAGMA foreign_keys=ON')
        db.execute('PRAGMA synchronous=FULL')
        return db

    @contextmanager
    def _tx(self):
        db = self._conn()
        try:
            db.execute('BEGIN IMMEDIATE')
            yield db
            db.execute('COMMIT')
        except BaseException:
            if db.in_transaction:
                db.execute('ROLLBACK')
            raise
        finally:
            db.close()

    def _init(self):
        # executescript commits pending transactions; initialize outside _tx.
        db = self._conn()
        try:
            db.execute('PRAGMA journal_mode=WAL')
            db.executescript('''
            CREATE TABLE IF NOT EXISTS principals (
                principal_id TEXT PRIMARY KEY,
                identity TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('OPERATOR','CONTROLLER')),
                token_digest TEXT NOT NULL UNIQUE,
                enabled INTEGER NOT NULL CHECK(enabled IN (0,1))
            );
            CREATE TABLE IF NOT EXISTS identity_seq (
                identity TEXT PRIMARY KEY,
                next_seq INTEGER NOT NULL CHECK(next_seq>=1)
            );
            CREATE TABLE IF NOT EXISTS instances (
                identity TEXT NOT NULL,
                seq INTEGER NOT NULL CHECK(seq>=1),
                principal_id TEXT NOT NULL REFERENCES principals(principal_id),
                allocation_key TEXT NOT NULL,
                nonce TEXT NOT NULL,
                state TEXT NOT NULL CHECK(state IN ('ACTIVE','REVOKED','RELEASED')),
                PRIMARY KEY (identity,seq),
                UNIQUE (identity, allocation_key)
            );
            CREATE UNIQUE INDEX IF NOT EXISTS one_active_instance_per_identity
              ON instances(identity) WHERE state='ACTIVE';
            CREATE TABLE IF NOT EXISTS domains (
                name TEXT PRIMARY KEY,
                epoch INTEGER NOT NULL CHECK(epoch>=0),
                owner_identity TEXT,
                owner_seq INTEGER,
                state TEXT NOT NULL CHECK(state IN ('FREE','OWNED','HOLD_UNKNOWN'))
            );
            CREATE TABLE IF NOT EXISTS intents (
                op_id TEXT PRIMARY KEY,
                domain TEXT NOT NULL,
                resource TEXT NOT NULL,
                identity TEXT NOT NULL,
                instance_seq INTEGER NOT NULL,
                epoch INTEGER NOT NULL,
                idempotency_key TEXT NOT NULL,
                expected_revision INTEGER CHECK(expected_revision>=0),
                payload_json TEXT NOT NULL,
                payload_sha256 TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN
                   ('PREPARED','DISPATCHING','UNCERTAIN','APPLIED','ABORTED')),
                evidence TEXT,
                UNIQUE (domain,idempotency_key)
            );
            CREATE TABLE IF NOT EXISTS simulated_cells (
                domain TEXT NOT NULL,
                resource TEXT NOT NULL,
                revision INTEGER NOT NULL,
                epoch INTEGER NOT NULL,
                payload_json TEXT NOT NULL,
                last_op_id TEXT NOT NULL,
                PRIMARY KEY(domain,resource)
            );
            CREATE TABLE IF NOT EXISTS audit (
                seq INTEGER PRIMARY KEY AUTOINCREMENT,
                event TEXT NOT NULL,
                detail_json TEXT NOT NULL,
                created_ns INTEGER NOT NULL
            );
            ''')
            db.execute('INSERT OR IGNORE INTO domains(name,epoch,state) VALUES(?,0,\'FREE\')', (DOMAIN,))
        finally:
            db.close()

    def _digest(self, value: str):
        return hmac.new(self.master_key, value.encode('utf-8'), hashlib.sha256).hexdigest()

    def _audit(self, db, event: str, **details):
        safe = json.dumps(details, sort_keys=True, ensure_ascii=False)
        db.execute('INSERT INTO audit(event,detail_json,created_ns) VALUES(?,?,?)',
                   (event, safe, time.time_ns()))

    def bootstrap_principal(self, principal_id, identity, role, bearer, *, bootstrap_secret):
        """Provisioning API for offline administrative bootstrap only.

        The admin bootstrap secret must be the server master key; never expose
        this method as a remote endpoint. Demo tests call it on temporary DBs.
        """
        if not isinstance(bootstrap_secret, bytes) or not hmac.compare_digest(bootstrap_secret, self.master_key):
            raise Rejected('BOOTSTRAP_UNAUTHORIZED')
        if role not in ('OPERATOR', 'CONTROLLER') or len(bearer) < 32:
            raise Rejected('INVALID_PRINCIPAL')
        if identity != IDENTITY and role != 'CONTROLLER':
            raise Rejected('OUT_OF_SCOPE_IDENTITY')
        with self._tx() as db:
            db.execute('INSERT INTO principals VALUES(?,?,?,?,1)',
                       (principal_id, identity, role, self._digest(bearer)))
            self._audit(db,'PRINCIPAL_PROVISIONED',principal_id=principal_id,identity=identity,role=role)

    def _principal(self, db, bearer, *, role=None, identity=None):
        # Query by digest, verify timing-safe equality and independently check scope.
        if not isinstance(bearer,str) or len(bearer)<32:
            raise Rejected('UNAUTHENTICATED')
        digest = self._digest(bearer)
        row = db.execute('SELECT principal_id,identity,role,enabled,token_digest FROM principals WHERE token_digest=?',
                         (digest,)).fetchone()
        if row is None or not hmac.compare_digest(row[4], digest) or row[3] != 1:
            raise Rejected('UNAUTHENTICATED')
        if role and row[2] != role:
            raise Rejected('ROLE_DENIED')
        if identity and row[1] != identity:
            raise Rejected('IDENTITY_DENIED')
        return row[0]

    def disable_principal(self, controller_bearer, principal_id):
        with self._tx() as db:
            self._principal(db,controller_bearer,role='CONTROLLER')
            # Disabling an operator does not silently hand its active instance to another.
            db.execute('UPDATE principals SET enabled=0 WHERE principal_id=?',(principal_id,))
            self._audit(db,'PRINCIPAL_DISABLED',principal_id=principal_id)

    def _instance_token(self,identity,seq,nonce,principal_id):
        return self._digest(f'instance|{identity}|{seq}|{nonce}|{principal_id}')

    def allocate(self, operator_bearer, allocation_key, *, identity=IDENTITY):
        """A single active instance per identity, with idempotent same-key retry.

        Returns an isolated-sandbox *candidate* (not a Notion identity claim).
        A repeat uses a deterministic HMAC token tied to a durable random nonce.
        """
        if not isinstance(allocation_key,str) or not 1 <= len(allocation_key) <= 128:
            raise Rejected('BAD_ALLOCATION_KEY')
        with self._tx() as db:
            pid = self._principal(db,operator_bearer,role='OPERATOR',identity=identity)
            prior = db.execute('SELECT seq,principal_id,nonce,state FROM instances WHERE identity=? AND allocation_key=?',
                               (identity,allocation_key)).fetchone()
            if prior:
                if prior[1]!=pid:
                    raise Rejected('ALLOCATION_KEY_ALREADY_USED')
                if prior[3]!='ACTIVE':
                    raise Rejected('ALLOCATION_REVOKED')
                seq,nonce=prior[0],prior[2]
                return {'instance':f'{identity}-I{seq:04d}','identity':identity,'seq':seq,
                        'instance_token':self._instance_token(identity,seq,nonce,pid),'replay':True}
            if db.execute("SELECT 1 FROM instances WHERE identity=? AND state='ACTIVE'",(identity,)).fetchone():
                raise Rejected('ACTIVE_INSTANCE_EXISTS')
            db.execute('INSERT OR IGNORE INTO identity_seq VALUES(?,1)',(identity,))
            seq=db.execute('SELECT next_seq FROM identity_seq WHERE identity=?',(identity,)).fetchone()[0]
            nonce=secrets.token_hex(24)
            db.execute('INSERT INTO instances VALUES(?,?,?,?,?,\'ACTIVE\')',
                       (identity,seq,pid,allocation_key,nonce))
            db.execute('UPDATE identity_seq SET next_seq=? WHERE identity=?',(seq+1,identity))
            self._audit(db,'INSTANCE_ALLOCATED_EXPERIMENTAL',identity=identity,seq=seq,principal=pid)
            return {'instance':f'{identity}-I{seq:04d}','identity':identity,'seq':seq,
                    'instance_token':self._instance_token(identity,seq,nonce,pid),'replay':False}

    def _instance(self,db,claim,principal_id):
        if not isinstance(claim,dict) or claim.get('identity')!=IDENTITY:
            raise Rejected('INVALID_CLAIM')
        seq=claim.get('seq')
        if type(seq) is not int:
            raise Rejected('INVALID_CLAIM')
        row=db.execute('SELECT principal_id,nonce,state FROM instances WHERE identity=? AND seq=?',
                       (IDENTITY,seq)).fetchone()
        if not row or row[2]!='ACTIVE' or row[0]!=principal_id:
            raise Rejected('REVOKED_OR_FOREIGN_INSTANCE')
        expected=self._instance_token(IDENTITY,seq,row[1],principal_id)
        token=claim.get('instance_token','')
        if not isinstance(token,str) or not hmac.compare_digest(expected,token):
            raise Rejected('INSTANCE_TOKEN_INVALID')
        return seq

    def _authorized_owner(self,db,claim,principal_id,epoch):
        seq=self._instance(db,claim,principal_id)
        row=db.execute('SELECT epoch,owner_identity,owner_seq,state FROM domains WHERE name=?',(DOMAIN,)).fetchone()
        if row!=(epoch,IDENTITY,seq,'OWNED'):
            raise Rejected('STALE_EPOCH_OR_NOT_OWNER')
        return seq

    def claim_domain(self,operator_bearer,claim):
        with self._tx() as db:
            pid=self._principal(db,operator_bearer,role='OPERATOR',identity=IDENTITY)
            seq=self._instance(db,claim,pid)
            epoch,owner,state=db.execute('SELECT epoch,owner_identity,state FROM domains WHERE name=?',(DOMAIN,)).fetchone()
            if owner is not None or state!='FREE':
                raise Rejected('DOMAIN_NOT_FREE')
            if db.execute("SELECT 1 FROM intents WHERE domain=? AND status IN ('DISPATCHING','UNCERTAIN')",(DOMAIN,)).fetchone():
                raise Rejected('UNRESOLVED_EXTERNAL_EFFECT')
            epoch+=1
            db.execute("UPDATE domains SET epoch=?,owner_identity=?,owner_seq=?,state='OWNED' WHERE name=?",
                       (epoch,IDENTITY,seq,DOMAIN))
            self._audit(db,'DOMAIN_CLAIMED_EXPERIMENTAL',domain=DOMAIN,epoch=epoch,seq=seq)
            return epoch

    def prepare(self,operator_bearer,claim,epoch,op_id,idempotency_key,resource,payload,*,expected_revision=None):
        """Durable reservation. No remote side effect in this operation."""
        if (not isinstance(resource,str) or not re.fullmatch(r'sandbox/[A-Za-z0-9][A-Za-z0-9_./-]{0,199}',resource)
                or '..' in resource or '//' in resource):
            raise Rejected('RESOURCE_SCOPE_DENIED')
        if expected_revision is not None and (type(expected_revision) is not int or expected_revision<0):
            raise Rejected('INVALID_EXPECTED_REVISION')
        if not isinstance(op_id,str) or not 1<=len(op_id)<=120 or not isinstance(idempotency_key,str) or not 1<=len(idempotency_key)<=120:
            raise Rejected('INVALID_OPERATION_KEY')
        try:
            canonical=json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)
        except (TypeError,ValueError):
            raise Rejected('INVALID_PAYLOAD')
        if len(canonical.encode('utf-8'))>100000:
            raise Rejected('PAYLOAD_TOO_LARGE')
        digest=hashlib.sha256(canonical.encode('utf-8')).hexdigest()
        with self._tx() as db:
            pid=self._principal(db,operator_bearer,role='OPERATOR',identity=IDENTITY)
            seq=self._authorized_owner(db,claim,pid,epoch)
            prior=db.execute('SELECT op_id,resource,identity,instance_seq,epoch,expected_revision,payload_sha256,status FROM intents WHERE domain=? AND idempotency_key=?',
                             (DOMAIN,idempotency_key)).fetchone()
            requested=(op_id,resource,IDENTITY,seq,epoch,expected_revision,digest)
            if prior:
                if prior[:7]!=requested:
                    raise Rejected('IDEMPOTENCY_CONFLICT')
                return {'op_id':op_id,'status':prior[7],'replay':True}
            if db.execute('SELECT 1 FROM intents WHERE op_id=?',(op_id,)).fetchone():
                raise Rejected('OP_ID_CONFLICT')
            db.execute("INSERT INTO intents(op_id,domain,resource,identity,instance_seq,epoch,idempotency_key,expected_revision,payload_json,payload_sha256,status) VALUES(?,?,?,?,?,?,?,?,?,?,'PREPARED')",
                       (op_id,DOMAIN,resource,IDENTITY,seq,epoch,idempotency_key,expected_revision,canonical,digest))
            self._audit(db,'INTENT_PREPARED',op_id=op_id,epoch=epoch,resource=resource)
            return {'op_id':op_id,'status':'PREPARED','replay':False}

    def _intent(self,db,op_id):
        row=db.execute('SELECT domain,resource,identity,instance_seq,epoch,expected_revision,payload_json,payload_sha256,status FROM intents WHERE op_id=?',(op_id,)).fetchone()
        if not row:
            raise Rejected('UNKNOWN_OPERATION')
        return row

    def commit_local(self,operator_bearer,claim,epoch,op_id,*,inject_crash_before_commit=False):
        """Only local simulated sink. Cell mutation and ledger commit share a DB transaction.

        For actual Notion, this atomic property DOES NOT hold.
        """
        with self._tx() as db:
            pid=self._principal(db,operator_bearer,role='OPERATOR',identity=IDENTITY)
            seq=self._authorized_owner(db,claim,pid,epoch)
            domain,resource,who,s,ep,expected_revision,body,digest,status=self._intent(db,op_id)
            if (domain,who,s,ep)!=(DOMAIN,IDENTITY,seq,epoch):
                raise Rejected('FOREIGN_OR_STALE_INTENT')
            if status=='APPLIED':
                return {'status':'IDEMPOTENT_REPLAY','op_id':op_id}
            if status!='PREPARED':
                raise Rejected('UNCERTAIN_OR_DISPATCHED_INTENT')
            prior=db.execute('SELECT revision FROM simulated_cells WHERE domain=? AND resource=?',(DOMAIN,resource)).fetchone()
            rev_before=prior[0] if prior else 0
            if expected_revision is not None and expected_revision!=rev_before:
                raise Rejected('RESOURCE_REVISION_CONFLICT')
            rev=rev_before+1
            db.execute('INSERT INTO simulated_cells VALUES(?,?,?,?,?,?) ON CONFLICT(domain,resource) DO UPDATE SET revision=excluded.revision,epoch=excluded.epoch,payload_json=excluded.payload_json,last_op_id=excluded.last_op_id',
                       (DOMAIN,resource,rev,epoch,body,op_id))
            db.execute("UPDATE intents SET status='APPLIED' WHERE op_id=?",(op_id,))
            self._audit(db,'LOCAL_SIMULATED_APPLY',op_id=op_id,revision=rev)
            if inject_crash_before_commit:
                raise RuntimeError('INJECTED_PRE_COMMIT_CRASH')
            return {'status':'SIMULATED_APPLIED','op_id':op_id,'revision':rev}

    def begin_external_dispatch_simulation(self,operator_bearer,claim,epoch,op_id):
        """Records the dangerous handoff but DOES NOT call Notion or any external API."""
        with self._tx() as db:
            pid=self._principal(db,operator_bearer,role='OPERATOR',identity=IDENTITY)
            seq=self._authorized_owner(db,claim,pid,epoch)
            dom,res,who,s,ep,expected_revision,body,digest,status=self._intent(db,op_id)
            if (dom,who,s,ep)!=(DOMAIN,IDENTITY,seq,epoch) or status!='PREPARED':
                raise Rejected('DISPATCH_PRECONDITION_FAILED')
            if db.execute("SELECT 1 FROM intents WHERE domain=? AND status IN ('DISPATCHING','UNCERTAIN')",(DOMAIN,)).fetchone():
                raise Rejected('EXTERNAL_DISPATCH_ALREADY_IN_FLIGHT')
            db.execute("UPDATE intents SET status='DISPATCHING' WHERE op_id=?",(op_id,))
            self._audit(db,'SIMULATED_EXTERNAL_DISPATCH_BEGIN',op_id=op_id)
            return {'status':'DISPATCHING','effect':'NOT_PERFORMED_BY_THIS_PACKAGE'}

    def recover_uncertain(self,controller_bearer):
        """On startup: no replays. Unsettled requests quarantine the domain."""
        with self._tx() as db:
            self._principal(db,controller_bearer,role='CONTROLLER')
            pending=[row[0] for row in db.execute("SELECT op_id FROM intents WHERE status='DISPATCHING'").fetchall()]
            for op_id in pending:
                db.execute("UPDATE intents SET status='UNCERTAIN' WHERE op_id=?",(op_id,))
                self._audit(db,'EXTERNAL_EFFECT_UNKNOWN',op_id=op_id)
            if pending or db.execute("SELECT 1 FROM intents WHERE status='UNCERTAIN'").fetchone():
                db.execute("UPDATE domains SET state='HOLD_UNKNOWN' WHERE name=?",(DOMAIN,))
            return {'unknown':pending,'domain_held':bool(pending) or bool(db.execute("SELECT 1 FROM intents WHERE status='UNCERTAIN'").fetchone())}

    def reconcile_external(self,controller_bearer,op_id,*,confirmed_effect,verified_evidence):
        """Manual control-plane decision; not independent proof of Notion state.

        A production adapter MUST verify evidence from the target after disabling
        old access. A string provided here never certifies real Notion effects.
        """
        if not verified_evidence or len(verified_evidence)<16:
            raise Rejected('EVIDENCE_REQUIRED')
        with self._tx() as db:
            self._principal(db,controller_bearer,role='CONTROLLER')
            dom,res,who,seq,epoch,expected_revision,body,dig,status=self._intent(db,op_id)
            if status not in ('DISPATCHING','UNCERTAIN'):
                raise Rejected('NOT_RECONCILABLE')
            db.execute('UPDATE intents SET status=?, evidence=? WHERE op_id=?',
                       ('APPLIED' if confirmed_effect else 'ABORTED',verified_evidence,op_id))
            self._audit(db,'EXTERNAL_RECONCILED_MANUALLY',op_id=op_id,claimed_effect=confirmed_effect)
            # Do not restore GREEN automatically: explicit externally verified gate required.
            return {'status':'DOCUMENTARY_APPLIED' if confirmed_effect else 'DOCUMENTARY_ABORTED',
                    'external_notion_proof':'NOT_ESTABLISHED'}

    def revoke_and_fence(self,controller_bearer,identity=IDENTITY):
        """Invalidates LOCAL tokens/epochs only, never direct Notion bypass."""
        blocked=False
        new_epoch=None
        with self._tx() as db:
            self._principal(db,controller_bearer,role='CONTROLLER')
            if db.execute("SELECT 1 FROM intents WHERE status IN ('DISPATCHING','UNCERTAIN') AND domain=?",(DOMAIN,)).fetchone():
                db.execute("UPDATE domains SET state='HOLD_UNKNOWN' WHERE name=?",(DOMAIN,))
                self._audit(db,'FENCE_REFUSED_UNKNOWN_EFFECT',domain=DOMAIN)
                blocked=True
            else:
                db.execute("UPDATE instances SET state='REVOKED' WHERE identity=? AND state='ACTIVE'",(identity,))
                row=db.execute('SELECT epoch FROM domains WHERE name=?',(DOMAIN,)).fetchone()
                new_epoch=row[0]+1
                db.execute("UPDATE domains SET epoch=?,owner_identity=NULL,owner_seq=NULL,state='FREE' WHERE name=?",(new_epoch,DOMAIN))
                self._audit(db,'LOCAL_EPOCH_FENCED',identity=identity,epoch=new_epoch)
        if blocked:
            raise UncertainEffect('UNRESOLVED_EXTERNAL_EFFECT_NO_TAKEOVER')
        return {'new_epoch':new_epoch,'external_fencing':'NOT_IMPLEMENTED'}

    def release(self,operator_bearer,claim):
        with self._tx() as db:
            pid=self._principal(db,operator_bearer,role='OPERATOR',identity=IDENTITY)
            seq=self._instance(db,claim,pid)
            if db.execute('SELECT 1 FROM domains WHERE owner_identity=? AND owner_seq=?',(IDENTITY,seq)).fetchone():
                raise Rejected('DOMAIN_STILL_OWNED')
            if db.execute("SELECT 1 FROM intents WHERE identity=? AND instance_seq=? AND status IN ('DISPATCHING','UNCERTAIN')",(IDENTITY,seq)).fetchone():
                raise Rejected('UNKNOWN_EXTERNAL_EFFECT')
            db.execute("UPDATE instances SET state='RELEASED' WHERE identity=? AND seq=?",(IDENTITY,seq))
            self._audit(db,'INSTANCE_RELEASED',instance_seq=seq)

    def snapshot(self,controller_bearer):
        with self._tx() as db:
            self._principal(db,controller_bearer,role='CONTROLLER')
            dom=db.execute('SELECT epoch,owner_identity,owner_seq,state FROM domains WHERE name=?',(DOMAIN,)).fetchone()
            status={s:db.execute('SELECT COUNT(*) FROM intents WHERE status=?',(s,)).fetchone()[0]
                    for s in ('PREPARED','DISPATCHING','UNCERTAIN','APPLIED','ABORTED')}
            return {'domain':DOMAIN,'epoch':dom[0],'owner':None if dom[1] is None else f'{dom[1]}-I{dom[2]:04d}',
                    'state':dom[3],'intents':status,'notion_enforcement':'NOT_IMPLEMENTED',
                    'live_instance_CM000006_I0001':'NOT_ALLOCATED'}

    def local_cell(self,controller_bearer,resource):
        with self._tx() as db:
            self._principal(db,controller_bearer,role='CONTROLLER')
            row=db.execute('SELECT revision,epoch,payload_json,last_op_id FROM simulated_cells WHERE domain=? AND resource=?',
                           (DOMAIN,resource)).fetchone()
            return None if row is None else {'revision':row[0],'epoch':row[1],'payload':json.loads(row[2]),'op_id':row[3]}

    def audit_events(self,controller_bearer):
        with self._tx() as db:
            self._principal(db,controller_bearer,role='CONTROLLER')
            return [dict(seq=r[0],event=r[1],details=json.loads(r[2]))
                    for r in db.execute('SELECT seq,event,detail_json FROM audit ORDER BY seq').fetchall()]
