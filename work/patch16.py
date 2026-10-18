p=r"D:\code\github\cad-craft\work\design_lib.py"
s=open(p,encoding="utf-8").read()
add='''

def label_seats(msp, name, seats, area, x, y, h=250):
    text(msp, name, x, y + 170, h, 'A-AREA', 'center')
    text(msp, f'{seats}座 / 约{area:.0f}㎡', x, y - 260, 200, 'A-AREA', 'center')
'''
if 'def label_seats' not in s:
    s += add
open(p,"w",encoding="utf-8").write(s)

p=r"D:\code\github\cad-craft\work\build.py"
s=open(p,encoding="utf-8").read()
s=s.replace("label_room(msp, '公共就餐区', 92.0, 10300, 20200)","label_seats(msp, '公共就餐区', 92, 100, 10300, 20200)")
s=s.replace("label_room(msp, '公共就餐区', 80.0, 3000, 10050)","label_seats(msp, '公共就餐区', 80, 84, 3000, 10050)")
open(p,"w",encoding="utf-8").write(s)
print("patched")
