import unittest,pathlib
from r186_vz_derived_reconciliation import reconcile_source,SourceBoundHold,SOURCE_ID,SOURCE_VERSION
FIX=pathlib.Path(__file__).resolve().parents[1]/'fixtures/r186_vz_source_excerpt_transcribed.md'
class TestR186(unittest.TestCase):
    def setUp(self):self.txt=FIX.read_text()
    def runreconcile(self,txt=None,id=SOURCE_ID,ver=SOURCE_VERSION):
        return reconcile_source(native_markdown=txt if txt is not None else self.txt,source_id=id,source_version=ver)
    def test_eight_actors(self):self.assertEqual(self.runreconcile()['actor_count'],8)
    def test_darek_conservative(self):self.assertEqual(self.runreconcile()['actors']['Darek']['transform_base']['regime'],'L3 + Espírito ON5 / d20 conservador')
    def test_ff_source_not_added_twice(self):self.assertEqual(self.runreconcile()['actors']['Serah']['ff_integrated']['hp_transform_plus_ff'],1237)
    def test_unsupported_version(self):
        with self.assertRaises(SourceBoundHold):self.runreconcile(ver='not-source')
    def test_source_id(self):
        with self.assertRaises(SourceBoundHold):self.runreconcile(id='party')
    def test_missing_actor(self):
        with self.assertRaises(SourceBoundHold):self.runreconcile(txt=self.txt.replace('<td>Asha</td>','<td>Serah</td>'))
    def test_tamper_hp(self):
        with self.assertRaises(SourceBoundHold):self.runreconcile(txt=self.txt.replace('<td>Serah</td><td>1211</td>', '<td>Serah</td><td>99999</td>'))
    def test_no_write(self):self.assertEqual(self.runreconcile()['native_writes'],0)
    def test_not_party_approved(self):self.assertFalse(self.runreconcile()['host_confirmation'])
    def test_missing_ff_table(self):
        with self.assertRaises(SourceBoundHold):self.runreconcile(txt=self.txt.split('## APLICAÇÃO FF-LOCK — v1.2')[0])
if __name__=='__main__':unittest.main()
