from pathlib import Path
from PIL import Image
import json,html
root=Path(__file__).resolve().parents[1];out=root/'evidence/city'
for p in out.glob('*.png'):
 Image.open(p).convert('RGB').save(p.with_suffix('.webp'),quality=88)
blocks=['''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Fly Home — shared city validation</title><style>body{background:#122c3b;color:#e7f0e8;font:17px/1.6 system-ui;max-width:1200px;margin:auto;padding:28px}a{color:#a6dbe9}h2{margin-top:2em}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}img{width:100%;height:auto}figure{margin:0}figcaption{font-size:14px}table{border-collapse:collapse}td,th{padding:8px;border:1px solid #52707b}</style><h1>共享城市 · 三条真实航路</h1><p><a href="index.html">进入游戏</a> · <a href="CITY-VALIDATION.md">完整说明与限制</a></p><p>同一世界入口分流、出口汇合。A 反光玻璃窄通道；B 圆点玻璃较宽通道；C 住宅绿地长绕行与指定停歇点。</p><p>浏览器模拟桌面、手机竖屏及横屏；未使用实体手机。当前网络无法访问 GitHub Pages，未声称线上实测。</p><h2>实际世界布局</h2><img style="max-width:760px" src="assets/city/layout.svg"><h2>航程验证</h2><table><tr><th>路线</th><th>完整飞行时间</th><th>剩余体力</th><th>生命</th></tr>''']
for r in json.loads((out/'model.json').read_text()):blocks.append(f'<tr><td>{r["route"]}</td><td>{r["time"]:.2f} s</td><td>{r["energy"]:.2f}</td><td>{r["health"]}</td></tr>')
blocks.append('</table><p>自动转向测试输入，读卡期间不计飞行时间；数值为游戏设计，不是科学测量。</p>')
def pics(names):
 blocks.append('<div class="grid">')
 for name in names:
  p=out/f'{name}.webp'
  if p.exists():blocks.append(f'<figure><a href="evidence/city/{p.name}"><img loading="lazy" src="evidence/city/{p.name}"></a><figcaption>{html.escape(name)}</figcaption></figure>')
 blocks.append('</div>')
for r in 'ABC':
 blocks.append(f'<h2>{r} · 同视角修改前后</h2>');pics([f'{d}-{r}-{v}' for d in ['desktop','portrait','landscape'] for v in ['before','after']])
 blocks.append(f'<h2>{r} · 连续实际轨迹截图</h2>');pics([f'flight-{r}-{i:02}' for i in range(11)])
if (out/'browser.json').exists():
 data=json.loads((out/'browser.json').read_text());blocks.append('<h2>串行浏览器性能</h2><p>固定场景，20 帧预热、60 帧采样。CPU Canvas 绘制时间，不代表实体手机帧率。</p><table><tr><th>尺寸</th><th>版本</th><th>路线</th><th>平均 ms</th><th>P95 ms</th></tr>')
 for p in data['performance']:blocks.append(f'<tr><td>{p["device"]}</td><td>{p["version"]}</td><td>{p["route"]}</td><td>{p["meanMs"]:.2f}</td><td>{p["p95Ms"]:.2f}</td></tr>')
 blocks.append('</table><p><a href="evidence/city/browser.json">完整浏览器结果</a> · <a href="evidence/city/camera.json">投影回归结果</a></p>')
(root/'city.html').write_text(''.join(blocks))
