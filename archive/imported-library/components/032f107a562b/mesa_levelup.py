"""Serviço de UX GUI V03 sobre o motor inalterado R17/R27.

Não calcula regras. Somente faz perguntas, confirma, guarda cópias, mostra
planos e encaminha commit e rollback ao SafeRunner/DurableController existentes.
"""
from __future__ import annotations
import copy
import hashlib
import json
import secrets
from datetime import datetime, timezone
from pathlib import Path

# importar pelo inicializador CLI garante shim Windows antes dos imports fcntl
from iniciar_levelup import (APP_ROOT, DialogueR17, RollLedger, DurableStore,
    DurableController, SafeLocalR17Runner, _atomic_json, validate_r17, digest)
from apresentacao_levelup import plan_report

class LocalHold(ValueError):pass

def save(path, body):
    _atomic_json(path,body)

def archive_import(folder,evidence):
    raw=evidence['original_raw_bytes']
    p=folder/'SNAPSHOT_ORIGINAL_IMUTAVEL.json'
    p.write_bytes(raw)
    if p.read_bytes()!=raw:
        raise LocalHold('HOLD arquivo de origem alterado na gravação')
    save(folder/'PROVENIENCIA_COPIA.json',{k:v for k,v in evidence.items()
         if k not in ('original_raw_bytes','snapshot')})
    if 'field_provenance' in evidence:
        save(folder/'MANIFESTO_ORIGEM_POR_CAMPO.json', evidence['field_provenance'])

class LocalSession:
    def __init__(self, label, fixture, target, *, root=APP_ROOT, source_evidence=None):
        self.label=label
        self.root=Path(root)
        self.initial=copy.deepcopy(fixture)
        validate_r17(self.initial)
        self.source_evidence=source_evidence
        self.run_id=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_'+secrets.token_hex(6)
        self.folder=self.root/'execucoes'/self.run_id
        self.folder.mkdir(parents=True,exist_ok=False)
        self.event_id='SIM-UI-'+secrets.token_hex(12)
        save(self.folder/'ESTADO_INICIAL.json',self.initial)
        if source_evidence:archive_import(self.folder,source_evidence)
        self.store=DurableStore(self.folder/'COPIA_LOCAL_3_DOCS', self.initial)
        self.dialogue=DialogueR17(copy.deepcopy(self.initial),target,self.event_id,
                                RollLedger(self.folder/'RECIBOS_DADOS'))
        self.transcript=[]
        self.committed=False

    @property
    def phase(self):return self.dialogue.phase
    def respond(self, answer):
        d=self.dialogue
        phase=d.phase
        if phase in ('HOLD','READY'):raise LocalHold('diálogo encerrado')
        question=d.prompt()
        try:
            d.respond(answer)
            self.transcript.append({'phase':phase,'question':question,
                                    'answer':answer,'accepted':True,'phase_after':d.phase})
            return d.phase
        except Exception as exc:
            self.transcript.append({'phase':phase,'question':question,'answer':answer,
                                    'accepted':False,'reason':str(exc)})
            # Propaga mensagens nativas do motor, sem simular validação própria.
            raise

    def preview(self):
        plan=self.dialogue._preview() if self.phase=='CONFIRM' else self.dialogue.executable_plan()
        return plan_report(plan,source=self.source_evidence,label=self.label)

    def cancel(self, reason='CANCELADO_PELO_MESTRE'):
        if self.committed or self.store.event(self.event_id) is not None:
            raise LocalHold('HOLD: efeito pode existir. Consultar WAL/recibo, não repetir.')
        current=self.store.get_all()
        if current != self.initial:
            raise LocalHold('HOLD: estado diverge antes de cancelar')
        save(self.folder/'RECIBO_CANCELAMENTO.json',{
            'schema':'LEVELUP-GUI-V03','status':'CANCELADO_SEM_APLICACAO',
            'reason':reason,'original_sha256':digest(self.initial),
            'current_sha256':digest(current),'transcript':self.transcript,
            'notion_writes':0,'canonical_certified':False})
        return True

    def commit(self):
        if self.phase!='READY':raise LocalHold('HOLD: é necessário CONFIRMO explícito')
        if self.committed:raise LocalHold('HOLD: já houve tentativa de commit')
        plan=self.dialogue.executable_plan()
        save(self.folder/'PREVIA_MOTOR.json',plan)
        save(self.folder/'COMPARACAO_ANTES_DEPOIS.json',{'before':plan['before'],
             'after':plan['updates'],'choices':plan.get('choices',{}),'status':'EXPERIMENTAL'})
        (self.folder/'COMPARACAO_ANTES_DEPOIS.txt').write_text(self.preview(),encoding='utf-8')
        # Um event_id único. Definir tentativa antes do runner previne retry cego.
        self.committed=True
        try:
            result=SafeLocalR17Runner(self.store).execute(self.dialogue)
            current=DurableStore(self.folder/'COPIA_LOCAL_3_DOCS').get_all()
            if (result['status']!='COMMITTED_LOCAL_VERIFIED' or
                digest(current)!=digest(plan['updates']) or current!=plan['updates']):
                raise LocalHold('HOLD: readback não corresponde ao plano')
            validate_r17(current)
            save(self.folder/'ESTADO_APLICADO.json',current)
            save(self.folder/'TRANSCRICAO_ENTRADAS_EXPERIMENTAIS.json',self.transcript)
            save(self.folder/'RECIBOS_ROLAGENS.json',self.dialogue.choices['roll_receipts'])
            if self.source_evidence:
                save(self.folder/'PROJECAO_SEM_REESCREVER_FICHA.json',{
                    'schema':'LEVELUP-PROJECAO-FIEL-V03',
                    'snapshot_original':self.source_evidence['snapshot'],
                    'snapshot_sha256':self.source_evidence['snapshot_sha256'],
                    'original_file_sha256':self.source_evidence['original_bytes_sha256'],
                    'field_provenance':self.source_evidence.get('field_provenance',{}),
                    'engine_projection_before':self.initial,'engine_projection_after':current,
                    'mechanical_source_authenticated':False,
                    'all_unknown_fields_kept_in_original':True,
                    'notion_write':False,'requires_human_reconciliation':True})
            receipt={'schema':'LEVELUP-GUI-V03','character':self.label,
                     'status':'EVOLUIDO_MANTIDO_EM_COPIA_LOCAL','event_id':self.event_id,
                     'target_level':self.dialogue.target_level,'before_sha256':digest(self.initial),
                     'after_sha256':digest(current),'confirmation':'CONFIRMO',
                     'readback_equal_plan':True,'rolled_receipts':len(self.dialogue.choices['roll_receipts']),
                     'rollback':'DISPONIVEL_NA_MESA','notion_writes':0,
                     'party_writes':0,'production_certified':False}
            save(self.folder/'RECIBO_EVOLUCAO.json',receipt)
            return receipt
        except Exception as exc:
            save(self.folder/'HOLD_VERIFICAR_ESTADO.json',{
                'error':type(exc).__name__+': '+str(exc),'event_id':self.event_id,
                'current_sha256':digest(self.store.get_all()),'automatic_retry':False})
            raise

    def restore(self):
        return restore_folder(self.folder)


