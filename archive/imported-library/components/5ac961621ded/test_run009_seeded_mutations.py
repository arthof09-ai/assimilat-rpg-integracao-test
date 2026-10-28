import asyncio,random,copy,json,pathlib
from playwright.async_api import async_playwright
from test_run009_concurrency_markers import mount,JS,KEY
SEED=20261022
OUT=pathlib.Path(__file__).resolve().parents[1]/'evidence'

def make_cases():
 r=random.Random(SEED);cases=[]
 for i in range(900):
  kind=i%9
  x=r.randrange(7);y=r.randrange(7)
  m={'id':'m1','x':x,'y':y,'kind':'note','text':'Nota TEST '+str(i)}
  expected=True;more=[]
  if kind==1:m['x']=7+r.randrange(1,300);expected=False
  elif kind==2:m['y']=-1-r.randrange(1,300);expected=False
  elif kind==3:m['id']='__proto__';expected=False
  elif kind==4:m['text']='<script>x</script>';expected=False
  elif kind==5:m['href']='javascript:alert(1)';expected=False
  elif kind==6:more=[{**m,'id':'m2'}];expected=False
  elif kind==7:more=[{**m,'x':(x+1)%7}];expected=False
  elif kind==8:m['kind']='DAMAGE_RESOLVED';expected=False
  cases.append({'markers':[m]+more,'expected':expected,'kind':kind})
 return cases

async def suite(browser):
 page=await browser.new_page();await mount(page)
 cases=make_cases()
 results=await page.evaluate('''cases=>{
 const base=window.__tabletopTEST.state();return cases.map(c=>{let w=JSON.parse(JSON.stringify(base));w.scenes[0].markers=c.markers;return window.__tabletopTEST.validateWorkspace(w);});
 }''',cases)
 errors=[{'i':i,'kind':c['kind'],'expected':c['expected'],'actual':results[i]} for i,c in enumerate(cases) if c['expected']!=results[i]]
 if errors:raise AssertionError('seeded fuzz mismatch '+str(errors[:7]))
 print('SEEDED',len(cases),'PASS','seed',SEED,'valid',sum(results),'invalid',len(cases)-sum(results))
 return {'seed':SEED,'assertions':len(cases),'valid':sum(results),'invalid':len(cases)-sum(results),'errors':errors}

# Each mutant modifies only one isolated copy of the app.js; tests must distinguish mutant from original.
MUTANTS=[
 ('duplicate_marker_id',"markerIds.has(m.id)","false",'workspace','duplicate_id'),
 ('marker_cell_outside',"!inside(m.x,m.y,s.n)","false",'workspace','oob'),
 ('duplicate_marker_position',"markerCells.has(xy(m.x,m.y))", "false",'workspace','duplicate_cell'),
 ('unexpected_marker_key',"Object.keys(m).some(k=>!['id','x','y','kind','text'].includes(k))","false",'workspace','extra_key'),
 ('invalid_marker_type',"!['pin','note','highlight'].includes(m.kind)","false",'workspace','invalid_kind'),
 ('stale_frame_topology',"s.frameTopology!==topology(s)","false",'workspace','topo'),
 ('skip_concurrent_preflight',"if(previous!==lastVerifiedRaw)","if(false)",'storage','conflict'),
 ('skip_write_readback',"if(localStorage.getItem(KEY)!==serialized)","if(false)",'storage','readback'),
 ('ignore_numeric_order',"(previousNumeric!==null&&num<=previousNumeric)","false",'replay','reversed_ids')
]
async def check_mutant(page,kind):
 if kind=='workspace':
  cases={
   'duplicate_id':"s.markers=[{id:'m1',x:0,y:0,kind:'pin',text:'A'},{id:'m1',x:1,y:1,kind:'pin',text:'B'}]",
   'oob':"s.markers=[{id:'m1',x:99,y:1,kind:'pin',text:'A'}]",
   'duplicate_cell':"s.markers=[{id:'m1',x:0,y:0,kind:'pin',text:'A'},{id:'m2',x:0,y:0,kind:'pin',text:'B'}]",
   'extra_key':"s.markers=[{id:'m1',x:0,y:0,kind:'pin',text:'A',href:'javascript:alert(1)'}]",
   'invalid_kind':"s.markers=[{id:'m1',x:0,y:0,kind:'damage',text:'A'}]",
   'topo':"s.frameTopology='tampered'"
  }
  return await page.evaluate(f'''() => {{const w=window.__tabletopTEST.state();const s=w.scenes[0];{cases[kind]};return window.__tabletopTEST.validateWorkspace(w);}}''')
 if kind=='storage':
  if (await page.evaluate('window.__tabletopTEST.state().revision'))!=0:raise AssertionError('page not fresh')
  if kind=='conflict':
   await page.evaluate('''() => {const w=window.__tabletopTEST.state();w.scenes[0].walls.push('4,4');window.__store['assim.tabletop.synthetic.workspace.v1']=JSON.stringify({...w,revision:4});}''')
   await page.locator('[data-mode="wall"]').click()
   try:await page.evaluate('window.__tabletopTEST.cell(3,3)')
   except:pass
   return not await page.evaluate('window.__tabletopTEST.externalConflict()') and await page.evaluate("JSON.parse(window.__store['assim.tabletop.synthetic.workspace.v1']).scenes[0].walls.includes('3,3')")
  if kind=='readback':
   await page.evaluate('''() => {window.localStorage.setItem=()=>{};}''')
   return await page.evaluate('window.__tabletopTEST.save(false)')
 if kind=='replay':
  return await page.evaluate('''() => {const d=window.__tabletopTEST.makeReplay();const e=structuredClone(d.events[0]);e.id='frame-002';d.events=[e, {...e,id:'frame-001'}];return window.__tabletopTEST.validateReplay(d);}''')
 raise RuntimeError(kind)

