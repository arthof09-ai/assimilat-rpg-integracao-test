"""Durable original R48 store, explicitly isolated TEST; no official item/stock."""
from __future__ import annotations
from pathlib import Path
import sys,json,copy,hashlib,shutil
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))
from native_pingente_runner import build_factory,make_order,REVIEW,KEY,CASE
from r48_factory import FactoryError
from r48_store import DurableFactory

def run(out=None):
 target=Path(out) if out else BASE/'results/R48_TEST_DURABLE_NEW'
 if target.exists():raise ValueError('TEST_STORE_ALREADY_EXISTS_DO_NOT_REUSE')
 target.mkdir(parents=True)
 store=DurableFactory(target)
 store.initialize(build_factory())
 f0,p0=store.recover();before=copy.deepcopy(f0.quantities)
 ptr0=copy.deepcopy(p0)
 req_magic=make_order(48321,'MAGIC_TEST')
 error=None
 try:store.commit_batch('SBX-R48-BATCH-VIGILIA-MAGIC-NEG-DURABLE',[req_magic],REVIEW)
 except FactoryError as e:error=str(e)
 assert error=='MAGIC_TRANSFER_NOT_DEMONSTRATED',error
 f1,p1=store.recover();assert f1.quantities==before and p1==ptr0 and not f1.journal
 structural=make_order(48322,'STRUCTURAL_TEST')
 req='SBX-R48-BATCH-VIGILIA-DURABLE-STRUCTURAL-NEW'
 commit=store.commit_batch(req,[structural],REVIEW,expected_head=f1.head)
 assert commit['disk_sequence']==1 and not commit['idempotent_replay']
 f2,p2=store.recover(expected_head=commit['r48_head']);after=copy.deepcopy(f2.quantities)
 assert f2.audit()['ok'] and len(f2.journal)==1 and len(f2.vault.events)==1 and len(f2.core.state['events'])==1
 assert commit['receipt']['orders'][0]['recipe_key']==KEY
 assert commit['receipt']['orders'][0]['status']=='EXPERIMENTAL_QA_PASS'
 assert commit['receipt']['orders'][0]['authenticity']['status']=='SIMULATED_CRYPTO_VALID_NOT_REAL'
 assert commit['receipt']['physical_products']==0 and commit['receipt']['official_stock_effect']==0
 replay=store.commit_batch(req,[structural],REVIEW)
 f3,p3=store.recover(expected_head=commit['r48_head'])
 assert replay['idempotent_replay'] and replay['disk_sequence']==1
 assert f3.snapshot()==f2.snapshot() and p3==p2
 summary={'mode':'R48_ORIGINAL_MODULES_IN_TWO_FILE_TEST_EXTENSION','case_id':CASE,
   'negative_magic':{'status':'REJECTED_BEFORE_COMMIT','reason':error,'store_pointer_unchanged':ptr0==p1,'before_stock_unchanged':f1.quantities==before},
   'structural':{'batch_id':req,'order_id':structural['order_id'],'recipe_key':KEY,
    'status':commit['receipt']['orders'][0]['status'],'r48_batch_receipt_sha256':hashlib.sha256(json.dumps(commit['receipt'],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),
    'r47_status':commit['receipt']['orders'][0]['authenticity']['status'],
    'stage_trace':commit['receipt']['orders'][0]['process_trace'],
    'synthetic_products':commit['receipt']['experimental_product_count'],
    'physical_products':0,'official_inventory_effect':0,'before':before,'after':after,
    'commit_sequence':p2['sequence'],'r48_head':f2.head,'r44_head':f2.core.state['head_hash'],'r47_head':f2.vault.head,
    'r46_and_r47_logged':True,'quality_witness':'PUBLIC_TEST_ROOT_AND_SYNTHETIC_MEASUREMENTS_ONLY'},
   'replay':{'idempotent':replay['idempotent_replay'],'sequence':replay['disk_sequence'],'unchanged':p3==p2},
   'durable_store':{'path':'results/R48_TEST_DURABLE_NEW','before_seq':ptr0['sequence'],'after_seq':p2['sequence'],
     'commits':p2['known_commits'],'snapshot_hash':p2['snapshot_sha256'],'readback_audit':f2.audit()['ok']},
   'transferencia_magica':'MAGIC_TRANSFER_NOT_DEMONSTRATED','rc':'RC3_TEST_INDICATIVO',
   'any_physical_item':False,'any_real_magic':False,'rc5_p4_prod':'HOLD','f5':'RED','c19_021':'UNKNOWN_EFFECT'}
 target.parent.joinpath('DURABLE_R48_PINGENTE_RESULTS.json').write_text(json.dumps(summary,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf8')
 print(json.dumps({k:summary[k] for k in ('negative_magic','structural','replay','durable_store')},ensure_ascii=False,indent=2)[:7000])
 return summary
if __name__=='__main__':run()
