import unittest
from hashlib import sha256
from levelup_engine import InvalidPlan
from transform_contract_v04 import (fixed_die_value, progress_max,extra_from_maxima,compute_transform_bonus,
  validate_resource_state,damage,deactivate,level_up_maxima,activate_verified,new_ledger,from_levelup_engine_preview)
from adapter_patch_planner_v04 import plan_minimal_field_patch


def state(*,normal_now=50,normal_max=100,item_now=20,item_max=20,spirit_now=0,spirit_max=156,
          transformed=False,pa_now=25,pa_max=50,pa_spirit_now=0,pa_spirit_max=100):
    return dict(normal_current=normal_now,normal_max=normal_max,item_current=item_now,item_max=item_max,
                spirit_current=spirit_now,spirit_max=spirit_max,transformed=transformed,
                pa_normal_current=pa_now,pa_normal_max=pa_max,
                pa_spirit_current=pa_spirit_now,pa_spirit_max=pa_spirit_max)

def activate(s,ledger,*,scene='S1',event='E1',rest=None,actor='A',spirit='SP'):
    return activate_verified(s,ledger,actor_id=actor,scene_id=scene,event_id=event,
             spirit_id=spirit,new_spirit_hp_max=156,new_spirit_pa_max=100,
             verified_rest=rest,activation_cost_paid_evidence='PREPAID-PROOF',provenance='SYNTHETIC-VERIFIED')

def short_rest(after=1,id='REST1',hours='4.5'):
    return dict(rest_id=id,kind='SHORT',completed=True,verified=True,
                after_activation_seq=after,duration_hours=hours)

