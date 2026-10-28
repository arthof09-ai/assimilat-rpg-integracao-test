"""Freeze R108-R117 into one additive, provenance-rich zip, no source writes."""
from pathlib import Path
import json,hashlib,zipfile,os,sqlite3,io,csv
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent
HIST=Path('/mnt/data/VLAB_R102_R107_AUDITORIA_17_CONTRATOS_CIENCIA_MESTRE_ONLY.zip')
ZIP=Path('/mnt/data/VLAB_R108_R117_NATIVE_CRITICO_FRACO_DESCARGA_MESTRE_ONLY.zip')
expected_hash='6bb377a3683a6b7559ae564a8edec005cfca4dc728808fcb61c5ea13b242af20'
sh=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert HIST.exists() and sh(HIST)==expected_hash
prior=json.loads((ROOT/'R113_COLD_CAUSAL_AUDIT.json').read_text());assert prior['selected_runs']==6
reported=prior['totals']; assert reported['native_attacks']==208 and reported['native_specials']==4
contract=json.loads((ROOT/'R117_17_CONTRACTS_BEFORE_AFTER.json').read_text()); assert len(contract['rows'])==17 and contract['count_terminal']==0
# Immutable supplementary classification of intermediate historical quarantines.
source=json.loads((ROOT/'R111_POLICY_DRIFT_HOLD.json').read_text());seen=[]
for x in source['files']:
    if x['policy_violation'] and not x['ledger'].endswith('.checkpoint.sqlite'): seen.append({'ledger':x['ledger'],'specials':x['count_specials'],'events':x['event_count'],'status':'EXCLUDED_WITH_CHECKPOINT_PRESERVED'})
assert len(seen)==4,seen
holds={'operation':'OP-VLAB-FUSION-SANDBOX-01','R109':json.loads((ROOT/'R109_UNKNOWN_EFFECT_HOLD.json').read_text()),'R110':json.loads((ROOT/'R110_UNKNOWN_EFFECT_HOLD.json').read_text()),'R111_scientifically_excluded_distinct_ledger_count':len(seen),'R111_excluded_unique':seen,'R115_fault_intent':'UNKNOWN_EFFECT_NO_RETRY','R115_fault_commit':'READBACK_NO_RETRY','R93_R95':'HISTORICAL_IMMUTABLE_NORMATIVE_PARITY_HOLD','terminal':0}
(ROOT/'R117_QUARANTINE_RECONCILED_NO_REPEAT.json').write_text(json.dumps(holds,ensure_ascii=False,indent=2)+'\n')
README='''# VLAB R108–R117 — MESTRE-SIDE ONLY / additive continuity

## Purpose
Controlled repair of the **existing historical v0.8.1 effect module**, not a new engine. The only changed historical module is `vlab_effects_v08.py`; the original source and Stage12/R18 durability bridge are bundled under `r61_extracted` byte-identically. Historical R107 ZIP is embedded under `historical_original_R107.zip` byte-identically; it contains earlier R101/R93/R95 and original R17/R18 chain. Earlier notebooks/old runs are not mutated.

## Trust classes
**Native partial integration on isolated v0.8.1 copy**: attacks, fully taped R6 critical, Weak <10% with disadvantage, optional conditional effort, source-bound Descarga Curta (`SAVE-HALF` even only). Committed using **unchanged** R18 historical SQLite layer. Not official live combat, not official VZ character page, not native v0.8.1 full production battle certification.

**COLD auditor:** `python r108_r117/r113_independent_cold_semantic_auditor.py`; independent standard-library-only semantic event and RNG calculations, no imports of patched engine. Expected `selected_runs=6`, `636 events`, `208 attacks`, `4 specials`, `6 natural crit`, `16 weak attacks`, `2 final efforts`, `PA220`.

**Regressions:** `cd r108_r117/native_v081_controlled && python -m unittest test_vlab_effects_v08.py -q` (28 existing); `cd r108_r117 && python -m unittest r114_native_regression_unit.py -q` (23 additional). Stage12 historical imports bundled under `r61_extracted`. Diff under `R116_NATIVE_V081_PATCH.diff`; reproducibility proven by `R116_PROVENANCE_PREFLIGHT_AND_PATCH.json`.

**Fault receipts:** `R115_FAULT_RECOVERY.json`; DO NOT rerun `r115_fault_worker.py` or `r115_fault_recovery.py` on existing ledgers. AFTER_INTENT deliberately pending/UNKNOWN_EFFECT; AFTER_COMMIT successfully recovered, no duplicate damage. `R109` and `R110` also UNKNOWN_EFFECT, DO NOT RETRY; `R111` four full fights policy drift held.

**DMG handoff:** `R116_DMG_HANDOFF_R97_R112.md` and `R116_DMG_NATIVE_RECEIPTS_212.csv`. No DMG ACK. R97 1344 receipts from historical R101 remain historical HOLD for critical mismatch and should not be pooled.

**Contract crosswalk:** `R117_17_CONTRACTS_BEFORE_AFTER.md` and `.json`; 0/17 terminal. The original R105 matrix remains in embedded R107 archive.

**NAC-PASS:** limited LOCAL LAB TEST PASS. Writer/lease/instance/ACK on Notion not acquired. Party/O Primeiro/DG/RPG canon WRITE=0.
'''
(ROOT/'README_R117_REPRODUCIBILITY.md').write_text(README)
# Include only necessary actual files and code; ignore pycache and runnable cache databases.
filemap={}
def add(path,arc):
    assert arc not in filemap,arc
    filemap[arc]=path
