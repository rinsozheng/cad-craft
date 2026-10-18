"""V1.5 Shenzhen Futian budget estimate. Quantities from the V1.5 design.

Prices are market composite rates for small/medium food-service fit-out in
Futian, Shenzhen (Oct 2026), including labour, auxiliary materials, normal
main materials, machinery, overhead and profit, excluding VAT. They are a
budget estimate, not a tender control price.
"""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'deliverables' / 'V1.5' / '深圳福田造价估算'
OUT.mkdir(parents=True, exist_ok=True)

FLOOR_1 = 224.51
FLOOR_2 = 144.80
TOTAL_AREA = FLOOR_1 + FLOOR_2
FLOOR_TILE = 357.0
LOCAL_CEILING = 70.0
ORIGINAL_CEILING_PAINT = 120.0
ALUMINIUM_CEILING = 20.5
LIGHT_BRICK_WALL = 10.88 * 3.0
WATERPROOF_TILE = LIGHT_BRICK_WALL * 2
GYPSUM_WALL = 13.00 * 3.0
PARTITION_PAINT = 39.0
WALLCLOTH = 86.6
PRIVATE_CEILING = 28.49
PUBLIC_SEATS = 170
PRIVATE_SEATS = 20
LIGHT_FIXTURES = 62
EMERGENCY_FIXTURES = 10

BOQ = [
    ('一、地面工程', [
        ('800×800地砖（含找平、粘结层、勾缝、5%损耗）', '两层公共区、包房、卫生间、厨房、库房', 'm²', FLOOR_TILE, 200,
         '按V1.5两层369.3㎡扣除墙柱及固定设备后约340㎡，另计5%损耗'),
    ]),
    ('二、吊顶工程', [
        ('公共区域局部吊顶（轻钢龙骨矿棉板/硅酸钙板）', '一层打菜/入口、二层屏前/活动区', 'm²', LOCAL_CEILING, 240,
         '局部吊顶约70㎡；其余保留原顶'),
        ('大面积原顶乳胶漆（腻子、底漆、面漆两遍）', '两层公共区及走道', 'm²', ORIGINAL_CEILING_PAINT, 55,
         '约120㎡；含基层处理'),
        ('厨房、库房铝扣板吊顶（600×600，含龙骨收边）', '一层厨房、库房', 'm²', ALUMINIUM_CEILING, 230,
         '厨房15.4㎡+库房5.1㎡'),
        ('包房天花满吊顶（轻钢龙骨石膏板，含乳胶漆）', '二层包房一、包房二', 'm²', PRIVATE_CEILING, 280,
         '包房净面积13.09+15.40㎡'),
    ]),
    ('三、隔墙及墙面工程', [
        ('轻质砖隔墙（100mm，含构造柱/圈梁界面处理）', '一层厨房、库房外围', 'm²', LIGHT_BRICK_WALL, 300,
         '隔墙轴线长约10.88m×3.0m高'),
        ('厨房、库房墙面防水及贴瓷片（双面）', '一层厨房、库房隔墙', 'm²', WATERPROOF_TILE, 190,
         '双面约65.3㎡；含防水基层、瓷砖、勾缝'),
        ('石膏板隔墙（双层12mm+75龙骨+50mm隔音棉）', '二层包房隔墙', 'm²', GYPSUM_WALL, 430,
         '隔墙轴线长约13.0m×3.0m高'),
        ('隔墙乳胶漆（公共侧）', '二层包房隔墙公共侧', 'm²', PARTITION_PAINT, 55,
         '单面约39㎡；包房内侧贴墙布'),
        ('包房墙面贴墙布（基层处理、环保胶、墙布）', '二层包房一、包房二', 'm²', WALLCLOTH, 165,
         '按包房内周长×3.0m扣除门洞约86.6㎡'),
    ]),
    ('四、空调工程', [
        ('全区域多联机空调（室内外机、铜管、冷凝水、保温、风口、控制）', '一层、二层全区域', 'm²', TOTAL_AREA, 480,
         '按369.3㎡；含常规安装，不含电力主干及新风主管'),
    ]),
    ('五、消防改造', [
        ('喷淋、烟感、应急照明、疏散指示、报警联动及调试', '一层、二层全区域', 'm²', TOTAL_AREA, 260,
         '按369.3㎡；不含消防水池/泵房/结构加固'),
    ]),
    ('六、电气照明', [
        ('LED面板灯/筒灯（含安装）', '公共区、厨房、卫生间、包房', '套', LIGHT_FIXTURES, 320,
         '按约62套暂估，最终按照度计算'),
        ('应急照明/疏散指示灯（含安装）', '疏散通道及出口', '套', EMERGENCY_FIXTURES, 220,
         '按10套暂估'),
    ]),
    ('七、厨房设备配套', [
        ('双眼灶/排烟罩（304不锈钢，含低噪风机、短管及灭火装置接口）', '一层厨房', '套', 1, 45000,
         '不含至屋面排烟井/长距离风管'),
        ('蒸饭/主食设备', '一层厨房', '套', 1, 9000, '蒸饭柜及配套'),
        ('冷柜', '一层厨房', '台', 2, 7000, '冷藏/冷冻各1台'),
        ('清洗/切配（双槽水池、操作台、沥水架）', '一层厨房', '套', 1, 12000, '304不锈钢'),
        ('洗消点（预洗、洗碗/消毒、保洁柜）', '一层厨房', '套', 1, 15000, '紧凑型商用配置'),
        ('厨房工作台', '一层厨房', '台', 2, 3500, '304不锈钢'),
        ('设备安装、水电燃气接驳及调试', '一层厨房', '项', 1, 22000,
         '接至现有预留点；不含燃气增容、隔油池、排烟井'),
    ]),
]

