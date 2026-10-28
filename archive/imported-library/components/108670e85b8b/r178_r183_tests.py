"""R178 range materialization + R183 adversarial and crash isolation. Only new TEST banks."""
import pathlib,sys,json,sqlite3,copy,shutil,hashlib,subprocess,os
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
import r180_r182_varok_leviathan as prod
import r183_independent_auditor as auditor
import vlab_r18_interactive as r18
from vlab_effects_v08 import EffectBlocked
CAN=auditor.CAN;SHA=auditor.SHA
DEV=ROOT/'evidence'/'R180_VAROK_LEVIATHAN_ARMOR_ON_FIRST_SOURCE_ATTACK_SEED17718001.sqlite'

def range_gates():
 accepted=[];rejected=[]
 for name,src,reach,dist,los,ammo_needed,ammo in [
  ('ISKIEL_WITHIN_80M','https://app.notion.com/p/3f6c2b324ede81a78a59d3d81fd5e966',80,60,True,True,True),
  ('VE YUN_WITHIN_30M','https://app.notion.com/p/3f6c2b324ede819e879bebb795001ba',30,25,True,False,None),
  ('ISKIEL_OUTSIDE_80M','https://app.notion.com/p/3f6c2b324ede81a78a59d3d81fd5e966',80,81,True,True,True),
  ('VE YUN_OUTSIDE_30M','https://app.notion.com/p/3f6c2b324ede819e879bebb795001ba',30,31,True,False,None),
  ('ISKIEL_LOS_FALSE','https://app.notion.com/p/3f6c2b324ede81a78a59d3d81fd5e966',80,20,False,True,True),
  ('ISKIEL_NO_AMMO','https://app.notion.com/p/3f6c2b324ede81a78a59d3d81fd5e966',80,20,True,True,False),
 ]:
  args={'range_m':reach,'dist_m':dist,'los':los,'required_ammo':ammo_needed,'ammo_available':ammo}
  rec={'case':name,'source_page':src,'source_max_m':reach,'experiment_distance_m':dist,'source_status':'NPC_PROPOSED_ENCOUNTER_SOURCE','args':args,'not':'CANONICAL_CAMPAIGN_POSITION'}
  try:rec['proof']=prod.numeric_range_gate(**args);rec['decision']='ALLOW_PREFLIGHT_ONLY';accepted.append(rec)
  except EffectBlocked as e:rec['decision']='DENY_BEFORE_COMMIT';rec['reason']=str(e);rejected.append(rec)
 assert len(accepted)==2 and len(rejected)==4
 # Persist one positive source-specified numerical preflight through the EXISTING R18 event_commit.
 db=ROOT/'evidence'/'R178_NUMERIC_SOURCE_RANGE_PREFLIGHT_ONLY.sqlite'
 if not db.exists():r18.init_db(db,'A',17717801)
 def preflight(s,p,seq):
  if p!=accepted[0]:raise EffectBlocked('RANGE_PAYLOAD_NOT_PINNED')
  allowed=prod.numeric_range_gate(**p['args'])
  if s['phase']!='INIT':raise EffectBlocked('PREFLIGHT_ALREADY_COMMITTED')
  s['range_preflight']={'source':p['source_page'],'source_status':p['source_status'],'criterion':allowed,'sample_m':60,'admitted_action':False}
  return {'source_range_evidence':allowed,'target':'LAB_POSITION','not_a_real_attack':True,'no_HP_or_PA_writes':True}
 if r18.load(db)[2]==0:r18.event_commit(db,'LAB-CMD-R178-NEW-RANGE-PREFLIGHT-01','R178_SOURCE_NUMERIC_RANGE_TEST',accepted[0],preflight)
 st,head,rev=r18.load(db);assert rev==1 and st['range_preflight']['sample_m']==60
 accepted[0]['r18_committed_db']=db.name
 result={'result':'PASS_SOURCE_NUMERIC_GATE','admitted_preflight':accepted,'rejected_preflight':rejected,'legitimate_range_preflight_commits':1,'actions_or_attacks_from_gate':0}
 (ROOT/'evidence'/'R178_NUMERIC_RANGE_TESTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 return result

def clone(label,edit):
 dst=ROOT/'negative_cases'/('R183_FORGERY_'+label+'.sqlite');shutil.copy2(DEV,dst)
 c=sqlite3.connect(dst)
 rows=[json.loads(row[0]) for row in c.execute('SELECT row_json FROM events ORDER BY seq')]
 state=json.loads(c.execute('SELECT value FROM meta WHERE key="state"').fetchone()[0]);edit(rows,state)
 prev=c.execute('SELECT value FROM meta WHERE key="genesis"').fetchone()[0]
 for i,row in enumerate(rows):
  row['prev']=prev
  if i:row['before_sha']=rows[i-1]['after_sha']
  if i==len(rows)-1:row['after_sha']=SHA(state)
  now=SHA(row)
  c.execute('UPDATE events SET prev=?,row_json=?,row_sha=?,before_sha=?,after_sha=? WHERE seq=?',(prev,CAN(row),now,row['before_sha'],row['after_sha'],row['seq']))
  prev=now
 c.execute('UPDATE meta SET value=? WHERE key="head"',(prev,));c.execute('UPDATE meta SET value=? WHERE key="state"',(CAN(state),));c.commit();c.close()
 cp=json.loads(pathlib.Path(str(DEV)+'.checkpoint.json').read_text());cp['body']['head']=prev;cp['body']['state']=state;cp['sha256']=SHA(cp['body'])
 pathlib.Path(str(dst)+'.checkpoint.json').write_text(json.dumps(cp,ensure_ascii=False,indent=2)+'\n')
 try:auditor.audit(dst)
 except (AssertionError,ValueError,TypeError,KeyError,sqlite3.Error) as e:
  return {'case':label,'status':'REJECTED_INDEPENDENT_SEMANTIC_AUDITOR','structural_hash_rebuilt':True,'checkpoint_rebuilt':True,'forged_db':dst.name,'error_type':type(e).__name__}
 raise AssertionError('INVALID_FORGERY_ACCEPTED: '+label)

def adversarial():
 assert auditor.audit(DEV)['result']=='PASS_SOURCE_SCOPED_R18_NATIVE_REPLAY'
 cases={
 'INITIATIVE':lambda rows,st:st['init_record']['VAROK'].__setitem__('exact',999),
 'GEOMETRY':lambda rows,st:st['geometry'].__setitem__('surface_contact',False),
 'SOURCE_IDENTITY':lambda rows,st:rows[1]['detail'].__setitem__('source_page',auditor.S['VAROK']['page']),
 'RD':lambda rows,st:rows[1]['detail']['attack'].__setitem__('rd_applied',34),
 'PA_DEBIT':lambda rows,st:rows[1]['detail']['PA_after'].__setitem__('VAROK',324),
 'ARMOR_PREVENTION':lambda rows,st:rows[1]['detail'].__setitem__('item_prevented',0),
 'DAMAGE_TAPE':lambda rows,st:rows[1]['payload']['tape']['damage'].__setitem__(0,9 if rows[1]['payload']['tape']['damage'][0]!=9 else 8),
 'REACTION_DUPLICATE':lambda rows,st:st.__setitem__('armor_used',False),
 'WRONG_POLICY':lambda rows,st:st.__setitem__('policy','ARMOR_OFF'),
 'NATIVE_EVENT_LOSS':lambda rows,st:st['native_events'].pop(),
 }
 result=[clone(k,v) for k,v in cases.items()]
 assert len(result)==10
 doc={'result':'PASS_TEN_SQL_SEMANTIC_FORGERIES_REJECTED','clones':result,'auditor':'LOCAL_SEPARATE_CODE_NOT_EXTERNAL_REVIEW'}
 (ROOT/'evidence'/'R183_ADVERSARIAL.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
 return doc

def crash_checks():
 records=[]
 for name,point,code in [('AFTER_INTENT','AFTER_INTENT',78),('AFTER_COMMIT','AFTER_COMMIT',77)]:
  path=ROOT/'evidence'/f'R183_FAULT_NEW_{name}.sqlite';seed=17718990 if name=='AFTER_INTENT' else 17718991
  newly_created=not path.exists()
  if newly_created:
   prod.setup(path,seed,'ARMOR_OFF')
   st,_,_=r18.load(path)
   payload={'seed':seed,'initiative':prod.initiative(seed),'geometry':st['geometry']}
   snippet='''import sys,json
from pathlib import Path
root=Path(sys.argv[1]);sys.path.insert(0,str(root/'code'))
import r180_r182_varok_leviathan as p
import vlab_r18_interactive as r18
db=sys.argv[2];seq=int(sys.argv[3]);st,_,_=r18.load(db);payload={'seed':seq,'initiative':p.initiative(seq),'geometry':st['geometry']}
r18.event_commit(db,'LAB-CMD-R183-'+sys.argv[4],'R183_COLD_FAULT_START',payload,p.start,failpoint=sys.argv[5])
'''
   outcome=subprocess.run([sys.executable,'-c',snippet,str(ROOT),str(path),str(seed),name,point],capture_output=True,text=True)
   assert outcome.returncode==code,(name,outcome.stderr)
  else:
   # Existing crashed AFTER_INTENT command is NEVER retried.
   assert name=='AFTER_INTENT' and code==78
  c=sqlite3.connect(path)
  m=dict(c.execute('SELECT key,value FROM meta'))
  state=json.loads(m['state']);rev=int(m['revision']);pending=c.execute('SELECT cmd_id FROM pending').fetchall();c.close()
  if name=='AFTER_INTENT':
   assert rev==0 and len(pending)==1 and state['phase']=='INIT'
   try:r18.load(path)
   except Exception as e:assert 'UNKNOWN_EFFECT' in str(e)
   else:raise AssertionError('PENDING_INTENT_WAS_ACCEPTED_AS_CLEAN')
  else:
   assert rev==1 and pending==[] and state['phase']=='ACTIVE'
   try:r18.event_commit(path,'LAB-CMD-R183-'+name,'R183_COLD_FAULT_START',{'seed':seed,'initiative':prod.initiative(seed),'geometry':state['geometry']},prod.start)
   except Exception as e:assert 'DUPLICATE COMMAND REJECTED' in str(e)
   else:raise AssertionError('REPLAY_DUPLICATE_AFTER_COMMIT')
  records.append({'new_bank':path.name,'failure':point,'child_process_exit':code,'revision_after':rev,'pending_count':len(pending),'state_phase':state['phase'],'retried':False,'new_attack_events':0,'historical_UNKNOWN_EFFECT_touched':False})
 doc={'result':'PASS_R18_KNOWN_TRANSACTION_FAILURE_POINTS','records':records,'note':'AFTER_INTENT remains pending NO-RETRY; AFTER_COMMIT persists exactly one control event'}
 (ROOT/'evidence'/'R183_CRASH_ISOLATION.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
 return doc

if __name__=='__main__':
 print(json.dumps({'range':range_gates()['result'],'adversarial':adversarial()['result'],'crash':crash_checks()['result']},ensure_ascii=False,indent=2))
