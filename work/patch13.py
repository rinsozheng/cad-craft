p=r"D:\code\github\cad-craft\work\build.py"
s=open(p,encoding="utf-8").read()

# move pantry equipment out of walls_2f
old='''    # service counter in pantry
    rect(msp, 13600, 800, 14100, 2800, 'A-SERVING')
    rect(msp, 13650, 900, 14050, 1500, 'A-SERVING')
    circle(msp, (13850, 1200), 90, 'A-SERVING')
    text(msp, '备餐/服务台', 13850, 2400, 150, 'A-SERVING', 'center')
    rect(msp, 10800, 600, 11600, 1200, 'A-KITCHEN')
    text(msp, '保温柜', 11200, 900, 140, 'A-KITCHEN', 'center')
    rect(msp, 11800, 600, 12600, 1200, 'A-KITCHEN')
    text(msp, '冰箱', 12200, 900, 140, 'A-KITCHEN', 'center')
'''
assert old in s
s=s.replace(old,'')
# insert into furn_2f at start
s=s.replace("""def furn_2f(msp, scheme='A'):
    if scheme == 'A':""","""def furn_2f(msp, scheme='A'):
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
    if scheme == 'A':""")

# screen size
s=s.replace("rect(msp, SCREEN_X0 + 200, SCREEN_Y0 + 50, SCREEN_X1 - 200, SCREEN_Y1 - 50, 'A-SCREEN')",
            "rect(msp, 5800, SCREEN_Y0 + 40, 8200, SCREEN_Y1 - 40, 'A-SCREEN')")
s=s.replace("text(msp, 'LED屏 3000x1700', 7000, 3220, 200, 'A-SCREEN', 'center')",
            "text(msp, 'LED屏 2400x1350', 7000, 3160, 180, 'A-SCREEN', 'center')")

# furn_1f tables flag
s=s.replace("def furn_1f(msp, scheme='A'):\n    # tables: scheme A = 8-seat long + 4-seat; scheme B = 6-seat + 4-seat\n    if scheme == 'A':",
            "def furn_1f(msp, scheme='A', tables=True):\n    # tables: scheme A = 8-seat long + 4-seat; scheme B = 6-seat + 4-seat\n    if tables and scheme == 'A':")
s=s.replace("    else:\n        for i in range(5):\n            table_6(msp, 1800 + i * 3000, 18600, 1800, 800)",
            "    elif tables:\n        for i in range(5):\n            table_6(msp, 1800 + i * 3000, 18600, 1800, 800)")
s=s.replace("        bar(msp, 15000, 20400, 19000, 20700, 8, 'S')\n    # serving counter and queue",
            "        bar(msp, 15000, 20400, 19000, 20700, 8, 'S')\n    # serving counter and queue")
# kitchen sheet no tables
s=s.replace("        furn_1f(msp, scheme); labels_1f(msp)\n    elif mode == 'kitchen':\n        furn_1f(msp, scheme); labels_1f(msp)",
            "        furn_1f(msp, scheme); labels_1f(msp)\n    elif mode == 'kitchen':\n        furn_1f(msp, scheme, tables=False); labels_1f(msp)")
open(p,"w",encoding="utf-8").write(s)
print("patched")
