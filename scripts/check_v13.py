"""Independent checks of saved V1.3 files, not just generator metadata."""
import json
import math
from pathlib import Path

import ezdxf
import pymupdf

from build_v12 import LIFT1, ORIGINS, WC2
from build_v13 import ACI

OUT=Path(__file__).resolve().parents[1]/'deliverables'/'V1.3'
source=ezdxf.readfile(OUT/'DXF'/'原始基准_只读转换.dxf')

def key(a,b):
    return tuple(sorted(tuple(round(float(p[i]),2) for i in (0,1)) for p in (a,b)))

checks=[]
for f,name,stool_count,table_count in [(1,'一楼功能分区与家具布置图',110,16),
                                      (2,'二楼功能分区与家具布置图',76,9)]:
    d=ezdxf.readfile(OUT/'DXF'/f'{name}.dxf');m=d.modelspace()
    assert d.header['$INSUNITS']==4
    for la,color in ACI.items():
        layer=d.layers.get(la)
        assert layer.dxf.color==color and not layer.dxf.hasattr('true_color'),la
    stools=[e for e in m.query('LWPOLYLINE') if e.dxf.layer=='凳子300']
    assert len(stools)==stool_count,(f,len(stools))
    for e in stools:
        pts=list(e.get_points())
        assert all(abs(max(p[i] for p in pts)-min(p[i] for p in pts)-300)<.01 for i in (0,1))
    tables=[e for e in m.query('LWPOLYLINE') if e.dxf.layer=='餐桌']
    assert len(tables)==table_count
    for e in tables:
        pts=list(e.get_points())
        sizes=sorted(max(p[i] for p in pts)-min(p[i] for p in pts) for i in (0,1))
        assert abs(sizes[0]-600)<.01 and abs(sizes[1]/600-round(sizes[1]/600))<.001
    labels=[e.dxf.text for e in m.query('TEXT')]
    assert any('本图所有尺寸单位' in s and 'mm' in s for s in labels)
    assert any('FH-1-01' in s for s in labels) if f==1 else any('FH-2-01' in s for s in labels)
    assert any('FH-1-02' in s for s in labels) if f==1 else True
    lines={key(e.dxf.start,e.dxf.end) for e in m.query('LINE')}
    ox,oy=ORIGINS[f]
    for h in (LIFT1 if f==1 else WC2):
        e=source.entitydb[h]
        assert key((e.dxf.start.x-ox,e.dxf.start.y-oy),(e.dxf.end.x-ox,e.dxf.end.y-oy)) in lines,h
    recovery=[e for e in m.query('LWPOLYLINE') if e.dxf.layer=='唯一回收点']
    assert len(recovery)==(1 if f==1 else 0)
    if f==1:
        assert labels.count('师傅1')==1 and labels.count('师傅2')==1
        assert any('常闭' in s for s in labels)
        closed=[e for e in m if e.dxf.layer=='常闭门']
        assert any(e.dxftype()=='LWPOLYLINE' for e in closed)
        a=source.entitydb['2B6AA'];c=(a.dxf.center.x-ox,a.dxf.center.y-oy)
        assert not any(math.dist(tuple(e.dxf.center)[:2],c)<.1 for e in m.query('ARC'))
        assert len([e for e in m.query('LINE') if e.dxf.layer in ('楼梯踏步','梯下投影')])>=17
        assert any('库房' in e.dxf.text and e.dxf.insert.y<2700 for e in m.query('TEXT'))
        assert any('厨房' in e.dxf.text and e.dxf.insert.y>2800 for e in m.query('TEXT'))
    else:
        assert any('小便斗区' in s for s in labels)
        assert any('示意' in s and '现场确认' in s for s in labels)
        newrows=[e for e in tables if all(abs(p[1]-8400)<.01 or abs(p[1]-9000)<.01 for p in e.get_points())]
        assert len(newrows)==2
        assert not any(s in ('备餐/服务间','餐具回收车') for s in labels)
    checks.append({'floor':f,'stools':len(stools),'public_tables':len(tables),
                   'dark_background_ACI_palette':'PASS','original_lift_or_WC_lines':'PASS'})

for path in OUT.glob('*.dwg'):
    name=path.stem
    dark=ezdxf.readfile(OUT/'DXF'/f'{name}.dxf')
    light=ezdxf.readfile(OUT/'DXF'/'打印源'/f'{name}.dxf')
    assert len(dark.modelspace())==len(light.modelspace())
    for a,b in zip(dark.modelspace(),light.modelspace()):
        assert a.dxftype()==b.dxftype()
        assert a.dxf.all_existing_dxf_attribs()==b.dxf.all_existing_dxf_attribs()
    labels=[e.dxf.text for e in dark.modelspace().query('TEXT')]
    assert any('单位' in s and 'mm' in s for s in labels),name
    assert any(s.endswith(' mm') for s in labels),name
    with pymupdf.open(OUT/f'{name}.pdf') as pdf:assert len(pdf)==1

geo=json.loads((OUT/'几何校核.json').read_text(encoding='utf-8'))
assert geo['failures']==[] and geo['screen_geometry_blocked']==[]
assert geo['public_seats']=={'1':110,'2':60}
assert all(item['minimum_occupied_envelope_spacing_mm']>=800 for item in geo['table_spacing'])
conv=json.loads((OUT/'转换验证.json').read_text(encoding='utf-8'))
assert len(conv)==9 and all(c['skipped']['count']==0 for c in conv)
print(json.dumps({'status':'PASS','saved_checks':checks,'DWG/PDF_pairs':len(conv),
                  'dark_and_print_geometry_identical':True,'geometry_errors':geo['failures']},ensure_ascii=False,indent=2))
