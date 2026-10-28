import asyncio, json, sys
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).parent/'baseline/public'
html=(ROOT/'index.html').read_text();css=(ROOT/'styles.css').read_text();js=(ROOT/'app.js').read_text()
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=await b.new_page(viewport={'width':390,'height':844})
  import re
  raw=re.sub(r'<meta http-equiv="Content-Security-Policy"[^>]*>','',html).replace('<link rel="stylesheet" href="styles.css">','').replace('<script src="app.js" defer></script>','')
  await page.set_content(raw)
  await page.evaluate('''() => {const db={}; Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem(k){return db[k]??null},setItem(k,v){if(window.__quotaFailure)throw new DOMException('quota exceeded','QuotaExceededError');db[k]=String(v)},removeItem(k){delete db[k]}}});window.__TESTSTORE=db;}''')
  await page.add_style_tag(content=css);await page.add_script_tag(content=js)
  current=await page.evaluate('window.__tabletopTEST.state()');candidate=json.loads(json.dumps(current));candidate['scenes'][0]['name']='Cena importada TEST'
  await page.evaluate('window.__quotaFailure=true')
  page.once('dialog',lambda d:asyncio.create_task(d.accept()))
  await page.locator('#restore').set_input_files({'name':'backup.json','mimeType':'application/json','buffer':json.dumps(candidate).encode()})
  await page.wait_for_timeout(110)
  now=await page.evaluate('window.__tabletopTEST.state()')
  msg=await page.locator('#message').inner_text()
  print(json.dumps({'workspace_mutated_despite_storage_error':now!=current,'message':msg,'status':await page.locator('#storageStatus').inner_text()},ensure_ascii=False))
  assert now==current,'RED: original workspace changed despite setItem failure'
  assert 'restaurado' not in msg.lower(),'RED: false success message after failed storage'
  await b.close()
asyncio.run(main())
