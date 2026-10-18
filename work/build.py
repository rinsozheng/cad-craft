import os, math, json
import ezdxf
from design_lib import *

SRC = r"D:\code\github\cad-craft\work\original.dxf"
OUT = r"D:\code\github\cad-craft\work\sheets"
os.makedirs(OUT, exist_ok=True)
src = ezdxf.readfile(SRC)
src_msp = src.modelspace()

# ================= 1F =================
def walls_1f(msp, scheme='A'):
    # ---- new partitions in lower wing ----
    # entry hall / dry store / waste room, y 600..2620
    # dry store
    double_wall(msp, 12100, 600, 12100, 2620)
    double_wall(msp, 12100, 2620, 12800, 2620)
    double_wall(msp, 13700, 2620, 14180, 2620)
    door(msp, 12800, 2620, 900, 0)          # dry store door
    # waste room
    double_wall(msp, 10170, 600, 10170, 2620)
    double_wall(msp, 10170, 2620, 10800, 2620)
    double_wall(msp, 11700, 2620, 12100, 2620)
    door(msp, 10800, 2620, 900, 0)
    # cold room
    double_wall(msp, 10000, 2620, 10000, 4800)
    double_wall(msp, 7420, 4800, 8000, 4800)
    double_wall(msp, 8900, 4800, 10000, 4800)
    door(msp, 8000, 4800, 900, 0)
    # dishwash room (rebuilt)
    double_wall(msp, 11770, 3760, 11770, 7000)
    double_wall(msp, 11770, 3760, 13180, 3760)
    double_wall(msp, 11770, 7000, 12350, 7000)
    double_wall(msp, 12650, 7000, 13180, 7000)
    door(msp, 12350, 7000, 900, 0)
    # corridor east wall: x 13180 from y 2620 to 14030 (door to kitchen at two points)
    for a, b in [(2620, 3500), (4400, 9000), (9900, 14030)]:
        double_wall(msp, 13180, a, 13180, b)
    door(msp, 13180, 3500, 900, 90)
    door(msp, 13180, 9000, 900, 90)
    # mop closet (existing small room retained) - add door
    door(msp, 8570, 10890, 800, 0)
    # serving counter (1.2 m deep) at the hall edge, 5 stations
    # drawn in furniture, not wall

def demo_1f(msp):
    # bottom-room partitions to remove
    for (x0, y0, x1, y1) in [
        (7420, 2620, 8422, 2730), (8530, 2620, 14180, 2730),
        (8422, 600, 8434, 2620),
        (11770, 3760, 11880, 5850), (11770, 5850, 14180, 5970),
    ]:
        line(msp, (x0, y0), (x1, y1), 'A-WALL-DEMO')
        if abs(x1 - x0) + abs(y1 - y0) < 2500:
            line(msp, (x0, y1), (x1, y0), 'A-WALL-DEMO')
    text(msp, '拆', 12500, 2670, 200, 'A-WALL-DEMO', 'center')
    text(msp, '拆', 8000, 2670, 200, 'A-WALL-DEMO', 'center')
    text(msp, '拆', 12000, 3900, 200, 'A-WALL-DEMO', 'center')