MEASURES_RATE = 0.04
OTHER_ITEMS = 40000.0
TAX_RATE = 0.09
CONTINGENCY_RATE = 0.05

def money(v):
    return round(v + 1e-9, 2)

def build_totals(direct_factor=1.0):
    lines = []
    direct = 0.0
    for group, items in BOQ:
        for name, location, unit, qty, rate, note in items:
            q = qty
            r = money(rate * direct_factor)
            amount = money(q * r)
            direct += amount
            lines.append((group, name, location, unit, q, r, amount, note))
    measures = money(direct * MEASURES_RATE)
    subtotal = money(direct + measures + OTHER_ITEMS)
    tax = money(subtotal * TAX_RATE)
    incl_tax = money(subtotal + tax)
    contingency = money(incl_tax * CONTINGENCY_RATE)
    total = money(incl_tax + contingency)
    return {
        'lines': lines, 'direct': money(direct), 'measures': measures,
        'other': OTHER_ITEMS, 'subtotal': subtotal, 'tax': tax,
        'incl_tax': incl_tax, 'contingency': contingency, 'total': total,
        'per_m2': money(total / TOTAL_AREA),
    }

base = build_totals(1.0)
economy = build_totals(0.90)
premium = build_totals(1.15)

# ---------- Excel ----------
wb = Workbook()
ws = wb.active
ws.title = '封面说明'
TITLE_FILL = PatternFill('solid', fgColor='1F4E78')
HEAD_FILL = PatternFill('solid', fgColor='D9EAF7')
WARN_FILL = PatternFill('solid', fgColor='FFF2CC')
TOTAL_FILL = PatternFill('solid', fgColor='E2F0D9')
THIN = Side(style='thin', color='B0B0B0')
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
CURRENCY = '¥#,##0.00'

def title_row(sheet, text, row=1, span=7):
    sheet.merge_cells(start_row=row, start_column=1, end_row=row, end_column=span)
    c = sheet.cell(row=row, column=1, value=text)
    c.font = Font(size=16, bold=True, color='FFFFFF')
    c.fill = TITLE_FILL
    c.alignment = Alignment(horizontal='center', vertical='center')
    sheet.row_dimensions[row].height = 28

def header(sheet, row, values):
    for i, v in enumerate(values, 1):
        c = sheet.cell(row=row, column=i, value=v)
        c.font = Font(bold=True)
        c.fill = HEAD_FILL
        c.border = BORDER
        c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

def widths(sheet, values):
    for i, w in enumerate(values, 1):
        sheet.column_dimensions[get_column_letter(i)].width = w

