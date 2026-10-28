"""R163 fresh SQLite fault injection and prospective receipt classification tests.
R18 imported from original frozen Stage12; no historical writes. Subprocess crash is intentional.
"""
import sys,subprocess,hashlib,json,sqlite3,os,pathlib,uuid
HERE=pathlib.Path(__file__).parent
STAGE=pathlib.Path('/mnt/data/vlab_r161_work/baseline_r160/r61_extracted/work/fusion_stage12')
sys.path.insert(0,str(STAGE));sys.path.insert(0,str(HERE))
import vlab_r18_interactive as core
from r162_receipt_producer_v1 import classify_committed_action as classify,ReceiptError
can=lambda d:json.dumps(d,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def verify(cond,mark):
 if not cond:raise AssertionError(mark)
def test_receipts():
 samples=[('spell',110,20,90,100),('spell',75,40,35,70),('spell',100,100,0,10),('spell',150,0,150,0),('weapon_attack',60,0,60,100),('weapon_attack',0,0,0,40)]
 out=[]
 for kind,raw,rd,post,before in samples:
  after=max(0,before-post);x={'action':kind,'raw':raw,'rd_applied':rd,('net' if kind=='weapon_attack' else 'effective'):post,
   ('before_hp' if kind=='weapon_attack' else 'hp_before'):before,
   ('after_hp' if kind=='weapon_attack' else 'hp_after'):after}
  if kind=='weapon_attack':x.update({'hp_loss_actual':before-after,'overkill':post-(before-after)})
  q=classify(x);verify(q['hp_effectively_lost']==min(before,post),'actual cap');verify(q['overkill']==max(0,post-before),'overkill');out.append(q)
 for t in ({'action':'spell','raw':100,'rd_applied':0,'effective':120,'hp_before':70,'hp_after':0},
           {'action':'spell','raw':100,'rd_applied':0,'effective':60,'hp_before':70,'hp_after':65}):
  try:classify(t);raise AssertionError('invalid accepted')
  except ReceiptError:pass
 return out

def fresh_db(tag,seed):
 d=HERE/'runs'/f'R163_{tag}_S{seed}.sqlite';d.parent.mkdir(exist_ok=True)
 verify(not d.exists(),'no repeat');core.init_db(d,'A',seed)
 return d

def create_intent(tag,seed,fail):
 db=fresh_db(tag,seed)
 # Committed sample reducer is strictly synthetic; source scope is transaction/receipt export, not mechanical combat.
 prog='''import sys;sys.path.insert(0,sys.argv[1]);import vlab_r18_interactive as c
p=sys.argv[2];defn=None

def runner(s,q,seq):
 s['R163_PROSPECTIVE_RECEIPT_SENTINEL']=q['hp_after'];return {'native_action':{'action':'spell','raw':120,'rd_applied':20,'effective':100,'hp_before':30,'hp_after':0,'PA_spent':55},'export_status':'NOT_YET_EXPORTED'}
c.event_commit(p,sys.argv[3],'RECEIPT_GATE_TEST',{'hp_after':0},runner,failpoint=sys.argv[4]);'''
 z=subprocess.run([sys.executable,'-c',prog,str(STAGE),str(db),f'LAB-CMD-R163_{tag}',fail],capture_output=True,text=True)
 verify(z.returncode in (77,78),'injected process exit '+str(z.returncode)+' '+z.stderr)
 con=sqlite3.connect(db);m=dict(con.execute('select key,value from meta'));pending=con.execute('select count(*) from pending').fetchone()[0];count=con.execute('select count(*) from events').fetchone()[0];integrity=con.execute('pragma integrity_check').fetchone()[0]
 verify(integrity=='ok','integrity')
 if fail=='AFTER_INTENT':verify((count,pending)==(0,1),'intent unchanged');verify('R163_PROSPECTIVE_RECEIPT_SENTINEL' not in json.loads(m['state']),'no partial state')
 else:
  verify((count,pending)==(1,0),'commit once');x=json.loads(con.execute('select row_json from events').fetchone()[0])['detail']['native_action'];verify(classify(x)['hp_effectively_lost']==30,'export correct after commit');verify(classify(x)['overkill']==70,'export overkill')
 con.close();return {'run':tag,'exit_code':z.returncode,'failpoint':fail,'events':count,'pending':pending,'readback_integrity':integrity,'status':'UNKNOWN_EFFECT_HOLD' if pending else 'COMMIT_ONCE_PASS'}

def main():
 tests=test_receipts();rec=[]
 for tag,seed,fail in [('FRESH_AFTER_INTENT',1163103,'AFTER_INTENT'),('FRESH_AFTER_COMMIT',1163104,'AFTER_COMMIT')]:rec.append(create_intent(tag,seed,fail))
 # Export fault: emulate content generation not physical DB mutation; failed prospective export to tempfile.
 d=HERE/'runs'/'R163_FRESH_AFTER_COMMIT_S1163104.sqlite';b=hashlib.sha256(d.read_bytes()).hexdigest()
 tmp=HERE/'R163_EXPORT_CRASH_UNPUBLISHED.tmp';tmp.write_text('{"partial":')
 tmp.unlink();verify(hashlib.sha256(d.read_bytes()).hexdigest()==b,'export cannot mutate ledger')
 result={'result':'PASS_NEW_FAULT_COPY','forward_receipt_unit_tests':len(tests),'negative_invalid_receipts':2,'injects':rec,'export_crash_no_published_csv':True,
 'original_R160_db_mutation':False,'recovery':'R18_AFTER_COMMIT_COLD_READBACK_ONLY','non_mechanical_fixture_scope':'TX_AND_EXPORT_ONLY'}
 (HERE/'R163_FORWARD_RECEIPT_AND_FAULTS.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(result,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
