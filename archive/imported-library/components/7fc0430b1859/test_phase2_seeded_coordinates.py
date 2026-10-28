import asyncio,json,random,pathlib
from playwright.async_api import async_playwright
from test_run009_concurrency_markers import mount
ROOT=pathlib.Path(__file__).resolve().parents[1]
async def main():
 r=random.Random(20261022);cases=[]
 safe=[(x,y) for y in range(7) for x in range(7) if (x,y) not in {(1,1),(1,3),(5,2)}]
 for i in range(600):
  x,y=r.choice(safe)
  if i%3==0:keys=[f'{x},{y}'];accept=True;plan='NO_CHANGE'
  elif i%3==1:keys=[f'{x:02d},{y:02d}'];accept=(x>=10 or y>=10);plan='SAFE_NORMALIZATION' if not accept else 'NO_CHANGE'
  else:keys=[f'{x},{y}',f'{x:02d},{y:02d}'];accept=False;plan='CONFLICT' if f'{x},{y}'!=f'{x:02d},{y:02d}' else 'CONFLICT'
  # for x=y=0 the alias 00,00 is still noncanonical; chosen safe cells under 7.
  cases.append({'keys':keys,'accept':accept,'plan':plan})
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=await b.new_page();await mount(page)
  out=await page.evaluate('''arr=>arr.map(c=>{let w=window.__tabletopTEST.state();w.scenes[0].walls=c.keys;const valid=window.__tabletopTEST.validateWorkspace(w);const p=window.__tabletopTEST.planCoordinateMigration(w);return {valid,status:p.status,canon:p.candidate?.scenes[0]?.walls};})''',cases)
  errors=[]
  for i,(c,actual) in enumerate(zip(cases,out)):
   if actual['valid']!=c['accept'] or actual['status']!=c['plan']:errors.append({'i':i,'case':c,'observed':actual})
  print(json.dumps({'seed':20261022,'cases':len(cases),'expected_valid':sum(c['accept'] for c in cases),'expected_reject':sum(not c['accept'] for c in cases),'failures':errors[:4]},ensure_ascii=False))
  (ROOT/'evidence'/'PHASE2_SEEDED_COORDS.json').write_text(json.dumps({'seed':20261022,'cases':len(cases),'errors':errors},ensure_ascii=False,indent=2))
  assert not errors
  await b.close()
asyncio.run(main())
