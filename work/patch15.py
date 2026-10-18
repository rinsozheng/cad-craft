p=r"D:\code\github\cad-craft\work\build.py"
s=open(p,encoding="utf-8").read()
s=s.replace("""        elif e.dxftype() == 'TEXT':
            c.dxf.insert = (e.dxf.insert.x + dx, e.dxf.insert.y + dy, 0)
        msp.add_entity(c)""","""        elif e.dxftype() == 'TEXT':
            c.dxf.insert = (e.dxf.insert.x + dx, e.dxf.insert.y + dy, 0)
            if c.dxf.hasattr('align_point'):
                ap = c.dxf.align_point
                c.dxf.align_point = (ap.x + dx, ap.y + dy, 0)
        msp.add_entity(c)""")
open(p,"w",encoding="utf-8").write(s)
print("patched")
