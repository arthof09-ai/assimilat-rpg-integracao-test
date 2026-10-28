import hashlib,zipfile,unittest
from pathlib import Path
from r16_gate import access,authorize_activation,TransformationLocked
from engine_r13 import make_fixture
from historical_bridge_r16 import R10_EXPECTED,R15_EXPECTED,sha
ROOT=Path(__file__).resolve().parent.parent

class NormativeRegressionTests(unittest.TestCase):
    def test_upstream_engine_r13_byte_identical(self):
        with zipfile.ZipFile(ROOT/'historical/UPSTREAM_R11_R15_VERIFIED.zip') as z:
            b=z.read('levelup_r11_r15_addendum/engine_r13.py')
        self.assertEqual(hashlib.sha256(b).hexdigest(),sha(ROOT/'engine_r13.py'))
    def test_upstream_r10_module_byte_identical(self):
        with zipfile.ZipFile(ROOT/'historical/UPSTREAM_R11_R15_VERIFIED.zip') as z:
            b=z.read('levelup_r11_r15_addendum/r10_recovery.py')
        self.assertEqual(hashlib.sha256(b).hexdigest(),sha(ROOT/'r10_recovery.py'))
    def test_verification_hashes(self):
        self.assertEqual(sha(ROOT/'historical/UPSTREAM_R10_VERIFIED.zip'),R10_EXPECTED)
        self.assertEqual(sha(ROOT/'historical/UPSTREAM_R11_R15_VERIFIED.zip'),R15_EXPECTED)
    def test_gate_on_every_ordinal_level(self):
        self.assertEqual(sum(access(level)['can_activate_transformation'] for level in range(1,26)),20)
        self.assertEqual(sum(not access(level)['can_activate_transformation'] for level in range(1,26)),5)
    def test_bronze_spirit_cannot_bypass_level(self):
        b=make_fixture()
        self.assertEqual(b['TRANSFORM']['spirit']['cap'],5)
        with self.assertRaises(TransformationLocked):
            authorize_activation(b['NORMAL']['level'],scene_id='SIM-X',rested=True,used_scene=False)
    def test_master_patch_preserves_bronze_table_history(self):
        t=(ROOT/'R16_CORRECAO_NORMATIVA_PROPOSTA.md').read_text()
        self.assertIn('HISTÓRICA/INAPLICÁVEL',t)
        self.assertIn('Prata 1',t)
        self.assertIn('PENDENTE DE GATES',t)
    def test_party_draft_has_necessary_decisions(self):
        t=(ROOT/'templates/MENSAGENS_PLAYER_SAFE_CANDIDATAS_R16.md').read_text()
        for x in ('quantos pontos de atributos normais','Como deseja dividir','60%','Dano, CA ou Vida','Confirma todas as escolhas','NÃO ENVIADAS'):
            self.assertIn(x.lower(),t.lower())
    def test_no_live_notions_write_code(self):
        for fn in ('r16_gate.py','dialogue_r16.py','historical_bridge_r16.py','native_preflight_r16.py'):
            code=(ROOT/fn).read_text()
            self.assertNotIn('requests.post(',code)
            self.assertNotIn('api.notion.com',code)
            self.assertNotIn('notion_update_page(',code)

if __name__=='__main__':unittest.main()
