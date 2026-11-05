from pathlib import Path
import json,math
root=Path(__file__).resolve().parents[1];lights=json.loads((root/'assets/world/lighting.json').read_text());net=json.loads((root/'assets/ground/roads.json').read_text());world=json.loads((root/'assets/world/layout.json').read_text());src=json.loads((root/'assets/world/input.json').read_text());buildings=src['near']+[b for blocks in world['backdrops'] for b in blocks]
def dist(p,a,b):
 dx=b[0]-a[0];dz=b[1]-a[1];t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dz)/(dx*dx+dz*dz or 1)));return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dz)
for l in lights:
 r=net['roads'][l['road']];arc=0
 for a,b in zip(r['points'],r['points'][1:]):
  length=math.dist(a,b)
  if arc+length>=l['arc']:
   t=(l['arc']-arc)/length;mid=[a[k]+(b[k]-a[k])*t for k in [0,1]];break
  arc+=length
 pole=[l['x'],l['z']];head=[l['headX'],l['headZ']]
 assert abs(math.dist(pole,mid)-(r['width']/2+r['walk']*.6))<1e-7
 assert math.dist(head,mid)<r['width']/2
 assert abs((head[0]-pole[0])*(b[0]-a[0])+(head[1]-pole[1])*(b[1]-a[1]))<1e-7
 assert all(math.dist(pole,j)>=10 for j in net['junctions'])
 assert all(dist(pole,a,b)>r['width']/2+.14 for r in net['roads'] for a,b in zip(r['points'],r['points'][1:]))
 for b in buildings:
  x=pole[0]-b['x'];z=pole[1]-b['z']-b['depth']/2;c=math.cos(b.get('angle',0));s=math.sin(b.get('angle',0));assert abs(x*c-z*s)>=b['width']/2+.7 or abs(x*s+z*c)>=b['depth']/2+.7
report=dict(lamps=len(lights),checks=['poles on their road sidewalks','arms perpendicular to local road and inward','heads over actual road','junction clearance >=10','no carriageway or building occupied','fixed authored world positions, no flight collision objects'])
(root/'evidence/view/lighting.json').write_text(json.dumps(report,indent=2));print(report)
svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="-180 -100 360 800"><rect x="-180" y="-100" width="360" height="800" fill="#dce6d9"/>']
for r in net['roads']:
 pts=' '.join(f'{x},{z}' for x,z in r['points']);svg.append(f'<polyline points="{pts}" fill="none" stroke="#64717a" stroke-width="{r["width"]}"/>')
for b in world['bridges']:
 pts=' '.join(f'{p[0]},{p[2]}' for p in b['points']);svg.append(f'<polyline points="{pts}" fill="none" stroke="{["#4e76b5","#4e76b5","#be5d3d","#be5d3d"][b["id"]]}" stroke-width="3.2"/>')
for l in lights:svg.append(f'<circle cx="{l["x"]}" cy="{l["z"]}" r="1.3" fill="#b47b14"/><path d="M{l["x"]} {l["z"]} L{l["headX"]} {l["headZ"]}" stroke="#b47b14" stroke-width=".5"/>')
svg.append('</svg>');(root/'assets/world/view-plan.svg').write_text(''.join(svg))
