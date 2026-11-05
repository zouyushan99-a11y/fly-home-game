from pathlib import Path
root=Path(__file__).resolve().parents[1];p=root/'index.html';s=p.read_text();a=s.index('const WORLD_LAYOUT=');b=s.index(';\nfunction cityBackdrop',a);s=s[:a]+'const WORLD_LAYOUT='+(root/'assets/world/layout.json').read_text()+s[b:];p.write_text(s)