def furn_1f(msp, scheme='A', tables=True):
    # tables: scheme A = 8-seat long + 4-seat; scheme B = 6-seat + 4-seat
    if tables and scheme == 'A':
        # north row 5 long tables
        for i in range(5):
            table_long(msp, 1800 + i * 3600, 18600, 2400, 800, 4)
        # west zone: 2 rows x (long + 4-seat)
        for yy in (14600, 16500):
            table_long(msp, 1800, yy, 2400, 800, 4)
            table_4(msp, 5800, yy, 1400, 800)
        # east zone
        for yy in (14600, 16500):
            table_long(msp, 14400, yy, 2400, 800, 4)
            table_4(msp, 17000, yy, 1400, 800)
            table_2(msp, 18500, yy + 50, 800, 700)
        # tray return at east wall
        rect(msp, 19300, 14200, 19820, 16600, 'A-SERVING')
        text(msp, '餐具回收', 19560, 15400, 160, 'A-SERVING', 'center', rot=90)
    elif tables:
        for i in range(5):
            table_6(msp, 1800 + i * 3000, 18600, 1800, 800)
        for yy in (14600, 16500):
            table_6(msp, 1800, yy, 1800, 800)
            table_4(msp, 5000, yy, 1400, 800)
            table_6(msp, 14400, yy, 1800, 800)
            table_4(msp, 16800, yy, 1400, 800)
        # north window counters
        bar(msp, 4600, 20400, 8000, 20700, 6, 'S')
        bar(msp, 15000, 20400, 19000, 20700, 8, 'S')
    # serving counter and queue
    rect(msp, 7600, 14030, 13180, 15230, 'A-SERVING')
    for i in range(5):
        x = 7600 + i * 1116
        rect(msp, x + 40, 14100, x + 1076, 15160, 'A-SERVING')
        circle(msp, (x + 558, 14630), 180, 'A-SERVING')
        text(msp, f'工位{i+1}', x + 558, 14850, 160, 'A-SERVING', 'center')
    # kitchen equipment
    equip_rect(msp, 7520, 6200, 8720, 8200, '灶台 4锅', 'A-KITCHEN', 160)
    equip_rect(msp, 7520, 8400, 8720, 10400, '灶台 4锅', 'A-KITCHEN', 160)
    equip_rect(msp, 7520, 10600, 8720, 11600, '蒸饭柜', 'A-KITCHEN', 150)
    equip_rect(msp, 7520, 11800, 8720, 12800, '蒸饭柜', 'A-KITCHEN', 150)
    # hood dashed
    rect(msp, 7420, 6000, 8820, 12900, 'A-KITCHEN')
    text(msp, '排烟罩', 8120, 5900, 180, 'A-KITCHEN', 'center')
    # prep / wash
    for yy in (7200, 8600):
        equip_rect(msp, 11200, yy, 12900, yy + 1000, '操作台', 'A-KITCHEN', 150)
    for yy in (9800, 11000):
        equip_rect(msp, 11770, yy, 12900, yy + 800, '水池', 'A-KITCHEN', 150)
    equip_rect(msp, 10600, 6200, 11600, 7200, '冰箱', 'A-KITCHEN', 150)
    equip_rect(msp, 10600, 7400, 11600, 8400, '冰箱', 'A-KITCHEN', 150)
    # cold room shelves
    equip_rect(msp, 7480, 2700, 7900, 4700, '冷藏', 'A-KITCHEN', 160)
    equip_rect(msp, 8000, 2700, 8400, 4700, '冷冻', 'A-KITCHEN', 160)
    equip_rect(msp, 8500, 2700, 9900, 3000, '货架', 'A-KITCHEN', 140)
    # dry store shelves
    for yy in (900, 1900):
        equip_rect(msp, 12180, yy, 14080, yy + 500, '货架', 'A-KITCHEN', 140)
    # waste room
    equip_rect(msp, 10300, 800, 10800, 1300, '垃圾桶', 'A-KITCHEN', 140)
    equip_rect(msp, 11000, 800, 11500, 1300, '垃圾桶', 'A-KITCHEN', 140)
    text(msp, '垃圾/回收', 11135, 2000, 170, 'A-KITCHEN', 'center')
    # dishwash
    equip_rect(msp, 11900, 4000, 13050, 4800, '洗碗机', 'A-KITCHEN', 150)
    equip_rect(msp, 11900, 5100, 13050, 5700, '预洗池', 'A-KITCHEN', 150)
    equip_rect(msp, 11900, 5900, 13050, 6800, '保洁柜', 'A-KITCHEN', 150)
    # plating / pass
    equip_rect(msp, 7600, 12300, 13100, 13200, '成品保温/备餐', 'A-KITCHEN', 170)
    equip_rect(msp, 7600, 13400, 13100, 13900, '出餐传递台', 'A-KITCHEN', 170)
    # paths
    arrow(msp, [(9600, 1000), (9600, 2500), (10800, 2500), (13500, 2500), (13500, 13500), (13500, 16000)], 'A-PATH')
    arrow(msp, [(10000, 18000), (10000, 17000)], 'A-PATH')

