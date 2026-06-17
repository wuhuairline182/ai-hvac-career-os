from __future__ import annotations

import argparse
import csv
from pathlib import Path

import xlrd
from xlutils.copy import copy as xl_copy


def load_items(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_purchase_import(template: Path, items_csv: Path, output: Path) -> None:
    items = load_items(items_csv)
    if not items:
        raise RuntimeError("items csv is empty")

    book = xlrd.open_workbook(str(template), formatting_info=True)
    wb = xl_copy(book)
    ws = wb.get_sheet(0)

    # Clear example rows but keep the first two template rows.
    for r in range(2, max(8, 2 + len(items))):
        for c in range(35):
            ws.write(r, c, "")

    main = items[0]
    main_columns = {
        0: main.get("purchase_title", ""),
        1: main.get("purchase_code", ""),
        2: main.get("supplier_name", ""),
        3: main.get("supplier_code", ""),
        4: main.get("counterparty", ""),
        5: main.get("currency", "人民币"),
        6: main.get("purchase_category", "常规采购"),
        7: main.get("buyer", ""),
        8: main.get("purchase_date", ""),
        9: main.get("summary", ""),
    }

    for idx, item in enumerate(items):
        row = 2 + idx
        if idx == 0:
            for col, value in main_columns.items():
                ws.write(row, col, value)
        else:
            ws.write(row, 1, "【产品明细】")

        ws.write(row, 10, item.get("product_name", ""))
        ws.write(row, 11, item.get("product_code", ""))
        ws.write(row, 12, item.get("model", ""))
        ws.write(row, 13, item.get("unit", ""))
        ws.write(row, 14, item.get("unit_attr", ""))
        ws.write(row, 15, float(item.get("quantity") or 0))
        ws.write(row, 16, item.get("need_qc", "否"))
        ws.write(row, 17, float(item.get("unit_price") or 0))
        ws.write(row, 18, item.get("include_tax", "否"))
        ws.write(row, 19, float(item.get("tax_rate") or 0))
        ws.write(row, 20, item.get("invoice_type", "不开票"))
        ws.write(row, 21, float(item.get("discount") or 1))
        ws.write(row, 22, float(item.get("line_discount") or 0))
        ws.write(row, 23, item.get("arrival_date", ""))
        ws.write(row, 24, item.get("line_remark", ""))
        ws.write(row, 31, item.get("brand", ""))
        ws.write(row, 32, item.get("stock_in_status", "未入库"))
        ws.write(row, 33, item.get("invoice_receive_status", "自动收票"))
        ws.write(row, 34, item.get("payment_status", "自动生成"))

    output.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(output))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate ERP purchase import xls from a CSV file.")
    parser.add_argument("--template", required=True, type=Path, help="Official ERP purchase import .xls template.")
    parser.add_argument("--items", required=True, type=Path, help="CSV in examples/purchase_items_sample.csv format.")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    write_purchase_import(args.template, args.items, args.output)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()

