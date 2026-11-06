"""Original explanatory SVG exhibits; no third-party image assets."""
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'assets/education';out.mkdir(exist_ok=True)
base='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 280"><defs><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#8cc5db"/><stop offset="1" stop-color="#e6e8cb"/></linearGradient><linearGradient id="glass"><stop stop-color="#387594"/><stop offset=".5" stop-color="#b1dae2"/><stop offset="1" stop-color="#325c7a"/></linearGradient><g id="bird"><path d="M-18 0Q-8-15 0-2Q9-14 20 0Q8-5 0 4Q-9-5-18 0" fill="#f2edda" stroke="#234659" stroke-width="2"/></g><g id="waterbird"><path d="M-10 0q12-9 23 0l-15 5zM10 0q0-20 8-23l12 3-13 2" fill="#f6efdc" stroke="#365464" stroke-width="2"/><path d="M0 5v15m7-16v15" stroke="#365464" stroke-width="2"/></g><g id="tree"><path d="M0 5v55" stroke="#75624b" stroke-width="7"/><circle cy="-5" r="26" fill="#387c67"/><circle cx="-17" cy="6" r="18" fill="#4e9172"/><circle cx="17" cy="3" r="19" fill="#77a47b"/></g><g id="person"><circle cy="-28" r="7" fill="#e8c291"/><path d="M0-20v24m-13-13 13-7 12 7M0 4l-9 17M0 4l9 17" fill="none" stroke="#bf7959" stroke-width="6" stroke-linecap="round"/></g></defs><rect width="800" height="280" rx="18" fill="url(#sky)"/>'''
scenes={}
scenes['glass']='''<path d="M0 230Q200 190 400 232T800 220V280H0" fill="#8ba980"/><path d="M400 12v255" stroke="#fcf3dd" stroke-width="3" stroke-dasharray="6 7"/>'''
for x in [210,600]:
 scenes['glass']+=f'<path d="M{x} 45l130-20v235l-130-12z" fill="url(#glass)" stroke="#e9f1e9" stroke-width="3"/><path d="M{x+20} 100q30-35 80 0m-85 40q40-30 90 0" fill="none" stroke="#fff" stroke-width="8" opacity=".4"/><use href="#tree" transform="translate({x+70} 207) scale(.6)" opacity=".45"/><use href="#bird" transform="translate({x-95} 130) scale(1.5)"/>'
scenes['glass']+='<path d="M136 133h70" stroke="#c57957" stroke-width="3" stroke-dasharray="7 7"/><path d="M525 134q30-2 32-50" fill="none" stroke="#286d62" stroke-width="3" stroke-dasharray="7 7"/>'
for x in range(612,730,15):
 for y in range(50,242,16):scenes['glass']+=f'<circle cx="{x}" cy="{y}" r="2.8" fill="#fff7df"/>'
scenes['light']='<rect width="800" height="280" rx="18" fill="#19334d"/><circle cx="400" cy="40" r="14" fill="#f0e8c7"/>'
for offset in [0,400]:
 for i,h in enumerate([100,155,125,185]):
  x=offset+28+i*85;scenes['light']+=f'<rect x="{x}" y="{260-h}" width="62" height="{h}" fill="#304e64"/>'
  for y in range(275-h,250,20):
   for xx in range(x+10,x+60,17):scenes['light']+=f'<rect x="{xx}" y="{y}" width="8" height="10" fill="{ "#f6ce82" if offset==0 or (xx+y)%3==0 else "#19394f"}"/>'
 if offset==0:scenes['light']+='<path d="M30 260 130 10 230 260M170 260 290 5 385 260" fill="#f6d588" opacity=".14"/>'
 for x,y in [(60,65),(150,35),(260,50)]:scenes['light']+=f'<use href="#bird" transform="translate({x+offset} {y})"/>'
