"""R29–R38 technical gates; supplements, never mutates, authentic baseline R28.
Read-only Notion evidence was separately verified with authorized Mestre connector.
"""
from __future__ import annotations
import copy, hashlib, json, os, subprocess, sys, unittest, zipfile
from pathlib import Path

WORK = Path(__file__).resolve().parent
ROOT=WORK/'r28'
PROVIDER=ROOT/'provider_r27'
sys.path.insert(0,str(PROVIDER))
from ponte_pa_craft_r27 import consultar_ficha_craft, ContractError
from engine_r26.parecer_semicanonico_r26 import BASE, FLOORS
from engine_r26.baseline_r25.baseline_r22.rank_guard_r22 import tariff
FIX=json.loads((PROVIDER/'fixture_craft_acessorio.json').read_text())
CORPUS=json.loads((WORK/'CORPUS_12_FONTE_NOTION.json').read_text())['cases']
RANKS=['Bronze','Prata','Ouro','Ouro Negro','Lendário']
EXP_FLOORS=[8,11,21,35,90]
EXP_BASE=[6,12,24,35,50]
EXP_ACTIVE_DAILY=[3,6,12,17,25]
EXP_PER_USE=[3,7,14,21,30]

class R30FinalTariffs(unittest.TestCase):
    def test_01_r28_hash_matches_persistent_baseline(self):
        path=(WORK/'PA_R28_QMC05_NATIVO_INTEGRADO_TEST_20261020.zip')
        if not path.exists():path=WORK.parent/'PA_R28_QMC05_NATIVO_INTEGRADO_TEST_20261020.zip'
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),'68acc4405250cbf03a89924fa4df1f3d36586f26a5a903610c6600e8f26a391e')
    def test_02_source_tariff_table_current_master_order(self):
        for idx,rank in enumerate(RANKS):
            with self.subTest(rank=rank):
                t=tariff(rank)
                self.assertEqual(BASE[rank],EXP_BASE[idx])
                self.assertEqual(FLOORS[rank],EXP_FLOORS[idx])
                self.assertEqual(t['passiva_por_dia'],EXP_BASE[idx])
                self.assertEqual(t['ativa_por_dia'],EXP_ACTIVE_DAILY[idx])
                self.assertEqual(t['ativa_por_uso'],EXP_PER_USE[idx])
    def test_03_five_real_floor_provider_calls(self):
        for idx,rank in enumerate(RANKS):
            with self.subTest(rank=rank):
                v=consultar_ficha_craft({'acao':'CONSULTAR_PA_TEST','item':'Canário sem poder próprio',
                    'familia':'acessório','rank_item':rank,'historico':False,'habilidades':[], 'bonus':[], 'pesquisa':{}})
                self.assertEqual(v['custo_pa']['pa_por_dia'],EXP_FLOORS[idx]);self.assertEqual(v['custo_pa']['pa_ativacoes_no_cenario'],0)
                self.assertFalse(v['governanca']['party_write'])
    def test_04_five_real_active_and_passive_rates(self):
        for idx,rank in enumerate(RANKS):
            with self.subTest(rank=rank):
                data=copy.deepcopy(FIX)
                data['rank_item']=rank
                for q in data['pesquisa'].values():q['rank_sugerido']=rank
                v=consultar_ficha_craft(data)
                a=v['habilidades']
                self.assertEqual([r['rank_efeito_proposto'] for r in a],[rank,rank])
                self.assertEqual([r['pa_por_dia'] for r in a],[EXP_BASE[idx],EXP_ACTIVE_DAILY[idx]])
                self.assertEqual(a[1]['pa_por_ativacao'],EXP_PER_USE[idx])
                self.assertEqual(a[1]['usos_no_dia'],2)
                if v['custo_pa']['pa_por_dia'] is not None:
                    self.assertEqual(v['custo_pa']['pa_ativacoes_no_cenario'],2*EXP_PER_USE[idx])
    def test_05_numeric_bonuses_do_not_double_count(self):
        v=consultar_ficha_craft(FIX)
        self.assertEqual(v['custo_pa']['parcela_numerica_pa_dia'],10)
        self.assertEqual(v['custo_pa']['pa_por_dia'],25)
        self.assertEqual(v['custo_pa']['pa_ativacoes_no_cenario'],6)
        self.assertEqual(v['custo_pa']['pa_total_no_cenario'],31)
    def test_06_zero_uses_is_not_zero_daily(self):
        x=copy.deepcopy(FIX);x['habilidades'][1]['usos_no_dia']=0
        v=consultar_ficha_craft(x)
        self.assertEqual(v['custo_pa']['pa_por_dia'],25)
        self.assertEqual(v['custo_pa']['pa_ativacoes_no_cenario'],0)
    def test_07_numeric_attack_vs_conditional_recurring_damage(self):
        # Signature verified by regression in original; flag via bridge here.
        x=copy.deepcopy(FIX);x['bonus'].append('+50 de dano de Vento por turno')
        v=consultar_ficha_craft(x)
        self.assertIsNone(v['custo_pa']['pa_por_dia'])
        self.assertIn('PARCIAL',v['gate'])
    def test_08_unknown_pa_is_not_zero(self):
        x=copy.deepcopy(FIX);x['pesquisa']={}
        v=consultar_ficha_craft(x)
        self.assertIsNone(v['custo_pa']['pa_por_dia'])
    def test_09_no_legacy_repricing(self):
        x=copy.deepcopy(FIX);x.update(historico=True,pa_historico={'pa_por_dia':18,'pa_por_ativacao':5})
        v=consultar_ficha_craft(x)
        self.assertIsNone(v['custo_pa']['pa_por_dia'])
        self.assertEqual(v['custo_pa']['pa_historico_preservado'],{'pa_por_dia':18,'pa_por_ativacao':5})
    def test_10_read_only_production_commit_denied(self):
        x=copy.deepcopy(FIX);x['acao']='PUBLICAR_NO_NOTION'
        with self.assertRaises(ContractError):consultar_ficha_craft(x)
    def test_11_incomplete_mobility_stays_open(self):
        x=copy.deepcopy(FIX);x['habilidades'][1]['descricao']='Ao ativar concede velocidade sobrenatural por um turno sem magnitude.'
        v=consultar_ficha_craft(x)
        self.assertIsNone(v['custo_pa']['pa_por_dia'])
    def test_12_party_write_flag_off(self):
        self.assertFalse(consultar_ficha_craft(FIX)['governanca']['party_write'])
    def test_13_deterministic_no_mutation(self):
        x=copy.deepcopy(FIX);y=copy.deepcopy(x)
        self.assertEqual(consultar_ficha_craft(x),consultar_ficha_craft(x));self.assertEqual(x,y)

