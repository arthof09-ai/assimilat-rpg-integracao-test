import asyncio,pathlib,json
from playwright.async_api import async_playwright
from test_integrated import mount
out=pathlib.Path(__file__).resolve().parents[1]/'evidence'
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=await b.new_page(viewport={'width':390,'height':844},accept_downloads=True);await mount(page)
  await page.screenshot(path=str(out/'TEST22_MOBILE_HOME_390.png'),full_page=True)
  old=await page.evaluate('window.__tabletopTEST.state()');await page.locator('#newScene').click()
  await page.locator('#restore').set_input_files({'name':'backup_old.json','mimeType':'application/json','buffer':json.dumps(old,ensure_ascii=False).encode()})
  await page.wait_for_timeout(150);await page.screenshot(path=str(out/'TEST21_STALE_BACKUP_REVIEW_390.png'),full_page=True)
  await page.locator('#restoreReviewCancel').click()
  current=await page.evaluate('window.__tabletopTEST.state()');nextc=json.loads(json.dumps(current));nextc['scenes'][0]['name']='backup_from_another_device'
  await page.evaluate('''w=>{const s=localStorage,set=s.setItem.bind(s),get=s.getItem.bind(s);let wrote=false;s.setItem=(k,v)=>{set(k,v);wrote=true};s.getItem=k=>{if(wrote)throw Error('readback blocked');return get(k)};try{window.__tabletopTEST.restoreCandidate(w)}catch(e){}}''',nextc)
  await page.screenshot(path=str(out/'TEST20_UNCERTAIN_STORAGE_ALERT_390.png'),full_page=True)
  await b.close()
asyncio.run(main())
