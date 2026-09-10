from __future__ import annotations

import json
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v4/output")
STATUS = OUT / "requirement-status.json"


def load_status() -> list[dict]:
    return json.loads(STATUS.read_text())


def save_status(rows: list[dict]) -> None:
    STATUS.write_text(json.dumps(rows, indent=2) + "\n")


def mark(ids, *, status: str, artifact=None, notes="", first_refusal=None) -> None:
    rows = load_status()
    by = {r["id"]: r for r in rows}
    if isinstance(ids, str):
        ids = [ids]
    for i in ids:
        if i not in by:
            raise KeyError(i)
        by[i]["status"] = status
        if artifact is not None:
            by[i]["artifact"] = artifact
        if notes:
            by[i]["notes"] = notes
        if first_refusal is not None:
            by[i]["firstRefusal"] = first_refusal
    save_status(list(by.values()) if False else rows)


def write_checkpoint(phase: int, *, notes: str, artifacts: list[str], helper_corrections=None) -> None:
    rows = load_status()
    req = json.loads(Path("/tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v4/requirements.json").read_text())
    required = []
    for p in req["phases"]:
        if p["n"] <= phase:
            required.extend(p["ids"])
    # standing S-* already in phase 0
    executed = [r["id"] for r in rows if r["status"] == "executed" and r["id"] in required]
    failed = [r["id"] for r in rows if r["status"] == "failed" and r["id"] in required]
    unexecuted = [i for i in required if i not in executed and i not in failed]
    # futureQualification ids are not in phase lists
    ck = {
        "phase": phase,
        "consumerId": "consumer-b.v12",
        "requirementIdsRequired": required,
        "requirementIdsExecuted": executed,
        "requirementIdsUnexecuted": unexecuted,
        "requirementIdsFailed": failed,
        "artifacts": artifacts,
        "helperCorrections": helper_corrections or [],
        "notes": notes,
    }
    path = OUT / "checkpoints" / f"phase-{phase}.json"
    path.write_text(json.dumps(ck, indent=2) + "\n")
    return ck
