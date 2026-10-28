"""Independent MESTRE-SIDE FOV research, NOT Assimilação canonical visibility rules.
Algorithms: Bresenham all-target line-of-sight; 8-octant classical recursive
shadowcasting (Bergström/RogueBasin); symmetric shadowcasting after Albert Ford
(algorithm published under CC0). Independently adapted for deterministic tests.
Input: grid width, height, walls {(x,y)}, origin (x,y), radius Euclidean.
Output: set of cells visible at this instant; no Party serialization.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable
from math import floor,ceil

Grid = tuple[int,int,frozenset[tuple[int,int]]]

def allowed(g,x,y):return 0<=x<g[0] and 0<=y<g[1]
def inside_radius(origin,p,r):return (p[0]-origin[0])**2+(p[1]-origin[1])**2<=r*r

def bresenham_points(a,b):
 x0,y0=a;x1,y1=b;dx=abs(x1-x0);dy=-abs(y1-y0);sx=1 if x0<x1 else -1;sy=1 if y0<y1 else -1;err=dx+dy
 while True:
  yield x0,y0
  if (x0,y0)==(x1,y1):break
  e2=2*err
  if e2>=dy:err+=dy;x0+=sx
  if e2<=dx:err+=dx;y0+=sy

def raycast(g,origin,r):
 out=set();walls=g[2]
 for y in range(max(0,origin[1]-r),min(g[1]-1,origin[1]+r)+1):
  for x in range(max(0,origin[0]-r),min(g[0]-1,origin[0]+r)+1):
   p=(x,y)
   if not inside_radius(origin,p,r):continue
   ray=list(bresenham_points(origin,p))
   if all(cell not in walls for cell in ray[1:-1]):out.add(p)
 return out

def classic_recursive(g,origin,r):
 visible={origin};walls=g[2]
 # 8 octants, standard recursive shadowcasting with floating slopes.
 transforms=((1,0,0,1),(0,1,1,0),(0,-1,1,0),(-1,0,0,1),(-1,0,0,-1),(0,-1,-1,0),(0,1,-1,0),(1,0,0,-1))
 def cast(row,start,end,xx,xy,yx,yy):
  if start<end or row>r:return
  blocked=False;newstart=start
  for dist in range(row,r+1):
   dx=-dist-1;dy=-dist
   while dx<0:
    dx+=1;x=origin[0]+dx*xx+dy*xy;y=origin[1]+dx*yx+dy*yy
    left=(dx-0.5)/(dy+0.5);right=(dx+0.5)/(dy-0.5)
    if start<right:continue
    if end>left:break
    ok=allowed(g,x,y);solid=(not ok) or (x,y) in walls
    if ok and inside_radius(origin,(x,y),r):visible.add((x,y))
    if blocked:
     if solid:newstart=right;continue
     blocked=False;start=newstart
    elif solid and dist<r:
     blocked=True;cast(dist+1,start,left,xx,xy,yx,yy);newstart=right
   if blocked:break
 for transform in transforms:cast(1,1.0,0.0,*transform)
 return visible

@dataclass
class Row:
 depth:int
 start:Fraction
 end:Fraction
 def tiles(self):
  # Floor(x+1/2), ceil(x-1/2) = rational ties-up / ties-down
  mn=floor(self.depth*self.start+Fraction(1,2))
  mx=ceil(self.depth*self.end-Fraction(1,2))
  return range(mn,mx+1)

def symmetric_ford(g,origin,r):
 """Center-to-center symmetric FOV for FLOOR origins, not full wall-origin model."""
 vis={origin}; walls=g[2]
 def pos(card,depth,col):
  ox,oy=origin
  return ((ox+col,oy-depth),(ox+col,oy+depth),(ox+depth,oy+col),(ox-depth,oy+col))[card]
 def scan(card,row):
  if row.depth>r:return
  prior=None
  for col in row.tiles():
   p=pos(card,row.depth,col)
   blocking=not allowed(g,*p) or p in walls
   floor_symmetric=(Fraction(col)>=row.depth*row.start and Fraction(col)<=row.depth*row.end)
   if allowed(g,*p) and inside_radius(origin,p,r) and (blocking or floor_symmetric):vis.add(p)
   if prior is True and not blocking:row.start=Fraction(2*col-1,2*row.depth)
   if prior is False and blocking:
    scan(card,Row(row.depth+1,row.start,Fraction(2*col-1,2*row.depth)))
   prior=blocking
  if prior is False:scan(card,Row(row.depth+1,row.start,row.end))
 for c in range(4):scan(c,Row(1,Fraction(-1),Fraction(1)))
 return vis

def explored_update(explored:set,current:set):return explored|current

def scenes(n):
 # Deterministic fixtures: each one includes origin and blockers; no RPG implication
 mid=n//2
 outer={(x,0) for x in range(n)}|{(x,n-1) for x in range(n)}|{(0,y) for y in range(n)}|{(n-1,y) for y in range(n)}
 return {
  'sala-retangular': (frozenset(outer),(mid,mid)),
  'corredor':(frozenset((x,y) for y in range(n) for x in range(n) if y not in (mid,mid+1)),(2,mid)),
  'parede-isolada':(frozenset({(mid+1,mid)}),(mid,mid)),
  'corredor-L':(frozenset((x,y) for x in range(n) for y in range(n) if not(y==mid and 1<=x<=mid or x==mid and mid<=y<n-1)),(2,mid)),
  'porta':(frozenset({(mid,y) for y in range(n) if y!=mid}),(mid-2,mid)),
  'obstaculos-diagonais':(frozenset((i,i) for i in range(2,n-2,2)),(mid,mid-2)),
  'canto-interno':(frozenset({(x,mid) for x in range(mid,n-1)} | {(mid,y) for y in range(mid,n-1)}),(mid-2,mid-2)),
  'canto-externo':(frozenset({(x,mid) for x in range(1,mid+1)} | {(mid,y) for y in range(1,mid+1)}),(mid+2,mid+2)),
  'junto-parede':(frozenset({(mid,y) for y in range(n)}),(mid-1,mid)),
  'espacos-abertos':(frozenset(),(mid,mid)),
 }
