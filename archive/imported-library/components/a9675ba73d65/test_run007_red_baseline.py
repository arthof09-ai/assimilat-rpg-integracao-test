"""Reproduction only, original untouched; PASS means three undesired behaviors were observed in TEST18."""
import asyncio,copy,json,pathlib,re
from playwright.async_api import async_playwright
BASE=pathlib.Path(__file__).resolve().parents[2]/'base/public'
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=await b.new_page(viewport={'width':390,'height':844})
  html=(BASE/'index.html').read_text();css=(BASE/'styles.css').read_text();js=(BASE/'app.js').read_text()
  html=re.sub(r'<meta http-equiv="Content-Security-Policy"[^>]*>','',html).replace('<link rel="stylesheet" href="styles.css">','').replace('<script src="app.js" defer></script>','')
  await page.set_content(html)
  await page.evaluate('''()=>{const store={};window.__TESTSTORE=store;Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem(k){return store[k]??null},setItem(k,v){store[k]=String(v)},removeItem(k){delete store[k]}}})}''')
  await page.add_style_tag(content=css);await page.add_script_tag(content=js)
  findings=[]
  old=await page.evaluate('window.__tabletopTEST.state()');new=copy.deepcopy(old);new['scenes'][0]['name']='RED_NEW'
  observed=await page.evaluate('''w=>{let wrote=false;const s=localStorage,og=s.getItem.bind(s),os=s.setItem.bind(s);s.setItem=(k,v)=>{os(k,v);wrote=true};s.getItem=k=>{if(wrote)throw new Error('read inaccessible');return og(k)};try{window.__tabletopTEST.restoreCandidate(w)}catch(e){}return {disk:window.__TESTSTORE['assim.tabletop.synthetic.workspace.v1'],ram:window.__tabletopTEST.state().scenes[0].name,msg:document.querySelector('#storageStatus').textContent};}''',new)
  findings.append({'test':'post_write_unknown_undetected','reproduced':json.loads(observed['disk'])['scenes'][0]['name']=='RED_NEW' and observed['ram']!='RED_NEW' and 'INDETERMINAD' not in observed['msg'].upper()})
  # reset original js by mounting and fresh storage
  await page.set_content(html);await page.evaluate('''()=>{const store={};window.__TESTSTORE=store;Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem(k){return store[k]??null},setItem(k,v){store[k]=String(v)},removeItem(k){delete store[k]}}})}''');await page.add_style_tag(content=css);await page.add_script_tag(content=js)
  old=await page.evaluate('window.__tabletopTEST.state()');await page.locator('#newScene').click();
  page.on('dialog',lambda d:asyncio.create_task(d.accept()))
  await page.locator('#restore').set_input_files({'name':'old.json','mimeType':'application/json','buffer':json.dumps(old,ensure_ascii=False).encode()});await page.wait_for_timeout(80)
  findings.append({'test':'old_backup_generic_confirmation','reproduced':len((await page.evaluate('window.__tabletopTEST.state()'))['scenes'])==1 and await page.locator('#restoreReview').count()==0})
  replay=await page.evaluate('window.__tabletopTEST.makeReplay()');replay['events']=[copy.deepcopy(replay['events'][0]) for _ in range(3)];
  for e,k in zip(replay['events'],['frame-002','custom-case-x','frame-001']):e['id']=k
  findings.append({'test':'mixed_id_downgrade','reproduced':await page.evaluate('d=>window.__tabletopTEST.validateReplay(d)',replay)})
  assert all(f['reproduced'] for f in findings),findings
  print(json.dumps({'baseline':'TEST18_UNMODIFIED','RED_reproduced':len(findings),'findings':findings},ensure_ascii=False,indent=2))
  out=pathlib.Path(__file__).resolve().parents[1]/'evidence/RED_TEST18_FINDINGS.json';out.write_text(json.dumps(findings,ensure_ascii=False,indent=2))
  await b.close()
asyncio.run(main())
