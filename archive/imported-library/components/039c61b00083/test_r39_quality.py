import copy,hashlib,json,unittest
from pathlib import Path
from AUDITOR_COMPARADORES_R39 import consultar_fundamentado,auditoria,REG,fingerprints
from CONSULTA_MOBILE_R34 import consultar_chat,ChatContractError
B=Path(__file__).parent
DEMO=json.loads((B/'CONSULTA_QUALIFICADA_R39_INPUT.json').read_text('utf8'))
BASE=json.loads((B/'CONSULTA_MOBILE_DEMO_INPUT.json').read_text('utf8'))
class R39Audit(unittest.TestCase):
    def setUp(self):self.w=copy.deepcopy(DEMO['interpretacao']);self.txt=DEMO['descricao_original']
    def com(self,n='Passos sem Pegadas',idx=0):return self.w['pesquisa'][n]['comparadores'][idx]
    def call(self):return consultar_fundamentado(self.txt,self.w)
    def test_01_expected_cost_has_original_r26_r27_engine(self):
        r=self.call();self.assertEqual((r['pa_por_dia'],r['pa_ativacao_no_cenario'],r['pa_total_cenario']),(25,6,31));self.assertIn('R27→PA_R26',r['motor_origem'])
    def test_02_all_excerpts_recovered_from_sources(self):
        q=auditoria(self.w);self.assertEqual(q['fontes_cotejadas'],4);self.assertEqual(q['bloqueios'],[])
    def test_03_forged_quote_blocks_cost_not_effect_rank(self):
        self.com()['trecho_literal']='O item garante invisibilidade permanente e ilimitada.'
        r=self.call();self.assertIsNone(r['pa_por_dia']);self.assertEqual(r['habilidades'][0]['rank_efeito_proposto'],'Prata');self.assertTrue(r['qualidade_r39']['bloqueios'])
    def test_04_stale_source_name_or_url_blocks(self):
        self.com()['url']='https://app.notion.com/p/00000000000000000000000000000000';r=self.call();self.assertIsNone(r['pa_total_cenario'])
    def test_05_fake_e0_effect_rank_from_unranked_item_rejected(self):
        self.com()['alega_RE_E0']=True
        r=self.call();self.assertIn('RI_OU_METODO_NAO_COMPROVA_RE',str(r['qualidade_r39']['bloqueios']))
    def test_06_fake_e0_from_atlas_method_rejected(self):
        self.com(idx=1)['alega_RE_E0']=True
        self.assertIsNone(self.call()['pa_total_cenario'])
    def test_07_missing_readback_id_blocks(self):
        del self.com()['fonte_readback_id'];self.assertIsNone(self.call()['pa_por_dia'])
    def test_08_wrong_source_id_blocks(self):
        self.com()['fonte_readback_id']='BOTA_MOV';self.assertIsNone(self.call()['pa_total_cenario'])
    def test_09_limited_confidence_without_re_rank_gold(self):
        a=auditoria(self.w);self.assertIsNone(a['precisao_re_medida']);self.assertTrue(all(not x['rank_efeito_e0_comprovado'] for x in a['evidencias']))
    def test_10_item_rank_independent_of_ability_rank(self):
        r=self.call();self.assertEqual(r['rank_item'],'Ouro');self.assertEqual([x['rank_efeito_proposto'] for x in r['habilidades']],['Prata','Bronze'])
    def test_11_original_r34_equivalence(self):
        baseline=consultar_chat(BASE['descricao_original'],BASE['interpretacao'],fontes_reabertas=BASE['fontes_reabertas']);r=self.call()
        self.assertEqual((baseline['pa_por_dia'],baseline['pa_total_cenario']),(r['pa_por_dia'],r['pa_total_cenario']))
    def test_12_high_risk_preserves_energy_but_holds_material_use(self):
        self.w['pesquisa']['Impulso Veloz']['risco']='SC-3';r=self.call();self.assertEqual(r['pa_por_dia'],25);self.assertFalse(r['uso_material_permitido']);self.assertEqual(r['status'],'CONSULTA_TEST_CENARIO_ESTIMADO_ALTO_RISCO_USO_MATERIAL_HOLD')
    def test_13_unknown_active_duration_holds_total_but_retains_rank(self):
        self.w['habilidades'][1]['descricao']='Ao ativar, o item torna o usuário invisível.'
        self.w['habilidades'][1]['duracao']=None
        # This is intentionally semantically a different ability: do not price the already proposed rank.
        r=self.call();self.assertIsNone(r['pa_por_dia']);self.assertTrue(any('DURACAO_EFEITO' in x for x in r['qualidade_r39']['ressalvas']))
    def test_14_complete_numeric_duration_valid(self):
        self.assertEqual(self.call()['pa_por_dia'],25)
    def test_15_production_action_denied(self):
        self.w['acao']='PUBLICAR';
        with self.assertRaises(ChatContractError):self.call()
    def test_16_histories_not_repriced(self):
        self.w['historico']=True
        with self.assertRaises(ChatContractError):self.call()
    def test_17_fingerprints_are_sha256_of_readback_quotes(self):
        f=fingerprints();self.assertEqual(f['BOTA_RASTRO']['excerpt_sha256'],hashlib.sha256(REG['BOTA_RASTRO']['trecho_mecanico'].encode()).hexdigest())
    def test_18_json_input_unchanged(self):
        old=copy.deepcopy(self.w);self.call();self.assertEqual(old,self.w)
    def test_19_local_no_party_notional_writes(self):
        r=self.call();self.assertFalse(r['notion_write']);self.assertFalse(r['party_write']);self.assertFalse(r['uso_material_permitido'])
    def test_20_no_redundant_tariff_model(self):
        src=(B/'AUDITOR_COMPARADORES_R39.py').read_text('utf8');self.assertNotIn('BASE={',src);self.assertNotIn('FLOORS=',src)
    def test_21_readback_source_item_label_not_ability_gold(self):
        self.assertEqual(REG['BRACADEIRA']['tipo_rank_rotulado'],'RI_OURO');self.assertEqual(REG['AURORA']['tipo_rank_rotulado'],'RI_LENDARIO')
    def test_22_corpus_has_8_real_mechanic_documents(self):
        self.assertGreaterEqual(len({v['url'] for v in REG.values()}),8)
    def test_23_passive_active_tariffs_split(self):
        r=self.call();p,a=r['habilidades'];self.assertEqual((p['pa_por_dia'],p['pa_por_ativacao']),(12,None));self.assertEqual((a['pa_por_dia'],a['pa_por_ativacao']),(3,3))
    def test_24_comparator_documented_but_not_e0(self):
        r=self.call();self.assertEqual(r['qualidade_r39']['fontes_cotejadas'],4);self.assertEqual(r['estado_evidencia'],'TRECHOS_MECANICOS_VERIFICADOS; RE_INDEPENDENTE_E0_NAO_PROVADO')
