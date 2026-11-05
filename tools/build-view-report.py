from pathlib import Path
import json,html
from PIL import Image
root=Path(__file__).resolve().parents[1];out=root/'evidence/view'
for p in out.glob('*.png'):
 Image.open(p).convert('RGB').save(p.with_suffix('.webp'),'WEBP',quality=90,method=4)
browser=json.loads((out/'browser.json').read_text());model=json.loads((out/'model.json').read_text())
parts=['''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fly Home · 本轮改进与验证</title><style>body{font:16px/1.65 system-ui;color:#e9f0ef;background:#102632;max-width:1200px;margin:auto;padding:24px}a{color:#a8dbef}h1,h2{line-height:1.3}section{margin:44px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:18px}figure{margin:0;padding:12px;background:#1c3643;border-radius:8px}img{width:100%;height:auto;max-height:720px;object-fit:contain}figcaption{font-size:14px}table{border-collapse:collapse;width:100%}td,th{padding:8px;border-bottom:1px solid #42606b;text-align:left}.scroll{overflow:auto}code{color:#b9dabb}.note{background:#25404b;padding:18px;border-radius:8px}</style><h1>Fly Home：幕墙、转向与城市设施</h1><p><a href="index.html?v=view-update">开始试玩</a> · <a href="VIEW-VALIDATION.md">完整验证报告</a></p><p class="note">本地 Chromium 验证完成；已测试桌面 1280×720、手机竖屏 390×844、横屏 844×390。未使用实体手机。GitHub Pages 访问被本环境代理以 HTTP 403 拒绝，不能声称已验证线上版本。截图由浏览器原尺寸 PNG 导出 WebP（质量 90，无缩放）。</p><section><h2>改了什么</h2><ul><li>未标记城市风险玻璃楼：正侧面连续幕墙，保留昼夜天空反射。村屋与非玻璃公共建筑不受影响。</li><li>左右转向：平滑水平偏转 ±8°，松手回正；地面和全部世界物体共用视角，HUD 固定。</li><li>新增两条接入原高架的匝道，形成 4 条桥路；为视线退让 6 栋背景楼，近景碰撞不变。</li><li>98 盏路灯依真实道路边界和方向布置，暖光向下，不新增游戏干扰。</li></ul></section>''']
def pictures(title,items,note=''):
 parts.append('<section><h2>'+title+'</h2><p>'+note+'</p><div class="grid">')
 for stem,label in items:
  file=f'evidence/view/{stem}.webp';assert (root/file).exists(),file
  parts.append(f'<figure><a href="{file}"><img loading="lazy" src="{file}" alt="{html.escape(label)}"></a><figcaption>{html.escape(label)}</figcaption></figure>')
 parts.append('</div></section>')
pictures('玻璃建筑：同模型、同视角',[(f'desktop-material-{time}-unmarked{suffix}',f'{label} · {version}') for time,label in [('day','白天未标记'),('night','夜间未标记')] for suffix,version in [('-before','修改前'),('','修改后')]],'受控材质展示场景，用于对比立面；不代表普通航路或高架可见性证据。几何和尺寸相同，修改后不再叠加住宅阳台。')
pictures('保留鸟友好标记',[(f'portrait-material-{t}-{m}',f'手机 · {label} · {ml}') for t,label in [('day','白天'),('night','夜间')] for m,ml in [('unmarked','未标记玻璃'),('marked','鸟友好标记玻璃')]])
pictures('水平转向：左、中、右',[(f'desktop-yaw-{v}',label) for v,label in [('left','左转 −8°'),('center','回正 0°'),('right','右转 +8°')]],'固定位置展示相机方向差异。连续输入、快速反向、松开和冻结状态另有自动化检查。')
pictures('正常航路的立交：白天 C 路线',[(f'portrait-journey-{p}',f'手机竖屏 · 旅程进度 {p}') for p in [15,18,20]],'关闭玻璃知识卡后向右进入 C；截图来自同一完整旅程按固定时间步连续推进，没有自由相机。也可在入口接近阶段观察连接匝道。')
pictures('正常航路的立交：夜间 A 路线',[(f'portrait-journey-{p}',f'手机竖屏 · 旅程进度 {p}') for p in [45.5,48,50]],'进入夜间街区，关闭知识卡后向左接近 A。此处包含从白天向夜景的原有渐变；桥梁受真实建筑遮挡，不会穿透显示。')
pictures('道路与照明：同场景前后',[(f'desktop-night-{v}',f'夜间街区 · {label}') for v,label in [('before','修改前'),('after','修改后')]],'相同位置和尺寸，新版本包含最大右转反馈；旧版本只有横移，没有相机偏航。路灯位置的客观验证另见俯视图和 lighting.json。')
parts.append('<section><h2>道路、高架和灯位</h2><p>灰色：既有道路；蓝色：原外围高架；橙色：新增连接匝道；金色点及短线：灯杆和灯臂。布局固定于世界坐标。</p><img style="max-height:1000px" src="assets/world/view-plan.svg" alt="道路、高架连接与路侧灯位俯视图"></section>')
parts.append('<section><h2>玩法与回归结果</h2><p>三种屏幕尺寸均通过知识卡、帮助、暂停、双语、A/B/C 入口、触屏、成功/失败、跳过和重启。近裁剪测试：越界屋顶投影 0、天空区域绿色块像素 0，Canvas 状态正确恢复。</p><table><tr><th>路线</th><th>完成生命</th><th>剩余体力</th><th>旅程用时（秒）</th></tr>')
for j in model['journeys']:
 if j['version']=='after':parts.append(f'<tr><td>{j["route"]}</td><td>{j["health"]}</td><td>{j["energy"]:.2f}</td><td>{j["totalSeconds"]:.2f}</td></tr>')
parts.append('</table><p>三条完整路线的数据均与本轮基线完全一致；资源数值属于游戏设计。模型自动驾驶证明可完成性，不代表所有玩家都能零碰撞。</p></section><section><h2>性能：同尺寸、同场景，串行测试</h2><p>每场景预热 20 帧、统计 80 帧 Canvas 绘制 CPU 时间。相同状态与天空；新版本采用最大 8° 偏航，旧版无偏航反馈。不降低渲染尺寸。云端 Chromium 数据不能视为实体手机帧率。</p><div class="scroll"><table><tr><th>屏幕</th><th>场景</th><th>修改前均值 / P95 ms</th><th>修改后均值 / P95 ms</th></tr>')
for device in ['desktop','portrait','landscape']:
 for scene in ['day','night','corner','green','final-edge','final-open']:
  rows=[next(p for p in browser['performance'] if p['device']==device and p['scene']==scene and p['version']==v) for v in ['before','after']]
  parts.append('<tr><td>'+device+'</td><td>'+scene+'</td>'+''.join(f'<td>{r["meanMs"]:.2f} / {r["p95Ms"]:.2f}</td>' for r in rows)+'</tr>')
parts.append('</table></div><p>新增镜头采样、幕墙和桥梁带来开销；当前城市场景平均绘制时间增加约 0.8～4.0 ms。未承诺所有设备达到固定帧率。</p></section><section><h2>原始证据与限制</h2><p>'+ ' · '.join(f'<a href="evidence/view/{name}.json">{name}.json</a>' for name in ['browser','camera','model','layout-checks','lighting','live','sequences'])+'</p><p>Canvas 采用对象深度排序、立面条带近似与静态灯光池，极端视角仍有透视近似。移动端仅浏览器模拟，线上未实际验证。完整说明见验证报告。</p></section></html>')
(root/'view.html').write_text(''.join(parts))
