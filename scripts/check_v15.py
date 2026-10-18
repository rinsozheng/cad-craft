"""Independent verification of saved V1.5 artifacts."""
import collections
import hashlib
import json
import math
from pathlib import Path

import ezdxf
import pymupdf

from build_v12 import LIFT1, ORIGINS, WC2
from build_v13 import ACI

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'deliverables'/'V1.5'
PREV=ROOT/'deliverables'/'V1.4'
source=ezdxf.readfile(OUT/'DXF'/'原始基准_只读转换.dxf')

def normal(v):
    if isinstance(v,str):return v.replace('V1.5','V1.4')
    if isinstance(v,(int,float,bool)) or v is None:return v
    if isinstance(v,dict):return {k:normal(x) for k,x in v.items()}
    return [normal(x) for x in v]

def sig(e):
    a={k:v for k,v in e.dxf.all_existing_dxf_attribs().items() if k not in ('handle','owner')}
    d={'type':e.dxftype(),'attributes':normal(a)}
    if e.dxftype()=='LWPOLYLINE':d['points']=normal(list(e.get_points()))
    return json.dumps(d,sort_keys=True,ensure_ascii=False)

def lk(a,b):
    return tuple(sorted(tuple(round(float(p[i]),2) for i in (0,1)) for p in (a,b)))

for f,name,stools in [(1,'一楼功能分区与家具布置图',110),(2,'二楼功能分区与家具布置图',80)]:
    d=ezdxf.readfile(OUT/'DXF'/f'{name}.dxf');m=d.modelspace()
    assert d.header['$INSUNITS']==4
    for la,c in ACI.items():
        assert d.layers.get(la).dxf.color==c and not d.layers.get(la).dxf.hasattr('true_color')
    chairs=[e for e in m.query('LWPOLYLINE') if e.dxf.layer=='凳子300']
    assert len(chairs)==stools,(f,len(chairs))
    for e in chairs:
        p=list(e.get_points())
        assert all(abs(max(q[i] for q in p)-min(q[i] for q in p)-300)<.01 for i in (0,1))
    linekeys={lk(e.dxf.start,e.dxf.end) for e in m.query('LINE')}
    ox,oy=ORIGINS[f]
    for h in (LIFT1 if f==1 else WC2):
        e=source.entitydb[h]
        assert lk((e.dxf.start.x-ox,e.dxf.start.y-oy),
                  (e.dxf.end.x-ox,e.dxf.end.y-oy)) in linekeys,h
    if f==1:
        old=ezdxf.readfile(PREV/'DXF'/f'{name}.dxf')
        assert collections.Counter(map(sig,old.modelspace()))==collections.Counter(map(sig,m))
    else:
        # Room 2 is 4000 length, room 1 3400; upper row at 9000.
        lines=[e for e in m.query('LINE') if e.dxf.layer=='新隔墙']
        assert any(abs(e.dxf.start.y-7600)<.01 and abs(e.dxf.end.y-7600)<.01 for e in lines)
        assert any(abs(e.dxf.start.y-3600)<.01 and abs(e.dxf.end.y-3600)<.01 for e in lines)
        circles=[e for e in m.query('CIRCLE') if e.dxf.layer=='餐桌']
        assert sorted(round(e.dxf.radius) for e in circles)==[750,900]
        text=[e.dxf.text for e in m.query('TEXT')]
        assert any('公共60座' in s and '包房20座' in s for s in text)
        assert any('包房二 / 12人' in s for s in text)
        assert 'Φ1800 mm / 12人' in text
        assert '4000 mm' in text and '3400 mm' in text
        row=[e for e in m.query('LWPOLYLINE') if e.dxf.layer=='餐桌'
             and abs(min(p[1] for p in e.get_points())-9000)<.01]
        assert len(row)==2
        # 12 private chairs around the larger table, 8 around the smaller.
        def near(rt):
            return [e for e in chairs if math.dist(
                ((min(p[0] for p in e.get_points())+max(p[0] for p in e.get_points()))/2,
                 (min(p[1] for p in e.get_points())+max(p[1] for p in e.get_points()))/2),rt)<1600]
        assert len(near((12415,5600)))==12
        assert len(near((12240,1800)))==8
        west_edge=min(min(p[0] for p in e.get_points()) for e in chairs if math.dist(
            ((min(p[0] for p in e.get_points())+max(p[0] for p in e.get_points()))/2,
             (min(p[1] for p in e.get_points())+max(p[1] for p in e.get_points()))/2),(12415,5600))<1600)
        assert west_edge-10190>=924
        assert '男卫门' in text and '女卫门' in text
        assert any('小便斗区（近楼梯）' in s for s in text)
        assert not any('女卫无小便斗区' in s for s in text)
        assert '蹲位1' in text and '蹲位2' in text
        squats=[e for e in m.query('ELLIPSE') if e.dxf.layer=='洁具标识_示意']
        assert {(round(e.dxf.center.x),round(e.dxf.center.y)) for e in squats}=={(725,700),(1475,700),(2700,700),(3600,700)}
        urinals=[e for e in m.query('LWPOLYLINE') if e.dxf.layer=='洁具标识_示意'
                 and abs(min(p[1] for p in e.get_points())-1550)<.01]
        assert len(urinals)==2
        assert any('洗手区（原样保留）' in s for s in text)
        prev=ezdxf.readfile(PREV/'DXF'/f'{name}.dxf')
        old_wash=[sig(v) for e in prev.modelspace().query('INSERT') for v in e.virtual_entities()]
        new_wash=[sig(v) for e in m.query('INSERT') for v in e.virtual_entities()]
        assert collections.Counter(old_wash)==collections.Counter(new_wash)
        # Screen mounting geometry, room 2 dimensions and table clearance.
        assert '400 mm' in text and '925 mm' not in text
        geo=json.loads((OUT/'几何校核.json').read_text(encoding='utf-8'))
        assert geo['failures']==[] and geo['screen_geometry_blocked']==[]
        assert geo['private_seats']==20
        assert geo['private_tables'][1]=={'room':2,'centre':[12415,5600.0],
                                          'diameter_mm':1800,'seats':12,'west_aisle_mm':925.0}
        assert geo['public_seats']=={'1':110,'2':60}
        assert all(s['minimum_occupied_envelope_spacing_mm']>=800 for s in geo['table_spacing'])

assert len(list(OUT.glob('*.dwg')))==9
for path in OUT.glob('*.dwg'):
    name=path.stem
    d=ezdxf.readfile(OUT/'DXF'/f'{name}.dxf')
    p=ezdxf.readfile(OUT/'DXF'/'打印源'/f'{name}.dxf')
    assert list(map(sig,d.modelspace()))==list(map(sig,p.modelspace()))
    with pymupdf.open(OUT/f'{name}.pdf') as pdf:assert len(pdf)==1
conv=json.loads((OUT/'转换验证.json').read_text(encoding='utf-8'))
assert len(conv)==9 and all(c['skipped']['count']==0 for c in conv)
assert hashlib.sha256((ROOT/'美莱食堂原始结构图.dwg').read_bytes()).hexdigest() in (OUT/'优化说明.md').read_text(encoding='utf-8')
print(json.dumps({'status':'PASS','room_one':'8 seats / Φ1500','room_two':'12 seats / Φ1800',
                  'room_two_west_aisle_mm':925,'public_seats':[110,60],'private_seats':20,
                  'toilets':'2 squat stalls each at bottom; 2 male urinals at top; male WC door',
                  'wash_area_identical_to_V14':True,'first_floor_identical_except_version':True,
                  'DWG_PDF_pairs':9},ensure_ascii=False,indent=2))