def labels_1f(msp, scheme='A'):
    label_room(msp, '厨房', 52.0, 9800, 9000)
    label_room(msp, '库房', 4.1, 13150, 1600)
    label_room(msp, '垃圾/回收', 3.9, 11135, 1600)
    label_room(msp, '冷藏/冷冻', 5.6, 8700, 3700)
    text(msp, '洗碗间 4.6 m2', 12475, 7250, 190, 'A-KITCHEN', 'center')
    label_room(msp, '入口/收货', 5.5, 8800, 1600)
    label_seats(msp, '公共就餐区', 92 if scheme == 'A' else 84, 100, 10300, 20200)
    text(msp, '打菜区（5工位）', 10390, 15450, 220, 'A-SERVING', 'center')
    text(msp, '排队区', 10390, 16000, 220, 'A-TEXT', 'center')
    text(msp, '员工入口', 9600, -150, 220, 'A-TEXT', 'center')
    text(msp, '主入口（双开门）', 9600, -500, 190, 'A-NOTE', 'center')
    text(msp, '至二层', 1000, 17500, 260, 'A-TEXT', 'center')
    text(msp, '楼梯', 1000, 16000, 240, 'A-TEXT', 'center')
    text(msp, '一层平面图', 10000, 22500, 500, 'A-TEXT', 'center')
    text(msp, '尺寸单位：mm  比例：1:100', 10000, 21400, 220, 'A-NOTE', 'center')
    north_arrow(msp, 19000, 22600)

def dims_1f(msp):
    dim_h(msp, 460, 19840, 22000, 20930, '19380', 'A-DIM')
    dim_v(msp, 14030, 20930, 21100, 19840, '6900', 'A-DIM')
    dim_v(msp, 600, 14030, 15100, 14180, '13430', 'A-DIM')
    dim_h(msp, 7420, 14180, 350, 600, '6760', 'A-DIM')
    dim_h(msp, 7420, 12900, 5200, 4800, '5480', 'A-DIM')
    dim_v(msp, 2620, 4800, 10100, 10000, '2180', 'A-DIM')
    dim_h(msp, 12100, 14180, 3000, 2620, '2080', 'A-DIM')
    text(msp, '主要尺寸（mm）', 10500, -2200, 300, 'A-DIM', 'center')

# ================= 2F =================
def walls_2f(msp, scheme='A'):
    # new doors in existing walls (symbols)
    sliding_door(msp, 10640, 8200, 900, True)   # room A sliding door
    sliding_door(msp, 10640, 4800, 900, True)   # room B sliding door
    sliding_door(msp, 10640, 1600, 900, True)   # pantry sliding door
    sliding_door(msp, 12200, 3560, 900, False)  # pantry to room B sliding door
    sliding_door(msp, 1730, 5600, 900, True)   # stair opening
    # toilet doors
    door(msp, 103124 - 101794.44, 12820 - 10680.03, 900, 0)
    door(msp, 104844 - 101794.44, 12820 - 10680.03, 900, 0)
    # screen wall
    rect(msp, SCREEN_X0, SCREEN_Y0, SCREEN_X1, SCREEN_Y1, 'A-WALL-NEW')
    rect(msp, 5800, SCREEN_Y0 + 40, 8200, SCREEN_Y1 - 40, 'A-SCREEN')
    text(msp, 'LED屏 2400x1350', 7000, 3160, 180, 'A-SCREEN', 'center')

