#!/usr/bin/env python3
"""R05 evidence oracle — source-grounded, NOT the Laboratorio runtime.
MESTRE-SIDE. Does not adjudicate canon, freeze rule authority, change Notion, or simulate a complete RPG fight.
"""
from __future__ import annotations
from itertools import product
from collections import Counter
from fractions import Fraction
import csv, json, hashlib, unittest
from pathlib import Path

ROOT=Path('/mnt/data')
PRIOR=json.loads((ROOT/'DMG-F1-R04-REPLAY-ISOLADO-v05.json').read_text())
D6=range(1,7)
PAIRS=list(product(D6,repeat=2))
SOURCE={
    'liu':('0b4c2b324ede837cb6be818dc8e36010','2026-10-01T09:40:50.721Z'),
    'monkey':('301c2b324ede828caccb813d3979267a','2026-10-01T18:00:42.589Z'),
    'combat':('3ebc2b324ede81f1be4be8804ac113c0','2026-10-07T23:51:04.971Z'),
    'character_creation':('3ebc2b324ede81449222f3c06b840613','2026-10-07T23:51:09.023Z'),
    'beast_creation':('3ebc2b324ede81f4992ac88a3588cacd','2026-10-07T20:58:56.199Z'),
    'historical_character_creation':('52ec2b324ede829fbfd881f261df8d0e','2026-09-30T16:32:31.637Z'),
    'taxonomy':('3f3c2b324ede81609a28e18c11d3cae4','2026-10-08T01:47:11.287Z'),
    'rdf_crosscheck_beast':('a47c2b324ede821f834481bef49fb8e3','2026-10-01T18:00:42.492Z'),
    'lab_rd_direction':('3f3c2b324ede81a398edd6df6bf0d8d4','2026-10-08T14:04:38.309Z'),
    'lab_v09':('3f3c2b324ede81e795d9c59794bcbdeb','2026-10-08T14:27:25.920Z'),
    'lab_action_catalog':('3f3c2b324ede8182a7c6da2804944d2f','2026-10-08T12:56:24.901Z'),
    'template':('528c2b324ede82d09cc6011a8ef5a26f','2026-09-30T04:34:37.809Z'),
    'peer_jaku':('2f6c2b324ede835796a9012df0a1a816','2026-09-30T04:36:54.035Z'),
    'peer_yin':('979c2b324ede821cb1680117cf30207a','2026-09-30T04:36:12.595Z'),
}

def roll2(dice,stat=54,skill=0,penalty=0):
    assert len(dice)==2 and all(v in D6 for v in dice)
    return sum(dice)+stat+skill+penalty

def strict_hit(total,defense):
    return total>defense

def damage2(dice,stat):
    return roll2(dice,stat)

def net_if_mitigated(gross,rdf):
    assert gross>=0 and rdf>=0
    return max(0,gross-rdf)

def total_outcomes(stat,defense,skill=0,penalty=0):
    vals=[roll2(d,stat,skill,penalty) for d in PAIRS]
    return dict(min=min(vals),max=max(vals),count=sum(v>defense for v in vals),denom=36,
        pmf={str(t):n for t,n in sorted(Counter(vals).items())})

def penalty_boundary(stat,defense,skill=0):
    # Need the MIN 2d6 result to exceed defense. For integer p: 2+stat+skill+p>defense.
    return defense - (2+stat+skill) + 1

CA=46
PRECOMP_DODGE=49
RAW_REFLEX_INCREMENT=PRECOMP_DODGE-CA
LIFE_LIU=235
DODGE_REFERENCES={
    'liu_normal':{'ca':46,'precomputed_reflex':49},
    'liu_transformed':{'ca':60,'precomputed_reflex':63},
    'jaku_normal':{'ca':29,'precomputed_reflex':35},
    'jaku_transformed':{'ca':39,'precomputed_reflex':45},
    'yin_normal':{'ca':29,'precomputed_reflex':37},
    'yin_transformed':{'ca':42,'precomputed_reflex':50},
}

