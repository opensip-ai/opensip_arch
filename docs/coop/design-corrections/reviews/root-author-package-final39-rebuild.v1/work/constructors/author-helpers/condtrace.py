"""Execution trace emitted at the comparison site, not a separately authored map."""
from __future__ import annotations

from typing import Any

TRACES: list[dict] = []
CURRENT_DOCUMENT: str | None = None


def reset() -> None:
    TRACES.clear()
    global CURRENT_DOCUMENT
    CURRENT_DOCUMENT = None


def set_document(kit_path: str | None) -> None:
    """Owning kit document for subsequent emits until changed."""
    global CURRENT_DOCUMENT
    CURRENT_DOCUMENT = kit_path


def emit(
    *,
    condition: str,
    instance: str,
    field: str,
    comparison: str,
    left: Any,
    right: Any,
    result: str,
    document: str | None = None,
    extra: dict | None = None,
) -> None:
    rec = {
        "document": document if document is not None else CURRENT_DOCUMENT,
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
