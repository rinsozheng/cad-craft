p=r"D:\code\github\cad-craft\work\build.py"
s=open(p,encoding="utf-8").read()
s=s.replace("""    text(msp, '男卫', 1000, 3200, 180, 'A-FIXTURE', 'center')
    text(msp, '女卫', 3300, 3200, 180, 'A-FIXTURE', 'center')""","")
s=s.replace("""    text(msp, '显示屏', 7000, 2750, 220, 'A-SCREEN', 'center')""","""    text(msp, '显示屏', 7000, 2750, 220, 'A-SCREEN', 'center')
    text(msp, '男卫', 1000, 3200, 180, 'A-AREA', 'center')
    text(msp, '女卫', 3300, 3200, 180, 'A-AREA', 'center')""")
open(p,"w",encoding="utf-8").write(s)
print("patched")
