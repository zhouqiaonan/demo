# 物流服务规则 — 数据导入快速上手

## 需要用到的两个文件

| 文件 | 说明 |
|---|---|
| `..._routed_..._deduped_....csv` | **主规则表。** 每行对应一条唯一的物流路由规则。主键：`sale_express_rules_id`。重量/尺寸等区间字段（`gross_weight`、`max_length` 等）使用 `GT_`/`GTE_`/`LT_`/`LTE_`/`@` 格式，按常规方式转换为 PostgreSQL range 类型即可。 |
| `..._routed_..._countries_....csv` | **目的地国家关联表。** 仅含两列：`sale_express_rules_id`（外键，指向主规则表）和 `country`（ISO 两位国家代码）。每条规则与每个目的地国家各占一行。 |

主规则表中不含 `country` 字段——一对多关系完全通过关联表来表达。

## 物流服务外键

请使用 `hangzhou_carrierservice_id` 作为外键，关联杭州数据库中的物流服务表。

字段 `bs_express_service_id` 中存储的是从旧系统保留下来的可读标签（格式为 `express>service>show_name`），仅用于数据溯源。**该字段无需导入生产系统**，在导入前或导入过程中直接忽略即可。

## 导入脚本需处理的已知问题

- 关联表中有 **1 行**的 `country` 字段为空，请作为 NULL 处理或直接跳过。
- **ID 100**（`SHAOKE-FR / GLS`）为占位符，对应的物流服务记录尚未在杭州数据库中创建，请跳过或单独处理。
- `ctime`/`mtime` 字段值为 `0` 的，应视为 NULL 处理。

## 重新生成文件的步骤（如需从头执行）

```bash
python3 carrierservice_rules_converter.py            # 将 XLSX 转换为 CSV
# 手动填写 hangzhou_carrierserviceid_conversion.csv 中的杭州物流服务 ID
python3 carrierservice_rules_converter.py --merge
python3 carrierservice_rules_converter.py --fixrouting
python3 carrierservice_rules_converter.py --countrycsv
```

完整文档请参阅 `README.md`。
