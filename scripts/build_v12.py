"""Build V1.2 from original CAD geometry; retain old deliverables as history.

Run with Python (ezdxf, shapely, pymupdf installed). CADCraft performs DWG/PDF
conversion. All dimensions below are millimetres in floor-local coordinates.
"""
from __future__ import annotations

import csv
import hashlib
import heapq
import json
import math
import random
import subprocess
from pathlib import Path

import ezdxf
import pymupdf
from ezdxf.addons import Importer
from ezdxf.enums import TextEntityAlignment
from ezdxf.math import Matrix44
from shapely.geometry import LineString, Polygon, box

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'deliverables' / 'V1.2'
CLI = Path(r'C:\Program Files\CADCraft\cadcraft-cli.exe')
SOURCE = ROOT / '美莱食堂原始结构图.dwg'
ORIGINS = {1: (73959.58264270716, 1014.8090422358064),
           2: (101794.44121770863, 10680.028566825611)}
COLORS = {
    '原有结构': (45, 45, 45), '原有卫生间': (70, 70, 70),
    '原有传菜梯': (25, 95, 150), '拟拆隔墙': (200, 60, 60),
    '新隔墙': (185, 100, 25), '门': (90, 115, 90),
    '餐桌': (35, 105, 75), '凳子300': (35, 105, 75),
    '厨房设备': (40, 90, 150), '打菜2人': (185, 95, 20),
    '唯一回收点': (150, 70, 30), '屏幕': (60, 75, 150),
    '净空保留': (110, 150, 160), '流线': (160, 75, 135),
    '文字': (35, 35, 35), '尺寸': (80, 85, 95), '图框': (50, 50, 50),
}

def make_doc():
    d = ezdxf.new('R2018', setup=True)
    d.header['$INSUNITS'] = 4
    d.styles.new('CN', dxfattribs={'font': 'simhei.ttf'})
    d.linetypes.new('PLAN_DASH', dxfattribs={'description': 'Plan clearance dashed',
                                          'pattern': [600.0, 400.0, -200.0]})
    for name, rgb in COLORS.items():
        la = d.layers.new(name)
        la.rgb = rgb
        la.dxf.lineweight = 25 if name in ('原有结构', '新隔墙') else 13
        if name in ('拟拆隔墙', '净空保留', '流线'):
            la.dxf.linetype = 'PLAN_DASH'
    return d

def ln(m, a, b, la='原有结构'):
    return m.add_line(a, b, dxfattribs={'layer': la})

def rect(m, r, la):
    x0, y0, x1, y1 = r
    return m.add_lwpolyline([(x0,y0),(x1,y0),(x1,y1),(x0,y1)], close=True,
                            dxfattribs={'layer': la})

def txt(m, s, p, h=180, la='文字', center=True, rot=0):
    e = m.add_text(s, dxfattribs={'height': h, 'style': 'CN', 'layer': la, 'rotation': rot})
    e.set_placement(p, align=TextEntityAlignment.MIDDLE_CENTER if center else TextEntityAlignment.LEFT)
    return e

def arrow(m, pts):
    for a,b in zip(pts, pts[1:]): ln(m,a,b,'流线')
    a,b = pts[-2:]
    t = math.atan2(b[1]-a[1],b[0]-a[0])
    for da in (-.5,.5):
        ln(m,b,(b[0]-220*math.cos(t+da),b[1]-220*math.sin(t+da)),'流线')

def dh(m, x0,x1,y,base):
    for x in (x0,x1):
        ln(m,(x,base),(x,y),'尺寸'); ln(m,(x-70,y-70),(x+70,y+70),'尺寸')
    ln(m,(x0,y),(x1,y),'尺寸'); txt(m,f'{x1-x0:.0f}',((x0+x1)/2,y+150),160,'尺寸')

def dv(m,y0,y1,x,base):
    for y in (y0,y1):
        ln(m,(base,y),(x,y),'尺寸'); ln(m,(x-70,y-70),(x+70,y+70),'尺寸')
    ln(m,(x,y0),(x,y1),'尺寸'); txt(m,f'{y1-y0:.0f}',(x+140,(y0+y1)/2),160,'尺寸',rot=90)

def wall(m,a,b):
    # 100mm double line with actual gaps at openings (no door drawn over solid wall).
    if a[0] == b[0]:
        x=a[0]
        for dx in (-50,50): ln(m,(x+dx,a[1]),(x+dx,b[1]),'新隔墙')
    else:
        y=a[1]
        for dy in (-50,50): ln(m,(a[0],y+dy),(b[0],y+dy),'新隔墙')

def slide(m,x,y,w=1000):
    ln(m,(x-35,y),(x-35,y+w),'门')
    ln(m,(x+35,y+w),(x+35,y+2*w),'门')
    ln(m,(x-100,y),(x+100,y),'门')
    ln(m,(x-100,y+w),(x+100,y+w),'门')

TABLES = {1: [], 2: []}
STOOLS = {1: [], 2: []}
KEEP = {1: [], 2: []}
OBJS = {1: [], 2: []}
NEW_WALLS = {1: [], 2: []}

