import unittest, csv, json
from pathlib import Path
from pa_r21_habilidades import fee, quote_item_r21, activation_summary

ROOT=Path(__file__).resolve().parent
RANKS=['Bronze','Prata','Ouro','Ouro Negro','Lendário']
FEES={'Bronze':5,'Prata':11,'Ouro':16,'Ouro Negro':35,'Lendário':91} # FIXTURE SINTÉTICA, NÃO é tabela oficial

def item(abilities,rank='Ouro',**kw):
 return quote_item_r21(item_rank=rank,abilities=abilities,passive_fees=FEES,**kw)

class TestHabilidades(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  with open(ROOT/'ATIVACOES_HISTORICAS_R21.csv',encoding='utf-8-sig',newline='') as f:cls.rows=list(csv.DictReader(f))
  cls.summary=json.loads((ROOT/'SINTese_ATIVACOES_R21.json').read_text(encoding='utf8'))
 def test_decision_floor_half_odd(self):self.assertEqual(fee('Prata','ATIVA',FEES),5)
 def test_decision_floor_half_legend(self):self.assertEqual(fee('Lendário','ATIVA',FEES),45)
 def test_fee_passive(self):self.assertEqual(fee('Ouro','PASSIVA',FEES),16)
 def test_missing_tariff_is_unknown(self):self.assertIsNone(fee('Ouro','PASSIVA',{}))
 def test_bad_fee_negative(self):
  with self.assertRaises(ValueError):fee('Ouro','PASSIVA',{'Ouro':-1})
 def test_bad_fee_fractional(self):
  with self.assertRaises(ValueError):fee('Ouro','PASSIVA',{'Ouro':2.5})
 def test_bad_fee_nan(self):
  with self.assertRaises(ValueError):fee('Ouro','PASSIVA',{'Ouro':'NaN'})
 def test_bad_fee_bool(self):
  with self.assertRaises(ValueError):fee('Ouro','PASSIVA',{'Ouro':True})
 def test_rank_unknown(self):
  with self.assertRaises(ValueError):fee('Bronze 5','PASSIVA',FEES)
 def test_mode_unknown(self):
  with self.assertRaises(ValueError):fee('Bronze','ATIVACAO',FEES)
 def test_no_abilities_gold_floor(self):self.assertEqual(item([])['daily_total_pa_day'],21)
 def test_active_only_gold_still_floor(self):
  x=item([{'id':'A','rank':'Ouro','mode':'ATIVA','activation_cost':14,'uses_today':1}]);self.assertEqual((x['daily_total_pa_day'],x['total_today_pa']), (21,35))
 def test_passive_and_active_gold_add(self):
  x=item([{'id':'P','rank':'Ouro','mode':'PASSIVA'},{'id':'A','rank':'Ouro','mode':'ATIVA','activation_cost':6,'uses_today':2}],attributes=3)
  self.assertEqual((x['base_ability_fees_known_total_pa_day'],x['daily_total_pa_day'],x['activation_total_today_pa'],x['total_today_pa']),(24,39,12,51))
 def test_bronze_active_two_above_floor(self):
  x=item([{'id':'A','rank':'Bronze','mode':'ATIVA','activation_cost':5,'uses_today':0}, {'id':'B','rank':'Bronze','mode':'ATIVA','activation_cost':6,'uses_today':0}],rank='Bronze')
  self.assertEqual(x['daily_total_pa_day'],8) # cada ativa floor(5/2)=2, soma 4, piso 8
 def test_o_nonretroactive(self):self.assertFalse(item([])['historical_repricing'])
 def test_missing_ability_fee_unknown_daily(self):
  x=quote_item_r21(item_rank='Bronze',abilities=[{'id':'X','rank':'Bronze','mode':'PASSIVA'}],passive_fees={})
  self.assertEqual(x['daily_lower_bound_pa'],8);self.assertIsNone(x['daily_total_pa_day'])
  self.assertEqual(x['pending_daily_ability_ids'],['X'])
 def test_cost_activation_unknown_when_used(self):
  x=item([{'id':'A','rank':'Ouro','mode':'ATIVA','uses_today':1}]);self.assertIsNone(x['activation_total_today_pa']);self.assertIsNone(x['total_today_pa'])
 def test_activation_no_uses_unknown_unit(self):
  x=item([{'id':'A','rank':'Ouro','mode':'ATIVA','uses_today':0}]);self.assertEqual(x['activation_total_today_pa'],0);self.assertIn('A',x['pending_activation_tariff_ids'])
 def test_effects_unpriced_unknown_daily(self):
  x=item([],effects_complete=False);self.assertIsNone(x['daily_total_pa_day']);self.assertEqual(x['daily_lower_bound_pa'],21)
 def test_rank_item_vs_rank_ability(self):
  with self.assertRaises(ValueError):item([{'id':'A','rank':'Ouro Negro','mode':'ATIVA'}])
 def test_mismatch_rank_can_flag(self):
  x=item([{'id':'A','rank':'Ouro Negro','mode':'ATIVA','activation_cost':10}],strict_rank_gate=False)
  self.assertTrue(x['warnings']);self.assertEqual(x['daily_total_pa_day'],21) # known fee 17, piso21
 def test_bad_event_dup_across_abilities(self):
  with self.assertRaises(ValueError):item([{'id':'A','rank':'Ouro','mode':'ATIVA','activation_cost':6,'uses_today':1,'activation_ids':['evt1']},{'id':'B','rank':'Ouro','mode':'ATIVA','activation_cost':6,'uses_today':1,'activation_ids':['evt1']}])
 def test_good_event_idempotent(self):
  x=item([{'id':'A','rank':'Ouro','mode':'ATIVA','activation_cost':6,'uses_today':2,'activation_ids':['evt1','evt2']}]);self.assertEqual(x['activation_total_today_pa'],12)
 def test_bad_event_len(self):
  with self.assertRaises(ValueError):item([{'id':'A','rank':'Ouro','mode':'ATIVA','activation_cost':6,'uses_today':2,'activation_ids':['evt1']}])
 def test_duplicate_ability_id(self):
  with self.assertRaises(ValueError):item([{'id':'A','rank':'Ouro','mode':'PASSIVA'},{'id':'A','rank':'Ouro','mode':'PASSIVA'}])
 def test_passive_cannot_activate(self):
  with self.assertRaises(ValueError):item([{'id':'A','rank':'Ouro','mode':'PASSIVA','activation_cost':6}])
 def test_negative_active_cost(self):
  with self.assertRaises(ValueError):item([{'id':'A','rank':'Ouro','mode':'ATIVA','activation_cost':-6}])
 def test_uses_must_integer(self):
  with self.assertRaises(ValueError):item([{'id':'A','rank':'Ouro','mode':'ATIVA','activation_cost':6,'uses_today':1.5}])
 def test_zero_fee_even_rank(self):self.assertEqual(fee('Bronze','ATIVA',{'Bronze':0}),0)
 def test_unequal_ranks_price_independently(self):
  x=item([{'id':'A','rank':'Bronze','mode':'PASSIVA'},{'id':'B','rank':'Ouro','mode':'ATIVA','activation_cost':7}]);self.assertEqual(x['base_ability_fees_known_total_pa_day'],13)
 def test_summary_sixteen(self):self.assertEqual(len(self.rows),16)
 def test_unique_thirteen_items(self):self.assertEqual(len(set(r['item_uuid'] for r in self.rows)),13)
 def test_all_source_urls(self):self.assertTrue(all(r['source_link'].startswith('https://app.notion.com/p/') for r in self.rows))
 def test_source_ranks_doc_two(self):self.assertEqual(sum(r['item_rank_status']=='E0_DOCUMENTAL' for r in self.rows),2)
 def test_summary_value(self):
  s=activation_summary(self.rows)
  self.assertEqual((s['abilities'],s['distinct_items'],s['min_pa'],s['max_pa'],s['mean_pa'],s['median_pa'],s['most_frequent_6pa_count']),(16,13,4,60,11.8125,6.5,6))
 def test_without_sixty(self):
  s=activation_summary(self.rows)['without_60'];self.assertEqual((s['n'],s['mean_pa'],s['median_pa']),(15,8.6,6))
 def test_no_automatic_e0_ability(self):self.assertTrue(all(r['ability_rank_evidence']!='E0' for r in self.rows))
 def test_does_not_conflate_item_and_ability_rank(self):self.assertEqual(len([r for r in self.rows if r['item_rank_E0'] and r['ability_rank_preliminary_band']]),2)
 def test_no_fabricated_generic_activation_tariff(self):self.assertNotIn('activation_by_rank_official',self.summary)
 def test_output_is_dict(self):self.assertIsInstance(item([]),dict)
 def test_failed_dup_dataset(self):
  with self.assertRaises(ValueError):activation_summary(self.rows+self.rows[:1])
if __name__=='__main__':unittest.main(verbosity=2)
