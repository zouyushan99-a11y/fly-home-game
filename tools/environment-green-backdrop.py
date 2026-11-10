from pathlib import Path
import json,subprocess
p=Path('assets/city/shared.json');world=json.loads(p.read_text());baseline=json.loads(subprocess.check_output(['git','show','6597a8f:assets/city/shared.json'],text=True));original={b['id']:b for group in baseline['backdrops'] for b in group};changes=[]
for group in world['backdrops'][:2]:
 for b in group:
  if b['x']>145:
   b.update(height=22+(b['seed']%5)*2,kind='residential',glass=False)
   changes.append({'id':b['id'],'heightBefore':original[b['id']]['height'],'heightAfter':b['height']})
p.write_text(json.dumps(world,separators=(',',':')));Path('evidence/environment/green-backdrop.json').write_text(json.dumps(changes,indent=2))
