from __future__ import annotations
import copy,json,unittest
from pathlib import Path
from CONSULTA_MOBILE_R34 import consultar_chat,ChatContractError,ficha_md
BASE=Path(__file__).parent
FIX=json.loads((BASE/'CONSULTA_MOBILE_DEMO_INPUT.json').read_text())
class R34MobileRealEngine(unittest.TestCase):
    def make(self):return copy.deepcopy(FIX)
    def test_01_mobile_plain_text_without_forms(self):
        p=self.make();r=consultar_chat(p['descricao_original'],p['interpretacao'],fontes_reabertas=p['fontes_reabertas'])
        self.assertEqual(r['pa_total_cenario'],31);self.assertEqual(r['rank_item'],'Ouro')
    def test_02_effect_ranks_independent(self):
        p=self.make();r=consultar_chat(p['descricao_original'],p['interpretacao'],fontes_reabertas=p['fontes_reabertas'])
        self.assertEqual([a['rank_efeito_proposto'] for a in r['habilidades']],['Prata','Bronze'])
    def test_03_confidence_exposed(self):
        p=self.make();r=consultar_chat(p['descricao_original'],p['interpretacao'],fontes_reabertas=p['fontes_reabertas'])
        self.assertTrue(all(a['confianca'] for a in r['habilidades']))
    def test_04_missing_comparator_readback_blocks_final_cost_but_not_rank(self):
        p=self.make();r=consultar_chat(p['descricao_original'],p['interpretacao'],fontes_reabertas=[])
        self.assertIsNone(r['pa_por_dia']);self.assertEqual(r['habilidades'][0]['rank_efeito_proposto'],'Prata');self.assertTrue(r['comparadores_sem_readback_confirmado'])
    def test_05_high_risk_still_can_be_priced_but_not_materially_used(self):
        p=self.make();p['interpretacao']['pesquisa']['Impulso Veloz']['risco']='SC-3'
        r=consultar_chat(p['descricao_original'],p['interpretacao'],fontes_reabertas=p['fontes_reabertas'])
        self.assertEqual(r['pa_por_dia'],25);self.assertEqual(r['pa_total_cenario'],31)
        self.assertIn('ALTO_RISCO',r['status']);self.assertFalse(r['uso_material_permitido'])
    def test_06_reject_empty_natural_text(self):
        p=self.make()
        with self.assertRaises(ChatContractError):consultar_chat('curto',p['interpretacao'])
    def test_07_reject_production_command(self):
        p=self.make();p['interpretacao']['acao']='PUBLICAR_NO_NOTION'
        with self.assertRaises(ChatContractError):consultar_chat(p['descricao_original'],p['interpretacao'])
    def test_08_never_changes_request(self):
        p=self.make();a=copy.deepcopy(p);consultar_chat(p['descricao_original'],p['interpretacao'],fontes_reabertas=p['fontes_reabertas']);self.assertEqual(p,a)
    def test_09_legacy_without_repricing_requires_r28(self):
        p=self.make();p['interpretacao']['historico']=True
        with self.assertRaises(ChatContractError):consultar_chat(p['descricao_original'],p['interpretacao'])
    def test_10_no_live_notional_writes(self):
        p=self.make();r=consultar_chat(p['descricao_original'],p['interpretacao'],fontes_reabertas=p['fontes_reabertas'])
        self.assertFalse(r['notion_write']);self.assertFalse(r['party_write']);self.assertIsNone(r['writer_lease_epoch'])
    def test_11_ficha_mestre_readable(self):
        p=self.make();s=ficha_md(consultar_chat(p['descricao_original'],p['interpretacao'],fontes_reabertas=p['fontes_reabertas']))
        self.assertIn('25 PA/dia',s);self.assertIn('31 PA',s);self.assertIn('Passos sem Pegadas',s)
    def test_12_deterministic_replay_and_source_hash(self):
        p=self.make();a=consultar_chat(p['descricao_original'],p['interpretacao'],fontes_reabertas=p['fontes_reabertas']);b=consultar_chat(p['descricao_original'],p['interpretacao'],fontes_reabertas=p['fontes_reabertas']);self.assertEqual(a,b)
if __name__=='__main__':unittest.main(verbosity=2)
