"""R216C2 READONLY independent source-scoped control audit (no engine imports)."""
from pathlib import Path
import sqlite3,json,hashlib,math,ast
ROOT=Path(__file__).resolve().parents[1]
def canonical(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def H(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def ck(ok,why):
 if not ok:raise AssertionError(why)
def coord(v):return tuple(float(x) for x in (ast.literal_eval(v) if isinstance(v,str) else v))
def audit(f):
 c=sqlite3.connect(f'file:{f}?mode=ro&immutable=1',uri=True)
 try:
  meta=dict(c.execute('select key,value from meta'));st=json.loads(meta['state']);rows=list(c.execute('select seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha from events order by seq'));pending=list(c.execute('select * from pending'))
  ck(len(rows)==2 and meta['revision']=='2' and not pending,'FULL_TWO_COMMITS_NO_PENDING');prev=meta['genesis'];rr=[];last=None
  for seq,cmd,old,jrow,rowsha,bef,aft in rows:
   row=json.loads(jrow);ck(old==prev==row['prev'] and H(row)==rowsha,'CHAIN');ck(row['seq']==seq and row['cmd_id']==cmd,'SEQ');ck(bef==row['before_sha'] and aft==row['after_sha'],'TRANSITION');ck(last is None or bef==last,'STATE_CONTINUITY');ck(row['kind']=='R216_CONTROL_NATIVE_TURN','KIND');ck(row['detail']['events_added'][0]['action']=='turn_start' and row['detail']['events_added'][-1]['action']=='turn_end','TURN_FULL_COVERAGE');rr+=row['detail']['events_added'];prev=rowsha;last=aft
  ck(prev==meta['head'] and last==H(st),'HEAD');ck(rr==st['native_events'],'EVENTS_EXACT')
  case=st['r216ctrl']['case'];ck(case in ('inside','outside') and st['phase']=='CENSORED_CONTROL_WINDOW','CASE_PHASE')
  spell=next(x for x in rr if x['action']=='R216_RAIZES_SOURCE_CAST');ck(spell['PA_spent']==85 and spell['radius']==4 and spell['center']==[7,1] and spell['standard_spent']==1,'SPELL_SOURCE_COST_AREA')
  ck(st['actors']['E']['pa']==719 and st['actors']['E']['standard']==0,'CAST_PA_RESOURCE');att=next(x for x in rr if x['action']=='weapon_attack');ck(att['from']=='R' and att['to']=='V' and att['attack_origin']=='NORMAL','NORMAL_ATTACK_NOT_ARTIFICIAL_DAMAGE');ck(att['before_hp']==734 and att['after_hp']==st['actors']['V']['hp'] and att['hp_loss_actual']==734-att['after_hp'],'HP_CAUSAL')
  ck(sum(x['action']=='turn_start' for x in rr)==2 and sum(x['action']=='turn_end' for x in rr)==2,'TWO_TURNS');ck(st['actors']['R']['standard']==0,'ATTACK_CONSUMED_STANDARD');ck(st['actors']['R']['pa']==344,'R_PA_NOT_INVENTED')
  if case=='inside':
   ev=next(x for x in rr if x['action']=='R216_RAIZES_SAVE_AT_TURN_START');ck(ev['rolls'] and len(ev['rolls'])==4 and sum(ev['rolls'])+23==ev['total'] and ev['total']<=76 and ev['success'] is False,'CONTROL_REFLEXO_FAIL');r=next(x for x in rr if x['action']=='R216_RAIZES_MOVEMENT_RESTRICTED');ck(r['movement_legal'] is False and r['no_HP_loss'] is True,'CONTROL_NO_FAKE_DAMAGE');ck(not any(e['action']=='move' for e in rr),'NO_FAKE_MOVE');ck(coord(st['actors']['R']['position'])==(3,1) and st['actors']['R']['movement']==1,'CONTROL_PRESERVE_MOVEMENT_RESOURCE');ck(sum(x['action']=='R216_RAIZES_NO_TRIGGER' for x in rr)==0,'INSIDE_TRIGGER')
  else:
   ck(sum(x['action']=='R216_RAIZES_NO_TRIGGER' for x in rr)==1,'NEGATIVE_NO_TRIGGER');ck(not any(e['action']=='R216_RAIZES_SAVE_AT_TURN_START' for e in rr),'NEGATIVE_NO_FABRICATED_SAVE');moves=[e for e in rr if e['action']=='move'];ck(len(moves)==1,'NEGATIVE_NATIVE_MOVE');m=moves[0];ck(coord(m['from'])==(2,1) and coord(m['to'])==(1,1) and float(m['travel_cost'])==1 and float(m['speed'])==4,'NEGATIVE_MOVE_PATH');ck(st['actors']['R']['movement']==0 and coord(st['actors']['R']['position'])==(1,1),'NEGATIVE_MOVE_DEBIT')
  return {'case':case,'seed':st['seed'],'file':f.name,'commits':2,'events':len(rr),'attack_HP_loss':att['hp_loss_actual'],'PA_activated':85,'move_completed':int(case=='outside'),'root_triggered':int(case=='inside'),'pass':'PASS_R216_CONTROL_SOURCE_SCOPED'}
 finally:c.close()

def run(root=ROOT):
 dbs=sorted((root/'evidence/db').glob('R216_CTRL_*.sqlite'));ck(len(dbs)==2,'CONTROL_EXACT_2_CASES');a=[audit(f) for f in dbs];ck(set(x['case'] for x in a)=={'inside','outside'},'POS_NEG_REQUIRED')
 res={'status':'PASS_R216_TERRAIN_CONTROL_INDEPENDENT_READ_ONLY','new_mechanic':'Raizes de Refugio ON5 proposed NPC, NOT Beast control','canonical_expiry':'HOLD','runs':a}
 (root/'evidence/reports/R216_CONTROL_INDEPENDENT_AUDIT.json').write_text(json.dumps(res,indent=2,ensure_ascii=False));return res
if __name__=='__main__':print(json.dumps(run(),indent=2,ensure_ascii=False))
