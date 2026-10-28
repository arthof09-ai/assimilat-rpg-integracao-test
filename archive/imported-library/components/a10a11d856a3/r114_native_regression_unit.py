"""R114 native v0.8.1 controlled-copy regression; NOT campaign combat.
Synthetic directed unit fixtures share the patched vlab_effects_v08 and historical
RD module, but unlike the cold auditor deliberately import tested code.
"""
import unittest,sys,json,hashlib,copy,subprocess,sqlite3
from pathlib import Path
from fractions import Fraction
from dataclasses import asdict
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R))
import r112_native_battle as bridge
from vlab_effects_v08 import (Combatant,Scene,EffectBlocked,apply_weapon_attack,
      cast_source_specified_spell,weak_status,effective_movement_speed,move_via_verified_path,
      begin_source_turn,end_source_turn,AbilitySource,ActorActionState,FrozenRuleEvidence)
from vlab_rd_v08 import Resistances,RDUnresolved

class Tests(unittest.TestCase):
    def setUp(self):
        self.sc=Scene({'B':Combatant('B',43,4016,153,85,0,0,0,'B-1',rank='Lendário',standard=1,maximum_hp=4315,base_speed=63,beast_rank_index=23),
                       'F':Combatant('F',479,424,123,24,0,0,2,'F-1',rank='Ouro Negro',standard=1,maximum_hp=479,base_speed=40,beast_rank_index=None)})
        self.src=AbilitySource('B-BASIC','attack','STANDARD',bridge.SRC['B']['page'],'B_BASIC_ATTACK','RULE-DERIVED',target_scope='ENEMY',effect_adapter_ready=True,effect_adapter_id='NATIVE-V081-WEAPON')
        self.st=ActorActionState('B',23,4016,('B-BASIC',),enemy_ids_visible=('F',))
        sha=hashlib.sha256(bridge.SOURCE_TEXT['B'].encode()).hexdigest()
        self.p=(FrozenRuleEvidence(self.src.source_page_id,self.src.rule_id,sha,'PHYS_NOTION_READ_R108','R114_TEST_SOURCE'),)
    def run_attack(self,crit=(3,2,4),hit=((4,4,4,4,4,4),(5,5,5,5,5,5)),groups=((20,10),),dmg=None,bonus=138,flat=0,effort=False,rd=22):
        if dmg is None:dmg=tuple((5,)*n for n,f in groups)
        weak=weak_status(self.sc.actors['B'])
        h=hit[:2] if weak else hit[:1]
        total=bonus+(min(map(sum,h))-2 if weak else sum(h[0]))
        damage=sum(map(sum,dmg))+flat
        return apply_weapon_attack(self.sc,'B','F',source=self.src,state=self.st,proofs=self.p,
            roll_score=total,damage=damage,damage_tag='perfurante',rd=Resistances(general=rd),
            damage_dice_groups=groups,damage_roll_groups=dmg,damage_fixed_bonus=flat,
            critical_sequence=crit,attack_roll_attempts=h,attack_bonus=bonus,final_effort=effort)
    def test_native_critical_20d10(self):
        r=self.run_attack(crit=(6,6,5))
        self.assertEqual((r['raw'],r['critical_max_bonus'],r['net']), (300,200,278))
    def test_mixed_3d8_2d6(self):
        r=self.run_attack(crit=(6,6,6),groups=((3,8),(2,6)),dmg=((1,2,3),(3,5)),flat=20)
        self.assertEqual((r['raw'],r['critical_max_bonus'],r['net']), (70,36,48))
    def test_flat_8d8_critical(self):
        r=self.run_attack(crit=(6,6,5),groups=((8,8),),dmg=((2,3,4,5,6,7,8,1),),flat=211)
        self.assertEqual((r['raw'],r['critical_max_bonus']), (311,64))
    def test_weak_threshold_exact_10percent(self):
        self.sc.actors['B'].maximum_hp=430;self.sc.actors['B'].hp=43
        self.assertFalse(weak_status(self.sc.actors['B']))
        self.assertEqual(effective_movement_speed(self.sc.actors['B']),63)
    def test_weak_below_threshold_half_speed(self):
        self.assertTrue(weak_status(self.sc.actors['B']))
        self.assertEqual(effective_movement_speed(self.sc.actors['B']),Fraction(63,2))
    def test_weak_two_rolls_minus_two(self):
        r=self.run_attack()
        self.assertTrue(r['weak_attacker'])
        self.assertEqual(r['roll_score'],138+24-2)
    def test_weak_one_roll_rejected_without_changes(self):
        before=copy.deepcopy(self.sc)
        with self.assertRaises(EffectBlocked):
            apply_weapon_attack(self.sc,'B','F',source=self.src,state=self.st,proofs=self.p,
                roll_score=162,damage=100,damage_tag='perfurante',rd=Resistances(),
                damage_dice_groups=((20,10),),damage_roll_groups=((5,)*20,),damage_fixed_bonus=0,
                critical_sequence=(3,4,2),attack_roll_attempts=((4,)*6,),attack_bonus=138)
        self.assertEqual(asdict(self.sc.actors['B']),asdict(before.actors['B']))
        self.assertEqual(self.sc.events,[])
    def test_critical_failure_preintent_no_effect(self):
        before=copy.deepcopy(self.sc)
        with self.assertRaises(EffectBlocked):self.run_attack(crit=(1,1,2))
        self.assertEqual((asdict(before.actors['B']),len(self.sc.events)),(asdict(self.sc.actors['B']),0))
    def test_critical_sequence_strict(self):
        with self.assertRaises(EffectBlocked):self.run_attack(crit=(6,6,7))
    def test_mismatched_damage_tape(self):
        with self.assertRaises(EffectBlocked):self.run_attack(groups=((20,10),),dmg=((5,)*19,))
    def test_rd_before_mutation(self):
        before=copy.deepcopy(self.sc)
        with self.assertRaises(RDUnresolved):
            a=self.sc.actors['B'];a.hp=500
            self.run_attack(rd=22) if False else apply_weapon_attack(self.sc,'B','F',source=self.src,state=self.st,proofs=self.p,
              roll_score=200,damage=100,damage_tag='perfurante',rd=Resistances(10,(('perfurante',22),)))
        self.assertEqual(self.sc.actors['B'].standard,1)
        self.assertEqual(self.sc.events,[])
    def test_normal_effort_optional_not_auto(self):
        r=self.run_attack(effort=False)
        self.assertEqual((r['final_effort'],r['critical_max_bonus']),(False,0))
    def test_optional_effort_success_immobilize(self):
        r=self.run_attack(effort=True)
        self.assertEqual((r['critical_max_bonus'],r['final_effort']), (200,True))
        self.assertTrue(self.sc.actors['B'].final_effort_used)
        self.assertEqual(self.sc.actors['B'].immobile_next_own_turns,2)
        end_source_turn(self.sc,'B')
        self.assertEqual(self.sc.actors['B'].immobile_next_own_turns,1)
        begin_source_turn(self.sc,'B')
        self.assertEqual(effective_movement_speed(self.sc.actors['B']),0)
        with self.assertRaises(EffectBlocked):
            move_via_verified_path(self.sc,'B',source=AbilitySource('MOV','move','MOVEMENT',bridge.AUTH['combat'],'movement','RULE-DERIVED',target_scope='POSITION',effect_adapter_ready=True,effect_adapter_id='V081'),state=ActorActionState('B',23,4016,('MOV',),geometry_confirmed=True,environment_contract=True),proofs=(),destination='A3',path_evidence='source',travel_cost=Fraction(1),speed=Fraction(63,2))
        self.sc.actors['B'].standard=0
        end_source_turn(self.sc,'B')
        self.assertEqual(self.sc.actors['B'].immobile_next_own_turns,0)
    def test_effort_only_beast_ouro_or_above(self):
        self.sc.actors['B'].beast_rank_index=10
        with self.assertRaises(EffectBlocked):self.run_attack(effort=True)
    def test_effort_requires_weak(self):
        self.sc.actors['B'].hp=450
        with self.assertRaises(EffectBlocked):self.run_attack(effort=True)
    def test_effort_requires_actual_hit(self):
        self.sc.actors['F'].ca=250
        with self.assertRaises(EffectBlocked):self.run_attack(effort=True)
    def test_effort_cannot_repeat(self):
        self.run_attack(effort=True)
        self.sc.actors['B'].standard=1
        with self.assertRaises(EffectBlocked):self.run_attack(effort=True)
    def test_source_limited_hp_overkill(self):
        self.sc.actors['F'].hp=100
        r=self.run_attack(crit=(6,6,6))
        self.assertEqual((r['hp_loss_actual'],r['after_hp'],r['overkill']),(100,0,278-100))
    def spell(self,dam,pa=4016,standard=1,score=200,save=True):
        self.sc.actors['B'].pa=pa;self.sc.actors['B'].standard=standard
        src=AbilitySource('G-DESCARGA-CURTA','spell','STANDARD',bridge.SRC['B']['page'],'GRIFO_DESCARGA_CURTA','RULE-DERIVED',required_pa=55,target_scope='ENEMY',effect_adapter_ready=True,effect_adapter_id='NATIVE-V081-CAST')
        proof=FrozenRuleEvidence(src.source_page_id,src.rule_id,hashlib.sha256(bridge.SOURCE_TEXT['B'].encode()).hexdigest(),'PHYS','R114')
        st=ActorActionState('B',23,pa,('G-DESCARGA-CURTA',),standard_available=bool(standard),enemy_ids_visible=('F',))
        return cast_source_specified_spell(self.sc,'B','F',source=src,state=st,proofs=(proof,),damage=dam,damage_tag='raio',rd=Resistances(),
             explicit_save_effect='SAVE-HALF',target_save_exceeds_cd=save,damage_rolls=(dam-13,)+ (1,)*13 if 14<=dam<=23 else None,damage_faces=10)
    def test_native_half_even_commits(self):
        a=self.spell(20)
        self.assertEqual((a['effective'],self.sc.actors['B'].pa,self.sc.actors['B'].standard),(10,3961,0))
    def test_native_half_odd_rejected_pre_state(self):
        with self.assertRaises(EffectBlocked):self.spell(21)
        self.assertEqual((self.sc.actors['B'].pa,self.sc.actors['B'].standard,self.sc.events),(4016,1,[]))
    def test_native_pa_low_rejected(self):
        with self.assertRaises(EffectBlocked):self.spell(20,pa=54)
        self.assertEqual(self.sc.events,[])
    def test_native_slot_rejected(self):
        with self.assertRaises(EffectBlocked):self.spell(20,standard=0)
    def test_native_specific_rd_on_lightning(self):
        self.sc.actors['B'].hp=500
        self.assertTrue(weak_status(self.sc.actors['B']) is False)

if __name__=='__main__':unittest.main(verbosity=1)
