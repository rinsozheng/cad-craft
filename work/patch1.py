import re
p=r"D:\code\github\cad-craft\work\design_lib.py"
s=open(p,encoding="utf-8").read()
s=s.replace("SCREEN_Y0, SCREEN_Y1 = 3460.00, 3660.00","SCREEN_Y0, SCREEN_Y1 = 3240.00, 3440.00")
s=s.replace("""        elif t == 'MTEXT':
            s = e.text
            try:
                s2 = s.encode('latin1').decode('gbk')
            except Exception:
                s2 = s
            if 'H' in s2 and s2.replace('H', '').isdigit():
                p = e.dxf.insert
                if in_floor(p.x, p.y):
                    text(msp, s2, *tr((p.x, p.y)), h=220, layer='A-NOTE')""","""        elif t == 'MTEXT':
            pass""")
open(p,"w",encoding="utf-8").write(s)
print("lib updated")
