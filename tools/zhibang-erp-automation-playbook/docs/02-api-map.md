# 已知接口地图

## 鉴权

| 功能 | 方法 | 路径 | 备注 |
| --- | --- | --- | --- |
| 登录 | POST | `/webapi/v3/ov1/login` | 返回 `header.session` |

## mobile ASP 列表

这些接口通常要用：

```json
{
  "session": "...",
  "cmdkey": "refresh",
  "datas": [
    {"id": "pagesize", "val": 500},
    {"id": "pageindex", "val": 1}
  ]
}
```

| 功能 | 路径 | 状态 |
| --- | --- | --- |
| 产品列表 | `/sysa/mobilephone/salesmanage/product/billlist.asp` | 可用 |
| 产品分类树 | `/sysa/mobilephone/systemmanage/product_sort_list.asp?stype=check` | 可用，不需要 `cmdkey=refresh` |
| 客户/供应商列表 | `/sysa/mobilephone/salesmanage/custom/list.asp` | 可用 |
| 项目列表 | `/sysa/mobilephone/salesmanage/chance/list.asp` | 可用 |
| 合同列表 | `/sysa/mobilephone/salesmanage/contract/billlist.asp` | 可用 |
| 采购列表 | `/sysa/mobilephone/storemanage/caigou/list.asp` | 可用 |
| 采购详情 | `/sysa/mobilephone/storemanage/caigou/add.asp?apihelptype=get` | 可用 |

## webapi 写入

| 功能 | 路径 | 鉴权 | 状态 |
| --- | --- | --- | --- |
| 产品新增 | `/webapi/v3/store/product/add` | `ZBAPI-Token: session` | 可用 |
| 产品修改 | `/webapi/v3/store/product/edit` | `ZBAPI-Token: session` | 可用，需谨慎 |
| 采购新增 | `/webapi/v3/ov1/storemanage/caigou/add?apihelptype=save` | 多次尝试不可靠 | 不建议 |

## 产品新增最小字段经验

常用字段：

```json
{
  "Title": "产品名称",
  "Code": "产品编码",
  "Model": "型号",
  "Sort1": 123,
  "CanOutStore": 1,
  "Roles": "3",
  "PriceMode": 3,
  "IncludeTax": 0,
  "Unitjb": 25,
  "ext3": "品牌",
  "PackingPrices": "JSON字符串"
}
```

新增前先用 `产品名称 + 型号 + 公司分类前缀` 查重。新增后反查产品列表，不要只相信接口返回值。

