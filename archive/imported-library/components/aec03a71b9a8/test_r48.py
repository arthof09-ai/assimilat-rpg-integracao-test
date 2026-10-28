import io,sys,zipfile,json,csv,unittest,hashlib
from pathlib import Path
import audit_peer_r48 as a
import peer_receive_r48 as cli

def zip_modified(zbytes, changes=None, removed=(), extra=None):
    changes=changes or {};extra=extra or {}
    with zipfile.ZipFile(io.BytesIO(zbytes)) as z:
        pairs={n:z.read(n) for n in z.namelist() if n not in removed}
    pairs.update(changes);pairs.update(extra)
    output=io.BytesIO()
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for n,b in pairs.items():z.writestr(n,b)
    return output.getvalue()

class TestR48Audit(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
    cls.z=a.PEER.read_bytes();cls.cs=a.CSV.read_bytes();cls.rows,cls.r45,cls.prov=a.read_inputs();cls.data=a.score(cls.rows,cls.r45)
 def test_01_real_user_zip_verified(self):self.assertEqual(a.sha(self.z),a.EXPECTED_ZIP_SHA)
 def test_02_outer_manifest_verified(self):self.assertEqual(self.prov['outer_manifest_files'],8)
 def test_03_inner_manifest_verified(self):self.assertEqual(self.prov['inner_manifest_files'],14)
 def test_04_peer_freeze_12(self):self.assertEqual(len(self.rows),12)
 def test_05_unique_images(self):self.assertEqual(self.prov['images'],12)
 def test_06_r45_frozen_26(self):self.assertEqual(len(self.r45),26)
 def test_07_original_valid_submission_zip(self):
    ret=cli.audit(self.z,'original.zip')
    self.assertEqual(ret['status'],'FORM_COMPLETE_NOT_SCIENTIFICALLY_VALIDATED')
    self.assertEqual(ret['provenance']['original_images_verified'],12)
    self.assertTrue(ret['provenance']['peer_package_signatures_verified'])
 def test_08_valid_csv_supported(self):self.assertEqual(cli.audit(self.cs,'review.csv')['status'],'FORM_COMPLETE_NOT_SCIENTIFICALLY_VALIDATED')
 def test_09_reject_renamed_oracle(self):
    with self.assertRaises(cli.IntegrityError):cli.audit(zip_modified(self.z, extra={'gabarito_legacy.json':b'{}'}),'x.zip')
 def test_10_reject_tampered_original_inner(self):
    with self.assertRaises(cli.IntegrityError):cli.audit(zip_modified(self.z, changes={cli.ORIGINAL_NAME:b'hi'}),'x.zip')
 def test_11_reject_renamed_gabarito_impostor(self):
    with self.assertRaises(cli.IntegrityError):cli.audit(zip_modified(self.z,extra={'NAO_GABARITO.zip':b'X'}),'x.zip')
 def test_12_reject_manifest_mismatch(self):
    with self.assertRaises(cli.IntegrityError):cli.audit(zip_modified(self.z,changes={'QA_RESULTS.json':b'{}'}),'x.zip')
 def test_13_reject_freeze_mismatch(self):
    with zipfile.ZipFile(io.BytesIO(self.z)) as z:m=json.loads(z.read('MANIFEST_SHA256_OUTPUT.json'))
    frozen=json.loads(zipfile.ZipFile(io.BytesIO(self.z)).read('FREEZE_RECORD.json'))
    frozen['csv_sha256']='0'*64
    fbytes=json.dumps(frozen).encode()
    m['files']['FREEZE_RECORD.json']=a.sha(fbytes)
    with self.assertRaises(cli.IntegrityError):cli.audit(zip_modified(self.z,changes={'FREEZE_RECORD.json':fbytes,'MANIFEST_SHA256_OUTPUT.json':json.dumps(m).encode()}),'x.zip')
 def test_14_reject_second_csv(self):
    with self.assertRaises(cli.IntegrityError):cli.audit(zip_modified(self.z,extra={'another.csv':self.cs}),'x.zip')
 def test_15_reject_traversal(self):
    with self.assertRaises(cli.IntegrityError):cli.audit(zip_modified(self.z,extra={'../evil.txt':b'attack'}),'x.zip')
 def test_16_reject_duplicate_case_in_csv(self):
    rows=list(csv.DictReader(io.StringIO(self.cs.decode('utf-8-sig')))); rows[1]['case_id']=rows[0]['case_id'];o=io.StringIO();w=csv.DictWriter(o,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    with self.assertRaises(cli.IntegrityError):cli.audit(o.getvalue().encode(),'bad.csv')
 def test_17_reject_missing_case_csv(self):
    rows=list(csv.DictReader(io.StringIO(self.cs.decode('utf-8-sig'))))[:-1];o=io.StringIO();w=csv.DictWriter(o,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    with self.assertRaises(cli.IntegrityError):cli.audit(o.getvalue().encode(),'bad.csv')
 def test_18_contamination_not_silent(self):self.assertEqual([x['case_id'] for x in self.rows if x['proposed_RE']=='INSUFICIENTE'],['TEC-E3532F6A98AC'])
 def test_19_11_eligible(self):self.assertEqual(self.data['n_eligible'],11)
 def test_20_7_matches(self):self.assertEqual(self.data['matching'],7)
 def test_21_naive_equal_to_frozen(self):self.assertEqual(self.data['matching'],self.data['simple_prata_baseline_hits'])
 def test_22_peer_in_R45_bands(self):self.assertEqual(self.data['within_R45_band'],11)
 def test_23_naive_in_R45_bands(self):self.assertEqual(self.data['naive_Prata_within_R45_band'],11)
 def test_24_peer_e2_all_differ(self):self.assertEqual(self.data['peer_grade_E2_n'],self.data['peer_grade_E2_disagree_n'])
 def test_25_ordinal_distance_all_at_most_one(self):self.assertEqual(self.data['within_one_rank'],11)
 def test_26_no_canonical_claim(self):self.assertEqual(self.data['canonizations'],0);self.assertIsNone(self.data['predictive_accuracy'])
 def test_27_kappa_recomputed(self):self.assertAlmostEqual(self.data['cohen_nominal_kappa'],0.18518518518518517)
 def test_28_stable_naive_counts(self):self.assertEqual(self.data['rank_prevalence_peer']['Prata'],7)
 def test_29_sources_in_9_pages(self):
    unique=set()
    for x in self.rows:
       for k in ('system_comparator_url','live_comparator_url','family_comparator_url'):
        if x[k]:unique.add(x[k].split('/p/')[-1].split('?')[0])
    self.assertEqual(len(unique),9)
 def test_30_all_frozen_sha_manifest_pinned(self):
    self.assertEqual(a.sha(a.PEER.read_bytes()),a.EXPECTED_ZIP_SHA)

if __name__=='__main__':unittest.main(verbosity=2)
