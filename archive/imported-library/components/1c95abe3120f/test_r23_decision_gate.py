"""Small falsification/regression suite, focused on authority and the five decisions."""
import unittest, json, csv, zipfile, hashlib, re
from pathlib import Path
from fractions import Fraction
P=Path(__file__).resolve().parent
D=json.loads((P/'R23_DECISION_REGISTER.json').read_text())
M=json.loads((P/'R23_B01_B18_MATRIX.json').read_text())
B=json.loads((P/'R23_B15_EVENT_CONTRACT.json').read_text())
S=json.loads((P/'R23_SOURCE_PROVENANCE.json').read_text())
R=json.loads((P/'REGISTRO_LOCAL_R23.json').read_text())
R22='b95b51239ee3e74bf96599a7aa119c73ebb7667a2d434f5f61100a02d6a4d972'
def sha(b):return hashlib.sha256(b).hexdigest()
class ContractQA(unittest.TestCase):
 def test_parent_zip_sha(self):self.assertEqual(sha((P/'R22_ORIGINAL_READONLY.zip').read_bytes()),R22)
 def test_parent_crc(self):
  with zipfile.ZipFile(P/'R22_ORIGINAL_READONLY.zip') as z:self.assertIsNone(z.testzip())
 def test_no_approvals(self):self.assertEqual(D['approval_count'],0);self.assertIn('NOT_APPROVED',D['proposal_status'])
 def test_exactly_five_decisions(self):self.assertEqual(len(D['decisions']),5)
 def test_ids(self):self.assertEqual([d['id'] for d in D['decisions']],['DEC-B11-A','DEC-B11-B','DEC-B11-C','DEC-B12-A','DEC-B12-B'])
 def test_all_choices_open(self):
  for d in D['decisions']:
   self.assertIsNone(d['master_choice']);self.assertFalse(d['adopted']);self.assertEqual(d['approval_state'],'AWAITING_EXPLICIT_MASTER_DECISION')
 def test_three_distinct_options_each(self):
  for d in D['decisions']:
   opts=d['choices'];self.assertEqual(len(opts),3)
   self.assertEqual(len({o['option_id'] for o in opts}),3)
   self.assertIn(d['recommendation_option'],[o['option_id'] for o in opts])
 def test_nac_hold(self):self.assertEqual(M['nac_pass_terminal'],'HOLD');self.assertEqual(M['notion_writes'],0)
 def test_18_original_contracts(self):
  self.assertEqual(len(M['rows']),18)
  self.assertEqual({x['criterion'] for x in M['rows']},{'B%02d'%i for i in range(1,19)})
  self.assertTrue(all(x['predicado_original'] for x in M['rows']))
 def test_no_status_promotion(self):
  self.assertTrue(all(x['estado_R22']==x['estado_R23'] and not x['new_certification_R23'] for x in M['rows']))
 def test_only_pass_b02(self):self.assertEqual([x['criterion'] for x in M['rows'] if x['estado_R23']=='PASS_DOCUMENTAL'],['B02'])
 def test_9_6_2(self):
  from collections import Counter
  self.assertEqual(Counter(x['estado_R23'] for x in M['rows']),{'PASS_DOCUMENTAL':1,'PARTIAL':9,'BLOCKED':6,'NOT_TESTED':2})
 def test_strict_zero(self):self.assertEqual(M['strict_fights']['completed'],0);self.assertEqual(M['strict_fights']['required'],2)
 def test_csv_zero(self):self.assertEqual(M['i0003_original_csv'],{'authenticated':0,'expected':9})
 def test_only_b11_b12_decisioned(self):
  for r in M['rows']:
   self.assertEqual(len(r['R23_decision_ids']),3 if r['criterion']=='B11' else 2 if r['criterion']=='B12' else 0)
 def test_reapplication_existing_not_a_sixth_decision(self):
  self.assertEqual(len(D['decisions']),5)
  self.assertNotIn('DEC-B12-STACK',str(D))
  self.assertIn('não empilha', (P/'DOSSIER_DECISORIO_R23.md').read_text().lower())
 def test_lui_only_18(self):
  d=next(d for d in D['decisions'] if d['id']=='DEC-B11-B')
  self.assertIn('+18',d['original']);self.assertIn('+30',d['gap']+d['original'])
  self.assertIn('NÃO',d['worked'])
 def test_no_brutal_multiplier_implied(self):
  d=next(d for d in D['decisions'] if d['id']=='DEC-B11-A')
  self.assertIn('não tem operador',d['gap'])
 def test_crit_order_math(self):
  self.assertEqual(Fraction(2,6**3),Fraction(1,108))
  self.assertEqual(Fraction(1,108)**2,Fraction(1,11664))
  self.assertNotEqual((6,5,6),(6,6,5))
 def test_crit_roll_dme(self):self.assertEqual(Fraction(11,2)+15,Fraction(41,2));self.assertEqual(Fraction(11,2)+35,Fraction(81,2))
 def test_dot_mean(self):self.assertEqual(3*Fraction(13,2),Fraction(39,2));self.assertEqual(2*Fraction(39,2),39)
 def test_b15_expected(self):
  self.assertEqual(Fraction(9,2)+2*Fraction(7,2),Fraction(23,2))
  self.assertEqual(Fraction(9,2)+5*Fraction(7,2),Fraction(22))
 def test_b15_synthetic_excluded(self):
  self.assertEqual(B['real_events_recovered'],0);self.assertTrue(B['illustrative_only']['excluded_from_evidence']);self.assertEqual(B['status'],'PROSPECTIVE_PLAN_NOT_EXECUTED')
 def test_b15_example_rolls(self):
  t=B['illustrative_only'];self.assertEqual(t['physical_roll']+sum(t['fire_base_rolls']),t['pre_weakness_raw'])
  self.assertEqual(t['physical_roll']+sum(t['fire_base_rolls'])+sum(t['fire_bonus_rolls']),t['post_weakness_raw'])
 def test_b15_minimal_fields(self):
  required=['scene_id','event_id','source_epoch','actor_source_sha256','target_fire_weakness_source','rd_resistance_by_tag','target_hp_before','target_hp_after','independent_readback','nac_pass_verdict']
  self.assertTrue(set(required)<=set(B['minimal_event_fields']))
 def test_primary_provenance(self):
  self.assertGreaterEqual(len(S['sources']),10)
  self.assertTrue(all(x['url'].startswith('https://app.notion.com/p/') for x in S['sources'].values()))
 def test_ack_unproven(self):self.assertEqual(S['ibx_ack'],'NOT_PROVEN');self.assertEqual(M['ibx76_status'],'NOVA_NO_ACK')
 def test_reg_before_after(self):self.assertEqual(R['record_before'],R['record_after']);self.assertTrue(R['safety_hold'])
 def test_csv_matches_json(self):
  with (P/'R23_B01_B18_MATRIX.csv').open(encoding='utf8') as f:rows=list(csv.DictReader(f))
  self.assertEqual(len(rows),18)
  self.assertEqual([r['criterion'] for r in rows],[r['criterion'] for r in M['rows']])
 def test_all_dossier_ids(self):
  s=(P/'DOSSIER_DECISORIO_R23.md').read_text(encoding='utf8')
  for d in D['decisions']:self.assertGreater(s.count(d['id']),1)
 def test_master_blanks(self):
  s=(P/'FOLHA_DECISOES_MESTRE_R23.md').read_text(encoding='utf8');self.assertIn('________',s)
  self.assertNotIn('APROVADO',S['ibx_ack'])
 def test_no_notion_write(self):self.assertEqual(R['notion_writes'],0)
 def test_r13_byte_unchanged(self):
  with zipfile.ZipFile(P/'R22_ORIGINAL_READONLY.zip') as z:
   self.assertEqual((P/'r13_oracle.py').read_bytes(),z.read('DMG_R22_DECISIVE_EVIDENCE_SANDBOX/r13_oracle.py'))
if __name__=='__main__':unittest.main()
