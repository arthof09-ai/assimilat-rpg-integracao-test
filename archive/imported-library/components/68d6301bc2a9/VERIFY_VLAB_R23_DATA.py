"""Cold readback of 32 stored full simulated combat databases + receipts."""
from __future__ import annotations
import hashlib,sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'fusion_stage12'))
import vlab_r23_benchmark_auto as benchmark
import vlab_r21_dynamic_a1 as a1

def check(base):
    root=Path(base)
    count=0;checkpoints=0;attacks=0;reactions=0
    for sub in ('records_main','records_sensitivity/baseline','records_sensitivity/variant'):
        for record in (root/sub).glob('runs/*/FINAL_RUN_RECORD.json'):
            data=json.loads(record.read_text('utf8'))
            if data['status']!='COMPLETE_LAB':raise ValueError('INCOMPLETE_DATA_RECORD')
            db=record.parent/(data['combat_id']+'.sqlite')
            history=a1.checked_history(db)
            if data['state_sha256']!=benchmark.digest(history['state']):raise ValueError('STATE_HASH_MISMATCH')
            if data['events_sha256']!=benchmark.digest(history['events']):raise ValueError('EVENT_HASH_MISMATCH')
            if data['head']!=history['head'] or data['revision']!=history['revision']:
                raise ValueError('REVISION_CHAIN_MISMATCH')
            metrics=benchmark.metrics_from_history(history)
            if metrics!=data['metrics']:raise ValueError('METRIC_READBACK_CHANGED')
            cp=record.parent/'checkpoints'/data['checkpoint']['checkpoint_name']
            if hashlib.sha256(cp.read_bytes()).hexdigest()!=data['checkpoint']['sha256']:
                raise ValueError('CHECKPOINT_HASH_MISMATCH')
            count+=1;checkpoints+=1;attacks+=metrics['attacks'];reactions+=metrics['reactions']
    if count!=32:raise ValueError('DENOMINATOR_32_NOT_FOUND')
    return {'status':'PASS','complete_runs':count,'audited_SQLite':count,
            'native_attack_receipts':attacks,'native_reactions':reactions,
            'verified_R22_checkpoint_ZIPs':checkpoints,'canonical_source_credit':0}
if __name__=='__main__':
    print(json.dumps(check(sys.argv[1]),sort_keys=True))