for p in ROOT.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(ROOT)
    if '__pycache__' in rel.parts or p.suffix in ('.pyc','.pyo'):continue
    if 'r116-patch-' in str(rel):continue
    filemap['r108_r117/'+rel.as_posix()]=p
# stage12 and old pre-patch v0.8.1 essential for cold reproducibility
for folder in [BASE/'r61_extracted'/'work'/'fusion_stage12',BASE/'r61_extracted'/'work'/'working'/'historical_v081_verified_original',BASE/'r61_extracted'/'work'/'working'/'historical_v09_documentary_rebuilt',BASE/'r61_extracted'/'work'/'working'/'candidate_independent_base']:
    assert folder.exists(),folder
    for p in folder.rglob('*'):
        if not p.is_file() or '__pycache__' in p.parts or p.suffix in('.pyc','.pyo'):continue
        filemap['r61_extracted/'+p.relative_to(BASE/'r61_extracted').as_posix()]=p
for name in ['STAGE12_AUTHORITY_RECHECK_MASTER_ONLY.json','STAGE11_EIGHT_CONFLICT_DISPOSITION_MASTER_ONLY.json']:
    path=BASE/'r61_extracted'/'work'/'reconstruction'/name
    assert path.exists()
    filemap['r61_extracted/work/reconstruction/'+name]=path
filemap['historical_original_R107.zip']=HIST
# Zip owns manifest; CRC and file SHA verified after creation.
manifest={'schema':'R117_INTERNAL_MANIFEST_1','operation':'OP-VLAB-FUSION-SANDBOX-01','baseline':'R01-R107 IMUTAVEL','file_count_excluding_manifest':len(filemap),'sha256':{arc:sh(p) for arc,p in sorted(filemap.items())},'writer':'NONE','17_terminal':0,'UNKNOWN_EFFECT':'HOLD_NO_RETRY','generated_utc_date':'2026-10-16'}
with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for arc,p in sorted(filemap.items()):z.write(p,arc)
    z.writestr('MANIFEST_R117.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(ZIP,'r') as z:
    assert z.testzip() is None
    names=z.namelist()
    m=json.loads(z.read('MANIFEST_R117.json'))
    assert len(names)==len(m['sha256'])+1 and len(names)==len(set(names))
    for arc,digest in m['sha256'].items(): assert hashlib.sha256(z.read(arc)).hexdigest()==digest,arc
    assert hashlib.sha256(z.read('historical_original_R107.zip')).hexdigest()==expected_hash
rec={'ZIP':str(ZIP),'sha256':sh(ZIP),'bytes':ZIP.stat().st_size,'total_entries':len(names),'hashed_entries':len(m['sha256']),'CRC':'PASS','hashes':'PASS','original_R107_archive_hash_preserved':expected_hash,'cold_auditor':'TO_RUN_FROM_EXTRACTED_ARCHIVE','library_readback':'NOT_YET','terminal_claims':0}
# JSON report lives outside archive to avoid self-referential hash.
(BASE/'R117_ZIP_FREEZE_RECEIPT.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(rec,ensure_ascii=False,indent=2))