title_row(ws, '美莱食堂 V1.5 改造工程——深圳福田区造价估算', 1, 4)
rows = [
    ('项目名称', '美莱食堂一、二层空间改造'),
    ('设计版本', 'V1.5（包房二12人、卫生间双蹲位、男卫小便斗及厕所门）'),
    ('项目地点', '深圳市福田区'),
    ('估算日期', '2026年10月18日'),
    ('建筑面积', f'一层 {FLOOR_1:.2f} ㎡ + 二层 {FLOOR_2:.2f} ㎡ = {TOTAL_AREA:.2f} ㎡'),
    ('定价口径', '深圳福田区中小型食堂/餐饮公装市场综合单价；含人工、辅材、常规主材、机具、管理及利润；不含增值税，税金单列'),
    ('价格性质', '方案阶段预算估算，不是政府定额、招标控制价或施工图预算；主材品牌、现场条件、报建要求会影响最终价格'),
    ('标准档估算', f'¥{base["total"]:,.0f}（含税及5%预备费，约 ¥{base["per_m2"]:,.0f}/㎡）'),
    ('建议控制区间', f'经济档约 ¥{economy["total"]:,.0f}；标准档约 ¥{base["total"]:,.0f}；品质档约 ¥{premium["total"]:,.0f}'),
]
r = 3
for k, v in rows:
    ws.cell(r, 1, k).font = Font(bold=True)
    ws.cell(r, 1).fill = HEAD_FILL
    ws.cell(r, 1).border = BORDER
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
    c = ws.cell(r, 2, v)
    c.alignment = Alignment(wrap_text=True, vertical='top')
    c.border = BORDER
    r += 1
widths(ws, [20, 38, 25, 25])

ws2 = wb.create_sheet('工程量计算')
title_row(ws2, '工程量计算书（依据V1.5图纸）', 1, 6)
header(ws2, 2, ['项目', '计算依据/公式', '工程量', '单位', '备注', '图纸依据'])
calc = [
    ('总建筑面积', '224.51 + 144.80', TOTAL_AREA, '㎡', '外墙内表面/图面量取', 'V1.5 几何校核'),
    ('地面地砖', '369.31 × (1-8%) × 1.05', FLOOR_TILE, '㎡', '扣墙柱/固定设备8%，加5%损耗', 'V1.5 平面'),
    ('公共局部吊顶', '一层40 + 二层30', LOCAL_CEILING, '㎡', '打菜/入口/屏前/活动区', 'V1.5 平面'),
    ('原顶乳胶漆', '一层60 + 二层60', ORIGINAL_CEILING_PAINT, '㎡', '公共区未吊顶部分', 'V1.5 平面'),
    ('厨房/库房铝扣板', '15.39 + 5.13', ALUMINIUM_CEILING, '㎡', '厨房、库房', 'V1.5 说明'),
    ('轻质砖隔墙', '10.88 m × 3.0 m', LIGHT_BRICK_WALL, '㎡', '一层厨房/库房外围', 'V1.5 一层新隔墙'),
    ('防水贴瓷片', '32.64 × 2', WATERPROOF_TILE, '㎡', '隔墙双面', 'V1.5 一层新隔墙'),
    ('石膏板隔墙', '13.00 m × 3.0 m', GYPSUM_WALL, '㎡', '二层包房隔墙', 'V1.5 二层新隔墙'),
    ('隔墙乳胶漆', '39.0 × 1', PARTITION_PAINT, '㎡', '公共侧单面', 'V1.5 二层'),
    ('包房墙布', '房间内周长×3.0-门洞', WALLCLOTH, '㎡', '包房一41.6+包房二45.0', 'V1.5 包房'),
    ('包房满吊顶', '13.09 + 15.40', PRIVATE_CEILING, '㎡', '两间包房', 'V1.5 包房'),
    ('空调', '369.31', TOTAL_AREA, '㎡', '全区域', 'V1.5 全楼'),
    ('消防改造', '369.31', TOTAL_AREA, '㎡', '全区域', 'V1.5 全楼'),
    ('LED灯具', '按8㎡/套暂估', LIGHT_FIXTURES, '套', '最终按照度计算', '方案暂估'),
    ('应急/疏散灯', '按出口/走道暂估', EMERGENCY_FIXTURES, '套', '含安装', '方案暂估'),
]
for i, row in enumerate(calc, 3):
    for j, v in enumerate(row, 1):
        c = ws2.cell(i, j, v)
        c.border = BORDER
        c.alignment = Alignment(wrap_text=True, vertical='top')
        if j == 3:
            c.number_format = '#,##0.00'
widths(ws2, [22, 30, 13, 8, 34, 26])

