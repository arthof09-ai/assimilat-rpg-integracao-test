"""R202 pure write-set planning, no connector, no native commit.
For R201 COLUMN_TABLE synthetic TEST only, pages must be physically re-fetched.
PRE history is appended to the SAME page's final Notion toggle in a later,
separately authorized stage; no child or source item is edited.
"""
from __future__ import annotations
import re
from r198_dynamic_source import sha,SourceSnapshot
from r199_r200_live_mobile import GateHold

R201_LAYOUT='COLUMN_TABLE_R144'

def scoped_writeset(*,source:SourceSnapshot,source_body:str,preview:dict):
 if source.layout!=R201_LAYOUT:raise GateHold('R202_LAYOUT_NOT_ADMITTED')
 if source.source_hash!=sha(source_body):raise GateHold('SOURCE_NOT_THE_OBSERVED_BODY')
 if source.page_id!=preview.get('source_id') or source.version!=preview.get('source_version') or source.fingerprint()!=preview.get('source_fingerprint'):
  raise GateHold('SOURCE_OR_PREVIEW_CHANGED')
 if preview['holds'] or not preview['after']:raise GateHold('UNRESOLVED_MECHANICS')
 if preview['mode']!='FIXED60_EXPLICIT':raise GateHold('ROLL_SOURCE_NOT_EVIDENCED')
 active=source_body.split('## Regras TEST — estrutura',1)[0]
 before=preview['before'];after=preview['after']
 def fld(name,b,a,head=''):
  if b==a:return None
  if head=='':
   v={'level':'**Nível:** ','int':'**Inteligência:** ','hp':'### Vida: ','pa':'### Alma: '}
   old=v[name]+str(b);new=v[name]+str(a)
  else:old=head+str(b);new=head+str(a)
  if active.count(old)!=1 or source_body.count(old)!=1:raise GateHold('AMBIGUOUS_LITERAL_'+name)
  return {'field':name,'old_str':old,'new_str':new,'before_sha':sha(old),'after_sha':sha(new)}
 edits=[]
 for spec in [('level',before['level'],after['level']),('int',before['natural_attrs']['INT'],after['natural_attrs']['INT'])]:
  e=fld(*spec)
  if e:edits.append(e)
 for field,prefix,bval,aval in [
  ('hp','### Vida: '+str(before['hp_current'])+'/',before['hp_max'],after['hp_max']),
  ('pa','### Alma: '+str(before['pa_current'])+'/',before['pa_max'],after['pa_max'])]:
  if bval!=aval:
   old=prefix+str(bval);new=prefix+str(aval)
   if source_body.count(old)!=1 or active.count(old)!=1:raise GateHold('AMBIGUOUS_'+field)
   edits.append({'field':field,'old_str':old,'new_str':new,'before_sha':sha(old),'after_sha':sha(new)})
 if after['natural_attrs']['SAB']!=before['natural_attrs']['SAB']:
  # Update both the visible effective stat and the natural value in the table.
  old_eff=before['natural_attrs']['SAB']+source.layers['title']['SAB'];new_eff=after['natural_attrs']['SAB']+source.layers['title']['SAB']
  a=re.search(r'\*\*Sabedoria:\*\*\s*'+str(old_eff)+r'[^\n]*',active)
  if not a or active.count(a.group(0))!=1 or source_body.count(a.group(0))!=1:raise GateHold('AMBIGUOUS_SAB_EFFECTIVE')
  old=a.group(0);new=old.replace('**Sabedoria:** '+str(old_eff),'**Sabedoria:** '+str(new_eff),1)+'; R202 +' +str(after['natural_attrs']['SAB']-before['natural_attrs']['SAB'])+' SAB natural'
  edits.append({'field':'sab_effective','old_str':old,'new_str':new,'before_sha':sha(old),'after_sha':sha(new)})
  # Match only the unique physical table row (whitespace may differ between renders).
  rows=list(re.finditer(r'<tr>\s*<td>SAB natural</td>\s*<td>'+str(before['natural_attrs']['SAB'])+r'</td>\s*<td>[^\n]*</td>\s*</tr>',source_body))
  if len(rows)!=1:raise GateHold('AMBIGUOUS_SAB_TABLE')
  before_table=rows[0].group(0)
  after_table=before_table.replace('<td>'+str(before['natural_attrs']['SAB'])+'</td>','<td>'+str(after['natural_attrs']['SAB'])+'</td>',1)
  after_table=after_table.replace('Efetivo '+str(old_eff)+' = natural '+str(before['natural_attrs']['SAB']),'Efetivo '+str(new_eff)+' = natural '+str(after['natural_attrs']['SAB']))
  edits.append({'field':'sab_natural_table','old_str':before_table,'new_str':after_table,'before_sha':sha(before_table),'after_sha':sha(after_table)})
 # Any other attribute requires its own exact field adapter. Do not silently omit.
 for a in ('FOR','DES','CON','CAR'):
  if before['natural_attrs'][a]!=after['natural_attrs'][a]:raise GateHold('R202_OTHER_ATTRIBUTE_ADAPTER_REQUIRED_'+a)
 return {'status':'WRITESET_PREPARED_NOT_DISPATCHED','tx':preview['tx'],'source_id':source.page_id,'source_version':source.version,'source_hash':source.source_hash,'preview_hash':preview['preview_hash'],'edits':edits,'snapshot_pre_required':True,'history_final_toggle_required':True,'child_identities':source.structural['child_ids'],'expected_after':after,'expected_structure':source.structural,'scope':'LAB_TEST_ONLY','signature':'NOT_HOST_SIGNED'}

def dryrun_diff(source_body:str,write_set:dict):
 s=source_body
 for e in write_set['edits']:
  if s.count(e['old_str'])!=1:raise GateHold('DRYRUN_AMBIGUOUS_'+e['field'])
  s=s.replace(e['old_str'],e['new_str'],1)
 for marker in ('<columns>','</columns>','<table','</table>','<details','</details>','<page url=','<mention-page','<image','notion-file-block://'):
  if source_body.count(marker)!=s.count(marker):raise GateHold('LAYOUT_CHANGED_'+marker)
 return {'status':'PREVIEW_DIFF_PASS_NOT_APPLIED','expected_body_sha':sha(s),'edits':len(write_set['edits']),'preserved_children':source_body.count('<page url='),'preserved_toggles':source_body.count('<details')}
