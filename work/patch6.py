p=r"D:\code\github\cad-craft\work\build.py"
s=open(p,encoding="utf-8").read()

# replace dims functions
start=s.index("def dims_1f(msp):")
end=s.index("# ================= 2F =================")
new='''def dims_1f(msp):
    dim_h(msp, 460, 19840, 22400, 20930, '19380', 'A-DIM')
    dim_v(msp, 14030, 20930, 21100, 19840, '6900', 'A-DIM')
    dim_v(msp, 600, 14030, 15100, 14180, '13430', 'A-DIM')
    dim_h(msp, 7420, 14180, 200, 600, '6760', 'A-DIM')
    dim_h(msp, 7420, 12900, 5000, 4800, '5480', 'A-DIM')
    dim_v(msp, 2620, 4800, 10100, 10000, '2180', 'A-DIM')
    dim_h(msp, 12100, 14180, 3000, 2620, '2080', 'A-DIM')
    dim_h(msp, 7600, 13180, 15500, 15230, '5580', 'A-DIM')
    text(msp, '主要尺寸（mm）', 15000, -1800, 300, 'A-DIM', 'center')

'''
s=s[:start]+new+s[end:]
start=s.index("def dims_2f(msp):")
end=s.index("# ================= sheets =================")
new='''def dims_2f(msp):
    dim_h(msp, 350, 14140, 11500, 10500, '13790', 'A-DIM')
    dim_v(msp, 0, 10500, 15500, 14140, '10500', 'A-DIM')
    dim_h(msp, 350, 4170, -900, 0, '3820', 'A-DIM')
    dim_v(msp, 0, 3440, 4700, 4170, '3440', 'A-DIM')
    dim_h(msp, 10640, 14140, 11000, 10500, '3500', 'A-DIM')
    dim_v(msp, 3560, 10500, 15000, 14140, '6940', 'A-DIM')
    dim_h(msp, 5500, 8500, 2500, 3440, '3000', 'A-DIM')
    text(msp, '主要尺寸（mm）', 12000, -1800, 300, 'A-DIM', 'center')

'''
s=s[:start]+new+s[end:]

# sheet modes for dims: no furniture
s=s.replace("""    elif mode == 'dims':
        furn_1f(msp, scheme); labels_1f(msp); dims_1f(msp)""","""    elif mode == 'dims':
        labels_1f(msp); dims_1f(msp)""")
s=s.replace("""    elif mode == 'dims':
        furn_2f(msp, scheme); labels_2f(msp); dims_2f(msp)""","""    elif mode == 'dims':
        labels_2f(msp); dims_2f(msp)""")

# titles
s=s.replace("text(msp, '一层平面图', 10000, 22000, 600, 'A-TEXT', 'center')","text(msp, '一层平面图', 10000, 22950, 600, 'A-TEXT', 'center')")
s=s.replace("north_arrow(msp, 19000, 22000)","north_arrow(msp, 19000, 22850)")
s=s.replace("text(msp, '二层平面图', 7200, 11400, 600, 'A-TEXT', 'center')","text(msp, '二层平面图', 7200, 11900, 600, 'A-TEXT', 'center')")
s=s.replace("text(msp, '尺寸单位：mm  比例：1:100', 7200, 10800, 220, 'A-NOTE', 'center')","text(msp, '尺寸单位：mm  比例：1:100', 7200, 11200, 220, 'A-NOTE', 'center')")
s=s.replace("north_arrow(msp, 13500, 11500)","north_arrow(msp, 15000, 11900)")
open(p,"w",encoding="utf-8").write(s)
print("patched")
