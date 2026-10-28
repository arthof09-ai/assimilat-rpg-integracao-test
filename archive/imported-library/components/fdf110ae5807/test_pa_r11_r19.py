import copy,unittest,sys,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(HERE))
import pa_r11_adapter as m

R09=ROOT/'PA_P0_R09_CORRIGENDA_TEST_20261018.zip'
def fx(kind,amount,**x):return {'id':x.pop('id','a'),'kind':kind,'magnitude':amount,'mode':x.pop('mode','PASSIVO_DIARIO'),**x}
def spec(effects,closed=True,**x):return {'source_class':'USER_EXPERIMENTAL_SPEC','effects':effects,'all_effects_documented':closed,**x}

class PAExtensionTests(unittest.TestCase):
    def test_link_original_engine(self):self.assertEqual(m.pa_r05.ATTR_RATE,5)
    def test_original_r05_context(self):
        st,r=m.converse('Bota Caminho Veloz');self.assertEqual(r['historical_lookup_R05']['pa_daily']['value'],18);self.assertEqual(r['daily_total_pa'],'18');self.assertEqual(r['historical_activation_pa_values'],[5])
    def test_adaga_35_without_daily_unit(self):
        _,r=m.converse('Adaga da Serpente');self.assertIsNone(r['daily_total_pa'])
    def test_five_rates(self):
        a=[fx('ATRIBUTO_PERMANENTE',5,permanent_confirmed=True),fx('DANO_FIXO_ADICIONAL',20,damage_is_fixed=True,id='d'),fx('DESLOCAMENTO_PERMANENTE_M',3,permanent_confirmed=True,id='m'),fx('BONUS_TESTE_ATAQUE',3,is_attack_test=True,id='t'),fx('CA_MAGICA',2,magical_origin_confirmed=True,id='c')]
        r=m.estimate(spec(a));self.assertEqual(r['daily_total_pa'],'53');self.assertEqual(r['identified_daily_subtotal_pa'],'53')
    def test_scope_unknown_has_no_total(self):self.assertIsNone(m.estimate(spec([fx('ATRIBUTO_PERMANENTE',5,permanent_confirmed=True)],closed=False))['daily_total_pa'])
    def test_mixed_unknown(self):
        r=m.estimate(spec([fx('ATRIBUTO_PERMANENTE',5,permanent_confirmed=True),fx('RD',10,id='z')]))
        self.assertEqual(r['identified_daily_subtotal_pa'],'25');self.assertIsNone(r['daily_total_pa'])
    def test_structural_ca(self):self.assertIsNone(m.estimate(spec([fx('CA_ESTRUTURAL',2)]))['daily_total_pa'])
    def test_unproven_magical_ca(self):self.assertIsNone(m.estimate(spec([fx('CA_MAGICA',2)]))['daily_total_pa'])
    def test_attack_is_not_reflex(self):self.assertIsNone(m.estimate(spec([fx('BONUS_TESTE_ATAQUE',3,is_attack_test=False)]))['daily_total_pa'])
    def test_fixed_not_basic(self):self.assertIsNone(m.estimate(spec([fx('DANO_FIXO_ADICIONAL',20)]))['daily_total_pa'])
    def test_conditional_critical(self):self.assertIsNone(m.estimate(spec([fx('DANO_FIXO_ADICIONAL',20,damage_is_fixed=True,conditional=True)]))['daily_total_pa'])
    def test_active_attr_not_daily(self):self.assertIsNone(m.estimate(spec([fx('ATRIBUTO_PERMANENTE',5,mode='ATIVO_POR_USO',permanent_confirmed=True)]))['daily_total_pa'])
    def test_daily_historical_not_add(self):
        daily={'pa':18,'unit':'PA/dia','source_url':'https://app.notion.com/p/3edc2b324ede8135b199fd0cdbb5463c','source_literal':'18 PA por dia','evidence':'LITERAL_DOCUMENTED'}
        r=m.estimate(spec([fx('DESLOCAMENTO_PERMANENTE_M',3,permanent_confirmed=True)],historical_daily=daily))
        self.assertEqual(r['daily_total_pa'],'18');self.assertEqual(r['identified_daily_subtotal_pa'],'3')
    def test_historical_conflict(self):
        daily={'pa':10,'unit':'PA/dia','source_url':'notion','source_literal':'10 PA/dia','evidence':'LITERAL_DOCUMENTED'}
        r=m.estimate(spec([fx('ATRIBUTO_PERMANENTE',5,permanent_confirmed=True)],historical_daily=daily))
        self.assertIsNone(r['daily_total_pa']);self.assertTrue(r['historical_cost_conflict'])
    def test_historical_wrong_unit(self):
        with self.assertRaises(ValueError):m.estimate(spec([],historical_daily={'pa':10,'unit':'PA/turno','evidence':'LITERAL_DOCUMENTED','source_url':'n','source_literal':'10 PA'}))
    def test_activation_literal(self):
        r=m.estimate(spec([],activation_costs=[{'ability_id':'salto','pa':5,'unit':'PA/ativação','evidence':'LITERAL_DOCUMENTED','source_url':'https://app.notion.com/p/3edc2b324ede8135b199fd0cdbb5463c','source_literal':'5 PA para ativar'}]))
        self.assertEqual(r['activation_costs'][0]['per_use_pa'],'5');self.assertIsNone(r['activation_total_pa'])
    def test_activation_unknown_not_zero(self):self.assertIsNone(m.estimate(spec([fx('ATIVACAO',3,mode='ATIVO_POR_USO')]))['daily_total_pa'])
    def test_activation_forgery_denied(self):
        with self.assertRaises(ValueError):m.estimate(spec([],activation_costs=[{'ability_id':'s','pa':5,'unit':'PA/ativação','evidence':'INFERIDO','source_url':'u','source_literal':'x'}]))
    def test_notions_unsigned(self):self.assertFalse(m.craft_handoff(m.estimate(spec([])))['message']['notion_signed'])
    def test_craft_not_ack(self):self.assertIsNone(m.craft_handoff(m.estimate(spec([])))['recipient_ack'])
    def test_94_census(self):
        r=m.r09_census(R09);self.assertEqual((r['rows'],r['master'],r['mirror'],r['identified_at_least_one'],r['unidentified']),(94,14,80,32,62))
    def test_correction_gate(self):
        r=m.r09_census(R09)['candidates'];self.assertEqual(r[0]['proposed_daily_pa_test'],3);self.assertIsNone(r[1]['proposed_daily_pa_test']);self.assertIsNone(r[2]['proposed_daily_pa_test'])
    def test_quote_simple_attribute(self):self.assertEqual(m.converse('item isolado com +5 DES permanente')[1]['daily_total_pa'],'25')
    def test_quote_simple_fixed_damage(self):self.assertEqual(m.converse('somente +20 dano fixo adicional')[1]['daily_total_pa'],'20')
    def test_quote_movement(self):self.assertEqual(m.converse('apenas +3 metros permanente')[1]['daily_total_pa'],'3')
    def test_quote_attack(self):self.assertEqual(m.converse('apenas +3 em teste de ataque')[1]['daily_total_pa'],'3')
    def test_quote_ca_magic(self):self.assertEqual(m.converse('apenas +2 CA mágica comprovada')[1]['daily_total_pa'],'2')
    def test_quote_ca_uncertain(self):self.assertIsNone(m.converse('apenas +2 CA')[1]['daily_total_pa'])
    def test_quote_ca_structural(self):self.assertIsNone(m.converse('apenas +2 CA estrutural')[1]['daily_total_pa'])
    def test_quote_mixed_rd(self):self.assertIsNone(m.converse('+5 DES permanente e RD20')[1]['daily_total_pa'])
    def test_budget_new(self):
        r=m.budget(pa_total=100,committed_in_snapshot=20,already_includes_item_daily=False,quoted_item_daily=25,activations=[{'event_id':'1','pa':5}]);self.assertEqual(r['pa_free_after_scenario'],'50')
    def test_budget_committed_no_double(self):
        r=m.budget(pa_total=100,committed_in_snapshot=45,already_includes_item_daily=True,quoted_item_daily=25,activations=[{'event_id':'1','pa':5}]);self.assertEqual(r['pa_free_after_scenario'],'50')
    def test_budget_debited_activation_not_again(self):
        r=m.budget(pa_total=100,committed_in_snapshot=20,already_includes_item_daily=False,quoted_item_daily=25,activations=[{'event_id':'1','pa':5}],already_debited_activation_ids=('1',));self.assertEqual(r['pa_free_after_scenario'],'55')
    def test_budget_insufficient(self):
        r=m.budget(pa_total=15,committed_in_snapshot=10,already_includes_item_daily=False,quoted_item_daily=25);self.assertEqual(r['status'],'INSUFICIENTE_NO_CENARIO')
    def test_budget_unknown(self):self.assertIsNone(m.budget(pa_total=100,committed_in_snapshot=20,already_includes_item_daily=False,quoted_item_daily=None)['pa_free_after_scenario'])
    def test_budget_unknown_commitments(self):self.assertIsNone(m.budget(pa_total=100,committed_in_snapshot=20,already_includes_item_daily=False,quoted_item_daily=5,unknown_commitments=True)['pa_free_after_scenario'])
    def test_budget_bad_total(self):
        with self.assertRaises(ValueError):m.budget(pa_total=10,committed_in_snapshot=20,already_includes_item_daily=False,quoted_item_daily=5)
    def test_budget_duplicate_new_events(self):
        with self.assertRaises(ValueError):m.budget(pa_total=100,committed_in_snapshot=0,already_includes_item_daily=False,quoted_item_daily=5,activations=[{'event_id':'x','pa':2},{'event_id':'x','pa':2}])
    def test_no_false_zero(self):self.assertIsNone(m.estimate(spec([]))['daily_total_pa'])
    def test_invalid_source(self):
        with self.assertRaises(ValueError):m.estimate({'source_class':'CANONICO_VERIFICADO','effects':[]})
    def test_negative_quote(self):
        with self.assertRaises(ValueError):m.estimate(spec([fx('ATRIBUTO_PERMANENTE',-5)]))
    def test_no_recipes_ever(self):self.assertFalse(m.estimate(spec([]))['new_recipe_permitted'])

if __name__=='__main__':unittest.main(verbosity=2)
