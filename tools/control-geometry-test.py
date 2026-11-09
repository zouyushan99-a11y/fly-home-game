"""Reproducible world occupancy and shared endpoint checks."""
import runpy,contextlib,io,json
from pathlib import Path
with contextlib.redirect_stdout(io.StringIO()):m=runpy.run_path(str(Path(__file__).with_name('plan-shared-city.py')))
d=m['data'];checks={'entranceRoadOverlaps':[b['id'] for es in d['entrances'] for b in es if any(m['intersects'](a,v,b,w) for a,v,w in m['segments'])], 'buildingOverlaps':[(a['id'],b['id']) for bs in d['buildings'] for i,a in enumerate(bs) for b in bs[i+1:] if m['overlap'](a,b,0)]}
assert not any(checks.values()),checks
for c in [0,1]:
 for u in [0,315]:assert len(set(round(m['line'](c,r,u),8) for r in 'ABC'))==1
 assert d['report'][c]['lengths']['A']<d['report'][c]['lengths']['B']<d['report'][c]['lengths']['C']
Path('evidence/control/geometry.json').write_text(json.dumps(checks,indent=2));print('PASS road reservations, solid footprints, common endpoints, distinct lengths')