ws3 = wb.create_sheet('分部分项报价')
title_row(ws3, '分部分项工程和单价措施项目清单（标准档）', 1, 8)
header(ws3, 2, ['序号', '项目名称', '部位/说明', '单位', '工程量', '综合单价(元)', '合价(元)', '备注'])
row = 3
no = 1
current_group = None
for group, name, location, unit, qty, rate, amount, note in base['lines']:
    if group != current_group:
        ws3.merge_cells(start_row=row, start_column=1, end_row=row, end_column=8)
        c = ws3.cell(row, 1, group)
        c.font = Font(bold=True, color='1F4E78')
        c.fill = HEAD_FILL
        c.border = BORDER
        row += 1
        current_group = group
    values = [no, name, location, unit, qty, rate, amount, note]
    for j, v in enumerate(values, 1):
        c = ws3.cell(row, j, v)
        c.border = BORDER
        c.alignment = Alignment(wrap_text=True, vertical='top')
        if j in (5,):
            c.number_format = '#,##0.00'
        if j in (6, 7):
            c.number_format = CURRENCY
    row += 1
    no += 1
# Direct total
ws3.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
c = ws3.cell(row, 1, '分部分项合计（不含税）')
c.font = Font(bold=True)
c.fill = TOTAL_FILL
c.border = BORDER
c.alignment = Alignment(horizontal='right')
c = ws3.cell(row, 7, base['direct'])
c.font = Font(bold=True)
c.fill = TOTAL_FILL
c.border = BORDER
c.number_format = CURRENCY
ws3.cell(row, 8, '').border = BORDER
widths(ws3, [7, 38, 32, 8, 11, 14, 15, 36])

ws4 = wb.create_sheet('费用汇总')
title_row(ws4, '费用汇总与三档估算', 1, 6)
header(ws4, 2, ['费用项目', '计算式', '标准档(元)', '经济档(元)', '品质档(元)', '说明'])
summary_rows = [
    ('分部分项工程费', '清单合价', base['direct'], economy['direct'], premium['direct'], '含人工、辅材、常规主材、机具、管理及利润'),
    ('措施项目费', '分部分项×4%', base['measures'], economy['measures'], premium['measures'], '安全文明、成品保护、临时设施、垃圾清运等'),
    ('其他项目费', '设计/报建/检测/保洁', base['other'], economy['other'], premium['other'], '设计深化、消防报验检测、开荒保洁等'),
    ('税前小计', '前三项合计', base['subtotal'], economy['subtotal'], premium['subtotal'], ''),
    ('增值税', '税前×9%', base['tax'], economy['tax'], premium['tax'], '一般计税'),
    ('含税工程费', '税前+增值税', base['incl_tax'], economy['incl_tax'], premium['incl_tax'], ''),
    ('预备费', '含税工程费×5%', base['contingency'], economy['contingency'], premium['contingency'], '方案阶段不可预见费'),
    ('估算总额', '含税工程费+预备费', base['total'], economy['total'], premium['total'], '建议按标准档控制'),
    ('单方造价', '总额÷369.31㎡', base['per_m2'], economy['per_m2'], premium['per_m2'], '元/㎡'),
]
for i, rowvals in enumerate(summary_rows, 3):
    for j, v in enumerate(rowvals, 1):
        c = ws4.cell(i, j, v)
        c.border = BORDER
        c.alignment = Alignment(wrap_text=True, vertical='top')
        if j in (3, 4, 5) and isinstance(v, (int, float)):
            c.number_format = CURRENCY if rowvals[0] != '单方造价' else '¥#,##0.00'
    if rowvals[0] == '估算总额':
        for j in range(1, 7):
            ws4.cell(i, j).fill = TOTAL_FILL
            ws4.cell(i, j).font = Font(bold=True)
widths(ws4, [22, 24, 16, 16, 16, 40])
ws4.cell(13, 1, '说明：经济档按标准档综合单价×0.90，品质档×1.15；其他项目费三档均按4万元暂估。三档均含9%增值税和5%预备费。')
ws4.merge_cells(start_row=13, start_column=1, end_row=13, end_column=6)
ws4.cell(13, 1).font = Font(italic=True, color='C00000')
ws4.cell(13, 1).fill = WARN_FILL
ws4.cell(13, 1).alignment = Alignment(wrap_text=True)

