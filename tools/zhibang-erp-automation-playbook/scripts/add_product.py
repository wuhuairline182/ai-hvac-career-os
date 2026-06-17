from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from zhibang_erp import ZhibangERPClient  # noqa: E402


def packing_prices(unit_id: int, purchase_price: float) -> str:
    return json.dumps(
        [
            {
                "Bm": 0,
                "Bl": 1,
                "UnitID": unit_id,
                "Txm": "",
                "Price1jy": purchase_price,
                "Price1": purchase_price,
                "Price2jy": 0,
                "Price2": 0,
                "Price3": 0,
                "Sort": 0,
                "CgMainUnit": 1,
                "XlhManage": 0,
                "MainStore": 0,
                "StoreCapacity": 0,
            }
        ],
        ensure_ascii=False,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Safely add one product after duplicate checking.")
    parser.add_argument("--title", required=True, help="Product name")
    parser.add_argument("--code", required=True, help="Product code")
    parser.add_argument("--model", required=True, help="Product model")
    parser.add_argument("--sort-id", required=True, type=int, help="ERP product category Sort1 id")
    parser.add_argument("--unit-id", required=True, type=int, help="ERP base unit id")
    parser.add_argument("--brand", default="")
    parser.add_argument("--purchase-price", type=float, default=0)
    parser.add_argument("--company-prefix", default="", help="Duplicate check category prefix")
    parser.add_argument("--execute", action="store_true", help="Actually call the add API")
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")
    client = ZhibangERPClient.from_env()
    existing = client.find_product(args.title, args.model, company_prefix=args.company_prefix)
    if existing:
        print("duplicate found; not adding")
        for row in existing:
            print(f"ord={row.get('ord')} code={row.get('cpbh')} category={row.get('fenlei')}")
        return

    payload = {
        "Title": args.title,
        "Code": args.code,
        "Model": args.model,
        "Sort1": args.sort_id,
        "CanOutStore": 1,
        "Roles": "3",
        "PriceMode": 3,
        "IncludeTax": 0,
        "Unitjb": args.unit_id,
        "Intro1": "Created by ERP automation playbook.",
        "ext3": args.brand,
        "PackingPrices": packing_prices(args.unit_id, args.purchase_price),
    }

    print(json.dumps({"dry_run": not args.execute, "payload": payload}, ensure_ascii=False, indent=2))
    if not args.execute:
        return

    result = client.add_product(payload)
    print(json.dumps({"api_result": result}, ensure_ascii=False, indent=2))
    verified = client.find_product(args.title, args.model, company_prefix=args.company_prefix)
    print(json.dumps({"verified_count": len(verified), "verified": verified[:3]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

