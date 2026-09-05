#!/usr/bin/env python3
"""Fail-closed checker for section31-supplier-coverage.v3.

Not a Phase-1A packet. Not SATISFIED evidence. Fails when a BOUND
supplier file is missing, its selector disappears, or its exact
byte digest moves (DIGEST-MOVED).
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TABLE = ROOT / "docs/coop/artifacts/section31-supplier-coverage.v3.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve(doc, selector: str):
    if not selector.startswith("$."):
        return False
    cur = doc
    for part in selector[2:].split("."):
        if not isinstance(cur, dict) or part not in cur:
            return False
        cur = cur[part]
    return True


def extract_section31_items(freeze_text: str) -> list[str]:
    marker = "### 3.1 Phase-1A insertion — mandatory"
    start = freeze_text.find(marker)
    if start < 0:
        raise SystemExit("FAIL: freeze §3.1 heading not found")
    rest = freeze_text[start:]
    end = rest.find("\n### 3.2 ")
    block = rest if end < 0 else rest[:end]
    items: list[str] = []
    current: list[str] = []
    for line in block.splitlines():
        if line.startswith("- "):
            if current:
                items.append(_normalize_item(" ".join(current)))
            current = [line[2:].strip()]
        elif current and line.startswith("  ") and line.strip():
            current.append(line.strip())
    if current:
        items.append(_normalize_item(" ".join(current)))
    return items


def _normalize_item(text: str) -> str:
    text = text.strip()
    if text.endswith(" and"):
        text = text[:-4].rstrip()
    return text.rstrip(";.")


def main() -> int:
    table = json.loads(TABLE.read_text())
    failures: list[str] = []

    freeze_path = ROOT / table["freezeSection31"]["path"]
    if not freeze_path.is_file():
        print("FAIL: freeze file missing")
        return 2
    freeze_digest = sha256(freeze_path)
    pinned = table["freezeSection31"]["wholeFileSha256"]
    if freeze_digest != pinned:
        failures.append(
            f"ENVIRONMENT: freeze digest moved {pinned} -> {freeze_digest}; fail-closed until successor re-pin"
        )

    live_items = extract_section31_items(freeze_path.read_text())
    pinned_items = table["freezeSection31"]["itemsVerbatim"]
    if live_items != pinned_items:
        failures.append(
            f"freeze §3.1 item texts no longer match pinned list (live {len(live_items)}, pinned {len(pinned_items)})"
        )

    rows = table["items"]
    expected_n = len(pinned_items)
    if expected_n != 8:
        failures.append(f"pinned freeze list is {expected_n} items, not 8")
    if table["counts"].get("items") != expected_n:
        failures.append(f"counts.items {table['counts'].get('items')} != pinned freeze list {expected_n}")
    if len(rows) != expected_n:
        failures.append(f"item count {len(rows)} != pinned freeze list {expected_n}")
    ids = [r.get("id") for r in rows]
    nums = [r.get("item") for r in rows]
    if ids != [f"S31-{i}" for i in range(1, expected_n + 1)]:
        failures.append(f"id mapping not S31-1..S31-{expected_n}: {ids}")
    if nums != list(range(1, expected_n + 1)):
        failures.append(f"item numbers not 1..{expected_n}: {nums}")
    if len(set(ids)) != len(ids):
        failures.append("duplicate item ids")
    for i, row in enumerate(rows):
        if i < len(pinned_items) and row.get("textVerbatim") != pinned_items[i]:
            failures.append(f"{row.get('id')}: textVerbatim does not match freeze item {i+1}")

    bound = 0
    unbound = 0
    for item in rows:
        standing = item["standing"]
        if standing == "UNBOUND":
            unbound += 1
            continue
        if standing != "BOUND":
            failures.append(f"{item['id']}: unknown standing {standing}")
            continue
        bound += 1
        supplier = item["supplier"]
        path = ROOT / supplier["path"]
        if not path.is_file():
            failures.append(f"{item['id']}: bound supplier missing: {supplier['path']}")
            continue
        expected_digest = supplier.get("sha256")
        if not expected_digest:
            failures.append(f"{item['id']}: BOUND supplier has no sha256")
            continue
        live_digest = sha256(path)
        if live_digest != expected_digest:
            failures.append(
                f"{item['id']}: DIGEST-MOVED {expected_digest} -> {live_digest}"
            )
            continue
        try:
            doc = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            failures.append(f"{item['id']}: bound supplier is not JSON: {exc}")
            continue
        if not resolve(doc, supplier["selector"]):
            failures.append(
                f"{item['id']}: selector {supplier['selector']} does not resolve on {supplier['path']}"
            )

    expected = table["counts"]
    if bound != expected["bound"] or unbound != expected["unbound"]:
        failures.append(
            f"count drift: bound={bound} unbound={unbound} expected {expected}"
        )

    if failures:
        print("FAIL")
        for f in failures:
            print(f"- {f}")
        return 1
    print(f"PASS bound={bound} unbound={unbound}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
