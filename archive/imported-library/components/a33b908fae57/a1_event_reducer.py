"""A1 synthetic, source-gated event reducer over Stage12's verified gateway.

ONLY a sandbox research harness.  Never interprets manual orders as canonical
initiative, never invents ties, simultaneous resolution, victory or PA refresh.
Real attack/defense effects are delegated to Stage12's original-backed gateway.
"""
from __future__ import annotations
from copy import deepcopy
from dataclasses import asdict
from hashlib import sha256
import json
from unified_gateway import UnifiedSyntheticGateway


def digest(value):
    return sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), default=str).encode()).hexdigest()


class A1Hold(ValueError):
    pass


class A1EventReducer:
    VERSION='A1-SYNTHETIC-REDUCER-0.1'
    def __init__(self, gateway: UnifiedSyntheticGateway, *, order: tuple[str,...], test_only=False):
        if type(gateway) is not UnifiedSyntheticGateway or test_only is not True:
            raise A1Hold('SANDBOX_GATEWAY_REQUIRED')
        if type(order) is not tuple or len(order)<2 or any(type(a) is not str for a in order):
            raise A1Hold('EXPLICIT_SYNTHETIC_ORDER_REQUIRED')
        if len(set(order))!=len(order) or set(order)!=set(gateway.engine.scene.actors):
            raise A1Hold('ORDER_ACTOR_SNAPSHOT_MISMATCH')
        self.gateway=gateway
        self.order=order
        self.round=0
        self.next_index=0
        self.phase='READY'
        self.active=None
        self.acted=False
        self.events=[]
        self.event_ids=set()
        self.chain='0'*64
        self.anchor=None
        self._seal()

    def _snapshot(self):
        return {'version':self.VERSION,'phase':self.phase,'round':self.round,
                'next_index':self.next_index,'active':self.active,'acted':self.acted,
                'order':self.order,'event_count':len(self.events),'chain':self.chain,
                'gateway':self.gateway.checkpoint(),'ids':sorted(self.event_ids),
                'scene_fingerprint':digest(asdict(self.gateway.engine.scene)),
                'resource_fingerprint':digest({'charges':self.gateway.engine.item_charges,
                                              'transform_ledger':self.gateway.engine.ledger.snapshot()})}

    def _seal(self): self.anchor=digest(self._snapshot())

    def checkpoint(self):
        snap=self._snapshot()
        if digest(snap)!=self.anchor: raise A1Hold('REDUCER_OR_GATEWAY_DRIFT')
        if len(self.events)!=len(self.event_ids):raise A1Hold('DUPLICATE_EVENT_HISTORY')
        predecessor='0'*64
        for i, ev in enumerate(self.events):
            if ev['index']!=i+1 or ev['previous']!=predecessor or digest({k:v for k,v in ev.items() if k!='hash'})!=ev['hash']:
                raise A1Hold('EVENT_LOG_TAMPERED')
            predecessor=ev['hash']
        if predecessor!=self.chain:raise A1Hold('CHAIN_MISMATCH')
        return deepcopy(dict(snap,canonical_credits=0,strict_ready=False,nac_pass_02='HOLD'))

    def dispatch(self, *, event_id:str, kind:str, actor_id=None, payload=None,
                 priority='SERIAL', simultaneous=False, strict=False):
        self.checkpoint()
        if strict:raise A1Hold('STRICT_REQUIRES_APPROVAL')
        if simultaneous or priority!='SERIAL':raise A1Hold('SIMULTANEITY_AND_TIE_NOT_AUTHORIZED')
        if type(event_id) is not str or not event_id.startswith('A1-LAB-') or event_id in self.event_ids:
            raise A1Hold('INVALID_OR_DUPLICATE_EVENT_ID')
        if kind not in {'ROUND_START','TURN_START','ACTION','TURN_END','ROUND_END'}:
            raise A1Hold('UNKNOWN_EVENT')
        if kind=='ROUND_START':
            if self.phase!='READY' or actor_id is not None or payload is not None:raise A1Hold('BAD_ROUND_START')
            self.round+=1;self.next_index=0;self.phase='AWAIT_TURN'
        elif kind=='TURN_START':
            if self.phase!='AWAIT_TURN' or self.next_index>=len(self.order) or actor_id!=self.order[self.next_index] or payload is not None:
                raise A1Hold('BAD_TURN_ORDER')
            self.active=actor_id;self.acted=False;self.phase='IN_TURN'
        elif kind=='ACTION':
            if self.phase!='IN_TURN' or self.acted or actor_id!=self.active or type(payload) is not dict:
                raise A1Hold('ACTION_OUTSIDE_TURN_OR_DUPLICATED')
            operation=payload.get('operation')
            # Reject unknown keys and forged frame before calling any mutable engine.
            if set(payload)!={'operation','params'} or type(payload['params']) is not dict:
                raise A1Hold('ACTION_SCHEMA_REJECTED')
            params=deepcopy(payload['params'])
            # Stage12's manually supplied turn identifier is a lab-only ordinal
            # global action number, not the turn number or official initiative.
            action_number=self.gateway.checkpoint()['executed']+1
            expected_turn=f'LAB-T{action_number}'
            if operation=='ACTION':
                if params.get('actor_id')!=actor_id or params.get('frame',{}).get('turn_id')!=expected_turn:
                    raise A1Hold('ACTOR_OR_MANUAL_FRAME_MISMATCH')
                result=self.gateway.action(**params,strict=False)
            elif operation=='ATTACK_WITH_DEFENSE':
                if (params.get('attacker_id')!=actor_id or params.get('attacker_frame',{}).get('turn_id')!=expected_turn
                    or params.get('defender_frame',{}).get('turn_id')!=expected_turn):
                    raise A1Hold('ATTACKER_OR_MANUAL_FRAME_MISMATCH')
                result=self.gateway.attack_with_defense(**params,strict=False)
            else:raise A1Hold('UNKNOWN_GATEWAY_OPERATION')
            self.acted=True
            payload={'operation':operation,'engine_event':result['audit']['sha256'],
                     'engine_checkpoint':self.gateway.checkpoint()['sha256']}
        elif kind=='TURN_END':
            if self.phase!='IN_TURN' or actor_id!=self.active or payload is not None:
                raise A1Hold('BAD_TURN_END')
            # Legal to pass without an action; not a canonical turn allowance.
            self.phase='AWAIT_TURN';self.active=None;self.acted=False;self.next_index+=1
        elif kind=='ROUND_END':
            if self.phase!='AWAIT_TURN' or self.next_index!=len(self.order) or actor_id is not None or payload is not None:
                raise A1Hold('ROUND_NOT_COMPLETE')
            self.phase='READY';self.next_index=0
        row={'index':len(self.events)+1,'event_id':event_id,'kind':kind,'actor_id':actor_id,
             'round':self.round,'phase_after':self.phase,'payload_digest':digest(payload),
             'engine_digest':self.gateway.checkpoint()['sha256'],
             'previous':self.chain,'canonical_credits':0}
        row['hash']=digest(row)
        self.chain=row['hash'];self.events.append(row);self.event_ids.add(event_id);self._seal()
        return deepcopy(row)


def assert_deterministic_replay(factory, events):
    """Rerun a command ledger against independent fresh LAB gateways."""
    x,y=factory(),factory()
    for data in events:
        first=x.dispatch(**deepcopy(data));second=y.dispatch(**deepcopy(data))
        if first!=second or x.checkpoint()!=y.checkpoint():raise A1Hold('REPLAY_DIVERGENCE')
    return {'status':'SYNTHETIC_REPLAY_PASS','events':len(events),
            'final_chain':x.checkpoint()['chain'],'canonical_credits':0}
