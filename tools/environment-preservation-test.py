from pathlib import Path
import subprocess,json
old=subprocess.check_output(['git','show','6597a8f:index.html'],text=True);new=Path('index.html').read_text()
def between(s,a,b):return s[s.index(a):s.index(b,s.index(a))]
checks={
 'journey_logic_unchanged_except_default_view':between(old,'class Journey','const palettes=')==between(new,'class Journey','const palettes=').replace("this.viewMode='third'","this.viewMode=this.viewMode||'first'"),
 'collision_algorithm_unchanged':between(old,'function buildingHitTime','// Wildlife positions')==between(new,'function buildingHitTime','// Wildlife positions'),
 'educational_content_unchanged':next(l for l in old.splitlines() if l.startswith('const EDUCATION_CONTENT='))==next(l for l in new.splitlines() if l.startswith('const EDUCATION_CONTENT=')),
 'quiz_logic_unchanged':between(old,'const LEARNING_BANK=','const routes={')==between(new,'const LEARNING_BANK=','const routes={'),
 'ending_unchanged':between(old,'function renderEnding()','function updateUI()')==between(new,'function renderEnding()','function updateUI()')
}
base=json.loads(subprocess.check_output(['git','show','6597a8f:assets/city/shared.json'],text=True));now=json.loads(Path('assets/city/shared.json').read_text())
for key in ['controls','entrances','branches','rests']:checks[key+'_unchanged']=base[key]==now[key]
assert all(checks.values()),checks
Path('evidence/environment/preservation.json').write_text(json.dumps(checks,indent=2));print('PASS preservation',checks)
