"""R212 fully independent SQLite/JSON auditor; never imports combat executor."""
from pathlib import Path
import json,hashlib,sqlite3
R=Path(__file__).resolve().parents[1];DB=R/'evidence/db';PRE=json.loads((R/'source/R212_PHYSICAL_AFTER_MOVE_PREREG.json').read_text())
def enc(obj):return json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(obj):return hashlib.sha256(enc(obj).encode()).hexdigest()
results=json.loads((R/'evidence/R212_RESULTS.json').read_text());out=[]
assert len(results)==len(PRE['seeds']) and {x['seed'] for x in results}==set(PRE['seeds'])
for line in results:
 if 'db' not in line:continue
 p=DB/line['db']; assert p.exists()
 c=sqlite3.connect(f'file:{p}?mode=ro',uri=True)
 try:
  rows=c.execute('SELECT seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha FROM events ORDER BY seq').fetchall()
  meta=dict(c.execute('SELECT key,value FROM meta'))
  assert len(rows)==2 and not c.execute('SELECT * FROM pending').fetchall()
  prev=meta['genesis'];prior_after=None
  for seq,cmd,previous,row_json,rowsha,before,after in rows:
   record=json.loads(row_json)
   assert seq==record['seq'] and cmd==record['cmd_id'] and prev==previous==record['prev']
   assert rowsha==sha(record) and record['before_sha']==before and record['after_sha']==after
   if prior_after is not None:assert before==prior_after
   prev=rowsha;prior_after=after
  st=json.loads(meta['state'])
  assert prev==meta['head'] and prior_after==sha(st) and int(meta['revision'])==2
  assert st['phase']=='CENSORED_TEST_WINDOW' and st['winner'] is None and st['active'] is None
  assert st['r212']['prereg_sha']==hashlib.sha256((R/'source/R212_PHYSICAL_AFTER_MOVE_PREREG.json').read_bytes()).hexdigest()
  assert len(st['r212']['shots'])==1 and len(st['r212']['path'])==1
  r=json.loads(rows[1][3]);ev=r['detail']['native_events_added']
  assert [x['action'] for x in ev]==['move','weapon_attack','turn_end']
  m,a=ev[:2];assert m['from']=='(0, 0)' and m['to']=='(5, 0)' and m['travel_cost']=='5' and m['speed']=='137/2'
  assert a['seq']==m['seq']+1 and a['attack_origin']=='NORMAL' and a['from']=='RAYA_REPLICA_R212' and a['to']=='ERISTAN_REPLICA_R212'
  assert not a['weak_attacker'] and a['advantage_levels']==0 and a['defensive_reaction'] is None
  assert len(a['attack_roll_attempts'])==1 and len(a['attack_roll_attempts'][0])==6
  assert a['roll_score']==sum(a['attack_roll_attempts'][0])+245 and a['ca_exact']=='76'
  groups=a['damage_roll_groups'];assert tuple(map(len,groups))==(16,12,4)
  for vals,faces in zip(groups,(8,6,12)): assert all(1<=v<=faces for v in vals)
  assert a['normal_damage']==sum(map(sum,groups))+294
  bonus=(16*8+12*6+4*12) if a['critical']=='POSITIVE' else 0
  assert a['raw']==a['normal_damage']+bonus
  assert a['hit'] and a['rd_applied']==25 and a['net']==max(0,a['raw']-25)
  assert a['hp_loss_actual']==min(630,a['net']) and a['before_hp']==630 and a['after_hp']==630-a['hp_loss_actual']
  assert a['after_hp']==st['actors']['ERISTAN_REPLICA_R212']['resource']['hp']
  raya=st['actors']['RAYA_REPLICA_R212']['resource'];er=st['actors']['ERISTAN_REPLICA_R212']['resource']
  assert raya['movement']==0 and raya['standard']==0 and raya['reaction']==1 and er['reaction']==1
  assert raya['pa']==632 and er['pa']==804
  assert st['r212']['positions_m']['RAYA_REPLICA_R212']==[5,0]
  assert line['hp_loss']==a['hp_loss_actual'] and line['head']==prev
  assert not [x for x in st['native_events'] if x.get('attack_origin')=='OPPORTUNITY']
  out.append({'run':line['run_id'],'sha':prev,'native_events':len(st['native_events']),'damage':a['hp_loss_actual'],'physical_RD_assumption':25,'critical':a['critical'],'censored':True})
 finally:c.close()
summary={'status':'PASS_R212_INDEPENDENT_R18_NATIVE_MOVEMENT_RANGED_PHYSICAL_SQLITE_CONDITIONAL_RD',
 'audited_runs':len(out),'native_moves':len(out),'native_attacks':len(out),'physical_hits':len(out),
 'damage_conditional_effective':sum(x['damage'] for x in out),'ko':0,'censures':len(out),
 'opportunity_attacks':0,'R43_gate':'BLOCKED-SOURCE-ADJACENCY',
 'source_limit':'mixed bow physical/magic damage attribution and physical RD are LAB-ONLY, not canonical',
 'observations':out}
(R/'evidence/R212_INDEPENDENT_SQL_AUDIT.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False));print(json.dumps({k:v for k,v in summary.items() if k!='observations'},indent=2))
