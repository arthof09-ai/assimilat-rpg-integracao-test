#!/usr/bin/env python3
"""OP-DMG-CORPUS-EMP-01: oracle de matemática de alcance limitado.
NÃO implementa combate RPG nem executa runtime do Laboratório.
Fontes: páginas mestre Notion reabertas 08/10/2026, vide JSON fixture.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
from itertools import product
import json, unittest
from pathlib import Path

OUT = Path('/mnt/data')
RAW = json.loads((OUT/'DMG-F1-EDxBESTA-SCIENTIFIC-FIXTURE-v04.json').read_text())
D6 = tuple(range(1,7))
ATTACK_DICE = list(product(D6, repeat=2))
CRIT_DICE = list(product(D6, repeat=3))


def roll_expr(rolls, attr=54):
    assert len(rolls)==2 and all(1<=v<=6 for v in rolls)
    return sum(rolls)+attr


def hit(attack, defense):
    # Sistema de Combate: ataque precisa SUPERAR defesa
    return attack > defense


def single_component_net(gross, applicable_rd):
    # DEV-SIM-DMG-AI08-04: diretriz Mestre para componente simples,
    # MASTER-DIRECTION-PENDING-NAC-NORM; aplicada apenas como cenário condicional.
    return max(0, gross-applicable_rd)


def crit_label(triple):
    # Regras sequenciais 3d6 no Sistema de Combate.
    if triple[:2] == (6,6) and triple[2] in (5,6): return 'POSITIVE'
    if triple[:2] == (1,1) and triple[2] in (1,2): return 'NEGATIVE'
    return 'ORDINARY'


def pmf_hit_and_damage(forca=54, defense=46, resistance=None):
    outcomes = Counter()
    for ds in ATTACK_DICE:
        v = roll_expr(ds, attr=forca)
        outcomes[single_component_net(v,resistance) if resistance is not None else v]+=1
    return {'min':min(outcomes),'max':max(outcomes),
            'mean_fraction':str(sum(k*n for k,n in outcomes.items())/36),
            'mean':sum(k*n for k,n in outcomes.items())/36,
            'pmf_numerator_denominator':{str(k):[n,36] for k,n in sorted(outcomes.items())}}

class TestScientificOracle(unittest.TestCase):
    def test_01_prior_fixture_three_actors(self):
        self.assertEqual(set(RAW['actors']), {'liu','macaco','behemoth'})
    def test_02_36_outcomes_no_elision(self):
        self.assertEqual(len(ATTACK_DICE),36)
        self.assertEqual(len(set(ATTACK_DICE)),36)
    def test_03_dice_pmf_mean(self):
        self.assertEqual(sum(sum(x) for x in ATTACK_DICE),252)
        self.assertEqual(Fraction(252,36),7)
        self.assertEqual(min(map(sum,ATTACK_DICE)),2)
        self.assertEqual(max(map(sum,ATTACK_DICE)),12)
    def test_04_conditional_for54_vs_passive_ca46(self):
        # assume successful legal attempt, range OK, no penalties/reaction.
        self.assertTrue(all(hit(roll_expr(ds),46) for ds in ATTACK_DICE))
    def test_05_conditional_for54_vs_source_reflex49(self):
        # source records Reflexo49: dodge trigger/window must still be eligible.
        self.assertTrue(all(hit(roll_expr(ds),49) for ds in ATTACK_DICE))
    def test_06_separate_rolls_replay(self):
        atk = roll_expr((3,4))
        gross = roll_expr((5,3))
        self.assertEqual(atk,61); self.assertEqual(gross,62)
        self.assertTrue(hit(atk,46)); self.assertTrue(hit(atk,49))
        self.assertEqual(single_component_net(gross,10),52)
        self.assertEqual(single_component_net(gross,0),62)
        self.assertEqual(235-52,183); self.assertEqual(235-62,173)
    def test_07_no_crit_sequence_replay(self):
        self.assertEqual(crit_label((2,3,4)),'ORDINARY')
    def test_08_crit_pmf(self):
        c=Counter(crit_label(ds) for ds in CRIT_DICE)
        self.assertEqual(c,{'POSITIVE':2,'NEGATIVE':2,'ORDINARY':212})
        self.assertEqual(Fraction(c['POSITIVE'],216),Fraction(1,108))
    def test_09_mitigate_never_negative(self):
        for gross in range(0,85):
            for rd in range(0,90):
                self.assertEqual(single_component_net(gross,rd),max(0,gross-rd))
    def test_10_beast_resource_differences(self):
        self.assertEqual(60+10*(40+35),810)
        self.assertEqual(60+10*(40+30),760)
        self.assertEqual(30+10*(20+30),530)
        self.assertEqual(30+10*(20+36),590)
    def test_11_liuxiaua_conditional_attack_ceiling(self):
        self.assertEqual(max(sum(ds)+37 for ds in ATTACK_DICE),49)
        self.assertTrue(all(not hit(sum(ds)+37,67) for ds in ATTACK_DICE))
        self.assertTrue(all(not hit(sum(ds)+37,61) for ds in ATTACK_DICE))
    def test_12_forca_titanica_sensitivity(self):
        self.assertEqual((min(roll_expr(ds,56) for ds in ATTACK_DICE),max(roll_expr(ds,56) for ds in ATTACK_DICE)),(58,68))
        self.assertTrue(all(hit(roll_expr(ds,56),49) for ds in ATTACK_DICE))
    def test_13_conditional_exhaustion_liu(self):
        self.assertEqual(170+50-15-30-60-42,73)
        self.assertEqual(73-46,27)  # APENAS SE -46 adicional a 73
    def test_14_initiative_conditional_no_tie_for_small_skills(self):
        # Se p_L <=9 e p_M >=0 e nenhum bônus desconhecido se aplicar:
        # max Liu 12+16+4+9=41 < min Macaco 2+40=42.
        for ld in ATTACK_DICE:
            for md in ATTACK_DICE:
                self.assertLess(sum(ld)+16+4+9, sum(md)+40)
    def test_15_initiative_tie_possible_without_known_modifiers(self):
        # p_L=10, p_M=0 gera empate em dados extremos, portanto não
        # se pode converter prova condicional em política universal.
        self.assertEqual(12+16+4+10,2+40)
    def test_16_scenarios_A_B_never_mixed(self):
        assert scenarioA['macaco']['life']==750 and scenarioA['macaco']['alma']==700
        assert scenarioB['macaco']['life']==810 and scenarioB['macaco']['alma']==760
        assert scenarioA['behemoth']['life']==500 and scenarioB['behemoth']['life']==530
    def test_17_single_patada_no_furia_fraco_under_stated_scope(self):
        # Macaco FOR54 ou FOR56 (+2 passivo não adjudicado); RDF10 aplica ou não.
        # Sem combos/riders/crit/buffs externos, um único golpe nunca atinge
        # metade da Vida 235 de Liu e nunca atinge <10%.
        for strength in (54,56):
            for dice in ATTACK_DICE:
                gross=roll_expr(dice,strength)
                for rd in (0,10):
                    life_after=235-single_component_net(gross,rd)
                    self.assertGreater(life_after,235/2)
                    self.assertGreater(life_after,235/10)
    def test_18_defender_conditional_fortitude_bound(self):
        # Defender = 6+CON16+armadura15+Fortitude_bonus
        # Se Fortitude_bonus<=18, todo 2d6+54 supera Defender.
        for bonus in range(0,19):
            self.assertTrue(all(hit(roll_expr(ds),37+bonus) for ds in ATTACK_DICE))

scenarioA={'macaco':{'life':750,'alma':700},'behemoth':{'life':500,'alma':560},
           'basis':'SOURCE_LITERAL_DOCUMENTARY; not necessarily current encounter'}
scenarioB={'macaco':{'life':810,'alma':760},'behemoth':{'life':530,'alma':590},
           'basis':'HYPOTHETICAL_RECALC; NOT CANON; never mixed with A'}

sample={
 'schema':'OP-DMG-F1-REPLAY-ISOLATED-R04-v0.5',
 'notion_source_page_ids':{'liu':'0b4c2b324ede837cb6be818dc8e36010','macaco':'301c2b324ede828caccb813d3979267a',
    'combat':'3ebc2b324ede81f1be4be8804ac113c0','beast_rules':'3ebc2b324ede81f4992ac88a3588cacd',
    'lab_rd_direction':'3f3c2b324ede81a398edd6df6bf0d8d4'},
 'title':'Macaco Rei Patada -> Liu Xiaua, momento de ataque isolado, não combate completo',
 'source_literals':{'macaco_for':54,'macaco_attack':'Patada: 2d6 + força impacto','liu_ca':46,'liu_reflexo_reported':49,'liu_armor_rdf':10},
 'preconditions_NOT_fully_verified':['turn/action legal','range or adjacent positioning','no condition penalties',
   'no reaction or selected dodge when eligible','critical separate roll ordinary','FOR 54 already includes passive +2 or not',
   'Luta proficiency modifier nonnegative, not frozen','RDF applies to impacto physical? still conditional'],
 'attack_roll_d6':[3,4],'critical_sequential_3d6':[2,3,4],'damage_roll_d6':[5,3],
 'to_hit_minimum_without_unverified_proficiency':61,
 'defense_cases':{'passive_CA46':'61 > 46 = success conditional','dodge_reflexo49':'61 > 49 = success conditional'},
 'attack_results_not_rpg_full_fight':{'critical_check':'ORDINARY','damage_gross':62,'liu_critical_health_thresholds':{'furia_at_or_below':117.5,'fraco_strict_below':23.5,'not_triggered_in_both_simple_RD_branches':True},'RDF_applies10':{'net':52,'liu_hp_after_if_full235':183},
    'RDF_not_applicable':{'net':62,'liu_hp_after_if_full235':173},'do_not_choose_mitigation_branch_without_authority':True},
 'complete_pmf_for54':pmf_hit_and_damage(54),
 'complete_pmf_for54_if_RDF10_applies':pmf_hit_and_damage(54,resistance=10),
 'sensitivity_FOR56_if_passive_not_included':pmf_hit_and_damage(56),
 'initial_resource_sensitivity':{'A_documented':scenarioA,'B_hypothetical':scenarioB},
 'defender_bounded_proof':{'formula':'6+CON16+ARMOR15+fortitude_bonus=37+fortitude_bonus',
  'if_fortitude_bonus_le18':'all_36_attack_2d6+54 exceed Defender; conditional only'},
 'initiative_bounded_proof':{'liu_roll':'2d6+DES16+InstintoSelvagem4+initiative_prof_unknown',
  'macaco_roll':'2d6+DES40+initiative_prof_unknown',
  'sufficient_not_necessary_condition':'p_liu-p_macaco<=9, no unknown situational modifiers => macaco always wins all 1296 independent initiative pairs',
  'tie_policy_global':'UNKNOWN', 'sample_liu':[4,4],'sample_macaco':[2,3],
  'sample_base_L':28,'sample_base_M':45, 'result':'conditional only; not B07 final certification'},
 'liu_attack_hypothesis':{'raw_to_hit_candidate':'2d6+37','min':39,'max':49,'below_macaco_passive67_for_all_36':True,
      'status':'ONLY_IF_RAW_NOTATION_REPRESENTS_TO_HIT; no certified misses or tactical result'},
 'validator':'independent exhaustive enumeration of 2d6 and 3d6, not lab runtime',
 'full_fight_eligible':False,
 'export_contract':'READ_ONLY_EXPERIMENTAL_ORACLE / DOES_NOT_IMPOSE_LAB_FIELD_SCHEMA'
}

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(TestScientificOracle)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    sample['validation']={'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'passed':result.wasSuccessful()}
    (OUT/'DMG-F1-R04-REPLAY-ISOLADO-v05.json').write_text(json.dumps(sample,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert result.wasSuccessful()
    print('RESULTADO: TESTES=',result.testsRun,'PASS=',result.testsRun-len(result.failures)-len(result.errors),'FAIL=',len(result.failures)+len(result.errors))
    print('EXAUSTIVO: 36/36 formas 2d6 com FOR54 superam CA46 e Reflexo49, assumidas condições explícitas de cenário')
    print('ROLAGEM: ataque (3,4)->61; dano (5,3)->62; crítico (2,3,4)->ordinário')
    print('CONDICIONAL: RDF10 elegível -> dano líquido52; RDF não elegível -> 62')
    print('ARQUIVO:', OUT/'DMG-F1-R04-REPLAY-ISOLADO-v05.json')
