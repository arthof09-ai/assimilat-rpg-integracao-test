"""R132 conservative structural span selector for Notion enhanced markdown TEST replicas.
It NEVER treats line indexes as physical block IDs. Connector lacks UUID access.
The wrapper handles version revalidation, one exact unique match, before/after
context, ancestor heading, typed region, and readback. No Notion credentials.
"""
from __future__ import annotations
from dataclasses import dataclass,asdict
import hashlib
class Hold(ValueError):pass
LAB='3fbc2b324ede804a95fafcb7b293c92c'
def digest(s:str):return hashlib.sha256(s.encode('utf-8')).hexdigest()

def between(page_text:str):
 if '<content>' not in page_text or '</content>' not in page_text:raise Hold('NO_NATIVE_CONTENT_BOUNDARY')
 return page_text.split('<content>',1)[1].split('</content>',1)[0]

@dataclass(frozen=True)
class Selection:
 target_id:str
 target_version:str
 literal:str
 literal_sha256:str
 before_sha256:str
 region_start:str
 region_end:str
 occurrence_count:int
 scope_sha256:str
 line_locator_hint:str
 native_block_uuid:None=None

def select(*,body:str,target_id:str,version:str,literal:str,region_start:str,region_end:str,preceding_context:str='',following_context:str=''):
 if not all((body,target_id,version,literal,region_start,region_end)):raise Hold('MISSING_IDENTIFIER_OR_SCOPE')
 if body.count(region_start)!=1:raise Hold('ANCESTOR_AMBIGUOUS')
 rest=body.split(region_start,1)[1]
 if rest.count(region_end)<1:raise Hold('REGION_END_MISSING')
 region=rest.split(region_end,1)[0]
 if region.count(literal)!=1:raise Hold('LITERAL_NOT_UNIQUE_IN_REGION')
 if body.count(literal)!=1:raise Hold('LITERAL_REPEATED_GLOBALLY')
 if preceding_context and preceding_context not in region.split(literal,1)[0][-350:]:raise Hold('PRECEDING_CONTEXT_DIFFERENT')
 if following_context and following_context not in region.split(literal,1)[1][:350]:raise Hold('FOLLOWING_CONTEXT_DIFFERENT')
 return Selection(target_id,version,literal,digest(literal),digest(body),region_start,region_end,1,digest(region),f'root-page text hint only / line {body[:body.index(literal)].count(chr(10))+1}')

def preflight(sel:Selection,*,page_id:str,version:str,body:str,replacement:str,parent_id:str,authorized:bool):
 if not authorized or parent_id!=LAB:raise Hold('WRITER_OR_PARENT_FORBIDDEN')
 if page_id!=sel.target_id or version!=sel.target_version:raise Hold('STALE_VERSION_OR_WRONG_PAGE')
 if digest(body)!=sel.before_sha256:raise Hold('SOURCE_BODY_CHANGED')
 if body.count(sel.literal)!=1 or replacement==sel.literal or not replacement:raise Hold('NOOP_OR_DUPLICATE_LITERAL')
 if sel.native_block_uuid is not None:raise Hold('PHANTOM_NATIVE_BLOCK_ID')
 return {'old_str':sel.literal,'new_str':replacement}

def compare_structure(before:str,after:str,*,old:str,new:str):
 expected=before.replace(old,new,1)
 if expected!=after:return {'result':'HOLD_UNEXPECTED_WRITE','only_expected_edit':False}
 tokens=['<columns>','</columns>','<table','</table>','<tr>','</tr>','<details','</details>','<page url=','<mention-page','notion-file-block://']
 metrics={k:{'before':before.count(k),'after':after.count(k)} for k in tokens}
 return {'result':'PASS_STRUCTURAL_ONLY','only_expected_edit':True,'metrics':metrics,'tokens_preserved':all(x['before']==x['after'] for x in metrics.values()),'before_hash':digest(before),'after_hash':digest(after)}

def checks():
 b='TITLE\n<columns>\n <column>\n Header\n **Field:** 16\n\told field\n </column>\n</columns>\n<details>\n Hidden Field 16\n</details>'
 s=select(body=b,target_id='ID',version='v1',literal='**Field:** 16',region_start='Header',region_end='</column>',preceding_context='',following_context='old field')
 count=0
 def ck(v):
  nonlocal count
  assert v;count+=1
 ck(s.occurrence_count==1)
 ck(preflight(s,page_id='ID',version='v1',body=b,replacement='**Field:** 17',parent_id=LAB,authorized=True)['new_str']=='**Field:** 17')
 ck(compare_structure(b,b.replace('**Field:** 16','**Field:** 17'),old='**Field:** 16',new='**Field:** 17')['tokens_preserved'])
 for kw in [{'version':'v2'},{'page_id':'OTHER'},{'parent_id':'PARTY'},{'authorized':False},{'body':b+' changed'}]:
  d={'page_id':'ID','version':'v1','body':b,'replacement':'**Field:** 17','parent_id':LAB,'authorized':True};d.update(kw)
  try:preflight(s,**d)
  except Hold:ck(True)
  else:raise AssertionError('unsafe target accepted')
 for literal in ('missing','Field 16'):
  try:select(body=b,target_id='ID',version='v1',literal=literal,region_start='Header',region_end='</column>')
  except Hold:ck(True)
  else:raise AssertionError('ambiguous accepted')
 try:select(body=b+'\n**Field:** 16',target_id='ID',version='v1',literal='**Field:** 16',region_start='Header',region_end='</column>')
 except Hold:ck(True)
 else:raise AssertionError('duplicate accepted')
 ck(compare_structure(b,b.replace('**Field:** 16','**Field:** 17')+'!',old='**Field:** 16',new='**Field:** 17')['result']=='HOLD_UNEXPECTED_WRITE')
 return count
if __name__=='__main__':print('R132',checks(),'direct selector checks PASS')
