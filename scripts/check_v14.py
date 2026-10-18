"""Check saved V1.4 edits, including unchanged first-floor and wash-area geometry."""
import collections
import hashlib
import json
from pathlib import Path

import ezdxf
import pymupdf

from build_v12 import LIFT1, ORIGINS, WC2
from build_v13 import ACI

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'deliverables'/'V1.4'
PREVIOUS=ROOT/'deliverables'/'V1.3'
source=ezdxf.readfile(OUT/'DXF'/'原始基准_只读转换.dxf')

def normal(value):
    if isinstance(value,str):return value.replace('V1.4','V1.3')
    if isinstance(value,(int,float,bool)) or value is None:return value
    if isinstance(value,dict):return {k:normal(v) for k,v in value.items()}
    return [normal(v) for v in value]

def signature(e):
    attrs={k:v for k,v in e.dxf.all_existing_dxf_attribs().items() if k not in ('handle','owner')}
    item={'type':e.dxftype(),'attributes':normal(attrs)}
    if e.dxftype()=='LWPOLYLINE':item['points']=normal(list(e.get_points()))
    return json.dumps(item,sort_keys=True,ensure_ascii=False)

def line_key(a,b):
    return tuple(sorted(tuple(round(float(p[i]),2) for i in (0,1)) for p in (a,b)))

saved={}
for f,name,expected_stools in [(1,'一楼功能分区与家具布置图',110),
                               (2,'二楼功能分区与家具布置图',76)]:
    d=ezdxf.readfile(OUT/'DXF'/f'{name}.dxf');m=d.modelspace();saved[f]=d
    assert d.header['$INSUNITS']==4
    for la,c in ACI.items():
        assert d.layers.get(la).dxf.color==c and not d.layers.get(la).dxf.hasattr('true_color')
    stools=[e for e in m.query('LWPOLYLINE') if e.dxf.layer=='凳子300']
    assert len(stools)==expected_stools
    for e in stools:
        pts=list(e.get_points())
        assert all(abs(max(p[i] for p in pts)-min(p[i] for p in pts)-300)<.01 for i in (0,1))
    tables=[e for e in m.query('LWPOLYLINE') if e.dxf.layer=='餐桌']
    for e in tables:
        pts=list(e.get_points());sides=sorted(max(p[i] for p in pts)-min(p[i] for p in pts) for i in (0,1))
        assert abs(sides[0]-600)<.01
        assert abs(sides[1]/600-round(sides[1]/600))<.001
    lines={line_key(e.dxf.start,e.dxf.end) for e in m.query('LINE')}
    ox,oy=ORIGINS[f]
    for handle in (LIFT1 if f==1 else WC2):
        e=source.entitydb[handle]
        assert line_key((e.dxf.start.x-ox,e.dxf.start.y-oy),
                        (e.dxf.end.x-ox,e.dxf.end.y-oy)) in lines,handle

# The entire first-floor model is identical, except the version label.
old1=ezdxf.readfile(PREVIOUS/'DXF'/'一楼功能分区与家具布置图.dxf')
assert collections.Counter(map(signature,old1.modelspace()))==collections.Counter(map(signature,saved[1].modelspace()))

m=saved[2].modelspace()
old2=ezdxf.readfile(PREVIOUS/'DXF'/'二楼功能分区与家具布置图.dxf')
# Original wash basin block and all original WC geometry must stay in place.
for kind in ('LINE','INSERT'):
    a=[signature(e) for e in old2.modelspace().query(kind) if e.dxf.layer=='原有卫生间']
    b=[signature(e) for e in m.query(kind) if e.dxf.layer=='原有卫生间']
    assert collections.Counter(a)==collections.Counter(b)
old_wash=[signature(v) for e in old2.modelspace().query('INSERT') for v in e.virtual_entities()]
new_wash=[signature(v) for e in m.query('INSERT') for v in e.virtual_entities()]
assert collections.Counter(old_wash)==collections.Counter(new_wash)

new_wall_lines=[e for e in m.query('LINE') if e.dxf.layer=='新隔墙']
assert any(abs(e.dxf.start.y-7600)<.01 and abs(e.dxf.end.y-7600)<.01 for e in new_wall_lines)
assert any(abs(e.dxf.start.y-3600)<.01 and abs(e.dxf.end.y-3600)<.01 for e in new_wall_lines)
assert not any(abs(e.dxf.start.y-7100)<.01 and abs(e.dxf.end.y-7100)<.01 for e in new_wall_lines)
texts=[e.dxf.text for e in m.query('TEXT')]
assert '4000 mm' in texts and '3400 mm' in texts
assert any('15.4' in t and '包房二' in t for t in texts)
assert any('女卫无小便斗区' in t for t in texts)
assert not any(t in ('男卫*','女卫*','小便斗区*') for t in texts)

ellipses=[e for e in m.query('ELLIPSE') if e.dxf.layer=='洁具标识_示意']
assert {(round(e.dxf.center.x),round(e.dxf.center.y)) for e in ellipses}=={(1150,525),(3100,525)}
urinals=[e for e in m.query('ARC') if e.dxf.layer=='洁具标识_示意']
assert len(urinals)==1 and abs(urinals[0].dxf.center.y-1595)<.01 and urinals[0].dxf.center.x<2130
upper_row=[]
for e in m.query('LWPOLYLINE'):
    if e.dxf.layer!='餐桌':continue
    pts=list(e.get_points());y0=min(p[1] for p in pts)
    if y0>8800:upper_row.append((min(p[0] for p in pts),y0,max(p[0] for p in pts),max(p[1] for p in pts)))
assert upper_row==[(10300.0,9000.0,11500.0,9600.0),(12500.0,9000.0,13700.0,9600.0)]

geo=json.loads((OUT/'几何校核.json').read_text(encoding='utf-8'))
assert geo['failures']==[] and geo['screen_geometry_blocked']==[]
assert geo['room_two_clear_length_mm']==4000 and geo['private_net_areas_m2']==[13.09,15.4]
assert geo['upper_row_shift_mm']==600
assert geo['public_seats']=={'1':110,'2':60}
assert all(s['minimum_occupied_envelope_spacing_mm']>=800 for s in geo['table_spacing'])
assert len(list(OUT.glob('*.dwg')))==9
for path in OUT.glob('*.dwg'):
    name=path.stem;d=ezdxf.readfile(OUT/'DXF'/f'{name}.dxf')
    p=ezdxf.readfile(OUT/'DXF'/'打印源'/f'{name}.dxf')
    assert list(map(signature,d.modelspace()))==list(map(signature,p.modelspace()))
    with pymupdf.open(OUT/f'{name}.pdf') as pdf:assert len(pdf)==1
conv=json.loads((OUT/'转换验证.json').read_text(encoding='utf-8'))
assert len(conv)==9 and all(c['skipped']['count']==0 for c in conv)
assert hashlib.sha256((ROOT/'美莱食堂原始结构图.dwg').read_bytes()).hexdigest() in (OUT/'优化说明.md').read_text(encoding='utf-8')
print(json.dumps({'status':'PASS','room_two_length_mm':4000,'private_areas_m2':[13.09,15.4],
                  'upper_row_shift_mm':600,'WC_zones':'bottom squats / male top urinal / female no urinal',
                  'wash_area_identical_to_V13':True,'first_floor_identical_except_version':True,
                  'DWG_PDF_pairs':9,'geometry_errors':geo['failures']},ensure_ascii=False,indent=2))
