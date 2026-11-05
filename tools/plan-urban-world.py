"""Deterministic, offline parcel/street/flyover planner. Original generated assets."""
from pathlib import Path
import json,math,random,heapq
root=Path(__file__).resolve().parents[1];src=json.loads((root/'assets/world/input.json').read_text());rng=random.Random(2155185)
near=list({(b['x'],b['z'],b['width'],b['depth'],b.get('angle',0)):b for b in src['near']}.values())
def bounds(b,pad=0):
 a=b.get('angle',0);co=abs(math.cos(a));si=abs(math.sin(a));ex=co*b['width']/2+si*b['depth']/2+pad;ez=si*b['width']/2+co*b['depth']/2+pad
 return (b['x']-ex,b['z']+b['depth']/2-ez,b['x']+ex,b['z']+b['depth']/2+ez)
def overlap(a,b,pad=0):
 A=bounds(a,pad);B=bounds(b);return A[0]<B[2] and A[2]>B[0] and A[1]<B[3] and A[3]>B[1]
def point_segment(p,a,b):
 dx=b[0]-a[0];dz=b[1]-a[1];t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dz)/(dx*dx+dz*dz or 1)));return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dz)
roads=json.loads(json.dumps(src['roads']['roads']));junctions=src['roads']['junctions'][:]
step=2;X0=-150;Z0=-90;NX=151;NZ=391
blocked=set()
for b in near:
 if b['chapter']>1:continue
 x0,z0,x1,z1=bounds(b,4.3)
 for iz in range(max(0,int((z0-Z0)//2)),min(NZ,int((z1-Z0)//2)+2)):
  for ix in range(max(0,int((x0-X0)//2)),min(NX,int((x1-X0)//2)+2)):
   if x0<=X0+ix*2<=x1 and z0<=Z0+iz*2<=z1:blocked.add((ix,iz))
def grid(p):return (round((p[0]-X0)/2),round((p[1]-Z0)/2))
def world(q):return [X0+q[0]*2,Z0+q[1]*2]
def nearest(p):
 q=grid(p)
 for radius in range(20):
  options=[(q[0]+dx,q[1]+dz) for dx in range(-radius,radius+1) for dz in range(-radius,radius+1) if 0<=q[0]+dx<NX and 0<=q[1]+dz<NZ and (q[0]+dx,q[1]+dz) not in blocked]
  if options:return min(options,key=lambda q:math.dist(world(q),p))
 raise ValueError('No free endpoint')
def find(a,b,penalty=None):
 start=nearest(a);goal=nearest(b);cost={start:0};parent={};heap=[(0,start)];closed=set()
 while heap:
  _,q=heapq.heappop(heap)
  if q in closed:continue
  if q==goal:break
  closed.add(q)
  for dx,dz in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
   n=(q[0]+dx,q[1]+dz)
   if not(0<=n[0]<NX and 0<=n[1]<NZ) or n in blocked or n in closed:continue
   if dx and dz and ((q[0]+dx,q[1]) in blocked or (q[0],q[1]+dz) in blocked):continue
   extra=penalty(n) if penalty else 0;v=cost[q]+math.hypot(dx,dz)+extra
   if v<cost.get(n,1e20):cost[n]=v;parent[n]=q;heapq.heappush(heap,(v+math.dist(n,goal),n))
 else:raise ValueError('No path')
 path=[goal]
 while path[-1]!=start:path.append(parent[path[-1]])
 path=[world(q) for q in reversed(path)];path[0]=list(a);path[-1]=list(b);return path
main=roads[0]['points']
def at(points,z):return min(points,key=lambda p:abs(p[1]-z))
spines={}
for side in [-1,1]:
 points=find([side*112,-60],[side*116,664]);spines[side]=points;roads.append({'kind':'avenue','width':4,'walk':1.1,'points':points})
 for z in [-60,664]:
  a=at(main,z);b=at(points,z);roads.append({'kind':'side','width':3.2,'walk':1,'points':find(a,b)});junctions.extend([a,b])
for r in src['roads']['roads'][1:]:
 a=r['points'][-1];side=-1 if a[0]<0 else 1;b=at(spines[side],a[1]+(12 if side>0 else -10));roads.append({'kind':'side','width':2.8,'walk':1,'points':find(a,b)});junctions.extend([a,b])
# Ground occupancy mask for flyover routing and supports.
segments=[(a,b,r['width']/2+r['walk']) for r in roads for a,b in zip(r['points'],r['points'][1:])]
def road_distance(p):return min(point_segment(p,a,b)-w for a,b,w in segments)
roadmask=set()
for a,b,w in segments:
 for iz in range(max(0,int((min(a[1],b[1])-w-2-Z0)//2)),min(NZ,int((max(a[1],b[1])+w+2-Z0)//2)+2)):
  for ix in range(max(0,int((min(a[0],b[0])-w-2-X0)//2)),min(NX,int((max(a[0],b[0])+w+2-X0)//2)+2)):
   if point_segment(world((ix,iz)),a,b)<w+1:roadmask.add((ix,iz))
bridges=[]
for side,low,high,mid in [(1,-45,290,180),(-1,325,665,485)]:
 source=at(spines[side],low);target=at(spines[side],high)
 # Force the elevated connector inside the perimeter street, across its feeder.
 connector=min(roads[13:],key=lambda r:abs(r['points'][-1][1]-mid)+abs(r['points'][-1][0]-side*112))
 crossing=min(connector['points'],key=lambda p:abs(p[0]-side*85))
 def penalty(q):
  if q not in roadmask:return 0
  p=world(q)
  if min(math.dist(p,source),math.dist(p,target),math.dist(p,crossing))<5:return 0
  return 18
 points=find(source,crossing,penalty)+find(crossing,target,penalty)[1:]
 # Erase path backtracking before constructing a continuous deck.
 clean=[];indices={}
 for p in points:
  k=tuple(p)
  if k in indices:
   clean=clean[:indices[k]+1];indices={tuple(q):i for i,q in enumerate(clean)}
  else:indices[k]=len(clean);clean.append(p)
 points=clean
 for _ in range(3):points=[points[0]]+[[sum([points[i-1][k],2*points[i][k],points[i+1][k]])/4 for k in range(2)] for i in range(1,len(points)-1)]+[points[-1]]
 lengths=[0]
 for a,b in zip(points,points[1:]):lengths.append(lengths[-1]+math.dist(a,b))
 total=lengths[-1];contacts=[s for p,s in zip(points,lengths) if road_distance(p)<1.8 and 12<s<total-12]
 ramp=min(80,min(contacts,default=100)-3,total-max(contacts,default=total-100)-3)
 if ramp<45:raise ValueError(f'Ramp crosses street: side {side}, ramp {ramp}, contacts {contacts[:4]}..{contacts[-4:]}')
 height=min(6.4,ramp*.095);smooth=lambda t:t*t*(3-2*t)
 vertices=[[p[0],height*smooth(min(1,s/ramp,(total-s)/ramp)),p[1],s] for p,s in zip(points,lengths)]
 piers=[];last=-30
 for v in vertices:
  if v[1]>1.3 and v[3]-last>=20 and road_distance([v[0],v[2]])>2.5:
   piers.append({'x':v[0],'z':v[2],'height':v[1]-.5,'width':1.6,'depth':1.6});last=v[3]
 bridges.append({'id':len(bridges),'side':side,'width':3.2,'height':height,'rampLength':ramp,'length':total,'points':vertices,'piers':piers,'crossing':crossing,'connections':[source,target]})
 print('bridge',side,'length',round(total,1),'height',height,'ramp',round(ramp,1),'piers',len(piers),flush=True)
# Parcels are selected after roads and bridge reservations; footprint separation is conservative.
all_placed=[];backdrops=[];bridge_segments=[([a[0],a[2]],[b[0],b[2]],br['width']/2+2) for br in bridges for a,b in zip(br['points'],br['points'][1:])]
def reserve_clear(b):
 x0,z0,x1,z1=bounds(b,2)
 for a,c,w in segments+bridge_segments:
  if max(a[0],c[0])+w<x0 or min(a[0],c[0])-w>x1 or max(a[1],c[1])+w<z0 or min(a[1],c[1])-w>z1:continue
  # Expanded bounding-box rejection deliberately reserves extra corner/plaza space.
  return False
 return not any(overlap(b,o,2) for o in near+all_placed)
starts=[0,315,630,945,1170];targets=[180,180,82,38,32]
for chapter,target_count in enumerate(targets):
 placed=[];start=starts[chapter]
 if chapter<2:clusters=[(side*x,start+z,sx,sz) for side in [-1,1] for x,z,sx,sz in [(92,45,18,40),(165,130,38,55),(245,235,40,68),(130,275,24,24)]]
 elif chapter<4:clusters=[(side*x,start+z,22,35) for side in [-1,1] for x,z in [(85,35),(132,110),(195,180)]]
 else:clusters=[(side*x,start+z,12,18) for side in [-1,1] for x,z in [(65,25),(95,85),(70,155),(110,200)]]
 attempts=0
 while len(placed)<target_count and attempts<24000:
  attempts+=1;cx,cz,sx,sz=clusters[rng.randrange(len(clusters))];x=rng.gauss(cx,sx);z=rng.gauss(cz,sz)
  if abs(x)<64 or z<start-45 or z>start+([305,305,275,215,220][chapter]):continue
  kind=(['office','residential','commercial','stepped'][rng.randrange(4)] if chapter<2 else 'public' if chapter==2 else 'village')
  width=rng.uniform(12,24) if chapter<2 else rng.uniform(7,15);depth=rng.uniform(12,22) if chapter<2 else rng.uniform(7,13)
  # Blocks near perimeter streets follow that avenue; outer groups follow a shared diagonal parcel axis.
  angle=(.0 if abs(cx)<150 else (.18 if cx>0 else -.18))
  b={'id':f'backdrop-{chapter}-{len(placed)}','chapter':chapter,'x':round(x,3),'z':round(z,3),'width':round(width,3),'depth':round(depth,3),'height':round(rng.uniform(28,112) if chapter<2 else rng.uniform(10,28) if chapter==2 else rng.uniform(6,13),3),'angle':angle,'kind':kind,'style':rng.randrange(3),'seed':chapter*1009+len(placed)*17,'side':1 if x>0 else -1,'background':True}
  if reserve_clear(b):placed.append(b);all_placed.append(b)
 backdrops.append(placed);print('district',chapter,'buildings',len(placed),'attempts',attempts,flush=True)
world_data={'backdrops':backdrops,'bridges':bridges,'endProgress':185,'seed':2155185,'baseline':'215a5dd'}
(root/'assets/world/layout.json').write_text(json.dumps(world_data,separators=(',',':')))
(root/'assets/ground/roads.json').write_text(json.dumps({'roads':roads,'junctions':junctions},separators=(',',':')))
(root/'evidence/urban/planning.json').write_text(json.dumps({'roadCountBefore':len(src['roads']['roads']),'roadCountAfter':len(roads),'backdropsBefore':[len(x) for x in src['backdrops']],'backdropsAfter':[len(x) for x in backdrops],'bridges':[{'length':b['length'],'height':b['height'],'rampLength':b['rampLength'],'piers':len(b['piers'])} for b in bridges]},indent=2))
