from __future__ import annotations
import copy
import unittest
from ibx17_r41_item_provenance import *

CAJADO_URL='https://app.notion.com/p/9efc2b324ede8250a37981fb1fef45dd'
GRIM_URL='https://app.notion.com/p/ed0c2b324ede8335b533810ceb462896'
CAJADO='''<page><content>
<details>
<summary>Bônus:</summary>
+3d6 em magias do elemento sombra
+1d6 dano de fogo
+2 CD
ALCANCE - 15 m
+2d6+2 dano
CATEGORIA DE DANO AUMENTADA EM 1
</details>
> Gasto: 21 PA por dia
## Habilidade:
(Pass.) Força Sombria: Magia das sombras são amplificadas. +3d6 de dano
</content></page>'''
GRIM='''<page><content>
**Efeitos Base:**
- **Memória Arcanica (Passivo):** Concede +130 de PA para lançar magias e aumenta a CD do usuário em +15.
- **Intelecto astral (passivo):** Maximiza seu intelecto com magia e concede **+25 de inteligência** para o usuário.
- **Maldição do Aprendiz (Ativo – 1x/semana):** Ao copiar uma magia aumenta sua CD em +15 e adiciona 12d12 de dano, mas você sofre 15d12 de dano necrótico.
</content></page>'''
SHEET=f'<page><content>Equipamento: <mention-page url="{GRIM_URL}"/>\n### Destreza: 19+3+15=50</content></page>'