def furn_2f(msp, scheme='A'):
    # service pantry equipment
    rect(msp, 13600, 800, 14100, 2800, 'A-SERVING')
    rect(msp, 13650, 900, 14050, 1500, 'A-SERVING')
    circle(msp, (13850, 1200), 90, 'A-SERVING')
    text(msp, '备餐/服务台', 13850, 2400, 150, 'A-SERVING', 'center')
    rect(msp, 10800, 600, 11600, 1200, 'A-KITCHEN')
    text(msp, '保温柜', 11200, 900, 140, 'A-KITCHEN', 'center')
    rect(msp, 11800, 600, 12600, 1200, 'A-KITCHEN')
    text(msp, '冰箱', 12200, 900, 140, 'A-KITCHEN', 'center')
    # tray return cart near stair
    rect(msp, 1850, 5000, 3050, 5600, 'A-SERVING')
    text(msp, '餐具回收车', 2450, 5300, 150, 'A-SERVING', 'center')
    if scheme == 'A':
        # main hall 3 rows x (2 long + 1 two)
        for yy in (4000, 6100, 8200):
            table_long(msp, 1900, yy, 2400, 800, 4)
            table_long(msp, 5700, yy, 2400, 800, 4)
            table_2(msp, 9500, yy + 50, 800, 700)
        # lower strip: long + six + two
        table_long(msp, 4400, 900, 2400, 800, 4)
        table_6(msp, 8000, 900, 1800, 800)
        table_2(msp, 9800, 950, 800, 700)
        # north window counter
        bar(msp, 5500, 10150, 9500, 10450, 10, 'S')
    else:
        # main hall 3 rows x (3 four-seat + 2 two-seat)
        for yy in (4000, 6100, 8200):
            table_4(msp, 1900, yy, 1400, 800)
            table_4(msp, 4700, yy, 1400, 800)
            table_4(msp, 7500, yy, 1400, 800)
            table_2(msp, 9300, yy + 50, 800, 700)
            table_2(msp, 10100, yy + 50, 800, 700)
        # lower strip: 2 six + 2 four
        table_6(msp, 4400, 900, 1800, 800)
        table_6(msp, 6600, 900, 1800, 800)
        table_4(msp, 8800, 900, 1400, 800)
        table_4(msp, 10000, 900, 1400, 800)
        # north counter 8
        bar(msp, 5500, 10150, 8500, 10450, 8, 'S')
    # private rooms
    round_table(msp, 12390, 8700, 1600, 10)
    round_table(msp, 12390, 5250, 1600, 10)
    # toilets fixtures
    # male: 2 WC + 2 urinals, x 350..1920 y 0..2020
    for i, xx in enumerate([550, 1250]):
        rect(msp, xx, 1300, xx + 500, 2000, 'A-FIXTURE')
        text(msp, 'WC', xx + 250, 1650, 140, 'A-FIXTURE', 'center')
    for xx in [500, 1000]:
        rect(msp, xx, 350, xx + 350, 650, 'A-FIXTURE')
        text(msp, '小便', xx + 175, 500, 110, 'A-FIXTURE', 'center')
    # female: 3 WC x 2250..4170
    for xx in [2400, 3050, 3700]:
        rect(msp, xx, 1100, xx + 450, 2000, 'A-FIXTURE')
        text(msp, 'WC', xx + 225, 1550, 130, 'A-FIXTURE', 'center')
    # sinks in lobby
    for xx in [600, 2400]:
        rect(msp, xx, 2500, xx + 600, 3000, 'A-FIXTURE')
        circle(msp, (xx + 300, 2750), 80, 'A-FIXTURE')

    # paths
    arrow(msp, [(1300, 6300), (2600, 6300), (4300, 6300), (4300, 5000)], 'A-PATH')
    arrow(msp, [(9800, 4000), (12000, 4000), (12000, 5000)], 'A-PATH')

def labels_2f(msp, scheme='A'):
    label_seats(msp, '公共就餐区', 80 if scheme == 'A' else 76, 84, 3000, 10050)
    text(msp, '包房1（8-10人） 12.5㎡', 12390, 10200, 175, 'A-AREA', 'center')
    text(msp, '包房2（8-10人） 11.8㎡', 12390, 6650, 175, 'A-AREA', 'center')
    label_room(msp, '备餐/服务间', 12.5, 12000, 2200)
    text(msp, '楼梯', 1040, 6300, 200, 'A-TEXT', 'center')
    text(msp, '至一层', 1040, 6000, 180, 'A-NOTE', 'center')
    text(msp, '显示屏', 7000, 2750, 220, 'A-SCREEN', 'center')
    text(msp, '男卫', 1000, 3200, 180, 'A-AREA', 'center')
    text(msp, '女卫', 3300, 3200, 180, 'A-AREA', 'center')
    text(msp, '二层平面图', 7200, 11650, 500, 'A-TEXT', 'center')
    text(msp, '尺寸单位：mm  比例：1:100', 7200, 10950, 220, 'A-NOTE', 'center')
    north_arrow(msp, 15000, 11700)

def dims_2f(msp):
    dim_h(msp, 350, 14140, -900, 0, '13790', 'A-DIM')
    dim_v(msp, 0, 10500, 15700, 14140, '10500', 'A-DIM')
    dim_h(msp, 350, 4170, -1800, 0, '3820', 'A-DIM')
    dim_v(msp, 0, 3440, 4700, 4170, '3440', 'A-DIM')
    dim_h(msp, 10640, 14140, 10650, 10500, '3500', 'A-DIM')
    dim_v(msp, 3560, 10500, 14700, 14140, '6940', 'A-DIM')
    dim_h(msp, 5500, 8500, 3700, 3440, '3000', 'A-DIM')
    text(msp, '主要尺寸（mm）', 9000, -2200, 300, 'A-DIM', 'center')

# ================= sheets =================
def base_1f(doc):
    msp = doc.modelspace()
    copy_original(msp, src_msp, O1, '1F')
    walls_1f(msp)
    return msp

def base_2f(doc):
    msp = doc.modelspace()
    copy_original(msp, src_msp, O2, '2F')
    walls_2f(msp)
    return msp

