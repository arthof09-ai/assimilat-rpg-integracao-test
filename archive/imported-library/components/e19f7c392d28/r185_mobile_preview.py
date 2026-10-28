"""LEVEL-UP IBX-17 R185: mobile-first READ-ONLY preview, no confirmation token.

Reuses the R172 conversational dispatcher; caller supplies *documented* fields.
Only computes ordinal target; changed stats demand source-provenance, not guesses.
"""
from __future__ import annotations
from dataclasses import dataclass
from r172_conversational_readonly_dispatch import FixtureContext,query as dispatch

RANKS=('Bronze','Prata','Ouro','Ouro Negro','Lendário')
class PreviewHold(ValueError): pass

@dataclass(frozen=True)
class ReadonlyCharacter:
    name:str
    target_id:str
    parent_id:str
    physical_version:str
    source_version:str
    ordinal:int
    stats:dict
    provenance:dict
    scope:str='LAB_TEST'

def rank_label(ordinal):
    if not isinstance(ordinal,int) or isinstance(ordinal,bool) or not 1<=ordinal<=25:
        raise PreviewHold('LEVEL_OUT_OF_CANONICAL_1_25_RANGE')
    return f'{RANKS[(ordinal-1)//5]} {((ordinal-1)%5)+1}'

def preview_two_levels(snapshot:ReadonlyCharacter,verified_deltas=None):
    if snapshot.scope!='LAB_TEST' or snapshot.parent_id!='3fbc2b324ede804a95fafcb7b293c92c':
        return {'state':'HOLD_OUTSIDE_LAB','write_authorized':False}
    if not all((snapshot.name,snapshot.target_id,snapshot.physical_version,snapshot.source_version)):
        return {'state':'HOLD_SOURCE_MISSING','write_authorized':False}
    if not isinstance(snapshot.stats,dict) or not isinstance(snapshot.provenance,dict):
        return {'state':'HOLD_BAD_SNAPSHOT','write_authorized':False}
    destination=snapshot.ordinal+2
    if destination>25 or snapshot.ordinal<1:
        return {'state':'HOLD_LEVEL_OUT_OF_RANGE','write_authorized':False}
    core=dispatch('level up',FixtureContext(target_id=snapshot.target_id,parent_id=snapshot.parent_id,
                                           physical_version=snapshot.physical_version,source_version=snapshot.source_version))
    if core['state']!='AWAITING_CHOICE_OR_PREVIEW':
        return {'state':'HOLD_DISPATCHER','write_authorized':False}
    before=rank_label(snapshot.ordinal);after=rank_label(destination)
    deltas=verified_deltas or {}
    changes={}
    for field,item in deltas.items():
        if field not in snapshot.stats or not isinstance(item,dict):raise PreviewHold('UNBOUND_FIELD')
        if item.get('before')!=snapshot.stats[field] or 'after' not in item or not item.get('source_id'):
            raise PreviewHold('DELTA_WITHOUT_SOURCE_OR_BEFORE_MISMATCH')
        changes[field]={'antes':item['before'],'depois':item['after'],'fonte':item['source_id']}
    needs=('distribuição de pontos de atributo','rolagem ou 60% fixo quando previsto',
           'marcos FF ainda não consumidos','TAP e teto do Espírito','derivados e itens condicionais')
    return {'state':'PREVIEW_READONLY_REQUIRES_CHOICES','character':snapshot.name,
            'level_before':before,'level_after':after,'steps':[rank_label(snapshot.ordinal+1),after],
            'verified_changes':changes,'decisions_pending':needs,'unverified_derived_values':'PENDENTE',
            'natural_language':f'{snapshot.name}: de {before} para {after} (dois níveis). Esta é apenas uma prévia.',
            'human_confirmation':'NOT_ATTESTED','native_effects':0,'write_authorized':False,
            'party_safe_output_authorized':False,'read_version':snapshot.physical_version,
            'source_version':snapshot.source_version}


def mobile_chat_turn(message:str,snapshot:ReadonlyCharacter|None,verified_deltas=None):
    """Natural-language READ-ONLY entrypoint for the requested two-level UX.

    Distinguishes a human request from human *confirmation*: conversation text
    is NOT a provider-authenticated consent token and cannot trigger writes.
    """
    import unicodedata,re
    if not isinstance(message,str):
        return {'state':'CLARIFY_INTENT','write_authorized':False}
    normalized=''.join(c for c in unicodedata.normalize('NFKD',message.lower()) if not unicodedata.combining(c))
    if re.search(r'\b(cancelar|cancela|desistir|desisto)\b',normalized):
        return {'state':'CANCELED_NO_WRITE','write_authorized':False,'native_effects':0}
    if re.search(r'\b(confirmo|confirmar|aprovado|pode aplicar|execute)\b',normalized):
        return {'state':'AWAITING_TRUSTED_HOST_CONFIRMATION','write_authorized':False,'native_effects':0}
    pattern=r'\b(?:subir|subo|aumentar|upar|evoluir|passar|passei)\b.*?\b(?:2|dois|duas)\s+(?:niveis|levels|level|nivel)\b'
    if not re.search(pattern,normalized):
        return {'state':'CLARIFY_LEVEL_REQUEST','write_authorized':False}
    if snapshot is None:
        return {'state':'AWAITING_SOURCE_BOUND_CHARACTER_SNAPSHOT','requested_levels':2,
                'message':'Informe a ficha ou selecione uma réplica TEST para leitura.',
                'write_authorized':False,'native_effects':0}
    return preview_two_levels(snapshot,verified_deltas)
