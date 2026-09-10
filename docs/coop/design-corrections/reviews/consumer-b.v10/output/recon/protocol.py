"""Provider protocol 3 host state machine from protocol3-transitions.v1.json.

Owner: docs/coop/design-corrections/native/protocol3-transitions.v1.json
Prose-owned (not in the table): frame payloads, identity token set, D9 mapping, stage count.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v10/subject")

IDENTITY_TOKENS = [
    "source-identity-snapshot2",
    "plan-identity-plan2",
    "fact-identity-fact2",
    "coverage-v3",
]

PROCESS_FAULT = {"deadline", "nonzero-exit", "signal-death", "stdout-byte"}


def load_table() -> dict:
    p = KIT / "docs/coop/design-corrections/native/protocol3-transitions.v1.json"
    return json.loads(p.read_text())


def identity_negotiated(hello_ack: dict) -> bool:
    caps = hello_ack.get("capabilities") or []
    return all(t in caps for t in IDENTITY_TOKENS)


class Protocol3:
    def __init__(self, table: dict | None = None, *, stage_count: int = 1):
        self.table = table or load_table()
        self.stage_count_override = stage_count
        self.reset()

    def reset(self) -> None:
        self.state = copy.deepcopy(self.table["initialState"])
        self.trace: list[str] = []
        self.source_bytes_sent_before_identity = False

    @property
    def phase(self) -> str:
        return self.state["phase"]

    def apply(self, frame: str, payload: dict | None = None) -> dict:
        payload = payload or {}
        pre = self._pre_match(frame)
        if pre:
            return pre
        row = self._match(frame)
        if row is None:
            return self._no_match()
        self._state_updates(frame, payload)
        nxt = row.get("next")
        if nxt == "ANALYZING_OR_READY_COMPLETE":
            self.state["stageIndex"] = int(self.state.get("stageIndex") or 0) + 1
            self.state["stagesCompleted"] = int(self.state.get("stagesCompleted") or 0) + 1
            if self.state["stageIndex"] == self.state.get("stageCount"):
                nxt = "READY_COMPLETE"
            else:
                nxt = "ANALYZING"
        if row.get("terminal"):
            self.state["terminalKind"] = row["terminal"]
        self.state["phase"] = nxt
        self.trace.append(row["id"])
        return {"id": row["id"], "phase": self.state["phase"], "state": copy.deepcopy(self.state)}

    def _pre_match(self, frame: str) -> dict | None:
        # FAULT is absorbing — first preMatchLaw entry.
        if self.state["phase"] == "FAULT":
            self.trace.append("FAULT-absorb")
            return {"id": "FAULT-absorb", "phase": "FAULT", "state": copy.deepcopy(self.state)}
        # post-terminal frames
        if self.state["phase"] in ("WAIT_ZERO_EXIT", "WAIT_EOF", "DONE"):
            if frame not in ("zero-exit", "eof") and frame not in PROCESS_FAULT:
                self.state["phase"] = "FAULT"
                self.trace.append("post-terminal-frame")
                return {"id": "post-terminal-frame", "phase": "FAULT", "state": copy.deepcopy(self.state)}
        # *PROCESS_FAULT from any phase → P3-33
        if frame in PROCESS_FAULT:
            self.state["phase"] = "FAULT"
            self.trace.append("P3-33")
            return {"id": "P3-33", "phase": "FAULT", "state": copy.deepcopy(self.state)}
        return None

    def _match(self, frame: str) -> dict | None:
        wild = self.table["wildcards"]["*PRE_COMPLETE"]["phases"]
        for row in self.table["rules"]:
            if row["phase"] == "*ANY":
                continue  # skipped by matching loop; applied by pre/no-match
            phase_ok = row["phase"] == self.state["phase"] or (
                row["phase"] == "*PRE_COMPLETE" and self.state["phase"] in wild
            )
            if not phase_ok:
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

    def _no_match(self) -> dict:
        self.state["phase"] = "FAULT"
        self.trace.append("P3-34")
        return {"id": "P3-34", "phase": "FAULT", "state": copy.deepcopy(self.state)}

    def _state_updates(self, frame: str, payload: dict) -> None:
        if frame == "HelloAck":
            self.state["identityNegotiated"] = identity_negotiated(payload)
        if frame == "OpenUniverse":
            self.state["dependencyMode"] = bool(payload.get("dependencyMode", False))
            self.state["preparedMode"] = bool(payload.get("preparedMode", False))
        if frame == "Analyze":
            self.state["stageCount"] = int(payload.get("stageCount", self.stage_count_override))
            self.state["stageIndex"] = 0
        source_frames = {
            "DependencySourceChunk",
            "DependencySourceManifest",
            "OpenUniverse",
            "PreparedOutputChunk",
            "PreparedOutputManifest",
            "SnapshotFileChunk",
            "SnapshotManifest",
        }
        if frame in source_frames:
            if not self.state.get("identityNegotiated"):
                self.source_bytes_sent_before_identity = True
            self.state["sourceBytesSent"] = True


def rust_hello_caps() -> list[str]:
    return [
        "source-identity-snapshot2",
        "plan-identity-plan2",
        "fact-identity-fact2",
        "coverage-v3",
        "sealed-vfs-v1",
        "multi-stage-analyze-v1",
        "rust-semantic-facts-v1",
        "resolution-completeness-v2",
        "unresolved-edge-v1",
        "dependency-source-v1",
        "prepared-output-v3",
        "native-context-v2",
    ]


def identity_versions() -> dict:
    return {"snapshot": 2, "plan": 2, "fact": 2, "coverage": 3}


def run_trace(events: list[tuple[str, dict]], *, stage_count: int = 1) -> dict:
    p = Protocol3(stage_count=stage_count)
    steps = []
    for frame, payload in events:
        steps.append(p.apply(frame, payload))
    return {
        "trace": list(p.trace),
        "phase": p.phase,
        "state": p.state,
        "sourceBytesSent": p.state.get("sourceBytesSent"),
        "identityNegotiated": p.state.get("identityNegotiated"),
        "sourceBytesSentBeforeIdentity": p.source_bytes_sent_before_identity,
        "steps": [{"id": s["id"], "phase": s["phase"]} for s in steps],
    }
