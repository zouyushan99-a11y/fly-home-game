from pathlib import Path
import json,html
root=Path(__file__).resolve().parents[1];out=root/'evidence/natural'
m=json.loads((out/'model.json').read_text());b=json.loads((out/'browser.json').read_text());layout=json.loads((out/'road-layout.json').read_text())
perf=[]
for device in ['desktop','portrait','landscape']:
 for scene in ['day','night','corner','green']:
  old=next(x for x in b['performance'] if x['device']==device and x['scene']==scene and x['version']=='before');new=next(x for x in b['performance'] if x['device']==device and x['scene']==scene and x['version']=='after')
  perf.append(f"| {device} / {scene} | {old['meanMs']:.2f} → {new['meanMs']:.2f} | {old['p95Ms']:.2f} → {new['p95Ms']:.2f} | {old['rafFPS']:.1f} → {new['rafFPS']:.1f} |")
journeys='\n'.join(f"| {r['route']} | {r['seconds']:.2f} | {r['health']} | {r['energy']:.2f} |" for r in m['journeys'])
text='''# Fly Home：自然入口与连续地面

基线 `cae0eb1`。移除空中矩形门框与三色地面引导色块；入口由错落的幕墙楼、带标记建筑和低矮公共建筑围合，保留少量辅助文字。三个通道宽度、前后位置不完全相同。

## 入口判定与玩法

入口的左右边界由实际建筑侧面加鸟的碰撞半径计算，纵向判定范围与街角位置对应，不再按屏幕三等分分配路线。飞入通道才确认一次，进入前可改变方向。直飞实体墙会按既有规则扣血并阻止向前穿透；仍能侧移转出，不存在隐藏的入口墙或自动换路。选中后不改变横向位置，后续各自地图和汇合结构保留。

改动局限于章节入口；后续挑战建筑、速度、标记材质、停歇及事件收费保留。C 的平滑绕行起点稍后移，避免入口确认时跳变。三条完整旅程的无碰撞控制器模拟均可完成，无重试或紧急恢复：

| 路线 | 飞行秒数 | 健康 | 剩余体力 |
|---|---|---|---|
'''+journeys+'''

时间不包括知识卡阅读或手动暂停。该结果不是新玩家成功率；所有资源数值仍是游戏设计。

## 道路与纹理根因

旧代码每隔 36 个世界单位独立拼接路段，并在分段中重置部分标线，另有一层不连续的庭院/横街矩形叠加。因此问题并非单纯贴图分辨率不足。

新路网为一条连续主路与六条错位支路，包含斜向路段、转弯和丁字连接。规划时避开三个路线版本建筑占地的并集，车道与人行道全宽逐段检测，不依赖先选路线再移动道路。固定路网预计算后内嵌，运行时无需执行路径搜索；可通过模型测试重建并比对。

自制四种可平铺俯视材质：沥青、人行道、路缘、草地。每张纹理两侧像素边界一致，无烘焙天空、透视、灯光或固定阴影。材质先合成为固定世界坐标地图，再单独铺设连续标线、斑马线、停止线。所有道路先绘制人行道并集，再绘制路缘和沥青并集，避免路口出现内部接缝。三条短步行连接通向入口建筑前方；不是每栋远景建筑都有独立支路。

地面采用水平扫描行透视映射，UV 来自世界坐标，不随路段重置。世界图缓存为 1080×2520，日夜复用同一布局并使用独立色调缓存；远处渐隐、缓存边缘透明过渡。原有水岸、村落与湿地区域保持原有地面处理。

素材与使用文件：`assets/ground/atlas.png`、四张单独纹理、`assets/ground/roads.json`；全部自制，来源与生成器见 `assets/ground/SOURCE.md`。实际合成地面图见 `evidence/natural/world-ground-map.png`。SVG 设计示意直接使用实际模型占地与路网坐标。

## 验证

- 桌面 1280×720、竖屏 390×844、横屏 844×390 的真实键盘/触屏事件分别验证三个入口；阅读、帮助、暂停与双语返回通过。
- 正式页面另外使用正常 RAF、真实等待与键盘/CDP 触屏，不注入游戏代码、不跳转时钟，验证三个尺寸的入口确认与暂停。
- 三条完整模型旅程、三尺寸完整混合旅程；混合旅程按 60 Hz 模拟、每 30 步渲染，属于加速回归。
- 物理通道边缘、撞墙不误选、侧移脱困、选择幂等、接近阶段反向操作、知识卡与暂停冻结体力/干扰计时通过。
- 每个车道和人行道线段避开全部候选建筑占地，预计算路网与重建结果一致。
- 三尺寸地面扫描行坐标和绘制范围检查：无非有限值、源纹理越界、地平线上方绘制；按像素中心反算的 UV 误差为零。缓存外边缘透明度接近零。
- 屋顶近裁剪边界专项回归、成功/失败、跳过、减少效果、重新开始及离线版本 smoke 测试均有独立记录。
- 所有页面错误记录为空。不是对所有硬件或所有操作组合的穷尽证明。

## 同条件性能

基线与修改后使用相同尺寸、相同固定场景、相同软件 Chromium，浏览器测试串行运行。每场景 100 帧，前 20 帧预热；CPU 数值为绘制耗时，RAF FPS 同时受虚拟机调度影响，不等于实体设备表现。没有降低整体画布清晰度。

| 尺寸 / 场景 | 平均 ms：前 → 后 | p95 ms：前 → 后 | RAF FPS：前 → 后 |
|---|---|---|---|
'''+ '\n'.join(perf)+'''

## 限制

- 未使用实体手机或平板；手机测试为 Chromium 视口与触屏模拟。
- 完整旅程主要由确定性控制器加速验证；正常速度手工输入检查覆盖入口及暂停，不冒充正常速度全程人工试玩。
- 地面图是有边界的预计算城市区域，通过透明边缘与远景渐隐接入原场景，并非无限开放世界。静态路网不包含行人或车辆模拟。
- 建筑纹理和玻璃反射沿用前版；本轮未重做全部建筑资产。
- 已尝试访问线上试玩页，代理返回 CONNECT 403，未实际验证线上运行；本地测试与成功推送不能证明 GitHub Pages 已部署。
'''
(root/'NATURAL-VALIDATION.md').write_text(text)
# Plan views are derived from the actual world coordinates, not decorative concept art.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="850" viewBox="0 0 1000 850"><rect width="1000" height="850" fill="#142e40"/><g font-family="sans-serif" fill="#f5ead0"><text x="25" y="35" font-size="24">自然通道与固定路网 · 实际世界坐标示意</text><text x="25" y="65" font-size="14">左：城市与夜间路网　右：首个入口俯视（浅色为可通行范围，非游戏门框）</text></g>']
def rect(b,ox,oy,k):
 x=ox+b['x']*k;y=oy+b['z']*k;cx=x;cy=y+b['depth']*k/2
 return f'<rect x="{x-b["width"]*k/2}" y="{y}" width="{b["width"]*k}" height="{b["depth"]*k}" transform="rotate({-b.get("angle",0)*180/3.14159265} {cx} {cy})" fill="{"#b4bc9a" if b.get("marked") else "#5e8498"}" stroke="#d2d6c0" stroke-width=".5"/>'
