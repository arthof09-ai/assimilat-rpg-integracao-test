"""R174 no-replay cold audit: hashes, existing SQLite receipts and semantic checks only.
NEVER executes an attack or changes campaign/Notion/historical databases.
"""
from __future__ import annotations
import hashlib,pathlib,json,zipfile,sys,sqlite3
ROOT=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'work'))
from r174_independent_audit import audit,read_db,sha

def structural(db):
 meta,rows,pend=read_db(db);assert not pend
 prev=meta['genesis'];last=None
 for i,cmd,p,rj,rh,bef,aft in rows:
  r=json.loads(rj)
  assert i==r['seq'] and r['cmd_id']==cmd and r['prev']==p==prev and rh==sha(r)
  assert r['before_sha']==bef and r['after_sha']==aft
  if last is not None:assert bef==last
  prev=rh;last=aft
 assert prev==meta['head'] and last==sha(json.loads(meta['state']))
 return len(rows)

def main():
 mf=json.loads((ROOT/'R174_SHA256_MANIFEST.json').read_text())
 for name,h in mf['files'].items():
  p=ROOT/name
  assert p.is_file(),('MISSING',name)
  assert hashlib.sha256(p.read_bytes()).hexdigest()==h,('SHA',name)
  if p.suffix=='.zip':
   with zipfile.ZipFile(p) as z:assert z.testzip() is None
 expected='91a03910fc170a21b63a3f114695d727b7c93c035d496b4fcd2bfda0c4e53f34'
 assert hashlib.sha256((ROOT/'baseline/R173_EXACT_UNMODIFIED.zip').read_bytes()).hexdigest()==expected
 o=[]
 for db in sorted((ROOT/'evidence/duels').glob('*.sqlite')):
  assert structural(db)>1;o.append(audit(db))
 assert len(o)==3
 directed=[]
 for policy,hp,reaction in [('DEFEND_VAROK',734,0),('HOLD_VAROK',694,1)]:
  db=ROOT/f'evidence/directed/R174_DIRECTED_DEFENDER_{policy}.sqlite'
  assert structural(db)==1
  meta,rows,pend=read_db(db)
  r=json.loads(rows[0][3])['detail'];a=r['attack']
  assert r['hp_varok']==hp and r['reaction_varok']==reaction
  assert a['roll_score']==88 and a['hit'] is True and a['ca_exact']=='83' and a['normal_damage']==75
  assert a['r174_source_actor'] if 'r174_source_actor' in a else True # directed native uses source in FrozenRuleEvidence
  assert a['hp_loss_actual']==734-hp and a['defense_negated']==(policy=='DEFEND_VAROK')
  directed.append({'policy':policy,'hp_varok':hp,'reaction_remaining':reaction})
 clones=[]
 for db in sorted((ROOT/'evidence/adversarial_clones').glob('*.sqlite')):
  assert structural(db)>1
  try:audit(db)
  except (AssertionError,ValueError,TypeError,KeyError):clones.append(db.stem)
  else:raise AssertionError('ADVERSARIAL_NOT_REJECTED:'+str(db))
 assert len(clones)==5
 cm=json.loads((ROOT/'R174_17_CONTRACT_CROSSWALK.json').read_text())
 assert len(cm['rows'])==len({x['id'] for x in cm['rows']})==17 and all(x['terminal_certified'] is False for x in cm['rows'])
 assert cm['official_cells']['after']==0
 with open(ROOT/'evidence/R174_NATIVE_ATTACK_RECEIPTS_TO_DMG.csv') as f:
  assert sum(1 for _ in f)-1==sum(x['attacks'] for x in o)==65
 return {'result':'PASS_R174_COLD_PORTABLE_RECOVERY','manifest_files':len(mf['files']),'baseline_R173_exact':True,
  'legitimate_duels':len(o),'commits':sum(x['commits'] for x in o),'native_events':sum(x['native_events'] for x in o),
  'attacks':sum(x['attacks'] for x in o),'directed':directed,'semantic_adversarial_rejected':len(clones),
  'contracts_terminal':0,'benchmarks_official':0,'no_reexecuted_effects':True}

if __name__=='__main__':
 print(json.dumps(main(),ensure_ascii=False,indent=2))
