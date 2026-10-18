import json, math, sys
import ezdxf
from collections import Counter, defaultdict

p = r"D:\code\github\cad-craft\work\original.dxf"
doc = ezdxf.readfile(p)
msp = doc.modelspace()

def ent_bbox(e):
    try:
        if e.dxftype() == "LINE":
            pts = [e.dxf.start, e.dxf.end]
        elif e.dxftype() == "POLYLINE":
            pts = [v.dxf.location for v in e.vertices]
        elif e.dxftype() == "LWPOLYLINE":
            pts = [e.get_point(i) for i in range(len(e))]
        elif e.dxftype() == "ARC":
            c = e.dxf.center; r = e.dxf.radius
            pts = [(c.x-r,c.y-r),(c.x+r,c.y+r)]
        elif e.dxftype() == "CIRCLE":
            c = e.dxf.center; r = e.dxf.radius
            pts = [(c.x-r,c.y-r),(c.x+r,c.y+r)]
        elif e.dxftype() == "MTEXT":
            pts = [e.dxf.insert]
        elif e.dxftype() == "TEXT":
            pts = [e.dxf.insert]
        elif e.dxftype() == "INSERT":
            pts = [e.dxf.insert]
        else:
            return None
        xs=[q[0] for q in pts]; ys=[q[1] for q in pts]
        return (min(xs),min(ys),max(xs),max(ys))
    except Exception:
        return None

rows=[]
for e in msp:
    bb=ent_bbox(e)
    rows.append(dict(type=e.dxftype(), layer=e.dxf.layer, handle=e.dxf.handle, bbox=bb,
                     text=(e.dxf.text if e.dxftype()=="TEXT" else (e.text if e.dxftype()=="MTEXT" else None))))

print("total", len(rows))
print("by type", Counter(r['type'] for r in rows))
print("by layer", Counter(r['layer'] for r in rows))
print("\nTEXTS:")
for r in rows:
    if r['text'] is not None:
        print(json.dumps(r, ensure_ascii=False, default=str))

print("\nLAYER BBOXES:")
for layer in sorted(set(r['layer'] for r in rows)):
    rs=[r for r in rows if r['layer']==layer and r['bbox']]
    if not rs: 
        print(layer, "no bbox", sum(1 for r in rows if r['layer']==layer)); continue
    x0=min(r['bbox'][0] for r in rs); y0=min(r['bbox'][1] for r in rs)
    x1=max(r['bbox'][2] for r in rs); y1=max(r['bbox'][3] for r in rs)
    print(f"{layer!r:30} n={len(rs):4} bbox=({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f}) size=({x1-x0:.0f}x{y1-y0:.0f})")

print("\nNON-TEXT ENTITIES (first 200):")
n=0
for r in rows:
    if r['text'] is None:
        print(json.dumps(r, ensure_ascii=False, default=str))
        n+=1
        if n>=200: break

with open(r"D:\code\github\cad-craft\work\entities.json","w",encoding="utf-8") as f:
    json.dump(rows,f,ensure_ascii=False,default=str,indent=1)
