p=r"D:\code\github\cad-craft\work\build.py"
s=open(p,encoding="utf-8").read()
s=s.replace("""    if mode == 'demo':
        labels_2f(msp, scheme)
    elif mode == 'furn':""","""    if mode == 'demo':
        labels_2f(msp, scheme)
        text(msp, '二层无墙体拆除；仅新增包房门洞、屏墙及服务间门洞', 7000, 9000, 220, 'A-NOTE', 'center')
    elif mode == 'furn':""")
open(p,"w",encoding="utf-8").write(s)
print("patched")