ws5 = wb.create_sheet('主材与定价假设')
title_row(ws5, '主材档次、综合单价口径与关键假设', 1, 4)
header(ws5, 2, ['项目', '采用标准', '综合单价口径', '风险/调整'])
assumptions = [
    ('地面地砖', '800×800中档防滑砖，国产品牌', '含找平、粘结、勾缝、损耗', '大板/进口品牌上浮30%-80%'),
    ('公共局部吊顶', '轻钢龙骨+矿棉板/硅酸钙板', '含龙骨、面层、收边', '造型/灯槽另计'),
    ('原顶乳胶漆', '环保腻子+底漆+两遍面漆', '含基层处理', '原顶空鼓/开裂修补另计'),
    ('厨房/库房铝扣板', '600×600，0.8mm', '含龙骨、收边、开孔', '灯具/风口开孔另计'),
    ('轻质砖隔墙', '100mm轻质砖', '含砌筑、构造柱界面、抹灰', '结构加固另计'),
    ('厨房墙面瓷片', '300×600中档防水砖', '含防水、粘结、勾缝', '全高贴砖按实际高度调整'),
    ('石膏板隔墙', '双层12mm+75龙骨+50mm隔音棉', '含龙骨、隔音棉、双面封板', '防火/隔声升级另计'),
    ('墙布', '中档无纺布墙布', '含基层、环保胶、铺贴', '进口/定制图案上浮'),
    ('空调', '国产/合资多联机，常规能效', '含室内外机、铜管、冷凝水、风口、控制', '品牌升级/新风/厨房补风另计'),
    ('消防', '本地合规消防改造', '含喷淋、烟感、应急、报警联动、调试', '水池/泵房/结构加固另计'),
    ('厨房设备', '304不锈钢商用设备', '含设备、安装、接至预留点', '燃气增容、隔油池、长距离排烟另计'),
    ('灯具', 'LED面板灯/筒灯，中档', '含灯具及安装', '智能控制/调光另计'),
]
for i, rowvals in enumerate(assumptions, 3):
    for j, v in enumerate(rowvals, 1):
        c = ws5.cell(i, j, v)
        c.border = BORDER
        c.alignment = Alignment(wrap_text=True, vertical='top')
widths(ws5, [20, 34, 38, 34])

ws6 = wb.create_sheet('不含项与风险')
title_row(ws6, '未包含项目、排除项与主要风险', 1, 3)
header(ws6, 2, ['类别', '内容', '处理建议'])
exclusions = [
    ('未包含', '餐桌椅、包房家具、显示屏、标识标牌、绿植、软装', '另行采购/询价'),
    ('未包含', '厨房排烟井、隔油池、燃气增容、给排水/电气主干管、消防水池/泵房', '按现场条件专项设计'),
    ('未包含', '结构加固、承重墙开洞、外立面改造、屋面防水', '结构专业复核后另计'),
    ('未包含', '新风/排风主干管、厨房补风、防排烟系统', '暖通专业深化'),
    ('未包含', '政府规费、物业管理押金、消防水池/泵房/结构加固', '按福田区实际报建流程及现场条件计'),
    ('未包含', '门及五金（包房推拉门、厨房工作门等）', '按门型/材质另询价，建议预留1.5~2.5万元'),
    ('未包含', '厨房、卫生间地面防水及暗地漏', '如原地面无防水，建议预留1.5~2.5万元'),
    ('未包含', '原隔墙拆除、垃圾外运、成品保护升级', '措施费仅含场内清运，拆除另计'),
    ('未包含', '踢脚线、收口、窗帘、五金配件', '按最终做法补充'),
    ('未包含', '家具、餐具、厨房小件、员工培训', '运营采购'),
    ('风险', '原图无尺寸标注、无机电/消防图，现场实测差异可能导致工程量变化', '施工前复测，按实调整'),
    ('风险', '厨房15.4㎡紧凑，设备品牌/排烟路径可能增加造价', '厨房顾问确认后再锁定'),
    ('风险', '包房二12人桌西侧通道925mm，东侧仅325mm；若需双侧通行需减小桌径或调整门位', '现场放线确认'),
    ('风险', '消防改造若需新增喷淋主管/水池泵房，可能增加10万以上', '消防专业现场评估'),
    ('风险', '空调若采用全新风/厨房专用空调，造价上浮', '暖通专业确认'),
]
for i, rowvals in enumerate(exclusions, 3):
    for j, v in enumerate(rowvals, 1):
        c = ws6.cell(i, j, v)
        c.border = BORDER
        c.alignment = Alignment(wrap_text=True, vertical='top')
