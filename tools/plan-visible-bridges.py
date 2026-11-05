"""Two connected elevated feeders through existing flight approach sightlines."""
from pathlib import Path
import json,math
root=Path(__file__).resolve().parents[1]
# Reuse deterministic obstacle-aware routing, without regenerating existing parcels.
exec((root/'tools/plan-urban-world.py').read_text().split('bridges=[]')[0])
layout=json.loads((root/'assets/world/view-planning-input.json').read_text());layout['bridges']=layout['bridges'][:2]
for targetID,sourceSide,sourceZ,crossZ,joinZ in [(0,-1,-45,118,150),(1,1,305,433,495)]:
 old=layout['bridges'][targetID];source=at(spines[sourceSide],sourceZ);idx=min((i for i,p in enumerate(old['points']) if abs(p[1]-6.4)<1e-6),key=lambda i:abs(old['points'][i][2]-joinZ));v=old['points'][idx];target=[v[0],v[2]];cross=at(main,crossZ)
 def penalty(q):
  if q not in roadmask:return 0
  p=world(q)
  return 0 if min(math.dist(p,source),math.dist(p,target),math.dist(p,cross))<5 else 18
 savedBlocked=blocked.copy()
 for qx in range(NX):
  for qz in range(NZ):
   q=(qx,qz);p=world(q)
   if math.dist(p,target)>7 and any(math.hypot(p[0]-v[0],p[1]-v[2])<5 for v in old['points']):blocked.add(q)
 points=find(source,cross,penalty)+find(cross,target,penalty)[1:]
 blocked=savedBlocked
 clean=[];indices={}
 for p in points:
  k=tuple(p)
  if k in indices:clean=clean[:indices[k]+1];indices={tuple(q):i for i,q in enumerate(clean)}
  else:indices[k]=len(clean);clean.append(p)
 points=clean
 for _ in range(3):points=[points[0]]+[[sum([points[i-1][k],2*points[i][k],points[i+1][k]])/4 for k in range(2)] for i in range(1,len(points)-1)]+[points[-1]]
 lengths=[0]
 for a,b in zip(points,points[1:]):lengths.append(lengths[-1]+math.dist(a,b))
 contacts=[s for p,s in zip(points,lengths) if road_distance(p)<1.8 and s>12];ramp=min(80,min(contacts,default=100)-3)
 if ramp<67:raise ValueError(('Insufficient ramp',targetID,ramp))
 vertices=[[p[0],6.4*(lambda t:t*t*(3-2*t))(min(1,s/ramp)),p[1],s] for p,s in zip(points,lengths)]
 piers=[];last=-30
 for p in vertices:
  if p[1]>1.3 and p[3]-last>20 and road_distance([p[0],p[2]])>3.8 and math.dist([p[0],p[2]],target)>8:piers.append(dict(x=p[0],z=p[2],height=p[1]-.5,width=1.6,depth=1.6));last=p[3]
 bridge=dict(id=len(layout['bridges']),width=3.2,height=6.4,rampLength=ramp,length=lengths[-1],points=vertices,piers=piers,crossing=cross,connections=[source,target],join=dict(bridgeId=targetID,pointIndex=idx),side=sourceSide)
 layout['bridges'].append(bridge);print('feeder',bridge['id'],'length',round(lengths[-1],1),'ramp',ramp,'cross',cross)
# Remove only peripheral parcels intersecting new bridge reservation. Foreground untouched.
removed=[]
for group in layout['backdrops']:
 for b in group[:]:
  x0,z0,x1,z1=bounds(b,3)
  if any(min(a[0],c[0])<x1 and max(a[0],c[0])>x0 and min(a[2],c[2])<z1 and max(a[2],c[2])>z0 for br in layout['bridges'][2:] for a,c in zip(br['points'],br['points'][1:])):group.remove(b);removed.append(b['id'])
layout['bridgeSightlineSetbacks']=sorted(set(layout.get('bridgeSightlineSetbacks',[])+removed))
(root/'assets/world/layout.json').write_text(json.dumps(layout,separators=(',',':')))
print('Background setbacks',removed)
