p=r"D:\code\github\cad-craft\work\build.py"
s=open(p,encoding="utf-8").read()
# 1F south rows move up
s=s.replace("for yy in (14300, 16500):","for yy in (14600, 16500):")
# public label 1F
s=s.replace("label_room(msp, '公共就餐区', 92.0, 10300, 19600)","label_room(msp, '公共就餐区', 92.0, 10300, 20550)")
# dishwash label move
s=s.replace("label_room(msp, '洗碗间', 4.6, 12500, 5400)","text(msp, '洗碗间 4.6 m2', 12475, 7250, 190, 'A-KITCHEN', 'center')")
# 2F private labels custom
s=s.replace("    label_room(msp, '包房1（8-10人）', 12.5, 12390, 10300)\n    label_room(msp, '包房2（8-10人）', 11.8, 12390, 6700)\n","""    text(msp, '包房1（8-10人）', 12390, 10200, 190, 'A-AREA', 'center')
    text(msp, '12.5 m2', 12390, 7150, 170, 'A-AREA', 'center')
    text(msp, '包房2（8-10人）', 12390, 6650, 190, 'A-AREA', 'center')
    text(msp, '11.8 m2', 12390, 3650, 170, 'A-AREA', 'center')
""")
open(p,"w",encoding="utf-8").write(s)
print("patched")
