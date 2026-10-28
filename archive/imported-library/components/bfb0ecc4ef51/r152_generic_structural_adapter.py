"""R152 generic read-only and preparatory Notion layout adapter.
No native block ID invented. Schema/section configurable per fixture; no target constants.
Updates only unique literals in well-scoped active field regions; never touches history,
child pages, mentions or assets; native writing via guarded external connector only.
"""
from dataclasses import dataclass
from hashlib import sha256
import re,json
class Hold(ValueError):pass
LAB='3fbc2b324ede804a95fafcb7b293c92c'

def h(x):return sha256(x.encode()).hexdigest()
@dataclass(frozen=True)
class TargetSource:
 page_id:str; parent_id:str; version:str; format:str; source_version:str

def parse_sections(body,config):
 if config['format']=='COLUMN_TABLE':
  if body.count('<columns>')!=1 or body.count('</columns>')!=1:raise Hold('COLUMN_REGION_AMBIGUOUS')
  section=body.split('<columns>',1)[1].split('</columns>',1)[0]
  fieldmap={}
  for key,pattern in config['patterns'].items():
   match=re.findall(pattern,section)
   if len(match)!=1:raise Hold('FIELD_AMBIGUOUS_'+key)
   fieldmap[key]={'raw':match[0],'value':match[0] if isinstance(match[0],str) else match[0][-1],'resource_current':match[0][0] if isinstance(match[0],tuple) and len(match[0])==2 else None,'region':'COLUMN','location_type':'ENRICHED_MARKDOWN_NOT_NATIVE_BLOCK_UUID'}
  return fieldmap
 if config['format']=='SECTION_JSON':
  start=config['start'];end=config['end']
  if body.count(start)!=1 or body.count(end)<1:raise Hold('ACTIVE_JSON_SECTION_AMBIGUOUS')
  section=body.split(start,1)[1].split(end,1)[0]
  m=re.search(r'```json\n([^\n]+)\n```',section)
  if not m:raise Hold('JSON_NOT_PRESENT')
  obj=json.loads(m.group(1));d={}
  for key,path in config['paths'].items():
   item=obj
   for node in path:item=item[node]
   d[key]={'value':item,'path':path,'region':'ACTIVE_JSON','location_type':'PAGE_SECTION_NOT_NATIVE_BLOCK_UUID'}
  return d
 raise Hold('UNKNOWN_FORMAT')

def prepare_write(*,target:TargetSource,body:str,config:dict,changes:dict,expected_version:str,authorized:bool):
 if not authorized or target.parent_id!=LAB:raise Hold('WRITER_OR_PARENT_FORBIDDEN')
 if expected_version!=target.version:raise Hold('STALE_TARGET_VERSION')
 discovered=parse_sections(body,config)
 if not changes or not set(changes).issubset(discovered):raise Hold('UNKNOWN_FIELD')
 if target.format=='COLUMN_TABLE':
  updates=[]
  for key,v in changes.items():
   prefix=config['prefixes'][key]
   if key in ('hp','pa'):
    prefix=prefix+str(discovered[key]['resource_current'])+'/'
   old=f"{prefix}{discovered[key]['value']}"
   new=f"{prefix}{v}"
   if body.count(old)!=1:raise Hold('FIELD_LITERAL_REPEATED_GLOBALLY_'+key)
   if old==new:raise Hold('NOOP_FIELD')
   updates.append({'old_str':old,'new_str':new,'field':key,'sha_before':h(old),'sha_after':h(new)})
  return {'status':'WRITESET_READY_NOT_APPLIED','target':target.page_id,'version':target.version,'edits':updates,'original_body_sha':h(body),'scope':'LAB_TEST'}
 if target.format=='SECTION_JSON':
  # Propose whole JSON block only when section is delimited and unique. No native write by this function.
  start,end=config['start'],config['end'];part=body.split(start,1)[1].split(end,1)[0]
  original=re.search(r'```json\n([^\n]+)\n```',part).group(1);obj=json.loads(original)
  for key,v in changes.items():
   path=config['paths'][key];cur=obj
   for node in path[:-1]:cur=cur[node]
   cur[path[-1]]=v
  updated=json.dumps(obj,ensure_ascii=False,separators=(',',':'))
  if body.count(original)!=1:raise Hold('JSON_BLOB_NOT_UNIQUE')
  return {'status':'WRITESET_READY_NOT_APPLIED','target':target.page_id,'version':target.version,'edits':[{'old_str':original,'new_str':updated,'field':','.join(changes),'sha_before':h(original),'sha_after':h(updated)}],'original_body_sha':h(body),'scope':'LAB_TEST'}

