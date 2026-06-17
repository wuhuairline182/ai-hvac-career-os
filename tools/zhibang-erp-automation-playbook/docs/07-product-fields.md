# 产品字段速查

## 读取产品列表常见字段

产品列表来自：

```text
/sysa/mobilephone/salesmanage/product/billlist.asp
```

常见字段：

| 字段 | 含义 |
| --- | --- |
| `ord` | 产品内部 ID |
| `cpname` | 产品名称 |
| `cpbh` | 产品编号 |
| `cpxh` | 产品型号 |
| `fenlei` | 分类路径 |
| `unitjb` | 基本单位 ID |
| `unitname` | 基本单位名称 |
| `units` | 单位映射 JSON 字符串 |

## 新增产品常用字段

| 字段 | 含义 | 经验 |
| --- | --- | --- |
| `Title` | 产品名称 | 必填 |
| `Code` | 产品编号 | 必填，自己生成时保持唯一 |
| `Model` | 型号 | 用于去重 |
| `Sort1` | 产品分类 ID | 从分类树获取 |
| `CanOutStore` | 可出库 | 常用 `1` |
| `Roles` | 产品角色 | 外购件常用 `"3"` |
| `PriceMode` | 计价方式 | 移动加权平均法常用 `3` |
| `IncludeTax` | 是否含税 | 不含税 `0`，含税 `1` |
| `Unitjb` | 基本单位 ID | 从产品单位或已有产品中取 |
| `ext3` | 品牌 | 可选 |
| `PackingPrices` | 价格策略 JSON 字符串 | 不是数组对象本身，而是 JSON 字符串 |

## 去重规则

推荐最小规则：

```text
公司分类前缀 + 产品名称 + 型号
```

例如只处理目标公司：

```text
目标公司->
```

不要只按名称去重，也不要只按产品编号去重。

