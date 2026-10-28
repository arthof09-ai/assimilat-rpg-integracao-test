#!/usr/bin/env python3
"""Prototype only: shared transactional allocator and fenced LOCAL write gateway.
NOT a Notion integration. Never use it to claim real Notion writer/lease/GREEN.
Use only in a deliberately configured shared host with a single enforced write API.
"""
import concurrent.futures
import hashlib
import json
import os
import secrets
import sqlite3
import tempfile
from pathlib import Path

class Rejected(RuntimeError):
    pass

class VLabGate:
    def __init__(self, database):
        self.database = str(database)
        with self.conn() as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS identities (
                identity TEXT PRIMARY KEY,
                next_seq INTEGER NOT NULL CHECK(next_seq>0)
            );
            CREATE TABLE IF NOT EXISTS instances (
                identity TEXT NOT NULL,
                seq INTEGER NOT NULL,
                token_hash TEXT NOT NULL,
                state TEXT NOT NULL CHECK(state IN ('ACTIVE','RELEASED')),
                PRIMARY KEY(identity, seq)
            );
            CREATE UNIQUE INDEX IF NOT EXISTS unique_active_instance
                ON instances(identity) WHERE state='ACTIVE';
            CREATE TABLE IF NOT EXISTS domains (
                domain TEXT PRIMARY KEY,
                epoch INTEGER NOT NULL,
                owner_identity TEXT,
                owner_seq INTEGER,
                owner_token_hash TEXT
            );
            CREATE TABLE IF NOT EXISTS local_writes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT NOT NULL,
                epoch INTEGER NOT NULL,
                owner_identity TEXT NOT NULL,
                owner_seq INTEGER NOT NULL,
                idempotency_key TEXT NOT NULL UNIQUE,
                payload_hash TEXT NOT NULL
            );
            ''')

    def conn(self):
        db = sqlite3.connect(self.database, timeout=30, isolation_level=None)
        db.execute('PRAGMA busy_timeout=30000')
        return db

    @staticmethod
    def digest(token):
        return hashlib.sha256(token.encode('utf8')).hexdigest()

    def allocate(self, identity='CM-000006'):
        token = secrets.token_urlsafe(32)
        with self.conn() as db:
            db.execute('BEGIN IMMEDIATE')
            db.execute('INSERT OR IGNORE INTO identities VALUES (?, 1)', (identity,))
            prior = db.execute('SELECT seq FROM instances WHERE identity=? AND state=\'ACTIVE\'', (identity,)).fetchone()
            if prior:
                raise Rejected('ACTIVE_INSTANCE_EXISTS')
            seq = db.execute('SELECT next_seq FROM identities WHERE identity=?', (identity,)).fetchone()[0]
            db.execute('INSERT INTO instances VALUES (?,?,?,?)', (identity, seq, self.digest(token), 'ACTIVE'))
            db.execute('UPDATE identities SET next_seq=? WHERE identity=?', (seq+1, identity))
            db.commit()
            return {'identity':identity,'instance':f'{identity}-I{seq:04d}','seq':seq,'token':token}

    def verify_instance(self, db, claim):
        row = db.execute('SELECT token_hash FROM instances WHERE identity=? AND seq=? AND state=\'ACTIVE\'', (claim['identity'], claim['seq'])).fetchone()
        if not row or row[0] != self.digest(claim['token']):
            raise Rejected('INVALID_OR_REVOKED_INSTANCE')

    def take_domain(self, claim, domain='VLAB:ENGINEERING-DOCS'):
        with self.conn() as db:
            db.execute('BEGIN IMMEDIATE')
            self.verify_instance(db, claim)
            row = db.execute('SELECT epoch,owner_identity FROM domains WHERE domain=?', (domain,)).fetchone()
            if row and row[1] is not None:
                raise Rejected('DOMAIN_ALREADY_OWNED')
            epoch=(row[0] if row else 0)+1
            db.execute('INSERT INTO domains VALUES (?,?,?,?,?) ON CONFLICT(domain) DO UPDATE SET epoch=excluded.epoch,owner_identity=excluded.owner_identity,owner_seq=excluded.owner_seq,owner_token_hash=excluded.owner_token_hash', (domain,epoch,claim['identity'],claim['seq'],self.digest(claim['token'])))
            db.commit()
            return epoch

    def commit_local(self, claim, domain, epoch, idempotency_key, payload):
        """Atomic only with the LOCAL SQLite row; not with external Notion writes."""
        with self.conn() as db:
            db.execute('BEGIN IMMEDIATE')
            self.verify_instance(db, claim)
            row=db.execute('SELECT epoch,owner_identity,owner_seq,owner_token_hash FROM domains WHERE domain=?',(domain,)).fetchone()
            if not row or row != (epoch, claim['identity'], claim['seq'], self.digest(claim['token'])):
                raise Rejected('STALE_FENCED_WRITER')
            payload_hash=hashlib.sha256(payload.encode('utf8')).hexdigest()
            previous=db.execute('SELECT domain,epoch,owner_identity,owner_seq,payload_hash FROM local_writes WHERE idempotency_key=?',(idempotency_key,)).fetchone()
            desired=(domain,epoch,claim['identity'],claim['seq'],payload_hash)
            if previous:
                if previous != desired:
                    raise Rejected('IDEMPOTENCY_KEY_CONFLICT')
                return 'IDEMPOTENT_REPLAY'
            db.execute('INSERT INTO local_writes(domain,epoch,owner_identity,owner_seq,idempotency_key,payload_hash) VALUES (?,?,?,?,?,?)', (domain,epoch,claim['identity'],claim['seq'],idempotency_key,payload_hash))
            db.commit()
            return 'LOCAL_COMMITTED'

    def release_domain(self, claim, domain, epoch):
        with self.conn() as db:
            db.execute('BEGIN IMMEDIATE')
            self.verify_instance(db,claim)
            row=db.execute('SELECT epoch,owner_identity,owner_seq,owner_token_hash FROM domains WHERE domain=?',(domain,)).fetchone()
            if row != (epoch, claim['identity'],claim['seq'],self.digest(claim['token'])):
                raise Rejected('NOT_DOMAIN_OWNER')
            db.execute('UPDATE domains SET owner_identity=NULL,owner_seq=NULL,owner_token_hash=NULL WHERE domain=?',(domain,))
            db.commit()

    def release_instance(self, claim):
        with self.conn() as db:
            db.execute('BEGIN IMMEDIATE')
            self.verify_instance(db,claim)
            if db.execute('SELECT 1 FROM domains WHERE owner_identity=? AND owner_seq=?',(claim['identity'],claim['seq'])).fetchone():
                raise Rejected('DOMAIN_STILL_OWNED')
            db.execute("UPDATE instances SET state='RELEASED' WHERE identity=? AND seq=?",(claim['identity'],claim['seq']))
            db.commit()


def self_test():
    with tempfile.TemporaryDirectory() as tmp:
        gate=VLabGate(Path(tmp)/'shared_gate.sqlite')
        def attempt(_):
            try:
                return gate.allocate()
            except Rejected as e:
                return str(e)
        with concurrent.futures.ThreadPoolExecutor(max_workers=24) as pool:
            responses=list(pool.map(attempt,range(24)))
        winners=[r for r in responses if isinstance(r,dict)]
        assert len(winners)==1, responses
        assert responses.count('ACTIVE_INSTANCE_EXISTS')==23
        owner=winners[0]
        epoch=gate.take_domain(owner)
        assert epoch==1
        assert gate.commit_local(owner,'VLAB:ENGINEERING-DOCS',epoch,'key-01','data-01')=='LOCAL_COMMITTED'
        assert gate.commit_local(owner,'VLAB:ENGINEERING-DOCS',epoch,'key-01','data-01')=='IDEMPOTENT_REPLAY'
        denied=[]
        def reject_bad(fn):
            try:fn()
            except Rejected as e:denied.append(str(e))
        reject_bad(lambda:gate.take_domain(owner))
        reject_bad(lambda:gate.commit_local(owner,'VLAB:ENGINEERING-DOCS',epoch,'key-01','CHANGED'))
        gate.release_domain(owner,'VLAB:ENGINEERING-DOCS',epoch)
        gate.release_instance(owner)
        successor=gate.allocate()
        assert successor['seq']==2
        new_epoch=gate.take_domain(successor)
        assert new_epoch==2
        reject_bad(lambda:gate.commit_local(owner,'VLAB:ENGINEERING-DOCS',epoch,'key-02','old writer'))
        reject_bad(lambda:gate.commit_local(successor,'VLAB:ENGINEERING-DOCS',epoch,'key-03','old epoch'))
        assert gate.commit_local(successor,'VLAB:ENGINEERING-DOCS',new_epoch,'key-04','new writer')=='LOCAL_COMMITTED'
        with gate.conn() as db:
            n=db.execute('SELECT COUNT(*) FROM local_writes').fetchone()[0]
        assert n==2
        print(json.dumps({'gate':'LOCAL_SQLITE_PROTOTYPE_ONLY','race_candidates':24,'granted':len(winners),'denied_parallel':23,'epochs':[epoch,new_epoch],'verified_local_writes':n,'replays':'idempotent','rejections':denied,'all_local_assertions':'PASS','notion_enforcement':'NOT_IMPLEMENTED','actual_CM000006_I0001':'NOT_ALLOCATED'},sort_keys=True,ensure_ascii=False))

if __name__=='__main__':self_test()