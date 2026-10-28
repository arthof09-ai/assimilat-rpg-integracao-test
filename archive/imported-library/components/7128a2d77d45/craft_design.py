"""Aprimoramento prospectivo do desenho CRAFT H2/P2, SEM fabricação.

O antigo fatorial R47 exige fisicamente combinações potencialmente não
admissíveis (magia instalada sem fonte/P2). Este plano não reivindica
impossibilidade normativa: sinaliza feasibility UNKNOWN e requer autorização.
"""
from __future__ import annotations
import math

STAGES=(
  {'id':'C0','source':False,'p2':False,'own_spell':False, 'role':'controle inerte sem ingrediente'},
  {'id':'C1','source':True,'p2':False,'own_spell':False, 'role':'propriedade natural do ingrediente'},
  {'id':'C2','source':True,'p2':True,'own_spell':False, 'role':'diferença incremental da vedação sem instalar magia própria'},
  {'id':'C3','source':True,'p2':True,'own_spell':True, 'role':'efeito incremental após instalação própria'},
)
CONTRASTS={
  'natural_source_C1_minus_C0':('C1','C0'),
  'P2_increment_C2_minus_C1':('C2','C1'),
  'own_spell_C3_minus_C2':('C3','C2'),
}


def gate_plan(record):
    issues=[]
    src=record.get('source_identity_and_lot');oil=record.get('oil_identity_and_lot')
    if record.get('stage_feasibility_confirmed') is not True:issues.append('STAGE_FEASIBILITY_UNCONFIRMED')
    if record.get('matched_substrate_confirmed') is not True:issues.append('MATCHED_SUBSTRATE_UNCONFIRMED')
    if record.get('assay_readout_predefined') is not True:issues.append('ASSAY_READOUT_NOT_PREREGISTERED')
    if not src:issues.append('SOURCE_ID_LOT_UNVERIFIED')
    if not oil:issues.append('OIL_ID_LOT_UNVERIFIED')
    if record.get('p2_recipe_salt_resolved') is not True:issues.append('P2_SALT_AUTHORITY_PENDING')
    if record.get('p2_recipe_energy_stage_resolved') is not True:issues.append('P2_ENERGY_AUTHORITY_PENDING')
    if record.get('oil_recipe_reconciled') is not True:issues.append('OIL_FORMULA_AUTHORITY_PENDING')
    if record.get('installation_procedure_approved') is not True:issues.append('OWN_SPELL_INSTALLATION_UNAPPROVED')
    if not record.get('qualified_operator_id'):issues.append('OPERATOR_UNVERIFIED')
    if not record.get('instrument_calibration_id'):issues.append('INSTRUMENT_CALIBRATION_UNVERIFIED')
    if not record.get('independent_witness_id'):issues.append('WITNESS_UNVERIFIED')
    if record.get('qualified_operator_id') and record.get('qualified_operator_id')==record.get('independent_witness_id'):
        issues.append('WITNESS_NOT_INDEPENDENT')
    return {'gate':'HOLD_NO_PHYSICAL_APPLICATION' if issues else 'FORM_READY_EXTERNAL_AUTHENTICATION_REQUIRED',
       'blockers':sorted(issues),'plan_only':True, 'effect_magic_observed':False,'item_created':False,'PA_charged':False}


def evaluate_record(record, plan):
    """Descriptive differences only. No causal claims without validated material events."""
    pre=gate_plan(plan)
    if pre['blockers']:return {'status':'HOLD','contrasts':None,'blockers':pre['blockers']}
    rows=record.get('observations',[])
    by={s['id']:[] for s in STAGES}
    for x in rows:
        id_=x.get('arm')
        if id_ not in by: return {'status':'HOLD','contrasts':None,'blockers':['INVALID_ARM']}
        value=x.get('outcome')
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):return {'status':'HOLD','contrasts':None,'blockers':['INVALID_OBSERVATION_VALUE']}
        by[id_].append(float(value))
    if any(len(x)==0 for x in by.values()):return {'status':'HOLD','contrasts':None,'blockers':['MISSING_COMPARISON_ARM']}
    means={k:sum(v)/len(v) for k,v in by.items()}
    return {'status':'DESCRIPTIVE_ONLY_UNAUTHENTICATED','contrasts':{k:means[a]-means[b] for k,(a,b) in CONTRASTS.items()},
       'means':means,'n_by_arm':{k:len(v) for k,v in by.items()},
       'randomization_verified':False,'physical_evidence_authenticated':False,
       'own_spell_installed_proven':False,'effect_magic_observed':False,'PA_charged':False,'item_created':False}


def design_record():
    return {'name':'staged matched contrasts; not automatically full factorial',
       'stages':list(STAGES),'contrasts':CONTRASTS,
       'requires':['matched substrate for all arms','comparison outcome predefined and quantifiable',
           'time windows aligned','blinded assessor if feasible','separate witness from operator',
           'actual ingredient lots and chain of custody','authorized P2 recipe and oil source',
           'independent replication','external physical witness verification'],
       'claim_rules':{'software_test':'NOT_REAL_MAGIC','form_complete':'NOT_AUTHENTICATED',
         'ingredient_effect_observed':'NOT_PROOF_OF_OWN_SPELL','P2_increment_observed':'NOT_PROOF_OF_OWN_SPELL',
         'C3_minus_C2_positive':'DESCRIPTIVE_ONLY_UNTIL_CAUSAL_IDENTIFICATION_AND_ATTESTATION'},
       'other_R47_factorial_arms':'OPTIONAL_FEASIBILITY_CHECK_NOT_REQUIRED_AS_PHYSICAL_STAGES',
       'no_writes_to_party':True,'item_produced':False}

if __name__=='__main__':
    import json
    from pathlib import Path
    out=Path(__file__).resolve().parents[1]/'outputs'
    out.mkdir(exist_ok=True)
    (out/'craft_staged_preflight.json').write_text(json.dumps({'plan':design_record(),
          'current_preflight':gate_plan({})},ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    print('PASS design; H2/RC5 HOLD')
