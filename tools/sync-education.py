"""Embed authored educational content and SVGs for online/offline parity."""
from pathlib import Path
import json,base64
root=Path(__file__).resolve().parents[1];content=json.loads((root/'assets/education/topics.json').read_text())
for id,item in content.items():item['image']='data:image/svg+xml;base64,'+base64.b64encode((root/f'assets/education/{id}.svg').read_bytes()).decode()
p=root/'index.html';s=p.read_text();a=s.find('const EDUCATION_CONTENT=');b=s.index('const routes={');s=s[:a if a>=0 else b]+'const EDUCATION_CONTENT='+json.dumps(content,ensure_ascii=False,separators=(',',':'))+';\nfor(const [id,t] of Object.entries(EDUCATION_CONTENT))lessons[id]={title:t.title,text:[0,1].map(i=>[t.impact[i],t.why[i],t.solution[i]].join(" ")),short:t.impact};\n'+s[b:];p.write_text(s)
