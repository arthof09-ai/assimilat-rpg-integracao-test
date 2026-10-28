from __future__ import annotations
import copy, hashlib, json, subprocess, sys, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import qmc05
import test_qmc05
import pa_r28_native as R
PROPOSAL=json.loads((ROOT.parents[1]/'PROJETO_COMPATIVO_LAMINA_E3.json').read_text())

class R28NativeIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lam=test_qmc05.get('lamina')
        cls.top=test_qmc05.get('topazio')
        cls.armor=test_qmc05.get('acolchoada')
        cls.seal=test_qmc05.get('selo')

    def test_01_native_result(self):
        self.assertEqual(self.lam['state'],'QMC05_PARECER_DOCUMENTAL_TEST')
    def test_02_exact_original_source(self):
        x=R.integrar_qualificado(self.lam)
        self.assertEqual(x['origem']['uuid'],'3edc2b324ede816f98a1fa7babd3c0d3')
        self.assertEqual(x['origem']['source_sha256'],self.lam['qmc04']['readback']['complete_content_sha256'])
    def test_03_historical_is_not_repriced(self):
        x=R.integrar_qualificado(self.lam)
        self.assertIsNone(x['historico']['r27']['pa_por_dia'])
        self.assertIsNone(x['historico']['projecao_energetica'])
    def test_04_unmapped_mode_preserved(self):
        x=R.integrar_qualificado(self.lam)
        self.assertEqual(len(x['historico']['efeitos_sem_modalidade']),1)
        self.assertEqual(x['historico']['efeitos_sem_modalidade'][0]['effect_id'],'E02')
    def test_05_no_party_writer(self):
        x=R.integrar_qualificado(self.lam)
        self.assertFalse(x['governanca']['PARTY_WRITE']);self.assertFalse(x['governanca']['primeiro_write'])
        self.assertFalse(x['governanca']['notion_write']);self.assertEqual(x['governanca']['receitas_criadas'],0)
    def test_06_unknown_pa_stays_unknown(self):
        x=R.integrar_qualificado(self.top)
        self.assertEqual(x['historico']['pa_documentado']['daily'],[])
        self.assertIsNone(x['historico']['r27']['pa_por_dia'])
    def test_07_armor_physical_ca_not_magic_price(self):
        x=R.integrar_qualificado(self.armor)
        self.assertEqual(x['origem']['effect_count'],4)
        self.assertIsNone(x['historico']['r27']['pa_por_dia'])
    def test_08_seal_rank_does_not_reprice(self):
        x=R.integrar_qualificado(self.seal)
        self.assertEqual(x['origem']['rank_item_original'],'Prata')
        self.assertIsNone(x['historico']['r27']['pa_por_dia'])
    def test_09_real_external_r27_called(self):
        x=R.integrar_qualificado(self.lam)
        self.assertIn('r27.consultar_ficha_craft',x['call_chain'])
        self.assertEqual(x['provider_contract'],R.SCHEMA_VERSION)
    def test_10_real_comparison(self):
        x=R.integrar_qualificado(self.lam,copy.deepcopy(PROPOSAL))
        p=x['cenario_novo']['r27_result']['habilidades'][0]
        self.assertEqual(p['rank_efeito_proposto'],'Prata')
        self.assertEqual(p['confianca'],'MEDIA')
        self.assertEqual((p['pa_por_dia'],p['pa_por_ativacao']),(6,7))
    def test_11_hypothesis_keeps_unknown_duration(self):
        x=R.integrar_qualificado(self.lam,copy.deepcopy(PROPOSAL))
        self.assertIn('DURACAO_ATIVA_NAO_DOCUMENTADA:E01',x['cenario_novo']['assumptions'])
        self.assertIsNone(x['cenario_novo']['r27_result']['custo_pa']['pa_por_dia'])
    def test_12_not_canonized(self):
        x=R.integrar_qualificado(self.lam,copy.deepcopy(PROPOSAL))
        self.assertTrue(x['cenario_novo']['nunca_e_item_canonico'])
        self.assertFalse(x['cenario_novo']['uso_material_permitido'])
    def test_13_reject_mismatched_source(self):
        q=copy.deepcopy(PROPOSAL);q['fonte_qmc05_uuid']='00000000000000000000000000000000'
        with self.assertRaises(R.R28ContractError):R.integrar_qualificado(self.lam,q)
    def test_14_reject_wrong_mode(self):
        q=copy.deepcopy(PROPOSAL);q['efeitos_selecionados'][0]['modalidade']='PASSIVA'
        with self.assertRaises(R.R28ContractError):R.integrar_qualificado(self.lam,q)
    def test_15_reject_new_unproven_effect_id(self):
        q=copy.deepcopy(PROPOSAL);q['efeitos_selecionados'][0]['effect_id']='E99'
        with self.assertRaises(R.R28ContractError):R.integrar_qualificado(self.lam,q)
    def test_16_reject_duplicate_effect_id(self):
        q=copy.deepcopy(PROPOSAL);q['efeitos_selecionados'].append(copy.deepcopy(q['efeitos_selecionados'][0]))
        with self.assertRaises(R.R28ContractError):R.integrar_qualificado(self.lam,q)
    def test_17_reject_no_comparator(self):
        q=copy.deepcopy(PROPOSAL);q['efeitos_selecionados'][0]['pesquisa']['comparadores']=[]
        with self.assertRaises(R.R28ContractError):R.integrar_qualificado(self.lam,q)
    def test_18_reject_fake_comparator_domain(self):
        q=copy.deepcopy(PROPOSAL);q['efeitos_selecionados'][0]['pesquisa']['comparadores'][0]['url']='https://evil.example/a'
        with self.assertRaises(R.R28ContractError):R.integrar_qualificado(self.lam,q)
    def test_19_reject_creating_proposal_by_repricing_same_item(self):
        q=copy.deepcopy(PROPOSAL);q['item_novo']='Lâmina Eclipse'
        with self.assertRaises(R.R28ContractError):R.integrar_qualificado(self.lam,q)
    def test_20_reject_non_original_fixture(self):
        with self.assertRaises(R.R28ContractError):R.integrar_qualificado({'state':'FAKE'})
    def test_21_reject_uuid_mismatch_in_native(self):
        v=copy.deepcopy(self.lam);v['structured_effects']['item_uuid']='x'
        with self.assertRaises(R.R28ContractError):R.integrar_qualificado(v)
    def test_22_determinism(self):
        a=R.integrar_qualificado(self.lam,copy.deepcopy(PROPOSAL));b=R.integrar_qualificado(self.lam,copy.deepcopy(PROPOSAL))
        self.assertEqual(a,b)
    def test_23_no_input_mutation(self):
        q=copy.deepcopy(PROPOSAL);before=copy.deepcopy(q);R.integrar_qualificado(self.lam,q)
        self.assertEqual(q,before)
    def test_24_cli_native_readonly(self):
        src=ROOT/'holdout/lamina.txt';url='https://app.notion.com/p/3edc2b324ede816f98a1fa7babd3c0d3'
        cmd=[sys.executable,str(ROOT/'qmc05.py'),'--url',url,'--readback',str(src),'--pa-r28']
        v=subprocess.run(cmd,capture_output=True,text=True,check=True)
        j=json.loads(v.stdout)
        self.assertEqual(j['contrato'],R.SCHEMA)
    def test_25_cli_native_proposal(self):
        src=ROOT/'holdout/lamina.txt';url='https://app.notion.com/p/3edc2b324ede816f98a1fa7babd3c0d3'
        cmd=[sys.executable,str(ROOT/'qmc05.py'),'--url',url,'--readback',str(src),'--pa-r28','--pa-projeto-json',str(ROOT.parents[1]/'PROJETO_COMPATIVO_LAMINA_E3.json')]
        v=subprocess.run(cmd,capture_output=True,text=True,check=True)
        j=json.loads(v.stdout);self.assertEqual(j['cenario_novo']['r27_result']['habilidades'][0]['pa_por_dia'],6)
    def test_26_legacy_cli_unchanged(self):
        url='https://app.notion.com/p/3edc2b324ede816f98a1fa7babd3c0d3'
        v=subprocess.run([sys.executable,str(ROOT/'qmc05.py'),'--url',url,'--readback',str(ROOT/'holdout/lamina.txt')],capture_output=True,text=True,check=True)
        self.assertIn('Lâmina Eclipse',v.stdout);self.assertNotIn(R.SCHEMA,v.stdout)
    def test_27_explicit_synthetic_action_denied_by_r27(self):
        v=R.integrar_qualificado(self.lam,copy.deepcopy(PROPOSAL))
        self.assertEqual(v['cenario_novo']['r27_result']['governanca']['craft_f5'],'RED_PRODUCAO_HOLD')
    def test_28_empty_mode_kept_as_unmapped(self):
        v=R.integrar_qualificado(self.top)
        self.assertEqual(len(v['historico']['efeitos_sem_modalidade']),2)
    def test_29_historical_input_rejects_unknown_branch(self):
        q=copy.deepcopy(PROPOSAL);q['modo']='CANONIZAR'
        with self.assertRaises(R.R28ContractError):R.integrar_qualificado(self.lam,q)
    def test_30_pa_formula_original_regression(self):
        from ponte_pa_craft_r27 import consultar_ficha_craft
        fixture=json.loads((ROOT.parents[1]/'provider_r27/fixture_craft_acessorio.json').read_text())
        p=consultar_ficha_craft(fixture)
        self.assertEqual((p['custo_pa']['pa_por_dia'],p['custo_pa']['pa_ativacoes_no_cenario']), (25,6))

if __name__=='__main__':unittest.main()
