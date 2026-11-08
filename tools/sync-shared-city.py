from pathlib import Path
root=Path(__file__).resolve().parents[1];p=root/'index.html';s=p.read_text();a=s.find('const SHARED_CITY=');b=s.index('// Route difficulty changes actual geometry.')
s=s[:a if a>=0 else b]+'const SHARED_CITY='+(root/'assets/city/shared.json').read_text()+';\n'+s[b:];p.write_text(s)
