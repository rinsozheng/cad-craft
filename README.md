# cad-craft — 美莱食堂平面设计

美莱食堂一、二层空间改造的需求、CAD图纸、预览、设计说明及生成脚本。

## 最新设计

当前版本为 **V1.5**：包房二改为12人Φ1800圆桌（包房一8人Φ1500），靠门西侧保留约925mm通道；男女卫各两个底部蹲位，男卫顶部靠楼梯一侧两个小便斗并设厕所门，女卫不标注小便斗区。沿用黑底高对比DWG和白底PDF。

- [成果入口与版本说明](deliverables/README.md)
- [V1.5 优化说明](deliverables/V1.5/优化说明.md)
- [一楼预览](deliverables/V1.5/预览图/一楼功能分区与家具布置图.png)
- [二楼预览](deliverables/V1.5/预览图/二楼功能分区与家具布置图.png)
- [综合预览](deliverables/V1.5/预览图/一二楼综合设计图.png)
- [深圳福田造价估算](deliverables/V1.5/深圳福田造价估算/美莱食堂V1.5_深圳福田_造价估算.md)
- [需求文档](docs/需求文档.md)

## 目录

| 路径 | 内容 |
|---|---|
| `美莱食堂原始结构图.dwg` | 原始建筑几何基准 |
| `docs/` | 项目需求与修订记录 |
| `deliverables/V1.5/` | 当前DWG、DXF、PDF、PNG预览、统计和校核结果 |
| `deliverables/V1.4/` | 上一版包房及卫生间微调成果 |
| `deliverables/V1.3/` | 配色、尺寸及标识细化成果 |
| `deliverables/V1.2/` | 更早方案成果 |
| `deliverables/` 根目录 | 首版成果和历史报告，最新内容以版本目录为准 |
| `scripts/` | 各版本生成及检查脚本 |
| `work/` | 原图转换、分析、绘图过程脚本和中间文件 |

## 本地生成与检查

环境：Windows、Python 3、CADCraft CLI，以及 `ezdxf`、`shapely`、`pymupdf`。

```powershell
python -m pip install ezdxf shapely pymupdf
python scripts/build_v15.py
python scripts/check_v15.py
```

脚本默认使用 `C:\Program Files\CADCraft\cadcraft-cli.exe`。模型单位为mm，PDF按页面适配输出。生成脚本会刷新对应版本成果目录。

图纸属于空间方案设计；现场尺寸、结构、消防、机电、厨房工艺及图内待确认事项见各版本说明。
