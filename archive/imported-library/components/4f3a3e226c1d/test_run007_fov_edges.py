"""Door/corridor and cache invalidation checks against TEST22 implementation (not rules)."""
import asyncio,json,pathlib,copy
from playwright.async_api import async_playwright
from test_integrated import mount
ROOT=pathlib.Path(__file__).resolve().parents[1]
async def suite(b,w,h):
 p=await b.new_page(viewport={'width':w,'height':h},accept_downloads=True);errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
 await mount(p);checks=[]
 async def ok(label,val):
  assert val,f'{w}x{h} {label}';checks.append(label)
 W=await p.evaluate('window.__tabletopTEST.state()');s=W['scenes'][0];s['n']=20;s['walls']=[f'10,{y}' for y in range(20)];s['danger']=[];s['frames']=[];s['frameTopology']=None;s['explored']=[];s['units'][0]['x']=7;s['units'][0]['y']=10;s['units'][2]['x']=17;s['units'][2]['y']=17;s['selected']='u1';s['fovEnabled']=True;s['fovRadius']=12
 await p.evaluate('w=>window.__tabletopTEST.restoreCandidate(w)',W)
 await ok('20x20 wall fixture validated',await p.evaluate('window.__tabletopTEST.validateWorkspace(window.__tabletopTEST.state())'))
 closed=await p.evaluate('window.__tabletopTEST.fovNow()')
 await ok('closed wall occludes behind','11,10' not in closed)
 await ok('closed wall includes origin','7,10' in closed)
 await ok('wall tile itself viewable','10,10' in closed)
 explored0=(await p.evaluate('window.__tabletopTEST.scene()'))['explored']
 await ok('initial explored bounded',len(explored0)>0 and len(explored0)<=400)
 await p.locator('[data-mode="wall"]').click();await p.evaluate('window.__tabletopTEST.cell(10,10)')
 opened=await p.evaluate('window.__tabletopTEST.fovNow()')
 await ok('opening door reveals beyond wall','11,10' in opened)
 await ok('opening changes FOV cache result',len(opened)>len(closed))
 await ok('door is removed', '10,10' not in (await p.evaluate('window.__tabletopTEST.scene()'))['walls'])
 # explored persists through occlusion (not official vision rule)
 await p.evaluate('window.__tabletopTEST.cell(10,10)')
 reclosed=await p.evaluate('window.__tabletopTEST.fovNow()')
 await ok('closing door occludes again','11,10' not in reclosed)
 await ok('explored continues remembering seen cell','11,10' in (await p.evaluate('window.__tabletopTEST.scene()'))['explored'])
 # radius and origin cache invalidation
 await p.select_option('#fovRadius','4')
 small=await p.evaluate('window.__tabletopTEST.fovNow()')
 await ok('radius4 reduces set',len(small)<len(closed))
 await p.select_option('#fovRadius','12')
 await ok('radius12 restores baseline set',set(await p.evaluate('window.__tabletopTEST.fovNow()'))==set(closed))
 # scene isolation + reload mock
 await p.locator('#newScene').click()
 await ok('new scene independent visibility',not (await p.evaluate('window.__tabletopTEST.scene()'))['fovEnabled'])
 await p.locator('#scenes').select_option('c1')
 await ok('switch back remembers explored','11,10' in (await p.evaluate('window.__tabletopTEST.scene()'))['explored'])
 await mount(p,fresh_storage=False)
 await ok('mock reload remembers FOV', (await p.evaluate('window.__tabletopTEST.scene()'))['fovEnabled'])
 await ok('mock reload remembers explored','11,10' in (await p.evaluate('window.__tabletopTEST.scene()'))['explored'])
 await ok('no page errors',not errs)
 await p.screenshot(path=str(ROOT/'evidence'/f'TEST22_FOV_DOOR_{w}x{h}.png'),full_page=True)
 await p.close();print(f'FOV DOORS {w}x{h}: {len(checks)}/{len(checks)} PASS');return checks
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);r={}
  for w,h in [(390,844),(360,740)]:r[f'{w}x{h}']=await suite(b,w,h)
  await b.close()
 total=sum(len(x) for x in r.values());print('TOTAL_FOV_DOOR',total)
 (ROOT/'evidence'/'test_run007_fov_edges.json').write_text(json.dumps({'total':total,'tests':r},ensure_ascii=False,indent=2))
asyncio.run(main())
