import asyncio,json,statistics,pathlib
from playwright.async_api import async_playwright
from test_integrated import mount,ROOT
OUT=ROOT.parent/'evidence'
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  all_results=[]
  for width,height in [(390,844),(360,740)]:
   page=await b.new_page(viewport={'width':width,'height':height});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   await mount(page)
   await page.locator('[data-mode="measure"]').click()
   await page.locator('.tile[data-xy="0,0"]').click();await page.locator('.tile[data-xy="3,4"]').click()
   await page.screenshot(path=str(OUT/f'TEST26_RULER_{width}x{height}.png'),full_page=False)
   samples={}
   for n in [7,20]:
    await page.select_option('#gridSize',str(n))
    await page.evaluate('''() => {const a=window.__tabletopTEST;for(let i=0;i<12;i++)a.render()}''')
    v=await page.evaluate('''()=>{const a=window.__tabletopTEST,ls=[];for(let i=0;i<80;i++){a.render();ls.push(a.lastRenderMs())}return ls}''')
    samples[f'{n}x{n}']={'n':len(v),'median_ms':round(statistics.median(v),3),'p95_ms':round(sorted(v)[int(len(v)*.95)-1],3)}
   assert not errors,errors
   all_results.append({'viewport':f'{width}x{height}','render_ms':samples,'JS_errors':errors})
   await page.close()
  await b.close()
 (OUT/'TEST26_BENCHMARK.json').write_text(json.dumps(all_results,ensure_ascii=False,indent=2))
 print(json.dumps(all_results,ensure_ascii=False,indent=2))
asyncio.run(main())