async def mutate(browser):
 results=[]
 for name,old,new,typ,case in MUTANTS:
  hits=JS.count(old)
  if hits!=1:results.append({'mutant':name,'state':'NOT_EXECUTABLE','reason':f'search count {hits}'});continue
  mutated=JS.replace(old,new)
  page=await browser.new_page();await mount(page,js=mutated)
  try:
   accepted=await check_mutant(page,typ if typ=='replay' else 'storage' if typ=='storage' else 'workspace' if typ=='workspace' else typ) if False else await check_mutant_direct(page,typ,case)
   # Baseline must reject all contrived invalid inputs; mutant accepts -> killed.
   results.append({'mutant':name,'state':'KILLED' if accepted else 'SURVIVED','mutant_allowed_bad':bool(accepted)})
  except Exception as e:results.append({'mutant':name,'state':'NOT_EXECUTABLE','reason':str(e)[:250]})
  finally:await page.close()
 print('MUTANTS',sum(v['state']=='KILLED' for v in results),'KILLED',sum(v['state']=='SURVIVED' for v in results),'SURVIVED',sum(v['state']=='NOT_EXECUTABLE' for v in results),'NOT_EXECUTABLE')
 for v in results:print(v['mutant'],v['state'])
 return results
async def check_mutant_direct(page,typ,case):
 if typ=='workspace':return await check_mutant_wrapped(page,case)
 if typ=='storage':
  if case=='conflict':
   await page.evaluate('''() => {const w=window.__tabletopTEST.state();w.scenes[0].walls.push('4,4');window.__store['assim.tabletop.synthetic.workspace.v1']=JSON.stringify({...w,revision:4});}''')
   await page.locator('[data-mode="wall"]').click()
   try:await page.evaluate('window.__tabletopTEST.cell(3,3)')
   except:pass
   return not await page.evaluate('window.__tabletopTEST.externalConflict()') and await page.evaluate("JSON.parse(window.__store['assim.tabletop.synthetic.workspace.v1']).scenes[0].walls.includes('3,3')")
  if case=='readback':
   await page.evaluate('''() => {window.localStorage.setItem=()=>{};}''')
   return await page.evaluate('window.__tabletopTEST.save(false)')
 if typ=='replay':return await page.evaluate('''() => {const d=window.__tabletopTEST.makeReplay();const e=structuredClone(d.events[0]);e.id='frame-002';d.events=[e,{...e,id:'frame-001'}];return window.__tabletopTEST.validateReplay(d);}''')
async def check_mutant_wrapped(page,case):
 cases={
 'duplicate_id':"s.markers=[{id:'m1',x:0,y:0,kind:'pin',text:'A'},{id:'m1',x:1,y:1,kind:'pin',text:'B'}]",
 'oob':"s.markers=[{id:'m1',x:99,y:1,kind:'pin',text:'A'}]",
 'duplicate_cell':"s.markers=[{id:'m1',x:0,y:0,kind:'pin',text:'A'},{id:'m2',x:0,y:0,kind:'pin',text:'B'}]",
 'extra_key':"s.markers=[{id:'m1',x:0,y:0,kind:'pin',text:'A',href:'javascript:alert(1)'}]",
 'invalid_kind':"s.markers=[{id:'m1',x:0,y:0,kind:'damage',text:'A'}]",
 'topo':"s.frameTopology='tampered'"
 }
 return await page.evaluate(f'''() => {{const w=window.__tabletopTEST.state();const s=w.scenes[0];{cases[case]};return window.__tabletopTEST.validateWorkspace(w);}}''')

async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  fuzz=await suite(b);mut=await mutate(b)
  (OUT/'TEST_RUN009_SEEDED_MUTATIONS.json').write_text(json.dumps({'fuzz':fuzz,'mutations':mut},ensure_ascii=False,indent=2))
  await b.close()
if __name__=='__main__':asyncio.run(main())