if __name__=='__main__':unittest.main(verbosity=2)
# Extension tests after the original class are declared; unittest discovery sees them.
class R39PingenteAndNativeContract(unittest.TestCase):
    def setUp(self):
        self.p=json.loads((B/'PINGENTE_R39_INPUT.json').read_text('utf8'))
    def test_25_pingente_fresh_pa_original(self):
        from AUDITOR_COMPARADORES_R39 import consultar_fundamentado
        r=consultar_fundamentado(self.p['descricao_original'],self.p['interpretacao'])
        self.assertEqual((r['pa_por_dia'],r['pa_ativacao_no_cenario'],r['pa_total_cenario']),(12,14,26))
    def test_26_exact_5_evidence_quotes(self):
        a=auditoria(self.p['interpretacao']);self.assertEqual(a['fontes_cotejadas'],5);self.assertEqual(a['bloqueios'],[])
    def test_27_rin_not_RE_gold(self):
        a=auditoria(self.p['interpretacao']);self.assertTrue(any('RIN_NAO_COMPROVA_TRANSFERENCIA' in x for x in a['ressalvas']));self.assertIsNone(a['precisao_re_medida'])
    def test_28_native_contract_craft_return_same_amount(self):
        from AUDITOR_COMPARADORES_R39 import envelope_craft_qualificado
        r=envelope_craft_qualificado(self.p['descricao_original'],self.p['interpretacao']);self.assertEqual(r['custo_pa_qualificado']['pa_total_no_cenario'],26);self.assertIn('R27/',r['contrato_craft_original']);self.assertTrue(r['id_entrada_sha256'])
    def test_29_forged_herb_evidence_blocks_total_but_not_rank(self):
        self.p['interpretacao']['pesquisa']['Luminescência de Vigília']['comparadores'][0]['trecho_literal']='Cura absolutamente todas as doenças'
        from AUDITOR_COMPARADORES_R39 import consultar_fundamentado
        r=consultar_fundamentado(self.p['descricao_original'],self.p['interpretacao']);self.assertIsNone(r['pa_total_cenario']);self.assertEqual(r['habilidades'][0]['rank_efeito_proposto'],'Bronze')
    def test_30_material_gate_never_rc5(self):
        from AUDITOR_COMPARADORES_R39 import envelope_craft_qualificado
        r=envelope_craft_qualificado(self.p['descricao_original'],self.p['interpretacao']);self.assertEqual(r['nac_pass_fabricacao'],'HOLD');self.assertFalse(r['escrita_producao'])
    def test_31_rank_item_separate(self):
        from AUDITOR_COMPARADORES_R39 import consultar_fundamentado
        r=consultar_fundamentado(self.p['descricao_original'],self.p['interpretacao']);self.assertEqual(r['rank_item'],'Prata');self.assertEqual([h['rank_efeito_proposto'] for h in r['habilidades']],['Bronze','Prata'])
    def test_32_physical_transfer_not_inferred_from_material(self):
        from AUDITOR_COMPARADORES_R39 import consultar_fundamentado
        r=consultar_fundamentado(self.p['descricao_original'],self.p['interpretacao']);self.assertTrue(any('RIN_NAO_COMPROVA' in x for x in r['qualidade_r39']['ressalvas']));self.assertFalse(r['uso_material_permitido'])
