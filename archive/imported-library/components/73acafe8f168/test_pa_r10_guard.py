import unittest
from pathlib import Path
from pa_r10_guard import quote_effects, correction_preview, load_r09

R09=Path(__file__).resolve().parent.parent/'PA_P0_R09_CORRIGENDA_TEST_20261018.zip'

def effect(kind,magnitude=1,**kw):return {'id':'e','kind':kind,'magnitude':magnitude,'mode':'PASSIVO_DIARIO',**kw}
class GuardR10(unittest.TestCase):
    def test_r09_identity(self):
        rows,gates,manifest=load_r09(R09)
        self.assertEqual(len(rows),94);self.assertEqual(len(gates),3)
        self.assertEqual(manifest['n_precificavel_r09'],32)
    def test_mira_candidato_nao_homologado(self):
        x=correction_preview('Mira Apurada',R09)
        self.assertEqual((x['historical_daily_pa'],x['proposed_daily_pa_test']),(4,3))
        self.assertFalse(x['can_use_as_canonical_pa'])
    def test_manto_ca_sem_origem(self):
        x=correction_preview('Manto de Proteção',R09)
        self.assertEqual(x['historical_daily_pa'],10)
        self.assertIsNone(x['proposed_daily_pa_test'])
        self.assertEqual(x['hypothetical_daily_if_magical_ca_confirmed'],2)
    def test_mobilidade_retirado(self):
        x=correction_preview('Mobilidade',R09)
        self.assertEqual(x['historical_daily_pa'],7)
        self.assertIsNone(x['proposed_daily_pa_test'])
        self.assertIn('RETIRADO',x['gate'])
    def test_atributo_mais_cinco(self):
        r=quote_effects([effect('ATRIBUTO_PERMANENTE',5,permanent_confirmed=True)],assertion_no_other_effects=True)
        self.assertEqual(r['daily_total_pa'],'25')
    def test_atributo_condicional_nao_autozero(self):
        r=quote_effects([effect('ATRIBUTO_PERMANENTE',5)],assertion_no_other_effects=True)
        self.assertIsNone(r['daily_total_pa'])
    def test_dano_fixo_20_regra_mestre(self):
        r=quote_effects([effect('DANO_FIXO_ADICIONAL',20,damage_is_fixed=True)],assertion_no_other_effects=True)
        self.assertEqual(r['daily_total_pa'],'20')
    def test_dano_critico_condicional_sem_preco_automatico(self):
        r=quote_effects([effect('DANO_FIXO_ADICIONAL',30,damage_is_fixed=True,conditional=True)],assertion_no_other_effects=True)
        self.assertIsNone(r['daily_total_pa'])
    def test_deslocamento_passivo_3(self):
        r=quote_effects([effect('DESLOCAMENTO_PERMANENTE_M',3,permanent_confirmed=True)],assertion_no_other_effects=True)
        self.assertEqual(r['daily_total_pa'],'3')
    def test_deslocamento_ativo_nao_tabela(self):
        r=quote_effects([effect('DESLOCAMENTO_ATIVO',8)],assertion_no_other_effects=True)
        self.assertIsNone(r['daily_total_pa'])
    def test_bonus_teste_ataque(self):
        r=quote_effects([effect('BONUS_TESTE_ATAQUE',3,is_attack_test=True)],assertion_no_other_effects=True)
        self.assertEqual(r['daily_total_pa'],'3')
    def test_reflexo_nao_teste_ataque(self):
        r=quote_effects([effect('BONUS_TESTE_ATAQUE',3,is_attack_test=False)],assertion_no_other_effects=True)
        self.assertIsNone(r['daily_total_pa'])
    def test_ca_magica_exige_prova(self):
        self.assertIsNone(quote_effects([effect('CA_MAGICA',2)],assertion_no_other_effects=True)['daily_total_pa'])
        self.assertEqual(quote_effects([effect('CA_MAGICA',2,magical_origin_confirmed=True)],assertion_no_other_effects=True)['daily_total_pa'],'2')
    def test_ca_estrutural_nao_magica(self):
        self.assertIsNone(quote_effects([effect('CA_ESTRUTURAL',2)],assertion_no_other_effects=True)['daily_total_pa'])
    def test_rd_desconhecida_nao_zero(self):
        self.assertIsNone(quote_effects([effect('RD',20)],assertion_no_other_effects=True)['daily_total_pa'])
    def test_total_misto_indeterminado(self):
        a=effect('ATRIBUTO_PERMANENTE',5,permanent_confirmed=True)
        b=effect('CURA',3);b['id']='b'
        r=quote_effects([a,b],assertion_no_other_effects=True)
        self.assertEqual(r['identified_daily_subtotal_pa'],'25')
        self.assertIsNone(r['daily_total_pa'])
    def test_composicao_cinco_tarifas(self):
        arr=[effect('ATRIBUTO_PERMANENTE',1,permanent_confirmed=True),
             effect('DANO_FIXO_ADICIONAL',2,damage_is_fixed=True),
             effect('DESLOCAMENTO_PERMANENTE_M',3,permanent_confirmed=True),
             effect('BONUS_TESTE_ATAQUE',4,is_attack_test=True),
             effect('CA_MAGICA',5,magical_origin_confirmed=True)]
        for i,a in enumerate(arr):a['id']=str(i)
        self.assertEqual(quote_effects(arr,assertion_no_other_effects=True)['daily_total_pa'],'19')
    def test_nao_somar_sem_cobertura_escopo(self):
        r=quote_effects([effect('ATRIBUTO_PERMANENTE',5,permanent_confirmed=True)])
        self.assertEqual(r['identified_daily_subtotal_pa'],'25')
        self.assertIsNone(r['daily_total_pa'])
    def test_pa_ativacao_nao_deriva_da_diaria(self):
        a=effect('ATRIBUTO_PERMANENTE',5,permanent_confirmed=True,mode='ATIVO_POR_USO')
        r=quote_effects([a],assertion_no_other_effects=True)
        self.assertIsNone(r['activation_pa']);self.assertIsNone(r['daily_total_pa'])
    def test_invalid_numbers_and_duplicates(self):
        for v in (0,-1,True,'NaN','inf'):
            with self.assertRaises(ValueError):quote_effects([effect('ATRIBUTO_PERMANENTE',v)])
        with self.assertRaises(ValueError):quote_effects([effect('RD'),effect('RD')])
    def test_unknown_kind_refuses(self):
        with self.assertRaises(ValueError):quote_effects([effect('INVENTADO')])

if __name__=='__main__':unittest.main(verbosity=2)
