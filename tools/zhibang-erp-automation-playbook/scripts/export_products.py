from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from zhibang_erp import ZhibangERPClient  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Export products through the mobile refresh list API.")
    parser.add_argument("--limit", type=int, default=0, help="Only print/write the first N rows.")
    parser.add_argument("--csv", type=Path, help="Optional output CSV path.")
    parser.add_argument("--company-prefix", default="", help="Optional category prefix filter, e.g. 目标公司->")
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")
    client = ZhibangERPClient.from_env()
    rows = client.product_rows()
    if args.company_prefix:
        rows = [row for row in rows if str(row.get("fenlei", "")).startswith(args.company_prefix)]
    if args.limit:
        rows = rows[: args.limit]

    fields = ["ord", "cpname", "cpbh", "cpxh", "fenlei", "unitjb", "unitname"]
    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        print(f"wrote {len(rows)} rows to {args.csv}")
        return

    for row in rows:
        print(" | ".join(str(row.get(field, "")) for field in fields))


if __name__ == "__main__":
    main()

