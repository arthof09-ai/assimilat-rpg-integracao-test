import asyncio,json,pathlib,statistics
from playwright.async_api import async_playwright
from test_integrated import mount
async def run():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=await browser.new_page(viewport={'width':390,'height':844});await mount(page)
  r=await page.evaluate('''() => {
  const api=window.__tabletopTEST;const t=()=>performance.now();let pairs=0,failures=[],samples=[],checks=0;
  for(let seed=0;seed<10;seed++){
   let w=api.state(),s=w.scenes[0];s.n=20;s.walls=[];s.danger=[];s.frames=[];s.frameTopology=null;
   s.units[2].x=17;s.units[2].y=17;
   for(let y=0;y<20;y++)for(let x=0;x<20;x++){
    const k=x+','+y,occupied=s.units.some(u=>u.x===x&&u.y===y);
    if(!occupied&&((x*31+y*17+seed*13)^(y*7+x*11+seed))%23===0)s.walls.push(k);
   }
   api.restoreCandidate(w);const origin={x:9,y:9};const start=t();let visible=api.shadowcast({...origin,radius:8});samples.push(t()-start);checks++;
   if(!visible.includes('9,9'))failures.push({kind:'origin',seed});
   if(visible.some(k=>{let [x,y]=k.split(',').map(Number);return x<0||y<0||x>=20||y>=20||(x-9)**2+(y-9)**2>64}))failures.push({kind:'bounds',seed});checks++;
   const points=[];for(let y=3;y<17;y+=3)for(let x=3;x<17;x+=3){const k=x+','+y;if(!s.walls.includes(k))points.push([x,y]);}
   const cache=new Map();for(const q of points)cache.set(q.join(','),new Set(api.shadowcast({x:q[0],y:q[1],radius:8})));
   for(let i=0;i<points.length;i++)for(let j=i+1;j<points.length;j++){
    let a=points[i].join(','),b=points[j].join(',');if(Math.hypot(points[i][0]-points[j][0],points[i][1]-points[j][1])>8)continue;
    pairs++;if(cache.get(a).has(b)!==cache.get(b).has(a))failures.push({kind:'asymmetry',seed,a,b});
   }
   checks++;
   // origin cannot reveal a cell beyond a closed full-height synthetic wall.
   let wallmap=api.state();wallmap.scenes[0].walls=[];for(let y=0;y<20;y++)wallmap.scenes[0].walls.push('10,'+y);
   api.restoreCandidate(wallmap);
   let ray=new Set(api.shadowcast({x:6,y:10,radius:12}));checks++;
   if(ray.has('13,10'))failures.push({kind:'through_wall',seed});
  }
  return {scenes:10,pairs,checks,failures,medianMs:samples.sort((a,b)=>a-b)[4],maxMs:Math.max(...samples)};
 }''')
  assert not r['failures'],r['failures'][:15]
  print(json.dumps(r,indent=2));await browser.close()
  (pathlib.Path(__file__).parents[1]/'evidence'/'fov_geometry_bench.json').write_text(json.dumps(r,indent=2))
asyncio.run(run())