class TestR05(unittest.TestCase):
    def test_01_previous_fixture_retained(self):
        self.assertEqual(PRIOR['source_literals']['liu_ca'],46)
        self.assertEqual(PRIOR['source_literals']['macaco_for'],54)
        self.assertEqual(PRIOR['validation']['tests_run'],18)
    def test_02_reaction_display_consistency(self):
        self.assertEqual((CA,PRECOMP_DODGE,RAW_REFLEX_INCREMENT),(46,49,3))
        self.assertEqual(DODGE_REFERENCES['liu_transformed']['precomputed_reflex']-DODGE_REFERENCES['liu_transformed']['ca'],3)
        self.assertEqual(DODGE_REFERENCES['jaku_normal']['precomputed_reflex']-DODGE_REFERENCES['jaku_normal']['ca'],6)
        self.assertEqual(DODGE_REFERENCES['yin_normal']['precomputed_reflex']-DODGE_REFERENCES['yin_normal']['ca'],8)
    def test_03_no_double_count_dodge(self):
        self.assertEqual(46+3,49)
        self.assertNotEqual(46+49,49)
        self.assertEqual(total_outcomes(54,95)['count'],0)
    def test_04_for54_ca46_all_dice_hit_when_no_penalty(self):
        self.assertEqual(total_outcomes(54,46)['count'],36)
    def test_05_for54_dodge49_all_hit_if_reaction_is_legal(self):
        self.assertEqual(total_outcomes(54,49)['count'],36)
    def test_06_for56_ca46_all_hit_if_buff_is_extra(self):
        self.assertEqual(total_outcomes(56,46)['count'],36)
    def test_07_for56_dodge49_all_hit_if_reaction_legal(self):
        self.assertEqual(total_outcomes(56,49)['count'],36)
    def test_08_threshold_for54_vs_ca(self):
        self.assertEqual(penalty_boundary(54,46),-9)
        self.assertEqual(total_outcomes(54,46,penalty=-9)['count'],36)
        self.assertLess(total_outcomes(54,46,penalty=-10)['count'],36)
    def test_09_threshold_for54_vs_dodge(self):
        self.assertEqual(penalty_boundary(54,49),-6)
        self.assertEqual(total_outcomes(54,49,penalty=-6)['count'],36)
        self.assertLess(total_outcomes(54,49,penalty=-7)['count'],36)
    def test_10_threshold_for56_vs_dodge(self):
        self.assertEqual(penalty_boundary(56,49),-8)
    def test_11_titan_rank_prata_conditional_plus11(self):
        self.assertEqual(total_outcomes(54,49,skill=11)['min'],67)
        self.assertEqual(total_outcomes(54,49,skill=11)['max'],77)
    def test_12_replay_atk_for54(self):
        self.assertEqual(roll2((3,4),54),61)
        self.assertTrue(strict_hit(61,46))
        self.assertTrue(strict_hit(61,49))
    def test_13_replay_atk_for56(self):
        self.assertEqual(roll2((3,4),56),63)
    def test_14_two_damage_fork_strict_source55(self):
        self.assertEqual(damage2((5,3),54),62)
        self.assertEqual(damage2((5,3),56),64)
    def test_15_mitigation_scoped_to_applicable_10(self):
        self.assertEqual(net_if_mitigated(62,10),52)
        self.assertEqual(net_if_mitigated(64,10),54)
    def test_16_nonapplicable_resistance_zero_branch(self):
        self.assertEqual(net_if_mitigated(62,0),62)
        self.assertEqual(net_if_mitigated(64,0),64)
    def test_17_life_branch4(self):
        self.assertEqual([LIFE_LIU-v for v in [52,62,54,64]],[183,173,181,171])
    def test_18_no_furia_or_fraco_single_basic_hit(self):
        for stat in (54,56):
            for dice in PAIRS:
                for rd in (0,10):
                    life=LIFE_LIU-net_if_mitigated(damage2(dice,stat),rd)
                    self.assertGreater(life,117.5)
                    self.assertGreater(life,23.5)
    def test_19_prata_dice_distribution_correct(self):
        self.assertEqual(len(PAIRS),36)
        self.assertEqual(Fraction(sum(sum(d) for d in PAIRS),36),7)
    def test_20_pmfs_have_36_units(self):
        for s in (54,56):
            self.assertEqual(sum(total_outcomes(s,49)['pmf'].values()),36)
    def test_21_per_component_damage_lacks_double_FOR(self):
        self.assertEqual(damage2((5,3),54),62)
        self.assertNotEqual(damage2((5,3),54),116)
    def test_22_atk_roll_not_damage_roll(self):
        self.assertEqual(roll2((3,4),54),61)
        self.assertEqual(damage2((5,3),54),62)
    def test_23_if_reaction_disallowed_passive_CA_still_separate(self):
        self.assertNotEqual(CA,PRECOMP_DODGE)
    def test_24_title_rank_alone_does_not_certify_action(self):
        self.assertFalse(FIXTURE['audit']['full_fight_certified'])
    def test_25_unknown_cost_is_not_zero(self):
        self.assertIsNone(FIXTURE['lab_adapter']['AbilitySource']['pa_cost'])
    def test_26_unknown_range_is_not_zero(self):
        self.assertIsNone(FIXTURE['lab_adapter']['AbilitySource']['range'])
    def test_27_unknown_actor_pa_is_not_imputed(self):
        self.assertIsNone(FIXTURE['lab_adapter']['ActorActionState']['pa_free'])
    def test_28_strict_integration_not_self_approved(self):
        self.assertEqual(FIXTURE['lab_adapter']['EXPECTED_PREFLIGHT']['status'],'STRICT_REJECT_PENDING_SOURCE_AND_SCENE')
    def test_29_life_alma_a_b_distinct(self):
        self.assertNotEqual(FIXTURE['sensitivity']['resources_A'],FIXTURE['sensitivity']['resources_B'])
    def test_30_source_ids_stable_and_explicit(self):
        self.assertEqual(len(SOURCE),14)
        self.assertTrue(all(len(id)==32 for id,_ in SOURCE.values()))
    def test_31_dodge_precomputed_not_prof_exact(self):
        self.assertEqual(FIXTURE['dodge']['increment_CA_to_reported_total'],3)
        self.assertIsNone(FIXTURE['dodge']['skill_reflexo_exact_component'])
    def test_32_no_runtime_claim(self):
        self.assertIsNone(FIXTURE['audit']['lab_execution_evidence'])

