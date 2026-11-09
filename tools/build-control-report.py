from pathlib import Path
from PIL import Image
import json
out=Path('evidence/control')
for p in out.glob('*.png'):Image.open(p).convert('RGB').save(p.with_suffix('.webp'),quality=89)
body='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Urban Wings · Flight control validation</title><style>body{font:18px/1.65 system-ui;background:#17323e;color:#eef4ed;max-width:1120px;margin:auto;padding:25px}a{color:#b6e6ea}img{width:100%}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px}td,th{padding:8px;border:1px solid #496470}table{border-collapse:collapse}</style><h1>Urban Wings · 飞行控制修复</h1><p><a href="index.html">进入游戏</a> · <a href="CONTROL-VALIDATION.md">完整测试说明与限制</a></p><p>按住 A/D、←/→ 或触屏箭头转弯，松开后保持新航向。金色「视角」按钮或 V 切换第一／第三人称。撞墙先阻挡，再执行伤害反馈；无敌时间不会让鸟穿墙。</p><p>前进型关卡支持左右转到侧向（±90°），不支持掉头倒飞。镜头在狭窄位置回缩；不会替鸟转向。手机测试为浏览器模拟，未使用实体设备。</p><h2>实际浏览器截图</h2><div class="grid">'''
for d in ['desktop','portrait','landscape']:
 for v in ['first','third']:
  p=out/f'{d}-{v}.webp'
  if p.exists():body+=f'<figure><img loading="lazy" src="{p.as_posix()}"><figcaption>{d} · {v}</figcaption></figure>'
body+='</div><h2>新控制规则下的全程模拟</h2><table><tr><th>环境／区内通路</th><th>成功</th><th>生命</th><th>剩余体力</th><th>用时</th></tr>'
for r in json.loads((out/'journeys.json').read_text()):body+=f'<tr><td>{r["route"]} / {r["lane"]+1}</td><td>{r["success"]}</td><td>{r["health"]}</td><td>{r["energy"]:.2f}</td><td>{r["time"]:.2f}s</td></tr>'
body+='</table><p>自动测试驾驶器只存在于测试脚本，游戏没有自动导航。读卡时间不计入飞行用时，资源数值为游戏设计。</p><h2>可检查的测试记录</h2><ul>'
for f in ['model','corners','browser','entries','camera','geometry','replay-browser','view-check','camera-corners','choices','ui']:
 if (out/f'{f}.json').exists():body+=f'<li><a href="evidence/control/{f}.json">{f}</a></li>'
body+='</ul>'
Path('controls.html').write_text(body)
