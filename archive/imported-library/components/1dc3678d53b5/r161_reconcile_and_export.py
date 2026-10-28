"""R161/R162: independent, read-only original SQLite reconciliation; repaired prospectively exported receipts.
No imports from resolver. Source originals are immutable in R160 extraction.
"""
import sqlite3,json,csv,hashlib,collections
from pathlib import Path
import os
BASE=Path(os.environ.get('R160_BASE_DIRECTORY','/mnt/data/vlab_r161_work/baseline_r160'))/'r151_r160'
HERE=Path(__file__).parent
INDEX=json.loads((BASE/'R160_SELECTED_LEDGER_COUNTS.json').read_text())
OLD=list(csv.DictReader((BASE/'R160_NEW_NATIVE_OFFENSE_RECEIPTS_SOURCE_SCOPED.csv').open()))
canon=lambda o:json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
sha=lambda o:hashlib.sha256(canon(o).encode()).hexdigest()
assert len(OLD)==154 and len(INDEX['per_run'])==9
key=lambda r:(r['ledger_file'].removesuffix('.sqlite'),int(r['seq_R18']),int(r['action_index_in_tx']))
original={key(r):r for r in OLD};assert len(original)==154
out=[];issues=[];counts=collections.Counter();per={}
for run,meta_expect in INDEX['per_run'].items():
 db=BASE/'runs'/f'{run}.sqlite';uri=f'file:{db.as_posix()}?mode=ro'
 con=sqlite3.connect(uri,uri=True)
 integrity=con.execute('pragma integrity_check').fetchone()[0]
 meta=dict(con.execute('select key,value from meta'))
 rows=list(con.execute('select seq,row_json,row_sha from events order by seq'))
 pending=con.execute('select count(*) from pending').fetchone()[0]
 assert integrity=='ok' and pending==0 and len(rows)==meta_expect['commits']
 assert int(meta['revision'])==len(rows)
 prev=meta['genesis'];local=0
 for seq,row_text,rowsha in rows:
  row=json.loads(row_text)
  assert row['seq']==seq and row['prev']==prev and sha(row)==rowsha,(run,seq,'row/hash')
  prev=rowsha
  detail=row.get('detail') or {}
  acts=detail.get('native_actions') or ([detail['native_action']] if detail.get('native_action') else [])
  for j,act in enumerate(acts,1):
   if act.get('action') not in ('weapon_attack','spell'):continue
   k=(run,seq,j);assert k in original,k
   r=original[k]; assert rowsha==r['row_SHA256'] and row['cmd_id']==r['cmd_id']
   kind=act['action'];before=act['before_hp'] if kind=='weapon_attack' else act['hp_before'];after=act['after_hp'] if kind=='weapon_attack' else act['hp_after']
   net=act['net'] if kind=='weapon_attack' else act['effective']
   raw=act['raw'];rd=act['rd_applied'];old_effective=int(r['hp_effectively_lost'])
   assert all(type(x)==int and x>=0 for x in (before,after,net,raw,rd))
   assert after==max(0,before-net),(k,before,after,net)
   actual=before-after;over=max(0,net-before)
   assert actual==min(before,net) and actual+over==net
   if kind=='weapon_attack':
    assert act['hp_loss_actual']==actual and act['overkill']==over
   assert int(r['net_post_RD'])==net
   if old_effective!=actual:issues.append({'run':run,'seq':seq,'native_idx':j,'kind':kind,'old_effective':old_effective,'corrected_effective':actual,'overkill_extra':old_effective-actual,'target_hp_before':before,'target_hp_after':after})
   new=dict(r);new['hp_effectively_lost']=actual;new['overkill']=over;new['hp_before']=before;new['hp_after']=after
   new['net_post_RD']=net;new['classification_version']='R162-HP-EFFECTIVE-CAP-V1';new['source_event_sha256']=rowsha
   new['audit_status']='R161_INDEPENDENT_RECONCILED_SOURCE_CONDITIONAL_NOT_OFFICIAL'
   out.append(new);counts.update({'receipts':1,'post_rd':net,'hp_effective':actual,'overkill':over,'raw':raw})
   local+=1
 assert prev==meta['head'] and local==meta_expect['native_offenses']
 per[run]={'commits':len(rows),'receipts':local,'pending':pending,'sqlite_sha256':hashlib.sha256(db.read_bytes()).hexdigest(),'head':prev}
 con.close()
assert len(out)==154 and sum(v['commits'] for v in per.values())==466
assert counts['post_rd']==counts['hp_effective']+counts['overkill']
assert [counts['post_rd'],counts['hp_effective'],counts['overkill']]==[11870,11808,62],counts
assert sum(i['overkill_extra'] for i in issues)==37 and len(issues)==3,issues
F=list(out[0]); p=HERE/'R162_CORRECTED_RECEIPTS_R160_HISTORICAL_UNMODIFIED.csv'
with p.open('w',newline='') as f:w=csv.DictWriter(f,F);w.writeheader();w.writerows(out)
result={'status':'PASS','original_R160_rows':len(OLD),'reconciled_receipts':len(out),'commits':sum(v['commits'] for v in per.values()),'new_export_only':str(p.name),
'original_post_rd':counts['post_rd'],'correct_hp_effective':counts['hp_effective'],'overkill':counts['overkill'],'old_sum_hp_effectively_lost':sum(int(x['hp_effectively_lost']) for x in OLD),
'old_unclassified_excess':sum(i['overkill_extra'] for i in issues),'old_incorrect_records':issues,'per_run':per,
'selected_original_zip_sha256':'7b208fe553809df6a999a1e4f9a70d7ad116033e929256bc71dbcd61843f3410','old_records_modified':False,
'interpretation':'native spell effective means after RD before HP cap; it is not HP effectively lost. Native weapon has separate hp_loss_actual.'}
(HERE/'R161_R162_NATIVE_RECONCILIATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('per_run',)},ensure_ascii=False,indent=2))
