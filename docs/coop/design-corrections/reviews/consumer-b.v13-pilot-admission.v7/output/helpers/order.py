"""x-opensip-order closed admission vocabulary from identity-and-evidence §3."""
from __future__ import annotations

from typing import Any, Callable

from . import canonical

VOCABULARY = {
    "sequence",
    "canonical-set",
    "canonical-order",
    "utf8",
    "path",
    "numeric",
    "ordinal",
    "predicate",
    "ruleId",
    "waiverId",
}


class OrderError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def _item_c_bytes(item: Any) -> bytes:
    return canonical.encode(item)


def check_order(items: list, annotation: Any, unique_items: bool = False) -> None:
    if annotation is None:
        annotation = "sequence"
    if isinstance(annotation, dict):
        by = annotation.get("by")
        if not isinstance(by, list) or not by:
            raise OrderError("ORDER_VOCAB", f"object form requires by: [key,...]; got {annotation!r}")
        keys = []
        for item in items:
            if type(item) is not dict:
                raise OrderError("ORDER_BY", "by-key order requires object items")
            tup = tuple(item.get(k) for k in by)
            # UTF-8 tuple of those item keys
            enc = b"\x1f".join(
                ("" if v is None else str(v)).encode("utf-8") for v in tup
            )
            keys.append(enc)
        _strict_unique_asc(keys, "by-key")
        return
    if annotation not in VOCABULARY:
        raise OrderError("ORDER_VOCAB", f"annotation {annotation!r} outside closed vocabulary")
    if annotation == "sequence":
        return
    if annotation == "canonical-order":
        encoded = [_item_c_bytes(x) for x in items]
        for i in range(1, len(encoded)):
            if encoded[i] < encoded[i - 1]:
                raise OrderError("ORDER_OR_DUPLICATE", "canonical-order not nondecreasing")
        return
    if annotation == "canonical-set":
        encoded = [_item_c_bytes(x) for x in items]
        _strict_unique_asc(encoded, "canonical-set")
        return
    if annotation == "utf8":
        if any(type(x) is not str for x in items):
            raise OrderError("ORDER_UTF8", "utf8 order requires string items")
        encoded = [x.encode("utf-8") for x in items]
        _strict_unique_asc(encoded, "utf8")
        return
    if annotation == "path":
        paths = []
        seen = set()
        for item in items:
            if type(item) is dict:
                p = item.get("path")
            else:
                p = item
            if type(p) is not str:
                raise OrderError("ORDER_PATH", "path order requires path string")
            if p in seen:
                raise OrderError("ORDER_PATH_DUP", f"duplicate inventory path {p!r}")
            seen.add(p)
            paths.append(p.encode("utf-8"))
        _strict_unique_asc(paths, "path")
        return
    if annotation == "numeric":
        if any(type(x) is not int or type(x) is bool for x in items):
            raise OrderError("ORDER_NUMERIC", "numeric order requires integers")
        for i in range(1, len(items)):
            if items[i] <= items[i - 1]:
                raise OrderError("ORDER_OR_DUPLICATE", "numeric not strictly ascending unique")
        return
    if annotation == "ordinal":
        for i, item in enumerate(items):
            if type(item) is not dict or "ordinal" not in item:
                raise OrderError("ORDER_ORDINAL", "ordinal order requires ordinal field")
            if item["ordinal"] != i:
                raise OrderError("ORDER_ORDINAL", f"ordinal {item['ordinal']} != index {i}")
        return
    if annotation == "predicate":
        keys = []
        for item in items:
            if type(item) is not dict:
                raise OrderError("ORDER_PREDICATE", "predicate items must be objects")
            tup = (item.get("ruleId", ""), item.get("subjectId", ""), item.get("predicateId", ""))
            keys.append("\x1f".join(tup).encode("utf-8"))
        _strict_unique_asc(keys, "predicate")
        return
    if annotation in ("ruleId", "waiverId"):
        keys = []
        for item in items:
            if type(item) is dict:
                v = item.get(annotation)
            else:
                v = item
            if type(v) is not str:
                raise OrderError("ORDER_KEY", f"{annotation} requires string")
            keys.append(v.encode("utf-8"))
        _strict_unique_asc(keys, annotation)
        return


def _strict_unique_asc(encoded: list[bytes], label: str) -> None:
    for i in range(1, len(encoded)):
        if encoded[i] <= encoded[i - 1]:
            raise OrderError(
                "ORDER_OR_DUPLICATE",
                f"{label}: not strictly ascending unique at index {i}",
            )


def cset(items: list) -> list:
    """Cset(X): unique members keyed by C(member), ordered by those bytes."""
    by = {}
    for item in items:
        by[_item_c_bytes(item)] = item
    return [by[k] for k in sorted(by)]
