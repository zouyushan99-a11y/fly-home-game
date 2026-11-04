from pathlib import Path
import json,html
root=Path(__file__).resolve().parents[1];out=root/'evidence/forks'
m=json.loads((out/'model.json').read_text());b=json.loads((out/'browser.json').read_text());live=json.loads((out/'live.json').read_text())
rows=[]
for route in 'ABC':
 old=next(x for x in m['routes'] if x['route']==route and x['version']=='before');new=next(x for x in m['routes'] if x['route']==route and x['version']=='after')
 rows.append(f"| {route} | {old['seconds']:.1f} → {new['seconds']:.1f} 秒 | {old['energy']:.2f} → {new['energy']:.2f} | {new['ledger']['flight']:.2f} | {new['ledger']['detour']:.0f} | {new['ledger']['light']:.0f} | +{new['ledger']['rest']:.0f} | +8 |")
perf=[]
for device in ['desktop','portrait','landscape']:
 for scene in ['day','night','green']:
  old=next(x for x in b['performance'] if x['device']==device and x['scene']==scene and x['version']=='before');new=next(x for x in b['performance'] if x['device']==device and x['scene']==scene and x['version']=='after')
  perf.append(f"| {device} / {scene} | {old['meanMs']:.2f} → {new['meanMs']:.2f} | {old['p95Ms']:.2f} → {new['p95Ms']:.2f} | {old['rafFPS']:.1f} → {new['rafFPS']:.1f} |")
tree_counts='、'.join(f"{['城市','夜间','廊道','村落','湿地'][t['stage']]} +{t['count']}" for t in m['addedTrees'])
report='''# Fly Home：加速、实体岔路口与城市地面

基线：66d1ba8。六阶段结构保留；四个原选路位置改为实体入口，路线确认后仍使用各自地图，不是整关并排车道。首次知识卡继续暂停阅读，读完后进入约 5.2 秒的安全接近区。穿过门框时按位置锁定一次；完整可达横向范围都有归属，边界归中央入口。

默认前进速度：9 → 12.15 世界单位/秒（+35%，不等同真实鸟速）。转向输入系数：0.62 → 0.78。碰撞减速、湿地减速、鸟群让行和既有伤害规则保留。C 的弯曲中心线增加实际路径长度，按路径弧长计算进度，末端位置与切线平滑接回主线。

## 体力与典型旅程

持续飞行消耗 0.40 → 0.54/秒，其余数值不变：C 每章绕道 -7；夜间 A/B/C -14/-8/-3；三处停歇 B 每处 +7、C 每处 +17；抵达 +8。均为游戏设计，非科学测量。

用时是实际模拟飞行时间，不含知识卡阅读、手动暂停和结束动画。典型样本由控制器对准通路，无碰撞、无重试、无紧急恢复；不是新玩家成功率。

| 路线 | 用时：前 → 后 | 剩余体力：前 → 后 | 修改后飞行消耗 | 绕道 | 干扰 | 停歇 | 抵达 |
|---|---|---|---|---|---|---|---|
'''+ '\n'.join(rows)+'''

## 测试

- 桌面 1280×720、手机竖屏 390×844、横屏 844×390：实际 Chromium 键盘、CDP 触屏长按；三条入口均能选择。读卡、帮助、暂停和双语返回流程通过。
- 未注入代码的正式页面：上述三尺寸分别实际选择 A、B、C；正常 RAF 运行、真实等待，没有测试时钟跳转。计时继续，暂停冻结。截图 `live-*`。
- 三条完整单一路线模型模拟，以及三尺寸的完整混合旅程（C/B/A/C）通过；后者以 60 Hz 模拟、每 30 步绘制一次，属于加速回归，不冒充逐帧正常速度全程试玩。
- 判定边界、偏离入口中心、判定前改变方向、判定幂等、停歇不可重复恢复通过。
- 同样的横向偏差样本，A 碰撞次数大于 B，B 仍存在碰撞；样本不是现实鸟撞概率。
- 成功、失败、跳过、简化知识总结、重新开始及减少效果结尾通过。结束期间资源、事件与碰撞冻结。
- 既有屋顶近裁剪修复保留；完整混合旅程的屋顶投影没有非有限值或穿越近裁剪面的点。边界专用结果见 `evidence/forks/clipping.json`。
- 网页及内嵌离线版启动、计时、暂停与减少效果 smoke 检查通过；未核验 file://。

## 性能

同一 Chromium 软件渲染环境、同尺寸与固定场景，各版本分开串行运行，无并发浏览器测试。每场景 100 帧，前 20 帧预热。平均和 p95 为 Canvas 绘制 CPU 时间；RAF FPS 受虚拟机调度影响，不是实体手机帧率。未降低整体清晰度；沿用立面纹理缓存、远景 LOD、屏外剔除，新树复用缓存精灵。

| 尺寸 / 场景 | 平均 ms：前 → 后 | p95 ms：前 → 后 | RAF FPS：前 → 后 |
|---|---|---|---|
'''+ '\n'.join(perf)+'''

## 设计与限制

- 路线建筑设计与参考来源：[ROUTE-DESIGN.md](ROUTE-DESIGN.md)。原有六类自制建筑图集继续使用，A/B/C 改变模型组合、材质处理、通道与高度。中英文帮助已同步体力值和入口说明。
- 新增道路、人行道、路缘、车道线、横向街道和斑马线；本轮未加入动态行人和车辆。
- 新树预先生成固定世界坐标，跨章节保持位置；树高低于飞行高度，无新增碰撞，湿地不加密。
- 未使用实体手机或平板。无真实鸟类科学测量或现实材料测试。
- ABC、FLAP/BirdSafe、Audubon 原始资料请求均被环境代理返回 CONNECT 403。本轮未完成原文在线查阅；列出参考入口及访问限制，不将一般知识概括冒充已核验文献结论。
- 已尝试访问 GitHub Pages 试玩地址，但代理返回 CONNECT 403；未实际验证线上版本。本地测试及成功推送不能证明 Pages 已完成部署。
'''
report += '\n新增固定树木数量：'+tree_counts+'。\n'
(root/'FORK-VALIDATION.md').write_text(report)
# Human-readable diagram: design intent, not a construction plan.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="500" viewBox="0 0 1080 500"><rect width="1080" height="500" fill="#102d40"/><g font-family="sans-serif" fill="#f5edcf"><text x="30" y="35" font-size="23">路线建筑设计 · 外观与空间对照（示意）</text>']
for i,(name,color,h) in enumerate([('A · 连续反光幕墙','#609db8',265),('B · 实体墙与标记玻璃','#d5ceb8',225),('C · 低矮公共建筑与绿地','#a5b68b',90)]):
 x=45+i*355;y=355-h;svg += [f'<text x="{x}" y="80" font-size="19">{name}</text>',f'<rect x="{x}" y="{y}" width="230" height="{h}" fill="{color}"/>',f'<path d="M{x+230},{y}l35,-20v{h}l-35,20z" fill="#426375"/>']
 for row in range(8 if i==0 else 6 if i==1 else 2):
  for col in range(5):
   xx=x+8+col*44;yy=y+10+row*(30 if i<2 else 32);svg.append(f'<rect x="{xx}" y="{yy}" width="{40 if i==0 else 29}" height="22" fill="#5a91ad"/>')
   if i==1:
    for dx in [5,13,21]:svg.append(f'<path d="M{xx+dx},{yy+4}v14" stroke="#fff8e9" stroke-width="2"/>')
 if i==2:
  for dx in [-10,260]:svg.append(f'<path d="M{x+dx},365v-60" stroke="#625541" stroke-width="5"/><circle cx="{x+dx}" cy="300" r="24" fill="#6e9456"/>')
 for k,t in enumerate([['短程 / 净开口 12','独立天空反射 · 无白点'],['较宽 / 净开口 16','窗洞、阳台与可见标记'],['曲线绕行 / 净开口 20','低屋顶、树群与一次性停歇']][i]):svg.append(f'<text x="{x}" y="{400+k*28}" font-size="16">{t}</text>')
