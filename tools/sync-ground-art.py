"""Sync the checked-in ground materials and precomputed road layout into the game.
Run sync-building-art.py afterwards to refresh the self-contained offline file.
"""
from pathlib import Path
root=Path(__file__).resolve().parents[1];p=root/'index.html';s=p.read_text()
for name,file,next_token in [('GROUND_ART','embedded.json','const BUILDING_ART'),('ROAD_LAYOUT','roads.json','let ROAD_WORLD')]:
 a=s.index('const '+name+'=');b=s.index(';\n'+next_token,a)
 s=s[:a]+'const '+name+'='+(root/'assets/ground'/file).read_text()+s[b:]
p.write_text(s)
