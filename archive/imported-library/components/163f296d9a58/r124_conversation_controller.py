"""R124 ChatGPT-side planning controller, additive to R95/R105/R107/R117.
This module does NOT independently make Notion API calls. Tool adapter receives
its prepared envelope after source and target have been re-opened and validated.
Not a replacement chatbot or production writer.
"""
from __future__ import annotations
import re, hashlib, json
from dataclasses import dataclass
LAB='3fbc2b324ede804a95fafcb7b293c92c'
CONSUMED=set() # persisted registry must be injected from the currently fetched page
class Hold(ValueError):pass
@dataclass(frozen=True)
class Target:
 id:str; name:str; parent:str; version:str; synthetic:bool; status:str

def parse_request(text):
 t=text.lower().strip()
 if re.search(r'\b(cancel|cancele|cancelar|não confirm|nao confirm)\b',t):return {'intent':'CANCEL','writes':0}
 if re.search(r'(nível|nivel|level)\s*down|corrigir\s+atribut',t):return {'intent':'LEVEL_DOWN','needs':['explicit_attribute_corrections','confirmation']}
 if re.search(r'(transform|esp[ií]rito)',t) and not re.search(r'evolu|suba|aument|níve|nivel',t):return {'intent':'TRANSFORM_PREVIEW','needs':['source_spirit','scene','rest','cost']}
 if re.search(r'\b(equip|equipamento|anel|grim[oó]rio)\b',t) and not re.search(r'evolu|suba|aument|níve|nivel',t):return {'intent':'INSPECT_LAYERS','needs':['equipment_state']}
 if re.search(r'\b(resultad|status|transa[cç][aã]o)\b',t):return {'intent':'QUERY_TRANSACTION','writes':0}
 if re.search(r'\b(revisar|altere a distribui|mude os pontos)\b',t):return {'intent':'REVISE_PREVIEW','needs':['new_allocations']}
 if re.search(r'\b(antecip|prever|pr[eé]via|simular)\b',t):return {'intent':'PREVIEW','writes':0}
 if re.search(r'\b(suba|evolu|aument|level up)\b',t):
  m=re.search(r'\b(\d+)\s*(?:n[ií]ve[ií]s|levels?)',t)
  n=int(m.group(1)) if m else 1
  if n<1 or n>25:raise Hold('INVALID_LEVEL_COUNT')
  return {'intent':'LEVEL_UP','levels':n,'needs':['per_level_allocations','growth_choices','confirmation']}
 return {'intent':'UNKNOWN','needs':['intent']}

def select_target(name,registry):
 hits=[t for t in registry if t.name.casefold()==name.casefold()]
 if len(hits)!=1:raise Hold('TARGET_NOT_UNIQUE_OR_NOT_FOUND')
 t=hits[0]
 if t.parent!=LAB or not t.synthetic:raise Hold('TARGET_NOT_AUTHORIZED_TEST_FIXTURE')
 if not t.id or not t.version or not t.status:raise Hold('TARGET_VERSION_OR_STATUS_UNKNOWN')
 return t

def prepare(text,*,target_name,registry,source_version,live_source_version,allocation_plan=None,growth=None,observed_event=None,authorization=None):
 intent=parse_request(text);target=select_target(target_name,registry)
 if intent['intent']=='CANCEL':return {'status':'CANCELED_NO_WRITE','target':target.id,'writes':0}
 if not source_version or source_version!=live_source_version:raise Hold('STALE_SOURCE')
 if target.status.startswith(('COMMITTED','RECOVERED')):
  if observed_event:return {'status':'NOOP_CONSUMED','target':target.id,'event':observed_event,'writes':0}
  raise Hold('TARGET_ALREADY_CONSUMED')
 if intent['intent'] in ('LEVEL_UP','LEVEL_DOWN'):
  if not allocation_plan or not growth:return {'status':'AWAITING_CHOICES','missing':['allocation_per_level','growth'],'writes':0}
  if intent.get('levels',len(allocation_plan))!=len(allocation_plan):raise Hold('PER_LEVEL_ALLOCATION_COUNT_INVALID')
  if authorization not in ('LAB_TEST_EXPLICIT_FROM_MESTRE',):return {'status':'AWAITING_AUTHORIZATION','writes':0}
 return {'status':'PREVIEW_READY_NO_WRITE','intent':intent,'target_id':target.id,'target_version':target.version,'source_version':source_version,'input':{'allocations':allocation_plan,'growth':growth},'authorization':authorization,'writer':'NATIVE_CONNECTOR_AFTER_REOPEN_ONLY','writes':0}

if __name__=='__main__':
 reg=[Target('fixture-a','FICHA TEST A',LAB,'v1',True,'PREPARED'),Target('fixture-b','FICHA TEST B',LAB,'v2',True,'PREPARED')]
 checks=0
 def ck(x):
  global checks
  assert x; checks+=1
 ck(select_target('FICHA TEST B',reg).id=='fixture-b')
 ck(parse_request('Suba 3 níveis')['levels']==3)
 ck(parse_request('Corrigir atributos sem perder nível')['intent']=='LEVEL_DOWN')
 ck(parse_request('Simular transformação')['intent']=='TRANSFORM_PREVIEW')
 ck(parse_request('Inspecionar equipamento')['intent']=='INSPECT_LAYERS')
 ck(parse_request('Cancelar prévia')['intent']=='CANCEL')
 ck(prepare('Suba um nível',target_name='FICHA TEST B',registry=reg,source_version='v',live_source_version='v')['status']=='AWAITING_CHOICES')
 ck(prepare('Suba um nível',target_name='FICHA TEST B',registry=reg,source_version='v',live_source_version='v',allocation_plan=[{'SAB':2}],growth=['FIXED60'],authorization='LAB_TEST_EXPLICIT_FROM_MESTRE')['target_id']=='fixture-b')
 ck(prepare('Cancelar',target_name='FICHA TEST A',registry=reg,source_version='v',live_source_version='v')['status']=='CANCELED_NO_WRITE')
 for kw in [{'source_version':'v','live_source_version':'old'}, {'source_version':'v','live_source_version':'v','allocation_plan':[{'SAB':2}],'growth':['FIXED60'],'authorization':'BAD'}]:
  try:
   v=prepare('Suba um nível',target_name='FICHA TEST A',registry=reg,**kw)
   ck(v['status']=='AWAITING_AUTHORIZATION')
  except Hold:ck('live_source_version' in kw and kw['live_source_version']=='old')
 try:select_target('FICHA TEST B',[Target('other','FICHA TEST B','PARTY', 'v2',True,'PREPARED')])
 except Hold:ck(True)
 else:raise AssertionError('Party writer enabled')
 print(f'R124: {checks}/{checks} direct checks PASS; dynamic registry, no production writer')