scenes['light']+='<path d="M470 242v-28h18m190 28v-28h18" fill="none" stroke="#f8deaa" stroke-width="3"/><path d="M487 215l-15 35h30zM695 215l-15 35h30z" fill="#f8deaa" opacity=".25"/>'
scenes['green']='<path d="M0 175h800v105H0" fill="#a6bb81"/><path d="M0 260H360l40-85" stroke="#e7d8b3" stroke-width="28"/><ellipse cx="610" cy="234" rx="100" ry="30" fill="#6faabc"/><path d="M500 280q20-80 70-90" stroke="#4a8a68" stroke-width="25" fill="none"/><use href="#tree" transform="translate(130 159)"/>'
for x,y,scale in [(445,130,1),(530,100,1.4),(720,155,1.2),(775,170,.8)]:scenes['green']+=f'<use href="#tree" transform="translate({x} {y}) scale({scale})"/>'
for x in [470,490,680,700]:scenes['green']+=f'<circle cx="{x}" cy="220" r="12" fill="#548664"/><circle cx="{x+4}" cy="217" r="3" fill="#d29661"/>'
scenes['green']+='<use href="#waterbird" transform="translate(620 211)"/><use href="#bird" transform="translate(590 110)"/>'
scenes['pond']='<path d="M0 140h800v140H0" fill="#9db381"/><path d="M320 190 760 160 800 267 410 280z" fill="#70a9b4" stroke="#c4bb91" stroke-width="14"/><path d="M350 195l380-22 25 20-365 35" fill="#c2cfb1"/>'
for x,y in [(40,90),(160,110)]:scenes['pond']+=f'<path d="M{x} {y+35}h90v65h-90z" fill="#e0d2af"/><path d="M{x-10} {y+35}l55-35 55 35z" fill="#a56856"/><rect x="{x+35}" y="{y+60}" width="20" height="40" fill="#567981"/>'
for x in [275,310,345]:scenes['pond']+=f'<use href="#tree" transform="translate({x} 155) scale(.65)"/>'
for x,y in [(440,210),(535,195),(660,200)]:scenes['pond']+=f'<use href="#waterbird" transform="translate({x} {y})"/>'
scenes['birds']='<path d="M0 180h800v100H0" fill="#a9b994"/><path d="M0 225h800v55H0" fill="#88b6ba"/><path d="M400 10v260" stroke="#faf4de" stroke-width="3" stroke-dasharray="6 7"/><use href="#person" transform="translate(45 180)"/><use href="#person" transform="translate(585 190)"/>'
for x in [220,280,340]:scenes['birds']+=f'<use href="#waterbird" transform="translate({x} 218)"/>'
for x,y in [(645,135),(700,100),(750,140)]:scenes['birds']+=f'<use href="#bird" transform="translate({x} {y})"/>'
scenes['birds']+='<path d="M615 195q10-45 35-65m35 70q10-35 20-65" stroke="#b47454" fill="none" stroke-width="2" stroke-dasharray="5 6"/>'
scenes['wetland']='<path d="M0 140h800v140H0" fill="#75a8b4"/><path d="M0 155q110 80 230 35l20 90H0" fill="#b8aa88"/><path d="M240 145h210v120H240z" fill="#80b9bb" stroke="#c0c29b" stroke-width="13"/><path d="M470 160q150-45 330 35v85H470z" fill="#96ae7c"/>'
for x in [505,550,595]:scenes['wetland']+=f'<use href="#tree" transform="translate({x} 135) scale(.7)"/><path d="M{x} 175l-15 25m15-25 15 25" stroke="#766752" fill="none" stroke-width="3"/>'
for x in range(660,800,13):scenes['wetland']+=f'<path d="M{x} 247v-68m0 35-8-20m8 6 8-20" stroke="#607d50" stroke-width="3"/><path d="M{x} 185v-12" stroke="#9a7651" stroke-width="5"/>'
for x,y in [(80,205),(150,225),(340,210)]:scenes['wetland']+=f'<use href="#waterbird" transform="translate({x} {y})"/>'
scenes['wetland']+='<use href="#bird" transform="translate(600 66)"/>'
for id,scene in scenes.items():(out/f'{id}.svg').write_text(base+scene+'</svg>')
print('Six original educational diagrams built')
