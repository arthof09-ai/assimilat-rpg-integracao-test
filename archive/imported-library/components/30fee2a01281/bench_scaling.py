"""Independent algorithm+Chromium visual benchmarks. No changes to TEST15 source."""
import os,json,random,time,statistics,heapq,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT=Path('/mnt/data/inovador_pesq_pos15/evidence');OUT.mkdir(exist_ok=True)
R=random.Random(20261022)
def med(x):return round(statistics.median(x),3)
def p95(x):return round(sorted(x)[int((len(x)-1)*.95)],3)
def grid(n):
 walls={(x,y) for y in range(n) for x in range(n) if R.random()<.16}
 return walls
DIR=((1,0),(-1,0),(0,1),(0,-1))
def bfs(n,walls,start):
 q=[start];prev={start:None};it=0
 for p in q:
  it+=1
  for dx,dy in DIR:
   c=(p[0]+dx,p[1]+dy)
   if 0<=c[0]<n and 0<=c[1]<n and c not in walls and c not in prev:prev[c]=p;q.append(c)
 return prev,it
def astar(n,walls,start,target):
 dist={start:0};prev={start:None};pq=[(abs(target[0]-start[0])+abs(target[1]-start[1]),0,start)];it=0
 while pq:
  _,d,p=heapq.heappop(pq)
  if d!=dist.get(p):continue
  it+=1
  if p==target:return prev,it
  for dx,dy in DIR:
   c=(p[0]+dx,p[1]+dy)
   if not(0<=c[0]<n and 0<=c[1]<n) or c in walls:continue
   nd=d+1
   if nd<dist.get(c,10**20):
    dist[c]=nd;prev[c]=p;heapq.heappush(pq,(nd+abs(target[0]-c[0])+abs(target[1]-c[1]),nd,c))
 return prev,it
def path_length(prev,end):
 if end not in prev:return None
 l=0;p=end
 while prev[p] is not None:l+=1;p=prev[p]
 return l
path_bench=[];checks=[]
for n in [20,30,50,70]:
 w=grid(n);start=(0,0);end=(n-1,n-1);w.discard(start);w.discard(end)
 opts=[(n//2,n//2),(n-1,n-1),(n//4,n-1),(n-1,n//4)]
 for target in opts:
  # Guarantee at least one valid route from (0,0): horizontal along top, then vertical at target column.
  for xx in range(target[0]+1):w.discard((xx,0))
  for yy in range(target[1]+1):w.discard((target[0],yy))
  w.discard(target)
 b_time=[];a_time=[];b_nodes=[];a_nodes=[];samples=75
 for i in range(samples):
  dest=opts[i%len(opts)]
  a=time.perf_counter_ns();bp,bn=bfs(n,w,start);b_time.append((time.perf_counter_ns()-a)/1e6)
  a=time.perf_counter_ns();ap,an=astar(n,w,start,dest);a_time.append((time.perf_counter_ns()-a)/1e6)
  checks.append({'size':n,'target':dest,'equal':path_length(bp,dest)==path_length(ap,dest),'b':path_length(bp,dest),'a':path_length(ap,dest)})
  b_nodes.append(bn);a_nodes.append(an)
 path_bench.append({'size':n,'runs':samples,'bfs_full_origin_median_ms':med(b_time),'bfs_full_origin_p95_ms':p95(b_time),'astar_single_target_median_ms':med(a_time),'astar_single_target_p95_ms':p95(a_time),'mean_bfs_nodes':round(statistics.mean(b_nodes)),'mean_astar_nodes':round(statistics.mean(a_nodes))})
# graph-edge invalidation regression: wall inserted on path -> old cached path invalid, recompute
n=20;w=set();start=(0,0);goal=(19,0);prior,_=bfs(n,w,start);block=(10,0);w.add(block);after,_=bfs(n,w,start)
checks.append({'name':'cache-invalidation','equal':path_length(prior,goal)!=path_length(after,goal),'before':path_length(prior,goal),'after':path_length(after,goal)})
# CSS DOM vs differential DOM vs canvas benchmark in Chromium local to avoid platform-specific external assets
js='''async () => {
const sizes=[20,30,50,70];const samples=35;const results=[];
const root=document.getElementById('root');
function stats(a){a.sort((x,y)=>x-y);return {median_ms:+a[Math.floor(a.length/2)].toFixed(3),p95_ms:+a[Math.floor(.95*(a.length-1))].toFixed(3)};}
for (const n of sizes){let full=[],diff=[],cv=[];let count=n*n;
for(let t=0;t<samples;t++){
 let arr=Array.from({length:count},(_,i)=>{const e=document.createElement('span');e.className='tile';e.dataset.key=String(i);e.textContent='·';return e});
 root.replaceChildren(...arr);
 let x=performance.now();
 for(let k=0;k<count;k++){arr[k].className=(k%9===t%9)?'tile blocked':'tile';arr[k].setAttribute('aria-label','casinha '+k);}
 full.push(performance.now()-x);
 x=performance.now();for(let k=0;k<Math.min(6,count);k++){arr[k].className='tile selected';arr[k].textContent=String(t);}diff.push(performance.now()-x);
 const c=document.getElementById('cv'),ctx=c.getContext('2d');c.width=n*8;c.height=n*8;
 x=performance.now();for(let yy=0;yy<n;yy++)for(let xx=0;xx<n;xx++){ctx.fillStyle=(xx+yy)%7?'#566':'#a54';ctx.fillRect(xx*8,yy*8,8,8);}cv.push(performance.now()-x);
}
results.push({size:n,cells:count,runs:samples,all_cells_attributes:stats(full),six_cells_patch:stats(diff),canvas_fill:stats(cv)});
}return {results,environment:navigator.userAgent};}'''
visual=None;error=None
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':390,'height':844})
  page.set_content('<html><body><div id="root"></div><canvas id="cv"></canvas></body></html>')
  visual=page.evaluate(js);browser.close()
except Exception as e:error=repr(e)
report={'environment':{'platform':sys.platform,'python':sys.version,'browser':'Chromium headless 390x844, synthetic DOM, not TEST15 or Android','seed':20261022},'path':path_bench,'correctness':{'passed':sum(x['equal'] for x in checks),'total':len(checks),'cache_case':checks[-1]},'visual':visual,'browser_error':error,'limitations':['BFS calculates all destinations, A* only one; use-case comparison, not equivalent work','Synthetic 30/50/70 grids are not supported by current TEST15 UI','Canvas sample measures painting only, not hit-testing, accessibility, scene management','CPU, garbage collection, device model differ from Android']}
(OUT/'BENCH_ESCALA_CAMINHOS_VISUAL.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('PATH',path_bench,'CORRECTNESS',report['correctness']);print('VISUAL',visual if visual else error)
