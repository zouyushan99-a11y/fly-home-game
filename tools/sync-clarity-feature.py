"""Synchronize the editable clarity UI/data source into the single-page game."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'index.html';s=p.read_text();a=s.index('const AREA_IMAGES=');b=s.index('const routes={',a)
p.write_text(s[:a]+(root/'tools/clarity-feature.js').read_text()+'\n'+s[b:])
