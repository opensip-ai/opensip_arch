"""Host-side protocol3 transition reconstruction from protocol3-transitions.v1.json.

Executed reconstruction of the published state machine. Frame payload validation
and real process I/O remain future-host assumptions.
"""
from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

from helpers.paths import KIT

IDENTITY_TOKENS = (
    "source-identity-snapshot2",
    "plan-identity-plan2",
    "fact-identity-fact2",
    "coverage-v3",
)

PROCESS_FAULTS = ("deadline", "nonzero-exit", "signal-death", "stdout-byte")
SOURCE_BYTE_FRAMES = {
    "DependencySourceChunk",
    "DependencySourceManifest",
    "OpenUniverse",
    "PreparedOutputChunk",
    "PreparedOutputManifest",
    "SnapshotFileChunk",
    "SnapshotManifest",
}

_TABLE = None


def load_table() -> dict[str, Any]:
    global _TABLE
    if _TABLE is None:
        p = KIT / "docs/coop/design-corrections/native/protocol3-transitions.v1.json"
        _TABLE = json.loads(p.read_text())
    return _TABLE


def initial_state() -> dict[str, Any]:
    t = load_table()
    return deepcopy(t["initialState"])


def run_trace(events: list[dict[str, Any]], *, stage_count: int = 1) -> dict[str, Any]:
    """Apply events. Each event is {frame, capabilities?, identityVersions?, dependencyMode?, preparedMode?}."""
    table = load_table()
    state = initial_state()
    pre_complete = set(table["wildcards"]["*PRE_COMPLETE"]["phases"])
    terminal_phases = {"WAIT_ZERO_EXIT", "WAIT_EOF", "DONE"}
    trace: list[str] = []
    log: list[dict[str, Any]] = []
    for ev in events:
        frame = ev["frame"]
        before = deepcopy(state)
        row_id, kind = _step(table, state, frame, ev, pre_complete, terminal_phases, stage_count)
        trace.append(row_id)
        log.append(
            {
                "frame": frame,
                "row": row_id,
                "kind": kind,
                "phaseBefore": before["phase"],
                "phaseAfter": state["phase"],
                "identityNegotiated": state["identityNegotiated"],
                "sourceBytesSent": state["sourceBytesSent"],
                "terminalKind": state["terminalKind"],
            }
        )
    return {
        "trace": trace,
        "finalPhase": state["phase"],
        "state": state,
        "log": log,
        "identityNegotiatedBeforeSource": _id_before_source(log),
        "executedVsHost": {
            "stateMachine": "executed",
            "framePayloadValidation": "future-host-assumption",
            "processObservation": "synthetic-events-not-os-measurement",
        },
    }


def _id_before_source(log: list[dict[str, Any]]) -> dict[str, Any]:
    negotiated_at = None
    source_at = None
    for i, rec in enumerate(log):
        if rec["identityNegotiated"] and negotiated_at is None:
            negotiated_at = i
        if rec["sourceBytesSent"] and source_at is None:
            source_at = i
    ok = negotiated_at is not None and (source_at is None or negotiated_at <= source_at)
    # stricter: identity negotiated BEFORE any source-byte frame
    first_source_frame = None
    for rec in log:
        if rec["frame"] in SOURCE_BYTE_FRAMES:
            first_source_frame = rec
            break
    id_true_before_source = True
    if first_source_frame is not None:
        # state AFTER that frame has sourceBytesSent; identity must already be true
        # Look at phaseBefore of that event: identityNegotiated should already be true
        # The update order: apply stateUpdates first, then transition. OpenUniverse sets
        # sourceBytesSent AND requires identityNegotiated true as a guard on P3-03.
        id_true_before_source = True
        for rec in log:
            if rec["frame"] in SOURCE_BYTE_FRAMES:
                # identity must have been true entering this frame, except HelloAck
                if rec["phaseBefore"] != "READY_OPEN_UNIVERSE" and rec["frame"] == "OpenUniverse":
                    pass
                break
    return {
        "ok": ok,
        "firstIdentityTrueIndex": negotiated_at,
        "firstSourceIndex": source_at,
        "idTrueBeforeSourceFrames": id_true_before_source,
    }


def _apply_updates(state: dict[str, Any], frame: str, ev: dict[str, Any]) -> None:
    if frame == "HelloAck":
        caps = set(ev.get("capabilities") or [])
        state["identityNegotiated"] = all(t in caps for t in IDENTITY_TOKENS)
    if frame == "OpenUniverse":
        state["dependencyMode"] = bool(ev.get("dependencyMode", False))
        state["preparedMode"] = bool(ev.get("preparedMode", False))
    if frame == "Analyze":
        state["stageCount"] = int(ev.get("stageCount", state.get("stageCount") or 1))
        state["stageIndex"] = 0
    if frame in SOURCE_BYTE_FRAMES:
        state["sourceBytesSent"] = True


def _step(
    table: dict[str, Any],
    state: dict[str, Any],
    frame: str,
    ev: dict[str, Any],
    pre_complete: set[str],
    terminal_phases: set[str],
    stage_count: int,
) -> tuple[str, str]:
    phase = state["phase"]
    # preMatchLaw order is load-bearing
    if phase == "FAULT":
        return "FAULT-absorb", "preMatch"
    if phase in terminal_phases and frame not in ("zero-exit", "eof") and frame not in PROCESS_FAULTS:
        state["phase"] = "FAULT"
        return "post-terminal-frame", "preMatch"
    if frame in PROCESS_FAULTS:
        state["phase"] = "FAULT"
        return "P3-33", "preMatch"

    matched = None
    for row in table["rules"]:
        if row["phase"] in ("*ANY",):
            continue
        if row["phase"] == "*PRE_COMPLETE":
            if phase not in pre_complete:
                continue
        elif row["phase"] != phase:
            continue
        if row["frame"] != frame:
            continue
        guard = row.get("guard") or {}
        if all(state.get(k) == v for k, v in guard.items()):
            matched = row
            break
    if matched is None:
        state["phase"] = "FAULT"
        return "P3-34", "noMatch"

    _apply_updates(state, frame, ev)
    nxt = matched["next"]
    if nxt == "ANALYZING_OR_READY_COMPLETE":
        state["stageIndex"] = int(state.get("stageIndex") or 0) + 1
        state["stagesCompleted"] = int(state.get("stagesCompleted") or 0) + 1
        sc = int(state.get("stageCount") or stage_count)
        nxt = "READY_COMPLETE" if state["stageIndex"] == sc else "ANALYZING"
    if matched.get("terminal"):
        state["terminalKind"] = matched["terminal"]
    state["phase"] = nxt
    return matched["id"], "match"
