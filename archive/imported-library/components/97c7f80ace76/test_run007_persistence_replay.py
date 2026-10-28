"""New TEST20–22 digital regressions: red baseline vs green product.
No network, no canonical data. Chrome storage is mocked because local HTTP is disabled.
"""
import asyncio, json, copy, pathlib, re, sys
from playwright.async_api import async_playwright
from test_integrated import mount
ROOT=pathlib.Path(__file__).resolve().parents[1]
KEY='assim.tabletop.synthetic.workspace.v1'

async def suite(browser,width,height):
 page=await browser.new_page(viewport={'width':width,'height':height}, accept_downloads=True)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 checks=[]
 def check(name,condition):
  if not condition:raise AssertionError(f'{width}x{height}: {name}')
  checks.append(name)
 async def ev(src,arg=None):return await page.evaluate(src,arg) if arg is not None else await page.evaluate(src)
 await mount(page)
 old=await ev('window.__tabletopTEST.state()');candidate=copy.deepcopy(old);candidate['scenes'][0]['name']='CANDIDATO_NOVO'
 # 1. failure before write: confirmed previous
 result=await ev('''(w)=>{const s=localStorage;const get=s.getItem.bind(s);s.setItem=()=>{throw new DOMException('quota','QuotaExceededError')};try{window.__tabletopTEST.restoreCandidate(w);return 'COMMIT';}catch(e){return e.storageStatus||e.message;}}''',candidate)
 check('quota classified confirmed failure',result=='FAILED_CONFIRMED')
 check('quota retains workspace',await ev('window.__tabletopTEST.state()')==old)
 check('quota does not enter unknown barrier',not await ev('window.__tabletopTEST.uncertain()'))
 # reset mocked functions for the next independent scenario
 await mount(page)
 old=await ev('window.__tabletopTEST.state()');candidate=copy.deepcopy(old);candidate['scenes'][0]['name']='CANDIDATO_NOVO'
 # 2. write succeeds but reads fail AFTER mutation, including rollback
 outcome=await ev('''(w)=>{
  const storage=localStorage,originalSet=storage.setItem.bind(storage),originalGet=storage.getItem.bind(storage);let wrote=false;
  storage.setItem=(key,value)=>{wrote=true;originalSet(key,value)};
  storage.getItem=(key)=>{if(wrote)throw new Error('read blocked AFTER write');return originalGet(key)};
  try{window.__tabletopTEST.restoreCandidate(w);return 'COMMITTED';}catch(e){return e.storageStatus||e.message;}
 }''',candidate)
 check('postwrite unknown status',outcome=='UNKNOWN_AFTER_WRITE')
 check('unknown retains old RAM',await ev('window.__tabletopTEST.state()')==old)
 check('unknown barrier active',await ev('window.__tabletopTEST.uncertain()'))
 check('visible alert',await page.locator('#storageConflict').is_visible())
 check('visible text says indefinite', 'indeterminada' in (await page.locator('#storageConflict').inner_text()).lower())
 check('barrier prevents new writes',await ev('''()=>{try{window.__tabletopTEST.restoreCandidate(window.__tabletopTEST.state());return false}catch(e){return e.storageStatus==='UNKNOWN_AFTER_WRITE'}}'''))
 # recover read access, confirm candidate present, export old RAM, then consciously adopt stored version
 await ev('''()=>{localStorage.getItem=(k)=>window.__TESTSTORE[k]??null;}''')
 check('reconciliation finds candidate',await ev('window.__tabletopTEST.inspectReconcile()')=='STORED_CANDIDATE')
 async with page.expect_download() as info:await page.locator('#storageExport').click()
 dl=await info.value
 check('backup of RAM downloadable',dl.suggested_filename.startswith('TABLETOP_RECUPERACAO_MEMORIA'))
 page.on('dialog',lambda d:asyncio.create_task(d.accept()))
 await page.locator('#storageAdopt').click()
 check('candidate adopted only after explicit confirmation',(await ev('window.__tabletopTEST.state()'))['scenes'][0]['name']=='CANDIDATO_NOVO')
 check('barrier cleared',not await ev('window.__tabletopTEST.uncertain()'))
 check('candidate identical on disk',await ev(f'''()=>JSON.stringify(window.__tabletopTEST.state())===localStorage.getItem('{KEY}')'''))
 await mount(page,fresh_storage=False)
 check('reload reads adopted version',(await ev('window.__tabletopTEST.state()'))['scenes'][0]['name']=='CANDIDATO_NOVO')
 # 3. persisted previous after injected changed-then-rolled back, should classify confirmed
 previous=await ev('window.__tabletopTEST.state()');tryState=copy.deepcopy(previous);tryState['scenes'][0]['name']='ROLLBACK_EXPECTED'
 result=await ev('''w=>{const s=localStorage,set=s.setItem.bind(s),get=s.getItem.bind(s);let writes=0;
 s.setItem=(k,v)=>{set(k,v);writes++};s.getItem=(k)=>{const t=get(k);if(writes===1) return 'different';return t};
 try{window.__tabletopTEST.restoreCandidate(w);return 'COMMITTED';}catch(e){return e.storageStatus||e.message;}}''',tryState)
 check('confirmed rollback is failure not unknown',result=='FAILED_CONFIRMED')
 check('rolled back storage identity',await ev(f'''()=>localStorage.getItem('{KEY}')''')==json.dumps(previous,ensure_ascii=False,separators=(',',':')))
 await mount(page,fresh_storage=False)
 # 4. stale restoration warning with 2 current scenes -> 1 incoming
 base=await ev('window.__tabletopTEST.state()');await page.locator('#newScene').click();current=await ev('window.__tabletopTEST.state()');check('created 2 scenes',len(current['scenes'])==2)
 await page.locator('#restore').set_input_files({'name':'older.json','mimeType':'application/json','buffer':json.dumps(base,ensure_ascii=False).encode()})
 await page.wait_for_timeout(80)
 check('stale review opens',await page.locator('#restoreReview').is_visible())
 summary=await page.locator('#restoreReviewSummary').inner_text()
 check('review gives counts','2 cena' in summary and '1 cena' in summary)
 check('stale does not mutate before confirm',len((await ev('window.__tabletopTEST.state()'))['scenes'])==2)
 await page.locator('#restoreReviewCancel').click()
 check('cancel keeps 2 scenes',len((await ev('window.__tabletopTEST.state()'))['scenes'])==2)
 await page.locator('#restore').set_input_files({'name':'older2.json','mimeType':'application/json','buffer':json.dumps(base,ensure_ascii=False).encode()})
 await page.wait_for_timeout(80)
 async with page.expect_download() as info:await page.locator('#restoreReviewExport').click()
 check('pre-restoration export offered',(await info.value).suggested_filename.startswith('TABLETOP_BACKUP_ANTES'))
 check('export does not restore',len((await ev('window.__tabletopTEST.state()'))['scenes'])==2)
 await page.locator('#restoreReviewConfirm').click()
 check('explicit confirm restores one scene',len((await ev('window.__tabletopTEST.state()'))['scenes'])==1)
 check('one scene persisted after review',len(json.loads(await ev(f'''()=>localStorage.getItem('{KEY}')'''))['scenes'])==1)
 # 5. mixed replay IDs fail-closed unless complete explicit sequence
 replay=await ev('window.__tabletopTEST.makeReplay()');replay['events']=[copy.deepcopy(replay['events'][0]) for _ in range(3)]
 for e,id in zip(replay['events'],['frame-002','custom-case-x','frame-001']):e['id']=id
 check('mixed without sequence rejected',not await ev('d=>window.__tabletopTEST.validateReplay(d)',replay))
 for i,e in enumerate(replay['events']):e['sequence']=10+i
 check('mixed with ordered sequence accepted',await ev('d=>window.__tabletopTEST.validateReplay(d)',replay))
 replay['events'][2]['sequence']=1
 check('mixed regressive seq rejected',not await ev('d=>window.__tabletopTEST.validateReplay(d)',replay))
 for i,e in enumerate(replay['events']):e['id']='custom-'+str(i);e.pop('sequence',None)
 check('arbitrary legacy by array index accepted',await ev('d=>window.__tabletopTEST.validateReplay(d)',replay))
 for i,e in enumerate(replay['events']):e['id']=f'frame-{i+1:03d}'
 check('numeric monotone accepted',await ev('d=>window.__tabletopTEST.validateReplay(d)',replay))
 replay['events'][1]['id']='frame-000'
 check('numeric regressive rejected',not await ev('d=>window.__tabletopTEST.validateReplay(d)',replay))
 # 6. dynamic geometry visibility and scene persistence
 await page.locator('#layerFov').check();await page.select_option('#gridSize','20')
 beforeFov=await ev('window.__tabletopTEST.fovNow()');check('fov visible TEST',isinstance(beforeFov,list) and len(beforeFov)>5)
 await page.locator('[data-mode="wall"]').click();await ev('window.__tabletopTEST.cell(5,5)')
 check('fov recomputes after edit', isinstance(await ev('window.__tabletopTEST.fovNow()'),list))
 await page.select_option('#fovRadius','4');low=await ev('window.__tabletopTEST.fovNow()')
 await page.select_option('#fovRadius','12');high=await ev('window.__tabletopTEST.fovNow()')
 check('fov radius change expands visible',len(high)>=len(low))
 await page.locator('#newScene').click()
 check('new scene fov separate',not (await ev('window.__tabletopTEST.scene()'))['fovEnabled'])
 await page.locator('#scenes').select_option('c1')
 check('return retains FOV state',(await ev('window.__tabletopTEST.scene()'))['fovEnabled'])
 check('no JS runtime errors',not errors)
 print(f'{width}x{height}: {len(checks)}/{len(checks)} PASS')
 await page.close();return checks

async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);
  results={}
  for w,h in [(390,844),(360,740)]:results[f'{w}x{h}']=await suite(b,w,h)
  await b.close()
 total=sum(map(len,results.values())); print('NEW_RUN007_TOTAL',total)
 (ROOT/'evidence'/'test_run007_results.json').write_text(json.dumps({'results':results,'total':total},ensure_ascii=False,indent=2))
asyncio.run(main())
