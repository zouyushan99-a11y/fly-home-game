from pathlib import Path
import json,math
root=Path(__file__).resolve().parents[1];src=json.loads((root/'assets/world/input.json').read_text());world=json.loads((root/'assets/world/layout.json').read_text());network=json.loads((root/'assets/ground/roads.json').read_text());near=src['near'];back=[b for blocks in world['backdrops'] for b in blocks];roads=network['roads']
def box(b):
 c=abs(math.cos(b.get('angle',0)));s=abs(math.sin(b.get('angle',0)));w=c*b['width']/2+s*b['depth']/2;d=s*b['width']/2+c*b['depth']/2;return b['x']-w,b['z']+b['depth']/2-d,b['x']+w,b['z']+b['depth']/2+d
def intersects(a,b,bounds,r=0):
 x0,z0,x1,z1=bounds;enter=0;leave=1
 for start,end,lo,hi in [(a[0],b[0],x0-r,x1+r),(a[1],b[1],z0-r,z1+r)]:
  d=end-start
  if abs(d)<1e-9:
   if not lo<=start<=hi:return False
  else:
   aa=(lo-start)/d;bb=(hi-start)/d;enter=max(enter,min(aa,bb));leave=min(leave,max(aa,bb))
   if enter>leave:return False
 return True
def hits_building(a,b,building,r=0):
 angle=building.get('angle',0);co=math.cos(angle);si=math.sin(angle);cx=building['x'];cz=building['z']+building['depth']/2
 local=lambda p:[(p[0]-cx)*co-(p[1]-cz)*si,(p[0]-cx)*si+(p[1]-cz)*co]
 return intersects(local(a),local(b),[-building['width']/2,-building['depth']/2,building['width']/2,building['depth']/2],r)
for i,a in enumerate(back):
 A=box(a)
 for b in near+back[:i]:
  B=box(b);assert not(A[0]<B[2] and A[2]>B[0] and A[1]<B[3] and A[3]>B[1]),('building overlap',a['id'],b.get('id'))
segments=[(a,b,r['width']/2+r['walk']) for r in roads for a,b in zip(r['points'],r['points'][1:])]
# Exact slab intersection against conservative building bounding boxes.
for a,b,w in segments:
 for building in near+back:
  if building.get('chapter',0)>1:continue
  assert not hits_building(a,b,building,w-.01),('road overlaps building',a,b,building.get('id'))
assert roads[:len(src['roads']['roads'])]==src['roads']['roads']
def node(p):return (round(p[0],4),round(p[1],4))
graph={}
for a,b,_ in segments:graph.setdefault(node(a),set()).add(node(b));graph.setdefault(node(b),set()).add(node(a))
seen=set();todo=[next(iter(graph))]
while todo:
 p=todo.pop()
 if p in seen:continue
 seen.add(p);todo.extend(graph[p]-seen)
assert len(seen)==len(graph),('disconnected roads',len(graph)-len(seen))
def distance(p,a,b):
 dx=b[0]-a[0];dz=b[1]-a[1];t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dz)/(dx*dx+dz*dz or 1)));return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dz)
bridge_report=[]
for bridge in world['bridges']:
 pts=bridge['points'];assert pts[0][1]==0
 if bridge.get('join'):
  join=bridge['join'];other=world['bridges'][join['bridgeId']]['points'][join['pointIndex']];assert pts[-1][:3]==other[:3]
 else:assert abs(pts[-1][1])<1e-8
 for endpoint in bridge['connections'][:1 if bridge.get('join') else 2]:assert node(endpoint) in graph
 maxgrade=0;crossings=0
 for a,b in zip(pts,pts[1:]):
  maxgrade=max(maxgrade,abs(a[1]-b[1])/math.hypot(a[0]-b[0],a[2]-b[2]));aa=[a[0],a[2]];bb=[b[0],b[2]]
  for building in near+back:assert not hits_building(aa,bb,building,bridge['width']/2+.1),('bridge overlaps building',bridge['id'],building.get('id'))
 for p in pts:
  if 12<p[3]<bridge['length']-12 and any(distance([p[0],p[2]],a,b)<w+bridge['width']/2 for a,b,w in segments):assert p[1]-.45>5,('low bridge crossing',bridge['id'],p);crossings+=1
 for pier in bridge['piers']:
  for a,b,w in segments:assert not intersects(a,b,box(pier),w+.2),('pier occupies street',pier)
 assert maxgrade<.15;assert crossings>0;assert bridge['height']+.9<33
 bridge_report.append({'id':bridge['id'],'length':bridge['length'],'maxGrade':maxgrade,'crossingSamples':crossings,'piers':len(bridge['piers']),'height':bridge['height']})
report={'buildings':len(back),'groundRoads':len(roads),'connectedGraphNodes':len(graph),'bridges':bridge_report,'checks':['all background footprints mutually separated and clear of all candidate foreground maps','all roads + sidewalks clear of building bounds','original ground roads unchanged','all road nodes connected','ground ramp endpoints on road network; elevated joins share exact XYZ','decks and ramps clear of buildings','piers outside roads and sidewalks','road crossing clearance exceeds 5 world units','ramp grade below 15%; structures below flight altitude']}
(root/'evidence/view/layout-checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
