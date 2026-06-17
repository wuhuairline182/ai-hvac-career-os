# Zhibang ERP Automation Playbook

这是一个给 AI/脚本接入智邦 ERP 用的实战手册和代码包。

它沉淀的是已经实测过的路径：哪些 API 真能用，哪些看起来能用但会坑，哪些业务单据应该改走 Excel 导入模板。

## 核心结论

- 登录使用 `/webapi/v3/ov1/login`，取返回的 `header.session`。
- 产品、项目、合同、采购等很多 ASP 列表接口要用 `cmdkey=refresh`，否则常常只返回 UI 骨架。
- mobile 列表数据在 `body.source.table.cols` 和 `body.source.table.rows`，需要自己 `zip(cols, row)`。
- 产品新增接口 `/webapi/v3/store/product/add` 可用，写入后必须反查产品列表确认。
- 采购单新增 API 不稳定：可能报 `bill.AddTool(...)`，也可能返回 `ok` 但不落库。
- 采购、预购、合同明细等批量业务单据，优先用 ERP 官方 Excel 导入模板。
- 不要用库存汇总判断产品是否存在，库存汇总只返回有库存的产品。

## 目录

- `docs/01-quickstart.md`：最快跑通产品列表。
- `docs/02-api-map.md`：已知可用接口和接口形态。
- `docs/03-import-templates.md`：Excel 导入模板规则。
- `docs/04-troubleshooting.md`：踩坑与排错。
- `docs/05-security.md`：账号、session、业务数据安全边界。
- `src/zhibang_erp/`：可复用 Python 客户端。
- `scripts/`：命令行工具示例。
- `templates/`：导入模板字段说明。
- `examples/`：脱敏样例数据。

## 安装

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

编辑 `.env`：

```text
ERP_BASE_URL=http://your-erp-host:6088
ERP_USER=你的账号
ERP_PASSWORD=你的密码
ERP_SERIAL=ai-client-001
```

## 快速测试

```powershell
python scripts/export_products.py --limit 20
```

如果成功，会输出前 20 个产品的名称、编号、型号、分类。

## 安全提醒

不要提交 `.env`、session 文件、验证码图片、ERP 原始导出、客户合同、采购明细、报销单、供应商联系人等敏感内容。这个仓库只应该存放代码、方法和脱敏样例。

