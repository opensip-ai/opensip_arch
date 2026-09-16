"""Host-side typescript-semantic protocol major-2 event machine (source44).

Normative source: docs/coop/design-corrections/native/typescript-protocol2-order.v1.json, READ AT RUNTIME. Rows, order, guards, wildcards,
pre-match/no-match laws, state updates, the stage-dependent transition of T2-13 and the terminal law all come from that table; nothing is copied here.
Guard keys name host state fields or the table's derived event observations (eventObservations: unavailablePayload, capabilities). An event carries
those observations under "observations"; ref/provider_exchange.py derives them from admitted payloads (native-evidence s9.7).
The table does not model framing bytes, byte limits or exit-status policy after Cancelled.
"""
import copy
import json

KIT = '/private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/subject/docs/'
TABLE_PATH = KIT + 'coop/design-corrections/native/typescript-protocol2-order.v1.json'
IDENTITY_TOKENS = ["source-identity-snapshot2", "plan-identity-plan2", "fact-identity-fact2", "coverage-v3"]


class TypeScriptProtocol2:
    def __init__(self, table=None):
        self.t = table or json.load(open(TABLE_PATH, "rb"))
        self.rules = self.t["rules"]
        assert len(self.rules) == self.t["ruleCount"] == 23
        self.pre_terminal = set(self.t["wildcards"]["*PRE_TERMINAL"]["phases"])
        # derivation check: *PRE_TERMINAL is START through READY_COMPLETE of the published phase list
        assert self.t["wildcards"]["*PRE_TERMINAL"]["phases"] == self.t["phases"][0:11]
        self.process_fault = set(self.t["wildcards"]["*PROCESS_FAULT"]["frames"])
        self.observation_keys = set(self.t["eventObservations"])

    def run(self, events):
        state = copy.copy(self.t["initialState"])
        trace = []
        for ev in events:
            frame = ev["frame"]
            if state["phase"] == "FAULT":
                trace.append({"frame": frame, "rule": "FAULT-absorb", "phase": "FAULT"})
                continue
            if state["phase"] in ("WAIT_ZERO_EXIT", "WAIT_EOF", "DONE") and frame not in ("zero-exit", "eof") and frame not in self.process_fault:
                state["phase"] = "FAULT"
                trace.append({"frame": frame, "rule": "post-terminal-frame", "phase": "FAULT"})
                continue
            if frame in self.process_fault:
                state["phase"] = "FAULT"
                trace.append({"frame": frame, "rule": "T2-22", "phase": "FAULT"})
                continue
            row = self._match(state, ev)
            if row is None:
                state["phase"] = "FAULT"
                trace.append({"frame": frame, "rule": "T2-23", "phase": "FAULT"})
                continue
            prior_phase = state["phase"]
            self._updates(state, ev, prior_phase)
            nxt = row["next"]
            if nxt == "ANALYZING_OR_READY_COMPLETE":
                state["stageIndex"] += 1
                state["stagesCompleted"] += 1
                nxt = "READY_COMPLETE" if state["stageIndex"] == state["stageCount"] else "ANALYZING"
            if "terminal" in row:
                state["terminalKind"] = row["terminal"]
            state["phase"] = nxt
            trace.append({"frame": frame, "rule": row["id"], "phase": nxt})
        return {"state": state, "trace": trace}

    def _guard_value(self, state, ev, key):
        if key in self.observation_keys:
            return (ev.get("observations") or {}).get(key)
        return state.get(key)

    def _match(self, state, ev):
        for row in self.rules:
            if row["phase"] == "*ANY":
                continue
            if row["phase"] == "*PRE_TERMINAL":
                if state["phase"] not in self.pre_terminal:
                    continue
            elif row["phase"] != state["phase"]:
                continue
            if row["frame"] != ev["frame"]:
                continue
            if all(self._guard_value(state, ev, k) == v for k, v in row.get("guard", {}).items()):
                return row
        return None

    def _updates(self, state, ev, prior_phase):
        frame = ev["frame"]
        if frame == "HelloAck":
            caps = (ev.get("observations") or {}).get("capabilities") or []
            state["identityNegotiated"] = all(tok in caps for tok in IDENTITY_TOKENS)
        if frame == "Analyze":
            state["stageCount"] = ev["stageCount"]
            state["stageIndex"] = 0
            state["outputSeen"] = False
        if frame in ("FactBatch", "Coverage"):
            state["outputSeen"] = True
        if frame == "Cancel":
            state["cancelPhase"] = prior_phase
        if frame in ("OpenUniverse", "SnapshotFileChunk", "SnapshotManifest"):
            state["sourceBytesSent"] = True

    def pairwise_disjoint(self):
        overlaps = []
        rows = [r for r in self.rules if r["phase"] != "*ANY"]
        for i, a in enumerate(rows):
            for b in rows[i + 1:]:
                pa = self.pre_terminal if a["phase"] == "*PRE_TERMINAL" else {a["phase"]}
                pb = self.pre_terminal if b["phase"] == "*PRE_TERMINAL" else {b["phase"]}
                if not (pa & pb) or a["frame"] != b["frame"]:
                    continue
                ga, gb = a.get("guard", {}), b.get("guard", {})
                if any(k in gb and gb[k] != v for k, v in ga.items()):
                    continue
                overlaps.append((a["id"], b["id"]))
        return overlaps
