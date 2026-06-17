from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass
from typing import Any, Iterable

import requests


def datas(**values: Any) -> list[dict[str, Any]]:
    return [{"id": key, "val": value} for key, value in values.items()]


def norm(value: Any) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\u3000", " ")
    return re.sub(r"\s+", " ", text).strip()


def parse_json_map(value: Any) -> dict[str, str]:
    if not value:
        return {}
    if isinstance(value, dict):
        return {str(k): str(v) for k, v in value.items()}
    try:
        obj = json.loads(str(value))
    except Exception:
        return {}
    return {str(k): str(v) for k, v in obj.items()} if isinstance(obj, dict) else {}


@dataclass
class TableResult:
    path: str
    cols: list[str]
    rows: list[dict[str, Any]]
    pages: list[dict[str, Any]]


class ZhibangERPClient:
    """Small client for Zhibang ERP's mixed webapi + mobile ASP interface."""

    def __init__(self, base_url: str, username: str, password: str, serial: str = "ai-client") -> None:
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.serial = serial
        self.session: str | None = None

    @classmethod
    def from_env(cls) -> "ZhibangERPClient":
        base_url = os.environ["ERP_BASE_URL"]
        username = os.environ["ERP_USER"]
        password = os.environ["ERP_PASSWORD"]
        serial = os.environ.get("ERP_SERIAL", "ai-client")
        return cls(base_url, username, password, serial)

    def post_json(
        self,
        path: str,
        payload: dict[str, Any],
        *,
        token: str | None = None,
        timeout: int = 60,
    ) -> dict[str, Any]:
        headers = {"Content-Type": "application/json; charset=utf-8"}
        if token:
            headers["ZBAPI-Token"] = token
        response = requests.post(self.base_url + path, json=payload, headers=headers, timeout=timeout)
        response.encoding = "utf-8"
        text = response.text
        if not text.strip():
            return {}
        try:
            return json.loads(text, strict=False)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Could not parse JSON from {path}: {text[:500]}") from exc

    def login(self) -> str:
        result = self.post_json(
            "/webapi/v3/ov1/login",
            {
                "datas": [
                    {"id": "user", "val": f"txt:{self.username}"},
                    {"id": "password", "val": f"txt:{self.password}"},
                    {"id": "serialnum", "val": f"txt:{self.serial}"},
                    {"id": "rndcode", "val": ""},
                ]
            },
        )
        header = result.get("header", {})
        session = header.get("session")
        if header.get("status") != 0 or not session:
            raise RuntimeError(f"ERP login failed: {header}")
        self.session = str(session)
        return self.session

    def require_session(self) -> str:
        if not self.session:
            return self.login()
        return self.session

    def rows_from_mobile_table(self, response: dict[str, Any]) -> tuple[list[str], list[dict[str, Any]], dict[str, Any]]:
        table = response.get("body", {}).get("source", {}).get("table", {})
        cols = [col.get("id") for col in table.get("cols", [])]
        raw_rows = table.get("rows", []) or []
        if isinstance(raw_rows, dict):
            raw_rows = [raw_rows]

        rows: list[dict[str, Any]] = []
        for raw in raw_rows:
            values = raw.get("value", []) if isinstance(raw, dict) else raw
            row = dict(zip(cols, values))
            if isinstance(raw, dict):
                row["_row_ord"] = raw.get("ord") or raw.get("id")
            rows.append(row)
        return cols, rows, table.get("page", {}) or {}

    def fetch_mobile_list(
        self,
        path: str,
        *,
        pagesize: int = 500,
        max_pages: int = 80,
        extra_datas: Iterable[dict[str, Any]] | None = None,
    ) -> TableResult:
        session = self.require_session()
        all_rows: list[dict[str, Any]] = []
        first_cols: list[str] = []
        pages: list[dict[str, Any]] = []

        for pageindex in range(1, max_pages + 1):
            payload_datas = datas(pagesize=pagesize, pageindex=pageindex)
            if extra_datas:
                payload_datas.extend(extra_datas)
            response = self.post_json(
                path,
                {"session": session, "cmdkey": "refresh", "datas": payload_datas},
            )
            cols, rows, page = self.rows_from_mobile_table(response)
            if pageindex == 1:
                first_cols = cols
            all_rows.extend(rows)
            pages.append(page)
            pagecount = int(page.get("pagecount") or pageindex) if isinstance(page, dict) else pageindex
            if not rows or pageindex >= pagecount:
                break
            time.sleep(0.05)

        return TableResult(path=path, cols=first_cols, rows=all_rows, pages=pages)

    def product_rows(self) -> list[dict[str, Any]]:
        return self.fetch_mobile_list("/sysa/mobilephone/salesmanage/product/billlist.asp").rows

    def customer_rows(self) -> list[dict[str, Any]]:
        return self.fetch_mobile_list("/sysa/mobilephone/salesmanage/custom/list.asp").rows

    def project_rows(self) -> list[dict[str, Any]]:
        return self.fetch_mobile_list("/sysa/mobilephone/salesmanage/chance/list.asp").rows

    def purchase_rows(self) -> list[dict[str, Any]]:
        return self.fetch_mobile_list("/sysa/mobilephone/storemanage/caigou/list.asp", pagesize=200).rows

    def product_categories(self) -> dict[str, str]:
        session = self.require_session()
        result = self.post_json(
            "/sysa/mobilephone/systemmanage/product_sort_list.asp?stype=check",
            {"session": session, "datas": datas(stype="check")},
        )
        nodes = result.get("body", {}).get("source", {}).get("trees", {}).get("nodes", [])
        return self._flatten_categories(nodes)

    def _flatten_categories(self, nodes: list[dict[str, Any]], prefix: str = "") -> dict[str, str]:
        found: dict[str, str] = {}
        for node in nodes or []:
            text = norm(node.get("text"))
            value = norm(node.get("value"))
            path = f"{prefix}->{text}" if prefix else text
            if text and value:
                found[path] = value
            children = node.get("nodes")
            if isinstance(children, list):
                found.update(self._flatten_categories(children, path))
        return found

    def unit_id_map(self, products: list[dict[str, Any]] | None = None) -> dict[str, str]:
        products = products if products is not None else self.product_rows()
        result: dict[str, str] = {}
        for row in products:
            for unit_id, unit_name in parse_json_map(row.get("units")).items():
                if unit_name:
                    result.setdefault(unit_name, unit_id)
            unit_id = norm(row.get("unitjb"))
            unit_name = norm(row.get("unitname"))
            if unit_id and unit_name:
                result.setdefault(unit_name, unit_id)
        return result

    def find_product(self, name: str | None = None, model: str | None = None, *, company_prefix: str = "") -> list[dict[str, Any]]:
        name_key = norm(name) if name else None
        model_key = norm(model).lower().replace(" ", "") if model else None
        matches: list[dict[str, Any]] = []
        for row in self.product_rows():
            if company_prefix and not norm(row.get("fenlei")).startswith(company_prefix):
                continue
            if name_key and norm(row.get("cpname")) != name_key:
                continue
            if model_key and norm(row.get("cpxh")).lower().replace(" ", "") != model_key:
                continue
            matches.append(row)
        return matches

    def add_product(self, payload: dict[str, Any]) -> dict[str, Any]:
        session = self.require_session()
        return self.post_json("/webapi/v3/store/product/add", payload, token=session)

    def verify_product_exists(self, name: str, model: str, *, company_prefix: str = "") -> bool:
        return bool(self.find_product(name=name, model=model, company_prefix=company_prefix))