def keep(f,name,r): KEEP[f].append((name,box(*r)))
def obj(f,name,r): OBJS[f].append((name,box(*r)))

def table(f,x,y,pairs,vertical=False):
    length = 600*pairs
    r = (x,y,x+600,y+length) if vertical else (x,y,x+length,y+600)
    seats=[]
    for i in range(pairs):
        for side in (-1,1):
            if vertical:
                cx=x-250 if side<0 else x+850; cy=y+300+600*i
            else:
                cx=x+300+600*i; cy=y-250 if side<0 else y+850
            seats.append((cx,cy))
            STOOLS[f].append(box(cx-150,cy-150,cx+150,cy+150))
    # Body envelope exceeds stool dimensions; 800mm aisle is measured OUTSIDE it.
    footprint=box(x-500,y-100,x+1100,y+length+100) if vertical else box(x-100,y-500,x+length+100,y+1100)
    TABLES[f].append({'id':f'{f}F-T{len(TABLES[f])+1:02}', 'table':r,
                      'pairs':pairs,'vertical':vertical,'seats':seats,'footprint':footprint})

def setup_layout():
    # Floor 1: two 6-seat tables in the lower wing; public route never enters BOH.
    table(1,8050,3600,3,True); table(1,8050,6600,3,True)
    for x,p in [(3300,4),(6700,3),(11300,4),(14700,4),(18100,2)]: table(1,x,15000,p)
    for x,p in [(1900,4),(5300,4),(11300,4),(14700,4),(18100,2)]: table(1,x,17400,p)
    for x,p in [(4150,4),(8000,4),(14900,4),(18300,2)]: table(1,x,19800,p)
    keep(1,'后门入口缓冲',(8200,600,11050,3200))
    keep(1,'员工主通道1750以上',(9250,3200,11050,9600))
    keep(1,'传菜梯旁1800主通道',(10100,9800,11900,12200))
    keep(1,'主厅1800通道',(9100,12200,11000,19300))
    keep(1,'主厅横向800通道',(1700,18500,19700,19300))
    keep(1,'楼梯门前',(1561,14150,3000,16200))
    keep(1,'上方左门门前',(1511,18800,3761,20930))
    keep(1,'上方右门门前',(11961,18800,14361,20930))
    keep(1,'传菜梯及1500操作面',(7421,10030,10071,11750))
    keep(1,'防火栓前',(5960,13250,7621,14350))
    # Floor 2: 2 rooms on right, dedicated 1440-wide guest aisle, lift apron below.
    for y in (5700,8100):
        table(2,2800,y,4); table(2,6200,y,4)
    table(2,4500,900,4)
    table(2,4400,3300,4)
    table(2,600,8500,2)
    keep(2,'原卫生间',(350,0,4170,3560))
    keep(2,'原楼梯及固定区',(350,3560,2700,7100))
    keep(2,'包房门前1440通道',(8700,100,10140,9700))
    keep(2,'下部800横向通道',(4170,2000,10140,2800))
    keep(2,'传菜梯及1800操作区',(7140,0,8740,2860))
    keep(2,'屏前活动和观看区',(2700,9400,8700,10500))
    # BOH and equipment are never placed in the public entrance or lift keepouts.
    obj(1,'厨房',(11150,800,14000,6200)); obj(1,'库房',(11150,6400,14000,8200))
    obj(1,'两人打菜台',(12000,9400,14000,10100))
    obj(1,'唯一回收台',(7700,12200,8300,14000))
    obj(2,'下包房',(10190,100,14040,3950)); obj(2,'上包房',(10190,4150,14040,8000))

# Remove only the lower-wing partitions that user allowed; retain original lift.
DEMO1 = set('2B482 2B502 2B505 2B4E8 2B503 2B4E9 2B504 2B484 2B489 2B48C 2B4DE 2B4F5 2B509 2B4F7 2B508 2B4FC 2B4FD 2B4FE 2B4FF 2B500 2B501 2B506 2B507'.split())
STAIR2 = set('2B16E 2B702 2B032 2B16B 2B031 2B16A 2B16C 2B16D 2B178 2B179 2B17A'.split())
WC2 = set('2B15E 2B162 2B163 2B14F 2B160 2B159 2B153 2B15B 2B154 2B15A 2B151 2B15D 2B152 2B15C 2B157 2B158'.split())
OUTER2 = set('2AF50 2AF56 2B230 2AF54 2B02F 2B02E 2B150'.split())
LIFT1 = set('2B472 2B473 2B474 2B475'.split())

SOURCE_POLYS = {1: [], 2: []}
PRESERVED_LINES = {1: [], 2: []}
ORIGINAL_REPORT=[]

