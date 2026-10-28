"""RUN008 independent regression for wall-removal replay validity and ruler (post-fix)."""
import asyncio, json, pathlib
from playwright.async_api import async_playwright
from test_integrated import mount, ROOT
MODES=['erase','danger','terrain']
async def repro(browser,mode,expect_fixed=False,width=390):
 page=await browser.new_page(viewport={'width':width,'height':844},accept_downloads=True)
 await mount(page)
 api='window.__tabletopTEST'
 async def ev(code):return await page.evaluate(code)
 # Wall x=3 y=2 free cell; frames captured while wall present.
 await ev(f"{api}.mode('wall')")
 await ev(f"{api}.cell(3,2)")
 await page.locator('#record').click()
 state0=await ev(f'{api}.scene()')
 assert '3,2' in state0['walls'] and state0['frames'] and state0['frameTopology']
 await ev(f"{api}.mode('{mode}')")
 await ev(f"{api}.cell(3,2)")
 changed=await ev(f'{api}.scene()')
 valid=await ev(f'{api}.validateWorkspace({api}.state())')
 result={'mode':mode,'before_frames':len(state0['frames']),'after_frames':len(changed['frames']),'wall_removed':'3,2' not in changed['walls'],'valid':valid,'status':await page.locator('#storageStatus').inner_text(),'frameTopology':changed['frameTopology']}
 assert result['wall_removed']
 if expect_fixed:
  assert valid and not changed['frames'] and changed['frameTopology'] is None,result
 else:
  assert not valid and changed['frames'] and changed['frameTopology'] is not None,result
 await page.close()
 return result
async def main():
 import sys
 fixed='--fixed' in sys.argv
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  a=[await repro(b,m,fixed) for m in MODES]
  await b.close()
 print(json.dumps(a,ensure_ascii=False,indent=2))
 (ROOT.parent/'evidence').mkdir(exist_ok=True)
 (ROOT.parent/'evidence'/('GREEN_topology.json' if fixed else 'RED_topology.json')).write_text(json.dumps(a,ensure_ascii=False,indent=2))
asyncio.run(main())
