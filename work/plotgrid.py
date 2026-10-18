import ezdxf, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc as MArc
import numpy as np

doc = ezdxf.readfile(r"D:\code\github\cad-craft\work\original.dxf")
msp = doc.modelspace()

def segs():
    S=[]
    for e in msp:
        t=e.dxftype()
        if t=="LINE":
            S.append((e.dxf.start.x,e.dxf.start.y,e.dxf.end.x,e.dxf.end.y,e.dxf.handle))
        elif t=="LWPOLYLINE":
            pts=[(x,y) for x,y,*_ in e.get_points()]
            if e.closed: pts.append(pts[0])
            for a,b in zip(pts,pts[1:]):
                S.append((a[0],a[1],b[0],b[1],e.dxf.handle))
    return S

def draw(x0,x1,y0,y1,name):
    fig,ax=plt.subplots(figsize=(16,12))
    for sx,sy,ex,ey,h in segs():
        if max(sx,ex)<x0 or min(sx,ex)>x1 or max(sy,ey)<y0 or min(sy,ey)>y1: continue
        ax.plot([sx/1000,ex/1000],[sy/1000,ey/1000],'-',lw=1.2,color='black')
    for e in msp.query('ARC'):
        c=e.dxf.center
        if not(x0<=c.x<=x1 and y0<=c.y<=y1): continue
        ax.add_patch(MArc((c.x/1000,c.y/1000),e.dxf.radius/1000,e.dxf.radius/1000,angle=0,
                          theta1=e.dxf.start_angle,theta2=e.dxf.end_angle,color='green',lw=1.2))
    ax.set_xlim(x0/1000,x1/1000); ax.set_ylim(y0/1000,y1/1000)
    ax.set_aspect('equal'); ax.grid(True,which='major',color='0.7',lw=0.5)
    ax.set_xticks(np.arange(np.floor(x0/1000),np.ceil(x1/1000)+0.01,1))
    ax.set_yticks(np.arange(np.floor(y0/1000),np.ceil(y1/1000)+0.01,1))
    ax.tick_params(labelsize=7)
    ax.set_title(name)
    fig.tight_layout(); fig.savefig(rf"D:\code\github\cad-craft\work\{name}.png",dpi=170); plt.close(fig)

draw(73500,95000,0,23000,"plan_1f_grid")
draw(101500,117000,10000,22000,"plan_2f_grid")
print("done")
