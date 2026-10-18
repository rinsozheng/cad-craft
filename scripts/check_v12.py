"""Independent checks on saved V1.2 CAD artifacts (run after build_v12.py)."""
import json
from pathlib import Path

import ezdxf
import pymupdf

from build_v12 import LIFT1, ORIGINS, WC2

root = Path(__file__).resolve().parents[1]
out = root / 'deliverables' / 'V1.2'
source = ezdxf.readfile(out / 'DXF' / '原始基准_只读转换.dxf')
saved = {}

def segment_key(a, b):
    return tuple(sorted((tuple(round(float(v), 2) for v in tuple(a)[:2]),
                         tuple(round(float(v), 2) for v in tuple(b)[:2]))))

results = []
for f, name, expected in [(1, '一楼功能分区与家具布置图', 110),
                          (2, '二楼功能分区与家具布置图', 68)]:
    d = ezdxf.readfile(out / 'DXF' / f'{name}.dxf')
    saved[f] = d
    m = d.modelspace()
    assert d.header['$INSUNITS'] == 4
    stools = [e for e in m.query('LWPOLYLINE') if e.dxf.layer == '凳子300']
    assert len(stools) == expected, (f, len(stools), expected)
    for e in stools:
        pts = list(e.get_points())
        assert abs(max(p[0] for p in pts)-min(p[0] for p in pts)-300) < .01
        assert abs(max(p[1] for p in pts)-min(p[1] for p in pts)-300) < .01
    tables = [e for e in m.query('LWPOLYLINE') if e.dxf.layer == '餐桌']
    for e in tables:
        pts = list(e.get_points())
        sizes = sorted([max(p[i] for p in pts)-min(p[i] for p in pts) for i in (0,1)])
        assert abs(sizes[0]-600) < .01
        assert abs(sizes[1]/600-round(sizes[1]/600)) < .001
    labels = [e.dxf.text for e in m.query('TEXT')]
    assert not any(s in ('备餐/服务间', '餐具回收车', '工位3', '师傅3') for s in labels)
    recovery = [e for e in m.query('LWPOLYLINE') if e.dxf.layer == '唯一回收点']
    assert len(recovery) == (1 if f == 1 else 0)
    linekeys = {segment_key(e.dxf.start, e.dxf.end) for e in m.query('LINE')}
    ox, oy = ORIGINS[f]
    handles = LIFT1 if f == 1 else WC2
    for handle in handles:
        e = source.entitydb[handle]
        assert segment_key((e.dxf.start.x-ox, e.dxf.start.y-oy),
                           (e.dxf.end.x-ox, e.dxf.end.y-oy)) in linekeys, handle
    if f == 1:
        assert labels.count('师傅1') == 1 and labels.count('师傅2') == 1
    results.append({'floor': f, 'stools_300mm': len(stools), 'table_depth_mm': 600,
                    'original_lift_or_WC_lines_verified': len(handles),
                    'recovery_points': len(recovery)})

assert len(list(out.glob('*.dwg'))) == 9
assert len(list(out.glob('*.pdf'))) == 9
for pdf in out.glob('*.pdf'):
    with pymupdf.open(pdf) as d:
        assert len(d) == 1
        assert d[0].rect.width > 0 and d[0].rect.height > 0

geom = json.loads((out / '几何校核.json').read_text(encoding='utf-8'))
assert geom['failures'] == [] and geom['screen_geometry_blocked'] == []
print(json.dumps({'status': 'PASS', 'saved_file_checks': results,
                  'DWG_count': 9, 'PDF_count': 9,
                  'geometry': geom['table_spacing']}, ensure_ascii=False, indent=2))
