"""Fixed-seed deterministic FOV and grid benchmark; no official gameplay."""
import json,random,time,statistics,platform,sys,hashlib,heapq
from pathlib import Path
from fov_research import *
OUT=Path('/mnt/data/inovador_pesq_pos15/evidence');OUT.mkdir(exist_ok=True)
methods={'Bresenham-los':raycast,'Recursive-classic':classic_recursive,'Symmetric-Ford':symmetric_ford}
assertions=[];bench=[];mismatches=[]
def test(label,passed,details=None):assertions.append({'name':label,'pass':bool(passed),'details':details})
for n,r in [(20,8),(30,12),(50,18),(70,24)]:
 for label,(walls,origin) in scenes(n).items():
  g=(n,n,walls)
  if origin in walls: continue
  output={k:v(g,origin,r) for k,v in methods.items()}
  for algo,vis in output.items():
   test(f'{n}-{label}-{algo}-origin',origin in vis)
   test(f'{n}-{label}-{algo}-range',all(inside_radius(origin,p,r) for p in vis))
   test(f'{n}-{label}-{algo}-bounds',all(allowed(g,*p) for p in vis))
  # Optical semantics differ at boundaries, so comparison differences are reported, not failures
  names=list(output)
  mismatches.append({'size':n,'scenario':label,'visible_counts':{k:len(v) for k,v in output.items()},'bresenham_vs_symmetric_diff':len(output[names[0]]^output[names[2]])})
  for name,method in methods.items():
   runs=[]
   for i in range(55):
    t=time.perf_counter_ns();method(g,origin,r);runs.append((time.perf_counter_ns()-t)/1e6)
   runs.sort()
   bench.append({'size':n,'scenario':label,'radius':r,'algorithm':name,'repetitions':55,'median_ms':round(statistics.median(runs),4),'p95_ms':round(runs[int(.95*(len(runs)-1))],4),'max_ms':round(max(runs),4),'min_ms':round(min(runs),4),'visible':len(output[name])})
# Guarantee of floor-to-floor visibility symmetry for symmetric Ford, fixed representative random fixture
rand=random.Random(20261022)
for n in (20,30):
 walls=frozenset((x,y) for x in range(n) for y in range(n) if rand.random()<.14)
 g=(n,n,walls);floors=[(x,y) for x in range(n) for y in range(n) if (x,y) not in walls]
 queries=rand.sample(floors, min(35,len(floors)))
 for a in queries:
  for b in rand.sample(floors,min(8,len(floors))):
   r=n
   if not inside_radius(a,b,r):continue
   ab=b in symmetric_ford(g,a,r);ba=a in symmetric_ford(g,b,r)
   test(f'symmetric-pair-{n}-{a}-{b}',ab==ba,{'ab':ab,'ba':ba})
# explored/current separation demo
for n in (20,):
 g=(n,n,frozenset({(10,y) for y in range(n) if y!=10}));a=symmetric_ford(g,(8,10),8);b=symmetric_ford(g,(13,10),8)
 test('discovered-monotonic',a<=explored_update(a,b))
 test('currently-visible-not-equal-discovered',a!=b and (a|b)!=b)
report={'environment':{'python':sys.version,'platform':platform.platform(),'clock':'perf_counter_ns','device':'container Linux CPU, NOT Chrome Android'},'method':'55 runs per size x scene x algorithm; fixed seed; no warmup; process scheduling/noise possible; p95 nearest index','cases':len(scenes(20)),'benchmarks':bench,'comparison':mismatches,'tests':assertions,'test_summary':{'pass':sum(x['pass'] for x in assertions),'total':len(assertions)},'limitation':'The three implementations do not share identical corner semantics; counts not interchangeable; paths != vision.'}
(OUT/'BENCH_FOV_PESQUISA.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print('assertions',report['test_summary']);print('failures', [x for x in assertions if not x['pass']][:10]);
for n in [20,30,50,70]:
 print('SIZE',n,[(alg,round(statistics.median([x['median_ms'] for x in bench if x['size']==n and x['algorithm']==alg]),3),round(statistics.median([x['p95_ms'] for x in bench if x['size']==n and x['algorithm']==alg]),3)) for alg in methods]);
print('diffs',mismatches[:3]);
