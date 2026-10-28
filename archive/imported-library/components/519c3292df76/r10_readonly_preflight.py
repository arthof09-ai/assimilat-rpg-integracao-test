"""R10 science-side failure-mode contract, NOT a VLAB adapter or game authority.
Never claims scene canonicity, even when every supplied field is syntactically valid.
"""
from __future__ import annotations
from typing import Mapping,Any
CODES=(
 ('R10-DENY-01','SCENE_ID_UNKNOWN'),
 ('R10-DENY-02','NOTION_SOURCE_CHANGED_AFTER_FREEZE'),
 ('R10-DENY-03','LAB_WRITER_OR_INSTANCE_UNKNOWN'),
 ('R10-DENY-04','PA_FREE_MISSING_OR_TIMING_UNKNOWN'),
 ('R10-DENY-05','ACTION_PA_COST_UNKNOWN_NOT_ZERO'),
 ('R10-DENY-06','ACTION_SLOT_OR_BOOTS_BONUS_ACTION_UNMAPPED'),
 ('R10-DENY-07','REACTION_BUDGET_NOT_SIGNED'),
 ('R10-DENY-08','TARGET_MAP_OR_REACH_UNSPECIFIED'),
 ('R10-DENY-09','ATTRIBUTE_OR_PROF_DOUBLE_COUNT'),
 ('R10-DENY-10','RDF_ORDER_NOT_APPROVED'),
 ('R10-DENY-11','CRITICAL_ORDER_MISREAD'),
 ('R10-DENY-12','OTHER_CHARACTER_SOURCE_AUTHORIZATION_REUSED'),
 ('R10-DENY-13','SOURCE_STATUS_LAB_ASSUMPTION_PROMOTED_TO_CURRENT'),
 ('R10-DENY-14','STRICT_FALSE_AS_OFFICIAL'),
 ('R10-DENY-15','SCHEDULER_SEED_METADATA_CLAIMED_AS_RANDOMNESS'),
 ('R10-DENY-16','NO_INDEPENDENT_REPLAY_OR_NAC_PASS'),
)
LIU='0b4c2b324ede837cb6be818dc8e36010'
MACACO='301c2b324ede828caccb813d3979267a'

def inspect_science_packet(s:Mapping[str,Any]):
    """Report evidence gaps only; syntax success is never a canonical PASS.

    A full fixture here is synthetic protocol-simulation input and does not grant
    engine/ledger permission. No tool I/O, randomness or mutations.
    """
    fail=[]
    def add(i,when):
        if when:fail.append(dict(case_id=CODES[i][0],reason=CODES[i][1]))
    add(0,not isinstance(s.get('scene_id'),str) or not s.get('scene_id','').strip())
    add(1,s.get('source_hash_rechecked') is not True or s.get('source_frozen_by_owner') is not True)
    add(2,s.get('lab_instance_verified') is not True or s.get('writer_scope_verified') is not True)
    pa=s.get('pa_free')
    add(3,type(pa) is not int or pa<0 or s.get('pa_temporal_basis_signed') is not True)
    action_cost=s.get('pa_cost')
    add(4,type(action_cost) is not int or action_cost<0 or s.get('action_cost_source_verified') is not True)
    add(5,s.get('action_slot_mapped_to_official_economy') is not True or s.get('boots_bonus_action_resolved') is not True)
    add(6,type(s.get('reaction_available')) is not bool or s.get('reaction_window_source_verified') is not True)
    add(7,s.get('geometry_with_reach_los_signed') is not True)
    add(8,s.get('actor_stats_skill_components_audited') is not True or s.get('dodge_total_is_49_not_increment') is not True)
    add(9,s.get('rdf10_component_policy_master_approved') is not True)
    add(10,s.get('critical_rolls_ordered') is not True)
    add(11,s.get('actor_source_page_ids')!=[LIU,MACACO] or s.get('character_specific_grant_signed') is not True)
    add(12,s.get('source_status')!='SIGNED_CURRENT_NOTION_SCENE' or s.get('source_authority_validated') is not True)
    add(13,s.get('strict_flag') is not True or s.get('engine_support_strict_legitimately_proven') is not True)
    add(14,s.get('rng_engine_draws_replay_verified') is not True or s.get('rng_is_more_than_metadata') is not True)
    add(15,s.get('independent_nac_pass_02') is not True or s.get('independent_replay_verified') is not True)
    return dict(status='DENY_REQUIRES_COMPETENT_EVIDENCE' if fail else 'SCIENCE_SCHEMA_COMPLETE_BUT_NOT_AN_ENGINE_AUTHORIZATION',
      blockers=fail,count=len(fail),official_attack_executed=False,terminal_B01_B18_certifications_awarded=0,
      scene_canonical=False,external_governance_required=True)

if __name__=='__main__':
    from json import dumps
    print(dumps(inspect_science_packet({}),ensure_ascii=False,indent=2))
