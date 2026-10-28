"""Fail-closed publication gate for CRAFT lab results; NOT a recipe/fabrication motor.
Never constructs, emulates, or trusts claims of material certification.
"""
from __future__ import annotations
import copy

REQUIRED=['r46_real_report','r47_real_attestation','source_mechanical_rendition',
          'magic_transfer_observation','real_lot_provenance','safe_point_writer',
          'c19_021_reconciled','fencing_effective','explicit_craft_f5_green',
          'nac_pass_productive']

def decide(proof:dict)->dict:
    if not isinstance(proof,dict):raise TypeError('REQUIRES_PROOF_OBJECT')
    # Fixture flags are not verifications. These fields require INDEPENDENT authenticated evidence
    # and an authorized gate, not assertions in a report or user-controllable JSON.
    statuses={k: 'NOT_VERIFIED' for k in REQUIRED}
    for k in REQUIRED:
        candidate=proof.get(k)
        # No claims in the lab input can self-authorize genuine external attestation.
        if candidate is not None:statuses[k]='CLAIM_UNVERIFIED_NEEDS_AUTHORITATIVE_READBACK'
    return {'status':'HOLD_MATERIAL_UNVERIFIED','RC5':False,'P4':False,
            'official_fabrication':False,'missing_authoritative_proofs':statuses,
            'reason':'R48/R44 simulated PASS, input fields and fake fixture signatures cannot prove material/magic/production authorization',
            'no_Party_or_First_write':True}
