"""Cold independent R173 data replay; does not execute a new combat effect.
Usage: python R173_COLD_PORTABLE_RECOVERY.py R173.zip receipt.json
"""
from __future__ import annotations
import tempfile,zipfile,hashlib,json,pathlib,sys,shutil,sqlite3
EXPECTED_R172='aecadd7a93186ce170fb3a84dfab21855be3121033372e0aa3a7c359f023dc17'
EXPECTED_ORIGINAL_CONTRACTS=17

def sha(data):return hashlib.sha256(data).hexdigest()
def cold(zip_path,receipt):
 zp=pathlib.Path(zip_path)
 with zipfile.ZipFile(zp) as z:
  files=z.namelist()
  assert len(files)==len(set(files)), 'DUPLICATE_ZIP_PATH'
  assert z.testzip() is None,'ZIP_BAD_CRC'
  man=json.loads(z.read('R173_SHA256_MANIFEST.json'))
  assert set(man)==set(files)-{'R173_SHA256_MANIFEST.json'},'MANIFEST_COVERAGE'
  for k,v in man.items():assert sha(z.read(k))==v,('BAD_HASH',k)
  assert sha(z.read('R172_BASELINE_EXACT.zip'))==EXPECTED_R172,'BAD_BASELINE'
  with tempfile.TemporaryDirectory(prefix='vlab_r173_cold_') as temp:
   root=pathlib.Path(temp)
   z.extractall(root)
   with zipfile.ZipFile(root/'R172_BASELINE_EXACT.zip') as base:
    assert base.testzip() is None
    base.extractall(root/'R172_REHYDRATED')
   target=root/'R172_REHYDRATED'
   shutil.copy2(root/'code/r173_source_battle.py',target/'r173_source_battle.py')
   shutil.copy2(root/'code/r173_independent_scientific_audit.py',target/'r173_independent_scientific_audit.py')
   # Replay independent examiner never imports R173 producer.
   sys.path.insert(0,str(target))
   import r173_independent_scientific_audit as auditor
   results=[]
   for pol in ('ALWAYS_DODGE','TACTICAL_SAVE'):
    db=root/'evidence'/f'R173_SOURCE_LEVIATHAN_{pol}_1730101.sqlite'
    with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as con:
     assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
     assert con.execute('SELECT COUNT(*) FROM pending').fetchone()[0]==0
    results.append(auditor.audit(db,True))
   bad=root/'evidence/ADVERSARIAL_TAMPER_REHASH_NOT_LEGITIMATE.sqlite'
   # Valid structural hash chain, but source math intentionally falsified.
   import vlab_r18_interactive as r18
   assert r18.load(bad)[2]==72
   try:auditor.audit(bad,False);raise AssertionError('TAMPER_ACCEPTED')
   except AssertionError as exc:
    if str(exc)=='TAMPER_ACCEPTED':raise
    if 'R173_SEMANTIC_MISMATCH_ATTACK_net' not in str(exc):raise
    badreason=str(exc)
   source=json.loads((root/'R173_SOURCE_ADMISSIBILITY.json').read_text())
   assert source['classification']['entire_duel_full_source_admissible'] is False
   contracts=json.loads((root/'R173_CONTRACT_DELTA.json').read_text())
   assert len(contracts['rows'])==EXPECTED_ORIGINAL_CONTRACTS
   assert contracts['R173_terminals']==0 and contracts['official_cells']['after']==0
   for a in results:
    assert a['attacks']==71 and a['journal_commits']==72 and a['winner']=='AUREN'
    assert a['metrics']['hp_loss']==6060 and a['metrics']['overkill']==155
    assert a['metrics']['post_rd']==6215 and a['metrics']['pa_spent']==0
   assert results[0]['metrics']['reactions_spent']==1 and results[1]['metrics']['reactions_spent']==0
   result={'result':'PASS_R173_COLD_PORTABLE_RECOVERY','R172_baseline_sha':EXPECTED_R172,
      'R173_zip_sha':sha(zp.read_bytes()),'zip_entries':len(files),'manifest_verified':len(man),
      'source_actors':'Sikong Auren L3 vs Leviata Ferro Mnemonico L4','new_matchup':1,
      'paired_policy_runs':2,'seed_class':'DEV_NOT_HOLDOUT','attack_attempts_per_run':71,
      'genuine_source_complete_battles':0,'conditional_sandbox_combat_executions':2,
      'journal_commits':sum(x['journal_commits'] for x in results),
      'native_events':sum(x['native_events'] for x in results),
      'net_damage_per_run':6215,'hp_loss_per_run':6060,'overkill_per_run':155,
      'adversarial_hash_recomputed_rejected':1,'adversarial_reason':badreason,
      'independent_verifier':'SEPARATE_LOCAL_SOURCE_MATH_AUDITOR_NOT_HUMAN_EXTERNAL',
      'terminal_contracts':0,'official_benchmark_cells':0,'canon_writes':0,'party_writes':0,
      'writer':'HOLD_NO_WRITER','R172_historical_effects_rerun':False,
      'results':results}
   rp=pathlib.Path(receipt);rp.parent.mkdir(exist_ok=True,parents=True)
   rp.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
   return result
if __name__=='__main__':
 out=cold(*sys.argv[1:3]);print(json.dumps({k:v for k,v in out.items() if k!='results'},ensure_ascii=False,indent=2))
