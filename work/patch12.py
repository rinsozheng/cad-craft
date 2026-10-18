p=r"D:\code\github\cad-craft\work\design_lib.py"
s=open(p,encoding="utf-8").read()
start=s.index("def legend(msp, x, y")
new='''def legend(msp, x, y, w=9500, h=2900):
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
'''
s=s[:start]+new
open(p,"w",encoding="utf-8").write(s)

p=r"D:\code\github\cad-craft\work\build.py"
s=open(p,encoding="utf-8").read()
s=s.replace("""    for (x0, y0, x1, y1) in [
        (7420, 2620, 8422, 2730), (8530, 2620, 14180, 2730),
        (8422, 600, 8434, 2620),
        (11770, 3760, 11880, 5850), (11770, 5850, 14180, 5970),
    ]:
        line(msp, (x0, y0), (x1, y1), 'A-WALL-DEMO')
        line(msp, (x0, y1), (x1, y0), 'A-WALL-DEMO')""","""    for (x0, y0, x1, y1) in [
        (7420, 2620, 8422, 2730), (8530, 2620, 14180, 2730),
        (8422, 600, 8434, 2620),
        (11770, 3760, 11880, 5850), (11770, 5850, 14180, 5970),
    ]:
        line(msp, (x0, y0), (x1, y1), 'A-WALL-DEMO')
        if abs(x1 - x0) + abs(y1 - y0) < 2500:
            line(msp, (x0, y1), (x1, y0), 'A-WALL-DEMO')""")
open(p,"w",encoding="utf-8").write(s)
print("patched")