widths(ws6, [12, 62, 36])

ws7 = wb.create_sheet('建议增项与单价依据')
title_row(ws7, '建议增项、不可预见项与市场单价参考', 1, 5)
header(ws7, 2, ['类型', '项目', '低值(元)', '高值(元)', '说明'])
addons = [
    ('建议增项', '门及五金（包房推拉门、厨房工作门）', 15000, 25000, '按门型/材质/五金品牌'),
    ('建议增项', '厨房、卫生间地面防水及暗地漏', 15000, 25000, '原地面无防水时必须增加'),
    ('建议增项', '原隔墙拆除及垃圾外运', 10000, 20000, '按拆除量和楼层运输'),
    ('建议增项', '厨房排烟井/隔油池/补风', 30000, 80000, '按现场土建及环保要求'),
    ('建议增项', '消防水池/泵房/结构加固', 100000, 250000, '如消防评估要求新增'),
    ('建议增项', '家具、显示屏、标识、餐具', 0, 0, '按运营采购另计'),
]
r=3
for item in addons:
    for j,v in enumerate(item,1):
        c=ws7.cell(r,j,v); c.border=BORDER; c.alignment=Alignment(wrap_text=True,vertical='top')
        if j in (3,4) and isinstance(v,(int,float)): c.number_format='¥#,##0'
    r+=1
r+=1
ws7.merge_cells(start_row=r,start_column=1,end_row=r,end_column=5)
c=ws7.cell(r,1,'市场综合单价参考区间（深圳福田，2026年10月，含人工辅材常规主材，不含税）')
c.font=Font(bold=True); c.fill=HEAD_FILL; c.border=BORDER
r+=1
header(ws7,r,['项目','低值','高值','本次采用','说明'])
rate_refs=[
    ('800×800地砖','元/㎡',180,260,200,'中档防滑砖，含找平/粘结/勾缝'),
    ('公共局部吊顶','元/㎡',200,280,240,'轻钢龙骨矿棉板/硅酸钙板'),
    ('石膏板隔墙+隔音棉','元/㎡',380,500,430,'双层12mm+75龙骨+50棉'),
    ('厨房/库房铝扣板','元/㎡',200,280,230,'600×600，含龙骨收边'),
    ('包房墙布','元/㎡',130,200,165,'中档无纺布'),
    ('多联机空调','元/㎡',420,600,480,'含铜管/冷凝水/风口/控制'),
    ('消防改造','元/㎡',220,320,260,'喷淋/烟感/应急/联动'),
    ('厨房设备配套','万元/项',10,15,12.4,'按清单设备及安装'),
    ('LED灯具','元/套',260,420,320,'含安装'),
]
r+=1
for name,unit,lo,hi,adopted,note in rate_refs:
    vals=[name+f'（{unit}）',lo,hi,adopted,note]
    for j,v in enumerate(vals,1):
        c=ws7.cell(r,j,v); c.border=BORDER; c.alignment=Alignment(wrap_text=True,vertical='top')
    r+=1
widths(ws7,[28,16,16,16,48])

# Save
xlsx = OUT / '美莱食堂V1.5_深圳福田_造价估算.xlsx'
wb.save(xlsx)

