"""IBX-17/R42 additive preview/decision bridge to EXISTING engine.

Not a level formula and not a Notion writer. An authenticated historical engine
callback supplies all game deltas. This layer enforces source receipts and
produces auditable before/after effects and guarded decision states.
"""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Callable
from ibx17_r41_item_provenance import EvidenceHold, sha256

LEVEL_UP='LEVEL_UP'
LEVEL_DOWN='LEVEL_DOWN_CORRECAO_SEM_PERDER_NIVEL'
REQUIRED_DOMAINS=(
    'atributos_naturais','equipamentos_bonus','titulos','vida','alma_PA',
    'FF_marcos','CA_defesas','ataques_dano','pericias_acerto','magias',
    'transformacao','rolagens_historico','blocos_midias','sincronizacao_master_party')
VALID={'ALTERA','NAO_ALTERA_VERIFICADO','PENDENTE'}


def _hash(record: dict) -> str:
    return sha256(json.dumps(record, sort_keys=True, ensure_ascii=False,separators=(',',':')))


def _check_source(source:dict):
    for k in ('page_id','surface','source_sha256','captured_at','original_page_url'):
        if not source.get(k):raise EvidenceHold('SOURCE_RECEIPT_MISSING:'+k)
    if source['surface'] not in ('MESTRE_TEST','MESTRE_MIRROR_READ_ONLY','PARTY_READ_ONLY'):
        raise EvidenceHold('UNKNOWN_SURFACE')


def _check_impact(impact:dict):
    if set(impact)!=set(REQUIRED_DOMAINS):raise EvidenceHold('IMPACT_DOMAIN_COVERAGE_INCOMPLETE')
    for domain,val in impact.items():
        if not isinstance(val,dict) or val.get('status') not in VALID:
            raise EvidenceHold('IMPACT_STATUS_UNKNOWN:'+domain)
        if not val.get('source_ref') or not val.get('explanation'):
            raise EvidenceHold('IMPACT_UNGROUNDED:'+domain)


def preview(*,source:dict,before:dict,change:dict,impact:dict,
            historical_engine:Callable,engine_receipt:dict) -> dict:
    _check_source(source);_check_impact(impact)
    if change.get('action') not in (LEVEL_UP,LEVEL_DOWN):raise EvidenceHold('UNKNOWN_LEVEL_OPERATION')
    if any(x['status']=='PENDENTE' for x in impact.values()):raise EvidenceHold('PENDING_IMPACT_GATE')
    for key in ('engine_name','version','source_sha256','rule_ref'):
        if not engine_receipt.get(key):raise EvidenceHold('HISTORIC_ENGINE_RECEIPT_MISSING:'+key)
    if not callable(historical_engine):raise EvidenceHold('HISTORIC_ENGINE_UNAVAILABLE')
    if not isinstance(before,dict) or not before:raise EvidenceHold('BEFORE_SHEET_INCOMPLETE')
    original=deepcopy(before)
    after=historical_engine(deepcopy(before),deepcopy(change),deepcopy(engine_receipt))
    if not isinstance(after,dict):raise EvidenceHold('ENGINE_INVALID_OUTPUT')
    if before!=original:raise EvidenceHold('INPUT_MUTATED_BY_ENGINE')
    if set(before)!=set(after):raise EvidenceHold('UNDECLARED_FIELDS_CREATED_OR_LOST')
    if 'level' not in before or 'level' not in after:raise EvidenceHold('LEVEL_FIELD_MISSING')
    if change['action']==LEVEL_DOWN and before['level']!=after['level']:
        raise EvidenceHold('LEVEL_DOWN_CANNOT_LOSE_LEVEL')
    if change['action']==LEVEL_UP and after['level']!=before['level']+1:
        raise EvidenceHold('LEVEL_UP_NOT_EXACTLY_ONE_LEVEL')
    deltas={k:{'before':before[k],'after':after[k]} for k in before if before[k]!=after[k]}
    if change['action']==LEVEL_UP and 'level' not in deltas:raise EvidenceHold('NO_LEVEL_UP')
    if not deltas:raise EvidenceHold('NO_ACTUAL_CHANGE')
    result={'source':source,'change':change,'engine_receipt':engine_receipt,
            'before':before,'after':after,'impact':impact,'field_deltas':deltas,
            'preimage_sha256':_hash(before),'postimage_sha256':_hash(after),
            'status':'PREVIEW_ONLY_REVIEW_REQUIRED','notion_writes':0,
            'official_character_changed':False}
    result['preview_sha256']=_hash(result)
    return result


def approval_decision(plan:dict, *, approved:bool, authorized_scope:str,
                      current_source_sha256:str, production_gate:bool=False):
    if _hash({k:v for k,v in plan.items() if k!='preview_sha256'})!=plan.get('preview_sha256'):
        return 'HOLD_PREVIEW_TAMPERED'
    if not approved:return 'REFUSED_NO_WRITE'
    if current_source_sha256!=plan['source']['source_sha256']:return 'HOLD_SOURCE_DRIFT'
    if authorized_scope=='MESTRE_TEST' and plan['source']['surface']=='MESTRE_TEST':
        return 'TEST_APPROVAL_ELIGIBLE_FOR_NATIVE_GATE'
    if not production_gate:return 'HOLD_OFFICIAL_APPROVAL_AND_NAC_PASS_MISSING'
    return 'HOLD_NATIVE_WRITER_INTEGRITY_AND_INDEPENDENT_APPROVAL'


def replay_plan(plan:dict, *, observed_before_sha256:str|None=None,
                observed_after_sha256:str|None=None):
    if observed_after_sha256==plan['postimage_sha256']:return 'NOOP_ALREADY_APPLIED'
    if observed_before_sha256==plan['preimage_sha256']:return 'PREVIEW_REAPPROVAL_AND_LIVE_SOURCE_REQUIRED'
    return 'HOLD_UNKNOWN_EFFECT_REOPEN_SOURCE'
