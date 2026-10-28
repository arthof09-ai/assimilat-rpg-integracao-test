import asyncio
from playwright.async_api import async_playwright
from test_integrated import mount
async def f():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);pg=await b.new_page(viewport={'width':390,'height':844});await mount(pg)
  print(await pg.evaluate('''() => {let w=window.__tabletopTEST.state(),s=w.scenes[0];s.n=20;s.walls=[];s.danger=[];s.frames=[];s.frameTopology=null;s.explored=[];s.units[2].x=17;s.units[2].y=17;s.units[0].x=7;s.units[0].y=10;s.selected='u1';for(let y=0;y<20;y++)s.walls.push('10,'+y);window.__tabletopTEST.restoreCandidate(w);s=window.__tabletopTEST.scene();let closed=window.__tabletopTEST.shadowcast({x:7,y:10,radius:12});let w2=window.__tabletopTEST.state();w2.scenes[0].walls=w2.scenes[0].walls.filter(v=>v!=='10,10');window.__tabletopTEST.restoreCandidate(w2);let opened=window.__tabletopTEST.shadowcast({x:7,y:10,radius:12});return {closed11:closed.includes('11,10'),opened11:opened.includes('11,10'),clen:closed.length,olen:opened.length,visibleDoor:opened.includes('10,10')}}'''))
  await b.close()
asyncio.run(f())
