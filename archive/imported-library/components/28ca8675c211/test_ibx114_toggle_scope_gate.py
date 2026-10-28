"""New TEST-only second-alternante and conflict regression, no Notion writes."""
import unittest
from ibx114_toggle_scope_gate import AnchoredChange,preflight_toggle_scoped
from ibx114_writer_v2_scope import LAB_TEST_CLONE,signature,ScopedWriteHold,verify_host_after,reconcile_partial

KIDS=''.join('<page url="https://app.notion.com/p/'+format(i+1,'032x')+'">k</page>' for i in range(20))
BODY='HEADER'+KIDS+''.join('<toggle>staged_'+str(i)+'</toggle>' for i in range(101))+'<toggle>SKILL_SCOPE_A / Acrobacia 4d6+10</toggle><toggle>SKILL_SCOPE_B / Fortitude 4d6+20</toggle>'
A=AnchoredChange('acrobacia','SKILL_SCOPE_A','Acrobacia 4d6+10','Acrobacia 4d6+11')
B=AnchoredChange('fortitude','SKILL_SCOPE_B','Fortitude 4d6+20','Fortitude 4d6+21')
V='TEST_VERSION'  # mocked version, never a real host version

def plan(body=BODY,changes=None,require_distinct_toggles=True,**extras):
    kw=dict(page_id=LAB_TEST_CLONE,version=V,expected_version=V,body=body,
            changes=[A,B] if changes is None else changes,lab_parent_verified=True,
            expected_sha256=signature(body)['sha256'],
            require_distinct_toggles=require_distinct_toggles)
    kw.update(extras)
    return preflight_toggle_scoped(**kw)

class ToggleScopeLabTests(unittest.TestCase):
    def test_two_distinct_toggles(self):
        p=plan();self.assertEqual(len(set(p.toggle_indices)),2)
        self.assertEqual(p.preview.gate,'LAB_TEST_PREPARED_NO_COMMIT')
    def test_full_expected_after_exact(self):
        p=plan().preview;result=verify_host_after(p,p.expected_after,after_version='MOCK_NEXT')
        self.assertEqual(result['status'],'PASS_TEST_NOTION_TARGET_ONLY')
        self.assertFalse(result['atomic_CAS_proven'])
    def test_wrong_anchor_hold(self):
        with self.assertRaisesRegex(ScopedWriteHold,'ANCHOR_IN_DIFFERENT_TOGGLE'):
            plan(changes=[AnchoredChange('a','SKILL_SCOPE_B',A.old,A.new)])
    def test_duplicate_anchor_hold(self):
        with self.assertRaisesRegex(ScopedWriteHold,'TOGGLE_ANCHOR_NOT_UNIQUE'):
            plan(changes=[AnchoredChange('a','4d6',A.old,A.new)])
    def test_scope_two_fields_same_toggle_denied(self):
        with self.assertRaisesRegex(ScopedWriteHold,'MULTIPLE_FIELDS_IN_SAME_TOGGLE'):
            plan(changes=[A,AnchoredChange('other','SKILL_SCOPE_A /','4d6+10','4d6+12')])
    def test_wrong_version_denied(self):
        with self.assertRaises(ScopedWriteHold):plan(expected_version='STALE')
    def test_wrong_hash_denied(self):
        with self.assertRaises(ScopedWriteHold):plan(expected_sha256='0'*64)
    def test_missing_second_target_denied(self):
        with self.assertRaises(ScopedWriteHold):
            plan(changes=[A,AnchoredChange('missing','SKILL_SCOPE_B','ABSENT_TARGET','new')])
    def test_no_second_toggle_denied(self):
        with self.assertRaisesRegex(ScopedWriteHold,'TARGET_NOT_INSIDE_TOGGLE'):
            plan(changes=[AnchoredChange('header','SKILL_SCOPE_A','HEADER','HEADER2')])
    def test_wrong_parent_denied(self):
        with self.assertRaises(ScopedWriteHold):plan(lab_parent_verified=False)
    def test_unbalanced_toggle_denied(self):
        with self.assertRaisesRegex(ScopedWriteHold,'UNBALANCED_TOGGLE_CLOSER'):
            plan(body=BODY+'</toggle>')
    def test_partial_reply_detection(self):
        p=plan().preview;partial=BODY.replace(A.old,A.new)
        self.assertEqual(verify_host_after(p,partial,after_version='MOCK_NEXT')['status'],'FAIL_OR_HOLD')
        d=reconcile_partial(BODY,partial,list(p.changes))
        self.assertEqual(d['status'],'PARTIAL_APPLY_DETECTED')
        self.assertFalse(d['host_rollback_executed'])
    def test_nested_anchored_scope(self):
        body=BODY.replace('<toggle>SKILL_SCOPE_A / Acrobacia 4d6+10</toggle>',
         '<toggle>OUTER<toggle>SKILL_SCOPE_A / Acrobacia 4d6+10</toggle></toggle>')
        # 104 toggles, not the known 103 -> hard hold before host.
        with self.assertRaisesRegex(ScopedWriteHold,'STRUCTURAL_SIGNATURE_NOT_TESTED'):
            plan(body=body)
    def test_drift_to_escaped_serializer_denied(self):
        with self.assertRaises(ScopedWriteHold):plan(body=BODY+r'\</details\>')

if __name__=='__main__':unittest.main()
