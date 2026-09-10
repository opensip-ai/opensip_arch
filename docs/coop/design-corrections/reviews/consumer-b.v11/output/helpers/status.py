from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from helpers.paths import OUTPUT, REQUIREMENTS, CONSUMER_ID

REQUIRED_FIELDS = [
    "id",
    "kind",
    "acceptBlocking",
    "status",
    "artifact",
    "firstRefusal",
    "notes",
]


def load_requirements() -> dict[str, Any]:
    return json.loads(REQUIREMENTS.read_text())


def all_ids(req: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for s in req["standing"]:
        rows.append(s)
    for r in req["requirements"]:
        rows.append(r)
    for f in req["futureQualification"]:
        rows.append(f)
    return rows


def init_status() -> dict[str, Any]:
    req = load_requirements()
    items = []
    for row in all_ids(req):
        status = "futureQualification" if row.get("kind") == "futureQualification" else "unexecuted"
        items.append(
            {
                "id": row["id"],
                "kind": row["kind"],
                "acceptBlocking": bool(row.get("acceptBlocking", False)),
                "status": status,
                "artifact": None,
                "firstRefusal": None,
                "notes": "",
                "phase": row.get("phase"),
            }
        )
    return {"consumerId": CONSUMER_ID, "items": items}


def load_status() -> dict[str, Any]:
    p = OUTPUT / "requirement-status.json"
    if p.exists():
        return json.loads(p.read_text())
    return init_status()


def save_status(st: dict[str, Any]) -> None:
    (OUTPUT / "requirement-status.json").write_text(json.dumps(st, indent=2, sort_keys=False) + "\n")


def mark(st: dict[str, Any], rid: str, status: str, *, artifact: str | None = None, notes: str = "", firstRefusal: Any = None) -> None:
    for item in st["items"]:
        if item["id"] == rid:
            item["status"] = status
            if artifact is not None:
                item["artifact"] = artifact
            if notes:
                item["notes"] = notes
            if firstRefusal is not None:
                item["firstRefusal"] = firstRefusal
            return
    raise KeyError(rid)


def write_checkpoint(
    phase: int,
    *,
    executed: list[str],
    required: list[str],
    artifacts: list[str],
    notes: str,
    helper_corrections: list[dict[str, Any]] | None = None,
    failed: list[str] | None = None,
) -> None:
    st = load_status()
    by_id = {i["id"]: i for i in st["items"]}
    unexec = [i for i in required if by_id[i]["status"] == "unexecuted"]
    fail = failed if failed is not None else [i for i in required if by_id[i]["status"] == "failed"]
    rec = {
        "phase": phase,
        "consumerId": CONSUMER_ID,
        "requirementIdsRequired": required,
        "requirementIdsExecuted": executed,
        "requirementIdsUnexecuted": unexec,
        "requirementIdsFailed": fail,
        "artifacts": artifacts,
        "helperCorrections": helper_corrections or [],
        "notes": notes,
    }
    cp = OUTPUT / "checkpoints"
    cp.mkdir(parents=True, exist_ok=True)
    (cp / f"phase-{phase}.json").write_text(json.dumps(rec, indent=2) + "\n")
    save_status(st)


def dump_json(path: Path, obj: Any) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, default=_default) + "\n")
    return str(path)


def _default(o: Any) -> Any:
    if isinstance(o, bytes):
        return o.hex()
    if isinstance(o, set):
        return sorted(o)
    raise TypeError(type(o))
