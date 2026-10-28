"""Evidence-sensitive maturity overlay on existing REC-EXEC auditor, no new authority.
Never derives physical or official RC5 from a populated form, simulated sensor,
PA correctness or a TEST factory ledger. External verification must be independent.
"""
from __future__ import annotations
import copy,hashlib,json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
QA_SOURCE=BASE/'vendor/recipe_qa.py'

def load_existing_qa():
    from importlib.util import spec_from_file_location,module_from_spec
    spec=spec_from_file_location('original_craft_qa_v1',QA_SOURCE)
    mod=module_from_spec(spec);spec.loader.exec_module(mod);return mod

def qualify(recipe:dict,pa_gate:dict,r48_admission:dict,independent_magic_measurement:dict|None=None) -> dict:
    qa=load_existing_qa().audit(recipe)
    documentary=qa['rc_ceiling_test']
    pa_ok=(pa_gate.get('pa_version_compatible') is True and
      pa_gate.get('pa_provider_reported_total_not_approved',{}).get('pa_por_dia')==12 and
      pa_gate.get('pa_provider_reported_total_not_approved',{}).get('pa_ativacoes_no_cenario')==14)
    r48_verified=(r48_admission.get('original_engine_invoked') is True and
        r48_admission.get('r48_receipt') is not None and
        r48_admission.get('status')=='RECEIPT_VERIFIED_IN_LAB')
    # IMPORTANT: no locally signed fixture is sufficient to prove a physical magical
    # mechanism. No independent magical authority/verifier is currently installed.
    magic_verifier_installed=False
    magic_valid=False
    if independent_magic_measurement is not None:
        # Explicitly reject semantic self-assertion "verified=true" from untrusted JSON.
        magic_valid=False
    material_rc5=(documentary=='RC5' and pa_ok and r48_verified and
                 magic_verifier_installed and magic_valid)
    reasons=[]
    if documentary!='RC5': reasons.append('REC_EXEC_DOCUMENTARY_INCOMPLETE')
    if not pa_ok: reasons.append('PA_RECEIPT_UNVERIFIED_OR_MISMATCH')
    if not r48_verified: reasons.append('R48_PINGENTE_RECEIPT_NOT_VERIFIED')
    if not magic_verifier_installed: reasons.append('INDEPENDENT_MAGICAL_MEASUREMENT_VERIFIER_NOT_INSTALLED')
    if not magic_valid: reasons.append('MAGICAL_TRANSFORMATION_RETENTION_NOT_VERIFIED')
    if recipe.get('manufacture',{}).get('approved_units') is None:reasons.append('NO_APPROVED_MEASURED_YIELD')
    if recipe.get('control',{}).get('economy',{}).get('status')=='PENDING': reasons.append('CTE_UTE_UNVERIFIED')
    if any(x['classification'].startswith('MATERIAL_PS') for x in recipe.get('bom',[])):
        reasons.append('PS_RESOURCE_JIT_AND_QUALITY_PENDING')
    reasons=list(dict.fromkeys(reasons))
    return {
      'schema':'CRAFT-REC-EXEC-PROOF-OVERLAY-v1.3-TEST',
      'case_id':recipe.get('case_id'), 'static_auditor_original':qa['engine'],
      'static_documentary_ceiling':documentary,
      'static_findings':[{'code':f['code'],'severity':f['severity']} for f in qa['findings']],
      'pa_provider_compatible':pa_ok,'r48_observed_receipt':r48_verified,
      'independent_magical_verifier_installed':magic_verifier_installed,
      'magic_independently_proven':magic_valid,
      'approved_units_measured':recipe.get('manufacture',{}).get('approved_units'),
      'maximum_indicative_operational_state':documentary,
      'official_RC5':material_rc5, 'PS_P4_promoted':False,
      'f5_production_authorized':False,'party_write':False,
      'blocks':reasons, 'status':'TEST_ONLY_CANNOT_GRANT_RC5'}