svg.append('<text x="30" y="478" font-size="14">尺寸与资源为游戏设计；玻璃反射在游戏中随昼夜天空变化。</text></g></svg>');(root/'assets/route-design.svg').write_text(''.join(svg))
parts=['<!doctype html><html lang="zh"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Fly Home · 岔路与城市更新</title><style>body{font:16px/1.7 system-ui;max-width:1200px;margin:30px auto;padding:16px;background:#102d40;color:#f5eddb}a{color:#b2dce8}img{max-width:100%;height:auto;border-radius:8px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}figure{margin:0}pre{white-space:pre-wrap;font:14px/1.8 system-ui;background:#19394c;padding:20px}</style><h1>Fly Home · 加速、岔路口与城市道路</h1><p><a href="index.html">试玩</a> · <a href="FORK-VALIDATION.md">测试报告</a> · <a href="ROUTE-DESIGN.md">建筑设计与资料访问限制</a></p><img src="assets/route-design.svg" alt="三条路线建筑设计对照"><h2>同视角修改前后</h2><div class="grid">']
for device in ['desktop','portrait','landscape']:
 for scene in ['day','night','green']:
  for version in ['before','after']:
   name=f'{device}-{scene}-{version}.png';parts.append(f'<figure><img loading="lazy" src="evidence/forks/{name}" alt="{name}"><figcaption>{device} / {scene} / {version}</figcaption></figure>')
parts.append('</div><h2>岔路口连续截图</h2><div class="grid">')
for route in 'ABC':
 for step in ['approach','near','entered']:
  name=f'desktop-fork-{route}-{step}.png';parts.append(f'<figure><img loading="lazy" src="evidence/forks/{name}" alt="{name}"><figcaption>{route} · {step}</figcaption></figure>')
parts.append('</div><h2>正式页面实时操作与总结</h2><div class="grid">')
for device,route in [('desktop','A'),('portrait','B'),('landscape','C')]:
 for name in [f'live-{device}-selected-{route}.png',f'{device}-summary-true.png']:
  parts.append(f'<figure><img loading="lazy" src="evidence/forks/{name}" alt="{name}"><figcaption>{name}</figcaption></figure>')
parts.append('</div><h2>数据与验证范围</h2><pre>'+html.escape(report)+'</pre></html>');(root/'forks.html').write_text(''.join(parts))
print('Generated forks.html, FORK-VALIDATION.md, assets/route-design.svg')
