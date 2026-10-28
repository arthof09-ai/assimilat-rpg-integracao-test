import unittest
from levelup_engine import InvalidPlan
from layered_vital_v03 import (validate_layers, layer_display, damage_three_layers,
    project_form_change, project_after_level, candidate_spirit_shield_capacity,
    validate_attribute_rate_confirmation, mandatory_new_character_fields)

def L(n=50,nmax=100,item=20,imax=20,spirit=156,smax=156,transformed=True):
    return dict(normal_current=n,normal_max=nmax,item_current=item,item_max=imax,
                spirit_current=spirit,spirit_max=smax,transformed=transformed)

def confirmation(total='5', ok=True):
    return dict(character_id='SYNTHETIC',player_id='test-player',confirmed=ok,
                confirmed_at='TEST-TIMESTAMP',confirmed_points_per_level=total,
                statement='Confirmo 5 por nível, incluindo 2 racial e 3 de títulos',
                source='DIRECT_PLAYER_INPUT')

class TestLayeredVitalsV03(unittest.TestCase):
    def test_damage_example_180(self):
        p=damage_three_layers(L(),180)
        self.assertEqual(p['debit'],{'spirit':156,'item':20,'normal':4})
        self.assertEqual(p['after']['normal_current'],46)
        self.assertEqual(p['after']['spirit_current'],0)
        self.assertEqual(p['after']['item_current'],0)
    def test_damage_only_spirit(self):
        x=damage_three_layers(L(),10)
        self.assertEqual(x['debit'],{'spirit':10,'item':0,'normal':0})
        self.assertEqual(x['after']['spirit_current'],146)
    def test_damage_spirit_and_item(self):
        x=damage_three_layers(L(),170)
        self.assertEqual(x['debit'],{'spirit':156,'item':14,'normal':0})
        self.assertEqual(x['after']['item_current'],6)
    def test_untransformed_item_priority(self):
        x=damage_three_layers(L(transformed=False),23)
        self.assertEqual(x['debit'],{'spirit':0,'item':20,'normal':3})
        self.assertEqual(x['after']['spirit_current'],156)
    def test_switch_off_does_not_reset_layers(self):
        x=damage_three_layers(L(),25)['after']
        z=project_form_change(x,transformed=False,external_gate_checked=True)['after']
        self.assertEqual((z['normal_current'],z['item_current'],z['spirit_current']), (50,20,131))
    def test_switch_back_does_not_refill_spirit(self):
        z=damage_three_layers(L(),25)['after']
        z=project_form_change(z,transformed=False,external_gate_checked=True)['after']
        z=project_form_change(z,transformed=True,external_gate_checked=True)['after']
        self.assertEqual(z['spirit_current'],131)
    def test_cannot_change_without_scene_rest_gate(self):
        with self.assertRaises(InvalidPlan):project_form_change(L(),transformed=False,external_gate_checked=False)
    def test_level_up_no_refills_any_layer(self):
        z=project_after_level(L(n=50,item=7,spirit=123),new_normal_max=120,new_item_max=30,new_spirit_max=200)['after']
        self.assertEqual((z['normal_current'],z['item_current'],z['spirit_current']),(50,7,123))
        self.assertEqual((z['normal_max'],z['item_max'],z['spirit_max']),(120,30,200))
    def test_negative_damage_denied(self):
        with self.assertRaises(InvalidPlan):damage_three_layers(L(),-2)
    def test_overkill_is_not_silently_lost(self):
        x=damage_three_layers(L(n=1,item=2,spirit=3),15)
        self.assertEqual(x['damage_unabsorbed_after_zero'],9)
    def test_invalid_state_rejected(self):
        with self.assertRaises(InvalidPlan):validate_layers(L(spirit=157))
        with self.assertRaises(InvalidPlan):validate_layers(L(n=-1))
        with self.assertRaises(InvalidPlan):validate_layers({**L(), 'extra':'unknown'})
    def test_display_three_layers(self):
        self.assertIn('156/156 transformação',layer_display(L()))
        self.assertIn('(inativa)',layer_display(L(transformed=False)))
    def test_derived_shield_and_no_beast_subtraction(self):
        with self.assertRaises(InvalidPlan):candidate_spirit_shield_capacity(100,256)
        result=candidate_spirit_shield_capacity(100,256,t6_evidence=True)
        self.assertEqual(result['shield_max_candidate'],156)
        self.assertTrue(result['no_refresh_policy_inferred'])
    def test_transformed_below_normal_denied(self):
        with self.assertRaises(InvalidPlan):candidate_spirit_shield_capacity(100,80,t6_evidence=True)
    def test_player_confirmation_mandatory(self):
        with self.assertRaises(InvalidPlan):validate_attribute_rate_confirmation(character_id='SYNTHETIC',components=[
            {'source_id':'racial','points_per_level':2,'physically_verified':True}],player_confirmation={})
    def test_player_confirmation_matches_sources(self):
        r=validate_attribute_rate_confirmation(character_id='SYNTHETIC',components=[
            {'source_id':'race','points_per_level':'2','physically_verified':True},
            {'source_id':'title','points_per_level':'3','physically_verified':True,'retroactive':True}],
            player_confirmation=confirmation())
        self.assertEqual(r['normal_points_per_level'],'5')
        self.assertTrue(r['spirit_tap_must_be_separate'])
    def test_player_discrepancy_blocks(self):
        with self.assertRaises(InvalidPlan):validate_attribute_rate_confirmation(character_id='SYNTHETIC',components=[
            {'source_id':'race','points_per_level':2,'physically_verified':True}],player_confirmation=confirmation())
    def test_duplicate_source_blocks_double_count(self):
        with self.assertRaises(InvalidPlan):validate_attribute_rate_confirmation(character_id='SYNTHETIC',components=[
            {'source_id':'race','points_per_level':2,'physically_verified':True},
            {'source_id':'race','points_per_level':3,'physically_verified':True}],player_confirmation=confirmation())
    def test_unverified_source_blocks(self):
        with self.assertRaises(InvalidPlan):validate_attribute_rate_confirmation(character_id='SYNTHETIC',components=[
            {'source_id':'unconfirmed','points_per_level':5,'physically_verified':False}],player_confirmation=confirmation())
    def test_fractional_points_allowed_if_exact(self):
        c=confirmation('3.5')
        r=validate_attribute_rate_confirmation(character_id='SYNTHETIC',components=[
            {'source_id':'race','points_per_level':'2','physically_verified':True},
            {'source_id':'title','points_per_level':'1.5','physically_verified':True}],player_confirmation=c)
        self.assertEqual(r['normal_points_per_level'],'3.5')
    def test_no_float_rounding(self):
        with self.assertRaises(InvalidPlan):validate_attribute_rate_confirmation(character_id='SYNTHETIC',components=[
            {'source_id':'race','points_per_level':1.5,'physically_verified':True}],player_confirmation=confirmation('1.5'))
    def test_template_has_explicit_normal_rate(self):
        self.assertIn('progression_normal_points_per_level',mandatory_new_character_fields())
        self.assertIn('progression_titles_per_level_and_retroactivity',mandatory_new_character_fields())

if __name__=='__main__':unittest.main()
