p=r"D:\code\github\cad-craft\work\build.py"
s=open(p,encoding="utf-8").read()
# 1F dims
s=s.replace("dim_h(msp, 7420, 12900, 5000, 4800, '5480', 'A-DIM')","dim_h(msp, 7420, 12900, 5200, 4800, '5480', 'A-DIM')")
s=s.replace("    dim_h(msp, 7600, 13180, 15500, 15230, '5580', 'A-DIM')\n","")
s=s.replace("dim_h(msp, 7420, 14180, 200, 600, '6760', 'A-DIM')","dim_h(msp, 7420, 14180, 350, 600, '6760', 'A-DIM')")
s=s.replace("text(msp, '主要尺寸（mm）', 15000, -1800, 300, 'A-DIM', 'center')","text(msp, '主要尺寸（mm）', 10500, -2200, 300, 'A-DIM', 'center')")
# entrance labels
s=s.replace("    text(msp, '员工入口', 9600, 300, 240, 'A-TEXT', 'center')\n    text(msp, '主入口（双开门）', 9600, 100, 200, 'A-NOTE', 'center')","    text(msp, '员工入口', 9600, -150, 220, 'A-TEXT', 'center')\n    text(msp, '主入口（双开门）', 9600, -500, 190, 'A-NOTE', 'center')")
# 2F dims bottom overall and room width
s=s.replace("dim_h(msp, 350, 14140, 11500, 10500, '13790', 'A-DIM')","dim_h(msp, 350, 14140, -900, 0, '13790', 'A-DIM')")
s=s.replace("dim_v(msp, 3560, 10500, 15000, 14140, '6940', 'A-DIM')","dim_v(msp, 3560, 10500, 14700, 14140, '6940', 'A-DIM')")
s=s.replace("dim_v(msp, 0, 10500, 15500, 14140, '10500', 'A-DIM')","dim_v(msp, 0, 10500, 15700, 14140, '10500', 'A-DIM')")
s=s.replace("dim_h(msp, 5500, 8500, 2500, 3440, '3000', 'A-DIM')","dim_h(msp, 5500, 8500, 3700, 3440, '3000', 'A-DIM')")
s=s.replace("text(msp, '主要尺寸（mm）', 12000, -1800, 300, 'A-DIM', 'center')","text(msp, '主要尺寸（mm）', 9000, -2200, 300, 'A-DIM', 'center')")
# 2F title/subtitle
s=s.replace("text(msp, '二层平面图', 7200, 11900, 600, 'A-TEXT', 'center')","text(msp, '二层平面图', 7200, 11750, 600, 'A-TEXT', 'center')")
s=s.replace("text(msp, '尺寸单位：mm  比例：1:100', 7200, 11200, 220, 'A-NOTE', 'center')","text(msp, '尺寸单位：mm  比例：1:100', 7200, 11450, 220, 'A-NOTE', 'center')")
s=s.replace("north_arrow(msp, 15000, 11900)","north_arrow(msp, 15000, 11700)")
# 1F title a bit lower
s=s.replace("text(msp, '一层平面图', 10000, 22950, 600, 'A-TEXT', 'center')","text(msp, '一层平面图', 10000, 22750, 580, 'A-TEXT', 'center')")
s=s.replace("north_arrow(msp, 19000, 22850)","north_arrow(msp, 19000, 22700)")
open(p,"w",encoding="utf-8").write(s)
print("patched")
