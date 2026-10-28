"""IBX17 R95: TEST-only conversational transaction gate over historical R75/R76 receipts. No Notion writes, no rerun of mechanics."""
import json,hashlib,copy
from pathlib import Path
ROOT=Path(__file__).parent
SOURCES={'UP':'IBX17_R75_UP_PAYLOAD_COMPACT_20261016.json','DOWN':'IBX17_R76_DOWN_PAYLOAD_COMPACT_20261016.json'}
def fp(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
class Held(Exception):pass
class Injected(Exception):pass
class TestAdapter:
 def __init__(self,s):self.state=copy.deepcopy(s);self.events={};self.journal=[]
 def apply(self,event,readset,after,inject=False):
  if event in self.events:
   if self.events[event]!=fp(after):raise Held('event-collision')
   return 'NOOP_ALREADY_APPLIED'
  if fp(self.state)!=readset:raise Held('stale-readset')
  pre=copy.deepcopy(self.state)
  try:
   for k in ['NORMAL','TRANSFORM','LOCKS']:
    self.state[k]=copy.deepcopy(after[k])
    if inject and k=='NORMAL':raise Injected('partial-write')
   assert self.state==after
  except Exception:
   self.state=pre
   assert fp(self.state)==readset
   raise
  self.events[event]=fp(after);self.journal.append((event,readset,fp(after)))
  return 'COMMITTED_IN_MEMORY'
def check(kind):
 d=json.loads((ROOT/SOURCES[kind]).read_text());assert d['fixture_label']=='SYNTHETIC_EXPLICIT_ONLY'
 assert sorted(d['before'])==['LOCKS','NORMAL','TRANSFORM'] and sorted(d['after'])==['LOCKS','NORMAL','TRANSFORM']
 m=TestAdapter(d['before']);readset=fp(d['before']);after=copy.deepcopy(d['after']);confirm=False;checks=[]
 def deny(f,label):
  try:f()
  except (Held,Injected):checks.append(label)
  else:raise AssertionError(label+' not rejected')
 def commit(event):
  if not confirm:raise Held('confirmation-required')
  if event==d['event_id']:raise Held('historical-mechanics-event-reused')
  return m.apply(event,readset,after)
 deny(lambda:commit('R95-MEM-'+kind),'no-confirmation')
 assert m.state==d['before'];checks.append('rejection-no-effect')
 confirm=True
 deny(lambda:commit(d['event_id']),'historical-event-fenced')
 deny(lambda:m.apply('R95-MEM-'+kind+'-fault',readset,after,True),'partial-failure-rollback')
 assert m.state==d['before'];checks.append('rollback-readback')
 assert commit('R95-MEM-'+kind)=='COMMITTED_IN_MEMORY';checks.append('isolated-commit')
 assert m.state==after;checks.append('after-readback')
 assert commit('R95-MEM-'+kind)=='NOOP_ALREADY_APPLIED';checks.append('idempotent-replay')
 altered=copy.deepcopy(after);altered['NORMAL']['level']+=1
 deny(lambda:m.apply('R95-MEM-'+kind,readset,altered),'collision-rejected')
 deny(lambda:m.apply('R95-MEM-'+kind+'-stale',readset,altered),'stale-rejected')
 assert len(m.journal)==1
 return {'type':kind,'source_receipt':d['engine'],'historical_mechanical_event':d['event_id'],'before_sha256':readset,'after_sha256':fp(after),'tests':checks,'test_count':len(checks),'local_journal':m.journal,'notion_commit':False,'real_character':False}
if __name__=='__main__':
 out={'operation':'LEVEL-UP-ENGINE / IBX-17','scope':'R95 isolated local orchestrator: preview-confirm-apply-readback-replay','runs':[check(k) for k in SOURCES], 'real_engine_rerun':False,'notion_mutations':0,'party_mutations':0,'missing_to_complete':['0→1 native source case','multi-level native source case','rank-crossing native source case','native Notion transactional write','crash recovery causal event chain','source-bound real confirmations','R87 original PRE','media binary hashes']}
 p=ROOT/'R95_LOCAL_FLOW_READBACK_20261016.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2));print('PASS:',sum(r['test_count'] for r in out['runs']),'asserts across',len(out['runs']),'original receipts; 0 Notion writes')
