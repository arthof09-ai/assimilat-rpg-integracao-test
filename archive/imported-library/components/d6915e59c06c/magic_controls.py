"""Discriminatory TEST control deck; synthetic input != actual magic measurements.
No magical physics engine implemented or implied. Fail-closed by construction.
"""
from __future__ import annotations
import json
from .r48_pingente_adapter import CASE

DECK=(
 ('NEGATIVE_NO_MAGIC',False,False,True,26,'WITHOUT_MAGIC_SOURCE'),
 ('PARTIAL_LUMINANCE_ONLY',False,True,True,26,'NO_ACTIVE_CORE'),
 ('ENERGY_INSUFFICIENT',True,True,True,25,'TOTAL_26_PA_REQUIRED'),
 ('STABILIZATION_LOST',True,True,False,26,'RETENTION_OR_SUPPORT_FAILED'),
 ('COMPLETE_PAPER_DESIGN',True,True,True,26,'MAGIC_PROOF_MISSING'),
)

def evaluate(row:tuple)->dict:
    name,core,herb,stable,budget,reason=row
    if not core and not herb:status='NEGATIVE_CONTROL_NO_MAGIC_COMPONENT'
    elif not core:status='PARTIAL_LIGHT_ONLY_NO_ACTIVE_CORE'
    elif not herb:status='PARTIAL_CORE_ONLY_NO_PASSIVE_HERB'
    elif not herb:status='PARTIAL_CONTROL_NO_PASSIVE_SOURCE'
    elif not stable:status='REJECTED_SYNTHETIC_STABILITY'
    elif budget<26:status='REJECTED_SYNTHETIC_ENERGY_BUDGET'
    else:status='DOCUMENT_COMPLETE_MAGIC_UNOBSERVED'
    # Always no successful magic, even on positive candidate with 26 PA.
    return {'control_id':name,'input_kind':'SYNTHETIC_FIXTURE_NOT_OBSERVATION',
      'control_hypothesis':reason,'has_crystal_core':core,'has_herb':herb,
      'supports_stabilization_assumed':stable,'scenario_pa_budget_fixture':budget,
      'outcome':status,'factory_R48_executed':False,'magical_transfer_proven':False,
      'physical_measurements':None,'observed_ability':None,
      'required_discriminator':'measured light output and magic-darkness comparator, verified independent of recipe description'}

def run_deck()->dict:
    cases=[evaluate(x) for x in DECK]
    return {'case_id':CASE,'deck':cases,'count':len(cases),
      'result_kind':'LOGICAL_GATE_EXECUTED; NO_MAGIC_EXPERIMENT_OR_REAL_R48_COMMIT',
      'none_falsely_approved':all(not a['magical_transfer_proven'] for a in cases),
      'physical_magic_verified':0}
