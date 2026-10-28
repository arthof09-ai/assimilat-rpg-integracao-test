"""DMG C28 -- read-only secondary observation of VLAB R205 evidence.
No runner imported or combat re-executed. The VLAB archive remains VLAB-owned.
"""
import hashlib,json,csv,io,sqlite3,tempfile,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent; OUT=ROOT/'publication'
archive=ROOT/'vlab_readonly/VLAB_R205_DEFESA_DE_VENTO_ANEL_CLASSIFICADO_MESTRE_ONLY.zip'
sha=hashlib.sha256(archive.read_bytes()).hexdigest()
assert sha=='62a9851b3a5ae7919b9225d9379a3d32c8736448e76bfcea4729dcbfe933cead'
rows=[]
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 ref=json.loads(z.read('new/r205/evidence/R205_RING_INDEPENDENT_AUDIT.json'))
 orig=json.loads(z.read('new/r205/evidence/R205_RING_LIVE_FIGHTS.json'))
 assert len(orig)==8 and ref['dbs']==8
 for o in orig:
  fname='new/r205/evidence/db/'+o['db']
  with tempfile.NamedTemporaryFile(suffix='.sqlite') as fp:
   fp.write(z.read(fname));fp.flush()
   con=sqlite3.connect('file:'+fp.name+'?mode=ro',uri=True)
   meta=dict(con.execute('SELECT key,value FROM meta'))
   state=json.loads(meta['state'])
   n_events=con.execute('SELECT COUNT(*) FROM events').fetchone()[0]
   con.close()
  # state is the *last* event state; the audit source contains published counters.
  assert meta['head']==o['head']
  assert n_events==o['commits']
  auditrow=ref['pairs'][str(o['seed'])]['on' if o['policy']=='MAGIC_ON' else 'off']
  assert auditrow['head']==o['head'] and auditrow['attacks']==o['attacks']
  assert auditrow['interceptions']==o['intercepted_attempts']
  assert auditrow['pa_spent']==o['pa_spent_item']
  assert auditrow['status']==o['status']
  assert (o['ring_markings'],o['ring_returns'],o['intercepted_attempts'])==((1,1,1) if o['policy']=='MAGIC_ON' else (0,0,0))
  assert (o['pa_spent_item']==36) == (o['policy']=='MAGIC_ON')
  # audited counts are VLAB events, NOT current DMG run count.
  rows.append([o['run_id'],o['seed'],o['policy'],o['status'],n_events,o['native_events'],o['attacks'],o['hits'],o['ring_markings'],o['ring_returns'],o['intercepted_attempts'],o['pa_spent_item'],o['final_hp'],o['rounds'],meta['head'],'LAB_SEMICANONICAL_CONTESTED_BEAST_RANK'])
assert sum(x[4] for x in rows)==384
assert sum(x[5] for x in rows)==1156
assert sum(x[6] for x in rows)==186
assert sum(x[8] for x in rows)==4 and sum(x[9] for x in rows)==4 and sum(x[10] for x in rows)==4
assert sum(x[11] for x in rows)==144
assert sum(x[3]=='KO' for x in rows)==4
assert sum(x[3]=='CENSORED_HORIZON' for x in rows)==4
pairs=[]
for seed in sorted(set(x[1] for x in rows)):
 off=next(x for x in rows if x[1]==seed and x[2]=='MAGIC_OFF')
 on=next(x for x in rows if x[1]==seed and x[2]=='MAGIC_ON')
 assert on[3]==off[3] and on[12]==off[12]
 pairs.append([seed,off[3],on[3],off[12],on[12],off[13],on[13],on[13]-off[13],off[6],on[6],on[10]])
with (OUT/'C28_VLAB_R205_PAIRED_OUTCOME_4_SEEDS.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['seed','status_OFF','status_ON','finalHP_OFF','finalHP_ON','rounds_OFF','rounds_ON','delta_rounds_ONminusOFF','attacks_OFF','attacks_ON','interceptions_ON']);w.writerows(pairs)
with (OUT/'C28_VLAB_R205_RING_READONLY_OBSERVATIONS_8.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['run_id','seed','policy','status','sqlite_commits','native_events','attack_attempts','hits','marks','returns','intercepts','pa_item','final_hp','rounds','head','limit']);w.writerows(rows)
info={'checked_archive_sha256':sha,'size_bytes':archive.stat().st_size,'crc_pass':True,'runs':8,'pairs':4,'sql_readonly':True,'attack_attempts':186,'commits':384,'native_events':1156,'ring_marks':4,'ring_returns':4,'intercepts_before_attack_roll':4,'item_pa_spent_total':144,'KOs':4,'censored':4,'paired_HP_outcome_changed_count':0,'paired_KO_status_changed_count':0,'combat_runners_executed':0,'evidence_is_real_existing_VLAB_TEST_executions_not_new_DMGC28_fights':True,'documentary_limits':['Ring semicanonical/incubating, not homologated production item','Beast Dracolion rank body Ouro versus tree Ouro Negro1; generic basic attack conditional','Only 4 paired seeds, no general survival treatment effect','Selo and Manopla not physically run in R205','Paired runs share seeds; not 8 independent samples'],'upstream_notion':'https://app.notion.com/p/3ffc2b324ede81c895eaeb0cd64d1c66'}
(OUT/'C28_VLAB_R205_READONLY_AUDIT.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS R205 existing SQLite',len(rows),'runs',info['commits'],'commits',info['native_events'],'events',info['intercepts_before_attack_roll'],'intercepts; 0 runner executions')
