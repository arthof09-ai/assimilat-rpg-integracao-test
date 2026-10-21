"""Execute original Orc P13 view tests and independently diff original P12 source.

Frozen TEST representation, not host writer, VLAB approval, Notion page QA or canon.
"""
from __future__ import annotations
import argparse
import base64
import copy
import hashlib
import json
import lzma
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

P13_VIEW_SHA = 'd0de11a7e78766d738ce9a07a11f018352bed64acc83f7e9d561fb7e0b385549'
P13_SCRIPT_SHA = 'ec7a993aee44a5ad58889a1aba76873d4e3889df87add3b0ab38c3b21f4635f7'
P13_ZIP_PROVENANCE_SHA = '76ca794ffe4845ab967dd38b5936bfdd30e0300d22c1ceca7b0b1386e184dfe7'
P12_JSON_NAME = ('orc25_r216p12_MASTER_CORRECTED/'
 'ORC_R216P12_25_NIVEIS_20_TRANSFORMACOES_MASTER_CORRIGIDOS.json')
P12_JSON_SHA = 'a54467e7786855f05289149ea8f978a3b0a30591549f46f6ab8cdabcc355a7a8'
P13_EXTRA_TOP = {
 'P13_Notion_combat_scope','P13_base_source_sha256',
 'P13_field_attack_dice_separated','P13_levelup_writer_status','P13_mutation_scope'
}
P13_EXTRA_ATTACK = {
 'TEST_RIDER_REQUIRES_PA_AND_VALID_HIT',
 'attack_test_separate_not_damage_TEST',
 'confirmed_weapon_damage_base_by_VLAB_TEST',
 'damage_components_NOT_auto_applied',
 'physical_attack_expression_original_P12_RETAINED_HISTORY'
}

def sha(data):return hashlib.sha256(data).hexdigest()

def original_comparison(p12,p13):
    assert set(p13)-set(p12)==P13_EXTRA_TOP, 'P13_TOP_METADATA_SCOPE_CHANGED'
    assert not(set(p12)-set(p13)), 'P13_DROPPED_P12_TOP_FIELD'
    assert p13['P13_base_source_sha256']==P12_JSON_SHA
    assert p13['P13_field_attack_dice_separated'] is True
    assert p13['schema'].startswith('IBX114-R216P13-READONLY-REPRESENTATION')
    assert p13['world_canon'] is False and p13['VLAB_accepted'] is False
    assert p13['Party_writes']==0
    a=copy.deepcopy(p13)
    for key in P13_EXTRA_TOP: a.pop(key)
    a['schema']=p12['schema']
    assert len(a['profiles'])==25 and len(p12['profiles'])==25
    for n,(legacy,current) in enumerate(zip(p12['profiles'],a['profiles']),1):
        assert legacy['ordinal']==current['ordinal']==n, 'P13_ORDER_CHANGED'
        assert legacy['rank']==current['rank'],'P13_RANK_CHANGED'
        before=legacy['FULL']['combat_attack_dme_preview_TEST']
        now=current['FULL']['combat_attack_dme_preview_TEST']
        assert set(now)-set(before)==P13_EXTRA_ATTACK, 'P13_ATTACK_PATCH_SCOPE_CHANGED'
        assert not(set(before)-set(now)), 'P13_ATTACK_LOST_FIELD'
        assert now['physical_attack_expression_original_P12_RETAINED_HISTORY']==before['physical_attack_expression']
        assert now['physical_attack_expression']==before['physical_dice']==now['physical_dice']
        assert 'FOR ' in before['physical_attack_expression']
        assert 'FOR(' in now['attack_test_separate_not_damage_TEST']
        assert now['FOR_damage_bonus_applied']==0
        assert now['confirmed_weapon_damage_base_by_VLAB_TEST']==before['physical_dice']
        assert current['pa_max_with_rings']==current['natural_pa']+100
        assert current['FULL']['daily_pa_two_soul_rings_TEST']==0
        for k in P13_EXTRA_ATTACK:now.pop(k)
        now['physical_attack_expression']=before['physical_attack_expression']
        assert current==legacy, 'P13_CHANGED_NON_PRESENTATION_FIELDS_LEVEL_'+str(n)
    assert a==p12,'P13_CHANGED_NON_PRESENTATION_DATA'
    assert sum(t['available'] for t in p13['transformations'])==20
    assert sum(map(len,p13['gear_ranked'].values()))==80
    return 25

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--p12-archive',type=Path,required=True)
    args=p.parse_args()
    root=Path(__file__).resolve().parents[1]/'experiments/levelup_p13'
    raw=base64.b64decode((root/'original_corrected_view.json.xz.b64').read_text().strip(),validate=True)
    view=lzma.decompress(raw)
    assert sha(view)==P13_VIEW_SHA,'P13_ORIGINAL_VIEW_SHA_MISMATCH'
    original_script=(root/'test_p13_view_cold.py').read_bytes()
    assert sha(original_script)==P13_SCRIPT_SHA,'P13_TEST_SCRIPT_SHA_MISMATCH'
    with zipfile.ZipFile(args.p12_archive.resolve()) as z:
        base=z.read(P12_JSON_NAME)
        assert sha(base)==P12_JSON_SHA,'P12_BASE_HASH_MISMATCH'
    repaired=original_comparison(json.loads(base),json.loads(view))
    with tempfile.TemporaryDirectory(prefix='p13_original_view_ci_TEST_') as td:
        q=Path(td)
        (q/'ORC_P13_25_LEVELS_20_TRANSFORMATIONS_FIELD_CORRECTED_VIEW.json').write_bytes(view)
        (q/'test_p13_view_cold.py').write_bytes(original_script)
        p=subprocess.run([sys.executable,'-I','-B',str(q/'test_p13_view_cold.py')],cwd=q,
          capture_output=True,text=True,timeout=35,check=False)
        if p.returncode or 'Ran 7 tests' not in p.stderr or '\nOK' not in p.stderr:
            raise AssertionError('P13_ORIGINAL_UNIT_TEST_FAILED:'+p.stderr[-1300:])
    print(json.dumps({
        'status':'PASS_P13_ORIGINAL_VIEW_CI_TEST_ONLY',
        'source_p13_zip_sha256_provenance_only':P13_ZIP_PROVENANCE_SHA,
        'view_sha256':P13_VIEW_SHA,
        'original_test_script_sha256':P13_SCRIPT_SHA,
        'original_test_methods_passed':7,
        'p12_to_p13_presentation_repairs_verified':repaired,
        'unchanged_nonpresentation_data':True,
        'normal_profiles':25,'transformed_profiles':20,'experimental_items':80,
        'notion_page_readback':'NOT_TESTED',
        'rpg_canon':'HOLD','vlab_acceptance':'HOLD','party_writes':0
    },sort_keys=True))

if __name__=='__main__':main()
