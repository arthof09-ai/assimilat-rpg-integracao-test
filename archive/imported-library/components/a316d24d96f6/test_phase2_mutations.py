import asyncio,json,pathlib
from playwright.async_api import async_playwright
from test_run009_concurrency_markers import mount,JS
ROOT=pathlib.Path(__file__).resolve().parents[1]
SOURCES=[
 ('skip_coord_canonical',"if(!isCanonicalCoord(key,s.n)||where.has(key))","if(where.has(key))",'coord'),
 ('clear_redo_on_noop','future=redoBeforeNoop;return;','future=[];return;','redo'),
 ('leave_ruler_outside_grid','if(rulerSceneId!==s.id||rulerA&&!inside(rulerA.x,rulerA.y,s.n)||rulerB&&!inside(rulerB.x,rulerB.y,s.n))','if(rulerSceneId!==s.id)','ruler')
]
async def test(page,kind):
 if kind=='coord':return await page.evaluate("()=>{const w=window.__tabletopTEST.state();w.scenes[0].walls=['02,02'];return window.__tabletopTEST.validateWorkspace(w)}")
 if kind=='redo':
  await page.locator('[data-mode="wall"]').click();await page.evaluate('window.__tabletopTEST.cell(4,4)');await page.evaluate('window.__tabletopTEST.undo()');await page.locator('[data-mode="erase"]').click();await page.evaluate('window.__tabletopTEST.cell(6,6)');await page.evaluate('window.__tabletopTEST.redo()');return '4,4' not in (await page.evaluate('window.__tabletopTEST.scene()'))['walls']
 if kind=='ruler':
  await page.select_option('#gridSize','20');await page.locator('[data-mode="measure"]').click();await page.evaluate('window.__tabletopTEST.cell(15,15)');await page.evaluate('window.__tabletopTEST.cell(19,19)');await page.select_option('#gridSize','7');return bool((await page.evaluate('window.__tabletopTEST.ruler()'))['end'])
async def main():
 results=[]
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for name,old,new,kind in SOURCES:
   if JS.count(old)!=1:results.append({'name':name,'status':'NOT_EXECUTABLE','detail':'target missing'});continue
   page=await b.new_page();await mount(page,js=JS.replace(old,new));out=await test(page,kind);results.append({'name':name,'status':'KILLED' if out else 'SURVIVED'});await page.close()
  await b.close()
 print(json.dumps(results,ensure_ascii=False))
 (ROOT/'evidence'/'PHASE2_MUTATIONS.json').write_text(json.dumps(results,indent=2))
 assert all(r['status']=='KILLED' for r in results)
asyncio.run(main())