def source_copy(d,m,src,f,demolition=False,structure_only=False):
    ox,oy=ORIGINS[f]
    def xy(p): return (float(p[0]-ox),float(p[1]-oy))
    def emit(a,b,layer):
        ln(m,a,b,layer)
        if layer not in ('拟拆隔墙','门'):
            PRESERVED_LINES[f].append(LineString([a,b]))
    for e in src.modelspace():
        kind=e.dxftype(); h=e.dxf.handle
        if kind=='LINE':
            if (e.dxf.start.x<100000) != (f==1): continue
            a,b=xy(e.dxf.start),xy(e.dxf.end)
            layer='原有结构'; remove=False
            if f==1:
                remove=h in DEMO1
                if h in LIFT1: layer='原有传菜梯'
                if h in ('2B4E0','2B4E5'): layer='门'  # original duplicate threshold, not a closed wall
            else:
                if h in OUTER2 or h in STAIR2: pass
                elif h in WC2: layer='原有卫生间'
                elif h in ('2B035','2B156','2B039','2B155'):
                    layer='原有卫生间'
                    if min(a[0],b[0]) >=4170:
                        remove=True
                    else:
                        # Preserve toilet top exactly within its existing footprint.
                        if max(a[0],b[0])>4170:
                            hi=(4170,a[1]); lo=min((a,b),key=lambda p:p[0])
                            emit(lo,hi,layer)
                            if demolition: ln(m,hi,max((a,b),key=lambda p:p[0]),'拟拆隔墙')
                            continue
                elif h=='2B038':
                    # Original 7440 line extends upward as a partition; preserve shaft part only.
                    emit((7440,0),(7440,1060),'原有传菜梯')
                    if demolition: ln(m,(7440,1060),(7440,3560),'拟拆隔墙')
                    continue
                elif h in ('2B03A','2B03B'): layer='原有传菜梯'
                else: remove=True
            if remove:
                if demolition: ln(m,a,b,'拟拆隔墙')
            elif f==2 and h in ('2B16B','2B032'):
                # Proposed 1000mm opening in an existing enclosure. Explicitly a
                # proposed cut, not an already-confirmed stair opening.
                if demolition: ln(m,(a[0],5500),(a[0],6500),'拟拆隔墙')
                emit((a[0],min(a[1],b[1])),(a[0],5500),layer)
                emit((a[0],6500),(a[0],max(a[1],b[1])),layer)
            else: emit(a,b,layer)
        elif kind=='LWPOLYLINE':
            pts=[xy(p) for p in e.get_points()]
            if not pts or (e[0][0]<100000)!=(f==1): continue
            m.add_lwpolyline(pts,close=e.closed,dxfattribs={'layer':'原有结构'})
            if e.closed: SOURCE_POLYS[f].append(Polygon(pts))
        elif kind=='ARC' and f==1:
            if e.dxf.center.x>=100000: continue
            m.add_arc(xy(e.dxf.center),e.dxf.radius,e.dxf.start_angle,e.dxf.end_angle,dxfattribs={'layer':'门'})
        elif kind=='INSERT' and f==2:
            # This is the ORIGINAL WC door block, not new fixtures.
            imp=Importer(src,d); before=set(x.dxf.handle for x in m)
            imp.import_entity(e,target_layout=m); imp.finalize()
            for inserted in m:
                if inserted.dxf.handle not in before:
                    inserted.transform(Matrix44.translate(-ox,-oy,0))
                    inserted.dxf.layer='原有卫生间'

def draw_tables(m,f):
    for t in TABLES[f]:
        rect(m,t['table'],'餐桌')
        for cx,cy in t['seats']: rect(m,(cx-150,cy-150,cx+150,cy+150),'凳子300')

def new_walls(m,f):
    segments=[]
    if f==1:
        # Simple kitchen/store only; no cold room, pantry, waste room, etc.
        segments=[((11100,600),(11100,4800)),((11100,5800),(11100,6300)),
                  ((11100,6300),(14140,6300)),((11100,6300),(11100,7000)),
                  ((11100,8000),(11100,8300)),((11100,8300),(14140,8300))]
        slide(m,11100,4800); slide(m,11100,7000)
    else:
        segments=[((10140,100),(10140,1500)),((10140,2500),(10140,5500)),
                  ((10140,6500),(10140,8100)),((10140,4050),(14140,4050)),
                  ((10140,8100),(14140,8100))]
        slide(m,10140,1500); slide(m,10140,5500)
        slide(m,1830,5500)
    for a,b in segments:
        wall(m,a,b); NEW_WALLS[f].append(LineString([a,b]).buffer(50,cap_style=2))

