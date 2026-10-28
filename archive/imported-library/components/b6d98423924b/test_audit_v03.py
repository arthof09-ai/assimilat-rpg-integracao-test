import unittest
from audit_regressions_v03 import rows,CASES

class TestAuditV03(unittest.TestCase):
    def test_11_pairs_22_metrics(self):
        self.assertEqual(len(CASES),11)
        self.assertEqual(len(list(rows())),22)
    def test_ye_ouro1_historical_plus2_both(self):
        y=[r for r in rows() if r['personagem'].startswith('Ye Ze') and r['fase_historica']=='Ouro 1']
        self.assertEqual([(r['simulacao_T6_dados_60_porcento'],r['bonus_escrito_na_ficha']) for r in y],[(33,44),(341,352)])
        self.assertTrue(all(r['bate_hipotese_mais_2'] for r in y))
    def test_doze_ouro5_plus2_both(self):
        d=[r for r in rows() if r['personagem'].startswith('Do Ze') and r['fase_historica']=='Ouro 5 (título)']
        self.assertEqual([(r['simulacao_T6_dados_60_porcento'],r['bonus_escrito_na_ficha']) for r in d],[(300,315),(1065,1080)])
    def test_niem_ouro2_alma_fixed_60_matches(self):
        n=[r for r in rows() if r['personagem']=='Nie Li' and r['fase_historica']=='Ouro 2' and r['recurso']=='Alma'][0]
        self.assertEqual(n['simulacao_T6_dados_60_porcento'],264)
        self.assertEqual(n['bonus_escrito_na_ficha'],264)
    def test_zeyun_ouro5_alma_exceeds_any_roll_in_simple_model(self):
        x=[r for r in rows() if r['personagem'].startswith('Ye Ze') and r['fase_historica']=='Ouro 5' and r['recurso']=='Alma'][0]
        self.assertEqual(x['limite_maximo_rolagens_condicional'],840)
        self.assertEqual(x['bonus_escrito_na_ficha'],1256)
        self.assertFalse(x['dentro_do_intervalo_rolagens_condicional'])
    def test_zhu_life_diverges(self):
        n=[r for r in rows() if r['personagem']=='Zhu Feng' and r['recurso']=='Vida'][0]
        self.assertEqual((n['simulacao_T6_dados_60_porcento'],n['bonus_escrito_na_ficha']),(228,156))

if __name__=='__main__':unittest.main()