def list_runs(root=APP_ROOT):
    runs=Path(root)/'execucoes'
    result=[]
    for folder in sorted(runs.glob('*'),reverse=True) if runs.exists() else []:
        receipt_path=folder/'RECIBO_EVOLUCAO.json'
        if not receipt_path.is_file():continue
        try:
            r=json.loads(receipt_path.read_text(encoding='utf-8'))
            result.append((folder,r))
        except (ValueError,OSError):
            result.append((folder,{'status':'HOLD_RECIBO_ILEGIVEL','character':folder.name}))
    return result


def read_run(folder):
    folder=Path(folder)
    r=json.loads((folder/'RECIBO_EVOLUCAO.json').read_text(encoding='utf-8'))
    initial=json.loads((folder/'ESTADO_INICIAL.json').read_text(encoding='utf-8'))
    after=json.loads((folder/'ESTADO_APLICADO.json').read_text(encoding='utf-8'))
    plan=json.loads((folder/'PREVIA_MOTOR.json').read_text(encoding='utf-8'))
    store=DurableStore(folder/'COPIA_LOCAL_3_DOCS')
    now=store.get_all()
    if (digest(initial)!=r['before_sha256'] or digest(after)!=r['after_sha256']
        or plan['before']!=initial or plan['updates']!=after
        or plan['event_id']!=r['event_id']):
        raise LocalHold('HOLD: histórico/plan/recibo divergentes')
    evt=store.event(r['event_id'])
    if not evt or evt['state']!='COMMITTED' or evt['intent_hash']!=r['after_sha256']:
        raise LocalHold('HOLD: WAL não confirma commit anterior')
    if r['status']=='EVOLUIDO_MANTIDO_EM_COPIA_LOCAL' and now!=after:
        raise LocalHold('HOLD: cópia atual difere da última evolução mantida')
    if r['status']=='EVOLUIDO_E_RESTAURADO_LOCAL' and now!=initial:
        raise LocalHold('HOLD: cópia restaurada diverge do original')
    source=None
    f=folder/'PROJECAO_SEM_REESCREVER_FICHA.json'
    if f.is_file():
        obj=json.loads(f.read_text(encoding='utf-8'))
        if obj['snapshot_sha256']!=__import__('adaptador_copia_local').canonical_sha(obj['snapshot_original']):
            raise LocalHold('HOLD: snapshot importado divergente')
        source={'snapshot':obj['snapshot_original']}
    return {'receipt':r,'comparison':plan_report(plan,source=source,label=r['character']),
            'current':now,'initial':initial,'after':after}


def restore_folder(folder):
    folder=Path(folder)
    view=read_run(folder)
    receipt=view['receipt']
    if receipt['status']!='EVOLUIDO_MANTIDO_EM_COPIA_LOCAL':
        raise LocalHold('HOLD: esta cópia não está marcada como MANTIDA')
    store=DurableStore(folder/'COPIA_LOCAL_3_DOCS')
    event=DurableController(store).explicit_rollback(receipt['event_id'])
    current=DurableStore(folder/'COPIA_LOCAL_3_DOCS').get_all()
    if event['state']!='COMMITTED' or current!=view['initial']:
        raise LocalHold('HOLD: restauração não corresponde ao estado original')
    save(folder/'ESTADO_RESTAURADO.json',current)
    receipt.update(status='EVOLUIDO_E_RESTAURADO_LOCAL',
                   rollback='ROLLED_BACK_VERIFIED_LOCAL',
                   rollback_sha256=digest(current),rollback_exact=True)
    save(folder/'RECIBO_EVOLUCAO.json',receipt)
    return receipt
