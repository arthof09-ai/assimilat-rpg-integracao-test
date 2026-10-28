"""READ-ONLY independent audit of R213 SQLite journals. Does NOT import R213 combat runner or v0.8.1."""
from __future__ import annotations
import sqlite3,json,hashlib,glob,collections,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=json.loads((ROOT/'sources/R44_R46_FROZEN_MASTER_SOURCE.json').read_text())['sources']
PRE=json.loads((ROOT/'sources/R213_PREREG.json').read_text());PHASH=hashlib.sha256((ROOT/'sources/R213_PREREG.json').read_bytes()).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def sha(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def require(c,msg):
 if not c:raise AssertionError(msg)
def audit(db):
 c=sqlite3.connect(f'file:{db}?mode=ro',uri=True)
 try:
  meta=dict(c.execute('SELECT key,value FROM meta'))
  events=c.execute('SELECT seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha FROM events ORDER BY seq').fetchall()
  pending=c.execute('SELECT cmd_id,base_head FROM pending').fetchall()
  if pending:
   require(not events and meta['revision']=='0' and len(pending)==1,'bad quarantine')
   return {'db':Path(db).name,'status':'QUARANTINED_PENDING_UNKNOWN_EFFECT','commits':0,'attacks':0}
  st=json.loads(meta['state']);r=st['r213'];case=r['case'];seed=st['seed'];mover=st['active']
  require(r['prereg_sha']==PHASH,'prereg sha');require(st['synthetic'] is True,'synthetic flag')
  require(len(events)==int(meta['revision'])==1,'revision');previous=meta['genesis']
  for number,cmd,prev,raw,h,b,a in events:
   row=json.loads(raw)
   require(number==row['seq'] and prev==previous and row['prev']==prev and row['cmd_id']==cmd and sha(row)==h,'R18 chain row')
   require(row['before_sha']==b and row['after_sha']==a and a==sha(st),'state consistency')
   require(row['payload']=={'case':case,'seed':seed,'prereg_sha':PHASH},'payload prereg')
   previous=h
  require(previous==meta['head'],'R18 chain head')
  ne=st['native_events'];require([e['seq'] for e in ne]==list(range(1,len(ne)+1)),'native monotonic')
  require(ne[0]['action']=='r213_departure_preflight','missing preflight')
  attacks=[e for e in ne if e['action']=='weapon_attack'];moves=[e for e in ne if e['action']=='move']
  require(all(e['attack_origin']=='OPPORTUNITY' and e['advantage_levels']==1 and e['net_levels']==1 for e in attacks),'AoO advantage native')
  require(ne[0]['metric_conversion']=='UNDEFINED_WORLD_RULE','forbidden world rule')
  eligible=ne[0]['eligible_reactions'];require([e['from'] for e in attacks]==eligible[:len(attacks)],'wrong actor/prio')
  for i,e in enumerate(attacks):
   a=SRC[e['from']];d=SRC[e['to']]
   require(len(e['attack_roll_attempts'])==2,'not two attempt advantages')
   require(e['roll_score']==max(map(sum,e['attack_roll_attempts']))+a['attack_bonus']+2,'score does not implement Advantage')
   require(e['normal_damage']==sum(sum(z) for z in e['damage_roll_groups'])+a['damage_bonus'],'damage tape invalid')
   require(e['after_hp']==max(0,e['before_hp']-e['net']),'hp relation')
   require(e['hp_loss_actual']==e['before_hp']-e['after_hp'],'effective hp')
   require(e['rd_applied']==min(e['raw'],d['rd']) if e['hit'] else e['rd_applied']==0,'rd mismatch')
   require(e['critical']!='NEGATIVE','neg crit not admitted')
   require(ne[0]['seq']<e['seq'],'AoO before trigger')
  for x in moves: require(x['seq']>max([q['seq'] for q in attacks],default=0),'movement published before AoO')
  if case=='DOUBLE':
   require(eligible==['F','V'] and len(attacks)==2 and len(moves)==1,'double')
   require(st['actors']['F']['resource']['reaction']==0 and st['actors']['V']['resource']['reaction']==0,'reaction consumption')
  if case=='NONADJACENT':
   require(not eligible and not attacks and len(moves)==1,'false opportunity')
   require(all(st['actors'][x]['resource']['reaction']==1 for x in ('F','V')),'spurious reaction')
  if case=='REACTION_SPENT':
   require(eligible==['V'] and [e['from'] for e in attacks]==['V'] and len(moves)==1,'spent reaction bypass')
   require(st['actors']['F']['resource']['reaction']==0,'spent snapshot lost')
  if case=='LETHAL':
   require(eligible==['F','V'] and len(attacks)==1 and attacks[0]['from']=='F','wrong lethal order')
   require(not moves and st['actors']['G']['resource']['position']=='(0.0, 0.0)','KO movement published')
   require(st['actors']['G']['resource']['hp']==0 and st['actors']['V']['resource']['reaction']==1,'KO second reaction not spared')
   require(r['movement_outcome']=='KO_INTERRUPTED_COST_UNRESOLVED','unknown movement cost invented')
  require(r['metrics']['aoo']==len(attacks) and r['metrics']['movement']==len(moves),'wrong counts')
  require(r['metrics']['reaction_spent']==len(attacks),'reactions')
  require(r['metrics']['hp_loss']==sum(x['hp_loss_actual'] for x in attacks),'damage accounting')
  require(r['metrics']['hits']==sum(bool(x['hit']) for x in attacks),'hit accounting')
  return {'db':Path(db).name,'status':'PASS_TEST_CONDITIONAL','commits':len(events),'attacks':len(attacks),'hits':sum(e['hit'] for e in attacks),
     'hp_loss':sum(e['hp_loss_actual'] for e in attacks),'moves':len(moves),'reactions':len(attacks),'native_events':len(ne),'case':case,'seed':seed}
 finally:c.close()

def main():
 rs=[audit(f) for f in sorted((ROOT/'evidence/db').glob('*.sqlite'))]
 committed=[x for x in rs if x['status']=='PASS_TEST_CONDITIONAL']
 totals={'sqlite_total':len(rs),'admitted':len(committed),'quarantined':len(rs)-len(committed),'commits':sum(x['commits'] for x in rs),
 'attacks':sum(x['attacks'] for x in committed),'hits':sum(x['hits'] for x in committed),'movement':sum(x['moves'] for x in committed),
 'reaction_spent':sum(x['reactions'] for x in committed),'hp_loss':sum(x['hp_loss'] for x in committed),'ko_case_count':sum(x['case']=='LETHAL' for x in committed)}
 receipt={'audit':'PASS_R213_INDEPENDENT_R18_NATIVE_OPPORTUNITY_FIXTURE_CONDITIONAL','scope':'LAB-TEST-CONDITIONAL','totals':totals,'per_db':rs,
 'limitations':['UNKNOWN_WORLD_BLOCK_WIDTH','TEST_ONLY_MOVER_SPEED_3M','UNKNOWN_MOVEMENT_COST_AFTER_KO','R45B_NATIVE_REACTION_DEBIT_INTERNAL_AFTER_ROLL'],'canonical_credit':0,'terminal_contracts':0,'matrix_cells_homologated':0}
 (ROOT/'evidence/R213_INDEPENDENT_SQL_AUDIT.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False))
 print(json.dumps(totals,indent=2));return receipt
if __name__=='__main__':main()