class R35TwelveIndependentRealSources(unittest.TestCase):
    def test_01_twelve_distinct_real_sources(self):
        self.assertEqual(len(CORPUS),12)
        self.assertEqual(len({x['notion_id'] for x in CORPUS}),12)
        self.assertTrue({'arma','armadura','acessório','artefato','inscrição'}<= {x['family'] for x in CORPUS})
        for c in CORPUS:
            with self.subTest(c=c['id']):
                self.assertEqual(len(c['notion_id']),32)
                self.assertGreater(len(c['ability']),40)
    def test_02_no_original_repriced_on_twelve_cases(self):
        for c in CORPUS:
            with self.subTest(c=c['id']):
                hist={}
                if c['daily'] is not None:hist['pa_por_dia']=c['daily']
                if c['activation'] is not None:hist['pa_por_ativacao']=c['activation']
                req={'acao':'CONSULTAR_PA_TEST','item':c['name'],'familia':c['family'],
                    'rank_item':c['rank'],'historico':True,
                    'habilidades':[{'nome':'Efeito documentado','modalidade':'PASSIVA','descricao':c['ability']}],
                    'pa_historico':hist,'bonus':[],'pesquisa':{}}
                actual=consultar_ficha_craft(req)
                self.assertIsNone(actual['custo_pa']['pa_por_dia'])
                self.assertEqual(actual['custo_pa']['pa_historico_preservado'],hist or None)
                self.assertIn('HISTORICO',actual['gate'])
    def test_03_cases_with_no_energy_remain_unknown(self):
        unknown=[c for c in CORPUS if c['daily'] is None and c['activation'] is None]
        self.assertEqual(len(unknown),4)
    def test_04_known_source_ranks_only_where_explicit(self):
        known=[c for c in CORPUS if c['rank']]
        self.assertEqual(len(known),6)
        self.assertEqual(set(x['rank'] for x in known),{'Ouro','Ouro Negro','Lendário'})
    def test_05_high_risk_comparator_scopes(self):
        art=next(x for x in CORPUS if x['id']=='ART-01')
        self.assertIn('24h',art['ability']);self.assertIn('SC-3/4',art['assertion'])
        ins=next(x for x in CORPUS if x['id']=='INS-02')
        self.assertIn('sete criaturas',ins['ability'])

if __name__=='__main__': unittest.main(verbosity=2)
