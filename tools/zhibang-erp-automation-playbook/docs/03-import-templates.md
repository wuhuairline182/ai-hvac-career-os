# Excel 导入模板策略

这个 ERP 的规律是：

- 基础资料：API 往往能写，例如产品新增、产品修改。
- 业务单据：API 很不稳定，官方导入模板反而更可靠。

建议策略：

1. 用 API 读取产品库、分类、客户、项目、供应商。
2. 用 API 补齐缺失产品。
3. 合同明细、预购明细、采购单等批量业务单据，生成官方 Excel 导入模板。
4. 用户在 ERP 页面手动导入，ERP 负责校验。
5. 导入失败后，根据失败文件修正模板生成逻辑。

## 采购导入

见 `templates/purchase-import-fields.md` 和 `scripts/make_purchase_import.py`。

生成示例：

```powershell
python scripts/make_purchase_import.py `
  --template "F:\采购导入_默认范例文档.xls" `
  --items examples/purchase_items_sample.csv `
  --output exports\采购导入_示例.xls
```

## 预购导入经验

- 如果 ERP 把空白行也识别成产品，说明模板里残留了范例数据或多余格式区域。
- 只保留真正有产品的行。
- 同一供应商一张表，便于一次导入一张供应商采购需求。
- 采购人员默认值可以在生成时统一填。

## 合同明细导入经验

- 产品分类必须与 ERP 现有分类一致。
- 新项目的一次性材料可以放入项目现场库，但长期标准品应该回归集采库/材料库/设备库。
- ERP 的导入机制通常是“有一条失败全表失败”，所以生成前要做查重和字段校验。