FIXTURE={
    'schema':'OP-DMG-CORPUS-EMP-01/SCIENTIFIC-ORACLE-R05-v0.6',
    'mission':'single natural beast attack against ED, MESTRE-SIDE ONLY',
    'no_repeat':['IBX-28','IBX-32','IBX-34/R03','IBX-34/R04','IBX-34/R04B','historical198'],
    'source_manifest':{k:{'page_id':i,'url':'https://app.notion.com/p/'+i,'observed_last_edit':t,'evidence_kind':'Notion source, no runtime authorization'} for k,(i,t) in SOURCE.items()},
    'dodge':{
        'combat_literal':'Esquiva = CA + Reflexo',
        'liu_profile_literal':'CA 46 (Reflexo 49)',
        'best_supported_interpretation':'Reflexo 49 is precomputed reaction defense total; do not add 46 again',
        'basis':'Liu normal/transformed delta 3; Jaku delta 6; Yin delta 8; base ficha stores CA and Reflexo side by side; Criação de Ficha adds proficiency to CA',
        'comparators':DODGE_REFERENCES,
        'increment_CA_to_reported_total':3,
        'skill_reflexo_exact_component':None,
        'separate_defenses':{'NO_REACTION':46,'REACTION_ESQUIVAR_ELIGIBLE':49},
        'status':'HIGH_CONFIDENCE_SOURCE_INTERPRETATION; not master ratified; need legal reaction window; 95 is DOUBLE-COUNT',
    },
    'strength':{
        'literal_sheet':54,'passive_literal':'+2 força',
        'scenarios':{'A_ALREADY_INCLUDED':54,'B_ADDITIONAL_IF_NOT_INCLUDED':56},
        'inclusion_status':'UNKNOWN, no construction ledger in source; cannot canonize +2',
        'lab_impact':'For purposes of hit/NO_NEGATIVE modifiers, both scenarios succeed vs CA46 and dodge49; damage differs by 2 per attack; do not mix branches'
    },
    'rdf':{
        'liu_armor_literal':'Armadura Pesada Anã (ON), RDF 10',
        'physical_category_evidence':'DMG-TAX-DATA-01: CONTUNDENTE/IMPACTO is physical; Rinolupo Prata4 describes RDF10 against physical attacks',
        'lab_master_direction':'If a single known-type component matches applicable RD, net=max(0,gross-RD); MASTER-DIRECTION-PENDING-NAC-NORM',
        'current_adjudication':'LIKELY physical impact in coverage; NOT sufficient evidence for simultaneous RD general+RDF priority or actual armor effective state',
        'stacking_with_general_RD':None,'armor_worn_at_encounter':None,'applies_impact_certified':False,
        'alternatives':{'IF_APPLIES10':10,'IF_NOT_APPLICABLE':0},
    },
    'proficiencies':{
        'character_creation_initial_selected_skill_bonus':2,
        'liu_skill_luta':None,'liu_skill_initiative':None,'liu_skill_reflexo_exact':None,
        'liu_instinto_selvagem_initiative_explicit':4,
        'monkey_if_titan_Prata_general_bonus':11,'monkey_luta_actual_application':None,
        'monkey_if_not_titan_Prata_general_bonus':8,
        'note':'A ficha Liu lists all proficiencies but BOLD selection is not preserved as a determinate Luta bonus. Monster rank proficiency is a table, not a confirmed individual choice/application.',
    },
    'sources_of_uncertainty':{
        'identity_alias':'one physical P5 page under Símio Demoníaco with body macaco rei, no alias canonization',
        'range':None,'line_of_sight':None,'starting_position':None,
        'reaction_available':None,'position_legal':None,'standard_action_available':None,
        'active_negative_status':None,'actor_pa_free':None,'source_frozen_evidence_lab_accepted':False,
        'scheduler_complete':False,'action_effect_adapter_lab_confirmed':False,
    },
    'scenario':{
        'attack_action':'Patada: 2d6 + força impacto',
        'attack_action_type':'STANDARD for normal attack only if attack mapped competently to standard normal attack',
        'environment_test_params_proposed_not_fact':{'adjacent':True,'same_visible_level':True,'no_cover':True,'reaction_choice':'NO_REACTION or ESQUIVAR explicitly', 'status_penalties':0,'known_buff_state':'NO OPTIONAL BUFF'},
        'dice_hit':[3,4],'dice_crit_sequential':[2,3,4],'dice_damage':[5,3],
        'legal_attack_confirmed':False,
    },
    'replay':{
        'source_CA':46,'source_dodge_total_likely':49,
        'A_FOR54':{'hit_roll_no_luta':61,'damage_gross':62,'if_RDF10_applicable':{'damage_net':52,'liu_life_from235':183},'if_not':{'damage_net':62,'liu_life_from235':173}},
        'B_FOR56':{'hit_roll_no_luta':63,'damage_gross':64,'if_RDF10_applicable':{'damage_net':54,'liu_life_from235':181},'if_not':{'damage_net':64,'liu_life_from235':171}},
        'rolls_are_distinct':True,'probability_hit_if_source_legal_and_luta>=0_and_no_penalties':{'vs_CA46':{'A':(36,36),'B':(36,36)},'vs_dodge49_when_reaction_legal':{'A':(36,36),'B':(36,36)}},
        'min_total_negative_modifier_to_still_guarantee_all_hit':{'A_vs_CA46':-9,'A_vs_dodge49':-6,'B_vs_CA46':-11,'B_vs_dodge49':-8},
        'double_count_95_branch':'REJECT AS INCONSISTENT WITH MULTIPLE SHEET CONVENTIONS',
        'source_tied_roll_policy':None,'attack_runtime_execution':False,
    },
    'sensitivity':{
        'resources_A':{'macaco':{'life':750,'alma':700},'behemoth':{'life':500,'alma':560}},
        'resources_B':{'macaco':{'life':810,'alma':760},'behemoth':{'life':530,'alma':590}},
        'note':'A literal historical vs B hypothetical under current Criação de Besta; no mix, no canonization; unaffected by single attack on Liu until encounter states chosen',
    },
    'lab_adapter':{
        'contract_basis':'Existing DEV-SIM-DMG-AIN01-03 v0.7 plus DEV-SIM-DMG-AI09-05 v0.9 documentation, not inspected source runtime ZIP',
        'AbilitySource':{'action_id':'RESEARCH-DMG-R05-MACACO-PATADA','type':'attack','economy':'STANDARD_CANDIDATE','source_page_id':SOURCE['monkey'][0],'rule_id':'Sistema-Combate-Regra3','pa_cost':None,'range':None,'los':None,'effect_adapter_status':'UNVERIFIED'},
        'ActorActionState':{'actor_id':'SOURCE-301c2b32-P5','rank':'Prata5','pa_free':None,'standard_available':None,'reaction_available':None,'position':None,'selected_skills':None},
        'FrozenRuleEvidence':{'state':'SOURCE_REFERENCES_AND_R03_CONTENT_HASH_ONLY','hash_accepted_by_lab':False,'source_readback_evidence':'MESTRE_NOTION_READONLY'},
        'SourcedOption':{'status':None,'not_authorized_to_announce_legal':True},
        'EXPECTED_PREFLIGHT':{'status':'STRICT_REJECT_PENDING_SOURCE_AND_SCENE','reasons':['UNKNOWN_ACTOR_PA_FREE','UNKNOWN_RANGE_LOS','UNKNOWN_ACTION_STATE','UNKNOWN_ACTUAL_INITIATIVE','UNACCEPTED_FROZEN_RULE_EVIDENCE','NO_LAB_EFFECT_ADAPTER_ACCEPTANCE']},
        'NEEDS_ENGINEER_REPLY':['exact version/code commit','ACK instance ID','native import field types','accepted/rejected preflight for research oracles','source freeze verification','scheduler/reaction implementation','runner event log/digest/seed if executed','actual expected comparison'],
    },
    'audit':{'previous_R04_math_tests':29,'new_R05_math_tests':None,'lab_execution_evidence':None,'full_fight_certified':False,'b01_to_b18_all_full_fight_certified':0,'NAC_PASS':'PENDING','writer_claimed':False},
}

