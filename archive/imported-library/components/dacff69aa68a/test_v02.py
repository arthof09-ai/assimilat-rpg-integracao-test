import json
import unittest
from pathlib import Path
from levelup_engine import InvalidPlan, fingerprint
from evolution_runtime import (validate_resource_state, projected_resources, apply_damage_temporary_first,
                               candidate_temp_hp_from_equipment_con, generate_save_manifest, transformed_bonus_from_preview,
                               plan_level_up_v02)

ROOT = Path(__file__).resolve().parents[1]


def fixture():
    s=json.loads((ROOT/'examples/synthetic_bronze_1.json').read_text())
    r=json.loads((ROOT/'examples/request_fixed_level2.json').read_text())
    r['expected_snapshot_hash']=fingerprint(s)
    return s,r


def resources(vida=50, maximum=100, pa=20, pa_max=50, temp=20, temp_max=20):
    return {'vida_atual':vida,'vida_maxima':maximum,'pa_atual':pa,'pa_capacidade':pa_max,
            'vida_temp_atual':temp,'vida_temp_maxima':temp_max}


class TestRuntimeV02(unittest.TestCase):
    def test_mestre_50_de_100_to_50_de_120(self):
        x=projected_resources(resources(),before_max_vida=100,after_max_vida=120,
                              before_pa_capacity=50,after_pa_capacity=80)
        self.assertEqual((x['after']['vida_atual'],x['after']['vida_maxima']),(50,120))
        self.assertEqual((x['after']['pa_atual'],x['after']['pa_capacidade']),(20,80))
        self.assertEqual(x['display'],'50/120 (20/20)')
        self.assertEqual(x['healed_by_level'],0)

    def test_temp_shield_absorbs_damage_first(self):
        p=apply_damage_temporary_first(resources(),15)
        self.assertEqual((p['vida_atual'],p['vida_temp_atual']),(50,5))
        p=apply_damage_temporary_first(resources(),23)
        self.assertEqual((p['vida_atual'],p['vida_temp_atual']),(47,0))

    def test_no_temp_hp_recharge_on_level(self):
        p=projected_resources(resources(temp=4),before_max_vida=100,after_max_vida=120,
                              before_pa_capacity=50,after_pa_capacity=55,after_temp_max=28)
        self.assertEqual((p['after']['vida_temp_atual'],p['after']['vida_temp_maxima']),(4,28))

    def test_temp_removed_clamps_without_healing(self):
        p=projected_resources(resources(temp=15),before_max_vida=100,after_max_vida=120,
                              before_pa_capacity=50,after_pa_capacity=55,after_temp_max=5)
        self.assertEqual(p['after']['vida_temp_atual'],5)

    def test_excess_resource_denied(self):
        with self.assertRaises(InvalidPlan):validate_resource_state(resources(vida=101))
        with self.assertRaises(InvalidPlan):validate_resource_state(resources(pa=70))

    def test_missing_current_state_denied(self):
        with self.assertRaises(InvalidPlan):validate_resource_state({'vida_atual':20})

    def test_candidate_temp_formula_requires_gate_id(self):
        with self.assertRaises(InvalidPlan):candidate_temp_hp_from_equipment_con(8,10)
        x=candidate_temp_hp_from_equipment_con(8,10,rule_id='PROPOSTA-CON-TEMP-POR-NIVEL')
        self.assertEqual(x['new_temp_hp_max_bonus'],80)
        self.assertTrue(x['not_canonical'])

    def test_save_no_fake_write_and_full_source_hash(self):
        src='# Ficha\n<details><summary>título antigo</summary>\nTexto histórico\n</details>\n<page url="https://app.notion.com/p/source"/>'
        s=generate_save_manifest(character_id='SYN',before_level=1,after_level=2,
                                 notion_page_id='PAGE',source_markup=src,event_id='EV-0001')
        self.assertEqual(s['native_toggles_count'],1)
        self.assertEqual(s['child_pages_referenced'],1)
        self.assertFalse(s['write_allowed'])
        self.assertEqual(s['save_location'],'end_of_existing_player_character_page_as_native_toggle')

    def test_duplicate_save_event_denied(self):
        with self.assertRaises(InvalidPlan):
            generate_save_manifest(character_id='S',before_level=1,after_level=2,
                                   notion_page_id='P',source_markup='SAVE-LEVEL-UP:EV-1',event_id='EV-1')

    def test_nonlevel_save_denied(self):
        with self.assertRaises(InvalidPlan):
            generate_save_manifest(character_id='S',before_level=2,after_level=1,
                                   notion_page_id='P',source_markup='Ficha',event_id='EV-1')

    def test_transformed_delta_is_not_beast_raw_hp(self):
        x=transformed_bonus_from_preview({'normal':{'Vida':100,'Alma_PA_Total':200},
                                         'transform':{'Vida':240,'Alma_PA_Total':320}})
        self.assertEqual((x['vida_bonus'],x['alma_bonus']),(140,120))
        self.assertIn('not_method',x)

    def test_transformed_floor(self):
        with self.assertRaises(InvalidPlan):transformed_bonus_from_preview(
            {'normal':{'Vida':100,'Alma_PA_Total':100}, 'transform':{'Vida':90,'Alma_PA_Total':120}})

    def test_complete_dry_run_preserves_current_and_generates_save_plan(self):
        s,r=fixture()
        x=plan_level_up_v02(s,r,resources=resources(vida=10,maximum=14,pa=8,pa_max=11,temp=3,temp_max=5),
             raw_page_markup='SIMULATED PAGE WITH FULL PREIMAGE',notion_page_id='SYN-ID',event_id='EV-2')
        self.assertFalse(x['write_allowed'])
        self.assertEqual((x['resources']['after']['vida_atual'],x['resources']['after']['vida_maxima']),(10,23))
        self.assertEqual((x['resources']['after']['pa_atual'],x['resources']['after']['pa_capacidade']),(8,19))
        self.assertEqual(x['transformed_additions']['vida_bonus'],1)
        self.assertEqual(x['pre_evolution_save']['from_level'],1)

    def test_unreconciled_old_hp_denied(self):
        s,r=fixture()
        with self.assertRaises(InvalidPlan):plan_level_up_v02(s,r,
            resources=resources(vida=10,maximum=44,pa=8,pa_max=11,temp=3,temp_max=5),
            raw_page_markup='FULL DATA',notion_page_id='P',event_id='EV')

if __name__=='__main__':unittest.main()
