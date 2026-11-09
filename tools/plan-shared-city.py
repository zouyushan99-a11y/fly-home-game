"""Deterministic connected A/B/C districts, with actual world-space footprint checks."""
from pathlib import Path
import json,math
root=Path(__file__).resolve().parents[1]
world=json.loads((root/'assets/world/layout.json').read_text());roads=json.loads((root/'assets/ground/roads.json').read_text())
controls={'A':[[0,0],[45,0],[80,-21],[110,-21],[145,-45],[170,-45],[220,-42],[270,-25],[305,0],[315,0]],'B':[[0,0],[45,0],[85,0],[110,0],[170,50],[230,50],[275,18],[305,0],[315,0]],'C':[[0,0],[45,0],[85,22],[110,22],[150,85],[185,105],[220,100],[260,73],[290,25],[305,0],[315,0]]}
def path(z):return math.sin(z/175)*10+math.sin(z/410)*14
def offset(route,u):
 pts=controls[route]
 if u<=0 or u>=315:return 0
 for (a,x),(b,y) in zip(pts,pts[1:]):
  if a<=u<=b:
   t=(u-a)/(b-a);return x+(y-x)*t*t*(3-2*t)
def line(c,r,u):return path(c*315+u)+offset(r,u)
def angle(c,r,u):return math.atan2(line(c,r,u+.05)-line(c,r,u-.05),.1)
def intersects(a,b,building,pad=0):
 ang=building.get('angle',0);co=math.cos(ang);si=math.sin(ang);cx=building['x'];cz=building['z']+building['depth']/2
 local=lambda p:((p[0]-cx)*co-(p[1]-cz)*si,(p[0]-cx)*si+(p[1]-cz)*co)
 a=local(a);b=local(b);lo=0;hi=1
 for i,size in enumerate([building['width']/2+pad,building['depth']/2+pad]):
  delta=b[i]-a[i]
  if abs(delta)<1e-9:
   if abs(a[i])>size:return False
  else:
   q=(-size-a[i])/delta;t=(size-a[i])/delta;lo=max(lo,min(q,t));hi=min(hi,max(q,t))
   if lo>hi:return False
 return True
def corners(b):
 co=math.cos(b.get('angle',0));si=math.sin(b.get('angle',0));return [(b['x']+x*co+z*si,b['z']+b['depth']/2-x*si+z*co) for x,z in [(-b['width']/2,-b['depth']/2),(b['width']/2,-b['depth']/2),(b['width']/2,b['depth']/2),(-b['width']/2,b['depth']/2)]]
def overlap(a,b,pad=1):
 A=corners(a);B=corners(b)
 for poly in [A,B]:
  for i in [0,1]:
   p,q=poly[i],poly[i+1];nx=-(q[1]-p[1]);nz=q[0]-p[0];L=math.hypot(nx,nz);nx/=L;nz/=L
   aa=[x*nx+z*nz for x,z in A];bb=[x*nx+z*nz for x,z in B]
   if max(aa)+pad<min(bb) or max(bb)+pad<min(aa):return False
 return True
