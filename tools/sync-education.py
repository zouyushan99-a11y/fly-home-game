"""Embed authored educational content and SVGs for online/offline parity."""
from pathlib import Path
import json,base64
root=Path(__file__).resolve().parents[1];content=json.loads((root/'assets/education/topics.json').read_text())
for id,item in content.items():item['image']='data:image/svg+xml;base64,'+base64.b64encode((root/f'assets/education/{id}.svg').read_bytes()).decode()
p=root/'index.html';s=p.read_text();a=s.index('const EDUCATION_CONTENT=');b=s.index('\nfor(const [id,t]',a)
s=s[:a]+'const EDUCATION_CONTENT='+json.dumps(content,ensure_ascii=False,separators=(',',':'))+';'+s[b:]
a=s.index('const LEARNING_BANK=');b=s.index('function storageGet',a)
s=s[:a]+'const LEARNING_BANK='+json.dumps(json.loads((root/'assets/education/questions.json').read_text()),ensure_ascii=False,separators=(',',':'))+';\n'+s[b:]
p.write_text(s)
