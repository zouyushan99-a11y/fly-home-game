from pathlib import Path
import json,math,html
root=Path(__file__).resolve().parents[1];out=root/'evidence/urban';world=json.loads((root/'assets/world/layout.json').read_text());roads=json.loads((root/'assets/ground/roads.json').read_text())['roads'];src=json.loads((root/'assets/world/input.json').read_text());m=json.loads((out/'model.json').read_text());b=json.loads((out/'browser.json').read_text());density=json.loads((out/'density.json').read_text())
# Plan and section drawings use the same coordinates/heights as the rendered models.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="900" viewBox="0 0 1000 900"><rect width="1000" height="900" fill="#173446"/><g font-family="sans-serif" fill="#f2e9cf"><text x="25" y="32" font-size="24">城市路网、建筑组团与立交桥 · 俯视连接图</text><text x="25" y="59" font-size="14">灰：地面道路　橙：高架连接　蓝灰：建筑占地　圆点：接地端点（游戏世界单位）</text></g>']
for road in roads:
 pts=' '.join(f'{480+x},{145+z}' for x,z in road['points']);svg.append(f'<polyline points="{pts}" fill="none" stroke="#cac5ad" stroke-width="{road["width"]+road["walk"]*2}" stroke-linejoin="round"/><polyline points="{pts}" fill="none" stroke="#657581" stroke-width="{road["width"]}" stroke-linejoin="round"/>')
def rect(b,ox,oy,k=1):
 x=ox+b['x']*k;y=oy+b['z']*k;return f'<rect x="{x-b["width"]*k/2}" y="{y}" width="{b["width"]*k}" height="{b["depth"]*k}" transform="rotate({-b.get("angle",0)*180/math.pi} {x} {y+b["depth"]*k/2})" fill="#7493a2" stroke="#a6b6b2" stroke-width=".4"/>'
for blocks in world['backdrops'][:2]:
 for building in blocks:svg.append(rect(building,480,145))
seen=set()
for building in src['near']:
 if building['chapter']>1:continue
 key=(building['x'],building['z'],building['width'],building['depth'])
 if key in seen:continue
 seen.add(key);svg.append(rect(building,480,145))
for bridge in world['bridges']:
 pts=' '.join(f'{480+x},{145+z}' for x,y,z,s in bridge['points']);svg.append(f'<polyline points="{pts}" fill="none" stroke="#ecba72" stroke-width="{bridge["width"]+1}" stroke-linejoin="round"/>')
 for x,z in bridge['connections']:svg.append(f'<circle cx="{480+x}" cy="{145+z}" r="5" fill="#f6d599" stroke="#f3ead3"/>')
 x,z=bridge['connections'][0];svg.append(f'<text x="{490+x}" y="{135+z}" fill="#f4d695" font-family="sans-serif" font-size="14">立交桥 {bridge["id"]+1}</text>')
svg.append('</svg>');(root/'assets/world/plan.svg').write_text(''.join(svg))
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="720" viewBox="0 0 1000 720"><rect width="1000" height="720" fill="#173446"/><g font-family="sans-serif" fill="#f2e9cf"><text x="25" y="30" font-size="23">立交桥沿线侧面高度 · 与地面道路连续衔接</text><text x="25" y="55" font-size="14">横轴为沿桥距离，纵轴为高度；游戏世界单位，横纵比例不同。</text></g>']
for bridge in world['bridges']:
 baseline=300+bridge['id']*330;ox=90;k=2.1;ky=6
 svg.append(f'<path d="M{ox},{baseline}H{ox+bridge["length"]*k}" stroke="#bac5b5" stroke-width="3"/><path d="M{ox},{baseline-34*ky}H{ox+bridge["length"]*k}" stroke="#87cbd4" stroke-dasharray="5 7"/><text x="{ox}" y="{baseline-34*ky-10}" fill="#a6d8df" font-family="sans-serif" font-size="14">鸟的固定飞行高度 34</text>')
 for pier in bridge['piers']:
  p=min(bridge['points'],key=lambda v:math.hypot(v[0]-pier['x'],v[2]-pier['z']));x=ox+p[3]*k;svg.append(f'<path d="M{x},{baseline}V{baseline-pier["height"]*ky}" stroke="#b9c0b6" stroke-width="3"/>')
 pts=' '.join(f'{ox+s*k},{baseline-y*ky}' for x,y,z,s in bridge['points']);svg.append(f'<polyline points="{pts}" fill="none" stroke="#edbd78" stroke-width="4"/>')
 svg.append(f'<text x="{ox}" y="{baseline+24}" fill="#f2e9cf" font-family="sans-serif" font-size="15">桥 {bridge["id"]+1}：长 {bridge["length"]:.1f} · 桥面高 6.4 · 两端坡道各 80 · 最大坡度约 12% · 桥墩 {len(bridge["piers"])}</text>')
 svg.append(f'<text x="{ox}" y="{baseline-50}" fill="#f2e9cf" font-family="sans-serif" font-size="13">接入地面道路 ↗</text><text x="{ox+bridge["length"]*k-115}" y="{baseline-50}" fill="#f2e9cf" font-family="sans-serif" font-size="13">↘ 接入地面道路</text>')
