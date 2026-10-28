import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
root=Path(__file__).parent
html=(root/'ARENA_TEST36_RECIBOS_VISUAIS_SINTETICOS_OFFLINE.html').read_text()
async def test():
 results=[]; shots=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for width,height in [(360,740),(390,844),(412,915)]:
   page=await browser.new_page(viewport={'width':width,'height':height})
   errors=[];requests=[]
   page.on('pageerror',lambda e: errors.append(str(e)))
   page.on('request',lambda r: requests.append(r.url))
   await page.set_content(html,wait_until='load');await page.wait_for_timeout(180)
   checks={}
   checks['49_cells']=await page.locator('#board .tile').count()==49 or await page.locator('#board').locator('[data-cell]').count()==49
   checks['main_application_loaded']=await page.locator('#viewport').count()==1
   checks['entry_button_visible']=await page.locator('#receiptOpen').is_visible()
   await page.locator('#receiptOpen').click()
   checks['dialog_open']=await page.locator('#receiptPanel').is_visible()
   checks['three_states']=await page.locator('#receiptPanel [data-mode]').count()==3
   for mode in ['ACCEPTED','REJECTED','UNKNOWN']:
    await page.locator(f'[data-mode="{mode}"]').click()
    checks[mode.lower()+'_rendered']=mode in await page.locator('#receiptStatus').inner_text()
   text=await page.locator('#receiptTrace').inner_text()
   checks['no_transmission']='NOT_SENT' in text
   checks['no_mechanics']='NOT_EXECUTED' in text
   checks['bad_schema_rejected']=await page.evaluate('window.__receiptFixtureTest.validate({...window.__receiptFixtureTest.fixtures.ACCEPTED,adminPassword:"hidden"})===false')
   checks['no_network']=not requests
   checks['no_js_errors']=not errors
   await page.screenshot(path=str(root/f'PROVA_RECIBOS_{width}x{height}.png'),full_page=False)
   await page.locator('#receiptClose').click()
   checks['dialog_closes']=not await page.locator('#receiptPanel').is_visible()
   results.append({'viewport':f'{width}x{height}','tests':checks,'pass':sum(checks.values()),'total':len(checks),'errors':errors,'requests':requests})
   print(width,height,sum(checks.values()),len(checks),checks,flush=True)
   await page.close()
  await browser.close()
 (root/'RESULTADOS_CHROMIUM.json').write_text(json.dumps({'results':results,'pass':sum(z['pass'] for z in results),'total':sum(z['total'] for z in results),'tested_environment':'Chromium Linux Playwright page.set_content, not Android phone','note':'No server, no official mechanics, no Party data'},indent=2,ensure_ascii=False))
 if any(z['pass']!=z['total'] for z in results):exit(1)
asyncio.run(test())
