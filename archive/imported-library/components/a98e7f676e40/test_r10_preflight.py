"""R10 16 independent negative branches; no actual Lab code or live character needed."""
import unittest
from r10_readonly_preflight import inspect_science_packet,CODES,LIU,MACACO

BASE=dict(scene_id='LAB-SYNTHETIC-CONTRACT-SCHEMA-NOT-CANON',source_hash_rechecked=True,source_frozen_by_owner=True,
    lab_instance_verified=True,writer_scope_verified=True,pa_free=73,pa_temporal_basis_signed=True,
    pa_cost=40,action_cost_source_verified=True,action_slot_mapped_to_official_economy=True,boots_bonus_action_resolved=True,
    reaction_available=True,reaction_window_source_verified=True,geometry_with_reach_los_signed=True,
    actor_stats_skill_components_audited=True,dodge_total_is_49_not_increment=True,rdf10_component_policy_master_approved=True,
    critical_rolls_ordered=True,actor_source_page_ids=[LIU,MACACO],character_specific_grant_signed=True,
    source_status='SIGNED_CURRENT_NOTION_SCENE',source_authority_validated=True,
    strict_flag=True,engine_support_strict_legitimately_proven=True,rng_engine_draws_replay_verified=True,rng_is_more_than_metadata=True,
    independent_nac_pass_02=True,independent_replay_verified=True)
# The 'BASE' is a positive-control TEST STUB, never signed by any authority.
CASE_OVERRIDE={
 0:{'scene_id':None},1:{'source_hash_rechecked':False},2:{'lab_instance_verified':None},
 3:{'pa_free':None},4:{'pa_cost':None},5:{'boots_bonus_action_resolved':None},
 6:{'reaction_available':None},7:{'geometry_with_reach_los_signed':False},
 8:{'dodge_total_is_49_not_increment':False},9:{'rdf10_component_policy_master_approved':False},
 10:{'critical_rolls_ordered':False},11:{'character_specific_grant_signed':False},
 12:{'source_status':'LAB-ASSUMPTION'},13:{'strict_flag':False},
 14:{'rng_is_more_than_metadata':False},15:{'independent_replay_verified':False},
}
class R10NegativePorts(unittest.TestCase):pass
for i in range(16):
 def mk(i):
  def check(self):
   s=dict(BASE,**CASE_OVERRIDE[i]);ret=inspect_science_packet(s)
   self.assertEqual(ret['status'],'DENY_REQUIRES_COMPETENT_EVIDENCE')
   self.assertIn(CODES[i][1],[x['reason'] for x in ret['blockers']]);self.assertFalse(ret['official_attack_executed'])
  return check
 setattr(R10NegativePorts,f'test_failclosed_{i+1:02d}',mk(i))

class R10PositiveStub(unittest.TestCase):
 def test_only_schema_ready_never_pass_or_fight(self):
  ret=inspect_science_packet(BASE)
  self.assertEqual(ret['status'],'SCIENCE_SCHEMA_COMPLETE_BUT_NOT_AN_ENGINE_AUTHORIZATION')
  self.assertEqual(ret['terminal_B01_B18_certifications_awarded'],0)
  self.assertFalse(ret['scene_canonical'])

if __name__=='__main__':unittest.main(verbosity=2)
