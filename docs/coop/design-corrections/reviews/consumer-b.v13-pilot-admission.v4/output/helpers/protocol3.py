"""Rust protocol-3 transition reconstruction from protocol3-transitions.v1.json.

Executed reconstruction of the published state machine. Process-level
observations (deadline, nonzero-exit, signal-death, stdout-byte) are
synthetic host observations, labelled as such — not native OS proof.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v13/subject")
DOC = json.loads(
    (KIT / "docs/coop/design-corrections/native/protocol3-transitions.v1.json").read_text()
)

PROCESS_FAULTS = set(DOC["wildcards"]["*PROCESS_FAULT"]["frames"])
PRE_COMPLETE = set(DOC["wildcards"]["*PRE_COMPLETE"]["phases"])
# native-evidence §9.1: four identity tokens required before source disclosure
IDENTITY_TOKENS = (
    "source-identity-snapshot2",
    "plan-identity-plan2",
    "fact-identity-fact2",
    "coverage-v3",
)


class Protocol3:
    def __init__(self):
        self.state = copy.deepcopy(DOC["initialState"])
        self.trace: list[str] = []
        self.events: list[dict] = []
        self.executedVsHost: list[dict] = []

    def _match_row(self, frame: str) -> dict | None:
        phase = self.state["phase"]
        for row in DOC["rules"]:
            row_phase = row.get("phase")
            if row_phase == "*ANY":
                continue
            if row_phase == "*PRE_COMPLETE":
                if phase not in PRE_COMPLETE:
                    continue
            elif row_phase != phase:
                continue
            if row.get("frame") != frame:
                continue
            guard = row.get("guard") or {}
            ok = True
            for k, v in guard.items():
                if self.state.get(k) != v:
                    ok = False
                    break
            if ok:
                return row
        return None

    def _apply_frame_updates(self, frame: str, payload: dict) -> None:
        if frame == "HelloAck":
            caps = set(payload.get("capabilities") or [])
            # identityNegotiated iff every identity token is present
            needed = set(IDENTITY_TOKENS)
            self.state["identityNegotiated"] = needed.issubset(caps)
        if frame == "OpenUniverse":
            self.state["dependencyMode"] = bool(payload.get("dependencyMode", False))
            self.state["preparedMode"] = bool(payload.get("preparedMode", False))
            self.state["sourceBytesSent"] = True
        if frame == "Analyze":
            self.state["stageCount"] = int(payload.get("stageCount", 1))
            self.state["stageIndex"] = 0
        if frame in {
            "DependencySourceChunk",
            "DependencySourceManifest",
            "PreparedOutputChunk",
            "PreparedOutputManifest",
            "SnapshotFileChunk",
            "SnapshotManifest",
        }:
            self.state["sourceBytesSent"] = True

    def _resolve_next(self, row: dict) -> str:
        nxt = row.get("next")
        if nxt == "ANALYZING_OR_READY_COMPLETE":
            self.state["stageIndex"] += 1
            self.state["stagesCompleted"] += 1
            if self.state["stageIndex"] == self.state["stageCount"]:
                return "READY_COMPLETE"
            return "ANALYZING"
        return nxt

    def step(self, frame: str, payload: dict | None = None, executed: str = "executed") -> str:
        payload = payload or {}
        phase_before = self.state["phase"]
        note = None
        # preMatchLaw, declared order
        if phase_before == "FAULT":
            self.trace.append("FAULT-absorb")
            rec = "FAULT-absorb"
            self.events.append({"frame": frame, "from": phase_before, "to": "FAULT", "trace": rec})
            self.executedVsHost.append({"frame": frame, "result": rec, "executedVsHost": executed})
            return rec
        if phase_before in ("WAIT_ZERO_EXIT", "WAIT_EOF", "DONE") and frame not in (
            "zero-exit",
            "eof",
        ) and frame not in PROCESS_FAULTS:
            self.state["phase"] = "FAULT"
            self.trace.append("post-terminal-frame")
            rec = "post-terminal-frame"
            self.events.append({"frame": frame, "from": phase_before, "to": "FAULT", "trace": rec})
            self.executedVsHost.append({"frame": frame, "result": rec, "executedVsHost": executed})
            return rec
        if frame in PROCESS_FAULTS:
            self.state["phase"] = "FAULT"
            self.trace.append("P3-33")
            rec = "P3-33"
            self.events.append({"frame": frame, "from": phase_before, "to": "FAULT", "trace": rec})
            self.executedVsHost.append(
                {
                    "frame": frame,
                    "result": rec,
                    "executedVsHost": "future-host-assumption"
                    if executed == "executed"
                    else executed,
                    "note": "process-fault frames are synthetic host observations in this reconstruction",
                }
            )
            return rec
        row = self._match_row(frame)
        if row is None:
            self.state["phase"] = "FAULT"
            self.trace.append("P3-34")
            rec = "P3-34"
            self.events.append({"frame": frame, "from": phase_before, "to": "FAULT", "trace": rec})
            self.executedVsHost.append({"frame": frame, "result": rec, "executedVsHost": executed})
            return rec
        self._apply_frame_updates(frame, payload)
        nxt = self._resolve_next(row)
        if row.get("terminal"):
            self.state["terminalKind"] = row["terminal"]
        self.state["phase"] = nxt
        rid = row["id"]
        self.trace.append(rid)
        self.events.append(
            {
                "frame": frame,
                "from": phase_before,
                "to": nxt,
                "trace": rid,
                "identityNegotiated": self.state["identityNegotiated"],
                "sourceBytesSent": self.state["sourceBytesSent"],
            }
        )
        self.executedVsHost.append({"frame": frame, "result": rid, "executedVsHost": executed})
        return rid

    def snapshot(self) -> dict:
        return {
            "state": copy.deepcopy(self.state),
            "trace": list(self.trace),
            "events": list(self.events),
            "executedVsHost": list(self.executedVsHost),
            "selector": "docs/coop/design-corrections/native/protocol3-transitions.v1.json",
        }
