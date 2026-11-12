from pathlib import Path
from PIL import Image
import json
root=Path('evidence/targeted')
for p in root.glob('*.png'):
 Image.open(p).convert('RGB').save(p.with_suffix('.webp'),quality=86)
flights=json.loads((root/'flights.json').read_text())['results']
final=json.loads((root/'three-flights.json').read_text())['results']
perf=json.loads((root/'performance.json').read_text())
entry=json.loads((root/'entry.json').read_text())
assert len(flights)==9 and len(final)==3 and len([r for r in entry if 'route' in r])==9
assert all(r['success'] and r['health']==100 for r in flights+final)
html='''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Urban Wings — UW-HABITAT-6 實測與對照</title><style>body{font:16px/1.65 system-ui;background:#132e3b;color:#edf3e7;max-width:1150px;margin:30px auto;padding:20px}a{color:#c4dfb6}img{width:100%;border-radius:9px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:14px}table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #657b80;padding:9px;text-align:left}figure{margin:8px 0 24px}small{color:#cad4cf}@media(max-width:650px){.pair{grid-template-columns:1fr}}</style><h1>Urban Wings · UW-HABITAT-6</h1><p>四棟玻璃樓、一次性知識事件、實際飛行距離體力、水鳥與濕地。</p><p><a href="index.html?v=UW-HABITAT-6">開始試玩</a> · <a href="TARGETED-VALIDATION.md">詳細實施與測試報告</a></p><p>下列對照使用相同遊戲鏡頭與尺寸。完整旅程由測試駕駛完成；入口另以鍵盤與瀏覽器觸屏事件測試。未使用實體手機，未實際驗證線上遊戲。渲染為現有 Canvas 風格與快取反射，並非真實即時光線追蹤。</p>'''
for label,scene in [('四棟高樓與反光通路','A-27'),('鳥友好玻璃通路','B-31'),('綠色繞行通路','C-31'),('生態溪流','stream'),('魚塘與村落','pond'),('米埔濕地','wetland')]:
 html+=f'<h2>{label}</h2><div class="pair"><figure><img loading="lazy" src="evidence/targeted/before-{scene}.webp" alt="修改前"><figcaption>修改前 · UW-GLASS-5</figcaption></figure><figure><img loading="lazy" src="evidence/targeted/after-{scene}.webp" alt="修改後"><figcaption>修改後 · UW-HABITAT-6</figcaption></figure></div>'
html+='<h2>看到干擾事件後再閱讀</h2><p>先有可見的行人和覓食鳥群，再看到起飛反應；卡片在觀察後出現。未看見事件則不強行彈卡。</p>'
for name in ['desktop','portrait','landscape']:
 html+=f'<details><summary>{name}：事件前後與知識卡</summary><div class="pair">'
 for suffix in ['disturbance-before','disturbance-after','disturbance-card','ponds']:
  html+=f'<figure><img loading="lazy" src="evidence/targeted/{name}-{suffix}.webp" alt="{name} {suffix}"><figcaption>{suffix}</figcaption></figure>'
 html+='</div></details>'
html+='<h2>按鍵／觸屏飛入入口：連續截圖</h2><p>由測試腳本發送真實鍵盤或觸屏事件，沒有呼叫選路或傳送函數。</p>'
for route in 'ABC':
 html+=f'<details><summary>手機直屏 · {route} 入口</summary><div class="pair">'
 for p in sorted(root.glob(f'portrait-entry-{route}-*.webp'),key=lambda p:int(p.stem.split('-')[-1])):
  html+=f'<figure><img loading="lazy" src="{p}" alt="入口連續畫面"><figcaption>{p.stem}</figcaption></figure>'
 html+='</div></details>'
html+='<h2>全程體力收支</h2><p>起始 100；所有下列旅程均健康 100 抵達。照明 −5、抵達 +10；額外繞道不重複收費。停歇上限為 100，所以實際入帳可能少於 20。數值屬遊戲設計。</p><table><tr><th>通路</th><th>秒</th><th>飛行消耗</th><th>停歇實收</th><th>剩餘體力</th></tr>'
for r in flights:html+=f'<tr><td>{r["route"]}{r["lane"]+1}</td><td>{r["time"]:.1f}</td><td>{-r["ledger"]["flight"]}</td><td>{r["ledger"]["rest"]}</td><td>{r["energy"]}</td></tr>'
html+='</table><h2>相同鏡頭的渲染耗時</h2><p>1000×650，串行軟體渲染；每場景 8 次預熱、24 次讀回完成的繪製。數值是毫秒，並非實體手機幀率。</p><table><tr><th>路線</th><th>之前 中位數 / p95</th><th>之後 中位數 / p95</th></tr>'
for route in 'ABC':
 rows=[r for r in perf['rows'] if r['route']==route]
 html+=f'<tr><td>{route}</td>'+''.join(f'<td>{r["median"]:.1f} / {r["p95"]:.1f}</td>' for r in rows)+'</tr>'
html+='</table><p><a href="evidence/targeted/model.json">模型檢查</a> · <a href="evidence/targeted/browser.json">場景測試</a> · <a href="evidence/targeted/entry.json">入口操作</a> · <a href="evidence/targeted/flights.json">九條全程</a> · <a href="evidence/targeted/three-flights.json">最終三路複測</a></p></html>'
Path('habitat.html').write_text(html)
p=Path('TARGETED-VALIDATION.md');s=p.read_text().split('## Recorded results')[0];s+='\n## Recorded results\n\nAll nine browser journeys and the final A/B/C centre-route rerun finished at Health 100. Keyboard and touch entry tests passed all three openings at all three sizes. The no-input run after normal A entry incurred a real collision. All three scene-size tests passed.\n\n| Route/path | Seconds | Flight cost | Actual rest | Final Energy |\n|---|---:|---:|---:|---:|\n'
for r in flights:s+=f'| {r["route"]}{r["lane"]+1} | {r["time"]:.1f} | {-r["ledger"]["flight"]} | {r["ledger"]["rest"]} | {r["energy"]} |\n'
s+='\nThe ecological routes consume 55–60 flight Energy versus 50–55 on A. This is approximately 12.9% more on average across the three tested paths, slightly below the initial 15–25% suggestion; it is retained to preserve forgiving completion. A direct clean run uses 55–60 including lighting, before arrival rewards.\n\n| Scene | Before median / p95 (ms) | After median / p95 (ms) |\n|---|---:|---:|\n'
for route in 'ABC':
 rows=[r for r in perf['rows'] if r['route']==route];s+=f'| {route} | '+ ' | '.join(f'{r["median"]:.1f} / {r["p95"]:.1f}' for r in rows)+' |\n'
p.write_text(s)
