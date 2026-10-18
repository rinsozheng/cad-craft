p=r"D:\code\github\cad-craft\work\design_lib.py"
s=open(p,encoding="utf-8").read()
add='''

def legend(msp, x, y, w=8500, h=2700):
    rect(msp, x, y, x + w, y + h, 'A-TITLE')
    text(msp, '图例 / LEGEND', x + 250, y + h - 420, 240, 'A-TITLE', 'left')
    yy = y + h - 850
    # existing
    line(msp, (x + 250, yy), (x + 850, yy), 'A-WALL-EXIST')
    text(msp, '原有墙体/结构', x + 1000, yy - 80, 190, 'A-NOTE', 'left')
    # new
    line(msp, (x + 250, yy - 380), (x + 850, yy - 380), 'A-WALL-NEW')
    line(msp, (x + 250, yy - 480), (x + 850, yy - 480), 'A-WALL-NEW')
    text(msp, '新增隔墙（100mm）', x + 1000, yy - 460, 190, 'A-NOTE', 'left')
    # demo
    line(msp, (x + 250, yy - 800), (x + 850, yy - 800), 'A-WALL-DEMO')
    line(msp, (x + 250, yy - 880), (x + 850, yy - 720), 'A-WALL-DEMO')
    text(msp, '拆除墙体（待结构复核）', x + 1000, yy - 860, 190, 'A-NOTE', 'left')
    # furniture
    rect(msp, x + 300, yy - 1220, x + 800, yy - 1020, 'A-FURN')
    text(msp, '家具/餐桌椅', x + 1000, yy - 1180, 190, 'A-NOTE', 'left')
    # equipment
    rect(msp, x + 300, yy - 1580, x + 800, yy - 1380, 'A-KITCHEN')
    text(msp, '厨房/服务设备', x + 1000, yy - 1540, 190, 'A-NOTE', 'left')
    # path
    line(msp, (x + 300, yy - 1880), (x + 800, yy - 1880), 'A-PATH')
    line(msp, (x + 800, yy - 1880), (x + 680, yy - 1820), 'A-PATH')
    text(msp, '人员/物流路径', x + 1000, yy - 1900, 190, 'A-NOTE', 'left')
    # notes
    text(msp, '注：1. 尺寸单位mm，比例1:100。2. 红色为拆除，橙色为新建。', x + 2600, yy - 250, 180, 'A-NOTE', 'left')
    text(msp, '3. 原始DWG保留；拆改、消防、结构、机电需专业复核。', x + 2600, yy - 550, 180, 'A-NOTE', 'left')
    text(msp, '4. 厨房/包房/显示屏等设备尺寸为方案参考，施工前复核。', x + 2600, yy - 850, 180, 'A-NOTE', 'left')
'''
if 'def legend' not in s:
    s += add
open(p,"w",encoding="utf-8").write(s)

p=r"D:\code\github\cad-craft\work\build.py"
s=open(p,encoding="utf-8").read()
# remove long demo notes and add 拆 labels
s=s.replace("""    text(msp, '拆除（待结构复核）', 10600, 3200, 220, 'A-WALL-DEMO', 'center')
    text(msp, '拆除（待结构复核）', 8300, 3000, 220, 'A-WALL-DEMO', 'center')""","""    text(msp, '拆', 12500, 2670, 200, 'A-WALL-DEMO', 'center')
    text(msp, '拆', 8000, 2670, 200, 'A-WALL-DEMO', 'center')
    text(msp, '拆', 12000, 3900, 200, 'A-WALL-DEMO', 'center')""")
# call legend in sheet functions
s=s.replace("""    sheet_frame(msp, -2500, -3500, 22300, 23700, '美莱食堂改造', '一层平面图', name, '1:100')
    save(doc, name)""","""    sheet_frame(msp, -2500, -3500, 22300, 23700, '美莱食堂改造', '一层平面图', name, '1:100')
    legend(msp, -2200, -3300)
    save(doc, name)""")
s=s.replace("""    sheet_frame(msp, -2500, -3500, 20000, 12500, '美莱食堂改造', '二层平面图', name, '1:100')
    save(doc, name)""","""    sheet_frame(msp, -2500, -3500, 20000, 12500, '美莱食堂改造', '二层平面图', name, '1:100')
    legend(msp, -2200, -3300)
    save(doc, name)""")
s=s.replace("""    sheet_frame(msp, -2500, -3500, 42000, 23700, '美莱食堂改造', '一、二层综合设计图', name, '1:100')
    save(doc, name)""","""    sheet_frame(msp, -2500, -3500, 42000, 23700, '美莱食堂改造', '一、二层综合设计图', name, '1:100')
    legend(msp, -2200, -3300)
    save(doc, name)""")
open(p,"w",encoding="utf-8").write(s)
print("patched")
