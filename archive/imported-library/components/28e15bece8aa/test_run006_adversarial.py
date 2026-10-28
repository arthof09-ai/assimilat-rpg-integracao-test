import asyncio,json,copy,os,pathlib
from playwright.async_api import async_playwright
from test_integrated import mount

KEY='assim.tabletop.synthetic.workspace.v1'
async def suite(browser,width,height):
 page=await browser.new_page(viewport={'width':width,'height':height}); errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 await mount(page);page.on('dialog',lambda dialog:asyncio.create_task(dialog.accept()));checks=[]
 async def ck(name,truth):
  if not truth:raise AssertionError(f'{width}×{height}: {name}')
  checks.append(name)
 async def ev(x):return await page.evaluate(x)
 async def import_backup(payload):
  await page.locator('#restore').set_input_files({'name':'restore.json','mimeType':'application/json','buffer':payload if isinstance(payload,bytes) else json.dumps(payload,ensure_ascii=False).encode()})
  await page.wait_for_timeout(110)
  if await page.locator('#restoreReview').is_visible():
   await page.locator('#restoreReviewConfirm').click()
   await page.wait_for_timeout(70)
 async def base():return await ev('window.__tabletopTEST.state()')
 before=await base();w=copy.deepcopy(before);w['scenes'][0]['name']='CENA_BACKUP_VALIDO'
 await ck('baseline valid',await ev('window.__tabletopTEST.validateWorkspace(window.__tabletopTEST.state())'))
 await ev('''() => {window.__quotaFailure=true;localStorage.setItem=()=>{throw new DOMException("Quota bloqueada","QuotaExceededError")};return true;}''')
 await import_backup(w)
 await ck('quota keeps in-memory workspace',await base()==before)
 await ck('quota does not claim restored','restaurado' not in (await page.locator('#message').inner_text()).lower())
 await ck('quota user-visible failure','rejeitado' in (await page.locator('#message').inner_text()).lower())
 # Restore normal mock used in baseline tests.
 await ev('''() => {window.__quotaFailure=false;localStorage.setItem=(k,v)=>{window.__TESTSTORE[k]=String(v)}}''')
 await import_backup(w)
 await ck('normal restores', (await base())['scenes'][0]['name']=='CENA_BACKUP_VALIDO')
 await ck('readback exact persisted', await ev(f'''() => JSON.stringify(window.__tabletopTEST.state())===localStorage.getItem('{KEY}')'''))
 await mount(page,fresh_storage=False)
 await ck('reload preserves accepted restoration',(await base())['scenes'][0]['name']=='CENA_BACKUP_VALIDO')
 before=await base();new=copy.deepcopy(before);new['scenes'][0]['name']='CENA_NAO_SALVA'
 await ev('''() => {localStorage.setItem=()=>{throw new Error("disk inaccessible")};return true;}''')
 await import_backup(new)
 await ck('generic setItem exception is transactional',await base()==before)
 await ck('setItem errors reported','disk inaccessible' in await page.locator('#message').inner_text())
 await ev('''() => {localStorage.setItem=(k,v)=>{window.__TESTSTORE[k]=String(v)}}''')
 await import_backup(b'{invalid')
 await ck('invalid JSON kept prior',(await base())==before)
 bad=copy.deepcopy(before);bad['scenes'][0]['units'][0]['x']=909
 await import_backup(bad)
 await ck('partially invalid scene kept prior',(await base())==before)
 bad=copy.deepcopy(before);bad['scenes'][0]['frameTopology']='tampered'
 await ck('frame topology tamper rejected',not await ev('''w=>window.__tabletopTEST.validateWorkspace(w)''') if False else not await page.evaluate('(w)=>window.__tabletopTEST.validateWorkspace(w)',bad))
 bad=copy.deepcopy(before);bad['scenes'][0]['frames']=[{'title':'One','positions':{u['id']:[u['x'],u['y']] for u in before['scenes'][0]['units']}}];bad['scenes'][0]['frameTopology']='tampered'
 await ck('frame/topology spoof rejected',not await page.evaluate('(w)=>window.__tabletopTEST.validateWorkspace(w)',bad))
 replay=await ev('window.__tabletopTEST.makeReplay()');replay['events']=[copy.deepcopy(replay['events'][0]) for _ in range(3)]
 for i,e in enumerate(replay['events']):e['id']=["ev-010","ev-004","ev-020"][i]
 await ck('numeric event regression rejected',not await page.evaluate('(d)=>window.__tabletopTEST.validateReplay(d)',replay))
 replay['events'][1]['id']='ev-012'
 await ck('numeric sequence gaps permitted',await page.evaluate('(d)=>window.__tabletopTEST.validateReplay(d)',replay))
 replay['events'][0]['sequence']=1;replay['events'][1]['sequence']=2;replay['events'][2]['sequence']=1
 await ck('explicit seq regression rejected',not await page.evaluate('(d)=>window.__tabletopTEST.validateReplay(d)',replay))
 replay['events'][2]['sequence']=6
 await ck('explicit monotone seq valid',await page.evaluate('(d)=>window.__tabletopTEST.validateReplay(d)',replay))
 del replay['events'][1]['sequence']
 await ck('partial sequence metadata rejected',not await page.evaluate('(d)=>window.__tabletopTEST.validateReplay(d)',replay))
 # Old v1 save missing new optional FOV fields must migrate on restore.
 legacy=copy.deepcopy(before)
 for s in legacy['scenes']:
  for k in ['explored','fovEnabled','fovRadius']:s.pop(k,None)
 await import_backup(legacy)
 after=await base()
 await ck('legacy workspace v1 migrated',after['scenes'][0]['explored']==[] and after['scenes'][0]['fovEnabled']==False and after['scenes'][0]['fovRadius']==8)
 await ck('legacy workspace persists new fields', 'fovRadius' in json.loads(await ev(f"localStorage.getItem('{KEY}')"))['scenes'][0])
 await page.locator('#layerFov').check()
 await ck('FOV layer toggles', (await base())['scenes'][0]['fovEnabled'])
 await ck('FOV initial center visible','1,1' in await ev('window.__tabletopTEST.fovNow()'))
 await ck('FOV explored nonempty',len((await base())['scenes'][0]['explored'])>0)
 await page.select_option('#fovRadius','4')
 await ck('FOV dimmed previously explored cells',await page.locator('.tile.fov-explored').count()>0)
 await page.select_option('#gridSize','20');await page.select_option('#fovRadius','12')
 await ck('20x20 FOV enabled',len(await ev('window.__tabletopTEST.fovNow()'))>10)
 await ck('20x20 stable tiles',await page.locator('.tile').count()==400)
 # Simmetry in completely open arena with origins within interior 20x20; no s.walls.
 fwd=await ev('window.__tabletopTEST.shadowcast({x:9,y:10,radius:8})')
 rev=await ev('window.__tabletopTEST.shadowcast({x:15,y:12,radius:8})')
 await ck('open floor pair FOV symmetric',('15,12' in fwd)==('9,10' in rev))
 await page.locator('[data-mode="wall"]').click();await ev('window.__tabletopTEST.cell(5,5)')
 await ck('wall edit valid', '5,5' in (await base())['scenes'][0]['walls'])
 await ck('FOV recompute after wall', isinstance(await ev('window.__tabletopTEST.fovNow()'),list))
 await page.locator('#newScene').click()
 await ck('new scene FOV independent',not (await base())['scenes'][1]['fovEnabled'])
 await page.locator('#scenes').select_option('c1')
 await ck('FOV persisted across scenes', (await base())['scenes'][0]['fovEnabled'])
 await ck('FOV persisted after reload',await ev('window.__tabletopTEST.validateWorkspace(window.__tabletopTEST.state())'))
 await ck('zero uncaught page errors',not errors)
 print(f'{width}x{height} NEW QA {len(checks)}/{len(checks)} PASS')
 await page.close();return checks
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);a=await suite(browser,390,844);b=await suite(browser,360,740);await browser.close()
  print('TOTAL',len(a)+len(b))
  (pathlib.Path(__file__).parents[1]/'evidence'/'new_adversarial_results.json').write_text(json.dumps({'viewport390':a,'viewport360':b,'total':len(a)+len(b)},ensure_ascii=False,indent=2))
asyncio.run(main())