for r in layout['roads']:
 points=' '.join(f'{210+x},{130+z}' for x,z in r['points']);svg.append(f'<polyline points="{points}" fill="none" stroke="#cbc6ad" stroke-width="{r["width"]+r["walk"]*2}" stroke-linejoin="round"/><polyline points="{points}" fill="none" stroke="#697782" stroke-width="{r["width"]}" stroke-linejoin="round"/>')
for building in layout['buildings']:svg.append(rect(building,210,130,1))
for building in layout['buildings']:
 if building.get('entrance') and building['chapter']==0:svg.append(rect(building,660,-40,5))
for p in layout['entrances'][0]:
 x=660+p['left']*5;y=-40+p['z']*5;svg.append(f'<rect x="{x}" y="{y}" width="{(p["right"]-p["left"])*5}" height="{(p["end"]-p["z"])*5}" fill="#d6cf9b44" stroke="#e1dba8" stroke-dasharray="3 4"/><text x="{x+10}" y="{y-8}" fill="#fff3d5" font-size="22">{p["route"]}</text>')
svg.append('<text x="530" y="620" fill="#f5ead0" font-size="15">入口范围来自相邻外墙与鸟的碰撞半径。</text><text x="530" y="650" fill="#f5ead0" font-size="15">游戏内无矩形框与三色地面色块。</text></svg>');(root/'assets/ground/layout.svg').write_text(''.join(svg))
parts=['<!doctype html><html lang="zh"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Fly Home · 自然通道与地面</title><style>body{font:16px/1.7 system-ui;max-width:1200px;margin:24px auto;padding:16px;background:#142e40;color:#f5ead0}a{color:#a9dbdf}img{max-width:100%;height:auto}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}figure{margin:0}pre{white-space:pre-wrap;font:14px/1.8 system-ui;background:#1b3b4d;padding:20px}</style><h1>Fly Home · 自然通道与连续地面</h1><p><a href="index.html">试玩</a> · <a href="NATURAL-VALIDATION.md">测试报告</a> · <a href="assets/ground/SOURCE.md">素材来源</a></p><p><a href="evidence/natural/world-ground-map.png">实际使用的地面合成图</a> · <a href="assets/ground/roads.json">固定路网坐标</a></p><h2>设计与实际贴图</h2><div class="grid"><figure><img src="assets/ground/layout.svg" alt="实际路网和入口范围"></figure><figure><img src="assets/ground/atlas.png" alt="沥青、人行道、路缘、草地图集"><figcaption>原始自制材质图集；道路标线单独铺设。</figcaption></figure></div>']
def gallery(title,names):
 parts.append('<h2>'+title+'</h2><div class="grid">')
 for name in names:
  parts.append(f'<figure><img loading="lazy" src="evidence/natural/{name}.png" alt="{name}"><figcaption>{name}</figcaption></figure>')
 parts.append('</div>')
gallery('同视角前后对比',[f'{d}-{s}-{v}' for d in ['desktop','portrait','landscape'] for s in ['day','night','corner'] for v in ['before','after']])
gallery('进入自然通道的连续截图',[f'desktop-fork-{r}-{s}' for r in 'ABC' for s in ['approach','near','entered']])
gallery('道路转角连续截图',[f'{d}-road-turn-{i}' for d in ['desktop','portrait','landscape'] for i in range(3)])
gallery('正式页面实时输入',[f'live-{d}-selected-{r}' for d,r in [('desktop','A'),('portrait','B'),('landscape','C')]])
parts.append('<h2>测试数据与限制</h2><pre>'+html.escape(text)+'</pre></html>');(root/'natural.html').write_text(''.join(parts));print('Generated natural.html and NATURAL-VALIDATION.md')
