import sys, json, copy, hashlib, pathlib, unittest
ROOT=pathlib.Path('/mnt/data/coord_recovery/qmc/QMC-02/qmc02')
sys.path.insert(0,str(ROOT))
import qmc02
sources=json.loads((ROOT/'source_readbacks.json').read_text())['sources']
class CoordinatorAdversarialAudit(unittest.TestCase):
    def test_real_bota_daily_and_activation(self):
        s=next(x for x in sources if 'Bota Caminho Veloz' in x['title'])
        d=qmc02.inspect_source(s)
        self.assertEqual(d['status'],'QUALIFICACAO_FONTE_AUTORIZADA_EM_EXTRATO')
        self.assertIn(18,[x['value'] for x in d['costs']['daily']]);self.assertIn(5,[x['value'] for x in d['costs']['activation']])
        self.assertEqual(d['recipe_creation'],'PROIBIDA')
    def test_untrusted_source_rejected(self):
        s=copy.deepcopy(sources[0]);s['source_surface']='PARTY'
        self.assertEqual(qmc02.inspect_source(s)['status'],'FONTE_FORA_ESCOPO_MESTRE')
    def test_content_mutated_without_declared_hash_not_detected(self):
        s=copy.deepcopy(sources[0]);s['content'] += ' FAKE EFFECT 999 PA'
        self.assertEqual(qmc02.inspect_source(s)['status'],'QUALIFICACAO_FONTE_AUTORIZADA_EM_EXTRATO')
    def test_content_mutated_with_declared_hash_rejected(self):
        s=copy.deepcopy(sources[0]);s['declared_content_sha256']=qmc02.digest(s['content'])
        s['content'] += ' FAKE EFFECT 999 PA'
        self.assertEqual(qmc02.inspect_source(s)['status'],'EXCERTO_ALTERADO_APOS_EXPORTACAO')
    def test_forged_self_consistent_transcription_is_not_authenticated(self):
        s=copy.deepcopy(sources[0]);s['content'] += '\nPROPOSTA INJETADA SEM FONTE: 999 PA por dia'
        s['declared_content_sha256']=qmc02.digest(s['content'])
        d=qmc02.inspect_source(s)
        self.assertEqual(d['status'],'QUALIFICACAO_FONTE_AUTORIZADA_EM_EXTRATO')
        self.assertIn(999,[x['value'] for x in d['costs']['daily']])
        self.assertIn('assinatura externa não comprovada',d['provenance']['authenticity'])
    def test_iso_r_pa_dia_not_applied_to_35_de_pa(self):
        a=qmc02.extract_costs('Uma adaga mágica.\n35 de PA.')
        self.assertEqual(a['daily'],[]);self.assertEqual(a['activation'],[])
        self.assertIn(35,[x['value'] for x in a['ambiguous']])
    def test_no_pa_or_recipe_from_external_mock(self):
        self.assertEqual(qmc02.validate_external_pa({'kind':'FIXTURE_SIMULADA','PA_dia':3})['status'],'SIMULACAO_NAO_OFICIAL')
if __name__=='__main__':unittest.main(verbosity=2)
