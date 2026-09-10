"""Execution trace emitted at the comparison site, not a separately authored map."""
from __future__ import annotations

from typing import Any

TRACES: list[dict] = []


def reset() -> None:
    TRACES.clear()


def emit(
    *,
    condition: str,
    instance: str,
    field: str,
    comparison: str,
    left: Any,
    right: Any,
    result: str,
    extra: dict | None = None,
) -> None:
    rec = {
        "condition": condition,
        "instance": instance,
        "field": field,
        "comparison": comparison,
        "left": _short(left),
        "right": _short(right),
        "result": result,
    }
    if extra:
        rec["extra"] = extra
    TRACES.append(rec)


def _short(v: Any) -> Any:
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    if isinstance(v, (list, tuple)):
        if len(v) > 12:
            return list(v[:12]) + [f"...+{len(v)-12}"]
        return list(v)
    if isinstance(v, dict):
        keys = list(v.keys())[:12]
        return {"keys": keys, "n": len(v)}
    if isinstance(v, (bytes, bytearray)):
        return f"bytes:{len(v)}"
    return str(v)[:200]


def snapshot() -> list[dict]:
    return list(TRACES)
