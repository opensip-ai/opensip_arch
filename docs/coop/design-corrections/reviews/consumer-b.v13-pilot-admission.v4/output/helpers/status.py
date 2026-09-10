"""Requirement status ledger. Later phases may not drop IDs."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v4/output")
REQS = Path("/tmp/opensip-design-corrections/consumer-b.v13/requirements.json")


def load_requirements() -> dict:
    return json.loads(REQS.read_text())


def all_ids(doc: dict) -> list[dict]:
    rows = []
    for s in doc["standing"]:
        rows.append(s)
    for r in doc["requirements"]:
        rows.append(r)
    for f in doc["futureQualification"]:
        rows.append(f)
    return rows


def init_status() -> list[dict]:
    doc = load_requirements()
    rows = []
    for r in all_ids(doc):
        rows.append(
            {
                "id": r["id"],
                "kind": r.get("kind"),
                "acceptBlocking": r.get("acceptBlocking", True),
                "status": "futureQualification"
                if r.get("kind") == "futureQualification"
                else "unexecuted",
                "artifact": None,
                "firstRefusal": None,
                "notes": "",
            }
        )
    return rows


def save_status(rows: list[dict]) -> None:
    (OUT / "requirement-status.json").write_text(json.dumps(rows, indent=2) + "\n")


def mark(rows: list[dict], rid: str, status: str, artifact: str | None = None, notes: str = "", first_refusal: Any = None) -> None:
    for r in rows:
        if r["id"] == rid:
            r["status"] = status
            if artifact:
                r["artifact"] = artifact
            if notes:
                r["notes"] = notes
            if first_refusal is not None:
                r["firstRefusal"] = first_refusal
            return
    raise KeyError(rid)


def checkpoint(phase: int, rows: list[dict], artifacts: list[str], notes: str, helper_corrections: list | None = None) -> None:
    required = [r["id"] for r in rows if r["status"] != "futureQualification"]
    executed = [r["id"] for r in rows if r["status"] == "executed"]
    failed = [r["id"] for r in rows if r["status"] == "failed"]
    unexecuted = [r["id"] for r in rows if r["status"] == "unexecuted"]
    doc = {
        "phase": phase,
        "consumerId": "consumer-b.v13",
        "requirementIdsRequired": required,
        "requirementIdsExecuted": executed,
        "requirementIdsUnexecuted": unexecuted,
        "requirementIdsFailed": failed,
        "artifacts": artifacts,
        "helperCorrections": helper_corrections or [],
        "notes": notes,
    }
    (OUT / "checkpoints").mkdir(parents=True, exist_ok=True)
    (OUT / f"checkpoints/phase-{phase}.json").write_text(json.dumps(doc, indent=2) + "\n")
    save_status(rows)
