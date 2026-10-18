"""V1.3 refinement. Reuses V1.2 CAD primitives, never overwrites V1.2 outputs.

DWG/DXF use adaptive ACI colours for a dark model background. PDF sources have
independent dark-on-white true colours. Geometry is identical between the two.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess

import ezdxf
import pymupdf
from ezdxf.addons import Importer
from ezdxf.math import Matrix44
from shapely.geometry import LineString, Polygon, box

import build_v12 as B

OUT = B.ROOT / 'deliverables' / 'V1.3'
ACI = {'原有结构':7,'原有卫生间':7,'原有传菜梯':4,'拟拆隔墙':1,
       '新隔墙':30,'门':3,'餐桌':3,'凳子300':3,'厨房设备':4,'打菜2人':30,
       '唯一回收点':30,'屏幕':6,'净空保留':9,'流线':6,'文字':7,'尺寸':2,'图框':7,
       '楼梯踏步':4,'梯下投影':9,'常闭门':2,'消防标识':1,'洁具标识_示意':4}
PRINT_RGB = dict(B.COLORS, **{'楼梯踏步':(30,100,145),'梯下投影':(110,120,130),
                           '常闭门':(150,90,25),'消防标识':(175,35,35),
                           '洁具标识_示意':(30,100,145)})
ROOMS = [(10190,100,14040,3500),(10190,3600,14040,7050)]
ROUND_CENTRES = [(12240,1800),(12240,5325)]
HYDRANTS = [
    {'id':'FH-1-01','floor':1,'handle':'2B5FC','point':(585.94,20395),
     'label':(-650,20350),'elbow':(-200,20395),'rotation':90,
     'basis':'原图标注与左上方柜体轮廓相邻，柜体约250×1230'},
    {'id':'FH-1-02','floor':1,'handle':'2B5F9','point':(6790.94,13800),
     'label':(5000,12100),'elbow':(6100,12400),'rotation':0,
     'basis':'原图标注与一层大厅左下角1260×700柜体轮廓相邻'},
    {'id':'FH-2-01','floor':2,'handle':'2B5FE','point':(3414.31,3766),
     'label':(5300,4700),'elbow':(4050,4700),'rotation':0,
     'basis':'按原图防火栓文字锚点定位，未虚构柜体尺寸'},
]
VERIFY_DATA = {}

def new_doc():
    d = B.make_doc()
    for la,color in ACI.items():
        if la not in d.layers: d.layers.new(la)
        layer=d.layers.get(la)
        layer.dxf.discard('true_color')
        layer.dxf.color=color
        layer.dxf.lineweight=30 if la in ('原有结构','图框','常闭门') else 18
    d.layers.get('梯下投影').dxf.linetype='PLAN_DASH'
    return d

def dh(m,a,b,y,base):
    B.dh(m,a,b,y,base)
    # The dimension text is the last entity added by the shared helper.
    e=list(m)[-1];e.dxf.text=f'{abs(b-a):.0f} mm'

def dv(m,a,b,x,base):
    B.dv(m,a,b,x,base)
    e=list(m)[-1];e.dxf.text=f'{abs(b-a):.0f} mm'

def setup():
    B.OUT=OUT
    B.setup_layout()
    # Replace only the room zones and append the additional row; other validated
    # entrance, table, lift and door buffers are carried forward from V1.2.
    B.OBJS[1]=[(n,p) for n,p in B.OBJS[1] if n not in ('厨房','库房')]
    B.obj(1,'库房',(11150,800,14000,2600))
    B.obj(1,'厨房',(11150,2800,14000,8200))
    B.OBJS[2]=[(n,p) for n,p in B.OBJS[2] if n not in ('下包房','上包房')]
    B.obj(2,'下包房',ROOMS[0]);B.obj(2,'上包房',ROOMS[1])
    B.table(2,10300,8400,2);B.table(2,12500,8400,2)
    B.keep(1,'左上防火栓前',(460.94,19780,1710.94,21010))
    B.keep(2,'防火栓前',(3000,3560,4170,4560))

def original(d,m,src,f,demo=False):
    B.source_copy(d,m,src,f,demolition=demo)
    if f==1:
        # Remove the original open leaf and arc ONLY; the door itself is retained
        # below in the normally-closed position at the same opening.
        ox,oy=B.ORIGINS[1]
        original_arc=src.entitydb['2B6AA']
        centre=(original_arc.dxf.center.x-ox,original_arc.dxf.center.y-oy)
        for e in list(m):
            if e.dxftype()=='ARC' and math.dist(tuple(e.dxf.center)[:2],centre)<.1:
                m.delete_entity(e)
            elif e.dxftype()=='LINE':
                h=src.entitydb['2B6A8']
                a=(h.dxf.start.x-ox,h.dxf.start.y-oy);b=(h.dxf.end.x-ox,h.dxf.end.y-oy)
                if math.dist(tuple(e.dxf.start)[:2],a)<.1 and math.dist(tuple(e.dxf.end)[:2],b)<.1:
                    m.delete_entity(e)

def walls(m,f):
    if f==1:
        seg=[((11100,600),(11100,1500)),((11100,2500),(11100,7000)),
             ((11100,8000),(11100,8300)),((11100,2700),(14140,2700)),
             ((11100,8300),(13000,8300)),((13900,8300),(14140,8300))]
        B.slide(m,11100,1500);B.slide(m,11100,7000)
        # Kitchen to serving work area: real 900mm gap in the north partition.
        B.ln(m,(13000,8300),(13000,9200),'门')
        m.add_arc((13000,8300),900,0,90,dxfattribs={'layer':'门'})
    else:
        seg=[((10140,100),(10140,1400)),((10140,2400),(10140,4900)),
             ((10140,5900),(10140,7100)),((10140,3550),(14140,3550)),
             ((10140,7100),(14140,7100))]
        B.slide(m,10140,1400);B.slide(m,10140,4900);B.slide(m,1830,5500)
    for a,b in seg:
        B.wall(m,a,b);B.NEW_WALLS[f].append(LineString([a,b]).buffer(50,cap_style=2))

def tables(m,f):
    B.draw_tables(m,f)
    for t in B.TABLES[f]:
        x0,y0,x1,y1=t['table']
        B.txt(m,f"{600*t['pairs']}×600 mm / {2*t['pairs']}人",
              ((x0+x1)/2,(y0+y1)/2),95,'文字',rot=90 if t['vertical'] else 0)

def equipment(m,f):
    if f==1:
        items=[((13500,900,14000,2500),'货架'),
               ((11300,2900,11900,3900),'冷柜'),
               ((13000,3100,13950,4900),'双眼灶/排烟罩'),
               ((13000,5200,13950,6200),'蒸饭/主食'),
               ((11300,4100,11900,5700),'清洗/切配'),
               ((11300,5900,11900,6500),'洗消点'),
               ((12500,7300,13900,7900),'工作台')]
        for r,name in items:
            B.rect(m,r,'厨房设备')
            B.txt(m,name,((r[0]+r[2])/2,(r[1]+r[3])/2),115,'厨房设备')
        B.rect(m,(12000,9400,14000,10100),'打菜2人')
        B.ln(m,(13000,9400),(13000,10100),'打菜2人')
        B.txt(m,'师傅1',(12500,9750),160,'打菜2人')
        B.txt(m,'师傅2',(13500,9750),160,'打菜2人')
        B.rect(m,(7700,12200,8300,14000),'唯一回收点')
        B.txt(m,'全楼唯一餐具回收',(8000,13100),135,'唯一回收点',rot=90)
    else:
        for cx,cy in ROUND_CENTRES:
            m.add_circle((cx,cy),750,dxfattribs={'layer':'餐桌'})
            B.txt(m,'Φ1500 mm',(cx,cy),145)
            for i in range(8):
                a=math.pi*2*i/8;x=cx+1000*math.cos(a);y=cy+1000*math.sin(a)
                B.rect(m,(x-150,y-150,x+150,y+150),'凳子300')
        B.rect(m,(4300,10400,6700,10500),'屏幕')
        B.txt(m,'上方墙面显示屏 2400×1350 mm',(5500,10850),175,'屏幕')

def leader(m,points,label,location,layer,h=160,rot=0):
    for a,b in zip(points,points[1:]):B.ln(m,a,b,layer)
    m.add_circle(points[0],55,dxfattribs={'layer':layer})
    B.txt(m,label,location,h,layer,rot=rot)

def fire(m,f,src):
    for item in HYDRANTS:
        if item['floor']!=f:continue
        e=src.entitydb[item['handle']]
        assert '防火栓' in e.plain_text()
        leader(m,[item['point'],item['elbow']],item['id']+' 原防火栓',
               item['label'],'消防标识',155,item['rotation'])

def stairs(m,f):
    if f==1:
        # Original upper treads at y=18530..19530 are retained. Extend schematic
        # downward at 250mm pitch, with a break and dashed under-stair projection.
        for y in range(14280,18530,250):
            B.ln(m,(460.94,y),(1560.94,y),'梯下投影' if y<17400 else '楼梯踏步')
        cut=[(460.94,17300),(800,17500),(1200,17300),(1560.94,17500)]
        for a,b in zip(cut,cut[1:]): B.ln(m,a,b,'楼梯踏步')
        B.ln(m,(700,15800),(700,19000),'楼梯踏步')
        for x in (570,830):B.ln(m,(700,19000),(x,18750),'楼梯踏步')
        B.txt(m,'上二楼',(1100,17900),170,'楼梯踏步',rot=90)
        B.rect(m,(1530.94,14330,1590.94,14930),'常闭门')
        m.add_circle((1560.94,14930),35,dxfattribs={'layer':'常闭门'})
        leader(m,[(1560.94,14630),(2200,13450)],'梯下杂物间门：约600 mm，常闭',
               (3700,13450),'常闭门',170)
        B.txt(m,'250踏步示意；步高/数量/上下对位现场复核',(3850,13000),140,'楼梯踏步')
    else:
        B.txt(m,'一楼上行到达示意',(1400,6600),145,'楼梯踏步')
        B.txt(m,'梯段对位现场复核',(1400,6150),135,'楼梯踏步')

def toilet_symbols(m):
    # The original has no male/female room labels or fixture schedule. These are
    # explicitly annotation icons, NOT added fixtures or a verified inventory.
    B.txt(m,'男卫*',(1180,3200),185,'洁具标识_示意')
    B.txt(m,'女卫*',(3100,3200),185,'洁具标识_示意')
    for x in (1150,3100):
        B.rect(m,(x-170,1320,x+170,1870),'洁具标识_示意')
        m.add_ellipse((x,1595),major_axis=(0,190),ratio=110/190,
                      dxfattribs={'layer':'洁具标识_示意'})
        B.txt(m,'蹲位区',(x,2190),130,'洁具标识_示意')
    B.rect(m,(650,250,1050,650),'洁具标识_示意')
    m.add_arc((850,450),135,180,360,dxfattribs={'layer':'洁具标识_示意'})
    B.txt(m,'小便斗区*',(1350,750),120,'洁具标识_示意')
    B.txt(m,'*左男右女及洁具图符为示意；实际位置、数量现场确认',
          (2800,-350),145,'洁具标识_示意')
    B.txt(m,'原墙、原蹲位分隔线保留，图符不代表新增洁具',
          (2800,-650),135,'洁具标识_示意')

def clearances(m,f):
    for name,p in B.KEEP[f]:
        if name.startswith('原'):continue
        B.rect(m,p.bounds,'净空保留')
    if f==1:
        B.arrow(m,[(9600,700),(10150,3400),(10150,9500),(11050,12200),(10150,15800)])
        B.txt(m,'员工主入口 / 原门洞约1150 mm',(9600,-300),180)
        B.txt(m,'入口缓冲 / 不摆桌',(9650,2000),180)
        B.txt(m,'主通道1800 mm',(10150,7000),165,rot=90)
        B.txt(m,'传菜梯操作面1500 mm',(9400,11150),145)
        B.txt(m,'排队在右侧，不占主通道',(12900,12600),150)
        B.txt(m,'门前净空',(2650,19550),150);B.txt(m,'门前净空',(13150,19550),150)
    else:
        # Updated direction at the top of the aisle does not cross the new row.
        B.arrow(m,[(9300,3000),(9300,6500),(9300,9550),(7800,9550)])
        B.txt(m,'包房门前通道1440 mm',(9450,4300),160,rot=90)
        B.txt(m,'传菜梯操作/取送1800 mm',(7950,2300),150)
        B.txt(m,'观看 / 活动留空',(5500,9850),180)

def labels(m,f):
    if f==1:
        B.txt(m,'库房 约5.1㎡',(12300,1750),175,'厨房设备')
        B.txt(m,'厨房 约15.4㎡',(12600,6750),175,'厨房设备')
        B.txt(m,'2人打菜 / 2个工位',(12600,10600),175,'打菜2人')
        B.txt(m,'原有传菜梯',(8000,10880),150,'原有传菜梯')
        B.txt(m,'公共110座',(16900,21400),220)
    else:
        B.txt(m,'包房一 / 8人 / 约13.1㎡',(12140,3250),170)
        B.txt(m,'包房二 / 8人 / 约13.3㎡',(12140,6800),170)
        B.txt(m,'包房上方新增一排：2张四人桌，共8座',(12200,9750),155)
        B.txt(m,'公共60座 + 包房16座',(5500,11450),230)

def dimensions(m,f,with_tables=True):
    if f==1:
        dh(m,460.94,19840.94,21700,20930)
        dv(m,14030,20930,20800,19840.94)
        dv(m,600,14030,15150,14140.94)
        dh(m,7420.94,14180.94,-850,600)
        # Kitchen/store net design dimensions, moved with the spaces.
        dh(m,11150,14000,2700,2800)
        dv(m,2800,8200,14600,14000)
        dv(m,800,2600,14600,14000)
        dv(m,1500,2500,10850,11100)
        dv(m,7000,8000,10850,11100)
        dh(m,9250,11050,9000,8500)
        dh(m,12000,14000,10250,10100)
        dh(m,7420.94,8570.94,12050,11550)
        dh(m,460.94,1560.94,19900,19530)
        dv(m,19280,19530,1850,1560.94)
    else:
        dh(m,350,14140,11950,10500);dv(m,0,10500,16000,14140)
        dh(m,10140,14140,7600,7100)
        dv(m,100,3500,14800,14140);dv(m,3600,7050,14800,14140)
        dv(m,1400,2400,9850,10140);dv(m,4900,5900,9850,10140)
        dh(m,8700,10140,7300,7100)
        dv(m,1060,2860,9000,8440)
        dh(m,7440,8440,-900,0)
        dh(m,350,2130,-1050,0);dh(m,2250,4050,-1050,0)
    B.txt(m,'本图所有尺寸单位：mm；模型1:1，PDF适合页面打印',
          (10500 if f==1 else 7800,-1500),175)

def title(m,f,name):
    bounds=(-1800,-3300,22000,23500) if f==1 else (-1400,-3300,16900,12900)
    centre=10500 if f==1 else 7800
    B.rect(m,bounds,'图框')
    B.txt(m,name,(centre,23000 if f==1 else 12400),320)
    B.txt(m,'美莱食堂 V1.3 | 600mm桌深 / 300mm凳面 | 黑底高对比DWG',
          (centre,-2050),175)
    B.txt(m,'实线：结构及桌凳；长虚线：净空；楼梯踏步和洁具图符为标识示意',
          (centre,-2470),150)
    B.txt(m,'最小桌组人体包络净距800 mm；门前、消防与传菜梯操作面不摆桌',
          (centre,-2850),150)

def verify(src):
    errors=[];spacing=[]
    for f in (1,2):
        envelope=Polygon([(460.94,14030),(7420.94,14030),(7420.94,600),
                          (14180.94,600),(14140.94,14030),(19840.94,14030),
                          (19840.94,20930),(460.94,20930)]) if f==1 else box(350,0,14140,10500)
        for t in B.TABLES[f]:
            p=t['footprint']
            if not envelope.buffer(1).covers(p):errors.append(t['id']+' outside building')
            for name,q in B.KEEP[f]+B.OBJS[f]:
                if p.intersection(q).area>1:errors.append(t['id']+' overlaps '+name)
            for q in B.SOURCE_POLYS[f]+B.NEW_WALLS[f]:
                if p.intersection(q).area>1:errors.append(t['id']+' overlaps wall/column')
            for q in B.PRESERVED_LINES[f]:
                if p.buffer(-1).intersects(q):errors.append(t['id']+' overlaps original wall')
        dist=min(a['footprint'].distance(b['footprint']) for i,a in enumerate(B.TABLES[f]) for b in B.TABLES[f][i+1:])
        spacing.append({'floor':f,'minimum_occupied_envelope_spacing_mm':round(dist,1)})
        if dist<799:errors.append(f'{f}F table spacing {dist}')
        for name,p in B.OBJS[f]:
            for name2,q in B.KEEP[f]:
                if p.intersection(q).area>1:errors.append(name+' overlaps '+name2)
    opaque=[box(10140,0,14140,7100),box(350,0,4170,3560),
            box(350,3560,2500,7000),box(7440,0,8440,1060)]+B.SOURCE_POLYS[2]
    blocked=[]
    for t in B.TABLES[2]:
        for p in t['seats']:
            if any(LineString([p,(5500,10400)]).intersection(q).length>1 for q in opaque):
                blocked.append([t['id'],p])
    if blocked:errors.append('screen sightlines '+str(blocked))
    for centre,r in zip(ROUND_CENTRES,ROOMS):
        cx,cy=centre;occupied=box(cx-1250,cy-1250,cx+1250,cy+1250)
        if not box(*r).covers(occupied):errors.append('room stool/body envelope outside room')
        if cx-1250-r[0]<800:errors.append('private door-side aisle below 800')
    evidence=[]
    for h in HYDRANTS:
        e=src.entitydb[h['handle']]
        assert '防火栓' in e.plain_text()
        evidence.append(dict(h,source_text=e.plain_text(),source_insert=list(e.dxf.insert)))
    result={'failures':errors,'table_spacing':spacing,
            'public_seats':{str(f):sum(len(t['seats']) for t in B.TABLES[f]) for f in (1,2)},
            'private_seats':16,'screen_geometry_blocked':blocked,'hydrant_source_evidence':evidence,
            'private_net_areas_m2':[round(box(*r).area/1e6,2) for r in ROOMS],
            'kitchen_net_design_m2':15.39,'store_net_design_m2':5.13,
            'stair_treads':'250mm pitch schematic; count and riser height require field confirmation',
            'under_stair_door':'normally closed; original open arc removed; not used as public entrance',
            'toilet_icons':'Annotation only. Left male/right female and fixture location/quantity unconfirmed; original walls retained.'}
    (OUT/'几何校核.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    if errors:raise RuntimeError('\n'.join(errors))
    return result

def detail():
    d=new_doc();m=d.modelspace()
    for y in (0,2400):
        B.rect(m,(0,y,2400,y+600),'餐桌')
        for i in range(4):
            for cy in (y-250,y+850):B.rect(m,(150+600*i,cy-150,450+600*i,cy+150),'凳子300')
        B.rect(m,(-100,y-500,2500,y+1100),'净空保留')
    dh(m,0,2400,3650,3000);dv(m,0,600,2900,2400)
    dh(m,0,600,-1400,0);dh(m,150,450,-1000,-400)
    dv(m,1100,1900,3300,2500)
    B.txt(m,'2400×600 mm桌 / 4对8人 / 凳面300×300 mm',(2000,4400),190)
    B.txt(m,'人体余量外仍留800 mm净通道；主通道优先1800 mm',(2000,4100),160)
    B.rect(m,(-1800,-2600,6000,5200),'图框')
    B.txt(m,'V1.3 餐桌、凳面与通道尺寸详图',(2000,4800),230)
    B.txt(m,'所有尺寸单位：mm；模型1:1；PDF适合页面打印',(2000,-1900),165)
    return d

def reports(result,conversions,initial_hash):
    (OUT/'转换验证.json').write_text(json.dumps(conversions,ensure_ascii=False,indent=2),encoding='utf-8')
    with (OUT/'桌位统计.csv').open('w',encoding='utf-8-sig',newline='') as fh:
        w=csv.writer(fh);w.writerow(['楼层','桌号','桌长mm','桌深mm','座位','凳面mm'])
        for f in (1,2):
            for t in B.TABLES[f]:w.writerow([f,t['id'],600*t['pairs'],600,2*t['pairs'],300])
        for name in ('包房一','包房二'):w.writerow(['二层',name,1500,'圆桌',8,300])
    with (OUT/'防火栓原图定位.csv').open('w',encoding='utf-8-sig',newline='') as fh:
        w=csv.writer(fh);w.writerow(['编号','楼层','原图文字句柄','原图文字X','原图文字Y','图内标识X','图内标识Y','定位依据'])
        for h in result['hydrant_source_evidence']:
            w.writerow([h['id'],h['floor'],h['handle'],*h['source_insert'][:2],*h['point'],h['basis']])
    (OUT/'优化说明.md').write_text(f'''# 美莱食堂 V1.3 细化优化说明

## 本版调整
- DWG/DXF：结构、图框、文字采用ACI 7自适应白/黑，尺寸黄色，设备青色，桌凳绿色，消防红色；不再用近黑色RGB线条。无需改变CADCraft全局背景。
- PDF：另用白底深色打印配色，几何与DWG相同，不把黑底的黄色/青色原样输出到白纸。
- 一层楼梯补250mm节距踏步示意、折断线、上行箭头；梯下为虚线投影，原图已有踏步保留。踏步数量、步高、净高及两层对位待现场核实，示意不等于已完成楼梯结构设计。
- 一层左侧梯下杂物间门改画常闭，取消原常开门弧。门为原约600mm小门，不作为员工进出路线。
- 原图三处防火栓编号FH-1-01、FH-1-02、FH-2-01，附原标注句柄和原坐标表；第三处依原文字锚点定位，未凭空增加柜体。操作区避让桌凳。
- 所有平面设计图加总体、房间、通道、传菜梯等尺寸；公共桌面逐桌写长×600mm，尺寸详图补300mm凳面及800mm净通道。统一单位mm，模型1:1，PDF按页适配，不冒充1:100定比施工图。

## 厨房、库房位置对调
库房在右下方：2850×1800mm，约5.13㎡。厨房移到其上方、靠近打菜区：2850×5400mm，约15.39㎡。中间分隔移至y=2700mm，厨房上方增加900mm工作门连通打菜台后场；员工后门和公共通道保持不穿过厨房/库房。2人2工位、唯一一楼回收点保持。

## 二楼包房和新增座位
两间包房净面积约{result['private_net_areas_m2'][0]}㎡、{result['private_net_areas_m2'][1]}㎡，仍各8人、Φ1500mm圆桌。门前1440mm通道保留。包房顶边从y=8100mm下移到7100mm，上方增加两张1200×600mm四人桌，合计新增8座。

公共座位：一楼110座，二楼60座，合计170座；包房另16座。二楼新增桌组不占包房门前、传菜梯操作区或公共屏前区。桌组人体包络外最小间距两层均800mm，包房门侧通行余量800mm以上。

## 卫生间标识的依据
原有卫生间墙线、蹲位分隔线和原始块保留。新增的蹲位/男卫小便斗符号置于独立“洁具标识_示意”层，仅用于识别，不代表增加洁具或确认数量。

**原图没有男女文字分配、小便斗定位和洁具表。**本版暂按左男右女标识，并在图内带星号注明现场核对。小便斗示意放在左间下部，实际位置和数量需业主/现场确认；没有把示意说成从原DWG读出的实测设施。

## 显示和使用
优先在CADCraft打开本目录DWG；黑底检视图在`预览图/*_黑底CADCraft.png`。PDF及普通PNG为白底配色。打印源DXF单独存于`DXF/打印源`，主要编辑源为`DXF`目录同名文件。

## 校核与限制
- 几何检测覆盖桌凳人体包络、墙柱、通道、包房门前、消防及传菜梯操作区。
- 所有60个二楼公共座位到屏幕中心的平面视线已检测，不穿过墙柱/房间；人员临时遮挡、立面角度仍需现场调试。
- 9套DWG均重新读取并对比实体数、跳过数；不能据此代替消防、结构、机电、厨房工艺复核。
- 仍固定2人打菜；600人60分钟没有由本次加8座自动获得保证。已按170个公共座位重算假设运营场景，见供餐分析。
- 原DWG未改动，SHA256：`{initial_hash}`。
''',encoding='utf-8')
    (B.ROOT/'deliverables'/'README.md').write_text('''# 当前方案入口

**当前最新：V1.3 配色、尺寸及布局细化版。**

- [一楼白底预览](V1.3/预览图/一楼功能分区与家具布置图.png)
- [二楼白底预览](V1.3/预览图/二楼功能分区与家具布置图.png)
- [一楼黑底CADCraft检视](V1.3/预览图/一楼功能分区与家具布置图_黑底CADCraft.png)
- [二楼黑底CADCraft检视](V1.3/预览图/二楼功能分区与家具布置图_黑底CADCraft.png)
- [V1.3说明](V1.3/优化说明.md)

厨房库房对调、常闭杂物门、楼梯踏步、防火栓和卫生间标识已补充；二层包房压缩后上方增加8座。
V1.1/V1.2保留为历史，当前图纸以V1.3目录为准。
''',encoding='utf-8')

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for p in (OUT/'DXF',OUT/'DXF'/'打印源',OUT/'预览图'):p.mkdir(exist_ok=True)
    initial_hash=hashlib.sha256(B.SOURCE.read_bytes()).hexdigest()
    raw=OUT/'DXF'/'原始基准_只读转换.dxf'
    subprocess.run([str(B.CLI),'convert',str(B.SOURCE),str(raw)],check=True,capture_output=True)
    src=ezdxf.readfile(raw);setup()
    specs=[(1,'一楼原始结构及拆改平面图','demo'),(1,'一楼功能分区与家具布置图','furn'),
           (1,'一楼厨房及打菜设备布置图','equip'),(1,'一楼尺寸标注平面图','dim'),
           (2,'二楼原始结构及拆改平面图','demo'),(2,'二楼功能分区与家具布置图','furn'),
           (2,'二楼尺寸标注平面图','dim')]
    docs={}
    for f,name,mode in specs:
        d=new_doc();m=d.modelspace();original(d,m,src,f,mode=='demo');walls(m,f)
        if mode in ('furn','dim'):tables(m,f)
        if mode!='demo':equipment(m,f)
        clearances(m,f);labels(m,f);stairs(m,f);fire(m,f,src)
        if f==2:toilet_symbols(m)
        dimensions(m,f,mode in ('furn','dim'));title(m,f,name)
        docs[name]=d
    verify(src)
    combo=new_doc();cm=combo.modelspace()
    for f,name in [(1,'一楼功能分区与家具布置图'),(2,'二楼功能分区与家具布置图')]:
        before=set(e.dxf.handle for e in cm);imp=Importer(docs[name],combo)
        imp.import_entities([e for e in docs[name].modelspace() if e.dxf.layer!='图框'],target_layout=cm);imp.finalize()
        if f==2:
            for e in cm:
                if e.dxf.handle not in before:e.transform(Matrix44.translate(24000,0,0))
    B.rect(cm,(-1800,-3300,41300,24000),'图框')
    B.txt(cm,'美莱食堂 V1.3 一二层综合设计图',(19000,23650),330)
    B.txt(cm,'本图尺寸单位mm；模型1:1；黑底高对比DWG / 白底配色PDF',(19500,-3050),185)
    docs['一二楼综合设计图']=combo
    docs['餐桌600与凳面300及通道详图']=detail()
    conversions=[]
    for name,d in docs.items():
        dx=OUT/'DXF'/f'{name}.dxf';d.saveas(dx)
        dwg=OUT/f'{name}.dwg'
        subprocess.run([str(B.CLI),'convert',str(dx),str(dwg)],check=True,capture_output=True)
        info=json.loads(subprocess.run([str(B.CLI),'info',str(dwg)],check=True,capture_output=True,
                                       text=True,encoding='utf-8').stdout)
        assert info['entityCount']==len(d.modelspace()),name
        assert info.get('skipped',{}).get('count',0)==0,name
        printable=ezdxf.readfile(dx)
        for layer in printable.layers:
            if layer.dxf.name in PRINT_RGB:layer.rgb=PRINT_RGB[layer.dxf.name]
        px=OUT/'DXF'/'打印源'/f'{name}.dxf';printable.saveas(px)
        subprocess.run([str(B.CLI),'convert',str(px),str(OUT/f'{name}.pdf')],check=True,capture_output=True)
        conversions.append({'file':dwg.name,'entities':info['entityCount'],'skipped':info.get('skipped'),
                            'DWG_palette':'ACI adaptive/dark','PDF_palette':'separate white-background true colour'})
        if name in ('一楼功能分区与家具布置图','二楼功能分区与家具布置图','一二楼综合设计图','餐桌600与凳面300及通道详图'):
            with pymupdf.open(OUT/f'{name}.pdf') as pdf:
                pdf[0].get_pixmap(dpi=200).save(OUT/'预览图'/f'{name}.png')
        if name in ('一楼功能分区与家具布置图','二楼功能分区与家具布置图'):
            subprocess.run([str(B.CLI),'convert',str(dwg),str(OUT/'预览图'/f'{name}_黑底CADCraft.png')],
                           check=True,capture_output=True)
    result=verify(src)
    B.simulation()
    sim=OUT/'两人供餐敏感性分析.md'
    sim.write_text(sim.read_text(encoding='utf-8').replace('V1.2','V1.3'),encoding='utf-8')
    reports(result,conversions,initial_hash)
    assert hashlib.sha256(B.SOURCE.read_bytes()).hexdigest()==initial_hash
    print(json.dumps({'output':str(OUT),'public_seats':result['public_seats'],
                      'private_areas_m2':result['private_net_areas_m2'],
                      'DWGs':len(conversions),'failures':result['failures']},ensure_ascii=False))

if __name__=='__main__':main()
