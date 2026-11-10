"""Embed the generated building assets and refresh the self-contained offline game."""
from pathlib import Path
import json,base64
root=Path(__file__).resolve().parents[1]
p=root/'index.html';s=p.read_text();a=s.index('const BUILDING_ART=');b=s.index(';\nclass FlightRenderer',a)
s=s[:a]+'const BUILDING_ART='+(root/'assets/buildings/embedded.json').read_text()+s[b:];p.write_text(s)
skies={n:'data:image/webp;base64,'+base64.b64encode((root/f'assets/sky/{n}-small.webp').read_bytes()).decode() for n in ['day','night','dawn','dusk']}
offline=s
for name in ['glass','light','green','pond','wetland']:
 asset=f'assets/area-previews/{name}.webp'
 if (root/asset).exists(): offline=offline.replace(asset,'data:image/webp;base64,'+base64.b64encode((root/asset).read_bytes()).decode())
(root/'fly-home-offline.html').write_text(offline.replace('<script>','<script>window.FLY_SKIES='+json.dumps(skies)+';</script><script>',1))
print('Embedded building art; offline version synchronized')
