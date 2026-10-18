p=r"D:\code\github\cad-craft\work\design_lib.py"
s=open(p,encoding="utf-8").read()
old='''def title_block(msp, x0, y0, w, h, title, subtitle, sheet, scale='1:100', notes=None):
    rect(msp, x0, y0, x0 + w, y0 + h, 'A-TITLE')
    line(msp, (x0, y0 + h - 900), (x0 + w, y0 + h - 900), 'A-TITLE')
    text(msp, title, x0 + 300, y0 + h - 520, 420, 'A-TITLE', 'left')
    text(msp, subtitle, x0 + 300, y0 + h - 1250, 300, 'A-TITLE', 'left')
    text(msp, f'图号：{sheet}', x0 + 300, y0 + 380, 260, 'A-TITLE', 'left')
    text(msp, f'比例：{scale}', x0 + 300, y0 + 120, 260, 'A-TITLE', 'left')
    text(msp, '单位：mm   版本：V1.1   日期：2026-10-18', x0 + w - 300, y0 + 120, 240, 'A-TITLE', 'right')
    if notes:
        text(msp, notes, x0 + w - 300, y0 + h - 1250, 220, 'A-NOTE', 'right')'''
new='''def title_block(msp, x0, y0, w, h, title, subtitle, sheet, scale='1:100', notes=None):
    rect(msp, x0, y0, x0 + w, y0 + h, 'A-TITLE')
    line(msp, (x0, y0 + h - 1200), (x0 + w, y0 + h - 1200), 'A-TITLE')
    text(msp, title, x0 + 300, y0 + h - 700, 380, 'A-TITLE', 'left')
    text(msp, subtitle, x0 + 300, y0 + h - 1500, 260, 'A-TITLE', 'left')
    text(msp, f'图号：{sheet}', x0 + 300, y0 + 650, 220, 'A-TITLE', 'left')
    text(msp, f'比例：{scale}', x0 + 300, y0 + 350, 220, 'A-TITLE', 'left')
    text(msp, '单位：mm   版本：V1.1   日期：2026-10-18', x0 + w - 300, y0 + 100, 200, 'A-TITLE', 'right')
    if notes:
        text(msp, notes, x0 + w - 300, y0 + h - 1500, 200, 'A-NOTE', 'right')'''
assert old in s
s=s.replace(old,new)
s=s.replace("tbw, tbh = 7200, 1900","tbw, tbh = 7200, 2600")
open(p,"w",encoding="utf-8").write(s)
print("title patched")