def compare_after(before,after,write_set):
 expected=before
 for e in write_set['edits']:
  if expected.count(e['old_str'])!=1:raise Hold('PRE_DIFF_AMBIGUITY')
  expected=expected.replace(e['old_str'],e['new_str'],1)
 if after!=expected:raise Hold('OUTSIDE_WRITESET_MODIFIED')
 immutable=['<columns>','</columns>','<table','</table>','<details','</details>','<page url=','<mention-page','notion-file-block://']
 return {'status':'PASS_ENRICHED_MARKDOWN_STRUCTURE','tokens':{k:before.count(k) for k in immutable},'structure_preserved':all(before.count(k)==after.count(k) for k in immutable),'scope':'MARKDOWN_LINK_STRUCTURE_NOT_BINARY_SHA'}

def column_config():return {'format':'COLUMN_TABLE','patterns':{'level':r'\*\*Nível:\*\*\s*(\d+)','int':r'\*\*Inteligência:\*\*\s*(\d+)','sab':r'\*\*Sabedoria:\*\*\s*(\d+)','hp':r'### Vida:\s*(\d+)/(\d+)','pa':r'### Alma:\s*(\d+)/(\d+)'},'prefixes':{'level':'**Nível:** ','int':'**Inteligência:** ','sab':'**Sabedoria:** ','hp':'### Vida: ','pa':'### Alma: '}}
def json_config():return {'format':'SECTION_JSON','start':'### R125 COMPOSITE ACTIVE','end':'<details','paths':{'level':['normal','level'],'ff':['locks','ff'],'hp':['resources','hp_max'],'pa':['resources','pa_max']}}

def selftest():
 a='''<columns>\n<column>\n**Nível:** 17\n### Vida: 240/309\n### Alma: 150/273 (30 comprometidos)\n</column>\n<column>\n**Inteligência:** 8\n**Sabedoria:** 9 (+2 título)\n</column>\n</columns>\n<table><tr></tr></table>\n<details>OLD **Nível:** 16</details>\n<page url="child">C</page>'''
 cfg=column_config();src=TargetSource('fixture1',LAB,'v1','COLUMN_TABLE','R1')
 fields=parse_sections(a,cfg);assert fields['level']['value']=='17' and fields['sab']['value']=='9'
 assert fields['hp']['value']=='309' and fields['hp']['resource_current']=='240'
 w=prepare_write(target=src,body=a,config=cfg,changes={'int':'10'},expected_version='v1',authorized=True)
 b=a.replace('**Inteligência:** 8','**Inteligência:** 10',1);assert compare_after(a,b,w)['structure_preserved']
 obj={'normal':{'level':1},'locks':{'ff':100},'resources':{'hp_max':23,'pa_max':34}}
 blob=json.dumps(obj,ensure_ascii=False,separators=(',',':'))
 c='### R125 COMPOSITE ACTIVE\n```json\n'+blob+'\n```\n<details>IMMUTABLE</details>'
 src2=TargetSource('fixture2',LAB,'v2','SECTION_JSON','R2')
 cfg2=json_config();assert parse_sections(c,cfg2)['ff']['value']==100
 w2=prepare_write(target=src2,body=c,config=cfg2,changes={'level':2},expected_version='v2',authorized=True)
 after=c.replace(w2['edits'][0]['old_str'],w2['edits'][0]['new_str'],1)
 assert compare_after(c,after,w2)['structure_preserved']
 checks=6
 for fn in [lambda:prepare_write(target=src,body=a,config=cfg,changes={'int':'10'},expected_version='stale',authorized=True),lambda:prepare_write(target=src,body=a,config=cfg,changes={'int':'10'},expected_version='v1',authorized=False),lambda:prepare_write(target=src,body=a+'\n**Inteligência:** 8',config=cfg,changes={'int':'10'},expected_version='v1',authorized=True),lambda:compare_after(a,b+'CHANGED',w)]:
  try:fn()
  except Hold:checks+=1
  else:raise AssertionError('unsafe accepted')
 return {'checks':checks,'interpreted_fixture_formats':['COLUMN_TABLE','SECTION_JSON'],'actual_writes_this_module':0,'native_block_id_claim':False}
if __name__=='__main__':print(json.dumps(selftest(),ensure_ascii=False))
