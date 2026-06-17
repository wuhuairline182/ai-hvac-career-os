# 排坑手册

## 只返回 UI 骨架，不返回数据

原因：用了 `apihelptype=get` 或普通页面初始化接口。

解决：列表类接口改用：

```json
{"session": "...", "cmdkey": "refresh", "datas": [{"id": "pagesize", "val": 500}, {"id": "pageindex", "val": 1}]}
```

## 会话过期

常见原因：

- 用了 mobile login，而不是 `/webapi/v3/ov1/login`。
- session 放错位置。
- session 已过期。

实测路径：

1. POST `/webapi/v3/ov1/login`。
2. 取 `header.session`。
3. mobile ASP 列表接口把 session 放 body JSON 里。

不要把 session 放 cookie/header/URL 参数里乱试。

## 产品列表查不到，但 ERP 页面能看到

不要用库存汇总。库存汇总只显示有库存的产品。

要用：

```text
/sysa/mobilephone/salesmanage/product/billlist.asp
```

并且带 `cmdkey=refresh`。

## rows 解析为空

检查是否从 `body.source.table` 取值。这个 ERP 的表格返回不是普通 `data.list`。

`rows` 有时是数组，有时是对象。代码要兼容。

## 中文乱码

请求和响应都按 UTF-8 处理：

```python
response.encoding = "utf-8"
json.loads(response.text, strict=False)
```

Windows PowerShell 对中文路径/脚本内中文有时会转码异常。复杂脚本建议写入 `.py` 文件运行，不要在命令行里拼超长中文。

## 采购新增接口失败

已实测多种方式：

- mobile `__sys_dosave`
- listview 对象/字符串两种格式
- `apihelptype=save`
- `cmdkey=save`
- webapi `ov1/storemanage/caigou/add?apihelptype=save`

问题：

- 报 `缺少对象: 'bill.AddTool(...)'`
- 或返回 `ok`，但反查采购列表没有落库

结论：采购新增不要硬走 API，改生成官方采购导入模板。

## 写入成功不等于真的成功

所有写入都必须反查：

- 新增产品后，反查产品列表。
- 尝试采购单后，按采购编号反查采购列表。
- 生成 Excel 后，读回文件确认行数和字段。

