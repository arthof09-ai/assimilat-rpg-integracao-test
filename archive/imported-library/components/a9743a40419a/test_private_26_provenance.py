"""TEST26 private timeline checks: local structure != cryptographic source authorization."""
import asyncio,json,copy,pathlib
from playwright.async_api import async_playwright
ROOT=pathlib.Path(__file__).parent
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=await b.new_page(viewport={'width':390,'height':844})
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  await page.set_content((ROOT/'TIMELINE_VLAB_R205_MESTRE_ONLY_TEST19.html').read_text())
  data=json.loads((ROOT/'VLAB_R205_TIMELINE_REAL_MESTRE_ONLY.json').read_text())
  labels=[]
  async def ck(label,value):
   assert value,label;labels.append(label)
  async def verify(d):return await page.evaluate('d=>window.__r205TEST.verifyStructure(d)',d)
  await ck('original structurally valid',(await verify(data))['ok'])
  await ck('counter 945',(await verify(data))['commits']==945)
  await ck('native 1425',(await verify(data))['native']==1425)
  await ck('added 1387',(await verify(data))['added']==1387)
  await ck('attacks 462',(await verify(data))['attacks']==462)
  forged=copy.deepcopy(data);forged['source']['sha256']='f'*64
  await ck('forged wellformed source accepted only structurally',(await verify(forged))['sourceStatus']=='SOURCE_UNVERIFIED')
  bad=copy.deepcopy(data);bad['summary']['innerEventsTotal']+=1
  await ck('tampered internal count rejected',not(await verify(bad))['ok'])
  bad=copy.deepcopy(data);bad['summary']['nativeEvents']+=1
  await ck('native count mismatch rejected',not(await verify(bad))['ok'])
  bad=copy.deepcopy(data);bad['summary']['attackRows']+=1
  await ck('attack count mismatch rejected',not(await verify(bad))['ok'])
  bad=copy.deepcopy(data);bad['summary']['databases']-=1
  await ck('database count mismatch rejected',not(await verify(bad))['ok'])
  bad=copy.deepcopy(data);bad['cases'][1]['id']=bad['cases'][0]['id']
  await ck('duplicate case ID rejected',not(await verify(bad))['ok'])
  bad=copy.deepcopy(data);bad['cases'][0]['events'][0]['addedCount']=-1
  await ck('negative event count rejected',not(await verify(bad))['ok'])
  await page.locator('#file').set_input_files(str(ROOT/'VLAB_R205_TIMELINE_REAL_MESTRE_ONLY.json'))
  await page.wait_for_function('window.__r205TEST.caseCount()===20')
  await ck('visible structure pass','STRUCTURE_VALID' in await page.locator('#provenance').inner_text())
  await ck('visible origin unverified','SOURCE_UNVERIFIED' in await page.locator('#provenance').inner_text())
  await ck('does not claim source verified','SOURCE_VERIFIED' not in await page.locator('#provenance').inner_text())
  await ck('no JS errors',not errors)
  print('PRIVATE_PROVENANCE',len(labels),'/',len(labels),'PASS')
  (ROOT/'test_private26_results.json').write_text(json.dumps({'total':len(labels),'tests':labels},ensure_ascii=False,indent=2))
  await b.close()
asyncio.run(main())
