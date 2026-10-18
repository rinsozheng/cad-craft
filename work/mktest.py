import ezdxf
doc=ezdxf.new('R2018')
doc.styles.add('CN', font='simhei.ttf')
msp=doc.modelspace()
msp.add_lwpolyline([(0,0),(5000,0),(5000,3000),(0,3000)], close=True, dxfattribs={'layer':'A-WALL'})
msp.add_text('美莱食堂 一层平面图', height=300, dxfattribs={'style':'CN','layer':'A-TEXT'}).set_placement((500,-800))
msp.add_line((0,-300),(0,0),dxfattribs={'layer':'A-DIM'})
doc.saveas(r'D:\code\github\cad-craft\work\test.dxf')
print('saved')
