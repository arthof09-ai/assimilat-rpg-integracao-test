"""Independent read-only consistency audit of the R70 acceptance matrix.
This is a separate code verifier, not an independent Comestre approval.
"""
import json,unittest
from pathlib import Path
P=Path(__file__).with_name('R70_ACCEPTANCE_MATRIX_20261016.json')
D=json.loads(P.read_text())
class R70Audit(unittest.TestCase):
 def test_ten_domains(self):self.assertEqual(len(D['domains']),10)
 def test_unique_domains(self):self.assertEqual(len({d['domain'] for d in D['domains']}),10)
 def test_nonpromotion(self):self.assertEqual(D['target_full_complex_level_up_down'],'0/2 CERTIFICADOS')
 def test_global_undetermined(self):self.assertEqual(D['overall_progress'],'NAO DETERMINAVEL AINDA')
 def test_no_party(self):self.assertEqual(D['domains'][9]['denominator']['Party_writes'],0)
 def test_no_o_primeiro(self):self.assertEqual(D['domains'][9]['denominator']['O_Primeiro_writes'],0)
 def test_no_source_mutations(self):self.assertEqual(D['domains'][9]['denominator']['source_mutations'],0)
 def test_v05_original(self):self.assertEqual(D['domains'][0]['denominator']['V05_hashes'],'483/483')
 def test_r30_original(self):self.assertEqual(D['domains'][0]['denominator']['R30_hashes'],'57/57')
 def test_r17_not_rerun(self):self.assertIn('not_rerun',list(D['domains'][0]['denominator'])[2])
 def test_media_not_binary(self):self.assertEqual(D['domains'][6]['denominator']['media_binary_sha_audited'],'0/13')
 def test_children_source_A(self):self.assertEqual(D['domains'][2]['denominator']['copy_A_direct_children'],'19/19')
 def test_children_source_B(self):self.assertEqual(D['domains'][2]['denominator']['copy_B_direct_children'],'19/19')
 def test_grandchild_A(self):self.assertEqual(D['domains'][2]['denominator']['A_nested'],'5/5')
 def test_grandchild_B(self):self.assertEqual(D['domains'][2]['denominator']['B_nested'],'5/5')
 def test_tables(self):self.assertEqual(D['domains'][2]['denominator']['evolution_tables'],'11/11')
 def test_columns(self):self.assertEqual(D['domains'][2]['denominator']['evolution_columns'],'8/8')
 def test_full_transform_hold(self):self.assertEqual(D['domains'][4]['denominator']['source_bound_complete'],'0/1')
 def test_historical_children_hold(self):self.assertEqual(D['domains'][7]['denominator']['historical_native_descendants'],'0/24')
 def test_only_four_targeted_fields(self):self.assertEqual(D['experimental_targeted_field_changes'],'4/4 READBACK POSITIVO')
 def test_fail_closed_production(self):self.assertIn('HOLD producao',D['nac_pass_02'])
 def test_first_pending(self):self.assertIn('ledger',D['first_pending'])
if __name__=='__main__':unittest.main(verbosity=2)
