import math
import ezdxf
from ezdxf.enums import TextEntityAlignment

# ---------- constants (local coordinates, mm) ----------
O1 = (73959.58264270716, 1014.8090422358064)
O2 = (101794.44121770863, 10680.028566825611)

# 1F
HALL_X0, HALL_X1 = 460.94, 19840.94
HALL_Y0, HALL_Y1 = 14030.00, 20930.00
LOW_X0, LOW_X1 = 7420.94, 14180.94
LOW_Y0, LOW_Y1 = 600.00, 14030.00
STAIR_X0, STAIR_X1 = 460.94, 1560.94
STAIR_Y0, STAIR_Y1 = 14030.00, 19530.00
ENTRY_X0, ENTRY_X1 = 9020.94, 10170.94

# 2F
W2_X0, W2_X1 = 350.00, 14140.00
W2_Y0, W2_Y1 = 0.00, 10500.00
TOI_X1, TOI_Y1 = 4170.00, 3440.00
PRIV_X = 10640.00
PRIV_Y0 = 3560.00
PRIV_MID = 6937.90
ST2_X0, ST2_X1 = 350.00, 1730.00
ST2_Y0, ST2_Y1 = 4860.00, 7000.00
SCREEN_X0, SCREEN_X1 = 5500.00, 8500.00
SCREEN_Y0, SCREEN_Y1 = 3240.00, 3440.00

LAYERS = {
    'A-WALL-EXIST': (7, 35, 'Continuous'),
    'A-WALL-DEMO': (1, 25, 'DASHED'),
    'A-WALL-NEW': (30, 25, 'Continuous'),
    'A-COLUMN': (7, 35, 'Continuous'),
    'A-DOOR': (3, 18, 'Continuous'),
    'A-WINDOW': (4, 18, 'Continuous'),
    'A-STAIR': (7, 18, 'Continuous'),
    'A-FURN': (3, 18, 'Continuous'),
    'A-FURN-DETAIL': (3, 13, 'Continuous'),
    'A-KITCHEN': (5, 25, 'Continuous'),
    'A-SERVING': (30, 25, 'Continuous'),
    'A-FIXTURE': (5, 18, 'Continuous'),
    'A-DIM': (1, 13, 'Continuous'),
    'A-TEXT': (7, 18, 'Continuous'),
    'A-AREA': (5, 18, 'Continuous'),
    'A-PATH': (6, 18, 'DASHED'),
    'A-SCREEN': (5, 25, 'Continuous'),
    'A-HATCH': (8, 9, 'Continuous'),
    'A-TITLE': (7, 18, 'Continuous'),
    'A-GRID': (8, 9, 'Continuous'),
    'A-NOTE': (7, 13, 'Continuous'),
    'A-GREEN': (3, 13, 'Continuous'),
}


def new_doc():
    doc = ezdxf.new('R2018', setup=True)
    doc.styles.add('CN', font='simhei.ttf')
    for name, (color, lw, lt) in LAYERS.items():
        lay = doc.layers.add(name, color=color, linetype=lt)
        lay.dxf.lineweight = lw
    doc.header['$INSUNITS'] = 4  # mm
    doc.header['$MEASUREMENT'] = 1
    return doc


def line(msp, p1, p2, layer='A-WALL-EXIST', **kw):
    return msp.add_line(p1, p2, dxfattribs={'layer': layer, **kw})


def poly(msp, pts, layer='A-WALL-EXIST', closed=False, **kw):
    return msp.add_lwpolyline(pts, close=closed, dxfattribs={'layer': layer, **kw})


def rect(msp, x0, y0, x1, y1, layer='A-WALL-EXIST'):
    return poly(msp, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], layer, closed=True)


def circle(msp, c, r, layer='A-FURN'):
    return msp.add_circle(c, r, dxfattribs={'layer': layer})


def arc(msp, c, r, a0, a1, layer='A-DOOR'):
    return msp.add_arc(c, r, a0, a1, dxfattribs={'layer': layer})


def text(msp, s, x, y, h=250, layer='A-TEXT', align='left', rot=0, width=0):
    t = msp.add_text(s, height=h, dxfattribs={'style': 'CN', 'layer': layer, 'rotation': rot})
    t.set_placement((x, y), align={
        'left': TextEntityAlignment.LEFT,
        'center': TextEntityAlignment.CENTER,
        'right': TextEntityAlignment.RIGHT,
        'middle': TextEntityAlignment.MIDDLE_CENTER,
    }.get(align, TextEntityAlignment.LEFT))
    return t


def mtext(msp, s, x, y, h=220, layer='A-NOTE', width=6000):
    return msp.add_mtext(s, dxfattribs={'style': 'CN', 'layer': layer, 'char_height': h, 'width': width}).set_location((x, y))


