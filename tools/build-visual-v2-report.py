from pathlib import Path
import json,html
root=Path(__file__).resolve().parents[1];r=json.loads((root/'evidence/visual-v2/results.json').read_text())
names=['城市','夜间街区','生态廊道','村落','湿地'];counts='\n'.join(f"| {names[x['chapter']]} | {x['before']} | {x['after']} | {x['after']-x['before']} |" for x in r['buildingCounts'])
rows=[]
for device in ['desktop','portrait','landscape']:
 for scene in ['day','night','lamps','grass','village','meadow']:
  p=[next(x for x in r['performance'] if x['device']==device and x['scene']==scene and x['version']==v) for v in ['before','after']]
  rows.append(f"| {device} / {scene} | {p[0]['meanMs']:.2f} → {p[1]['meanMs']:.2f} | {p[0]['p95Ms']:.2f} → {p[1]['p95Ms']:.2f} | {p[0]['rafFPS']:.1f} → {p[1]['rafFPS']:.1f} |")
md='''# Fly Home：知识总结与建筑视觉更新

基线：`1c74574ddbc63d353d6eb6714ad5c2d143af7a8d`。游戏入口 `index.html`；对比图集 `visual-v2.html`；建筑设计与三视图 `assets/buildings/catalog.html`。

## 实现

- 总结仅保留已遇见的玻璃、照明、生态连通性、湿地四类知识，每条标题加一句知识说明。正常完整旅程显示四条；提前中断只显示已解锁主题。移除撞击数、路线统计、操作技巧、反思输入与长文，保留成功/失败提示、再飞一次及折叠阅读。中英文同步。
- 六类建筑先由 `build-building-designs.py` 生成设计板、同比例正/侧/俯视图与 18 张 SVG 贴图，再嵌入游戏；三视图的退台、裙楼、坡顶与实际模型对应。自制素材及来源见 `assets/buildings/SOURCES.md`。
- 窗格是透明遮罩，上层建筑构件与底层天空采样分开。前侧立面按实际楼高重复相同楼层带，底部独立门厅。屋顶独立映射，村屋两片坡顶也实际使用屋顶贴图。昼夜天空、暗窗和亮窗沿用原渲染逻辑；侧面有独立立面贴图。
- 纹理加载时栅格化并预生成夜间版本、64 像素中景版本；使用有界纹理与合成缓存、屏外剔除和距离分级。中景只给部分建筑使用低细节贴图，远景主要为明暗轮廓，不增加逐楼动态反射。没有降低全局分辨率。
- 夜间路灯以固定世界位置生成，灯杆、灯具和暖色向下地面光随建筑共同按深度排序；无闪烁。灯高 9，飞行高度固定 34，玩家不能触及，不新增障碍或干扰扣减。
- 白天草地加入缓存的短草、色差与少量野花纹理；依城市、廊道、村落、湿地水岸使用不同位置和配色，保留空地、水道和疏密差异。减少效果时草地摆动冻结；装饰不参与碰撞。

## 外围建筑数量

下表是稳定世界中的外围建筑总数，不是单帧可见数；原有近景建筑与全部路线开口几何不变。外围建筑足迹处于玩家可达横向范围之外。湿地无新增建筑。

| 区域 | 修改前 | 修改后 | 新增 |
|---|---:|---:|---:|
'''+counts+'''

## 测试

实际运行 `node tools/visual-v2-validation.cjs`、`node tools/building-feature-test.cjs`、`node tools/interaction-test.cjs`、`node tools/smoke.cjs`。

- 全部 12 组航路近景几何逐项不变；背景固定且不可达。
- A/B/C 完整旅程均成功，无紧急恢复、无重试；剩余体力仍为 25.44 / 52.44 / 59.44，健康均 100。模拟数值属于游戏设计，不是科学测量。
- 36 组阅读→选路→飞行流程通过，覆盖帮助、暂停、双语、触屏与检查点恢复。
- 三尺寸成功/失败结束、自动完成、跳过、减少效果、重启及中英文四主题总结通过；无文本输入。结束期间资源、碰撞与事件冻结。
- 18 张立面/屋顶贴图成功解码；日夜玻璃纹理不同；减少效果的草地输出静止；草地与路灯确有可见绘制且不改变体力。无浏览器脚本异常。
- 正式网页和同步离线版烟测通过；离线验证阻断资源子请求，不代表已验证 file:// 双击。

图片：三尺寸同场景修改前后、成功/失败中英文总结、六类建筑日夜实际 Canvas 渲染。建筑展示相机用于观察材质，不是游戏中的额外关卡。测试入口仅通过浏览器路由注入，正式游戏无测试 API。

## 同场景性能

顺序运行单个浏览器，视口为 1280×720、390×844、844×390，DPR 上限保持原值。每个固定场景预热 20 帧，再采集 80 帧；RAF 与 Canvas 调用耗时分别报告。此测试没有推动模拟进度，不能代表整段实机旅程性能；一次采样有噪声，不是实体设备保证。曾发现 SVG 逐帧滤镜开销，已改成栅格缓存及中景 LOD。新增细节仍有开销，尤其桌面软件渲染，未宣称性能完全不变。

| 视口 / 场景 | Canvas 平均 ms（前→后） | P95 ms（前→后） | RAF FPS（前→后） |
|---|---:|---:|---:|
'''+ '\n'.join(rows)+'''

## 限制与线上状态

手机测试为 Chromium 触屏/视口模拟，未使用实体手机。建筑仍为 Canvas 伪 3D，透视纹理、透明层和排序为近似；反射不是实时光线追踪。设计为程序绘制的插画风格，不是照片实景。

当前环境访问 `zouyushan99-a11y.github.io` 被代理 403 拒绝，因此未实际验证线上版本或 Pages 构建成功。Git 推送状态以交付说明为准，不能由本地测试推断线上已更新。

## 素材维护

先运行 `python3 tools/build-building-designs.py` 重新生成设计与贴图，再运行 `python3 tools/sync-building-art.py` 更新游戏内嵌资源及离线文件。SVG 源文件可单独编辑；自定义后同步 embedded.json，避免重新生成覆盖手工改动。
'''
(root/'VISUAL-V2-VALIDATION.md').write_text(md)
s='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fly Home · 建筑与环境更新</title><style>body{font:16px/1.7 system-ui;background:#102d3e;color:#f6eedc;max-width:1200px;margin:auto;padding:24px}a{color:#f0cc91}img{max-width:100%;border-radius:8px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px}figure{margin:0}section{margin:40px 0}td,th{padding:8px;border:1px solid #71858a}table{border-collapse:collapse}pre{white-space:pre-wrap;font-size:12px}.scroll{overflow:auto}@media(max-width:650px){.pair{grid-template-columns:1fr}}</style><h1>Fly Home · 知识、建筑与环境</h1><p><a href="index.html">开始试玩 ↗</a> · <a href="assets/buildings/catalog.html">六类设计 / 三视图 / 实际贴图</a> · <a href="VISUAL-V2-VALIDATION.md">完整报告与限制</a> · <a href="evidence/visual-v2/results.json">原始数据</a></p><p>外围建筑 239 → 505；航路近景几何保持不变。精简中英文知识总结，增加路灯与草地。已本地浏览器验证，线上访问受代理限制，尚未验证线上版本。未使用实体手机。</p><h2>外围建筑数量</h2><table><tr><th>区域</th><th>前</th><th>后</th><th>新增</th></tr>'''
for x in r['buildingCounts']:s+=f"<tr><td>{names[x['chapter']]}</td><td>{x['before']}</td><td>{x['after']}</td><td>{x['after']-x['before']}</td></tr>"
s+='</table>'
for device in ['desktop','portrait','landscape']:
 s+=f'<section><h2>{device} · 同场景前后</h2>'
 for scene,label in [('day','城市与建筑'),('night','夜间材质'),('lamps','路灯与暖光'),('grass','生态廊道'),('village','村落草地'),('meadow','湿地水岸')]:
  s+=f'<h3>{label}</h3><div class="pair">'
  for version in ['before','after']:s+=f'<figure><figcaption>{version}</figcaption><a href="evidence/visual-v2/{device}-{scene}-{version}.png"><img loading="lazy" src="evidence/visual-v2/{device}-{scene}-{version}.png"></a></figure>'
  s+='</div>'
 s+='</section>'
s+='<h2>简化后的知识总结</h2><div class="pair">'
for success,language in [('true','zh'),('true','en'),('false','zh'),('false','en')]:s+=f'<figure><figcaption>{success} / {language}</figcaption><img loading="lazy" src="evidence/visual-v2/portrait-summary-{success}-{language}.png"></figure>'
s+='</div><h2>性能实测（前→后）</h2><p>软件 Chromium；固定场景单轮采样。新增细节有开销，不承诺实体设备帧率。完整方法和限制见报告。</p><pre>'+html.escape('\n'.join(rows))+'</pre></html>'
(root/'visual-v2.html').write_text(s)
print('Wrote visual-v2.html and VISUAL-V2-VALIDATION.md')
