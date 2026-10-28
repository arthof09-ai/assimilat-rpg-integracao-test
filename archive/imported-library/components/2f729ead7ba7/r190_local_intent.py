"""One distinct R190 LAB event; persists R173 intent before any Notion mechanical effect.
This script does not contact Notion and is not an authority to write there.
"""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).parent))
sys.path.insert(0,str(Path(__file__).resolve().parent/'compat_runtime'))
from r173_sqlite_causal_ledger import Ledger,LAB,AUTH
from r188_r189_vertical import initial_test_state,calculate
TARGET='3fec2b324ede81d1bed5d6d0a7d60681'
TX='IBX17-R190-MVP-VERTICAL-20261019-01'
STAGE='NORMAL_TWO_LEVELS'
PRE_VERSION='2026-10-19T16:50:46.069Z'
SOURCE_VERSION='IBX17-R99@2026-10-16T21:42:47.998Z'
DB=Path(__file__).parent/'evidence'/'r190_native_ledger.sqlite'
DB.parent.mkdir(exist_ok=True)
ALLOC=[{'FOR':0,'DES':0,'CON':0,'INT':2,'SAB':0,'CAR':0},{'FOR':0,'DES':0,'CON':0,'INT':0,'SAB':2,'CAR':0}]
PLAN=calculate(initial_test_state(fixture_id=TARGET),tx=TX,per_level_allocations=ALLOC)
normal_before=PLAN['before']['normal'];normal_after=PLAN['after']['normal']
KEYS={'LEVEL':'level','ATTR_FOR':'FOR','ATTR_DES':'DES','ATTR_CON':'CON','ATTR_INT':'INT','ATTR_SAB':'SAB','ATTR_CAR':'CAR','VIDA_ATUAL':'hp_current','VIDA_MAXIMA':'hp_max','PA_ATUAL':'pa_current','PA_MAXIMO':'pa_max','PA_COMPROMETIDO':'pa_committed','PA_LIVRE':'pa_free','FF':'ff','CA':'ca','CD_MAGIA':'magic_cd','LUTA':'luta'}
def projected(n):
 return {k:(n['natural_attrs'][val] if k.startswith('ATTR_') else n[val]) for k,val in KEYS.items()}

def physical_fields(n,tx_state,tx_id):
 return {'target':TARGET,'parent':LAB,'character_id':'SYNTH-R99-R190-REPLICA-TEST','tx_state':tx_state,'tx_id':tx_id,'fields':projected(n),'spirit_active':False,'spirit_cap':16,'spirit_tap_test':0,'spirit_carry':0,'ff_locks':'100=CA(1);200=DANO(1);300=VIDA(4,3)','history_snapshot_pre':True,'table_sentinel':'R190-LAB-SENTINEL-KEEP','source_mention':True}
BEFORE=physical_fields(normal_before,'PRE','NONE')
AFTER=physical_fields(normal_after,'AFTER_PENDING_READBACK',TX)
def prepare_intent():
 with Ledger(DB) as l:
  r=l.create_intent(tx=TX,stage=STAGE,target=TARGET,parent=LAB,source_version=SOURCE_VERSION,before=BEFORE,after=AFTER,pre_version=PRE_VERSION,authority=AUTH)
  return {'create_intent':r,'chain':l.verify_chain(TX,STAGE),'classification':l.classify(TX,STAGE),'before':BEFORE,'after':AFTER,'local_math_steps':PLAN['steps'],'ledger_path':str(DB)}
if __name__=='__main__':
 print(json.dumps(prepare_intent(),ensure_ascii=False,indent=2))