if __name__=='__main__':
    tests=unittest.defaultTestLoader.loadTestsFromTestCase(TestR05)
    res=unittest.TextTestRunner(verbosity=0).run(tests)
    assert res.wasSuccessful(), 'R05 QA FAIL'
    FIXTURE['audit']['new_R05_math_tests']=res.testsRun
    FIXTURE['audit']['new_R05_failures']=len(res.failures)+len(res.errors)
    FIXTURE['audit']['source_fingerprint_scope']='prior verified R03 hash and last edited readback; live re-fetch acceptance required by lab'
    FIXTURE['audit']['content_fingerprint_json_sha256_computed_later']=None
    out=ROOT/'DMG-F1-R05-ORACULO-ATAQUE-DODGE-RDF-v06.json'
    out.write_text(json.dumps(FIXTURE,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(f'QA_R05 PASS={res.testsRun} FAIL={len(res.failures)+len(res.errors)}')
    for s in (54,56):
        v1,v2=total_outcomes(s,46),total_outcomes(s,49)
        print(f'FOR={s} hit_vs_CA46={v1["count"]}/36 hit_vs_DODGE49={v2["count"]}/36 range={v1["min"]}..{v1["max"]}')
    print(f'FILE={out} BYTES={out.stat().st_size} SHA256={hashlib.sha256(out.read_bytes()).hexdigest()}')