def save(doc, name):
    p = os.path.join(OUT, name + '.dxf')
    doc.saveas(p)
    print('saved', p)
    return p

def sheet_1f(name, mode, scheme='A'):
    doc = new_doc(); msp = base_1f(doc)
    if mode == 'demo':
        demo_1f(msp); labels_1f(msp, scheme)
    elif mode == 'furn':
        furn_1f(msp, scheme); labels_1f(msp, scheme)
    elif mode == 'kitchen':
        furn_1f(msp, scheme, tables=False); labels_1f(msp, scheme)
        # hide furniture? kitchen sheet still shows tables lightly; acceptable
    elif mode == 'dims':
        labels_1f(msp, scheme); dims_1f(msp)
    sheet_frame(msp, -2500, -3500, 22300, 23700, '美莱食堂改造', '一层平面图', name, '1:100')
    legend(msp, -2200, -3300)
    save(doc, name)

def sheet_2f(name, mode, scheme='A'):
    doc = new_doc(); msp = base_2f(doc)
    if mode == 'demo':
        labels_2f(msp, scheme)
        text(msp, '二层无墙体拆除；仅新增包房门洞、屏墙及服务间门洞', 7000, 9000, 220, 'A-NOTE', 'center')
    elif mode == 'furn':
        furn_2f(msp, scheme); labels_2f(msp, scheme)
    elif mode == 'dims':
        labels_2f(msp, scheme); dims_2f(msp)
    sheet_frame(msp, -2500, -3500, 20000, 12500, '美莱食堂改造', '二层平面图', name, '1:100')
    legend(msp, -2200, -3300)
    save(doc, name)

def combined(name, scheme='A'):
    doc = new_doc(); msp = doc.modelspace()
    # 1F at 0,0
    copy_original(msp, src_msp, O1, '1F')
    walls_1f(msp); furn_1f(msp, scheme); labels_1f(msp, scheme)
    # 2F shifted
    dx, dy = 23000, 0
    # draw 2F into a temporary doc then copy entities
    tmp = new_doc(); tmsp = tmp.modelspace()
    copy_original(tmsp, src_msp, O2, '2F')
    walls_2f(tmsp); furn_2f(tmsp, scheme); labels_2f(tmsp, scheme)
    for e in tmsp:
        c = e.copy()
        # translate
        if e.dxftype() == 'LINE':
            c.dxf.start = (e.dxf.start.x + dx, e.dxf.start.y + dy, 0)
            c.dxf.end = (e.dxf.end.x + dx, e.dxf.end.y + dy, 0)
        elif e.dxftype() == 'LWPOLYLINE':
            c.set_points([(p[0] + dx, p[1] + dy) for p in e.get_points()], format='xy')
        elif e.dxftype() == 'CIRCLE':
            c.dxf.center = (e.dxf.center.x + dx, e.dxf.center.y + dy, 0)
        elif e.dxftype() == 'ARC':
            c.dxf.center = (e.dxf.center.x + dx, e.dxf.center.y + dy, 0)
        elif e.dxftype() == 'TEXT':
            c.dxf.insert = (e.dxf.insert.x + dx, e.dxf.insert.y + dy, 0)
            if c.dxf.hasattr('align_point'):
                ap = c.dxf.align_point
                c.dxf.align_point = (ap.x + dx, ap.y + dy, 0)
        msp.add_entity(c)
    # 2F labels shifted? handled by entity copy
    text(msp, '二层', 23000 + 7200, 11400, 600, 'A-TEXT', 'center')
    sheet_frame(msp, -2500, -3500, 42000, 23700, '美莱食堂改造', '一、二层综合设计图', name, '1:100')
    legend(msp, -2200, -3300)
    save(doc, name)

if __name__ == '__main__':
    sheet_1f('1F_A_furn', 'furn', 'A')
    sheet_1f('1F_A_kitchen', 'kitchen', 'A')
    sheet_1f('1F_A_demo', 'demo', 'A')
    sheet_1f('1F_A_dims', 'dims', 'A')
    sheet_2f('2F_A_furn', 'furn', 'A')
    sheet_2f('2F_A_demo', 'demo', 'A')
    sheet_2f('2F_A_dims', 'dims', 'A')
    combined('COMBINED_A', 'A')
    sheet_1f('1F_B_furn', 'furn', 'B')
    sheet_2f('2F_B_furn', 'furn', 'B')
    combined('COMBINED_B', 'B')
