import asyncio,json,pathlib,sys
from playwright.async_api import async_playwright
from test_run009_concurrency_markers import mount,JS
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  out={}
  page=await b.new_page();await mount(page)
  out['noncanonical_wall_accepted']=await page.evaluate("() => {const w=window.__tabletopTEST.state();w.scenes[0].walls.push('02,02');return window.__tabletopTEST.validateWorkspace(w)}")
  out['canonical_wall_accepted']=await page.evaluate("() => {const w=window.__tabletopTEST.state();w.scenes[0].walls.push('2,2');return window.__tabletopTEST.validateWorkspace(w)}")
  await page.locator('[data-mode="wall"]').click();await page.evaluate('window.__tabletopTEST.cell(4,4)');await page.evaluate('window.__tabletopTEST.undo()')
  await page.locator('[data-mode="erase"]').click();await page.evaluate('window.__tabletopTEST.cell(6,6)');await page.evaluate('window.__tabletopTEST.redo()')
  out['no_op_erase_lost_redo']='4,4' not in (await page.evaluate('window.__tabletopTEST.scene()'))['walls']
  page2=await b.new_page();await mount(page2)
  await page2.select_option('#gridSize','20');await page2.locator('[data-mode="measure"]').click();await page2.evaluate('window.__tabletopTEST.cell(15,15)');await page2.evaluate('window.__tabletopTEST.cell(19,19)');await page2.select_option('#gridSize','7')
  out['ruler_outside_grid_after_resize']=bool((await page2.evaluate('window.__tabletopTEST.ruler()'))['end'])
  out['ruler_description']=await page2.locator('#rulerStatus').inner_text()
  print(json.dumps(out,ensure_ascii=False,indent=2));await b.close()
  assert out['noncanonical_wall_accepted'] and out['no_op_erase_lost_redo'] and out['ruler_outside_grid_after_resize']
if __name__=='__main__':asyncio.run(main())
