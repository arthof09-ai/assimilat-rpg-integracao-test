"""IBX-17 R61 additive Notion TEST-only projection/readback guard.

No Notion network calls or engine logic. Uses original R17/R30 output, not a new
level-up calculation engine. Source page editing, Party and production unsupported.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import re

LAB_PARENT = '3fbc2b324ede804a95fafcb7b293c92c'
MARKER = '## ESTADO ATIVO — PROJEÇÃO NOTION'
BOUNDARY = '## PROVENIÊNCIA'

FIELDS = ('ENGINE_EVENT','ENGINE_FULL_STATE_SHA256','TRANSACTION_STATUS',
          'NIVEL','FOR','DES','CON','INT','SAB','CAR','VIDA_MAX',
          'VIDA_ATUAL','PA_MAX','PA_ATUAL','PA_COMPROMETIDO','CA','FF',
          'CD_MAGICA','TAP_NIVEL_EFETIVO','TAP_OVERLAY_FOR',
          'TAP_OVERLAY_SAB','TAP_OVERLAY_DES','TAP_OVERLAY_CON','FF_LOCK_COUNT')

class ProjectionHold(ValueError):
    pass


def parse_active(doc: str) -> dict[str,str]:
    if not isinstance(doc,str) or doc.count(MARKER)!=1 or doc.count(BOUNDARY)!=1:
        raise ProjectionHold('ACTIVE_BLOCK_AMBIGUOUS')
    block=doc.split(MARKER,1)[1].split(BOUNDARY,1)[0]
    items=re.findall(r'^([A-Z_0-9]+): ([^\n]+)$',block,re.M)
    keys=[k for k,_ in items]
    if len(keys)!=len(set(keys)):raise ProjectionHold('DUPLICATE_ACTIVE_FIELD')
    if not {'ENGINE_EVENT','ENGINE_FULL_STATE_SHA256','TRANSACTION_STATUS'}<=set(keys):
        raise ProjectionHold('MISSING_IDENTITY')
    return dict(items)


def make_expected(full_state:dict[str,Any], event_id:str, state_hash:str, status:str, kind:str)->dict[str,str]:
    if kind not in ('UP','DOWN') or not re.fullmatch(r'[a-f0-9]{64}',state_hash):
        raise ProjectionHold('BAD_KIND_OR_HASH')
    n=full_state['NORMAL']; tr=full_state['TRANSFORM']; locks=full_state['LOCKS'];attrs=n['attrs']
    payload={'ENGINE_EVENT':event_id,'ENGINE_FULL_STATE_SHA256':state_hash,
             'TRANSACTION_STATUS':status,'NIVEL':str(n['level']),
             'FOR':str(attrs['FOR']),'DES':str(attrs['DES']),'CON':str(attrs['CON']),
             'INT':str(attrs['INT']),'SAB':str(attrs['SAB']),'CAR':str(attrs['CAR']),
             'VIDA_MAX':str(n['hp_max']),'VIDA_ATUAL':str(n['hp_current']),
             'PA_MAX':str(n['pa_max']),'PA_ATUAL':str(n['pa_current']),
             'PA_COMPROMETIDO':str(n['pa_committed']),'CA':str(n['derived']['ca']),
             'FF':str(n['derived']['ff']),'CD_MAGICA':str(n['derived']['magic_cd']),
             'TAP_NIVEL_EFETIVO':str(tr['effective_level']),
             'FF_LOCK_COUNT':str(len(locks['milestones']))}
    if kind=='UP':
        payload['TAP_OVERLAY_FOR']=str(tr['attrs']['FOR'])
        payload['TAP_OVERLAY_SAB']=str(tr['attrs']['SAB'])
    else:
        payload['TAP_OVERLAY_DES']=str(tr['attrs']['DES'])
        payload['TAP_OVERLAY_CON']=str(tr['attrs']['CON'])
    return payload


def validate(actual: dict[str,str], expected: dict[str,str])->None:
    if actual!=expected:
        differences={k:(expected.get(k),actual.get(k)) for k in set(expected)|set(actual)
                     if expected.get(k)!=actual.get(k)}
        raise ProjectionHold('READBACK_MISMATCH:'+repr(differences))


def plan_patch(document:str, before:dict[str,str],after:dict[str,str], *,
               page_parent:str,source_is_official:bool=False)->tuple[str,str]|None:
    if page_parent != LAB_PARENT or source_is_official:
        raise ProjectionHold('OUTSIDE_TEST_LAB')
    curr=parse_active(document)
    if curr == after: return None # verified idempotent NOOP
    validate(curr,before)
    before_lines=[f'{key}: {v}' for key,v in before.items()]
    after_lines=[f'{key}: {v}' for key,v in after.items()]
    old=MARKER+'\n'+'\n'.join(before_lines)
    new=MARKER+'\n'+'\n'.join(after_lines)
    if document.count(old)!=1:
        raise ProjectionHold('PATCH_NOT_CONTIGUOUS_OR_MULTIPLE_MATCHES')
    return old,new


def verify_archived(document:str,event_id:str,old_hash:str)->None:
    if 'ARQUIVO NATIVO' not in document or old_hash not in document.split('ARQUIVO NATIVO',1)[1]:
        raise ProjectionHold('HISTORY_MISSING_OR_WRONG')
    if event_id not in document:raise ProjectionHold('EVENT_MISSING')
