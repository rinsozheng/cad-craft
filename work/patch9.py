p=r"D:\code\github\cad-craft\work\design_lib.py"
s=open(p,encoding="utf-8").read()
s=s.replace("tbw, tbh = 7200, 2600","tbw, tbh = 7200, 3000")
s=s.replace("text(msp, title, x0 + 300, y0 + h - 700, 380, 'A-TITLE', 'left')","text(msp, title, x0 + 300, y0 + h - 750, 380, 'A-TITLE', 'left')")
s=s.replace("text(msp, subtitle, x0 + 300, y0 + h - 1500, 260, 'A-TITLE', 'left')","text(msp, subtitle, x0 + 300, y0 + h - 1600, 260, 'A-TITLE', 'left')")
s=s.replace("text(msp, f'图号：{sheet}', x0 + 300, y0 + 650, 220, 'A-TITLE', 'left')","text(msp, f'图号：{sheet}', x0 + 300, y0 + 800, 220, 'A-TITLE', 'left')")
s=s.replace("text(msp, f'比例：{scale}', x0 + 300, y0 + 350, 220, 'A-TITLE', 'left')","text(msp, f'比例：{scale}', x0 + 300, y0 + 450, 220, 'A-TITLE', 'left')")
s=s.replace("text(msp, '单位：mm   版本：V1.1   日期：2026-10-18', x0 + w - 300, y0 + 100, 200, 'A-TITLE', 'right')","text(msp, '单位：mm   版本：V1.1   日期：2026-10-18', x0 + w - 300, y0 + 150, 200, 'A-TITLE', 'right')")
open(p,"w",encoding="utf-8").write(s)

p=r"D:\code\github\cad-craft\work\build.py"
s=open(p,encoding="utf-8").read()
s=s.replace("text(msp, '二层平面图', 7200, 11750, 600, 'A-TEXT', 'center')","text(msp, '二层平面图', 7200, 11650, 500, 'A-TEXT', 'center')")
s=s.replace("text(msp, '尺寸单位：mm  比例：1:100', 7200, 11450, 220, 'A-NOTE', 'center')","text(msp, '尺寸单位：mm  比例：1:100', 7200, 10950, 220, 'A-NOTE', 'center')")
s=s.replace("dim_h(msp, 10640, 14140, 11000, 10500, '3500', 'A-DIM')","dim_h(msp, 10640, 14140, 10650, 10500, '3500', 'A-DIM')")
s=s.replace("dim_h(msp, 350, 4170, -900, 0, '3820', 'A-DIM')","dim_h(msp, 350, 4170, -1800, 0, '3820', 'A-DIM')")
# combined private room labels
s=s.replace("""    text(msp, '包房1（8-10人）', 12390, 10200, 190, 'A-AREA', 'center')
    text(msp, '12.5 m2', 12390, 7150, 170, 'A-AREA', 'center')
    text(msp, '包房2（8-10人）', 12390, 6650, 190, 'A-AREA', 'center')
    text(msp, '11.8 m2', 12390, 3650, 170, 'A-AREA', 'center')""","""    text(msp, '包房1（8-10人） 12.5㎡', 12390, 10200, 175, 'A-AREA', 'center')
    text(msp, '包房2（8-10人） 11.8㎡', 12390, 6650, 175, 'A-AREA', 'center')""")
open(p,"w",encoding="utf-8").write(s)
print("patched")
