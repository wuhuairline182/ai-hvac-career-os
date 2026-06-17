# 给其他 AI 的接入提示词

可以把下面这段直接发给另一个 AI。账号密码让使用者自己输入，不要写进提示词。

```text
你现在要协助我连接并使用智邦 ERP。不要按现代 REST API 直觉猜接口，必须按下面已实测路径走。

基本原则：
1. 先只做只读测试，不要写入、删除、审批。
2. 登录使用 POST /webapi/v3/ov1/login，取 header.session。
3. mobile ASP 列表接口的 session 放 body JSON，不放 cookie/header/URL。
4. 列表接口通常要带 cmdkey=refresh，否则只会返回 UI 骨架。
5. 解析列表时用 body.source.table.cols + body.source.table.rows 自己 zip。
6. 不要用库存汇总判断产品存在，库存汇总只显示有库存的产品。
7. 新增产品前用 产品名称 + 型号 + 公司分类前缀 查重。
8. 写入后必须反查列表/详情确认真的落库。
9. 采购新增 API 不可靠，失败或返回 ok 但不落库时，改生成 ERP 官方 Excel 导入模板。
10. 不要输出 token、session、密码，不要把登录态或 ERP 原始导出提交到 GitHub。

登录：
POST /webapi/v3/ov1/login
Content-Type: application/json; charset=utf-8
body:
{
  "datas": [
    {"id": "user", "val": "txt:账号"},
    {"id": "password", "val": "txt:密码"},
    {"id": "serialnum", "val": "txt:ai-client-001"},
    {"id": "rndcode", "val": ""}
  ]
}

产品列表：
POST /sysa/mobilephone/salesmanage/product/billlist.asp
body:
{
  "session": "header.session",
  "cmdkey": "refresh",
  "datas": [
    {"id": "pagesize", "val": 500},
    {"id": "pageindex", "val": 1}
  ]
}

表格解析：
table = resp["body"]["source"]["table"]
cols = [c["id"] for c in table["cols"]]
for raw in table["rows"]:
    values = raw.get("value", raw) if isinstance(raw, dict) else raw
    row = dict(zip(cols, values))

产品分类：
POST /sysa/mobilephone/systemmanage/product_sort_list.asp?stype=check
body:
{
  "session": "header.session",
  "datas": [{"id": "stype", "val": "check"}]
}

产品新增：
POST /webapi/v3/store/product/add
Header: ZBAPI-Token: header.session

采购单：
采购列表/详情可读，但新增保存不可靠。不要硬写采购新增 API。优先生成采购导入模板。
```

