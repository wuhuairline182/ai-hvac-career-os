# 快速开始

## 1. 登录方式

不要使用 mobile login 的 URL 传参方式。实测可用的是：

```http
POST /webapi/v3/ov1/login
Content-Type: application/json; charset=utf-8
```

```json
{
  "datas": [
    {"id": "user", "val": "txt:账号"},
    {"id": "password", "val": "txt:密码"},
    {"id": "serialnum", "val": "txt:ai-client-001"},
    {"id": "rndcode", "val": ""}
  ]
}
```

成功后取 `header.session`。这个 session 可以给很多 mobile ASP 列表接口使用。

## 2. 产品列表

产品列表不是普通 GET，也不是 `apihelptype=get`。

```http
POST /sysa/mobilephone/salesmanage/product/billlist.asp
Content-Type: application/json; charset=utf-8
```

```json
{
  "session": "header.session",
  "cmdkey": "refresh",
  "datas": [
    {"id": "pagesize", "val": 500},
    {"id": "pageindex", "val": 1}
  ]
}
```

返回数据在：

```text
body.source.table.cols
body.source.table.rows
body.source.table.page
```

解析时把 `cols[*].id` 和每一行的 value zip 起来。

## 3. 本仓库脚本

```powershell
python scripts/export_products.py --limit 20
python scripts/check_product_exists.py --name "产品名称" --model "型号" --company-prefix "目标公司->"
```

