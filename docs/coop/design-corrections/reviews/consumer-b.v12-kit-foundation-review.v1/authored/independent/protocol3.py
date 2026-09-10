"""Independent protocol3 transition reconstruction from protocol3-transitions.v1.json.

Frame payload schema and native process spawn are future-host assumptions.
"""
from __future__ import annotations

import copy
from independent.schema_and_order import load_json

DOC = load_json("native/protocol3-transitions.v1.json")
IDENTITY_TOKENS = (
    "source-identity-snapshot2",
    "plan-identity-plan2",
    "fact-identity-fact2",
    "coverage-v3",
)
PROCESS_FAULT = set(DOC["wildcards"]["*PROCESS_FAULT"]["frames"])
PRE_COMPLETE = set(DOC["wildcards"]["*PRE_COMPLETE"]["phases"])
SOURCE_FRAMES = {
    "DependencySourceChunk",
    "DependencySourceManifest",
    "OpenUniverse",
    "PreparedOutputChunk",
    "PreparedOutputManifest",
    "SnapshotFileChunk",
    "SnapshotManifest",
}


def fresh_state() -> dict:
    return copy.deepcopy(DOC["initialState"])


def _apply_updates(state: dict, event: dict) -> None:
    frame = event["frame"]
    if frame == "HelloAck":
        caps = set(event.get("capabilities") or [])
        state["identityNegotiated"] = all(t in caps for t in IDENTITY_TOKENS)
    if frame == "OpenUniverse":
        state["dependencyMode"] = bool(event.get("dependencyMode"))
        state["preparedMode"] = bool(event.get("preparedMode"))
    if frame == "Analyze":
        state["stageCount"] = int(event.get("stageCount") or state.get("stageCount") or 0)
        state["stageIndex"] = 0
    if frame in SOURCE_FRAMES:
        state["sourceBytesSent"] = True


def _guard_ok(guard: dict | None, state: dict) -> bool:
    if not guard:
        return True
    return all(state.get(k) == v for k, v in guard.items())


def _match_row(state: dict, frame: str):
    for row in DOC["rules"]:
        if row["id"] in ("P3-33", "P3-34"):
            continue
        phase_ok = row["phase"] == state["phase"] or (
            row["phase"] == "*PRE_COMPLETE" and state["phase"] in PRE_COMPLETE
        )
        if not phase_ok:
            continue
        if row["frame"] != frame:
            continue
        if _guard_ok(row.get("guard"), state):
            return row
    return None


def step(state: dict, event: dict) -> dict:
    """Apply one event. Returns {traceId, phaseAfter, state}."""
    frame = event["frame"]
    # preMatchLaw order is load-bearing
    if state["phase"] == "FAULT":
        return {"traceId": "FAULT-absorb", "phaseAfter": "FAULT", "state": state}
    if state["phase"] in ("WAIT_ZERO_EXIT", "WAIT_EOF", "DONE") and frame not in (
        "zero-exit",
        "eof",
    ) and frame not in PROCESS_FAULT:
        state["phase"] = "FAULT"
        return {"traceId": "post-terminal-frame", "phaseAfter": "FAULT", "state": state}
    if frame in PROCESS_FAULT:
        state["phase"] = "FAULT"
        return {"traceId": "P3-33", "phaseAfter": "FAULT", "state": state}
    row = _match_row(state, frame)
    if row is None:
        state["phase"] = "FAULT"
        return {"traceId": "P3-34", "phaseAfter": "FAULT", "state": state}
    _apply_updates(state, event)
    nxt = row["next"]
    if nxt == "ANALYZING_OR_READY_COMPLETE":
        state["stageIndex"] = state.get("stageIndex", 0) + 1
        state["stagesCompleted"] = state.get("stagesCompleted", 0) + 1
        nxt = "READY_COMPLETE" if state["stageIndex"] == state.get("stageCount") else "ANALYZING"
    if row.get("terminal"):
        state["terminalKind"] = row["terminal"]
    state["phase"] = nxt
    return {
        "traceId": row["id"],
        "phaseAfter": state["phase"],
        "state": state,
    }


def run_trace(events: list[dict], *, stage_count: int | None = None) -> dict:
    state = fresh_state()
    if stage_count is not None:
        state["stageCount"] = stage_count
    steps = []
    for ev in events:
        rec = step(state, ev)
        steps.append(
            {
                "event": ev,
                "traceId": rec["traceId"],
                "phaseAfter": rec["phaseAfter"],
                "identityNegotiated": state["identityNegotiated"],
                "sourceBytesSent": state["sourceBytesSent"],
                "terminalKind": state["terminalKind"],
            }
        )
    return {"final": copy.deepcopy(state), "steps": steps}
