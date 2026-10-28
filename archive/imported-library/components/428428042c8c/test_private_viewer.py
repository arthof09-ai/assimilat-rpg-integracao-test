import asyncio,copy,json,pathlib
from playwright.async_api import async_playwright
root=pathlib.Path(__file__).parent
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=await b.new_page(viewport={'width':390,'height':844});errors=[];requests=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda req:requests.append(req.url))
  await page.set_content((root/'TIMELINE_VLAB_R205_MESTRE_ONLY_TEST19.html').read_text())
  checks=[]
  async def ok(name,cond):
   assert cond,name;checks.append(name)
  await ok('script API loaded',await page.evaluate('typeof window.__r205TEST==="object"'))
  await ok('starts empty', 'Aguardando arquivo' in await page.locator('#status').inner_text())
  source=root/'VLAB_R205_TIMELINE_REAL_MESTRE_ONLY.json'
  await page.locator('#file').set_input_files(str(source))
  await page.wait_for_function('window.__r205TEST.caseCount()===20')
  await ok('20 cases loaded',await page.evaluate('window.__r205TEST.caseCount()===20'))
  summary=await page.evaluate('window.__r205TEST.counts()')
  await ok('945 actual commit rows',summary['commits']==945)
  await ok('2812 inner records',summary['innerEventsTotal']==2812)
  await ok('462 attack receipt rows',summary['attackRows']==462)
  await ok('detail no 2D invented', 'Coordenada' not in await page.locator('#detail').inner_text())
  before=await page.evaluate('window.__r205TEST.selected().seq')
  await page.locator('#next').click()
  await ok('next advances event',await page.evaluate('window.__r205TEST.selected().seq')==before+1)
  await page.locator('#prev').click()
  await ok('prev restores event',await page.evaluate('window.__r205TEST.selected().seq')==before)
  await page.locator('#case').select_option('19')
  await ok('last case selected',await page.evaluate('window.__r205TEST.selected().seq')==1)
  obj=json.loads(source.read_text());bad=copy.deepcopy(obj);bad['cases'][0]['events'][1]['seq']=1
  await ok('reject regress in seq',not await page.evaluate('(d)=>window.__r205TEST.validate(d)',bad))
  bad=copy.deepcopy(obj);bad['cases'][0]['events'][1]['prevHash']='0'*64
  await ok('reject broken chain',not await page.evaluate('(d)=>window.__r205TEST.validate(d)',bad))
  bad=copy.deepcopy(obj);bad['source']['sha256']='missing'
  await ok('reject malformed source sha',not await page.evaluate('(d)=>window.__r205TEST.validate(d)',bad))
  bad=copy.deepcopy(obj);bad['scope']='PARTY'
  await ok('reject non-master scope',not await page.evaluate('(d)=>window.__r205TEST.validate(d)',bad))
  await ok('no JS errors',not errors)
  await ok('no network requests',not requests)
  await page.screenshot(path=str(root/'TIMELINE_R205_390x844_PRIVATE.png'),full_page=True)
  print('PRIVATE TIMELINE',len(checks),'/',len(checks),'PASS')
  await b.close()
asyncio.run(main())
