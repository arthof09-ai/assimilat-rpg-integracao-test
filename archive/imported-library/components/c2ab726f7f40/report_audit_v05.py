"""Player-safe evolution report validator, per IBX-17 readback requirements.

Separate complete change manifest from user-facing text. If a changed property is
not in the report, or secret Mestre keys appear, stop communication.
"""
from __future__ import annotations
import re

class ReportHold(ValueError):pass
SECRET_TERMS=(r'\bBAP\b',r'\bMESTRE_ONLY\b',r'\bwriter(?:_|\b)',r'\blease\b',r'\bhidden[_ -]?seed\b',r'\btechnique[_-]?source\b')


def validate_player_report(*,before:dict,after:dict,report_fields:dict,
                           written_field_keys:set,detail:str)->dict:
    """Only pass if every mutated field has an exhaustive before→after entry.

    No game-semantic decisions are inferred from missing input.
    """
    if not isinstance(before,dict) or not isinstance(after,dict) or not isinstance(report_fields,dict):
        raise ReportHold('Snapshot completo obrigatório')
    if set(before)!=set(after):raise ReportHold('Chaves mudaram inesperadamente: não inventar comparação')
    changed={k:(before[k],after[k]) for k in before if before[k]!=after[k]}
    if changed and set(changed)!=set(report_fields):
        missing=set(changed)-set(report_fields)
        over=set(report_fields)-set(changed)
        raise ReportHold(f'Relatório não cobre exatamente os campos alterados: faltam={sorted(missing)}, extras={sorted(over)}')
    if changed and set(changed)!=set(written_field_keys):
        raise ReportHold('Touch-set físico e manifesto do relatório divergem')
    for k, pair in changed.items():
        if report_fields[k] != {'before':pair[0],'after':pair[1]}:
            raise ReportHold(f'Antes/depois inconsistente: {k}')
    scrub=str(detail)+' '.join(str(x) for x in report_fields)
    if any(re.search(p,scrub,re.I) for p in SECRET_TERMS):
        raise ReportHold('Informação Mestre-only/protocolo interno detectada')
    if changed and len(detail.strip())<20:raise ReportHold('Relatório deve ser claro e legível à player')
    return {'status':'PLAYER_REPORT_COVERAGE_PASS_OFFLINE','changed':len(changed),
            'field_names':sorted(changed),'material_readback_witnessed':False,
            'safe_to_send_to_party':False,
            'reason':'Party-safe content alone is not authorization to publish; depends on final NAC-PASS'}


def pa_spend_policy_guard(*,normal_pa_available:int,spirit_pa_available:int,
                          technique_cost:int,explicit_policy:str|None):
    """No invented ordering of normal-vs-spirit PA. Both sources are real PA."""
    if any(type(x)is not int or x<0 for x in (normal_pa_available,spirit_pa_available,technique_cost)):
        raise ReportHold('PA inválido')
    if spirit_pa_available and technique_cost>0 and explicit_policy not in ('SPIRIT_FIRST','NORMAL_FIRST','EXPLICIT_SPLIT'):
        return {'status':'HOLD_NO_CANONICAL_PA_SPEND_PRIORITY','cost':technique_cost,
                'normal_available':normal_pa_available,'spirit_available':spirit_pa_available,
                'no_payment_performed':True}
    if technique_cost>normal_pa_available+spirit_pa_available:
        return {'status':'HOLD_INSUFFICIENT_TOTAL_PA','no_payment_performed':True}
    return {'status':'VALIDATE_POLICY_SOURCE_FIRST','requested_policy':explicit_policy,
            'no_payment_performed':True,'no_automatic_spend':True}
