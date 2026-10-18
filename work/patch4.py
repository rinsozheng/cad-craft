p=r"D:\code\github\cad-craft\work\design_lib.py"
s=open(p,encoding="utf-8").read()
add='''

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
'''
if 'def sliding_door' not in s:
    s += add
open(p,"w",encoding="utf-8").write(s)

p=r"D:\code\github\cad-craft\work\build.py"
s=open(p,encoding="utf-8").read()
s=s.replace("door(msp, 10640, 8200, 900, 0)     # room A door, swings east into room","sliding_door(msp, 10640, 8200, 900, True)   # room A sliding door")
s=s.replace("door(msp, 10640, 4800, 900, 0)     # room B door","sliding_door(msp, 10640, 4800, 900, True)   # room B sliding door")
s=s.replace("door(msp, 10640, 1600, 900, 0)     # pantry door","sliding_door(msp, 10640, 1600, 900, True)   # pantry sliding door")
s=s.replace("door(msp, 12200, 3560, 900, 270)   # pantry to room B, swings south","sliding_door(msp, 12200, 3560, 900, False)  # pantry to room B sliding door")
s=s.replace("door(msp, 1730, 5600, 900, 180)    # stair opening, swings into stair","sliding_door(msp, 1730, 5600, 900, True)   # stair opening")
# sinks remove third
s=s.replace("for xx in [600, 2400, 3300]:","for xx in [600, 2400]:")
# toilet labels
s=s.replace("text(msp, '男卫', 1100, 1850, 220, 'A-FIXTURE', 'center')","text(msp, '男卫', 1000, 3200, 180, 'A-FIXTURE', 'center')")
s=s.replace("text(msp, '女卫', 3200, 1850, 220, 'A-FIXTURE', 'center')","text(msp, '女卫', 3300, 3200, 180, 'A-FIXTURE', 'center')")
# stair labels
s=s.replace("text(msp, '楼梯', 1040, 4600, 220, 'A-TEXT', 'center')","text(msp, '楼梯', 1040, 6300, 200, 'A-TEXT', 'center')")
s=s.replace("text(msp, '至一层', 1040, 4300, 200, 'A-NOTE', 'center')","text(msp, '至一层', 1040, 6000, 180, 'A-NOTE', 'center')")
# 1F label cleanup
s=s.replace("    label_room(msp, '打菜/排队', 18.0, 10390, 14700)\n","")
s=s.replace("    label_room(msp, '餐具回收', 2.8, 15750, 14320)\n","")
s=s.replace("    text(msp, '打菜区（5工位）', 10390, 13600, 260, 'A-SERVING', 'center')","    text(msp, '打菜区（5工位）', 10390, 15450, 220, 'A-SERVING', 'center')")
s=s.replace("    text(msp, '排队区', 10390, 15850, 240, 'A-TEXT', 'center')","    text(msp, '排队区', 10390, 16000, 220, 'A-TEXT', 'center')")
open(p,"w",encoding="utf-8").write(s)
print("patched")
