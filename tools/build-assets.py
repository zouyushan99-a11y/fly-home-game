from pathlib import Path
from PIL import Image
import shutil,base64,json
root=Path(__file__).resolve().parents[1]
files={'day':'exec-8cfae7ce-fa20-481e-94be-a4fe3a2a5cf6.png','night':'exec-514f2002-b700-4ac8-bd5b-69b8990d37da.png','dawn':'exec-d5d5b569-ab04-4239-93e7-8a9010e0f207.png','dusk':'exec-e54f9047-e67b-4c62-b90f-7d5ba98ac614.png'}
manifest={};embedded={}
for name,filename in files.items():
 original=root/'assets/sky/originals'/f'{name}.png'
 if not original.exists():shutil.copyfile(Path('/workspace/generated_images')/filename,original)
 im=Image.open(original).convert('RGB')
 for suffix,width,quality in [('',min(1774,im.width),84),('-small',960,78)]:
  resized=im.resize((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS)
  out=root/'assets/sky'/f'{name}{suffix}.webp';resized.save(out,'WEBP',quality=quality,method=6)
  manifest[out.name]={'size':resized.size,'bytes':out.stat().st_size}
 embedded[name]='data:image/webp;base64,'+base64.b64encode((root/'assets/sky'/f'{name}-small.webp').read_bytes()).decode()
 manifest[name+'-original']={'size':im.size,'bytes':original.stat().st_size}
html=(root/'index.html').read_text()
(root/'fly-home-offline.html').write_text(html.replace('<script>', '<script>window.FLY_SKIES='+json.dumps(embedded)+';</script><script>',1))
(root/'assets/sky/manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest,indent=2))