class Parser(unittest.TestCase):
    def test_01_content(self):self.assertIn('Efeitos Base',content_of_fetch(GRIM))
    def test_02_boundary_bad(self):
        with self.assertRaises(EvidenceHold):content_of_fetch('<content>abc')
    def test_03_mentions(self):self.assertEqual(len(parse_references(content_of_fetch(SHEET))),1)
    def test_04_title_page(self):
        a=parse_references(f'<page url="{CAJADO_URL}">Cajado</page>')[0]
        self.assertEqual((a.kind,a.title_literal),('page','Cajado'))
    def test_05_refs_duplicate_count(self):
        refs=parse_references(f'<mention-page url="{GRIM_URL}"/>\n<mention-page url="{GRIM_URL}"/>')
        self.assertEqual(unique_references(refs)[0]['lines'],[1,2])
    def test_06_no_ref_fake(self):self.assertEqual(parse_references('https://app.notion.com/p/123'),[])
    def test_07_grim_int(self):
        effects=extract_effects(GRIM,source_url=GRIM_URL)['effects']
        self.assertTrue(any(e['domain']=='INT' and e['value']=='+25' for e in effects))
    def test_08_grim_pa(self):
        effects=extract_effects(GRIM,source_url=GRIM_URL)['effects']
        self.assertTrue(any(e['domain']=='PA' and e['value']=='+130' for e in effects))
    def test_09_grim_cd(self):
        effects=extract_effects(GRIM,source_url=GRIM_URL)['effects']
        self.assertTrue(any(e['domain']=='CD' and e['value']=='+15' for e in effects))
    def test_10_cajado_dice(self):
        e=extract_effects(CAJADO,source_url=CAJADO_URL)['effects']
        self.assertTrue(any(z['value']=='+3d6' and z['mode']=='DICE_OR_FORMULA' for z in e))
    def test_11_cajado_cost(self):
        e=extract_effects(CAJADO,source_url=CAJADO_URL)['effects']
        self.assertTrue(any(z['value']=='21' and z['mode']=='COST' for z in e))
    def test_12_not_applied(self):
        e=extract_effects(GRIM,source_url=GRIM_URL)['effects']
        self.assertTrue(all(z['applied_to_total']=='NAO_COMPROVADO' for z in e))
    def test_13_unknown_status(self):
        with self.assertRaises(EvidenceHold):extract_effects(GRIM,source_url=GRIM_URL,status='INVENTADO')
    def test_14_item_bad_url(self):
        with self.assertRaises(EvidenceHold):extract_effects(GRIM,source_url='notion.so')
    def test_15_summary_no_new_page(self):
        i=extract_effects(GRIM,source_url=GRIM_URL)
        self.assertFalse(make_mention_summary('Grimório',i,item_ref=GRIM_URL)['new_item_page_created'])
    def test_16_summary_wrong_ref(self):
        i=extract_effects(GRIM,source_url=GRIM_URL)
        with self.assertRaises(EvidenceHold):make_mention_summary('Grimório',i,item_ref=CAJADO_URL)
    def test_17_no_auto_apply_unknown(self):
        i=extract_effects(GRIM,source_url=GRIM_URL)
        s=make_mention_summary('Grimório',i,item_ref=GRIM_URL)
        with self.assertRaisesRegex(EvidenceHold,'UNKNOWN_EQUIP'):
            reconcile_numeric(80,55,[s],'INT')
    def test_18_reconcile_known(self):
        i=extract_effects(GRIM,source_url=GRIM_URL,status='ATIVO_COMPROVADO')
        s=make_mention_summary('Grimório',i,item_ref=GRIM_URL,applicability='INCLUIDO_COMPROVADO')
        v=reconcile_numeric(80,55,[s],'INT');self.assertTrue(v['consistent']);self.assertEqual(v['bonus'],25)
    def test_19_reconcile_wrong(self):
        i=extract_effects(GRIM,source_url=GRIM_URL,status='ATIVO_COMPROVADO')
        s=make_mention_summary('Grimório',i,item_ref=GRIM_URL,applicability='INCLUIDO_COMPROVADO')
        self.assertEqual(reconcile_numeric(90,55,[s],'INT')['status'],'CONFLICT')
    def test_20_unknown_natural_hold(self):self.assertEqual(reconcile_numeric(80,None,[],'INT')['status'],'HOLD_NATURAL_UNKNOWN')
    def test_21_double_count_blocked(self):
        i=extract_effects(GRIM,source_url=GRIM_URL,status='ATIVO_COMPROVADO')
        s=make_mention_summary('Grimório',i,item_ref=GRIM_URL,applicability='INCLUIDO_COMPROVADO')
        with self.assertRaisesRegex(EvidenceHold,'DUPLICATED_ITEM'):
            reconcile_numeric(105,55,[s,s],'INT')
    def test_22_inactive_not_added(self):
        i=extract_effects(GRIM,source_url=GRIM_URL,status='ARMAZENADO')
        s=make_mention_summary('Grimório',i,item_ref=GRIM_URL,applicability='NAO_INCLUIDO')
        self.assertEqual(reconcile_numeric(55,55,[s],'INT')['bonus'],0)
    def test_23_incidence_hold(self):
        i=extract_effects(GRIM,source_url=GRIM_URL,status='ATIVO_COMPROVADO')
        s=make_mention_summary('Grimório',i,item_ref=GRIM_URL,applicability='PENDENTE')
        with self.assertRaisesRegex(EvidenceHold,'BONUS_INCIDENCE'):
            reconcile_numeric(80,55,[s],'INT')
    def test_24_calc_mismatch(self):self.assertEqual(arithmetic_mismatches(content_of_fetch(SHEET))[0]['computed'],37)
    def test_25_no_false_mismatch(self):self.assertEqual(arithmetic_mismatches('15+5=20'),[])
    def test_26_snapshot_freeze(self):
        i=extract_effects(GRIM,source_url=GRIM_URL)
        s=make_mention_summary('Grimório',i,item_ref=GRIM_URL)
        f=freeze_archive_snapshot('a'*32,content_of_fetch(SHEET),[s],original_reference_ids=[i['item_id']])
        self.assertFalse(f['native_write']);self.assertEqual(f['summaries'][0]['item_label'],'Grimório')
    def test_27_no_child_cloning(self):
        with self.assertRaisesRegex(EvidenceHold,'CHILD_PAGES'):
            freeze_archive_snapshot('a'*32,f'<page url="{GRIM_URL}">Item</page>',[],original_reference_ids=[])
    def test_28_snapshot_missing_mention(self):
        with self.assertRaises(EvidenceHold):freeze_archive_snapshot('a'*32,'no mentions',[],original_reference_ids=['f'*32])
    def test_29_snapshot_unknown_item(self):
        i=extract_effects(GRIM,source_url=GRIM_URL)
        s=make_mention_summary('Grimório',i,item_ref=GRIM_URL)
        with self.assertRaisesRegex(EvidenceHold,'SUMMARY_WITHOUT_MENTION'):
            freeze_archive_snapshot('a'*32,'no mentions',[s],original_reference_ids=[])
    def test_30_immutable_excerpt(self):
        i=extract_effects(GRIM,source_url=GRIM_URL)
        s=make_mention_summary('Grimório',i,item_ref=GRIM_URL)
        p1=freeze_archive_snapshot('a'*32,content_of_fetch(SHEET),[s],original_reference_ids=[i['item_id']])
        ix=copy.deepcopy(i);ix['effects'][0]['literal']='upgraded'
        s2=make_mention_summary('Grimório',ix,item_ref=GRIM_URL)
        p2=freeze_archive_snapshot('a'*32,content_of_fetch(SHEET),[s2],original_reference_ids=[i['item_id']])
        self.assertNotEqual(p1['immutable_extratos_sha256'],p2['immutable_extratos_sha256'])
        self.assertEqual(p1['summaries'][0]['bonus_objetivos'],s['bonus_objetivos'])
    def test_31_refusal(self):self.assertEqual(request_gate(surface='MESTRE',approved=False,synthetic=True,source_stable=True,history_preserved=True),'NO_WRITE_REFUSAL')
    def test_32_test_approval(self):self.assertEqual(request_gate(surface='MESTRE',approved=True,synthetic=True,source_stable=True,history_preserved=True),'TEST_MUTATION_ELIGIBLE_ONLY')
    def test_33_party_hold(self):self.assertTrue(request_gate(surface='PARTY',approved=True,synthetic=True,source_stable=True,history_preserved=True).startswith('HOLD_'))
    def test_34_official_hold(self):self.assertTrue(request_gate(surface='MESTRE',approved=True,synthetic=False,source_stable=True,history_preserved=True).startswith('HOLD_'))
    def test_35_drift_hold(self):self.assertEqual(request_gate(surface='MESTRE',approved=True,synthetic=True,source_stable=False,history_preserved=True),'HOLD_SOURCE_DRIFT')
    def test_36_history_hold(self):self.assertEqual(request_gate(surface='MESTRE',approved=True,synthetic=True,source_stable=True,history_preserved=False),'HOLD_HISTORY_INTEGRITY')

if __name__=='__main__':unittest.main()
