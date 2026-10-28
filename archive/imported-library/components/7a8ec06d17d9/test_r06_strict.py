import unittest
from r06_contracts import R06Hold,native_duplicate_strict
from test_r06 import envelope, FILE, BLOCK0, BLOCK1, CHILD0, CHILD1


class StrictNotionRegression(unittest.TestCase):
    def test_known_children_only(self):
        a=f'<page url="https://app.notion.com/p/{CHILD0}" color="red">Ficha aninhada</page>'
        b=f'<page url="https://app.notion.com/p/{CHILD1}" color="red">Ficha aninhada</page>'
        self.assertEqual(native_duplicate_strict(envelope(a),envelope(b))['state'],'STRICT_SEMANTIC_PARITY')

    def test_unverified_unrelated_mention_hold(self):
        a=f'<page url="https://app.notion.com/p/{CHILD0}">Ficha</page><mention-page url="https://app.notion.com/p/{"1"*32}"/>'
        b=f'<page url="https://app.notion.com/p/{CHILD1}">Ficha</page><mention-page url="https://app.notion.com/p/{"2"*32}"/>'
        self.assertEqual(native_duplicate_strict(envelope(a),envelope(b))['state'],'UNVERIFIED_REMAP_HOLD')
        p=native_duplicate_strict(envelope(a),envelope(b),verified_extra_remaps={'1'*32:'2'*32})
        self.assertEqual(p['state'],'STRICT_SEMANTIC_PARITY')
        self.assertEqual(p['witnessed_extra_mappings'],1)

    def test_media_remap(self):
        a='![](notion-file-block://'+BLOCK0+'/'+FILE+'?name=f.jpg)'
        b='![](notion-file-block://'+BLOCK1+'/'+FILE+'?name=f.jpg)'
        self.assertEqual(native_duplicate_strict(envelope(a),envelope(b))['remapped_media_blocks'],1)

    def test_reuse_same_image_block_id_fails(self):
        a='![](notion-file-block://'+BLOCK0+'/'+FILE+'?name=f.jpg)'
        with self.assertRaises(R06Hold):native_duplicate_strict(envelope(a),envelope(a))

    def test_changing_image_file_is_not_proven(self):
        a='![](notion-file-block://'+BLOCK0+'/'+FILE+'?name=f.jpg)'
        b='![](notion-file-block://'+BLOCK1+'/'+('2'*36)+'?name=f.jpg)'
        with self.assertRaises(R06Hold):native_duplicate_strict(envelope(a),envelope(b))

    def test_label_divergence_rejected(self):
        a=f'<page url="https://app.notion.com/p/{CHILD0}">Title</page>'
        b=f'<page url="https://app.notion.com/p/{CHILD1}">Other</page>'
        with self.assertRaises(R06Hold):native_duplicate_strict(envelope(a),envelope(b))

    def test_orphaned_old_native_asset_rejected(self):
        a='![](notion-file-block://'+BLOCK0+'/'+FILE+'?name=f.jpg)'
        b=a+' text'
        with self.assertRaises(R06Hold):native_duplicate_strict(envelope(a),envelope(b))

    def test_unknown_effect_present_stays_hold(self):
        from r06_contracts import EventJournal,sha
        j=EventJournal('actor','event',{'x'*36:sha('source')})
        j.prepare();j.report_unknown('timeout');j.reconcile(observed='PRESENT',proof='full source readback')
        self.assertEqual(j.state,'RECONCILED_PRESENT_HOLD')
        with self.assertRaises(R06Hold):j.witnessed_save('x'*36,sha('source'))

if __name__=='__main__':unittest.main()
