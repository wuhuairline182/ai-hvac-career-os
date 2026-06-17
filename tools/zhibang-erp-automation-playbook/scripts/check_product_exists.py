from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from zhibang_erp import ZhibangERPClient  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Check product duplicates by product name + model.")
    parser.add_argument("--name", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--company-prefix", default="")
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")
    client = ZhibangERPClient.from_env()
    matches = client.find_product(args.name, args.model, company_prefix=args.company_prefix)
    if not matches:
        print("not found")
        return
    for row in matches:
        print(
            f"found ord={row.get('ord')} code={row.get('cpbh')} "
            f"name={row.get('cpname')} model={row.get('cpxh')} category={row.get('fenlei')}"
        )


if __name__ == "__main__":
    main()

