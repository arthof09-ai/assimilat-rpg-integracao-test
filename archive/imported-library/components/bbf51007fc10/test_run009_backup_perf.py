import asyncio,json, pathlib,statistics,tempfile,random
from playwright.async_api import async_playwright
from test_run009_concurrency_markers import mount,sc
OUT=pathlib.Path(__file__).resolve().parents[1]/'evidence';OUT.mkdir(parents=True,exist_ok=True)
async def check_case(browser,w,h):
 page=await browser.new_page(viewport={'width':w,'height':h},accept_downloads=True)
 await mount(page);checks=[]
 async def ck(label,ok):
  if not ok:raise AssertionError(f'{w}x{h} {label}')
  checks.append(label)
 await page.locator('[data-mode="mark"]').click()
 await page.evaluate('window.__tabletopTEST.cell(4,4)')
 await page.locator('#markerText').fill('Marco persistente')
 await page.locator('#markerSave').click()
 before=await page.evaluate('window.__tabletopTEST.state()')
 await ck('marker in valid workspace',await page.evaluate('window.__tabletopTEST.validateWorkspace(window.__tabletopTEST.state())'))
 # UI backup/restore round trip with the built-in file input.
 file=OUT/f'backup_markers_{w}.json';file.write_text(json.dumps(before,ensure_ascii=False))
 await page.evaluate('window.__tabletopTEST.cell(4,4)');await page.locator('#markerDelete').click()
 await ck('removed before restore',(await sc(page))['markers']==[])
 page.once('dialog',lambda dialog:asyncio.create_task(dialog.accept()))
 await page.locator('#restore').set_input_files(str(file))
 await page.wait_for_timeout(200)
 await ck('backup restores visual marker',len((await sc(page))['markers'])==1)
 await ck('restore persisted after readback','restaurado' in (await page.locator('#storageStatus').inner_text()).lower())
 await ck('restore does not change PA',(await sc(page))['units'][0]['pa']==60)
 # Simulate page reload with stored physical bytes injected before mounting a brand new JS context.
 from test_run009_concurrency_markers import raw,KEY
 stored=await raw(page)
 other=await browser.new_page(viewport={'width':w,'height':h});await mount(other,stored)
 await ck('reload restores markers',len((await sc(other))['markers'])==1)
 await ck('reload preserves revision',(await other.evaluate('window.__tabletopTEST.state()'))['revision']==json.loads(stored)['revision'])
 # Resize drops marker out of new bounds without losing other valid data.
 await other.select_option('#gridSize','20')
 await other.evaluate('window.__tabletopTEST.mode("mark")')
 await other.evaluate('window.__tabletopTEST.cell(19,19)')
 await other.locator('#markerText').fill('Extremo TEST')
 await other.locator('#markerSave').click()
 await ck('20x20 marker added',len((await sc(other))['markers'])==2)
 other.once('dialog',lambda d:asyncio.create_task(d.dismiss()))
 await other.select_option('#gridSize','7')
 await ck('cancel resize preserves markers',len((await sc(other))['markers'])==2)
 other.once('dialog',lambda d:asyncio.create_task(d.accept()))
 await other.select_option('#gridSize','7')
 await ck('out of range marker removed by resize',len((await sc(other))['markers'])==1)
 await ck('resize state valid',await other.evaluate('window.__tabletopTEST.validateWorkspace(window.__tabletopTEST.state())'))
 # visual layer independent; FOV and ruler coexist without modifying markers.
 await other.locator('#layerFov').check()
 await other.evaluate('window.__tabletopTEST.mode("measure")')
 await other.evaluate('window.__tabletopTEST.cell(0,0)')
 await other.evaluate('window.__tabletopTEST.cell(3,4)')
 await ck('ruler geometric unaffected','Manhattan 7' in await other.locator('#rulerStatus').inner_text())
 await ck('marker unaffected by ruler',len((await sc(other))['markers'])==1)
 await ck('FOV still enabled',(await sc(other))['fovEnabled'])
 # 40 marker capacity + guarded overflow.
 await other.evaluate('window.__tabletopTEST.mode("mark")')
 count0=len((await sc(other))['markers']);
 coords=[(x,y) for y in range(7) for x in range(7) if (x,y)!=(4,4)]
 for x,y in coords[:40-count0]:
  await other.evaluate('([x,y])=>window.__tabletopTEST.openMarkerDialog(x,y)',[x,y])
  await other.locator('#markerText').fill('M'+str(x)+'.'+str(y))
  await other.locator('#markerSave').click()
 await ck('marker count capped at 40',len((await sc(other))['markers'])==40)
 x,y=coords[40-count0]
 await other.evaluate('([x,y])=>window.__tabletopTEST.openMarkerDialog(x,y)',[x,y]);await other.locator('#markerText').fill('Overflow');await other.locator('#markerSave').click()
 await ck('marker overflow rejected',len((await sc(other))['markers'])==40 and 'Limite' in await other.locator('#markerFormError').inner_text())
 await other.locator('#markerCancel').click()
 # benchmark: force true render cycle, no Android claim.
 await other.select_option('#gridSize','20')
 await other.evaluate('window.__tabletopTEST.render()')
 measured=[]
 for i in range(35):
  measured.append(await other.evaluate('''() => {window.__tabletopTEST.render();return window.__tabletopTEST.lastRenderMs()}'''))
 await ck('render finite with 40 marks',all(0<=x<1000 for x in measured))
 await ck('marker SVG=40',await other.locator('#markerOverlay .visual-mark').count()==40)
 await ck('scroll width fits',await other.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
 await page.close();await other.close()
 return checks,{'medianMs':round(statistics.median(measured),2),'p95Ms':round(sorted(measured)[int(len(measured)*.95)],2),'renderCount':len(measured)}
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  out={}
  for wh in [(390,844),(360,740)]:
   c,m=await check_case(b,*wh);out[f'{wh[0]}x{wh[1]}']={'checks':c,'benchmark':m};print(wh,len(c),'PASS',m)
  await b.close()
  (OUT/'TEST_RUN009_BACKUP_PERF.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
  print('TOTAL',sum(len(v['checks']) for v in out.values()))
if __name__=='__main__':asyncio.run(main())