# ---------- CSV ----------
import csv
csv_path = OUT / '美莱食堂V1.5_深圳福田_分部分项.csv'
with csv_path.open('w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['序号', '分部', '项目名称', '部位/说明', '单位', '工程量', '综合单价(元)', '合价(元)', '备注'])
    for i, (group, name, location, unit, qty, rate, amount, note) in enumerate(base['lines'], 1):
        w.writerow([i, group, name, location, unit, qty, rate, amount, note])
    w.writerow(['', '', '分部分项合计', '', '', '', '', base['direct'], '不含税'])
    w.writerow(['', '', '措施项目费4%', '', '', '', '', base['measures'], ''])
    w.writerow(['', '', '其他项目费', '', '', '', '', base['other'], '设计/报建/检测/保洁'])
    w.writerow(['', '', '税前小计', '', '', '', '', base['subtotal'], ''])
    w.writerow(['', '', '增值税9%', '', '', '', '', base['tax'], ''])
    w.writerow(['', '', '含税工程费', '', '', '', '', base['incl_tax'], ''])
    w.writerow(['', '', '预备费5%', '', '', '', '', base['contingency'], ''])
    w.writerow(['', '', '估算总额', '', '', '', '', base['total'], '标准档'])

# ---------- Markdown ----------
md = f'''# 美莱食堂 V1.5 改造工程——深圳福田区造价估算

**估算日期：** 2026-10-18  
**设计版本：** V1.5  
**项目地点：** 深圳市福田区  
**建筑面积：** 一层 {FLOOR_1:.2f} ㎡ + 二层 {FLOOR_2:.2f} ㎡ = **{TOTAL_AREA:.2f} ㎡**

## 1. 估算结论

| 档次 | 估算总额（含税、含5%预备费） | 单方造价 |
|---|---:|---:|
| 经济档（标准档单价×0.90） | **¥{economy['total']:,.0f}** | ¥{economy['per_m2']:,.0f}/㎡ |
| **标准档（推荐）** | **¥{base['total']:,.0f}** | **¥{base['per_m2']:,.0f}/㎡** |
| 品质档（标准档单价×1.15） | **¥{premium['total']:,.0f}** | ¥{premium['per_m2']:,.0f}/㎡ |

**建议：** 按标准档 **约 {base['total']/10000:.0f} 万元** 控制预算，另留 5%～10% 风险金；若空调、消防或厨房设备品牌升级，按品质档 **约 {premium['total']/10000:.0f} 万元** 准备。

> 本估算为方案阶段市场综合单价预算，不是政府定额、招标控制价或施工图预算。价格按深圳福田区2026年10月中小型食堂/餐饮公装水平假设，含人工、辅材、常规主材、机具、管理及利润，不含增值税（税金单列）。

## 2. 分部分项汇总

| 分部 | 合价（元） | 占比 |
|---|---:|---:|
'''
for group in [g for g, _ in BOQ]:
    amount = sum(line[6] for line in base['lines'] if line[0] == group)
    md += f'| {group} | {amount:,.0f} | {amount/base["direct"]*100:.1f}% |\n'
md += f'''| **分部分项合计** | **{base['direct']:,.0f}** | **100%** |

## 3. 详细清单

| 序号 | 项目 | 部位 | 单位 | 工程量 | 综合单价 | 合价 |
|---:|---|---|---|---:|---:|---:|
'''
for i, (group, name, location, unit, qty, rate, amount, note) in enumerate(base['lines'], 1):
    md += f'| {i} | {name} | {location} | {unit} | {qty:,.2f} | {rate:,.0f} | {amount:,.0f} |\n'
md += f'''
## 4. 费用汇总

| 费用项目 | 计算式 | 金额（元） |
|---|---|---:|
| 分部分项工程费 | 清单合价 | {base['direct']:,.0f} |
| 措施项目费 | 分部分项×4% | {base['measures']:,.0f} |
| 其他项目费 | 设计/报建/检测/保洁 | {base['other']:,.0f} |
| 税前小计 | 前三项合计 | {base['subtotal']:,.0f} |
| 增值税 | 税前×9% | {base['tax']:,.0f} |
| 含税工程费 | 税前+增值税 | {base['incl_tax']:,.0f} |
| 预备费 | 含税×5% | {base['contingency']:,.0f} |
| **估算总额** | 含税+预备费 | **{base['total']:,.0f}** |

## 5. 工程量依据

- 总建筑面积：V1.5 图面量取 224.51 + 144.80 = 369.31 ㎡；
- 一层新隔墙轴线长约 10.88 m，按 3.0 m 高计 32.64 ㎡，双面防水贴瓷片 65.28 ㎡；
- 二层新隔墙轴线长约 13.00 m，按 3.0 m 高计 39.00 ㎡；
- 包房墙布：包房一内周长×3.0 扣门洞约 41.6 ㎡，包房二约 45.0 ㎡，合计 86.6 ㎡；
- 包房满吊顶：13.09 + 15.40 = 28.49 ㎡；
- 厨房、库房铝扣板：15.39 + 5.13 = 20.52 ㎡；
- 地面地砖：总面积扣墙柱/固定设备 8%，加 5% 损耗，约 357 ㎡；
- 空调、消防按两层全区域 369.31 ㎡；
- 灯具按约 8 ㎡/套暂估 62 套，另应急/疏散 10 套。

## 6. 定价口径与主材假设

- 地面：800×800 中档防滑砖，含找平、粘结、勾缝；
- 公共局部吊顶：轻钢龙骨矿棉板/硅酸钙板；
- 原顶乳胶漆：腻子+底漆+两遍面漆；
- 厨房/库房：600×600 铝扣板；
- 一层厨房/库房隔墙：100mm 轻质砖，双面防水贴瓷片；
- 二层包房隔墙：双层12mm石膏板+75龙骨+50mm隔音棉；
- 包房墙面：中档无纺布墙布；
- 空调：国产/合资多联机，含铜管、冷凝水、风口、控制；
- 消防：喷淋、烟感、应急照明、疏散指示、报警联动及调试；
- 厨房设备：304不锈钢商用设备，含安装及接至预留点；
- 灯具：LED 面板灯/筒灯中档。

## 7. 未包含项（重要）

- 餐桌椅、包房家具、显示屏、标识标牌、软装；
- 厨房排烟井、隔油池、燃气增容、给排水/电气主干管、消防水池/泵房；
- 结构加固、承重墙开洞、外立面、屋面防水；
- 新风/排风主干管、厨房补风、防排烟系统；
- 消防报建/验收代办、检测费、物业押金；
- 餐具、厨房小件、员工培训。

## 8. 主要风险

1. 原图无尺寸标注和机电/消防图，现场实测差异可能改变工程量；
2. 厨房仅约15.4㎡，设备品牌和排烟路径可能增加造价；
3. 包房二12人桌西侧通道约925mm，东侧仅约325mm；如要求双侧通行，需减小桌径或调整门位；
4. 消防若需新增喷淋主管/水池泵房，可能增加10万元以上；
5. 空调若采用全新风或厨房专用空调，造价上浮。

## 9. 建议增项与价格区间

以下项目未计入标准档，但实际改造中大概率发生，建议在预算中预留：

| 建议增项 | 低值（元） | 高值（元） | 说明 |
|---|---:|---:|---|
| 门及五金（包房推拉门、厨房工作门） | 15,000 | 25,000 | 按门型、材质、五金品牌 |
| 厨房、卫生间地面防水及暗地漏 | 15,000 | 25,000 | 原地面无防水时必须增加 |
| 原隔墙拆除及垃圾外运 | 10,000 | 20,000 | 按拆除量和楼层运输 |
| 厨房排烟井/隔油池/补风 | 30,000 | 80,000 | 按现场土建及环保要求 |
| 消防水池/泵房/结构加固 | 100,000 | 250,000 | 如消防评估要求新增 |
| 家具、显示屏、标识、餐具 | 另计 | 另计 | 运营采购 |

**单价参考区间（深圳福田，2026年10月，含人工辅材常规主材，不含税）：**

| 项目 | 低值 | 高值 | 本次采用 |
|---|---:|---:|---:|
| 800×800地砖 | 180元/㎡ | 260元/㎡ | 200元/㎡ |
| 公共局部吊顶 | 200元/㎡ | 280元/㎡ | 240元/㎡ |
| 石膏板隔墙+隔音棉 | 380元/㎡ | 500元/㎡ | 430元/㎡ |
| 厨房/库房铝扣板 | 200元/㎡ | 280元/㎡ | 230元/㎡ |
| 包房墙布 | 130元/㎡ | 200元/㎡ | 165元/㎡ |
| 多联机空调 | 420元/㎡ | 600元/㎡ | 480元/㎡ |
| 消防改造 | 220元/㎡ | 320元/㎡ | 260元/㎡ |
| 厨房设备配套 | 10万元/项 | 15万元/项 | 12.4万元/项 |
| LED灯具 | 260元/套 | 420元/套 | 320元/套 |

## 10. 文件

- `美莱食堂V1.5_深圳福田_造价估算.xlsx`：封面、工程量、分部分项、费用汇总、主材假设、不含项；
- `美莱食堂V1.5_深圳福田_分部分项.csv`：可导入Excel的清单。
'''
(OUT / '美莱食堂V1.5_深圳福田_造价估算.md').write_text(md, encoding='utf-8')

print(f'''标准档: 分部分项 {base['direct']:,.0f} / 税前 {base['subtotal']:,.0f} / 含税 {base['incl_tax']:,.0f} / 总额 {base['total']:,.0f} / {base['per_m2']:,.0f} 元每平米
经济档: {economy['total']:,.0f} / 品质档: {premium['total']:,.0f}
输出: {OUT}''')
