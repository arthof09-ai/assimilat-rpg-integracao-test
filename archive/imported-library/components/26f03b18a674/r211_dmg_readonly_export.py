"""Source-preserving only, SQL READONLY, emits per-target events without counting targets as independent runs."""
from pathlib import Path
import sqlite3,json,csv
ROOT=Path(__file__).resolve().parents[1]
rows=[]
for p in sorted((ROOT/'evidence/db').glob('R211_DYN_AOE_S*.sqlite')):
 c=sqlite3.connect('file:'+str(p)+'?mode=ro',uri=True)
 try:
  st=json.loads(dict(c.execute('select key,value from meta'))['state']);pol=st['r211']['policy'];seed=st['seed'];casts={}
  for ev in st['native_events']:
   if ev['action']=='r211_area_cast':casts[ev['seq']]=ev
   if ev['action']=='r211_area_target':
    par=casts[ev['cast_seq']]
    rows.append({'RUN_ID':p.stem,'SEED_PAIR':seed,'POLICY':pol,'UNIT':'PER_TARGET_RESOLUTION_NOT_COMBAT',
      'CAST_EVENT':ev['cast_seq'],'TARGET_EVENT':ev['seq'],'TARGET':ev['target'],
      'CENTER':str(par['center_m']),'POSITION':str(ev['position_m']),
      'SPELL_SOURCE':'https://app.notion.com/p/3f6c2b324ede819cae98ec0f6a63de76',
      'SPELL':'Tempestade de Esporos','ACTION':'STANDARD','PA_PER_CAST_ONLY':80,
      'SHARED_DICE':str(par['common_roll']),'DAMAGE_ROLL_BRUTO':par['raw_spell_damage'],
      'SAVE_DICE':str(ev['save_dice']),'SAVE_ATTRIBUTE_PURE':ev['save_attribute_pure'],
      'SAVE_TOTAL':ev['save_total'],'SAVE_CD':ev['save_cd'],'SAVE_SUCCESS':ev['save_success'],
      'DAMAGE_AFTER_SAVE':ev['damage_raw'],'RD_MAGIC_TEST':ev['rd_magic'],
      'DAMAGE_POST_RD':ev['damage_post_rd'],'HP_ACTUALLY_LOST':ev['hp_effective'],
      'OVERKILL':ev['overkill'],'HP_BEFORE':ev['hp_before'],'HP_AFTER':ev['hp_after'],
      'SOURCE_STATUS':'PROPOSTO_CONFLICT_BEAST_RD_MAGIC_TEST0','CENSORING':'HORIZON_NOT_VICTORY'})
 finally:c.close()
assert len(rows)==50
out=ROOT/'evidence/R211_DMG_READONLY_RECEIPTS.csv'
with out.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print(out,'rows',len(rows))
