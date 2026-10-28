import copy, importlib.util, json, tempfile, unittest
from pathlib import Path
from .r48_pingente_adapter import (map_recipe, admission, verify_orig_engine, AdapterBlocked,
    KEY,CASE,CORE,HERB,FIBER)
from .magic_controls import run_deck, evaluate, DECK

BASE=Path(__file__).resolve().parents[1]
FIX=BASE/'fixtures'

def fixtures():
    return (json.loads((FIX/'recipe.json').read_text()),
            json.loads((FIX/'pa_gate.json').read_text()),
            json.loads((FIX/'r48_archived_contract.json').read_text()))

class Core(unittest.TestCase):
    def setUp(self):
        self.rec,self.pa,self.archive=fixtures()
    def mapping(self):return map_recipe(self.rec,self.pa,self.archive)
    def test_mapping_admits_known_case(self):self.assertEqual(self.mapping()['case_id'],CASE)
    def test_exact_source_set(self):self.assertEqual({x['source_page_id'] for x in self.mapping()['trace_bom']},{CORE,HERB,FIBER})
    def test_rank_item_vs_ability_not_inferred(self):self.assertEqual(self.rec['target']['family'],'EQUIPAMENTO')
    def test_no_official_output(self):self.assertIsNone(self.mapping()['recipe_candidate']['official_rec_id'])
    def test_explicit_no_r48_success(self):self.assertEqual(self.mapping()['kind'],'INPUT_ADAPTER_ONLY_NOT_FACTORY_OUTPUT')
    def test_zero_physical_magic(self):self.assertFalse(self.mapping()['physical_magic_proven'])
    def test_source_drift_blocks(self):
        r=copy.deepcopy(self.rec);r['bom'][1]['source_ref']='https://app.notion.com/p/00000000000000000000000000000000'
        with self.assertRaisesRegex(AdapterBlocked,'SOURCE_SET_CHANGED'):map_recipe(r,self.pa,self.archive)
    def test_qty_zero_blocks(self):
        r=copy.deepcopy(self.rec);r['bom'][0]['qty']=0
        with self.assertRaisesRegex(AdapterBlocked,'NONPOSITIVE_BOM'):map_recipe(r,self.pa,self.archive)
    def test_unauthorized_write_blocks(self):
        r=copy.deepcopy(self.rec);r['request_write']=True
        with self.assertRaisesRegex(AdapterBlocked,'OFFICIAL_WRITE_FORBIDDEN'):map_recipe(r,self.pa,self.archive)
    def test_forged_case_id_blocks(self):
        r=copy.deepcopy(self.rec);r['case_id']='DUPLICATE-ID'
        with self.assertRaisesRegex(AdapterBlocked,'WRONG_OR_NON_TEST_CASE'):map_recipe(r,self.pa,self.archive)
    def test_process_unaccounted_material_blocks(self):
        r=copy.deepcopy(self.rec);r['operations'][0]['inputs'].append('UNREGISTERED_GLUE')
        with self.assertRaisesRegex(AdapterBlocked,'PROCESS_INPUT_NOT_PRODUCED'):map_recipe(r,self.pa,self.archive)
    def test_final_node_missing_blocks(self):
        r=copy.deepcopy(self.rec);r['final_node']='NONEXISTENT'
        with self.assertRaisesRegex(AdapterBlocked,'FINAL_NODE_UNREACHABLE'):map_recipe(r,self.pa,self.archive)
    def test_operation_drift_blocks(self):
        r=copy.deepcopy(self.rec);r['operations'].pop()
        with self.assertRaisesRegex(AdapterBlocked,'OPERATIONS_CHANGED'):map_recipe(r,self.pa,self.archive)
    def test_pa_mismatch_blocks(self):
        p=copy.deepcopy(self.pa);p['pa_version_compatible']=False
        with self.assertRaisesRegex(AdapterBlocked,'PA_PREVALIDATOR_NOT_COMPATIBLE'):map_recipe(self.rec,p,self.archive)
    def test_pa_day_drift_blocks(self):
        p=copy.deepcopy(self.pa);p['pa_provider_reported_total_not_approved']['pa_por_dia']=999
        with self.assertRaisesRegex(AdapterBlocked,'PA_PROVIDER_RECEIPT_CHANGED'):map_recipe(self.rec,p,self.archive)
    def test_pa_activation_drift_blocks(self):
        p=copy.deepcopy(self.pa);p['pa_provider_reported_total_not_approved']['pa_ativacoes_no_cenario']=999
        with self.assertRaisesRegex(AdapterBlocked,'PA_ACTIVATION_SCENARIO_CHANGED'):map_recipe(self.rec,p,self.archive)
    def test_archived_schema_missing_blocks(self):
        a=copy.deepcopy(self.archive);a.pop('SBX-TLI-R44-v1')
        with self.assertRaisesRegex(AdapterBlocked,'ORIGINAL_R48_RECIPE_CONTRACT_UNVERIFIED'):map_recipe(self.rec,self.pa,a)
    def test_archived_allowlist_expected(self):
        with tempfile.TemporaryDirectory() as t:
            report=admission(self.rec,self.pa,self.archive,Path(t))
            self.assertIn('R48_ORIGINAL_ALLOWLIST_REJECTS_PINGENTE',report['blocks'])
            self.assertIn('R46_MAGIC_QA_SCHEMA_UNSUPPORTED',report['blocks'])
            self.assertFalse(report['original_engine_invoked'])
            self.assertIsNone(report['r48_receipt'])
    def test_engine_absent_refuses(self):
        with tempfile.TemporaryDirectory() as t:
            report=verify_orig_engine(Path(t));self.assertFalse(report['ok']);self.assertEqual(len(report['defects']),3)
    def test_engine_wrong_hash_refuses(self):
        with tempfile.TemporaryDirectory() as t:
            path=Path(t)/'r48_factory.py';path.write_text('DANGEROUS_FAKE_ENGINE')
            a=verify_orig_engine(Path(t));self.assertTrue(any('HASH_MISMATCH' in x for x in a['defects']))
    def test_no_separate_PA_engine_created(self):self.assertEqual(self.pa['pa_policy_id'],'MESTRE-PA-ATIVA-DIA50-USO60-20261020-CORRIGIDO')
    def test_rc5_never_awarded_without_magic(self):
        with tempfile.TemporaryDirectory() as t:
            a=admission(self.rec,self.pa,self.archive,Path(t));self.assertFalse(a['RC5'])
    def test_sources_identified_as_test(self):
        c=self.mapping()['recipe_candidate'];self.assertTrue(c['testable_only_in_sandbox'])
        self.assertEqual(c['source_status'],'FONTE_MESTRE + PS_NAO_P4')
    def test_no_magic_benefit_from_fiber(self):
        r=self.mapping();f=[x for x in r['trace_bom'] if x['source_page_id']==FIBER][0]
        self.assertEqual(f['role'],'ligante');self.assertEqual(f['evidence_kind'],'MATERIAL_PS_NAO_P4')
    def test_r46_zero_magic_qa_as_missing(self):self.assertEqual(self.mapping()['recipe_candidate']['qa_rules'],[])
    def test_r48_orders_require_true_attestation(self):self.assertIn('attestation',self.mapping()['r48_expected_order_fields'])

