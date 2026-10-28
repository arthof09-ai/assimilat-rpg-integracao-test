import asyncio,pathlib,re,json,statistics
from playwright.async_api import async_playwright
from test_integrated import mount,ROOT
OLD=(ROOT.parent/'archive'/'TEST06_ORIGINAL.html').read_text()
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  report=[]
  for w,h in [(390,844),(360,740)]:
   old=await browser.new_page(viewport={'width':w,'height':h})
   await old.set_content(OLD)
   await old.evaluate('window.__arenaTest.reset(20)')
   for i in range(3):await old.locator('#units .unit').first.click()
   samples=[]
   for i in range(18):
    t=await old.evaluate('''(i) => {const b=document.querySelectorAll('#units .unit')[i%2];const t=performance.now();b.click();return performance.now()-t;}''',i)
    samples.append(t)
   omed=statistics.median(samples)
   await old.close()
   new=await browser.new_page(viewport={'width':w,'height':h})
   await mount(new)
   await new.select_option('#gridSize','20')
   for i in range(3):await new.evaluate('window.__tabletopTEST.render()')
   new_samples=await new.evaluate('''() => {let out=[];for(let i=0;i<18;i++){const b=document.querySelectorAll('#unitList .unitBtn')[i%2],t=performance.now();b.click();out.push(performance.now()-t);}return out;}''')
   nmed=statistics.median(new_samples)
   report.append({'viewport':f'{w}x{h}','test06_median_ms':round(omed,2),'test15_median_ms':round(nmed,2),'test06_samples':len(samples),'test15_samples':len(new_samples)})
   print(w,h,'old',omed,'new',nmed)
   await new.close()
  await browser.close()
 (ROOT.parent/'evidence'/'benchmark_vs_test06.json').write_text(json.dumps(report,indent=2))
if __name__=='__main__':asyncio.run(main())
