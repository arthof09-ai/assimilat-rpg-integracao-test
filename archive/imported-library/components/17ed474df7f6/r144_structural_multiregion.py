"""R144 structural multi-region plan. Never embeds match literals in destination page.
Notion adapter uses one block-contained exact field per change and readback.
"""
from dataclasses import dataclass
from hashlib import sha256
import json
class Hold(ValueError):pass
PARENT='3fcc2b324ede81868256e6db67ece28e'
CHILD='3fcc2b324ede816baed0f833958640ec'
EVENT='IBX17-R144-SYNTH-MULTIREGION-20261017-02'
LEVEL={"old":"**Nível:** 16","new":"**Nível:** 17"}
HP={"old":"### Vida: 240/292","new":"### Vida: 240/309"}
PA={"old":"### Alma: 150/258 (30 comprometidos)","new":"### Alma: 150/273 (30 comprometidos)"}
SAB={"old":"**Sabedoria:** 7 (+2 título sintético)","new":"**Sabedoria:** 9 (+2 título sintético; +2 natural SAB R144 TEST)"}
TABLE_OLD='<td>CON</td>\n<td>10</td>\n<td>Sem bônus de item</td>\n</tr>\n</table>'
TABLE_NEW='<td>CON</td>\n<td>10</td>\n<td>Sem bônus de item</td>\n</tr>\n<tr>\n<td>SAB natural</td>\n<td>7</td>\n<td>EFETIVO 9 = natural7 + titulo2 (TEST), sem soma dupla</td>\n</tr>\n</table>'
CHILD_OLD='CHILD_R144_EVENT: PREPARED'
CHILD_NEW='CHILD_R144_EVENT: RECORDED_AFTER_PARENT_TABLE_READBACK'

def h(s):return sha256(s.encode('utf-8')).hexdigest()

def preflight(body,*,stage,expected_version,observed_version,parent,scope):
 if parent!='3fbc2b324ede804a95fafcb7b293c92c' or scope!='LAB_TEST':raise Hold('WRITER_FORBIDDEN')
 if observed_version!=expected_version:raise Hold('STALE')
 pairs=[LEVEL,HP,PA,SAB] if stage=='COLUMNS' else [{'old':TABLE_OLD,'new':TABLE_NEW}] if stage=='TABLE' else [{'old':CHILD_OLD,'new':CHILD_NEW}]
 if any(body.count(x['old'])!=1 or body.count(x['new'])>0 for x in pairs):raise Hold('NON_UNIQUE_OR_ALREADY_COMMITTED')
 return pairs

def compare_structure(before,after,pairs,*,allow_new_row):
 x=before
 for p in pairs:x=x.replace(p['old'],p['new'],1)
 if x!=after:raise Hold('UNPLANNED_CONTENT')
 keys=['<columns>','<table ','<details','<page url=','<mention-page','notion-file-block://']
 for k in keys:
  if before.count(k)!=after.count(k):raise Hold('STRUCTURE_CHANGED_'+k)
 for k in ['<tr>','</tr>']:
  delta=after.count(k)-before.count(k)
  if delta!=(1 if allow_new_row else 0):raise Hold('ROW_CHANGE_OUTSIDE_WRITESET')
 return True

def test():
 body='X '+LEVEL['old']+' Y '+HP['old']+' Z '+PA['old']+' '+SAB['old']+' '+TABLE_OLD
 prs=preflight(body,stage='COLUMNS',expected_version='v',observed_version='v',parent='3fbc2b324ede804a95fafcb7b293c92c',scope='LAB_TEST')
 after=body
 for p in prs:after=after.replace(p['old'],p['new'])
 assert compare_structure(body,after,prs,allow_new_row=False)
 assert compare_structure(after,after.replace(TABLE_OLD,TABLE_NEW),[{'old':TABLE_OLD,'new':TABLE_NEW}],allow_new_row=True)
 try:preflight(body+LEVEL['old'],stage='COLUMNS',expected_version='v',observed_version='v',parent='3fbc2b324ede804a95fafcb7b293c92c',scope='LAB_TEST')
 except Hold:pass
 else:raise AssertionError('duplicate accepted')
 try:preflight(body,stage='COLUMNS',expected_version='v',observed_version='v2',parent='3fbc2b324ede804a95fafcb7b293c92c',scope='LAB_TEST')
 except Hold:pass
 else:raise AssertionError('stale accepted')
 return 4

if __name__=='__main__':
 n=test();receipts={'event':EVENT,'parent':PARENT,'child':CHILD,'stages':{'COLUMNS':[{'old_sha256':h(p['old']),'after_sha256':h(p['new'])} for p in (LEVEL,HP,PA,SAB)],'TABLE':{'old_sha256':h(TABLE_OLD),'after_sha256':h(TABLE_NEW)},'CHILD':{'old_sha256':h(CHILD_OLD),'after_sha256':h(CHILD_NEW)}},'level_from_to':[16,17],'natural_sab_delta':2,'growth_fixed_d12':7,'hp_max':[292,309],'pa_max':[258,273],'current_hp':240,'current_pa':150,'normal_ff':290,'title_and_equipment_untouched':True}
 path='/mnt/data/IBX17_R137_R146/evidence/R144_STRUCTURAL_FIELD_HASHES.json';open(path,'w').write(json.dumps(receipts,indent=2,ensure_ascii=False));print('R144 local',n,'CHECKS PASS; receipt',path)