def double_wall(msp, x0, y0, x1, y1, t=100, layer='A-WALL-NEW'):
    """Axis wall from (x0,y0) to (x1,y1) with thickness t."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    if L == 0:
        return
    nx, ny = -dy / L * t / 2, dx / L * t / 2
    line(msp, (x0 + nx, y0 + ny), (x1 + nx, y1 + ny), layer)
    line(msp, (x0 - nx, y0 - ny), (x1 - nx, y1 - ny), layer)
    line(msp, (x0 + nx, y0 + ny), (x0 - nx, y0 - ny), layer)
    line(msp, (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), layer)


def wall_rect(msp, x0, y0, x1, y1, t=100, layer='A-WALL-NEW'):
    """Rectangular room wall band drawn as two closed rectangles."""
    rect(msp, x0, y0, x1, y1, layer)
    rect(msp, x0 + t, y0 + t, x1 - t, y1 - t, layer)


def door(msp, x, y, w=900, rot=0, layer='A-DOOR'):
    """Simple door: leaf line + 90 deg swing arc. rot degrees."""
    a = math.radians(rot)
    # hinge at (x,y), leaf along local +x
    ex, ey = x + w * math.cos(a), y + w * math.sin(a)
    line(msp, (x, y), (ex, ey), layer)
    msp.add_arc((x, y), w, rot, rot + 90, dxfattribs={'layer': layer})
    # jamb ticks
    line(msp, (x - 50, y - 50), (x + 50, y + 50), layer)


def dim_h(msp, x1, x2, y, y0, text_s=None, layer='A-DIM', h=180):
    line(msp, (x1, y0 + 50), (x1, y - 120), layer)
    line(msp, (x2, y0 + 50), (x2, y - 120), layer)
    line(msp, (x1, y), (x2, y), layer)
    tick = 90
    line(msp, (x1 - tick, y - tick), (x1 + tick, y + tick), layer)
    line(msp, (x2 - tick, y - tick), (x2 + tick, y + tick), layer)
    s = text_s if text_s is not None else f'{abs(x2 - x1):.0f}'
    text(msp, s, (x1 + x2) / 2, y + 70, h, layer, 'center')


def dim_v(msp, y1, y2, x, x0, text_s=None, layer='A-DIM', h=180):
    line(msp, (x0 + 50, y1), (x - 120, y1), layer)
    line(msp, (x0 + 50, y2), (x - 120, y2), layer)
    line(msp, (x, y1), (x, y2), layer)
    tick = 90
    line(msp, (x - tick, y1 - tick), (x + tick, y1 + tick), layer)
    line(msp, (x - tick, y2 - tick), (x + tick, y2 + tick), layer)
    s = text_s if text_s is not None else f'{abs(y2 - y1):.0f}'
    text(msp, s, x - 70, (y1 + y2) / 2, h, layer, 'center', rot=90)


def chair(msp, cx, cy, w=450, d=450, facing='N', layer='A-FURN'):
    """Chair square + back line. facing = side the back is on."""
    rect(msp, cx - w / 2, cy - d / 2, cx + w / 2, cy + d / 2, layer)
    if facing == 'N':
        line(msp, (cx - w / 2, cy + d / 2 - 60), (cx + w / 2, cy + d / 2 - 60), layer)
    elif facing == 'S':
        line(msp, (cx - w / 2, cy - d / 2 + 60), (cx + w / 2, cy - d / 2 + 60), layer)
    elif facing == 'E':
        line(msp, (cx + w / 2 - 60, cy - d / 2), (cx + w / 2 - 60, cy + d / 2), layer)
    else:
        line(msp, (cx - w / 2 + 60, cy - d / 2), (cx - w / 2 + 60, cy + d / 2), layer)


def table_long(msp, x, y, w=2400, d=800, per_side=4, layer='A-FURN'):
    """Table lower-left (x,y). Chairs on long sides."""
    rect(msp, x, y, x + w, y + d, layer)
    pitch = w / per_side
    for i in range(per_side):
        cx = x + pitch * (i + 0.5)
        chair(msp, cx, y - 250, facing='S', layer=layer)
        chair(msp, cx, y + d + 250, facing='N', layer=layer)


def table_6(msp, x, y, w=1800, d=800, layer='A-FURN'):
    table_long(msp, x, y, w, d, 3, layer)


def table_4(msp, x, y, w=1400, d=800, layer='A-FURN'):
    table_long(msp, x, y, w, d, 2, layer)


def table_2(msp, x, y, w=800, d=700, layer='A-FURN'):
    rect(msp, x, y, x + w, y + d, layer)
    chair(msp, x + w / 2, y - 250, facing='S', layer=layer)
    chair(msp, x + w / 2, y + d + 250, facing='N', layer=layer)


def round_table(msp, cx, cy, dia=1600, seats=10, layer='A-FURN'):
    circle(msp, (cx, cy), dia / 2, layer)
    circle(msp, (cx, cy), dia / 2 - 60, layer)
    r = dia / 2 + 320
    for i in range(seats):
        a = 2 * math.pi * i / seats
        chair(msp, cx + r * math.cos(a), cy + r * math.sin(a), facing='N', layer=layer)


def bar(msp, x0, y0, x1, y1, n, side='E', layer='A-FURN'):
    """Bar counter rectangle and n stools."""
    rect(msp, x0, y0, x1, y1, layer)
    if side in ('E', 'W'):
        pitch = (y1 - y0) / n
        for i in range(n):
            cy = y0 + pitch * (i + 0.5)
            cx = x1 + 280 if side == 'E' else x0 - 280
            chair(msp, cx, cy, 400, 400, 'N', layer)
    else:
        pitch = (x1 - x0) / n
        for i in range(n):
            cx = x0 + pitch * (i + 0.5)
            cy = y1 + 280 if side == 'N' else y0 - 280
            chair(msp, cx, cy, 400, 400, 'N', layer)


def equip_rect(msp, x0, y0, x1, y1, label='', layer='A-KITCHEN', h=150):
    rect(msp, x0, y0, x1, y1, layer)
    if label:
        text(msp, label, (x0 + x1) / 2, (y0 + y1) / 2, h, layer, 'center')


def sink(msp, x0, y0, x1, y1, layer='A-KITCHEN'):
    rect(msp, x0, y0, x1, y1, layer)
    rect(msp, x0 + 80, y0 + 80, x1 - 80, y1 - 80, layer)
    circle(msp, ((x0 + x1) / 2, (y0 + y1) / 2), 40, layer)


def arrow(msp, pts, layer='A-PATH', head=350):
    for a, b in zip(pts, pts[1:]):
        line(msp, a, b, layer)
    if len(pts) >= 2:
        a, b = pts[-2], pts[-1]
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        for da in (math.radians(155), math.radians(-155)):
            line(msp, b, (b[0] + head * math.cos(ang + da), b[1] + head * math.sin(ang + da)), layer)


def label_room(msp, name, area, x, y, layer='A-AREA', h=260):
    text(msp, name, x, y + 180, h, layer, 'center')
    text(msp, f'{area:.1f} m2', x, y - 260, h - 50, layer, 'center')


def title_block(msp, x0, y0, w, h, title, subtitle, sheet, scale='1:100', notes=None):
    rect(msp, x0, y0, x0 + w, y0 + h, 'A-TITLE')
    line(msp, (x0, y0 + h - 1200), (x0 + w, y0 + h - 1200), 'A-TITLE')
    text(msp, title, x0 + 300, y0 + h - 750, 380, 'A-TITLE', 'left')
    text(msp, subtitle, x0 + 300, y0 + h - 1600, 260, 'A-TITLE', 'left')
    text(msp, f'图号：{sheet}', x0 + 300, y0 + 800, 220, 'A-TITLE', 'left')
    text(msp, f'比例：{scale}', x0 + 300, y0 + 450, 220, 'A-TITLE', 'left')
    text(msp, '单位：mm   版本：V1.1   日期：2026-10-18', x0 + w - 300, y0 + 150, 200, 'A-TITLE', 'right')
    if notes:
        text(msp, notes, x0 + w - 300, y0 + h - 1500, 200, 'A-NOTE', 'right')


def sheet_frame(msp, x0, y0, x1, y1, title, subtitle, sheet, scale='1:100'):
    rect(msp, x0, y0, x1, y1, 'A-TITLE')
    rect(msp, x0 + 150, y0 + 150, x1 - 150, y1 - 150, 'A-TITLE')
    tbw, tbh = 7200, 3000
    title_block(msp, x1 - 150 - tbw, y0 + 150, tbw, tbh, title, subtitle, sheet, scale)


def north_arrow(msp, x, y, size=900):
    circle(msp, (x, y), size * 0.45, 'A-TITLE')
    poly(msp, [(x, y + size * 0.55), (x - size * 0.18, y - size * 0.25), (x, y - size * 0.15),
               (x + size * 0.18, y - size * 0.25)], 'A-TITLE', closed=True)
    text(msp, 'N', x, y + size * 0.65, 260, 'A-TITLE', 'center')


def copy_original(msp, src_msp, origin, which='1F', layer='A-WALL-EXIST'):
    """Copy original linework for one floor, translated to local coords."""
    ox, oy = origin
    def tr(p):
        return (p[0] - ox, p[1] - oy)
    def in_floor(x, y):
        if which == '1F':
            return x < 100000
        return x > 100000
    for e in src_msp:
        t = e.dxftype()
        if t == 'LINE':
            s, q = e.dxf.start, e.dxf.end
            if in_floor(s.x, s.y) and in_floor(q.x, q.y):
                line(msp, tr((s.x, s.y)), tr((q.x, q.y)), layer)
        elif t == 'LWPOLYLINE':
            pts = [(p[0], p[1]) for p in e.get_points()]
            if pts and all(in_floor(*p) for p in pts):
                poly(msp, [tr(p) for p in pts], layer, closed=e.closed)
        elif t == 'ARC':
            c = e.dxf.center
            if in_floor(c.x, c.y):
                arc(msp, tr((c.x, c.y)), e.dxf.radius, e.dxf.start_angle, e.dxf.end_angle, 'A-DOOR')
        elif t == 'MTEXT':
            pass


def sliding_door(msp, x, y, w=900, vertical=True, layer='A-DOOR'):
    """Sliding door symbol in a wall opening."""
    if vertical:
        rect(msp, x - 40, y, x + 40, y + w, layer)
        rect(msp, x - 120, y + w * 0.15, x + 120, y + w * 0.15 + 60, layer)
        line(msp, (x, y + w * 0.55), (x - 500, y + w * 0.55), layer)
        line(msp, (x - 500, y + w * 0.55), (x - 380, y + w * 0.55 + 80), layer)
        line(msp, (x - 500, y + w * 0.55), (x - 380, y + w * 0.55 - 80), layer)
    else:
        rect(msp, x, y - 40, x + w, y + 40, layer)
        rect(msp, x + w * 0.15, y - 120, x + w * 0.15 + 60, y + 120, layer)
        line(msp, (x + w * 0.55, y), (x + w * 0.55, y - 500), layer)
        line(msp, (x + w * 0.55, y - 500), (x + w * 0.55 + 80, y - 380), layer)
        line(msp, (x + w * 0.55, y - 500), (x + w * 0.55 - 80, y - 380), layer)


def legend(msp, x, y, w=9500, h=2900):
    rect(msp, x, y, x + w, y + h, 'A-TITLE')
    text(msp, '图例 / LEGEND', x + 250, y + h - 380, 220, 'A-TITLE', 'left')
    line(msp, (x + 4200, y + 200), (x + 4200, y + h - 500), 'A-TITLE')
    yy = y + h - 750
    line(msp, (x + 250, yy), (x + 750, yy), 'A-WALL-EXIST')
    text(msp, '原有墙体/结构', x + 900, yy - 70, 170, 'A-NOTE', 'left')
    line(msp, (x + 250, yy - 330), (x + 750, yy - 330), 'A-WALL-NEW')
    line(msp, (x + 250, yy - 420), (x + 750, yy - 420), 'A-WALL-NEW')
    text(msp, '新增隔墙（100mm）', x + 900, yy - 400, 170, 'A-NOTE', 'left')
    line(msp, (x + 250, yy - 700), (x + 750, yy - 700), 'A-WALL-DEMO')
    text(msp, '拆除墙体（待结构复核）', x + 900, yy - 740, 170, 'A-NOTE', 'left')
    rect(msp, x + 280, yy - 1050, x + 720, yy - 900, 'A-FURN')
    text(msp, '家具/餐桌椅', x + 900, yy - 1020, 170, 'A-NOTE', 'left')
    rect(msp, x + 280, yy - 1380, x + 720, yy - 1230, 'A-KITCHEN')
    text(msp, '厨房/服务设备', x + 900, yy - 1350, 170, 'A-NOTE', 'left')
    line(msp, (x + 300, yy - 1660), (x + 700, yy - 1660), 'A-PATH')
    line(msp, (x + 700, yy - 1660), (x + 600, yy - 1610), 'A-PATH')
    text(msp, '人员/物流路径', x + 900, yy - 1680, 170, 'A-NOTE', 'left')
    nn = y + h - 650
    text(msp, '注：1. 尺寸单位mm，比例1:100。', x + 4450, nn, 160, 'A-NOTE', 'left')
    text(msp, '2. 红色为拆除，橙色为新建。', x + 4450, nn - 300, 160, 'A-NOTE', 'left')
    text(msp, '3. 原始DWG保留；拆改、消防、结构、', x + 4450, nn - 600, 160, 'A-NOTE', 'left')
    text(msp, '   机电需专业复核。', x + 4450, nn - 850, 160, 'A-NOTE', 'left')
    text(msp, '4. 厨房/包房/显示屏设备尺寸为方案', x + 4450, nn - 1150, 160, 'A-NOTE', 'left')
    text(msp, '   参考，施工前复核。', x + 4450, nn - 1400, 160, 'A-NOTE', 'left')


def label_seats(msp, name, seats, area, x, y, h=250):
    text(msp, name, x, y + 170, h, 'A-AREA', 'center')
    text(msp, f'{seats}座 / 约{area:.0f}㎡', x, y - 260, 200, 'A-AREA', 'center')
