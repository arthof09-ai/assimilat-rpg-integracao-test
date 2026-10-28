"""R162 read-only spell save phase test with real R159 successful save event; source R160 untouched."""
import json,sqlite3,sys
from pathlib import Path
HERE=Path(__file__).parent;sys.path.insert(0,str(HERE))
from r162_receipt_producer_v1 import classify_committed_action,ReceiptError
import os
BASE=Path(os.environ.get('R160_BASE_DIRECTORY','/mnt/data/vlab_r161_work/baseline_r160'))/'r151_r160'/'runs'
file=BASE/'R159_ED_GRIFO_AUREN_BE_SPECIAL_DEV_S998803.sqlite'
with sqlite3.connect(f'file:{file.as_posix()}?mode=ro',uri=True) as c:
 rows=[json.loads(r[0]) for r in c.execute('select row_json from events order by seq')]
saved=[r['detail']['native_action'] for r in rows if r['detail'].get('native_action',{}).get('action')=='spell' and r['detail']['native_action'].get('save_exceeds_cd')]
assert len(saved)==1
x=saved[0];z=classify_committed_action(x)
assert z['gross_spell_dice_pre_save']==74 and z['raw_damage']==37 and z['net_post_RD']==37 and z['hp_effectively_lost']==37
odd=dict(x);odd['damage_rolls']=list(x['damage_rolls']);odd['damage_rolls'][0]+=1
try:classify_committed_action(odd);raise AssertionError('ODD_NOT_BLOCKED')
except ReceiptError as e:assert str(e)=='ODD_HALF_HOLD_NO_ROUNDING_RULE'
invalid=dict(x);invalid['raw']=38;invalid['effective']=38;invalid['hp_after']=485
try:classify_committed_action(invalid);raise AssertionError('WRONG_HALF_ACCEPTED')
except ReceiptError as e:assert str(e)=='SAVING_THROW_NATIVE_TRANSCRIPT_MISMATCH'
full=dict(x);full['save_exceeds_cd']=False;full['raw']=74;full['effective']=74;full['hp_before']=74;full['hp_after']=0
assert classify_committed_action(full)['gross_spell_dice_pre_save']==74
r={'status':'PASS_FOUR_SAVE_PHASE_ASSERTIONS','real_native_source_run':file.stem,'gross_pre_save':74,'native_post_save_pre_rd':37,'effective_HP_loss':37,'odd_half':'HOLD_REJECTED','inconsistent_half':'REJECTED','full_save_fail':'PASS','historical_db_modified':False}
(HERE/'R162_MAGIC_SAVE_SEMANTICS_READONLY.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(r,indent=2,ensure_ascii=False))
