# 地源热泵报价文件格式补充规则

> 本文件是 `tools/hvac_quote_ground_source_rulebook.md` 的格式补充。若与旧规则冲突，以本文件为准。

## 1. 方案设计书表格字体

所有方案设计书中的表格字体统一为：

```text
字体：宋体
字号：小四，12pt
```

适用范围包括：

- 室内设计参数表
- 负荷确定表
- 末端配置表
- 夏季/冬季设备功率表
- 报价汇总表
- 主机系统造价表
- 地源井造价表
- 末端系统造价表
- 附录业绩表

要求：

- 表头、正文、合计行均使用宋体小四。
- 不要出现同一表格内字体有粗有细、高矮胖瘦不一致的情况。
- 除非用户明确要求，表格正文不要使用小五、五号、9pt 或其它压缩字体。
- Word 表格如果因合并单元格导致字体抽查显示“混合字号”，应使用整表选择区强制应用宋体小四。
- 表格可按页面宽度自适应，但不能为了塞内容把字压小。

## 2. Word COM 操作建议

修改 Word 表格字体时，建议同时做整表 Range 和 Selection 两次设置：

```python
table.Range.Select()
word.Selection.Font.Name = "宋体"
word.Selection.Font.NameFarEast = "宋体"
word.Selection.Font.Size = 12
word.Selection.Font.Bold = 0

table.Range.Font.Name = "宋体"
table.Range.Font.NameFarEast = "宋体"
table.Range.Font.Size = 12
```

合并单元格可能导致逐单元格访问失败，但整表选择区通常可以覆盖。

## 3. 交付前格式核查

交付方案设计书前，至少抽查每个表格的以下位置：

- 第一行第一列
- 第一行第二列
- 第二行第一列
- 最后一行第一列

确认字体均为：

```text
宋体 / 小四 / 12pt
```

如果 Word 返回混合字号，应再次整表刷格式，再打开文档目视确认。
