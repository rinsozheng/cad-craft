import ezdxf, json
p = r"D:\code\github\cad-craft\work\original.dxf"
doc = ezdxf.readfile(p)
msp = doc.modelspace()

def fix(s):
    if s is None: return None
    try:
        return s.encode('latin1').decode('gbk')
    except Exception:
        return s

print("POLYLINES")
for e in msp.query('LWPOLYLINE'):
    pts = [(round(x,1), round(y,1)) for x,y,*_ in e.get_points()]
    print(e.dxf.handle, "closed" if e.closed else "open", pts)
print("\nARCS")
for e in msp.query('ARC'):
    c=e.dxf.center
    print(e.dxf.handle, f"c=({c.x:.1f},{c.y:.1f}) r={e.dxf.radius:.1f} a={e.dxf.start_angle:.1f}->{e.dxf.end_angle:.1f}")
print("\nINSERT")
for e in msp.query('INSERT'):
    print(e.dxf.handle, e.dxf.name, tuple(round(v,1) for v in e.dxf.insert), e.dxf.xscale, e.dxf.yscale, e.dxf.rotation)
print("\nTEXTS")
for e in msp.query('MTEXT'):
    print(e.dxf.handle, tuple(round(v,1) for v in e.dxf.insert), repr(fix(e.text)), "->", repr(fix(e.plain_text())))
print("\nLINES")
for e in msp.query('LINE'):
    s,t=e.dxf.start,e.dxf.end
    print(f"{e.dxf.handle} {s.x:.1f},{s.y:.1f} -> {t.x:.1f},{t.y:.1f}  L={((t.x-s.x)**2+(t.y-s.y)**2)**0.5:.1f}")
