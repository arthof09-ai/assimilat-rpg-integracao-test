"""R04 tests use REAL R27 and REAL CRAFT v1.2, never mock PA tariffs."""
from __future__ import annotations
import copy,hashlib,json,os,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent
P=Path(os.environ.get('R04_R27_DIR',ROOT/'pa_r28/provider_r27'))
C=Path(os.environ.get('R04_CRAFT_DIR',ROOT/'craft_v12/CRAFT_RECIPE_PA_LAB_v1_2_CORRIGIDO'))
sys.path.insert(0,str(P));sys.path.insert(0,str(C));sys.path.insert(0,str(ROOT))
from ponte_pa_craft_r27 import consultar_ficha_craft
from pa_nac_preflight import gate as craft_gate
from R04_VINCULO_RECIBO_CRAFT_TEST import bind_and_run

class R04RealBinding(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recipe=json.loads((C/'receita_test_input.json').read_text())
        cls.request=json.loads((C/'pa_r27_request.json').read_text())
        cls.raw=(C/'pa_r27_receipt_fresh_R26_UNCHANGED.json').read_bytes()
        cls.receipt=json.loads(cls.raw)
        cls.boots=consultar_ficha_craft(json.loads((P/'fixture_craft_acessorio.json').read_text()))
    def bound(self,recipe=None,request=None,raw=None):
        return bind_and_run(recipe if recipe is not None else copy.deepcopy(self.recipe),
                            request if request is not None else copy.deepcopy(self.request),
                            raw if raw is not None else self.raw,
                            native_r27=consultar_ficha_craft,native_craft_gate=craft_gate,
                            r48_executable=True,r48_recipe_executed=False)
    def test_01_actual_baseline_is_bound(self):
        r=self.bound();self.assertEqual(r['state'],'BOUND_TEST_RECEIPT_R27_TO_CRAFT_V12');self.assertTrue(r['receipt_bound'])
    def test_02_costs_from_original(self):
        self.assertEqual(self.bound()['scenario_pa'],{'daily':12,'activations':14,'scenario_total':26})
    def test_03_craft_not_green(self):
        r=self.bound();self.assertEqual(r['production'],'DENY');self.assertEqual(r['original_craft_gate']['qa_ceiling_test_only'],'RC4')
    def test_04_no_rights(self):
        r=self.bound();self.assertIsNone(r['writer']);self.assertFalse(r['notion_write']);self.assertFalse(r['party_write']);self.assertIsNone(r['authoritative_RE_E0'])
    def test_05_receipt_source_sha_anchor(self):
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(),self.recipe['pa']['source_receipt_sha256'])
    def test_06_r27_native_recomputed_byte_semantic_equivalence(self):
        self.assertEqual(consultar_ficha_craft(self.request),self.receipt)
    def test_07_original_craft_silent_wrong_item_documented(self):
        result=craft_gate(self.recipe,self.boots,r48_executable=True,r48_recipe_executed=False)
        self.assertTrue(result['pa_version_compatible']);self.assertEqual(result['production'],'DENY')
    def test_08_swap_boots_denied(self):
        alt=json.dumps(self.boots,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n'
        self.assertEqual(self.bound(raw=alt)['state'],'HOLD_RECEIPT_SHA_NOT_BOUND_TO_RECIPE')
    def test_09_tampered_recipe_amount_denied(self):
        r=copy.deepcopy(self.recipe);r['pa']['daily']['amount']=99
        self.assertEqual(self.bound(recipe=r)['state'],'HOLD_RECIPE_PA_TOTALS_NOT_PROVIDER')
    def test_10_tampered_recipe_total_denied(self):
        r=copy.deepcopy(self.recipe);r['pa']['scenario_total']=999
        self.assertEqual(self.bound(recipe=r)['state'],'HOLD_RECIPE_PA_TOTALS_NOT_PROVIDER')
    def test_11_tampered_recipe_per_use_denied(self):
        r=copy.deepcopy(self.recipe);r['pa']['per_activation']['amount']=99
        self.assertEqual(self.bound(recipe=r)['state'],'HOLD_RECIPE_PER_ACTIVATION_NOT_PROVIDER')
    def test_12_tampered_recipe_use_count_denied(self):
        r=copy.deepcopy(self.recipe);r['pa']['scenario_uses']=3
        self.assertEqual(self.bound(recipe=r)['state'],'HOLD_RECIPE_USES_NOT_PROVIDER')
    def test_13_changed_recipe_name_denied(self):
        r=copy.deepcopy(self.recipe);r['target']['identity']='Tênis do Exílio — TEST E3'
        self.assertEqual(self.bound(recipe=r)['state'],'HOLD_RECIPE_ITEM_IDENTITY_MISMATCH')
    def test_14_changed_source_hash_denied(self):
        r=copy.deepcopy(self.recipe);r['pa']['source_receipt_sha256']='0'*64
        self.assertEqual(self.bound(recipe=r)['state'],'HOLD_RECEIPT_SHA_NOT_BOUND_TO_RECIPE')
    def test_15_modified_request_denied(self):
        q=copy.deepcopy(self.request);q['habilidades'][1]['usos_no_dia']=1
        self.assertEqual(self.bound(request=q)['state'],'HOLD_ORIGINAL_PROVIDER_RESULT_MISMATCH')
    def test_16_altered_receipt_content_denied(self):
        p=copy.deepcopy(self.receipt);p['custo_pa']['pa_por_dia']=99
        alt=json.dumps(p,sort_keys=True,ensure_ascii=False,indent=2).encode()+b'\n'
        self.assertEqual(self.bound(raw=alt)['state'],'HOLD_RECEIPT_SHA_NOT_BOUND_TO_RECIPE')
    def test_17_duplicate_json_key_denied(self):
        self.assertEqual(self.bound(raw=b'{"x":1,"x":2}')['state'],'HOLD_RECIBO_JSON_INVALIDO')
    def test_18_nan_injection_denied(self):
        self.assertEqual(self.bound(raw=b'{"x":NaN}')['state'],'HOLD_RECIBO_JSON_INVALIDO')
    def test_19_receipt_not_json_denied(self):
        self.assertEqual(self.bound(raw=b'HELLO')['state'],'HOLD_RECIBO_JSON_INVALIDO')
    def test_20_too_large_denied(self):
        self.assertEqual(self.bound(raw=b'X'*300000)['state'],'HOLD_RECIBO_JSON_INVALIDO')
    def test_21_history_denied(self):
        q=copy.deepcopy(self.request);q['historico']=True
        self.assertEqual(self.bound(request=q)['state'],'HOLD_ORIGINAL_PROVIDER_RESULT_MISMATCH')
    def test_22_missing_rank_denied(self):
        q=copy.deepcopy(self.request);q['rank_item']=None
        self.assertIn(self.bound(request=q)['state'],('HOLD_ORIGINAL_PROVIDER_RESULT_MISMATCH','HOLD_ORIGINAL_PROVIDER_REJECTED_REQUEST'))
    def test_23_unknown_production_action_denied(self):
        q=copy.deepcopy(self.request);q['acao']='PUBLICAR'
        self.assertEqual(self.bound(request=q)['state'],'HOLD_ORIGINAL_PROVIDER_REJECTED_REQUEST')
    def test_24_r27_duplicate_name_denied(self):
        q=copy.deepcopy(self.request);q['habilidades'][1]['nome']=q['habilidades'][0]['nome']
        self.assertEqual(self.bound(request=q)['state'],'HOLD_ORIGINAL_PROVIDER_REJECTED_REQUEST')
    def test_25_per_activation_needs_itemization(self):
        # Keep the R27 receipt consistent and update the recipe source pin for a
        # DIFFERENT synthetic design. The v1.2 recipe schema's single rate cannot
        # safely represent this pair. No pricing arithmetic is reproduced here.
        q=copy.deepcopy(self.request)
        q['habilidades'].append({'nome':'Sopro Secundário','modalidade':'ATIVA','descricao':'Com uma ação padrão, por 1 turno ilumina a área adjacente.','usos_no_dia':1})
        q['pesquisa']['Sopro Secundário']={'rank_sugerido':'Bronze','risco':'SC-1','justificativa':'Fixture sintética somente TEST; sem alegação E0.','comparadores': [{'url':'https://app.notion.com/p/3eec2b324ede81ea8920c52473ecc3ab','tipo':'sistemico','comparacao_mecanica':'Comparador TEST não constitui homologação.'}]}
        fresh=consultar_ficha_craft(q)
        raw=json.dumps(fresh,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n'
        # Only if full cost available; this test checks correspondence gate,
        # not endorsement of effects or funding.
        if fresh['custo_pa']['pa_por_dia'] is None:self.skipTest('R27 kept multi-active synthetic fixture in HOLD (desired)')
        r=copy.deepcopy(self.recipe)
        r['pa']['source_receipt_sha256']=hashlib.sha256(raw).hexdigest()
        r['pa']['daily']['amount']=fresh['custo_pa']['pa_por_dia']
        r['pa']['scenario_total']=fresh['custo_pa']['pa_total_no_cenario']
        r['pa']['scenario_uses']=3
        self.assertEqual(self.bound(recipe=r,request=q,raw=raw)['state'],'HOLD_PER_ACTIVATION_FIELD_NEEDS_ITEMIZATION')
    def test_26_wrong_source_rank_not_repriced(self):
        q=copy.deepcopy(self.request);q['rank_item']='Bronze'
        self.assertNotEqual(self.bound(request=q)['state'],'BOUND_TEST_RECEIPT_R27_TO_CRAFT_V12')
    def test_27_same_scenario_no_mutation(self):
        r=copy.deepcopy(self.recipe);q=copy.deepcopy(self.request);self.bound(recipe=r,request=q);self.assertEqual(r,self.recipe);self.assertEqual(q,self.request)
    def test_28_bad_receipt_type_fails_closed(self):
        self.assertEqual(self.bound(raw='not bytes')['state'],'HOLD_RECIBO_JSON_INVALIDO')
    def test_29_bad_recipe_pa_fields_fails_closed(self):
        r=copy.deepcopy(self.recipe);r['pa']['daily']['amount']=True
        self.assertEqual(self.bound(recipe=r)['state'],'HOLD_RECIPE_PA_FIELDS_INVALID')
    def test_30_manual_production_claim_not_conferred(self):
        r=self.bound();self.assertEqual(r['official_pa'],None);self.assertEqual(r['original_craft_gate']['official_rec_ids'],0)

if __name__=='__main__':unittest.main(verbosity=2)