segments=[(a,b,r['width']/2+r['walk']) for r in roads['roads'] for a,b in zip(r['points'],r['points'][1:])]
segments += [([a[0],a[2]],[b[0],b[2]],br['width']/2+.5) for br in world['bridges'] for a,b in zip(br['points'],br['points'][1:])]
data={'controls':controls,'entrances':[],'buildings':[],'backdrops':[],'rests':[],'vegetation':[],'report':[]}
for c in [0,1]:
 start=c*315;base=path(start+80)
 entrance=[]
 for i,(x,z,w,d,h,kind,marked) in enumerate([[-36,68,18,24,88,'office',False],[-12,72,10,26,68,'office',False],[10,82,12,25,72,'office',True],[44,87,18,23,25,'residential',False]]):
  if c==0 and i==1:w=8;d=16
  if c==1 and i==0:x+=2
  entrance.append(dict(id=f'{c}-entrance-{i}',chapter=c,entry=True,entrance=True,shared=True,x=base+x,z=start+z,width=w,depth=d,height=h,kind=kind,marked=marked,glass=kind=='office',angle=0,seed=c*73+i*17,style=i%3,side=-1 if i<2 else 1,route='B' if marked else 'C' if kind=='residential' else 'A'))
 placed=entrance[:];routes={r:[(line(c,r,u),start+u) for u in range(105,301,2)] for r in controls};gates=[]
 def free(b,route,clearance=0):
  if any(overlap(b,o,1.3) for o in placed):return False
  if any(intersects(a,v,b,w+.3) for a,v,w in segments):return False
  for r,points in routes.items():
   if r==route:continue
   if any(intersects(a,v,b,{'A':5.5,'B':8,'C':12}[r]) for a,v in zip(points,points[1:])):return False
  return True
 # Deep, proportionate solids, never paper-thin gate panels.
 for r in ['A','B','C']:
  for j,u0 in enumerate([132,182,232]):
   gap={'A':5.2,'B':8,'C':13}[r];shift=(1 if j%2==0 else -1)*{'A':4.6,'B':7.3,'C':1.5}[r]
   choices=[]
   for du in [0,5,-5,10,-10,15,-15]:
    candidates=[]
    for side in [-1,1]:
     u=u0+du;a=angle(c,r,u);w=14 if r!='C' else 17;d=20 if r!='C' else 18;t=shift+side*(gap+w/2)
     b=dict(id=f'{c}-shared-{r}-{j}-{side}',chapter=c,shared=True,entry=False,route=r,x=line(c,r,u)+math.cos(a)*t,z=start+u-math.sin(a)*t-d/2,width=w,depth=d,height=(76+(j%2)*13 if r=='A' else 70+j*6 if r=='B' else 38+j*3),angle=a,kind='office' if r!='C' else 'residential',marked=r=='B',glass=r!='C',style=j%3,seed=c*1000+j*39+side,side=side,severe=False,gate=j,opening=shift,gap=gap,routeZ=start+u)
     if free(b,r):candidates.append(b)
    choices.append(candidates)
   best=max(choices,key=len);placed.extend(best);gates.extend(best)
  # Buildings around the corridor follow parcels, with courtyards between groups.
  for j,u in enumerate(range(112,281,23)):
   for side in [-1,1]:
    a=angle(c,r,u);w=15+(j%3)*2;d=20+(j%2)*4;clear={'A':8.2,'B':12,'C':19}[r];t=side*(clear+w/2)
    b=dict(id=f'{c}-shared-{r}-side-{j}-{side}',chapter=c,shared=True,entry=False,route=r,x=line(c,r,u)+math.cos(a)*t,z=start+u-math.sin(a)*t-d/2,width=w,depth=d,height=(82+(j%3)*12 if r=='A' else 66+(j%3)*9 if r=='B' else 30+(j%3)*7),angle=a,kind='office' if r!='C' else 'residential',marked=r=='B',glass=r!='C',style=j%3,seed=c*2000+j*31+side,side=side,severe=False)
    if free(b,r):placed.append(b)
 # A middle layer encloses the corridors without putting towers in the flight openings.
 for r in ['A','B','C']:
  for j,u in enumerate(range(118,281,26)):
   for side in [-1,1]:
    a=angle(c,r,u);w=18;d=22;t=side*(34+w/2)
    b=dict(id=f'{c}-shared-{r}-middle-{j}-{side}',chapter=c,shared=True,entry=False,route=r,x=line(c,r,u)+math.cos(a)*t,z=start+u-math.sin(a)*t-d/2,width=w,depth=d,height=(92+j%3*8 if r=='A' else 78+j%3*8 if r=='B' else 37+j%3*4),angle=a,kind='office' if r!='C' else 'residential',marked=r=='B',glass=r!='C',style=j%3,seed=c*3000+j*23+side,side=side,severe=False)
    if free(b,r):placed.append(b)
 # Retain the skyline except parcels that would invade a route or new footprint.
 kept=[];removed=[]
 for b in world['backdrops'][c]:
  bad=any(overlap(b,o,1) for o in placed)
  if not bad:bad=any(intersects(a,v,b,{'A':7,'B':10,'C':15}[r]) for r,points in routes.items() for a,v in zip(points,points[1:]))
  if bad:removed.append(b)
  else:
   b=dict(b);u=b['z']+b['depth']/2-start
   if 110<u<290:
    r=min(controls,key=lambda r:abs(b['x']-line(c,r,u)))
    if abs(b['x']-line(c,r,u))<65:
     b.update(shared=True,route=r,kind='residential' if r=='C' else 'office',glass=r!='C',marked=r=='B')
   kept.append(b)
 for r in ['B','C']:
  if c==1 and r=='B':continue
  u=216;x=line(c,r,u);data['rests'].append(dict(id=f'city-{c}-{r}',chapter=c,route=r,x=x,z=start+u,radius=7 if r=='B' else 10))
 for j,u in enumerate(range(109,280,12)):
  r='C';a=angle(c,r,u)
  for side in [-1,1]:
   t=side*(12+(j%3)*2);x=line(c,r,u)+math.cos(a)*t;z=start+u-math.sin(a)*t
   if any(intersects([x,z],[x,z],b,2) for b in placed+kept):continue
   if any(math.dist([x,z],restp)<12 for restp in [[r['x'],r['z']] for r in data['rests'] if r['chapter']==c]):continue
   data['vegetation'].append(dict(tree=True,decorative=True,x=x,z=z,height=17+(j%4)*2,seed=c*91+j*7+side,depth=0))
 # Three real interior corridors, joined at u=110 and u=290. Clear their swept envelopes.
 branches={}
 for r in controls:
  branches[r]=[]
  for lane in [-1,0,1]:
   points=[]
   for u in range(110,291,2):
    envelope=math.sin(math.pi*(u-110)/180)**2
    shift=lane*{'A':18,'B':28,'C':24}[r]*envelope+(3*math.sin((u-110)/180*math.pi*2)*envelope if lane==1 else 0)
    points.append([line(c,r,u)+shift,start+u])
   branches[r].append(points)
 def on_branch(b):
  return any(intersects(a,v,b,3.5 if r=='A' else 4.5 if r=='B' else 5.5) for r in controls for pts in branches[r] for a,v in zip(pts,pts[1:]))
 placed=[b for b in placed if b.get('entrance') or not on_branch(b)]
 kept=[b for b in kept if not on_branch(b)]
 # Divider islands make the three openings physical, with cross-links between groups.
 for r in controls:
  for j,u in enumerate([155,170,185,200,215,230,245]):
   for side in [-1,1]:
    shift=side*{'A':9,'B':14,'C':12}[r]*math.sin(math.pi*(u-110)/180)**2
    b=dict(id=f'{c}-inner-{r}-{j}-{side}',chapter=c,shared=True,entry=False,route=r,x=line(c,r,u)+shift,z=start+u-4,width=7,depth=8,height=44 if r!='C' else 28,angle=0,kind='office' if r!='C' else 'residential',glass=r!='C',marked=r=='B',style=j%3,seed=c*50+j*7+side,side=side,severe=False)
    if not on_branch(b) and not any(overlap(b,o,0) for o in placed+kept) and not any(intersects(a,v,b,w) for a,v,w in segments):placed.append(b)
 data.setdefault('branches',[]).append(branches)
 data['entrances'].append(entrance);data['buildings'].append(placed);data['backdrops'].append(kept)
 lengths={r:sum(math.hypot(line(c,r,i/10)-line(c,r,(i-1)/10),.1) for i in range(1,3151)) for r in controls}
 data['report'].append(dict(chapter=c,buildings=len(placed),routeBuildings={r:sum(b['route']==r for b in placed) for r in controls},gateBuildings={r:sum(b['route']==r for b in gates) for r in controls},backdropsKept=len(kept),backdropsRemoved=len(removed),lengths=lengths))
(root/'assets/city/shared.json').write_text(json.dumps(data,separators=(',',':')))
print(json.dumps(data['report'],indent=2))
