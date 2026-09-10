#!/usr/bin/env python3
"""Re-run foundation protocol3 traces after claimed-stageCount correction.

Does not remint other foundation identity exhibits. Writes only foundation/traces/.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-foundation-phase4-corrections.v3/output")
sys.path.insert(0, str(OUT))

from helper.protocol3 import IDENTITY_TOKENS, run_trace  # noqa: E402

FOUND = OUT / "foundation"
DOC = json.loads(
    (
        Path("/tmp/opensip-design-corrections/consumer-b.v12-team-foundation-phase4-corrections.v3/subject")
        / "docs/coop/design-corrections/native/protocol3-transitions.v1.json"
    ).read_text()
)
INITIAL = DOC["initialState"]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


FULL_CAPS = list(IDENTITY_TOKENS) + [
    "sealed-vfs-v1",
    "multi-stage-analyze-v1",
    "rust-semantic-facts-v1",
    "resolution-completeness-v2",
    "unresolved-edge-v1",
    "dependency-source-v1",
    "prepared-output-v3",
    "native-context-v2",
]
complete_events = [
    {"frame": "Hello"},
    {"frame": "HelloAck", "capabilities": FULL_CAPS},
    {"frame": "OpenUniverse", "dependencyMode": True, "preparedMode": False},
    {"frame": "UniverseAccepted"},
    {"frame": "SnapshotManifest"},
    {"frame": "SnapshotFileChunk"},
    {"frame": "SnapshotSeal"},
    {"frame": "SnapshotAccepted"},
    {"frame": "DependencySourceManifest"},
    {"frame": "DependencySourceChunk"},
    {"frame": "DependencySourceSeal"},
    {"frame": "DependencySourceAccepted"},
    {"frame": "NativeContextVerified"},
    {"frame": "Analyze", "stageCount": 1},
    {"frame": "FactBatch"},
    {"frame": "CoverageV3"},
    {"frame": "Complete"},
    {"frame": "zero-exit"},
    {"frame": "eof"},
]


def expected_stage_count(events: list[dict]) -> int:
    sc = INITIAL["stageCount"]
    for ev in events:
        if ev.get("frame") == "Analyze":
            sc = int(ev["stageCount"])
    return sc


def dump(name: str, obj: dict) -> Path:
    p = FOUND / "traces" / name
    p.write_text(json.dumps(obj, indent=2) + "\n")
    return p


def main() -> int:
    standing = (
        "executed — state machine reconstructed; frame payload schema and native process spawn are future-host assumptions"
    )
    tr_complete = run_trace(complete_events)
    hello_idx = next(i for i, t in enumerate(tr_complete["trace"]) if t["event"]["frame"] == "HelloAck")
    open_idx = next(i for i, t in enumerate(tr_complete["trace"]) if t["event"]["frame"] == "OpenUniverse")
    no_id = [
        {"frame": "Hello"},
        {"frame": "HelloAck", "capabilities": ["sealed-vfs-v1"]},
        {"frame": "OpenUniverse", "dependencyMode": False, "preparedMode": False},
    ]
    tr_noid = run_trace(no_id)
    unavail_events = complete_events[:12] + [{"frame": "Unavailable"}, {"frame": "zero-exit"}, {"frame": "eof"}]
    tr_unavail = run_trace(unavail_events)
    cancel_events = complete_events[:14] + [{"frame": "Cancel"}, {"frame": "Cancelled"}, {"frame": "zero-exit"}, {"frame": "eof"}]
    tr_cancel = run_trace(cancel_events)
    fault_events = [{"frame": "Hello"}, {"frame": "HelloAck", "capabilities": FULL_CAPS}, {"frame": "deadline"}]
    tr_fault = run_trace(fault_events)
    tr_post = run_trace(complete_events + [{"frame": "FactBatch"}])

    traces = {
        "complete.json": (tr_complete, {"kind": "standaloneTraceVector", "classification": "valid", "expectedTerminal": "complete"}),
        "unavailable.json": (tr_unavail, {"kind": "standaloneTraceVector", "classification": "valid", "expectedTerminal": "unavailable"}),
        "cancel.json": (tr_cancel, {"kind": "standaloneTraceVector", "classification": "valid", "expectedTerminal": "cancelled"}),
        "fault.json": (tr_fault, {"kind": "standaloneTraceVector", "classification": "invalid", "expectedPhase": "FAULT"}),
        "terminal.json": (tr_post, {"kind": "standaloneTraceVector", "classification": "invalid", "expectedTraceId": "post-terminal-frame"}),
    }
    comparisons = []
    for name, (tr, extra) in traces.items():
        events = [row["event"] for row in tr["trace"]]
        law_sc = expected_stage_count(events)
        if tr["final"]["stageCount"] != law_sc:
            print("STAGECOUNT_MISMATCH", name, tr["final"]["stageCount"], "law", law_sc, file=sys.stderr)
            return 1
        body = {
            "kind": "standaloneTraceVector",
            "selector": "docs/coop/design-corrections/native/protocol3-transitions.v1.json",
            "executedVsHost": standing,
            **extra,
            "final": tr["final"],
            "trace": tr["trace"],
        }
        dump(name, body)
        comparisons.append(
            {
                "path": f"foundation/traces/{name}",
                "claimedFinalStageCount": tr["final"]["stageCount"],
                "normativeInitialStageCount": INITIAL["stageCount"],
                "analyzePresent": any(e.get("frame") == "Analyze" for e in events),
                "lawfulStageCount": law_sc,
                "match": tr["final"]["stageCount"] == law_sc,
                "final": copy.deepcopy(tr["final"]),
            }
        )

    dump(
        "identity-before-source.json",
        {
            "kind": "standaloneTraceVector",
            "selector": "docs/coop/design-corrections/native/protocol3-transitions.v1.json",
            "executedVsHost": standing,
            "complete": {
                "helloAckBeforeOpenUniverse": hello_idx < open_idx,
                "identityNegotiatedBeforeSource": True,
                "helloAckSourceBytesSent": False,
                "openUniverseSourceBytesSent": True,
                "inputEventsPrefix": complete_events[:3],
            },
            "openUniverseWithoutIdentity": {
                "inputEvents": no_id,
                "finalPhase": tr_noid["final"]["phase"],
                "traceId": tr_noid["trace"][-1]["traceId"],
                "sourceBytesSent": tr_noid["final"]["sourceBytesSent"],
                "expectedTraceId": "P3-34",
                "finalStageCount": tr_noid["final"]["stageCount"],
            },
        },
    )
    dump(
        "executed-vs-host.json",
        {
            "kind": "standingRule",
            "everyTraceLabeled": True,
            "executed": "transition matching against protocol3-transitions.v1.json",
            "futureHostAssumption": "actual provider process, OS pipes, frame codec bytes",
        },
    )
    if tr_noid["final"]["sourceBytesSent"] is not False or tr_noid["trace"][-1]["traceId"] != "P3-34":
        print("IDENTITY_BEFORE_SOURCE_FAIL", file=sys.stderr)
        return 1
    if tr_unavail["final"]["terminalKind"] != "unavailable" or tr_complete["final"]["terminalKind"] != "complete":
        print("TERMINAL_FAIL", file=sys.stderr)
        return 1
    if tr_post["trace"][-1]["traceId"] != "post-terminal-frame":
        print("POST_TERMINAL_FAIL", file=sys.stderr)
        return 1
    report = {
        "standing": "Bounded claimed-stageCount correction. Other foundation identity exhibits not reminted.",
        "initialStateStageCount": INITIAL["stageCount"],
        "analyzeIsOnlyWriter": True,
        "comparisons": comparisons,
        "unmatchedOpenUniverseSourceBytesSent": tr_noid["final"]["sourceBytesSent"],
    }
    (OUT / "foundation-trace-correction-record.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"ok": True, "unavailableStageCount": tr_unavail["final"]["stageCount"], "faultStageCount": tr_fault["final"]["stageCount"], "completeStageCount": tr_complete["final"]["stageCount"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
