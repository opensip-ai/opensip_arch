"""Host-side protocol3 transition reconstruction from protocol3-transitions.v1.json.

Executed reconstruction of the published state machine. Frame payload validation
and native compiler/process execution are future-host assumptions, labeled as such.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v3/subject")
DOC = json.loads(
    (KIT / "docs/coop/design-corrections/native/protocol3-transitions.v1.json").read_text()
)

IDENTITY_TOKENS = (
    "source-identity-snapshot2",
    "plan-identity-plan2",
    "fact-identity-fact2",
    "coverage-v3",
)

PROCESS_FAULT_FRAMES = set(DOC["wildcards"]["*PROCESS_FAULT"]["frames"])
PRE_COMPLETE = set(DOC["wildcards"]["*PRE_COMPLETE"]["phases"])
SOURCE_BYTE_FRAMES = {
    "DependencySourceChunk",
    "DependencySourceManifest",
    "OpenUniverse",
    "PreparedOutputChunk",
    "PreparedOutputManifest",
    "SnapshotFileChunk",
    "SnapshotManifest",
}


def _fresh() -> dict:
    return copy.deepcopy(DOC["initialState"])


def _guard_ok(guard: dict | None, state: dict) -> bool:
    if not guard:
        return True
    return all(state.get(k) == v for k, v in guard.items())


def _apply_frame_updates(state: dict, frame: str, event: dict) -> None:
    if frame == "HelloAck":
        caps = event.get("capabilities") or []
        state["identityNegotiated"] = all(t in caps for t in IDENTITY_TOKENS)
    elif frame == "OpenUniverse":
        state["dependencyMode"] = bool(event.get("dependencyMode", False))
        state["preparedMode"] = bool(event.get("preparedMode", False))
    elif frame == "Analyze":
        state["stageCount"] = int(event.get("stageCount", 1))
        state["stageIndex"] = 0
    if frame in SOURCE_BYTE_FRAMES:
        state["sourceBytesSent"] = True


def step(state: dict, event: dict) -> dict:
    """Apply one event. Returns {traceId, state, executedVsHost}."""
    frame = event["frame"]
    phase = state["phase"]

    # preMatchLaw order is load-bearing
    if phase == "FAULT":
        return {"traceId": "FAULT-absorb", "state": state, "executedVsHost": "executed"}
    if phase in ("WAIT_ZERO_EXIT", "WAIT_EOF", "DONE") and frame not in {
        "zero-exit",
        "eof",
    } | PROCESS_FAULT_FRAMES:
        state["phase"] = "FAULT"
        return {"traceId": "post-terminal-frame", "state": state, "executedVsHost": "executed"}
    if frame in PROCESS_FAULT_FRAMES:
        state["phase"] = "FAULT"
        return {"traceId": "P3-33", "state": state, "executedVsHost": "executed"}

    # matchLaw: first match wins; skip *ANY rows
    matched = None
    for row in DOC["rules"]:
        if row["phase"] == "*ANY":
            continue
        if row["phase"] == "*PRE_COMPLETE":
            if phase not in PRE_COMPLETE:
                continue
        elif row["phase"] != phase:
            continue
        if row["frame"] != frame:
            continue
        if not _guard_ok(row.get("guard"), state):
            continue
        matched = row
        break

    if matched is None:
        state["phase"] = "FAULT"
        return {"traceId": "P3-34", "state": state, "executedVsHost": "executed"}

    _apply_frame_updates(state, frame, event)
    nxt = matched["next"]
    if nxt == "ANALYZING_OR_READY_COMPLETE":
        state["stageIndex"] += 1
        state["stagesCompleted"] += 1
        if state["stageIndex"] == state["stageCount"]:
            nxt = "READY_COMPLETE"
        else:
            nxt = "ANALYZING"
    if matched.get("terminal"):
        state["terminalKind"] = matched["terminal"]
    state["phase"] = nxt
    return {"traceId": matched["id"], "state": copy.deepcopy(state), "executedVsHost": "executed"}


def run_trace(events: list[dict], *, stage_count: int = 1) -> dict:
    state = _fresh()
    # stageCount is an invocation property supplied to the transition system
    state["stageCount"] = stage_count
    trace = []
    for ev in events:
        rec = step(state, ev)
        trace.append(
            {
                "event": ev,
                "traceId": rec["traceId"],
                "phaseAfter": rec["state"]["phase"],
                "identityNegotiated": rec["state"]["identityNegotiated"],
                "sourceBytesSent": rec["state"]["sourceBytesSent"],
                "terminalKind": rec["state"]["terminalKind"],
                "executedVsHost": rec["executedVsHost"],
            }
        )
    return {
        "final": copy.deepcopy(state),
        "trace": trace,
        "selector": "docs/coop/design-corrections/native/protocol3-transitions.v1.json",
    }
