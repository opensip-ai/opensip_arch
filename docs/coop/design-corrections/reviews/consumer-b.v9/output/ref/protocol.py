"""Independent implementation of the Rust major-3 provider state law.

Read from docs/coop/design-corrections/native/protocol3-transitions.v1.json
(the published 34-row first-match/total-fallback table, its wildcards, its
pre-match law, its guard law, its state updates, the stage-dependent
transition and the terminal law).  No author model was read.
"""
from __future__ import annotations

import kit

TBL = kit.doc("protocol3")
PHASES = TBL["phases"]
RULES = [r for r in TBL["rules"] if r["phase"] != "*ANY"]
PRE_COMPLETE = set(TBL["wildcards"]["*PRE_COMPLETE"]["phases"])
PROCESS_FAULT = set(TBL["wildcards"]["*PROCESS_FAULT"]["frames"])
IDENTITY_TOKENS = {"source-identity-snapshot2", "plan-identity-plan2",
                   "fact-identity-fact2", "coverage-v3"}
SOURCE_BYTE_FRAMES = {"DependencySourceChunk", "DependencySourceManifest",
                      "OpenUniverse", "PreparedOutputChunk",
                      "PreparedOutputManifest", "SnapshotFileChunk",
                      "SnapshotManifest"}


def initial_state(stage_count=1):
    st = dict(TBL["initialState"])
    st["_declaredStageCount"] = stage_count
    return st


def step(state, frame, payload=None):
    """One event.  Returns (state, traceId)."""
    st = dict(state)
    name = frame

    # --- preMatchLaw, in the order its entries are listed -------------------
    if st["phase"] == "FAULT":
        return st, "FAULT-absorb"
    if st["phase"] in ("WAIT_ZERO_EXIT", "WAIT_EOF", "DONE") and \
            name not in ("zero-exit", "eof") and name not in PROCESS_FAULT:
        st["phase"] = "FAULT"
        return st, "post-terminal-frame"
    if name in PROCESS_FAULT:
        st["phase"] = "FAULT"
        return st, "P3-33"

    # --- matchLaw: first match wins in declared order ----------------------
    for rule in RULES:
        if rule["phase"] == "*PRE_COMPLETE":
            if st["phase"] not in PRE_COMPLETE:
                continue
        elif rule["phase"] != st["phase"]:
            continue
        if rule["frame"] != name:
            continue
        guard = rule.get("guard", {})
        if any(st.get(k) != v for k, v in guard.items()):
            continue
        # (1) state updates of the INCOMING frame
        if name == "HelloAck":
            st["identityNegotiated"] = IDENTITY_TOKENS <= set(
                (payload or {}).get("capabilities", []))
        if name == "OpenUniverse":
            st["dependencyMode"] = bool((payload or {}).get("dependencyMode"))
            st["preparedMode"] = bool((payload or {}).get("preparedMode"))
        if name == "Analyze":
            st["stageCount"] = st["_declaredStageCount"]
            st["stageIndex"] = 0
        if name in SOURCE_BYTE_FRAMES:
            st["sourceBytesSent"] = True
        # (2) resolve next, including the stage-dependent transition
        nxt = rule["next"]
        if nxt == "ANALYZING_OR_READY_COMPLETE":
            st["stageIndex"] += 1
            st["stagesCompleted"] += 1
            nxt = "READY_COMPLETE" if st["stageIndex"] == st["stageCount"] \
                else "ANALYZING"
        # (3) terminal
        if "terminal" in rule:
            st["terminalKind"] = rule["terminal"]
        # (4) phase
        st["phase"] = nxt
        return st, rule["id"]

    # --- noMatchLaw --------------------------------------------------------
    st["phase"] = "FAULT"
    return st, "P3-34"


def trace(events, stage_count=1):
    st = initial_state(stage_count)
    out = []
    for ev in events:
        frame = ev if isinstance(ev, str) else ev[0]
        payload = None if isinstance(ev, str) else ev[1]
        st, tid = step(st, frame, payload)
        out.append({"frame": frame, "rule": tid, "phase": st["phase"],
                    "terminalKind": st["terminalKind"],
                    "identityNegotiated": st["identityNegotiated"],
                    "sourceBytesSent": st["sourceBytesSent"],
                    "stagesCompleted": st["stagesCompleted"]})
    return st, out


HELLO_ACK_OK = ("HelloAck", {"capabilities": sorted(
    IDENTITY_TOKENS | {"sealed-vfs-v1", "multi-stage-analyze-v1",
                       "rust-semantic-facts-v1", "resolution-completeness-v2",
                       "unresolved-edge-v1", "dependency-source-v1",
                       "native-context-v2"})})
HELLO_ACK_V1_ONLY = ("HelloAck", {"capabilities": ["rust-semantic-facts-v1"]})
OPEN_PLAIN = ("OpenUniverse", {"dependencyMode": False, "preparedMode": False})
OPEN_DEPS = ("OpenUniverse", {"dependencyMode": True, "preparedMode": False})


def pairwise_disjoint():
    """The published claim that the rows are pairwise disjoint, checked."""
    def expand(rule):
        phases = (TBL["wildcards"]["*PRE_COMPLETE"]["phases"]
                  if rule["phase"] == "*PRE_COMPLETE" else [rule["phase"]])
        return [(p, rule["frame"], tuple(sorted(rule.get("guard", {}).items())))
                for p in phases]
    seen = {}
    clashes = []
    for rule in RULES:
        for p, f, g in expand(rule):
            key = (p, f)
            for g2, rid2 in seen.get(key, []):
                if _guards_can_coincide(dict(g), dict(g2)):
                    clashes.append((rule["id"], rid2, p, f))
            seen.setdefault(key, []).append((g, rule["id"]))
    return clashes


def _guards_can_coincide(a, b):
    for k in set(a) & set(b):
        if a[k] != b[k]:
            return False
    return True
