import unittest,sys
sys.path.insert(0,'/mnt/data/levelup_r207_r216/previous')
from r198_dynamic_source import parse_notion,SourceHold
from r199_r200_live_mobile import MobileSession,GateHold
P='3ffc2b324ede81d383e4df1d5a4633ed'
V='2026-10-20T10:45:46.234Z'
PARENT='https://app.notion.com/p/3fbc2b324ede804a95fafcb7b293c92c'
BODY='''<callout icon="🧪" color="yellow_bg">
**IBX17-R213-ACTIVE-FACE-VALIDATED — PERSONAGEM SINTÉTICO DO LABORATÓRIO**
</callout>
## R213 — FICHA TÉCNICA ATIVA / READBACK DE PREPARAÇÃO TEST
**Identidade experimental:** HOLDOUT-R213-HUMANO-L17-TEST
**Classificação:** Ouro Negro 2 — nível 17
**Raça:** Humano (SINTÉTICA)
**Atributos:** Naturais, sem equipamento de atributo nem títulos
<table header-row="true">
<tr><td>Atributo</td><td>Natural TEST</td><td>Efetivo TEST</td><td>Origem</td></tr>
<tr><td>FOR</td><td>13</td><td>13</td><td>trilha sintética R213</td></tr>
<tr><td>DES</td><td>11</td><td>11</td><td>trilha sintética R213</td></tr>
<tr><td>CON</td><td>10</td><td>10</td><td>trilha sintética R213</td></tr>
<tr><td>INT</td><td>13</td><td>13</td><td>trilha sintética R213</td></tr>
<tr><td>SAB</td><td>6</td><td>6</td><td>trilha sintética R213</td></tr>
<tr><td>CAR</td><td>6</td><td>6</td><td>trilha sintética R213</td></tr>
</table>
**Orçamento natural TEST:** 59/59 (25 iniciais+17×2).
**Vida TEST:** atual 180 / máxima 311 = natural 304 + lock FF300 Vida 7.
**Alma TEST:** atual 200 / máxima 354; PA comprometido 20; PA livre 334.
**Força Física TEST:** 340 = 10×(FOR13+DES11+CON10)
**Classe de Armadura TEST:** 20 = Humano 6 + DES11 + armadura sintética CA2 + FF100 CA1.
**CD de Magia TEST:** 15 = INT13 + proficiência TEST2.
---
<details><summary>Legacy archived R55</summary>FOR9999 DES9999 NOT ACTIVE</details>
<page url="https://app.notion.com/p/be0c2b324ede82bdab85818b32fb1377">TEST child</page>
'''

def get(body=BODY,page=P,ver=V):return parse_notion(page_id=page,version=ver,native_parent_url=PARENT,body=body,expect_id=P)

class AdapterR213(unittest.TestCase):
 def test_fetch_adapter_state(self):
  s=get();self.assertEqual(s.layout,'R213_COMPLEX_HOLDOUT_ACTIVE_TABLE');self.assertEqual(s.normal['level'],17);self.assertEqual(s.normal['hp_max'],311);self.assertEqual(s.normal['pa_max'],354);self.assertEqual(sum(s.normal['natural_attrs'].values()),59)
 def test_preview_mobile_reuses_existing_engine(self):
  s=get();m=MobileSession(s,'IBX17-R214-HOLDOUT-L18-FUTURE-TEST',1)
  q=m.request_choices();self.assertEqual(q['points_per_level'],2)
  v=m.revise([{'FOR':0,'DES':0,'CON':0,'INT':0,'SAB':2,'CAR':0}]);self.assertEqual(v['after']['hp_max'],328);self.assertEqual(v['after']['pa_max'],374);self.assertEqual(v['after']['ff'],340);self.assertEqual(v['holds'],[]);self.assertEqual(v['writes'],0)
 def test_no_write_without_host_confirm(self):
  s=get();m=MobileSession(s,'IBX17-R214-HOLDOUT-L18-FUTURE-TEST',1);v=m.revise([{'FOR':0,'DES':0,'CON':0,'INT':0,'SAB':2,'CAR':0}]);
  with self.assertRaises(GateHold):m.revalidate_for_write(s,v['preview_hash'],approval=None)
 def test_reject_drift(self):
  s=get();m=MobileSession(s,'IBX17-R214-HOLDOUT-L18-FUTURE-TEST',1);v=m.revise([{'FOR':0,'DES':0,'CON':0,'INT':0,'SAB':2,'CAR':0}]);
  with self.assertRaises(GateHold):m.revalidate_for_write(get(body=BODY+'X'),v['preview_hash'],approval='FAKE')
 def test_reject_budget(self):
  s=get();m=MobileSession(s,'IBX17-R214-HOLDOUT-L18-FUTURE-TEST',1)
  with self.assertRaises(GateHold):m.revise([{'FOR':0,'DES':0,'CON':0,'INT':0,'SAB':5,'CAR':0}])
 def test_reject_writable_party_parent(self):
  with self.assertRaises(SourceHold):parse_notion(page_id=P,version=V,native_parent_url='https://app.notion.com/p/bc49c16dd495824ea26f0186c4101d48',body=BODY,expect_id=P)
 def test_no_archive_activation(self):
  s=get();self.assertEqual(s.normal['natural_attrs']['FOR'],13)
 def test_reject_tamper(self):
  with self.assertRaises(SourceHold):get(body=BODY.replace('59/59','53/53'))
 def test_reject_repeated_active(self):
  with self.assertRaises(SourceHold):get(body=BODY+'\n## R213 — FICHA TÉCNICA ATIVA / READBACK DE PREPARAÇÃO TEST')

if __name__=='__main__':unittest.main(verbosity=2)
