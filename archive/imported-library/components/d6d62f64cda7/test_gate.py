import sys,unittest,tempfile,json,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from source_fence import notion_id,source_registry,fence,sanitize_for_r26,wrap_native_result
REG=source_registry(ROOT/'fixtures/sources.json')
RET='836c2b324ede83e2aae6016379ef2135'
def comp(sid,query='',role=None,quote=None):
 x=REG[sid]
 return {'url':'https://app.notion.com/p/'+sid+query,'tipo':role or x['role'],
         'comparacao_mecanica':x['qualifier'],'source_anchor':quote if quote is not None else x['verbatim_anchor']}
class GateTests(unittest.TestCase):
 def test_registry_census(self):self.assertEqual(len(REG),13)
 def test_live_notional_anchor_snapshot_all_12(self):
  self.assertEqual(len(REG),13)
  for s in REG.values():
   self.assertTrue(s['anchor_match_readback'])
   self.assertEqual(s['anchor_checked_in_Notion_fetch_on'],'2026-10-21')
   self.assertIn('T',s['last_edited_at_from_Notion_fetch'])
 def test_source_without_anchor_proof_rejected(self):
  obj=json.loads((ROOT/'fixtures/sources.json').read_text())
  obj['sources'][0]['anchor_match_readback']=False
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'registry.json';f.write_text(json.dumps(obj))
   with self.assertRaisesRegex(ValueError,'NOT_VERIFIED'):source_registry(f)
 def test_uuid_normalize(self):
  u='https://app.notion.com/p/'+RET
  self.assertEqual(notion_id(u),RET)
  self.assertEqual(notion_id(u+'?pvs=204'),RET)
  self.assertEqual(notion_id(u+'?pvs=205'),RET)
  dashed=RET[:8]+'-'+RET[8:12]+'-'+RET[12:16]+'-'+RET[16:20]+'-'+RET[20:]
  self.assertEqual(notion_id('https://app.notion.com/p/'+dashed),RET)
 def test_urls_rejected(self):
  samples=['http://app.notion.com/p/'+RET, 'https://other.com/p/'+RET,
   'https://app.notion.com.evil.com/p/'+RET,'https://user@app.notion.com/p/'+RET,
   'https://app.notion.com:443/p/'+RET,'https://app.notion.com/p/'+RET+'#x',
   'https://app.notion.com/p/'+RET+'?name=RankBronze',
   'https://app.notion.com/p/'+RET+'?pvs=0',
   'https://app.notion.com/p/'+RET+'/../', 'https://app.notion.com/p/'+RET+'?pvs=204&pvs=205',
   'https://app.notion.com/%70/'+RET, 'https://app.notion.com/p/'+RET+'\\no',
   'https://app.notion.com/p/'+RET+'\n', 'https://app.notion.com/p/'+RET.upper()+'?x=y',
   'https://app.notion.com/p/'+RET+'?pvs=204#fragment', 'https://app.notion.com/p/'+('f'*32)]
  for url in samples:
   if url.endswith('/'+('f'*32)):continue # Valid unknown UUID: tested by missing-registry test
   with self.subTest(url=url),self.assertRaises(ValueError):notion_id(url)
 def test_collisions_are_one(self):
  a=fence([comp(RET,'?pvs=204'),comp(RET,'?pvs=205')],REG,effect_mechanism='REACTIVE_FIRE_SAVE_AT_RANGE')
  self.assertEqual(len(a.unique_sources),1)
  self.assertIn('UUID_DUPLICATE_VARIANT_QUERY',a.reasons)
 def test_tento_mirror_pages_not_two_evidences(self):
  a='d3fc2b324ede83c3a1bb01356904ce06'
  b='33fc2b324ede830284c1819bfe775d2c'
  v=fence([comp(a),comp(b)],REG,effect_mechanism='REACTIVE_FIRE_SAVE_AT_RANGE')
  self.assertEqual(len(v.unique_sources),1)
  self.assertIn('MIRROR_TEXT_REPRESENTATION_NOT_INDEPENDENT',v.reasons)
 def test_mirror_reversed(self):
  a='d3fc2b324ede83c3a1bb01356904ce06'
  b='33fc2b324ede830284c1819bfe775d2c'
  v=fence([comp(b),comp(a)],REG,effect_mechanism='REACTIVE_FIRE_SAVE_AT_RANGE')
  self.assertEqual(len(v.unique_sources),1)
 def test_collision_can_not_fake_type(self):
  a=fence([comp(RET),comp(RET,'?pvs=206',role='vivo')],REG,effect_mechanism='REACTIVE_FIRE_SAVE_AT_RANGE')
  self.assertEqual(len(a.unique_sources),1)
 def test_invalid_role(self):
  x=fence([comp(RET,role='vivo')],REG,effect_mechanism='REACTIVE_FIRE_SAVE_AT_RANGE')
  self.assertFalse(x.eligible)
 def test_missing_source(self):
  x=comp(RET);x['url']='https://app.notion.com/p/'+'f'*32
  a=fence([x],REG,effect_mechanism='REACTIVE_FIRE_SAVE_AT_RANGE')
  self.assertFalse(a.eligible)
 def test_missing_anchor_holds_source(self):
  x=comp(RET);x.pop('source_anchor')
  self.assertFalse(fence([x],REG,effect_mechanism='REACTIVE_FIRE_SAVE_AT_RANGE').eligible)
 def test_false_quote(self):
  a=fence([comp(RET,quote='some invented quote')],REG,effect_mechanism='REACTIVE_FIRE_SAVE_AT_RANGE')
  self.assertFalse(a.eligible)
 def test_no_comparison(self):
  x=comp(RET);x['comparacao_mecanica']='vago'
  self.assertFalse(fence([x],REG,effect_mechanism='REACTIVE_FIRE_SAVE_AT_RANGE').eligible)
 def test_distinct_sources_can_be_advisory(self):
  x=fence([comp(RET),comp('3f2c2b324ede815498cddb7844245f7e')],REG,effect_mechanism='REACTIVE_FIRE_SAVE_AT_RANGE')
  self.assertTrue(x.eligible)
  self.assertEqual(len(x.unique_sources),2)
  self.assertFalse(x.direct_sources)
  self.assertEqual(x.state,'EVIDENCE_FOR_ADVISORY_ONLY')
 def test_fenced_has_canonical_url(self):
  a=fence([comp(RET,'?pvs=204')],REG,effect_mechanism='REACTIVE_FIRE_SAVE_AT_RANGE')
  self.assertEqual(a.sanitized_comparators[0]['url'],'https://app.notion.com/p/'+RET)
 def test_empty_input(self):
  a=fence([],REG,effect_mechanism='NONE')
  self.assertFalse(a.eligible)
  self.assertIn('ZERO_USABLE_RESEARCH',a.reasons)
 def test_research_reject_empty(self):
  y=sanitize_for_r26('X','Prata','justification',[],REG,'FOO')
  self.assertEqual(y['pesquisa'],{})
 def test_no_rank_automatically(self):
  x=fence([comp(RET)],REG,effect_mechanism='REACTIVE_FIRE_SAVE_AT_RANGE')
  result=wrap_native_result({'r26':{'pareceres':[{'habilidade':'x','rank_efeito_recomendado':'Prata','confianca':'MEDIA','estado':'E3'}]},'some_pa_daily':30},x)
  self.assertIsNone(result['canonical_RE'])
  self.assertIsNone(result['authorized_pa_use'])
  self.assertIsNone(result['authorized_pa_daily'])
  self.assertNotIn('native_r26',result)
 def test_zero_direct_adjudicated(self):
  for sid in REG:
   x=fence([comp(sid)],REG,effect_mechanism=REG[sid]['mechanism'])
   self.assertEqual(x.direct_sources,())
 def test_registry_refuse_fake_adjudication(self):
  obj=json.loads((ROOT/'fixtures/sources.json').read_text())
  obj['sources'][0]['effect_rank_adjudicated']=True
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'registry.json';f.write_text(json.dumps(obj))
   with self.assertRaisesRegex(ValueError,'NO_INDEPENDENT_EFFECT_RANK_VERIFIED'):source_registry(f)
 def test_registry_refuse_duplicate(self):
  obj=json.loads((ROOT/'fixtures/sources.json').read_text())
  obj['sources'].append(obj['sources'][0])
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'registry.json';f.write_text(json.dumps(obj))
   with self.assertRaisesRegex(ValueError,'DUPLICATE'):source_registry(f)
 def test_research_template_preserves_prompt(self):
  x=sanitize_for_r26('Teste','Bronze','Teste comparativo de elemento sob limitação e sem duração canônica conhecida.',[comp(RET)],REG,'REACTIVE_FIRE_SAVE_AT_RANGE')
  self.assertEqual(x['pesquisa']['Teste']['rank_sugerido'],'Bronze')
  self.assertTrue(x['fence'].eligible)
 def test_sources_no_gold(self):
  raw=(ROOT/'fixtures/sources.json').read_text().lower()
  for k in ['r45_frozen','oracle.json','predict_peer_score']:
   self.assertNotIn(k,raw)
 def test_source_claims_not_e0(self):
  self.assertEqual(sum(x['effect_rank_adjudicated'] for x in REG.values()),0)
if __name__=='__main__':unittest.main()
