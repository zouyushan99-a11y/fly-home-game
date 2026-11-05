"""Deterministic sidewalk fixtures derived from connected road centerlines."""
from pathlib import Path
import json,math,runpy
root=Path(__file__).resolve().parents[1]
net=json.loads((root/'assets/ground/roads.json').read_text());world=json.loads((root/'assets/world/layout.json').read_text());near=json.loads((root/'assets/world/input.json').read_text())['near'];buildings=near+[b for bs in world['backdrops'] for b in bs]
def dist(p,a,b):
 dx=b[0]-a[0];dz=b[1]-a[1];t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dz)/(dx*dx+dz*dz or 1)));return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dz)
def inside(p,b):
 x=p[0]-b['x'];z=p[1]-b['z']-b['depth']/2;c=math.cos(b.get('angle',0));s=math.sin(b.get('angle',0));return abs(x*c-z*s)<b['width']/2+.7 and abs(x*s+z*c)<b['depth']/2+.7
lights=[]
for ri,r in enumerate(net['roads']):
 arc=0;nexts=12
 for a,b in zip(r['points'],r['points'][1:]):
  length=math.dist(a,b)
  if length<1e-8:continue
  dx=(b[0]-a[0])/length;dz=(b[1]-a[1])/length
  while nexts<=arc+length:
   t=(nexts-arc)/length;center=[a[k]+(b[k]-a[k])*t for k in range(2)]
   for side in [-1,1]:
    offset=r['width']/2+r['walk']*.6;p=[center[0]+side*dz*offset,center[1]-side*dx*offset]
    if not -70<p[1]<630 or any(math.dist(p,j)<10 for j in net['junctions']) or any(inside(p,v) for v in buildings):continue
    if any(math.hypot(p[0]-v['x'],p[1]-v['z'])<14 for v in lights):continue
    if any(dist(p,u,v)<other['width']/2+.15 for other in net['roads'] for u,v in zip(other['points'],other['points'][1:])):continue
    headOffset=max(0,r['width']/2-.5)
    lights.append(dict(x=p[0],z=p[1],headX=center[0]+side*dz*headOffset,headZ=center[1]-side*dx*headOffset,road=ri,arc=nexts,side=side,baseY=0,depth=0,lamp=True))
   nexts+=30
  arc+=length
(root/'assets/world/lighting.json').write_text(json.dumps(lights,separators=(',',':')))
p=root/'index.html';s=p.read_text();start=s.find('const STREET_LIGHTS=');end=s.index('const WORLD_LAYOUT=');s=s[:start if start>=0 else end]+'const STREET_LIGHTS='+json.dumps(lights,separators=(',',':'))+';\n'+s[end:];p.write_text(s)
print('Stable sidewalk lamps:',len(lights))
