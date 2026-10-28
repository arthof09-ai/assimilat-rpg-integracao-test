"""RUN-008 TEST24/25/26: topology, ruler, undo, export, FOV and visibility pause.
Only synthetic data; Chromium emulation, not physical Android certification.
"""
import asyncio,json,copy,pathlib
from playwright.async_api import async_playwright
from test_integrated import mount,ROOT

async def suite(browser,width,height):
 page=await browser.new_page(viewport={'width':width,'height':height},accept_downloads=True)
 await mount(page)
 a='window.__tabletopTEST';c=[];errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 async def ck(name,pred):
  assert pred,f'{width}x{height} - {name}';c.append(name)
 async def ev(code):return await page.evaluate(code)
 for mode in ['erase','danger','terrain']:
  await mount(page)
  await page.locator('[data-mode="wall"]').click()
  await ev(f'{a}.cell(3,2)')
  await page.locator('#record').click()
  initial=await ev(f'{a}.scene()')
  await ck('captured frame '+mode,bool(initial['frames'] and initial['frameTopology']))
  await page.locator(f'[data-mode="{mode}"]').click()
  await ev(f'{a}.cell(3,2)')
  now=await ev(f'{a}.scene()')
  await ck('topological edit '+mode,'3,2' not in now['walls'])
  await ck('old frames invalidated '+mode,not now['frames'] and now['frameTopology'] is None)
  await ck('local replay viewer cleared '+mode,await ev(f'{a}.replay()===null'))
  await ck('workspace valid '+mode,await ev(f'{a}.validateWorkspace({a}.state())'))
  await ck('persisted valid '+mode, bool(await ev("localStorage.getItem('assim.tabletop.synthetic.workspace.v1')")))
  await ev(f'{a}.undo()')
  undone=await ev(f'{a}.scene()')
  await ck('undo wall and replay '+mode,'3,2' in undone['walls'] and len(undone['frames'])>=1)
  await ck('undo workspace valid '+mode,await ev(f'{a}.validateWorkspace({a}.state())'))
  await ev(f'{a}.redo()')
  redone=await ev(f'{a}.scene()')
  await ck('redo edit valid '+mode,'3,2' not in redone['walls'] and not redone['frames'])
  await ck('redo workspace valid '+mode,await ev(f'{a}.validateWorkspace({a}.state())'))
  # Actual exported backup and simulated reload preserving good scene.
  async with page.expect_download() as di:await page.locator('#backup').click()
  download=await di.value;tmp=ROOT.parent/'evidence'/f'backup_{mode}_{width}.json';await download.save_as(str(tmp))
  exported=json.loads(tmp.read_text())
  await ck('export consistent '+mode,exported['scenes'][0]['walls']==redone['walls'])
  await mount(page,fresh_storage=False)
  reloaded=await ev(f'{a}.scene()')
  await ck('reload valid '+mode,'3,2' not in reloaded['walls'] and await ev(f'{a}.validateWorkspace({a}.state())'))
 # Non-topological danger/terrain edit must retain valid captured replay
 await mount(page)
 await page.locator('#record').click()
 start=await ev(f'{a}.scene()');await ck('initial frame recorded',len(start['frames'])==1)
 for mode in ['danger','terrain','erase']:
  await page.locator(f'[data-mode="{mode}"]').click();await ev(f'{a}.cell(4,4)')
  cur=await ev(f'{a}.scene()')
  await ck('cosmetic keeps frames '+mode,len(cur['frames'])==1 and cur['frameTopology']==start['frameTopology'])
  await ck('cosmetic workspace valid '+mode,await ev(f'{a}.validateWorkspace({a}.state())'))
 # Ruler click events; confirm no movement/resources/logs.
 await mount(page)
 await page.locator('[data-mode="measure"]').click()
 before=await ev(f'{a}.scene()')
 await page.locator('.tile[data-xy="0,0"]').click()
 await ck('ruler point one', (await ev(f'{a}.ruler()'))['start']=={'x':0,'y':0})
 await page.locator('.tile[data-xy="3,4"]').click()
 measure=await ev(f'{a}.ruler()')
 await ck('ruler second click',measure['end']=={'x':3,'y':4})
 await ck('ruler metrics display', 'Manhattan 7' in measure['text'] and 'reta 5.00' in measure['text'])
 after=await ev(f'{a}.scene()')
 await ck('ruler never moves units',after['units']==before['units'])
 await ck('ruler never edits map',after['walls']==before['walls'] and after['danger']==before['danger'] and after['terrain']==before['terrain'])
 await ck('ruler never changes resources/frames', after['frames']==before['frames'] and after['logs']==before['logs'] and after['stepsUsed']==before['stepsUsed'])
 await ck('ruler line visually present',await page.locator('#rulerOverlay').is_visible())
 await page.locator('#zoom').fill('72')
 await ck('zoom leaves distance invariant','Manhattan 7' in (await ev(f'{a}.ruler()'))['text'])
 await ck('zoom redraws svg properly',float(await page.locator('#rulerSegment').get_attribute('x2'))>220)
 await page.locator('.tile[data-xy="1,0"]').click()
 rr=await ev(f'{a}.ruler()')
 await ck('third click resets initial point',rr['start']=={'x':1,'y':0} and rr['end'] is None)
 await page.locator('[data-mode="pan"]').click()
 await ck('ruler deactivation clears overlay',not await page.locator('#rulerOverlay').is_visible())
 await ck('mode is pan',(await ev(f'{a}.scene()'))['mode']=='pan')
 # FOV and ruler are separate - activating FOV does not affect ruler mechanics
 await page.locator('#layerFov').check()
 await page.locator('[data-mode="measure"]').click()
 await ev(f'{a}.cell(0,0)');await ev(f'{a}.cell(3,4)')
 await ck('measure works with FOV','Manhattan 7' in (await ev(f'{a}.ruler()'))['text'])
 await ck('scene remains valid with measurement',await ev(f'{a}.validateWorkspace({a}.state())'))
 await page.locator('[data-mode="play"]').click()
 # Replay auto pause on visibilitychange; synthetic browser visibility signal
 await ev(f'{a}.cell(1,1)');await ev(f'{a}.cell(2,1)')
 await page.locator('#record').click()
 await page.locator('#replayPlay').click()
 await ck('auto playback started','Pausar' in (await page.locator('#replayPlay').inner_text()))
 await ev("() => {Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'));}")
 await ck('replay paused on background','Reproduzir' in (await page.locator('#replayPlay').inner_text()))
 await ck('background notice shown','segundo plano' in (await page.locator('#message').inner_text()))
 await ck('no runtime errors',not errors)
 result={'viewport':f'{width}x{height}','checks':len(c),'labels':c}
 await page.close();return result
async def main():
 (ROOT.parent/'evidence').mkdir(exist_ok=True)
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  results=[]
  for width,height in [(390,844),(360,740)]:
   r=await suite(b,width,height);results.append(r);print(f'{width}x{height}: {r["checks"]}/{r["checks"]} PASS')
  await b.close()
 total=sum(r['checks'] for r in results);print('RUN008_INTERACTIONS_TOTAL',total)
 (ROOT.parent/'evidence'/'RUN008_NEW_TESTS.json').write_text(json.dumps({'total':total,'results':results},ensure_ascii=False,indent=2))
asyncio.run(main())
