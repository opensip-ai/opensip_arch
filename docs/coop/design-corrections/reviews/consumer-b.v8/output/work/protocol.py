"""The Rust major-3 provider state machine, reconstructed from its PUBLISHED
normative inputs only.

Inputs: native/protocol3-transitions.v1.json (rows, order, wildcards,
preMatchLaw, noMatchLaw, guardLaw, stateUpdates, stageDependentTransitions,
terminalLaw, initialState, initializationAndUpdateOrder) and
native-evidence.md sections 9.1, 9.2, 9.5, 10 (identity negotiation, the frame
table, and the terminal-kind -> stage authority / D9 mapping, which the table
declares PROSE-OWNED).
"""
from __future__ import annotations

import json

import osip

T = json.loads(osip.doc_bytes(
    "docs/coop/design-corrections/native/protocol3-transitions.v1.json").decode())
PHASES = T["phases"]
RULES = T["rules"]
PRE_COMPLETE = set(T["wildcards"]["*PRE_COMPLETE"]["phases"])
PROCESS_FAULT = set(T["wildcards"]["*PROCESS_FAULT"]["frames"])
SOURCE_BYTE_FRAMES = {
    "DependencySourceChunk", "DependencySourceManifest", "OpenUniverse",
    "PreparedOutputChunk", "PreparedOutputManifest", "SnapshotFileChunk",
    "SnapshotManifest"}
IDENTITY_TOKENS = ["source-identity-snapshot2", "plan-identity-plan2",
                   "fact-identity-fact2", "coverage-v3"]

# native section 9.2 / 9.3, derived from *PRE_COMPLETE = phases[1:17]
assert PRE_COMPLETE == set(PHASES[1:17])
assert len(PHASES) == 22 and T["ruleCount"] == len(RULES) == 34


def pairwise_disjoint():
    """The table asserts its rows are pairwise disjoint; check it rather than
    assume it, since first-match-wins would otherwise hide an overlap."""
    conc = [r for r in RULES if r["phase"] != "*ANY"]
    bad = []
    for i, a in enumerate(conc):
        for b in conc[i + 1:]:
            pa = PRE_COMPLETE if a["phase"] == "*PRE_COMPLETE" else {a["phase"]}
            pb = PRE_COMPLETE if b["phase"] == "*PRE_COMPLETE" else {b["phase"]}
            if not (pa & pb) or a["frame"] != b["frame"]:
                continue
            ga, gb = a.get("guard", {}), b.get("guard", {})
            shared = set(ga) & set(gb)
            if shared and any(ga[k] != gb[k] for k in shared):
                continue          # mutually exclusive guards
            bad.append((a["id"], b["id"]))
    return bad


class Machine:
    def __init__(self, stage_count=1):
        self.s = dict(T["initialState"])
        self.s["stageCount"] = stage_count
        self.trace = []
        self.stage_count = stage_count

    def step(self, frame, payload=None):
        p = self.s["phase"]
        # ---- preMatchLaw, in the declared ORDER (load-bearing) -------------
        if p == "FAULT":
            self.trace.append("FAULT-absorb")
            return
        if p in ("WAIT_ZERO_EXIT", "WAIT_EOF", "DONE") and \
                frame not in ("zero-exit", "eof") and frame not in PROCESS_FAULT:
            self.s["phase"] = "FAULT"
            self.trace.append("post-terminal-frame")
            return
        if frame in PROCESS_FAULT:
            self.s["phase"] = "FAULT"
            self.trace.append("P3-33")
            return
        # ---- matchLaw: FIRST MATCH WINS in the declared order --------------
        for r in RULES:
            if r["phase"] == "*ANY":
                continue
            phases = PRE_COMPLETE if r["phase"] == "*PRE_COMPLETE" else {r["phase"]}
            if p not in phases or r["frame"] != frame:
                continue
            if any(self.s.get(k) != v for k, v in r.get("guard", {}).items()):
                continue
            self._apply_updates(frame, payload)
            nxt = r["next"]
            if nxt == "ANALYZING_OR_READY_COMPLETE":
                self.s["stageIndex"] += 1
                self.s["stagesCompleted"] += 1
                nxt = ("READY_COMPLETE" if self.s["stageIndex"] == self.s["stageCount"]
                       else "ANALYZING")
            if "terminal" in r:
                self.s["terminalKind"] = r["terminal"]
            self.s["phase"] = nxt
            self.trace.append(r["id"])
            return
        # ---- noMatchLaw ---------------------------------------------------
        self.s["phase"] = "FAULT"
        self.trace.append("P3-34")

    def _apply_updates(self, frame, payload):
        if frame == "HelloAck":
            caps = (payload or {}).get("capabilities", [])
            self.s["identityNegotiated"] = all(t in caps for t in IDENTITY_TOKENS)
        if frame == "OpenUniverse":
            self.s["dependencyMode"] = bool((payload or {}).get("dependencyMode"))
            self.s["preparedMode"] = bool((payload or {}).get("preparedMode"))
        if frame == "Analyze":
            self.s["stageCount"] = self.stage_count
            self.s["stageIndex"] = 0
        if frame in SOURCE_BYTE_FRAMES:
            self.s["sourceBytesSent"] = True

    def run(self, events):
        for e in events:
            if isinstance(e, tuple):
                self.step(*e)
            else:
                self.step(e)
        return self


# --------------------------------------------------------------------------
# PROSE-OWNED: terminalKind -> stage authority / D9 (native sections 4.3, 10)
# --------------------------------------------------------------------------

def stage_authority(machine):
    s = machine.s
    if s["phase"] == "FAULT":
        return {"factsAdmitted": False, "coverageAdmitted": False, "runSealed": False,
                "class": "operational-failed", "exitCode": 4,
                "errorCode": "PROVIDER.PROTOCOL_VIOLATION",
                "faultCause": "provider-protocol",
                "stageTerminal": "provider-fault",
                "why": "a worker that faults contributes no facts, no Coverage and "
                       "no Run; its diagnostics are an operational record only"}
    k = s["terminalKind"]
    if k == "provider-fault":
        return {"factsAdmitted": False, "coverageAdmitted": False, "runSealed": False,
                "class": "operational-failed", "exitCode": 4,
                "errorCode": "PROVIDER.PROTOCOL_VIOLATION",
                "faultCause": "provider-protocol", "stageTerminal": "provider-fault"}
    if k == "cancelled":
        return {"factsAdmitted": False, "coverageAdmitted": False, "runSealed": False,
                "class": "interrupted", "exitCode": 130, "signal": "SIGINT",
                "stageTerminal": "cancelled"}
    if k == "complete":
        return {"factsAdmitted": True, "coverageAdmitted": True, "runSealed": True,
                "class": "success", "exitCode": 0, "stageTerminal": "complete",
                "resolutionCompletenessState": "complete (RC-2 preconditions met)"}
    if k in ("unavailable", "budget-exhausted"):
        return {"factsAdmitted": True, "coverageAdmitted": True, "runSealed": True,
                "class": "indeterminate", "exitCode": 3,
                "reasonCodes": ["COVERAGE.BUDGET_EXHAUSTED"] if k == "budget-exhausted"
                else ["VERDICT.INDETERMINATE"],
                "stageTerminal": k,
                "resolutionCompletenessState": "partial (RC-2: a stage that ended "
                                               "%s is partial regardless of edge "
                                               "count)" % k}
    return {"incomplete": True, "phase": s["phase"], "terminalKind": k}
