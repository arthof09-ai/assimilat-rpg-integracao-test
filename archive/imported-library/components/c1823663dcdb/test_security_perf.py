import asyncio,json,pathlib,statistics
from playwright.async_api import async_playwright
from test_integrated import mount,ROOT
async def main():
 total=[];metrics=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  for w,h in [(390,844),(360,740)]:
   page=await browser.new_page(viewport={'width':w,'height':h})
   errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
   await mount(page)
   chk=[]
   async def ok(name,condition):
    if not condition: raise AssertionError((w,h,name))
    chk.append(name)
   a=lambda script:page.evaluate(script)
   await ok('empty tiles without tokens hidden',await page.locator('.tile .token:not([hidden])').count()==3)
   await page.select_option('#gridSize','20')
   await ok('20x20 only 3 tokens visible',await page.locator('.tile .token:not([hidden])').count()==3)
   # 30 renders on 20x20 in sandbox; report percentile p50/p95 from same browser process.
   samples=await a('''() => {let times=[];for(let i=0;i<30;i++){window.__tabletopTEST.render();times.push(window.__tabletopTEST.lastRenderMs());}return times;}''')
   median=statistics.median(samples);p95=sorted(samples)[int(.95*len(samples))-1]
   metrics.append({'viewport':f'{w}x{h}','median_render_ms':round(median,2),'p95_render_ms':round(p95,2),'max_render_ms':round(max(samples),2)})
   await ok('render measured 30 iterations',len(samples)==30)
   await ok('no NaN render',all(x>=0 and x<600 for x in samples))
   await ok('DOM 400 gridcells stable after rerender',await page.locator('.tile').count()==400)
   await ok('no empty token incorrectly shown',await page.locator('.tile .token:not([hidden])').count()==3)
   before=await a('window.__tabletopTEST.state()')
   viewport=page.locator('#viewport');r=await viewport.bounding_box();x=r['x']+r['width']*.4;y=r['y']+r['height']*.4
   # synthetic touch positions on viewport; no native phone tested.
   await a('''() => {const v=document.querySelector('#viewport');v.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,pointerId:41,pointerType:'touch',clientX:150,clientY:300}));v.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,pointerId:42,pointerType:'touch',clientX:210,clientY:300}));}''')
   await a('''() => {const v=document.querySelector('#viewport');v.dispatchEvent(new PointerEvent('pointermove',{bubbles:true,pointerId:42,pointerType:'touch',clientX:260,clientY:300}));v.dispatchEvent(new PointerEvent('pointercancel',{bubbles:true,pointerId:41,pointerType:'touch',clientX:150,clientY:300}));v.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,pointerId:42,pointerType:'touch',clientX:260,clientY:300}));}''')
   await ok('synthetic pinch changes zoom',int((await page.locator('#zoomLabel').inner_text()).split()[0])>=44)
   await ok('pinch does not move tokens',(await a('window.__tabletopTEST.state()'))==before)
   # adverse token name XSS input blocked while panel stays alive
   await page.locator('#newToken').click();await page.locator('#tokName').fill('<img src=x onerror=alert(1)>');await page.locator('#commitToken').click()
   await ok('unsafe token name rejected',len((await a('window.__tabletopTEST.scene()'))['units'])==3)
   await page.locator('#tokName').fill('OK TEST');await page.locator('#commitToken').click()
   await ok('safe name accepted',len((await a('window.__tabletopTEST.scene()'))['units'])==4)
   # JSON mutator attacks: reject odd flags, invalid colliding walls, duplicate scene IDs, huge array, script-like note safe via textarea
   await ok('reject forged source kind',not await a('''() => {let r=window.__tabletopTEST.makeReplay();r.source.kind='VLAB_TEST_EXPORT';return window.__tabletopTEST.validateReplay(r);}'''))
   await ok('reject duplicate walls',not await a('''() => {let r=window.__tabletopTEST.makeReplay();r.grid.walls=[[2,2],[2,2]];return window.__tabletopTEST.validateReplay(r);}'''))
   await ok('reject invalid JSON scene position',not await a('''() => {let w=window.__tabletopTEST.state();w.scenes[0].units[0].x=500;return window.__tabletopTEST.validateWorkspace(w);}'''))
   await ok('reject duplicate token IDs',not await a('''() => {let w=window.__tabletopTEST.state();w.scenes[0].units[1].id=w.scenes[0].units[0].id;return window.__tabletopTEST.validateWorkspace(w);}'''))
   await ok('reject too many scenes',not await a('''() => {let w=window.__tabletopTEST.state();w.scenes=Array(9).fill(w.scenes[0]);return window.__tabletopTEST.validateWorkspace(w);}'''))
   await ok('reject forged actor team',not await a('''() => {let w=window.__tabletopTEST.state();w.scenes[0].units[0].team='admin';return window.__tabletopTEST.validateWorkspace(w);}'''))
   await ok('reject unknown schema',not await a('''() => {let w=window.__tabletopTEST.state();w.schema='official.VLAB';return window.__tabletopTEST.validateWorkspace(w);}'''))
   await ok('no JS page errors',not errors)
   total+=chk
   print(f'{w}x{h}: {len(chk)} security/perf/gesture assertions PASS; render median={median:.2f}ms p95={p95:.2f}ms')
   await page.screenshot(path=str(ROOT.parent/'evidence'/f'security_mobile_{w}.png'),full_page=True)
   await page.close()
  await browser.close()
 print('TOTAL security/perf assertions',len(total))
 (ROOT.parent/'evidence'/'perf_security_results.json').write_text(json.dumps({'checks':len(total),'metrics':metrics},indent=2))
if __name__=='__main__':asyncio.run(main())