svg.append('</svg>');(root/'assets/world/bridge-section.svg').write_text(''.join(svg))
# Terminal housing taper and old/new destination markers.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="760" height="700" viewBox="0 0 760 700"><rect width="760" height="700" fill="#71856a"/><text x="20" y="30" fill="#fff0cb" font-family="sans-serif" font-size="22">末段：村落边缘 → 水岸 → 开阔湿地</text>']
pathx=lambda z:math.sin(z/175)*10+math.sin(z/410)*14
left=[];right=[]
for z in range(1130,1601,10):
 width=30+math.sin(z/31)*2+math.sin(z/73)*3;x=pathx(z);y=60+(z-1130)*1.2;left.append((380+(x-width)*1.2,y));right.append((380+(x+width)*1.2,y))
svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in left+right[::-1])+'" fill="#8da4ac"/>')
for building in world['backdrops'][4]:svg.append(rect(building,380,60-1130*1.2,1.2))
for z,label in [(1170,'末段起点'),(1395,'原终点'),(1575,'新终点')]:
 y=60+(z-1130)*1.2;svg.append(f'<path d="M100,{y}H660" stroke="#e7d5aa" stroke-dasharray="5 5"/><text x="105" y="{y-7}" fill="#fff0cb" font-family="sans-serif" font-size="15">{label}</text>')
svg.append('</svg>');(root/'assets/world/final-plan.svg').write_text(''.join(svg))
rows=[]
for route in 'ABC':
 old=next(r for r in m['journeys'] if r['route']==route and r['version']=='before');new=next(r for r in m['journeys'] if r['route']==route and r['version']=='after');rows.append(f"| {route} | {old['finalSeconds']:.2f} → {new['finalSeconds']:.2f} | {old['energy']:.2f} → {new['energy']:.2f} | {old['totalSeconds']:.2f} → {new['totalSeconds']:.2f} |")
perf=[]
for device in ['desktop','portrait','landscape']:
 for scene in ['day','night','corner','green','final-edge','final-open']:
  old=next(r for r in b['performance'] if r['device']==device and r['scene']==scene and r['version']=='before');new=next(r for r in b['performance'] if r['device']==device and r['scene']==scene and r['version']=='after');perf.append(f"| {device} / {scene} | {old['meanMs']:.2f} → {new['meanMs']:.2f} | {old['p95Ms']:.2f} → {new['p95Ms']:.2f} | {old['rafFPS']:.1f} → {new['rafFPS']:.1f} |")
