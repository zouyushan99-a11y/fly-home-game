from pathlib import Path
from PIL import Image
import json
root=Path(__file__).resolve().parents[1];out=root/'evidence/education'
for p in out.glob('*.png'):Image.open(p).convert('RGB').save(p.with_suffix('.webp'),'WEBP',quality=90,method=4)
topics=json.loads((root/'assets/education/topics.json').read_text())
s=['''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fly Home · 知识展板与学习旅程</title><style>body{font:16px/1.7 system-ui;background:#112b3a;color:#eff1e4;margin:auto;max-width:1200px;padding:24px}h1,h2{line-height:1.3}a{color:#c8e2c4}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}figure{margin:0;background:#204252;padding:12px;border-radius:12px}img{width:100%;max-height:760px;object-fit:contain}section{margin:40px 0}figcaption{font-size:14px}.note{padding:18px;background:#35524e;border-radius:12px}table{border-collapse:collapse;width:100%}td,th{padding:10px;border-bottom:1px solid #4d6771;text-align:left}</style><h1>让每次飞行都有所发现</h1><p>Fly Home · 六主题图文展板与香港保育知识总结</p><p><a href="index.html?v=education">开始试玩</a> · <a href="fly-home-offline.html?v=education">自包含离线版</a> · <a href="EDUCATION-VALIDATION.md">完整测试报告</a> · <a href="assets/education/SOURCES.md">来源核验记录</a></p><p class="note">三份指定 HKBWS 原始来源均被本环境网络代理阻断，未取得原文。本版按需求省略未核实统计数字，并保留实际来源链接及公民科学说明。没有使用实体手机；线上页面未实际验证。</p><section><h2>本轮改进</h2><p>每个主题都有解释性原创插图、影响、原因及解决办法。英文主体 56～63 词；繁体中文同步。弹窗冻结真实游戏状态，玩家自行继续。碰撞和接近触发共用去重队列，绕过停歇点或特定场景也不会漏掉知识。现有城市画面、操控、路线、资源和重聚结尾保留。</p></section>''']
def gallery(title,items,note=''):
 s.append(f'<section><h2>{title}</h2><p>{note}</p><div class="grid">')
 for name,label in items:
  path=f'evidence/education/{name}.webp';assert (root/path).exists(),path;s.append(f'<figure><a href="{path}"><img loading="lazy" src="{path}" alt="{label}"></a><figcaption>{label}</figcaption></figure>')
 s.append('</div></section>')
gallery('从简短提示到知识展板',[('desktop-before','修改前：城市入口提示'),('desktop-glass-zh','修改后：完整玻璃知识展板')],'同一城市入口与桌面尺寸。新版不再把主知识卡写成选路操作提示。')
gallery('六个主题',[(f'desktop-{id}-zh',t['title'][0]) for id,t in topics.items()])
gallery('手机阅读与横屏',[(f'{d}-glass-en',label) for d,label in [('portrait','竖屏：图文分区，固定继续按钮'),('landscape','横屏：图文并排，内部滚动')]],'中英文内容等量保留，手机不会被替换成一两句短提示。知识卡可切换语言和打开帮助，暂停返回后保留当前展板。')
gallery('学习总结与证据',[('desktop-summary-zh','成功总结：已读知识与保育行动'),('desktop-summary-evidence-en','公民科学说明及原始来源'),('portrait-failure-summary','失败总结：只回顾实际读过的知识')],'总结截图使用受控已读状态检查排版；真实完整旅程已另行测试。截图为浏览器原尺寸 PNG 的 WebP 导出（质量 90，无缩放）。')
s.append('<section><h2>测试结果</h2><p>桌面 1280×720、竖屏 390×844、横屏 844×390，各完成 A/B/C。每条旅程六主题均只显示一次；模拟阅读 10 秒，状态和世界像素完全不变。实际页面以真实 RAF 阅读 7 秒，无自动关闭，键盘/触屏选择路线正常；横屏另测离线版。</p><table><tr><th>路线</th><th>生命</th><th>剩余体力</th><th>飞行用时（不含阅读）</th></tr>')
for j in json.loads((out/'model.json').read_text())['journeys']:s.append(f'<tr><td>{j["route"]}</td><td>{j["health"]}</td><td>{j["energy"]:.3f}</td><td>{j["seconds"]:.2f} 秒</td></tr>')
s.append('</table><p>与本轮修改前一致，数值属于游戏设计，不是科学测量。</p><p>'+ ' · '.join(f'<a href="evidence/education/{x}.json">{x}.json</a>' for x in ['model','browser','live','summary','preservation'])+'</p><p>此外覆盖碰撞优先、致命碰撞、重复触发、跳过场景兜底、暂停/帮助/双语、成功/失败、跳过动画与重新开始。渲染器源代码与基线完全相同。</p></section><section><h2>仍存在的限制</h2><p>尚无实体手机或学生用户研究。HKBWS 统计原文未能核实，因此本版不展示数字卡；未来必须核对原报告的范围、时期、方法和数字后再启用。当前网络限制也阻止 GitHub Pages 线上核验，推送成功不能视为线上实测。</p></section></html>')
(root/'education.html').write_text(''.join(s))