class TestV04(unittest.TestCase):
    def test_d12_remains_7(self):
        self.assertEqual(fixed_die_value(12),7)
        self.assertEqual((fixed_die_value(10),fixed_die_value(12)),(6,7))
    def test_all_fixed_values(self):
        self.assertEqual([fixed_die_value(x) for x in (6,8,10,12,20,30,40,50,60)],
                         [4,5,6,7,12,18,24,30,36])
    def test_exact_1000_minus_300(self):
        x=extra_from_maxima(300,500,1000,1000,source_verified=True)
        self.assertEqual((x['vida_espiritual_temporaria'],x['alma_pa_adicional']),(700,500))
    def test_floor_when_normal_exceeds_transform(self):
        x=extra_from_maxima(1000,1000,500,500,source_verified=True)
        self.assertEqual(x['vida_espiritual_temporaria'],0)
        self.assertEqual(x['alma_pa_adicional'],0)
    def test_maxima_require_evidence(self):
        with self.assertRaises(InvalidPlan):extra_from_maxima(100,100,200,200,source_verified=False)
    def test_preview_delta_requires_physical_evidence(self):
        sample={'status':'SIMULATED_PREVIEW_ONLY','source_snapshot_sha256':'synthetic',
                'normal':{'Vida':300,'Alma_PA_Total':500},
                'transform':{'Vida':1000,'Alma_PA_Total':1000}}
        with self.assertRaises(InvalidPlan):
            from_levelup_engine_preview(sample,evidence_reconciled=False)
        result=from_levelup_engine_preview(sample,evidence_reconciled=True)
        self.assertEqual(result['delta']['vida_espiritual_temporaria'],700)
        self.assertEqual(result['delta']['alma_pa_adicional'],500)
    def test_preview_without_spirit_denied(self):
        with self.assertRaises(InvalidPlan):
            from_levelup_engine_preview({'status':'SIMULATED_PREVIEW_ONLY',
                 'normal':{'Vida':100,'Alma_PA_Total':100},'transform':None},
                 evidence_reconciled=True)
    def test_ouro_1_fixed_60_transform(self):
        # level 11, d12=7. initial 10 +11*(7+20)=307.
        x=progress_max(ordinal_level=11,initial_base=10,con_or_int_intrinsic=20,
                       transform=True,source_id='SYNTHETIC')
        self.assertEqual((x['die'],x['die_fixed'],x['derived_max']),(12,7,307))
    def test_ouro_base_diff_exact(self):
        x=compute_transform_bonus(ordinal_level=11,race_vida_shift=0,race_alma_shift=0,
                                  initial_vida=10,initial_alma=10,transformed_con=20,
                                  transformed_int=30,normal_vida_max=200,normal_alma_max=300,
                                  spirit_cap_level=21,verified_source_id='SYNTHETIC')
        self.assertEqual(x['bonus']['vida_espiritual_temporaria'],107)
        self.assertEqual(x['bonus']['alma_pa_adicional'],117)
    def test_weaker_spirit_requires_manual_evidence(self):
        with self.assertRaises(InvalidPlan):
            compute_transform_bonus(ordinal_level=16,race_vida_shift=0,race_alma_shift=0,
                                    initial_vida=10,initial_alma=10,transformed_con=20,
                                    transformed_int=30,normal_vida_max=300,normal_alma_max=400,
                                    spirit_cap_level=10,verified_source_id='SYNTHETIC')
    def test_ouro_negro_transformation_d20_not_d12(self):
        r=progress_max(ordinal_level=16,initial_base=10,con_or_int_intrinsic=20,
                       transform=True,source_id='SYNTHETIC')
        self.assertEqual((r['die'],r['die_fixed'],r['derived_max']),(20,12,522))
    def test_corrupted_event_sequence_denied(self):
        a=activate(state(),new_ledger('A'))
        s=deactivate(a['after'])['after']
        ledger=a['ledger'];ledger['events'][0]['seq']='bad'
        with self.assertRaises(InvalidPlan):activate(s,ledger,scene='S2',event='E2',rest=short_rest())
    def test_spirit_once_in_scene(self):
        a=activate(state(),new_ledger('A'));s=deactivate(a['after'])['after']
        with self.assertRaises(InvalidPlan):activate(s,a['ledger'],scene='S1',event='E2',rest=short_rest())
    def test_same_scene_rest_cannot_reset(self):
        a=activate(state(),new_ledger('A'));s=deactivate(a['after'])['after']
        with self.assertRaises(InvalidPlan):activate(s,a['ledger'],scene='S1',event='E2',rest=short_rest())
    def test_later_scene_no_rest_denied(self):
        a=activate(state(),new_ledger('A'));s=deactivate(a['after'])['after']
        with self.assertRaises(InvalidPlan):activate(s,a['ledger'],scene='S2',event='E2')
    def test_short_rest_4_to_6(self):
        a=activate(state(),new_ledger('A'));s=deactivate(a['after'])['after']
        for h in ('3.9','6.1'):
            with self.assertRaises(InvalidPlan):activate(s,a['ledger'],scene='S2',event='E2',rest=short_rest(hours=h))
        for h in ('4','6'):
            y=activate(s,a['ledger'],scene='S2',event='E2',rest=short_rest(hours=h))
            self.assertEqual(y['after']['spirit_current'],156)
    def test_full_refill_new_valid_activation(self):
        a=activate(state(),new_ledger('A'))
        s=damage(a['after'],100)['after']
        s['pa_spirit_current']=17
        s=deactivate(s)['after']
        b=activate(s,a['ledger'],scene='S2',event='E2',rest=short_rest())
        self.assertEqual((b['after']['spirit_current'],b['after']['pa_spirit_current']),(156,100))
        self.assertEqual((b['after']['normal_current'],b['after']['pa_normal_current'],b['after']['item_current']),(50,25,20))
    def test_full_damage_order(self):
        a=activate(state(),new_ledger('A'))
        x=damage(a['after'],180)
        self.assertEqual(x['debit'],{'spirit':156,'item':20,'normal':4})
        self.assertEqual(x['after']['normal_current'],46)
    def test_outside_form_item_then_normal(self):
        x=damage(state(),23)
        self.assertEqual(x['debit'],{'spirit':0,'item':20,'normal':3})
    def test_no_recharge_on_level(self):
        a=activate(state(),new_ledger('A'))
        s=damage(a['after'],87)['after'];s['pa_spirit_current']=12
        v=level_up_maxima(s,new_normal_vida_max=120,new_normal_pa_max=80,
                         new_spirit_vida_max=200,new_spirit_pa_max=150)
        self.assertEqual((v['after']['normal_current'],v['after']['spirit_current'],v['after']['pa_spirit_current']),
                         (50,69,12))
    def test_no_recharge_from_deactivation(self):
        a=activate(state(),new_ledger('A'))
        s=damage(a['after'],80)['after'];s['pa_spirit_current']=3
        x=deactivate(s)
        self.assertEqual((x['after']['spirit_current'],x['after']['pa_spirit_current']),(0,0))
        self.assertEqual(x['after']['normal_current'],50)
    def test_ledger_actor_separation(self):
        with self.assertRaises(InvalidPlan):activate(state(),new_ledger('B'))
    def test_event_replay_denied(self):
        a=activate(state(),new_ledger('A'))
        s=deactivate(a['after'])['after']
        with self.assertRaises(InvalidPlan):activate(s,a['ledger'],scene='S2',event='E1',rest=short_rest())
    def test_rest_only_verified(self):
        a=activate(state(),new_ledger('A'))
        s=deactivate(a['after'])['after']
        r=short_rest();r['verified']=False
        with self.assertRaises(InvalidPlan):activate(s,a['ledger'],scene='S2',event='E2',rest=r)
    def test_rest_wrong_order(self):
        a=activate(state(),new_ledger('A'))
        s=deactivate(a['after'])['after']
        with self.assertRaises(InvalidPlan):activate(s,a['ledger'],scene='S2',event='E2',rest=short_rest(after=0))
    def test_normal_pa_never_heals_from_spirit(self):
        a=activate(state(pa_now=2),new_ledger('A'))
        self.assertEqual((a['after']['pa_normal_current'],a['after']['pa_spirit_current']),(2,100))
    def test_explicit_rolls(self):
        x=progress_max(ordinal_level=11,initial_base=10,con_or_int_intrinsic=10,transform=True,
                       dice_mode='rolled',verified_rolls=[4]*11,source_id='SYNTHETIC')
        self.assertEqual((x['die'],x['derived_max']),(12,164))
    def test_no_hidden_rolls(self):
        with self.assertRaises(InvalidPlan):progress_max(ordinal_level=11,initial_base=10,
                   con_or_int_intrinsic=10,transform=True,dice_mode='rolled',source_id='SYNTHETIC')
    def test_no_double_count_equip_temp(self):
        x=extra_from_maxima(300,400,1000,900,source_verified=True)
        self.assertEqual(x['vida_espiritual_temporaria'],700)
    def test_patch_requires_unique_field(self):
        src='### Vida: 50/100 {toggle="true" color="red"}\n### Alma: 25/50'
        x=plan_minimal_field_patch(source_markup=src,source_sha256=sha256(src.encode()).hexdigest(),
              original_exact='### Vida: 50/100 {toggle="true" color="red"}',
              replacement_exact='### Vida: 50/120 {toggle="true" color="red"}',
              notion_page_id='12345678-1234-1234-1234-123456789012',field_id='VIDA_NORMAL')
        self.assertEqual(x['status'],'READ_ONLY_PATCH_CANDIDATE')
        self.assertFalse(x['write_allowed'])
    def test_patch_refuses_mutated_page(self):
        src='### Vida: 50/100'
        with self.assertRaises(InvalidPlan):plan_minimal_field_patch(source_markup=src,source_sha256='bad',
             original_exact='### Vida: 50/100',replacement_exact='### Vida: 50/120',
             notion_page_id='12345678-1234-1234-1234-123456789012',field_id='Vida')
    def test_patch_cannot_reorganize(self):
        src='### Vida: 50/100'
        with self.assertRaises(InvalidPlan):plan_minimal_field_patch(source_markup=src,
             source_sha256=sha256(src.encode()).hexdigest(),original_exact='### Vida: 50/100',
             replacement_exact='### Health: 50/120',notion_page_id='12345678-1234-1234-1234-123456789012',field_id='Vida')

if __name__=='__main__':unittest.main()