class Controls(unittest.TestCase):
    def test_five_controls_distinct(self):self.assertEqual(len({x[0] for x in DECK}),5)
    def test_negative_fails(self):self.assertEqual(evaluate(DECK[0])['outcome'],'NEGATIVE_CONTROL_NO_MAGIC_COMPONENT')
    def test_partial_fails(self):self.assertEqual(evaluate(DECK[1])['outcome'],'PARTIAL_LIGHT_ONLY_NO_ACTIVE_CORE')
    def test_energy_fails(self):self.assertEqual(evaluate(DECK[2])['outcome'],'REJECTED_SYNTHETIC_ENERGY_BUDGET')
    def test_stability_fails(self):self.assertEqual(evaluate(DECK[3])['outcome'],'REJECTED_SYNTHETIC_STABILITY')
    def test_full_is_unobserved(self):self.assertEqual(evaluate(DECK[4])['outcome'],'DOCUMENT_COMPLETE_MAGIC_UNOBSERVED')
    def test_not_one_magic_proven(self):self.assertTrue(run_deck()['none_falsely_approved'])
    def test_no_physical_measurements_claimed(self):self.assertTrue(all(x['physical_measurements'] is None for x in run_deck()['deck']))
    def test_no_r48_claimed(self):self.assertTrue(all(x['factory_R48_executed'] is False for x in run_deck()['deck']))

if __name__=='__main__':unittest.main()
