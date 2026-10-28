import asyncio,json,re,pathlib
from playwright.async_api import async_playwright
ROOT=pathlib.Path('/mnt/data/tabletop_run009/baseline/public')
KEY='assim.tabletop.synthetic.workspace.v1'
async def mount(page,base=ROOT):
 html=(base/'index.html').read_text();css=(base/'styles.css').read_text();js=(base/'app.js').read_text()
 html=re.sub(r'<meta http-equiv="Content-Security-Policy"[^>]*>','',html).replace('<link rel="stylesheet" href="styles.css">','').replace('<script src="app.js" defer></script>','')
 await page.set_content(html)
 await page.evaluate('''() => {window.__store={}; Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem(k){return window.__store[k]??null},setItem(k,v){window.__store[k]=String(v)},removeItem(k){delete window.__store[k]}}});}''')
 await page.add_style_tag(content=css);await page.add_script_tag(content=js)
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  a,b=await browser.new_page(),await browser.new_page()
  await mount(a);await mount(b)
  await a.locator('[data-mode="wall"]').click();await a.evaluate('window.__tabletopTEST.cell(3,3)')
  a_raw=await a.evaluate(f'window.__store[{json.dumps(KEY)}]')
  await b.evaluate('([k,v])=>{window.__store[k]=v}',[KEY,a_raw])
  await b.locator('[data-mode="wall"]').click();await b.evaluate('window.__tabletopTEST.cell(4,4)')
  b_raw=await b.evaluate(f'window.__store[{json.dumps(KEY)}]')
  ans={'source':'TEST26 original','test':'two independent JS pages with shared storage manually propagated (SIMULATED, not true storage event)','wall_A_committed': '3,3' in json.loads(a_raw)['scenes'][0]['walls'],'wall_A_survived_B': '3,3' in json.loads(b_raw)['scenes'][0]['walls'],'wall_B_committed':'4,4' in json.loads(b_raw)['scenes'][0]['walls'],'B_message':await b.locator('#message').inner_text()}
  print(json.dumps(ans,ensure_ascii=False,indent=2))
  await browser.close()
if __name__=='__main__':asyncio.run(main())