def equipment(m,f):
    if f==1:
        for r,s in [((13000,1000,13950,2800),'双眼灶/排烟罩'),
                    ((13000,3100,13950,4100),'蒸饭/主食'),
                    ((11300,1000,11900,2600),'清洗/切配'),
                    ((11300,2900,11900,3900),'冷柜'),
                    ((12500,5300,13900,5900),'工作台'),
                    ((13500,6500,14000,8100),'货架')]:
            rect(m,r,'厨房设备'); txt(m,s,((r[0]+r[2])/2,(r[1]+r[3])/2),130,'厨房设备')
        rect(m,(12000,9400,14000,10100),'打菜2人')
        ln(m,(13000,9400),(13000,10100),'打菜2人')
        for x,s in [(12500,'师傅1'),(13500,'师傅2')]: txt(m,s,(x,9750),180,'打菜2人')
        rect(m,(7700,12200,8300,14000),'唯一回收点')
        txt(m,'全楼唯一餐具回收',(8000,13100),140,'唯一回收点',rot=90)
        # Compact washing module inside kitchen, not in the queue or main route.
        rect(m,(11300,4100,11900,4700),'厨房设备')
        txt(m,'洗消点',(11600,4400),120,'厨房设备')
    else:
        for cy in (2050,6050):
            m.add_circle((12240,cy),750,dxfattribs={'layer':'餐桌'})
            for i in range(8):
                a=2*math.pi*i/8; cx=12240+1000*math.cos(a); yy=cy+1000*math.sin(a)
                rect(m,(cx-150,yy-150,cx+150,yy+150),'凳子300')
        # Mount on ORIGINAL upper wall, between column positions. No screen partition.
        rect(m,(4300,10400,6700,10500),'屏幕')
        txt(m,'上方墙面显示屏 2400×1350',(5500,10850),180,'屏幕')

def clearances(m,f):
    for name,p in KEEP[f]:
        # Avoid drawing around entire toilets/stairs, only relevant circulation envelopes.
        if name.startswith('原'): continue
        rect(m,p.bounds,'净空保留')
    if f==1:
        arrow(m,[(9600,700),(10150,3400),(10150,9500),(11050,12200),(10150,15800)])
        txt(m,'员工主入口（现状门洞约1150，门内不设库房）',(9600,-300),195)
        txt(m,'入口缓冲 / 不摆桌',(9650,2000),190)
        txt(m,'主通道1800',(10150,7000),180,rot=90)
        txt(m,'传菜梯操作面1500',(9400,11150),155)
        txt(m,'排队在右侧，不占主通道',(12900,12600),160)
        txt(m,'楼梯及门前保持通畅',(3200,13700),170)
        txt(m,'门前净空',(2650,19550),160)
        txt(m,'门前净空',(13150,19550),160)
    else:
        arrow(m,[(9300,3000),(9300,6500),(9300,9550),(7800,9550)])
        txt(m,'包房专用通道1440',(9450,4400),180,rot=90)
        txt(m,'传菜梯操作/取送1800',(7950,2300),160)
        txt(m,'观看 / 活动留空',(5500,9850),185)
        txt(m,'原固定区/上楼口复核',(1400,6700),145)
        txt(m,'通往一层回收点',(1400,6100),145)

def labels(m,f):
    if f==1:
        txt(m,'简化厨房 约15.4㎡',(12500,4500),180,'厨房设备')
        txt(m,'库房 约5.1㎡',(12600,7550),180,'厨房设备')
        txt(m,'2人打菜 / 2个工位',(12600,10600),190,'打菜2人')
        txt(m,'原有传菜梯',(8000,10880),165,'原有传菜梯')
        txt(m,'公共座位 '+str(sum(len(t['seats']) for t in TABLES[1]))+' 座',(15800,21400),240)
        txt(m,'600mm桌面 / 300mm凳面 / 按600mm一对座位',(11000,22250),220)
    else:
        txt(m,'原男/女卫生间及蹲位原样保留',(2100,-450),190,'原有卫生间')
        txt(m,'传菜梯（原位保留）',(7940,650),145,'原有传菜梯')
        txt(m,'包房一 / 8人',(12140,3700),190)
        txt(m,'包房二 / 8人',(12140,7700),190)
        txt(m,'两包房约15.0㎡/间（净面积）',(12200,8500),170)
        txt(m,'公共 '+str(sum(len(t['seats']) for t in TABLES[2]))+' 座 + 包房16座',(5500,11450),240)

def title(m,f,title_s):
    # Drawn full size in model space. PDF is fit-to-paper, NOT a claimed fixed 1:100 plot.
    if f==1: bounds=(-1800,-3000,22000,23500); xpos=10500; top=23000
    else: bounds=(-1200,-3000,16900,12900); xpos=7800; top=12400
    rect(m,bounds,'图框'); txt(m,title_s,(xpos,top),350)
    txt(m,'美莱食堂 | V1.2 简洁优化 | 单位mm | 模型1:1；PDF适合页面打印',(xpos,-1200),190)
    txt(m,'深绿：桌凳  蓝：原传菜梯/设备  橙：新墙/两人打菜  虚线：必须留空',(xpos,-1700),170)
    txt(m,'桌边留100+凳面300+人体余量100；外侧次通道≥800，主通道优先1800',(xpos,-2150),165)
    txt(m,'拆墙按业主可拆隔墙意向表达；原图未提供结构证明，施工前核实',(xpos,-2550),160)

