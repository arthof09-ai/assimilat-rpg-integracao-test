from __future__ import annotations
import unittest
from fractions import Fraction as F
from r200_geometry import affected,freeze_parameters,preflight_cast,SpatialBlocked,SourceGap
class TestR200Space(unittest.TestCase):
    def test_A_single_at9(self):self.assertEqual(affected('single',(0,0),{'enemy':(9,0)},target='enemy')['hits'],['enemy'])
    def test_B_single_beyond9(self):self.assertFalse(affected('single',(0,0),{'enemy':(F(901,100),0)},target='enemy')['valid'])
    def test_C_cone_explicit_lab_wedge(self):
        q=affected('cone',(0,0),{'ahead':(4,0),'behind':(-1,0),'lateral':(1,3),'outside':(5,0)},
            specific={'half_angle_geometry':'TEST_WEDGE_SLOPE_1_TO_1','aperture_origin':'LAB_TEST_ONLY'},direction=(1,0))
        self.assertEqual(q['hits'],['ahead']);self.assertIn('LAB_CONE',q['mode'])
    def test_D_aoe_three(self):
        q=affected('circular',(0,0),{'A':(9,0),'B':(9,2),'C':(9,-2),'far':(17,0)},center=(9,0))
        self.assertEqual(set(q['hits']),{'A','B','C'});self.assertFalse(q['caster_in_area'])
    def test_E_caster_outside(self):self.assertFalse(affected('circular',(0,0),{'A':(9,0)},center=(9,0))['caster_in_area'])
    def test_F_caster_inside_included(self):
        q=affected('circular',(0,0),{'self':(0,0),'foe':(2,0)},center=(3,0));self.assertTrue(q['caster_in_area']);self.assertIn('self',q['hits'])
    def test_G_specific_precedence(self):self.assertEqual(freeze_parameters('single',{'range_m':F(4)})['range_m'],4)
    def test_H_partial_specific(self):
        q=freeze_parameters('circular',{'radius_m':F(2)})
        self.assertEqual((q['radius_m'],q['center_range_m']),(2,9))
    def test_I_unknown_shape_rejected(self):
        with self.assertRaises(SourceGap):freeze_parameters('multitarget_unspecified')
    def test_J_edges_exact(self):
        self.assertEqual(set(affected('circular',(0,0),{'edge':(15,0),'beyond':(F(1501,100),0)},center=(9,0))['hits']),{'edge'})
        self.assertEqual(affected('cone',(0,0),{'tip':(F(9,2),0),'beyond':(F(451,100),0)},direction=(1,0),specific={'half_angle_geometry':'TEST_WEDGE_SLOPE_1_TO_1','aperture_origin':'LAB_TEST_ONLY'})['hits'],['tip'])
    def test_K_invalid_no_pa(self):
        w={'source':'Notion','known_by':'caster','name':'whip','cost_pa':8,'kind':'single'}
        with self.assertRaises(SpatialBlocked):preflight_cast('caster',{'caster':(0,0),'wolf':(10,0)},spell=w,pa_free=91,already_spent_pa=0,target='wolf')
    def test_L_valid_preflight_cost_preserved(self):
        w={'source':'Notion','known_by':'caster','name':'whip','cost_pa':8,'kind':'single'}
        r=preflight_cast('caster',{'caster':(0,0),'wolf':(9,0)},spell=w,pa_free=91,already_spent_pa=0,target='wolf')
        self.assertTrue(r['preflight_no_debit']);self.assertEqual(r['cost_pa'],8)
    def test_cone_without_aperture_fail_closed(self):
        with self.assertRaises(SourceGap):affected('cone',(0,0),{'foe':(2,0)},direction=(1,0))
    def test_range_specific_overrides(self):
        self.assertFalse(affected('single',(0,0),{'t':(5,0)},specific={'range_m':4},target='t')['valid'])
if __name__=='__main__':unittest.main()
