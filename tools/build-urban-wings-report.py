from pathlib import Path
import json,math
from PIL import Image
D=json.loads(Path('assets/city/shared.json').read_text());out=Path('evidence/urban-wings');out.mkdir(exist_ok=True)
for chapter in [0,1]:
 parts=['<svg xmlns="http://www.w3.org/2000/svg" width="850" height="900"><rect width="100%" height="100%" fill="#18333e"/><g transform="translate(260,830) scale(2,-2.4)">']
 for b in D['buildings'][chapter]:parts.append(f'<rect x="{b["x"]-b["width"]/2}" y="{b["z"]-chapter*315}" width="{b["width"]}" height="{b["depth"]}" fill="#8aa0a4"/>')
 for r,color in [('A','#6bc6ec'),('B','#fff0a5'),('C','#7ed9a0')]:
  for lane,pts in enumerate(D['branches'][chapter][r]):parts.append(f'<polyline points="'+ ' '.join(f'{x},{z-chapter*315}' for x,z in pts)+f'" fill="none" stroke="{color}" stroke-width="1.6"/>')
 parts.append('</g><text x="30" y="35" fill="white" font-size="22">Urban Wings — '+('Day' if chapter==0 else 'Night')+' / A · B · C × 3 paths</text></svg>');(out/f'paths-{chapter}.svg').write_text(''.join(parts))
for p in out.glob('*.png'):Image.open(p).convert('RGB').save(p.with_suffix('.webp'),quality=90)
rows=json.loads((out/'model.json').read_text());body='<html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Urban Wings · flight views and paths</title><style>body{font:18px system-ui;background:#18333e;color:white;margin:30px}img{max-width:100%}a{color:#aee7e8}td,th{padding:10px}</style><h1>Urban Wings</h1><p><a href="index.html">试玩</a> · <a href="URBAN-WINGS-VALIDATION.md">验证记录</a></p><h2>同一城市内的多通路</h2>'
for c in [0,1]:body+=f'<img loading="lazy" src="evidence/urban-wings/paths-{c}.svg">'
body+='<h2>九种通路完整航程模拟</h2><table><tr><th>路线</th><th>区内通路</th><th>用时秒</th><th>剩余体力</th></tr>'
for r in rows:body+=f'<tr><td>{r["route"]}</td><td>{r["lane"]+1}</td><td>{r["time"]:.2f}</td><td>{r["energy"]:.2f}</td></tr>'
body+='</table><p>每个编号在白天与夜间分别实际飞行；松开输入不会自动横移。所有数值为游戏设计。</p><p><a href="evidence/urban-wings/browser.json">54 次浏览器航程</a> · <a href="evidence/urban-wings/view-check.json">镜头安全与性能</a> · <a href="evidence/urban-wings/entry.json">键盘／触屏入口</a></p>'
for p in out.glob('*.webp'):body+=f'<h3>{p.stem}</h3><img loading="lazy" src="{p.as_posix()}">'
Path('urban-wings.html').write_text(body)
