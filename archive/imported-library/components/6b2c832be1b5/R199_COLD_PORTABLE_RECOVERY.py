#!/usr/bin/env python3
"""R199 cold ZIP recovery. Read-only auditing: NEVER execute fight producers.
Works on an extracted temporary clone, not on the published evidence or historical database.
"""
from __future__ import annotations
import hashlib,importlib.util,json,pathlib,sqlite3,sys,tempfile,zipfile

EXPECTED_R198='b7fc08a1cee2891c52fbf8e446ef96da8193430a45268cc141abcbc7a9f6f11b'

def digest(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def check(condition,message):
    if not condition:raise AssertionError(message)
def load_module(name,p):
    spec=importlib.util.spec_from_file_location(name,p)
    mod=importlib.util.module_from_spec(spec)
    sys.modules[name]=mod
    spec.loader.exec_module(mod)
    return mod

def verify_zip(zippath):
    zp=pathlib.Path(zippath).resolve();check(zp.is_file(),'R199 ZIP missing')
    with zipfile.ZipFile(zp) as z:
        check(z.testzip() is None,'ZIP CRC failure')
        names=[i.filename for i in z.infolist() if not i.is_dir()]
        check('R199_SHA256_MANIFEST.json' in names,'manifest absent')
        check(len(names)==len(set(names)),'duplicate archive entries')
        with tempfile.TemporaryDirectory(prefix='r199_cold_') as tmp:
            # Fail closed for path traversal.
            out=pathlib.Path(tmp).resolve()
            check(all((out/name).resolve().is_relative_to(out) for name in names),'zip path traversal')
            z.extractall(out)
            manifest=json.loads((out/'R199_SHA256_MANIFEST.json').read_text())
            entries=manifest['entries']
            check(set(entries)==set(names)-{'R199_SHA256_MANIFEST.json'},'manifest coverage')
            for relative,detail in entries.items():
                p=out/relative
                check(p.is_file() and p.stat().st_size==detail['size'] and digest(p)==detail['sha256'],f'sha mismatch {relative}')
            baseline=out/'baseline/VLAB_R198_COMBATES_BENCH_INTEGRADO_MESTRE_ONLY.zip'
            check(digest(baseline)==EXPECTED_R198,'R198 original ZIP SHA changed')
            audit=load_module('r199_independent_replay',out/'new/r199/code/r199_independent_replay.py')
            fight_dbs=sorted((out/'new/r199/evidence/db').glob('*.sqlite'))
            check(len(fight_dbs)==32,'32 new fight DB expected')
            records=[audit.semantic(p) for p in fight_dbs]
            totals={field:sum(int(r[field]) for r in records) for field in ('commits','native_events','attacks','spells','pa_spent','transform_activations','transform_expirations','beast_power_uses')}
            for field,want in [('commits',575),('native_events',1775),('attacks',488),('spells',101),('pa_spent',1128),('transform_activations',8),('transform_expirations',6),('beast_power_uses',56)]:
                check(totals[field]==want,f'fight total changed: {field}={totals[field]} wanted {want}')
            statuses={}
            for r in records:statuses[r['fight_status']]=statuses.get(r['fight_status'],0)+1
            check(sum(statuses.values())==32,'status denominator drift')
            check(sum(v for k,v in statuses.items() if 'CENSORED' in k)==2,'expected two censored')
            bad_paths=sorted((out/'new/r199/evidence/negative').glob('*/*.sqlite'))
            check(len(bad_paths)==16,'Expected v1+v2 preserved adversarial clones')
            rejected=[]
            for p in bad_paths:
                try:audit.semantic(p)
                except (AssertionError,ValueError,KeyError,TypeError,IndexError):rejected.append(p.name)
            check(len(rejected)==len(bad_paths),'semantic tampered clone was accepted')
            # Historical R198 magic metric readback; does not touch old DBs.
            errata=load_module('r199_magic_metric_errata',out/'new/r199/code/r199_magic_metric_errata.py')
            historic_dbs=sorted((out/'new/evidence/magic_db').glob('*.sqlite'))
            check(len(historic_dbs)==8,'R198 historic magic evidence missing')
            old=[errata.corrected(p) for p in historic_dbs]
            cast_n=sum(x['casts'] for x in old);paid_n=sum(x['pa_spent'] for x in old)
            spell_actual=sum(x['water_spell_hp_removed'] for x in old)
            decline_damage=sum(x['water_spell_hp_removed'] for x in old if x['policy']=='DECLINE_WHIP')
            check((cast_n,paid_n,spell_actual,decline_damage)==(20,160,163,0),'R198 magic errata regressed')
            dry_dbs=sorted((out/'new/r199/evidence/dry_runs_v1_preserved').glob('*.sqlite'))
            check(len(dry_dbs)==6,'R199 dry original preserved')
            dry_pending=0
            for p in dry_dbs:
                conn=sqlite3.connect(f'file:{p}?mode=ro',uri=True)
                try:dry_pending+=conn.execute('SELECT COUNT(*) FROM pending').fetchone()[0]
                finally:conn.close()
            check(dry_pending==1,'one UNKNOWN_EFFECT pending expected preserved')
            ui=(out/'new/r199/ui/VLAB_R199_COMBATES_MAGIA_TRANSFORMACAO_OFFLINE.html').read_text()
            check('Poderes e transformação' in ui and 'R199_' in ui,'R199 interface bridge missing')
            return {'status':'PASS_R199_COLD_PORTABLE_RECOVERY',
                'zip_path':str(zp),'zip_sha256':digest(zp),'zip_bytes':zp.stat().st_size,
                'archive_files':len(names),'manifest_verified':len(entries),'baseline_R198_sha256':EXPECTED_R198,
                'fight_dbs':len(fight_dbs),'fight_totals':totals,'outcomes':statuses,
                'adversarial_clones_rejected':len(rejected),'adversarial_clones_total':len(bad_paths),
                'historic_magic_dbs_read_only':len(old),'historic_spells':cast_n,
                'historic_spell_PA':paid_n,'historic_spell_HP_removed':spell_actual,
                'historic_decline_spell_HP_removed':decline_damage,
                'dry_original_banks':len(dry_dbs),'dry_pending_unretried':dry_pending,
                'old_battles_rerun':0,'official_benchmarks_added':0,'terminal_contracts_certified':0,
                'independent_human_auditor':False,'production':'HOLD'}

def main():
    if len(sys.argv) not in (2,3):raise SystemExit('Usage: python R199_COLD_PORTABLE_RECOVERY.py <r199.zip> [receipt.json]')
    receipt=verify_zip(sys.argv[1]);print(json.dumps(receipt,ensure_ascii=False,indent=2))
    if len(sys.argv)==3:pathlib.Path(sys.argv[2]).write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
