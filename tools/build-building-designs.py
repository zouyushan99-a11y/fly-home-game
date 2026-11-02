"""Original architectural drawings and transparent facade/roof atlases. No external art."""
from pathlib import Path
import json,base64
root=Path(__file__).resolve().parents[1]/'assets/buildings';root.mkdir(parents=True,exist_ok=True)
specs=[('office','Harbour Prism',24,56,20,'#b6c7cc','#3f6578'),('residential','Garden Terraces',24,42,18,'#d7c6ad','#5c756e'),('commercial','Market Arcade',30,48,24,'#c6a586','#8c5948'),('stepped','Sky Gardens',28,70,24,'#b4c4c9','#365b70'),('village','Courtyard House',18,10,14,'#e6d6b2','#a5674d'),('public','Wetland Pavilion',30,14,24,'#d8ddc7','#65815b')]
def rect(x,y,w,h,c,extra=''):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" {extra}/>'
def svg(w,h,body):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>'
data={}
for kind,name,w,h,d,wall,accent in specs:
 faces={}
 for face in ['front','side']:
  cols=4 if face=='front' else 3
  body='';holes=[]
  floors=2 if kind=='village' else max(2,round(h/3.5))
  pitch=440/floors;cw=256/cols
  for row in range(floors):
   for col in range(cols):
    x=col*cw+10;y=24+row*pitch;ww=cw-20;hh=pitch-13
    if kind in ['office','stepped']:x=col*cw+3;ww=cw-6;hh=pitch-4
    if kind=='public':hh=pitch-18;ww=cw-15
    holes.append(f'M{x},{y}h{ww}v{hh}h{-ww}z')
  # Even-odd holes leave the live sky layer visible in glass panes.
  body+=f'<path fill="{wall}" fill-rule="evenodd" d="M0,0H256V512H0Z '+''.join(holes)+'"/>'
  for row in range(floors):
   y=24+row*pitch
   body+=rect(0,y-4,256,3,accent)
   for col in range(cols):
    x=col*cw+10;ww=cw-20
    if kind in ['office','stepped']:x=col*cw+3;ww=cw-6
    body+=rect(x+ww/2,y,1.5,pitch-13,'#dce2de')
    if kind=='residential':
     body+=rect(x-4,y+pitch-17,ww+8,6,'#eee0c9')+rect(x-4,y+pitch-26,ww+8,2,accent)
     for k in range(5):body+=rect(x+k*ww/4,y+pitch-25,1,8,accent)
     body+=rect(x+ww-9,y+5,12,9,'#bec6c1')+rect(x+ww-7,y+7,8,1,'#69787b')
    if kind=='village':
     body+=rect(x-6,y,5,pitch-14,accent)+rect(x+ww+1,y,5,pitch-14,accent)
    if kind=='stepped' and row%3==0:body+=rect(x,y+pitch-10,ww,7,'#667b51')
  body+=rect(0,0,256,17,accent)+rect(0,468,256,44,wall)
  if kind in ['commercial','office','public']:
   for col in range(4):
    body+=rect(col*64+7,476,49,36,'#35566a')+rect(col*64+5,468,53,8,['#a7614d','#617f72','#d4bc87','#798999'][col])
  else:body+=rect(110,470,36,42,'#5b655c')+rect(116,476,24,20,'#8bafa9')
  body+=rect(0,507,256,5,accent)
  faces[face]=svg(256,512,body)
 roof=rect(0,0,256,256,accent)+rect(8,8,240,240,wall)+rect(17,17,222,222,accent)
 for k in range(4):roof+=rect(30+k*45,55,30,74,'#496b7a')+rect(30+k*45,90,30,2,'#b4c7cd')
 roof+=rect(30,170,64,38,'#b9c1b6')+rect(36,177,52,5,'#718183')
 if kind in ['public','stepped']:roof+=rect(115,165,110,55,'#6b8658')
 if kind=='village':
  roof=rect(0,0,256,256,accent)
  for y in range(0,256,12):roof+=rect(0,y,256,2,'#ce9573')
  roof+=rect(124,0,8,256,'#e0b79b')
 faces['roof']=svg(256,256,roof)
 for face,source in faces.items():(root/f'{kind}-{face}.svg').write_text(source)
 data[kind]={face:'data:image/svg+xml;base64,'+base64.b64encode(source.encode()).decode() for face,source in faces.items()}
 # Orthographic views use a shared 7 px / design metre; all three retain scale.
 sc=7;fw=w*sc;fh=h*sc;sd=d*sc
 sheet=rect(0,0,1100,820,'#f2eee1')+f'<g font-family="system-ui" fill="#203a47"><text x="40" y="45" font-size="26">{name} / {kind}</text><text x="40" y="74">Front · Side · Roof — shared scale 7 px / design metre; {w} × {d} × {h} m</text></g>'
 for face,x,y,ww,hh in [('front',60,700-fh,fw,fh),('side',380,700-fh,sd,fh),('roof',700,190,fw,sd)]:
  src=data[kind][face];shape=''
  if face!='roof' and kind in ['stepped','commercial']:
   if kind=='stepped':
    mid=.76 if face=='front' else .78;top=.51 if face=='front' else .55
    points=[(0,hh),(ww,hh),(ww,hh*.58),(ww*(1+mid)/2,hh*.58),(ww*(1+mid)/2,hh*.24),(ww*(1+top)/2,hh*.24),(ww*(1+top)/2,0),(ww*(1-top)/2,0),(ww*(1-top)/2,hh*.24),(ww*(1-mid)/2,hh*.24),(ww*(1-mid)/2,hh*.58),(0,hh*.58)]
   else:
    upper=.68 if face=='front' else .74;points=[(0,hh),(ww,hh),(ww,hh*.75),(ww*(1+upper)/2,hh*.75),(ww*(1+upper)/2,0),(ww*(1-upper)/2,0),(ww*(1-upper)/2,hh*.75),(0,hh*.75)]
   pts=' '.join(f'{x+xx},{y+yy}' for xx,yy in points);shape=f'<defs><clipPath id="{face}"><polygon points="{pts}"/></clipPath></defs><g clip-path="url(#{face})">'
  sheet+=shape+rect(x,y,ww,hh,'#597e8d')+f'<image href="{src}" x="{x}" y="{y}" width="{ww}" height="{hh}" preserveAspectRatio="none"/>'+('</g>' if shape else '')
  if face=='roof' and kind in ['stepped','commercial']:
   for ratio in ([.76,.51] if kind=='stepped' else [.68]):sheet+=f'<rect x="{x+ww*(1-ratio)/2}" y="{y+hh*(1-ratio)/2}" width="{ww*ratio}" height="{hh*ratio}" fill="none" stroke="#f2eddb" stroke-width="3"/>'
  if face=='front' and kind=='village':sheet+=f'<path d="M{x},{y} L{x+ww/2},{y-17.5} L{x+ww},{y}Z" fill="{accent}"/>'
  sheet+=f'<text x="{x}" y="{y+hh+25}" font-family="system-ui" fill="#203a47">{face}</text>'

 sheet+=f'<text x="60" y="785" font-family="system-ui" fill="#203a47">{kind}: transparent panes receive live sky; roof is a separate UV island. Scale is design reference.</text>'
 (root/f'{kind}-three-views.svg').write_text(svg(1100,820,sheet))
 # A distinct design board precedes the technical sheet and explains material intent.
 text={'office':'Slender mullions · recessed lobby · blue-green glazing','residential':'Balconies · warm stone bands · air conditioners','commercial':'Four shop bays · sheltered podium · upper tower','stepped':'Three setbacks · planted terraces · cool glazing','village':'Two storeys · shutters · terracotta ridge roof','public':'Low pavilion · broad glazing · green roof'}[kind]
 board=rect(0,0,900,700,'#112f40')+f'<text x="40" y="55" fill="#f1d399" font-family="system-ui" font-size="30">{name}</text><text x="40" y="90" fill="#e2e8df" font-family="system-ui">{text}</text>'
 board+=f'<image href="{data[kind]["front"]}" x="220" y="130" width="220" height="470"/><image href="{data[kind]["side"]}" x="440" y="170" width="140" height="430"/><image href="{data[kind]["roof"]}" x="620" y="190" width="190" height="190"/>'
 board+=f'<text x="40" y="650" fill="#e2e8df" font-family="system-ui">Original vector architecture · {w}m facade / {d}m depth / {h}m reference height</text>'
 (root/f'{kind}-design.svg').write_text(svg(900,700,board))
(root/'embedded.json').write_text(json.dumps(data,separators=(',',':')))
(root/'SOURCES.md').write_text('# Building art sources\n\nAll six designs, orthographic sheets and SVG facade/roof textures are original procedural vector artwork created for Fly Home by tools/build-building-designs.py. No third-party architectural images or baked sky photography are used. Window holes are transparent; existing live sky imagery remains a separate rendering layer. Design dimensions are fictional architectural references, not measured buildings. Existing sky sources remain documented in assets/sky/SOURCES.md.\n\nFront and side share floor bands. Runtime repeats the middle elevation band to match actual building height, uses a separate lobby, and maps the roof UV island independently. Setbacks use the existing geometric footprint.\n')
print('Created six designs, six orthographic sheets and 18 facade/roof assets')
