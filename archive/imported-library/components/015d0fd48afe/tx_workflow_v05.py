"""A small, deterministic save-before-edit transaction state machine.

Models intent/reconcile/reopen/commit without direct Notion transport. Failure
injection and readback are explicit: may not retry UNKNOWN_EFFECT writes.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

STEPS=['DISCOVER','CONFIRM_PLAYER_RATE','PREPARE_PREIMAGE','APPEND_SAVE','VERIFY_SAVE','PLAN_PATCH',
       'APPLY_PATCH','VERIFY_PATCH','RECONCILE','REPORT','NAC_PASS','CLOSED']

class TxHold(ValueError):pass

@dataclass
class Tx:
    event_id:str
    page_id:str
    state:str='DISCOVER'
    confirmed_player_rate:bool=False
    source_snapshot_sha:str|None=None
    saved_sha:str|None=None
    updated_sha:str|None=None
    unknown_effect:bool=False
    applied_operations:set[str]=field(default_factory=set)
    history:list[dict]=field(default_factory=list)

    def advance(self, next_state:str, *,proof:str, op_id:str|None=None):
        if self.unknown_effect:raise TxHold('UNKNOWN_EFFECT: reabrir alvo e reconciliar antes de avançar')
        if next_state not in STEPS:raise TxHold('Estado inválido')
        if next_state==self.state:
            raise TxHold('Checkpoint não cria avanço; evitar contar ciclo vazio')
        ix=STEPS.index(self.state); target=STEPS.index(next_state)
        if target!=ix+1:raise TxHold(f'Fluxo fora da ordem: {self.state}→{next_state}')
        if not isinstance(proof,str) or len(proof.strip())<8:
            raise TxHold('Prova específica obrigatória')
        if next_state=='PREPARE_PREIMAGE' and not self.confirmed_player_rate:
            raise TxHold('Player não confirmou taxa de atributo por nível')
        if next_state=='APPEND_SAVE' and not self.source_snapshot_sha:
            raise TxHold('Sem fonte antes')
        if next_state=='PLAN_PATCH' and self.saved_sha!=self.source_snapshot_sha:
            raise TxHold('Não planejar patch sem save íntegro')
        if next_state=='VERIFY_PATCH' and not self.updated_sha:
            raise TxHold('Sem readback do estado alterado')
        if next_state in ('APPEND_SAVE','APPLY_PATCH'):
            if not op_id:raise TxHold('op_id idempotente obrigatório')
            if op_id in self.applied_operations:raise TxHold('Operação já solicitada: reabrir em vez de repetir')
            self.applied_operations.add(op_id)
        before=self.state
        self.state=next_state
        self.history.append({'from':before,'to':next_state,'proof':proof,'op_id':op_id})
        return self.state

    def ambiguous(self, op_id:str):
        self.unknown_effect=True
        self.history.append({'event':'UNKNOWN_EFFECT','op_id':op_id})

    def reopen_reconcile(self, *,observed_state:str,proof:str):
        if not self.unknown_effect:raise TxHold('Não há UNKNOWN_EFFECT')
        if observed_state not in ('operation_applied','operation_absent') or len(proof.strip())<8:
            raise TxHold('Readback ausente/inconclusivo: HOLD')
        self.unknown_effect=False
        self.history.append({'event':'RECONCILED','observed':observed_state,'proof':proof})
        return {'state':self.state,'observed':observed_state,
                'next':'Do not replay if applied' if observed_state=='operation_applied' else 'Verify preconditions before reissue with new fencing'}

    def safe_status(self):
        return {'event_id':self.event_id,'state':self.state,'history_events':len(self.history),
                'unknown_effect':self.unknown_effect,'closed':self.state=='CLOSED',
                'notion_write':False,'party_writer_authorized':False}
