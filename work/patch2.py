p=r"D:\code\github\cad-craft\work\build.py"
s=open(p,encoding="utf-8").read()

# 1F A east zone + tray return
s=s.replace("""        # east zone
        for yy in (14300, 16500):
            table_long(msp, 13400, yy, 2400, 800, 4)
            table_4(msp, 17400, yy, 1400, 800)
        # east bar
        bar(msp, 19420, 14200, 19820, 18100, 8, 'W')""",
"""        # east zone
        for yy in (14300, 16500):
            table_long(msp, 14400, yy, 2400, 800, 4)
            table_4(msp, 17000, yy, 1400, 800)
            table_2(msp, 18500, yy + 50, 800, 700)
        # tray return at east wall
        rect(msp, 19300, 14200, 19820, 16600, 'A-SERVING')
        text(msp, '餐具回收', 19560, 15400, 160, 'A-SERVING', 'center', rot=90)""")

# 1F B east zone + remove bar + north counters
s=s.replace("""            table_6(msp, 13400, yy, 1800, 800)
            table_4(msp, 16000, yy, 1400, 800)
        bar(msp, 19420, 14200, 19820, 18100, 8, 'W')""",
"""            table_6(msp, 14400, yy, 1800, 800)
            table_4(msp, 16800, yy, 1400, 800)
        # north window counters
        bar(msp, 4600, 20400, 8000, 20700, 6, 'S')
        bar(msp, 15000, 20400, 19000, 20700, 8, 'S')""")

# old tray return remove
s=s.replace("""    # tray return
    rect(msp, 14500, 14030, 17000, 14630, 'A-SERVING')
    text(msp, '餐具回收', 15750, 14320, 200, 'A-SERVING', 'center')
""","")

# 2F doors
s=s.replace("door(msp, 10640, 8200, 900, 180)   # room A door, swings west","door(msp, 10640, 8200, 900, 0)     # room A door, swings east into room")
s=s.replace("door(msp, 10640, 4800, 900, 180)   # room B door","door(msp, 10640, 4800, 900, 0)     # room B door")
s=s.replace("door(msp, 10640, 1600, 900, 180)   # pantry door","door(msp, 10640, 1600, 900, 0)     # pantry door")
s=s.replace("door(msp, 12200, 3560, 900, 90)    # pantry to room B","door(msp, 12200, 3560, 900, 270)   # pantry to room B, swings south")
s=s.replace("door(msp, 1730, 5600, 900, 0)      # stair opening","door(msp, 1730, 5600, 900, 180)    # stair opening, swings into stair")

# 2F A furniture: rows, remove bar, north counter, lower strip
s=s.replace("""        for yy in (3800, 6100, 8400):
            table_long(msp, 1900, yy, 2400, 800, 4)
            table_long(msp, 5700, yy, 2400, 800, 4)
            table_2(msp, 9500, yy + 50, 800, 700)
        # lower strip: long + six + two
        table_long(msp, 4400, 900, 2400, 800, 4)
        table_6(msp, 8000, 900, 1800, 800)
        table_2(msp, 10000, 950, 800, 700)
        # east bar
        bar(msp, 10340, 4000, 10620, 10000, 10, 'W')""",
"""        for yy in (4000, 6100, 8200):
            table_long(msp, 1900, yy, 2400, 800, 4)
            table_long(msp, 5700, yy, 2400, 800, 4)
            table_2(msp, 9500, yy + 50, 800, 700)
        # lower strip: long + six + two
        table_long(msp, 4400, 900, 2400, 800, 4)
        table_6(msp, 8000, 900, 1800, 800)
        table_2(msp, 9800, 950, 800, 700)
        # north window counter
        bar(msp, 5500, 10150, 9500, 10450, 10, 'S')""")

# 2F B rows
s=s.replace("""        for yy in (3800, 6100, 8400):
            table_4(msp, 1900, yy, 1400, 800)""","""        for yy in (4000, 6100, 8200):
            table_4(msp, 1900, yy, 1400, 800)""")

# 2F sinks and remove duplicate toilet labels
s=s.replace("""    for xx in [1500, 2600, 3500]:
        rect(msp, xx, 2500, xx + 600, 3000, 'A-FIXTURE')
        circle(msp, (xx + 300, 2750), 80, 'A-FIXTURE')""",
"""    for xx in [600, 2400, 3300]:
        rect(msp, xx, 2500, xx + 600, 3000, 'A-FIXTURE')
        circle(msp, (xx + 300, 2750), 80, 'A-FIXTURE')""")
s=s.replace("""    text(msp, '男卫', 1100, 2200, 220, 'A-FIXTURE', 'center')
    text(msp, '女卫', 3200, 2200, 220, 'A-FIXTURE', 'center')""",
"""    text(msp, '男卫', 1100, 1850, 220, 'A-FIXTURE', 'center')
    text(msp, '女卫', 3200, 1850, 220, 'A-FIXTURE', 'center')""")

# labels 2F: remove duplicate room labels, move public label
s=s.replace("""    label_room(msp, '公共就餐区', 80.0, 6200, 9600)""","""    label_room(msp, '公共就餐区', 80.0, 3000, 10050)""")
s=s.replace("""    label_room(msp, '男卫', 4.3, 950, 3700)
    label_room(msp, '女卫', 4.5, 3300, 3700)
""","")
s=s.replace("""    text(msp, '显示屏', 7000, 3000, 220, 'A-SCREEN', 'center')""","""    text(msp, '显示屏', 7000, 2750, 220, 'A-SCREEN', 'center')""")

# seat labels 1F
s=s.replace("label_room(msp, '公共就餐区', 96.0, 10300, 19600)","label_room(msp, '公共就餐区', 92.0, 10300, 19600)")

open(p,"w",encoding="utf-8").write(s)
print("build patched")
