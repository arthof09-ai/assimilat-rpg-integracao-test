"""R17 offline binding of dialogue confirmation -> durable local execution.

This is a safety wrapper, not a Notion writer and not a release gate.
Only a DialogueR17 READY object can initiate synthetic writes; the same event
never double-grants. Unknown effects cause HOLD/readback rather than guessing.
"""
from __future__ import annotations
import copy
from dialogue_r17 import DialogueR17
from engine_r17 import validate_r17
from durable_r14 import DurableController
from r10_recovery import digest,Conflict
from roll_ledger_r17 import RollLedger

class RunnerHold(ValueError):pass

class SafeLocalR17Runner:
    def __init__(self,store):
        self.store=store;self.core=DurableController(store)
    @staticmethod
    def _review(dialogue):
        if not isinstance(dialogue,DialogueR17) or dialogue.phase!='READY':
            raise RunnerHold('no completed human-choice dialogue confirmation')
        if not dialogue.answers or dialogue.answers[-1]['phase']!='CONFIRM' or dialogue.answers[-1]['answer']!='CONFIRMO':
            raise RunnerHold('no final explicit CONFIRMO')
        plan=dialogue.executable_plan()
        if plan['event_id']!=dialogue.event_id:
            raise RunnerHold('plan identity changed since confirmation')
        if not plan['event_id'].startswith('SIM-') or plan['writer_authorized'] is not False:
            raise RunnerHold('not an authorized synthetic plan')
        if digest(plan['before'])!=plan['before_digest']:
            raise RunnerHold('tampered before-digest')
        if any(digest(plan['updates'][key])!=plan['diff'][key]['after_sha256'] for key in plan['updates']):
            raise RunnerHold('tampered computed snapshot')
        for receipt in plan['choices']['roll_receipts'].values():
            RollLedger.verify(receipt)
        validate_r17(plan['before']);validate_r17(plan['updates'])
        return plan
    def execute(self,dialogue):
        p=self._review(dialogue)
        event=self.store.event(p['event_id'])
        if event is not None:
            if event['intent_hash']!=digest(p['updates']):
                raise RunnerHold('same event ID but different intent')
            if event['state']!='COMMITTED':
                raise RunnerHold('incomplete/compensated WAL requires reconciliation before new action')
            if digest(self.store.get_all())!=digest(p['updates']):
                raise RunnerHold('previously COMMITTED event cannot be claimed applied after rollback')
            return {'status':'NOOP_VERIFIED_IDEMPOTENT','event_id':p['event_id'],
                    'after_digest':digest(p['updates']),'rolls_new':0,'native_writes':0}
        if digest(self.store.get_all())!=p['before_digest']:
            raise RunnerHold('preimage changed after preview; cannot execute')
        e=self.core.run(p)
        if e['state']!='COMMITTED' or digest(self.store.get_all())!=digest(p['updates']):
            raise RunnerHold('UNKNOWN_EFFECT_OR_BAD_READBACK: reopen/reconcile, no blind retry')
        return {'status':'COMMITTED_LOCAL_VERIFIED','event_id':p['event_id'],
                'after_digest':digest(p['updates']),'rolls_new':0,'native_writes':0}
    def rollback(self,dialogue):
        p=self._review(dialogue)
        e=self.store.event(p['event_id'])
        if not e or e['state']!='COMMITTED':raise RunnerHold('no committed source event')
        out=self.core.explicit_rollback(p['event_id'])
        if out['state']!='COMMITTED' or digest(self.store.get_all())!=p['before_digest']:
            raise RunnerHold('rollback was not exact; HOLD')
        return {'status':'ROLLED_BACK_VERIFIED_LOCAL','before_digest':p['before_digest'],'native_writes':0}

    def verified_player_safe_local_report(self,dialogue):
        """R25: build a play-facing CANDIDATE only after an exact LOCAL readback.

        Not a sender, not a Party approval, not proof of a native Notion update.
        Explicit allowlist prevents inclusion of synthetic Spirit secrets (BAP,
        rolls, hashes, source IDs, GM-only history) from the internal plan.
        """
        from engine_r13 import ATTRS,rank
        p=self._review(dialogue)
        ev=self.store.event(p['event_id'])
        if not ev or ev['state']!='COMMITTED' or ev['intent_hash']!=digest(p['updates']):
            raise RunnerHold('report denied: synthetic event is not committed')
        if digest(self.store.get_all())!=digest(p['updates']):
            raise RunnerHold('report denied: committed state did not pass readback')
        b=p['before']['NORMAL'];n=p['updates']['NORMAL']
        if n['level']<6:
            note='Transformação permanece indisponível em Bronze.'
        else:
            note='A evolução não ativou nem renovou a Transformação.'
        changes={key:{'antes':b['attrs'][key],'depois':n['attrs'][key]}
                 for key in ATTRS if b['attrs'][key]!=n['attrs'][key]}
        return {
            'tipo':'PREVIA_DE_RELATORIO_LOCAL_NAO_PUBLICADO',
            'personagem':'PERSONAGEM_SINTETICO_TESTE',
            'nivel_anterior':b['level'],'nivel_atual':n['level'],
            'classificacao_anterior':rank(b['level'])[2],
            'classificacao_atual':rank(n['level'])[2],
            'alteracoes_atributos_normais':changes,
            'vida_maxima':{'antes':b['hp_max'],'depois':n['hp_max']},
            'vida_atual':{'antes':b['hp_current'],'depois':n['hp_current']},
            'alma_maxima':{'antes':b['pa_max'],'depois':n['pa_max']},
            'alma_atual':{'antes':b['pa_current'],'depois':n['pa_current']},
            'pa_livre':{'antes':b['pa_free'],'depois':n['pa_free']},
            'classe_armadura':{'antes':b['derived']['ca'],'depois':n['derived']['ca']},
            'classe_dificuldade_magia':{'antes':b['derived']['magic_cd'],'depois':n['derived']['magic_cd']},
            'forca_fisica':{'antes':b['derived']['ff'],'depois':n['derived']['ff']},
            'observacao_forma':note,
            'aviso':'Demonstração local: nenhuma ficha do Notion foi alterada; não enviar à Party.'}