report='''# Fly Home：延长末段、错落街区与城市立交桥

基线 `215a5dd`。六阶段结构、自然入口、原近景碰撞地图、知识卡、双语、触屏、暂停、玻璃反射及结束流程保留。

## 最后一段

进度边界 140–165 → 140–185，纵向飞行距离 225 → 405 世界单位（1.8 倍）。未降低速度。实际模拟末段约 22.6 → 40.1 秒（包含鸟群让行减速，不包含阅读与手动暂停）。新终点才触发成功和抵达奖励；通过原终点时仍继续飞行。

末段外围新增 32 栋低矮村屋，按组团从入口和村落边缘延伸至水岸，随后退出湿地核心。1 栋横跨阶段入口边界；位置始终存在于世界中，提前可见，不依靠章节切换生成。高度约 6–13，带坡屋顶；均在飞行通道外。

| 路线 | 末段用时 秒：前 → 后 | 抵达后体力：前 → 后 | 全程飞行秒数：前 → 后 |
|---|---|---|---|
'''+ '\n'.join(rows)+'''

模拟采用合理避障控制器，三条路线均健康 100、无重试、无紧急恢复；不代表新玩家成功率。每秒消耗 0.54，绕道、干扰、停歇及抵达 +8 保持原值；表中剩余体力包含抵达奖励。延长部分额外消耗约 9.41 体力，A 在奖励前仍约有 7.75 余量。所有数值是游戏设计。

## 道路和建筑

原有 7 段地面道路保持原坐标，扩展为 19 段连通路网，连接节点图中的分叉由 6 增至 15，独立环路数由 0 增至 8。增加外围街道和连接支路，使原来的支路末端接回路网。主路、外围道路、连接支路使用不同宽度，沿用世界坐标地面纹理与路口材质并集处理。

外围建筑按固定随机种子和街区组团重新规划：城市 182 → 180、夜间 188 → 180、廊道 96 → 82、村落 39 → 38、末段边缘 0 → 32，总数 505 → 512。变化重点是组团与开敞空间，并非均匀加密。

在相同 60×60 单元比较窗口内，城市空单元 1 → 7，夜间 1 → 11；单元密度变异系数城市 0.37 → 0.63、夜间 0.47 → 0.72。更高的差异表现为密集街区与疏朗庭院并存。建筑同时改变横向和前后位置；朝向随街区轴线与外围街道组织，固定于世界坐标。所有新外围建筑与道路、桥梁及全部候选近景地图分开预留占地。

## 立交桥

两座高架连接均从地面街道起坡，再回接地面路网，长度约 349.9 / 356.0 世界单位；桥面最高 6.4，两端坡道各 80，最大坡度约 12%。分别有 14 / 15 个桥墩，坡道部分也有支撑。包含桥面、侧梁、护栏、标线及克制的夜间边缘标记。

跨越支路处桥下净空超过 5；桥墩不占用车道、人行道或斑马线。既有地面道路没有被替换。桥梁与坡道避开建筑，占地检查使用全部候选路线。桥面和护栏最高约 7.3，低于固定飞行高度 34；属于不可触及的低空景观，不新增碰撞、体力或照明干扰事件。

设计文件：`assets/world/plan.svg`（俯视连接）、`bridge-section.svg`（沿线高度）、`final-plan.svg`（末段村屋渐疏）。图中坐标与实际模型一致。布局由自制离线生成器 `tools/plan-urban-world.py` 产生，固定种子 2155185，未使用外部模型素材。

## 实际验证范围

- 三条完整路线模型模拟完成，经过旧终点不结束，新终点正常完成；暂停/知识卡冻结，成功与失败冻结资源和事件，重启清除状态。
- 全部原近景建筑与自然入口几何逐项对比未变。新增外围建筑互不重叠，也不侵入候选近景地图；道路与人行道全宽、桥面、坡道、桥墩分别检测占地。
- 地面道路连接图全部 1762 个节点连通，桥两端位于路网节点且高度为零；坡道高度连续，最大坡度及净空通过检查。
- 桌面 1280×720、手机竖屏 390×844、横屏 844×390：键盘/CDP 触屏入口、知识卡、帮助、双语、暂停、结尾、跳过、减少效果和重新开始通过。
- 正式页面另用正常 RAF 和真实等待验证输入与入口，未注入游戏代码。完整旅程另以 60 Hz 模拟、每 30 步绘制，属于加速回归。
- 连续旅程截图按实际状态推进至 12/15/18、45.5/48/50、150/165/178/184/185.1；没有逐张重置位置与体力。自动关闭知识卡，不冒充正常速度人工全程试玩。
- 桥梁跨近裁剪面专项检查：三个尺寸的投影均有限、在近裁剪面前，没有绘制到地平线上方，Canvas 变换/透明度/滤镜保持正常。屋顶绿色横杠专项回归及完整延长旅程同样通过。
- 网页与内嵌离线版启动、暂停和减少效果 smoke 通过；未核验 file://。

## 性能

相同尺寸与固定场景，修改前后浏览器分开串行运行；每场景 100 帧，前 20 帧预热。软件 Chromium 的绘制 CPU 耗时与 RAF 帧率受虚拟机调度影响，不代表实体手机。新增布局离线生成，建筑、桥面和桥墩几何缓存，继续使用屏外剔除、远景简化和现有纹理缓存；未降低整体画布清晰度。

| 尺寸 / 场景 | 平均 ms：前 → 后 | p95 ms：前 → 后 | RAF FPS：前 → 后 |
|---|---|---|---|
'''+ '\n'.join(perf)+'''

## 限制

- 未使用实体手机或平板；已测试的是 Chromium 视口与触屏模拟。
- 立交桥为游戏尺度景观，不是工程施工模型；未增加动态行人或车辆。
- 背景采用简化立面和距离分级，远处不会像近景建筑一样细致。近景航路保留，因此原挑战开口的排列仍保留。
- 性能按实测列出，部分城市桌面场景约 38–46 FPS；没有宣称所有场景稳定 60 FPS。
- 已尝试访问线上试玩页，但环境代理返回 CONNECT 403，未实际核验线上运行；成功推送不等于已核验 GitHub Pages 部署。
'''
(root/'URBAN-VALIDATION.md').write_text(report)
(root/'assets/world/SOURCE.md').write_text('''# Layout provenance and regeneration

Original deterministic procedural layout; no third-party bridge models. Baseline foreground and roads: repository commit 215a5dd. All road, parcel and bridge coordinates are precomputed once and embedded in index.html.

Regenerate from the repository root:

```
node tools/export-world-input.cjs
python3 tools/plan-urban-world.py
python3 tools/sync-world-layout.py
python3 tools/sync-ground-art.py
python3 tools/sync-building-art.py
node tools/urban-model-test.cjs
python3 tools/urban-layout-test.py
```

The new end progress in layout.json must match STAGE_ENDS[4]. The old natural-layout rebuild check targets the earlier seven-road layout; use the urban suites for this revision.\n''')
parts=['<!doctype html><html lang="zh"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Fly Home · 街区、立交与新终点</title><style>body{font:16px/1.7 system-ui;max-width:1200px;margin:24px auto;padding:16px;background:#173446;color:#f2e9cf}a{color:#acdce1}img{max-width:100%;height:auto}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}figure{margin:0}pre{white-space:pre-wrap;font:14px/1.8 system-ui;background:#204457;padding:20px}</style><h1>Fly Home · 街区、立交桥与新终点</h1><p><a href="index.html">试玩</a> · <a href="URBAN-VALIDATION.md">完整报告</a> · <a href="assets/world/SOURCE.md">布局来源与生成方法</a></p><div class="grid">']
for name in ['plan','bridge-section','final-plan']:parts.append(f'<figure><a href="assets/world/{name}.svg"><img src="assets/world/{name}.svg" alt="{name}"></a></figure>')
parts.append('</div>')
def gallery(title,names):
 parts.append('<h2>'+title+'</h2><div class="grid">')
 for name in names:parts.append(f'<figure><img loading="lazy" src="evidence/urban/{name}.png" alt="{name}"><figcaption>{name}</figcaption></figure>')
 parts.append('</div>')
gallery('同视角修改前后',[f'{d}-{s}-{v}' for d in ['desktop','portrait','landscape'] for s in ['day','night','final-edge','final-open'] for v in ['before','after']])
gallery('连续推进中的立交区域',[f'{d}-journey-{p}' for d in ['desktop','portrait','landscape'] for p in ['12','15','18','45.5','48','50']])
gallery('飞抵新终点：实际旅程状态',[f'{d}-journey-{p}' for d in ['desktop','portrait','landscape'] for p in ['150','165','178','184','185.1']])
parts.append('<h2>数据、测试与限制</h2><pre>'+html.escape(report)+'</pre></html>');(root/'urban.html').write_text(''.join(parts));print('Generated urban.html, URBAN-VALIDATION.md and plan/section SVGs')