def dimensions(m,f):
    if f==1:
        dh(m,460.94,19840.94,21700,20930)
        dv(m,600,14030,15050,14140)
        dh(m,9250,11050,9200,8500)
        dh(m,3300,5700,14500,15000)
        dv(m,15000,15600,6100,5700)
        dh(m,11150,14000,550,800)
    else:
        dh(m,350,14140,11950,10500)
        dv(m,0,10500,15500,14140)
        dh(m,8700,10140,8400,8100)
        dv(m,1060,2860,8900,8440)

def verify(src):
    failures=[]; spacing=[]
    for f in (1,2):
        envelope=Polygon([(460.94,14030),(7420.94,14030),(7420.94,600),(14180.94,600),
                          (14140.94,14030),(19840.94,14030),(19840.94,20930),(460.94,20930)]) if f==1 else box(350,0,14140,10500)
        for t in TABLES[f]:
            p=t['footprint']
            if not envelope.buffer(1).covers(p): failures.append(f"{t['id']} outside envelope")
            for name,q in KEEP[f]+OBJS[f]:
                if p.intersection(q).area>1: failures.append(f"{t['id']} overlaps {name}")
            for q in SOURCE_POLYS[f]+NEW_WALLS[f]:
                if p.intersection(q).area>1: failures.append(f"{t['id']} overlaps column/new wall")
            for q in PRESERVED_LINES[f]:
                if p.buffer(-1).intersects(q): failures.append(f"{t['id']} overlaps original wall")
        ds=[a['footprint'].distance(b['footprint']) for i,a in enumerate(TABLES[f]) for b in TABLES[f][i+1:]]
        spacing.append({'floor':f,'minimum_occupied_envelope_spacing_mm':round(min(ds),1)})
        if min(ds)<799: failures.append(f'{f}F furniture body envelope spacing <800: {min(ds)}')
        for name,p in OBJS[f]:
            for k,q in KEEP[f]:
                if p.intersection(q).area>1: failures.append(f'{f}F {name} overlaps {k}')
    # All public sightlines checked against opaque rooms/WC/stair + shaft walls, not other people.
    opaque=[box(10140,0,14140,8100),box(350,0,4170,3560),box(350,3560,2500,7000),box(7440,0,8440,1060)]+SOURCE_POLYS[2]
    blocked=[]
    for t in TABLES[2]:
        for p in t['seats']:
            sight=LineString([p,(5500,10400)])
            if any(sight.intersection(q).length>1 for q in opaque): blocked.append([t['id'],p])
    if blocked: failures.append(f'public screen sightlines blocked: {blocked}')
    # Guest-room stools have a 1250mm occupied radius including body allowance;
    # the west-side service strip is >=800mm clear to the inner face of wall.
    for cy in (2050,6050):
        occupied=box(12240-1250,cy-1250,12240+1250,cy+1250)
        room=box(10190,100 if cy==2050 else 4150,14040,3950 if cy==2050 else 8000)
        if not room.covers(occupied): failures.append('private seating outside room')
        if occupied.bounds[0]-10190 <800: failures.append('private door-side aisle <800')
    result={'failures':failures,'table_spacing':spacing,'public_seats':{str(f):sum(len(t['seats']) for t in TABLES[f]) for f in (1,2)},
            'private_seats':16,'screen_geometry_blocked':blocked,
            'original_wc_line_handles_retained':sorted(WC2),
            'original_1f_lift_line_handles_retained':sorted(LIFT1),
            'toilet_fixtures_added':0,
            'checks':'table+stool+body envelopes / protected routes / door buffers / original wall lines / columns / new walls / lift landing / public wall sightlines',
            'limits':'Does not establish field dimensions, egress compliance, actual human occupancy, production capacity or accessible-route compliance.'}
    (OUT/'几何校核.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    if failures: raise RuntimeError('\n'.join(failures))
    return result

def simulation():
    """Deterministic sensitivity analysis, NOT measured operational capacity."""
    n1,n2=(sum(len(t['seats']) for t in TABLES[f]) for f in (1,2))
    rows=[]
    for scenario in ('均匀45分钟到达','自然波动45分钟到达','前10分钟集中到达'):
        rng=random.Random(20261018)
        if scenario.startswith('均匀'):
            arrivals=[45*i/599 for i in range(600)]
        elif scenario.startswith('自然'):
            arrivals=sorted(45*rng.betavariate(2,2) for _ in range(600))
        else:
            arrivals=sorted(10*rng.random() for _ in range(600))
        for seconds in (8,12,20,30):
            servers=[0.0,0.0]
            seats={1:[0.0]*n1,2:[0.0]*n2}
            for v in seats.values(): heapq.heapify(v)
            last_service=last_eat=last_release=max_queue=0
            # Build actual FCFS service starts first, then compute waiting counts.
            starts=[]
            for arrival in arrivals:
                available=heapq.heappop(servers)
                start=max(arrival,available); end=start+seconds/60
                heapq.heappush(servers,end); starts.append(start)
                last_service=max(last_service,end)
                # Select earliest available floor, including assumed travel time.
                choices=[]
                for f,travel in ((1,.5),(2,1.5)):
                    choices.append((max(end+travel,seats[f][0]),f))
                sit,f=min(choices)
                heapq.heappop(seats[f]); heapq.heappush(seats[f],sit+17)
                last_eat=max(last_eat,sit+15); last_release=max(last_release,sit+17)
            waiting=[(a,s) for a,s in zip(arrivals,starts) if s>a+1e-9]
            events=[(a,1) for a,s in waiting]+[(s,-1) for a,s in waiting]
            count=0
            for _,delta in sorted(events,key=lambda p:(p[0],p[1])):
                count+=delta; max_queue=max(max_queue,count)
            rows.append([scenario,seconds,round(last_service,1),round(last_eat,1),round(last_release,1),max_queue,'是' if last_eat<=60 else '否'])
    with (OUT/'两人供餐敏感性.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['到达场景','每师傅每完整套餐秒数','最后取餐分钟','最后吃完分钟','最后清台分钟','最大等待人数','60分钟全部吃完']);w.writerows(rows)
    md=['# 两人供餐敏感性分析（V1.2）','','固定2名师傅、2工位，不计包房员工容量。以下为假设模型，不是实测结果。',
        f'公共座位：一层{n1}、二层{n2}。每人用餐15分钟、清台2分钟；取餐后步行一层0.5分钟/二层1.5分钟。按各层座位可用时刻分配，先进先出取餐。',
        '模型没有细化楼梯双向排队、厨房缺菜、入口限流、送盘中断或收盘服务，实际表现可能更慢。',
        '自然波动使用固定随机种子20261018，45分钟Beta(2,2)到达；集中到达使用前10分钟均匀随机。',
        '', '|场景|秒/人/师傅|最后取餐|最后吃完|最后清台|最大等待人数|60分钟达标|',
        '|---|---:|---:|---:|---:|---:|---|']
    md += ['|'+'|'.join(map(str,r))+'|' for r in rows]
    md += ['', '## 采用建议', '',
           '先按2人实际菜单试打至少30份，记录从领取餐盘到完整套餐交付的时间，不能把只舀一勺菜的时间当作整份套餐时间。',
           '预分装餐盘、自取米饭/汤和错峰可以尝试；若试运行仍达不到60分钟，就延长就餐窗口或减少同一窗口堂食人数，本版不擅自增人、增工位。',
           '最大队列可能远超过设计排队区，仅用于证明拥堵风险，不能将大量员工全部容纳在图中小排队区，更不能排至楼梯或疏散门口。']
    (OUT/'两人供餐敏感性分析.md').write_text('\n'.join(md),encoding='utf-8')

def reports(check,conversion,initial_hash):
    n1,n2=(check['public_seats'][str(f)] for f in (1,2)); total=n1+n2
    req=ROOT/'docs'/'需求文档.md'
    (OUT/'优化说明.md').write_text(f'''# 美莱食堂 V1.2 简洁优化说明

## 本次方案
- 一层公共{n1}座，二层公共{n2}座，合计{total}座；两包房各8座，共16座，不计入员工容量。
- 公共桌面600mm深；每600mm桌长配一对相向座位，采用1200/1800/2400mm长桌；全部凳面300×300mm。
- 通道按“桌外100mm间隙+300mm凳面+100mm人体余量”后校核；最小桌组人体占用包络间距800mm，不把300mm凳面当作全部人体空间。

## 一层：员工入口直达就餐，简化厨房
图下方后门为员工主入口。门内留空，主通道沿中间上行，整个过程不穿过厨房或库房。门洞原状约1150mm，未擅自扩大；门内1800mm主通道不能消除门洞本身的瓶颈。

厨房在右下角，约15.4㎡（2850×5400），旁设普通库房约5.1㎡；不再独立设置冷库、垃圾间、入口收货间。双眼灶、蒸饭、冷柜、清洗切配、工作台简化表示，不按面积保证600餐完整生产能力。

右侧仅2个打菜工位、2名师傅，台面2000×700mm，后留约1000mm工作带；排队在右侧，不占员工主通道。两层共用唯一回收台在一层大厅下方左侧，毗邻主通道，采用一体收盘/分类设施，另配紧凑洗消点；最终洁污流程仍需结合设备与给排水深化。

一层原传菜梯是原图中段1150×1320mm方框，绝非保洁间。保留轮廓，东侧退1500mm操作面；同段主通行路线向右让开，留1800mm通过带。原防火栓、楼梯及图上方两个门前预留净空。

## 二层：仅两个包房，其余开放
卫生间完全沿用原图墙线、隔断/蹲位线和原有门块，不增加WC、尿斗或水池；原图未说明男女对应关系时不重分配。原楼梯形固定区域和结构柱保留。

原东侧长隔墙、中间不必要隔墙按拟拆处理；原下方传菜梯（1000×1060mm）保留，并留1800mm操作/取送面。新的两间包房移至右侧下、中部，约15㎡净面积/间，圆桌直径1500mm，8个300mm凳位；门洞真实断开，门前1440mm专用通道不摆桌凳。二层不设服务间，不设回收区/回收车。

显示屏挂图上方原墙、避开柱，位置x=4300—6700mm，参考2400×1350mm，底标高建议约1200mm；取消上一版中央屏墙。主要公共餐桌朝向布局与上方屏幕平行，公共位到屏幕中心的平面视线已检查，不穿过包房、卫生间、楼梯围合区或传菜梯。人员站立遮挡、显示屏俯仰角/文字大小需实物确认；包房不承诺观看公共屏幕。

原图二层左侧梯形固定区的用途和上楼对位尚缺定位依据，不再将其直接认定为已验证楼梯。按既有固定区预留，东侧1000mm通行口作为拟开门洞表达；是否可开及其与真实楼梯关系需现场核对。

## 关于600人/60分钟
本版尊重2人打菜，不增加工位。2人平均每人20秒完成一份完整套餐，理论6人/分钟、600份仅取餐需100分钟；每人12秒则刚好10人/分钟，60分钟无任何就餐尾时，不能作为已满足目标。

若最后一人还要留15分钟就餐及约2分钟通行，取餐需在43分钟结束，2人需每人约8.6秒完成完整一份；该速度必须实测，不能假定。可先确定菜单和份量，试做预分装餐盘、米饭/汤自行领取、提前备餐，但本版仍只配置2名打菜人员。

因此“600人60分钟全部吃完”目前**未验证满足**；如实测不能达成，优先调整分批窗口/预分装流程，而非擅改本版2人约束。公共{total}座若持续15分钟占座，简单座位小时上限约{total*4}人次（不含取餐/通行），也不能替代完整运营验证。

详见`两人供餐敏感性分析.md`和CSV：分别计算均匀到达、自然波动、集中到达，以及8/12/20/30秒每完整套餐的假设场景，包含取餐、步行、按楼层找座、吃完和清台尾时，不把小时平均速度当作全部完成时间。

## 核实事项
- 一、二层原图量取围合参考约224.5/144.8㎡，不是完整法定建筑面积；净可用面积需逐区闭合测量及现场复测。
- 原图一、二层传菜梯均有文字证据，但两张平面未给定位轴网，不能仅凭平移认定竖向对位；固定区、楼梯、传菜梯和所有结构柱均保留，竖向关系待现场确认。
- 拟拆墙体按业主可拆意向表达，不代表已完成结构/消防认定。
- 厨房约15㎡是本次简化意向，不代表完整烹饪600餐已通过工艺核算；菜单、设备和提前加工方式需确认。
- 唯一回收点位于一层，二层员工端空盘下楼；传菜梯是否允许脏餐具运输、能否时段隔离需确认，不默认洁污同运。

## 文件及验证
源DWG未更改（SHA256 `{initial_hash}`）。9套编辑DWG/DXF、对应PDF，另附两层及综合PNG预览。
DWG重新打开的实体数/跳过数见`转换验证.json`；读入无跳过只证明文件可解析，不代表结构、卫生或疏散合规。
几何检查见`几何校核.json`；保留原始尺寸，不使用截图描摹，不沿用上一版新增卫生间设施。
模型1:1毫米，PDF按页面适配输出，**不是标注为1:100的定比施工图**；不提供未实测的北向。
需求来源：`{req.relative_to(ROOT)}` V1.2增补。
''',encoding='utf-8')
    (OUT/'转换验证.json').write_text(json.dumps(conversion,ensure_ascii=False,indent=2),encoding='utf-8')
    with (OUT/'桌位统计.csv').open('w',encoding='utf-8-sig',newline='') as fh:
        w=csv.writer(fh); w.writerow(['楼层','桌号','桌长mm','桌深mm','座位','凳面mm'])
        for f in (1,2):
            for t in TABLES[f]: w.writerow([f,t['id'],600*t['pairs'],600,len(t['seats']),300])
        w.writerow(['二层','包房一',1500,'圆桌',8,300]);w.writerow(['二层','包房二',1500,'圆桌',8,300])
    (ROOT/'deliverables'/'README.md').write_text('''# 当前方案入口

**当前最新：V1.2 简洁优化版。**

请先查看：[V1.2优化说明](V1.2/优化说明.md)、[一层预览](V1.2/预览图/一楼功能分区与家具布置图.png)、[二层预览](V1.2/预览图/二楼功能分区与家具布置图.png)。

V1.2统一采用600mm公共桌深、300mm凳面、2人打菜，后门为员工主入口；二层原卫生间和传菜梯保留，无服务间和二层回收点。

本目录根部原有图纸、报告属于V1.1历史方案（含5工位等已取消内容），以V1.2版本目录为准。
''',encoding='utf-8')

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for name in ('DXF','预览图'): (OUT/name).mkdir(exist_ok=True)
    initial=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    source_dxf=OUT/'DXF'/'原始基准_只读转换.dxf'
    subprocess.run([str(CLI),'convert',str(SOURCE),str(source_dxf)],check=True,capture_output=True)
    src=ezdxf.readfile(source_dxf)
    setup_layout()
    sheets=[(1,'一楼原始结构及拆改平面图','demo'),(1,'一楼功能分区与家具布置图','furn'),
            (1,'一楼厨房及打菜设备布置图','equip'),(1,'一楼尺寸标注平面图','dim'),
            (2,'二楼原始结构及拆改平面图','demo'),(2,'二楼功能分区与家具布置图','furn'),
            (2,'二楼尺寸标注平面图','dim')]
    docs={}; conversion=[]
    for f,name,mode in sheets:
        d=make_doc();m=d.modelspace()
        source_copy(d,m,src,f,demolition=mode=='demo')
        new_walls(m,f)
        if mode in ('furn','dim'): draw_tables(m,f)
        if mode!='demo': equipment(m,f)
        clearances(m,f);labels(m,f)
        if mode=='dim': dimensions(m,f)
        title(m,f,name)
        if mode=='demo': txt(m,'红虚线为拟拆；保留卫生间、传菜梯、柱和楼梯固定区',(10000 if f==1 else 7000,8700 if f==1 else 8800),160)
        docs[name]=d
    verify(src)
    # Combined plan uses entity transform, including TEXT alignment points and INSERT.
    combo=make_doc();cm=combo.modelspace()
    for f,name in [(1,'一楼功能分区与家具布置图'),(2,'二楼功能分区与家具布置图')]:
        s=docs[name]; imp=Importer(s,combo)
        before=set(e.dxf.handle for e in cm)
        imp.import_entities([e for e in s.modelspace() if e.dxf.layer!='图框'],target_layout=cm);imp.finalize()
        if f==2:
            for e in cm:
                if e.dxf.handle not in before: e.transform(Matrix44.translate(24000,0,0))
    rect(cm,(-1800,-3000,40500,23500),'图框')
    txt(cm,'美莱食堂 V1.2 / 一二层简洁综合方案',(19000,23000),350)
    txt(cm,'600桌深 / 300凳面 / 2人打菜 / 原卫生间及传菜梯保留',(19000,-1700),220)
    txt(cm,'单位mm，模型1:1；PDF适合页面打印，非定比例施工图',(19000,-2350),180)
    docs['一二楼综合设计图']=combo
    # 9th sheet highlights 600/300 module with a real dimensioned schematic.
    detail=make_doc();dm=detail.modelspace()
    rect(dm,(0,0,2400,600),'餐桌')
    for i in range(4):
        for cy in (-250,850): rect(dm,(150+600*i,cy-150,450+600*i,cy+150),'凳子300')
    dh(dm,0,2400,1500,600);dv(dm,0,600,2900,2400);dh(dm,0,600,-1000,0)
    rect(dm,(-100,-500,2500,1100),'净空保留')
    rect(dm,(-100,1900,2500,3500),'净空保留')
    rect(dm,(0,2400,2400,3000),'餐桌')
    dv(dm,1100,1900,3300,2500)
    txt(dm,'2400×600桌 / 4对8人 / 凳面300×300',(1200,4200),210)
    txt(dm,'人体余量后仍留800mm次通道；主通道按1800mm优先',(1200,3900),180)
    rect(dm,(-1800,-2600,6000,5200),'图框')
    txt(dm,'V1.2 餐桌模块与通道校核',(2000,4800),250)
    txt(dm,'门洞、包房门前和传菜梯操作区另按总平面留空',(2000,-2000),150)
    docs['餐桌600与凳面300及通道详图']=detail
    for name,d in docs.items():
        dx=OUT/'DXF'/f'{name}.dxf';d.saveas(dx)
        for ext in ('dwg','pdf'):
            p=OUT/f'{name}.{ext}'
            r=subprocess.run([str(CLI),'convert',str(dx),str(p)],capture_output=True,text=True,encoding='utf-8',errors='replace')
            if r.returncode: raise RuntimeError(r.stderr)
        r=subprocess.run([str(CLI),'info',str(OUT/f'{name}.dwg')],check=True,capture_output=True,text=True,encoding='utf-8')
        info=json.loads(r.stdout)
        if info.get('skipped',{}).get('count',0): raise RuntimeError(f'{name}: skipped entities')
        if info['entityCount']!=len(d.modelspace()): raise RuntimeError(f'{name}: entity count changed')
        conversion.append({'file':name+'.dwg','entities':info['entityCount'],'skipped':info.get('skipped')})
        if name in ('一楼功能分区与家具布置图','二楼功能分区与家具布置图','一二楼综合设计图','餐桌600与凳面300及通道详图'):
            with pymupdf.open(OUT/f'{name}.pdf') as pdf:
                pdf[0].get_pixmap(dpi=200).save(OUT/'预览图'/f'{name}.png')
    result=verify(src)
    simulation()
    reports(result,conversion,initial)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==initial,'Original DWG changed!'
    print(json.dumps({'output':str(OUT),'seats':result['public_seats'],'DWGs':len(conversion),'geometry_failures':result['failures']},ensure_ascii=False))

if __name__=='__main__': main()
