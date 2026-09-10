#!/usr/bin/env python3
"""Bounded successor recheck of protocol3 standalone traces.

Reads: original 80-file kit (protocol3 + native-evidence identity tokens),
this bundle's data-manifest and raw trace JSON, and (for disposition only)
this origin's prior review finding. Claimed finals are comparison targets,
never oracles.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

PREV = Path("/tmp/opensip-design-corrections/consumer-b.v12-fresh-foundation-data-review.v1")
KIT = PREV / "subject"
HERE = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-foundation-trace-recheck.v1")
DATA = HERE / "data"
OUT = Path(__file__).resolve().parent
PY = "/tmp/opensip-architecture-review-env/bin/python"

MANIFEST_EXPECTED = "ffe67281dd8fc681310797d9f3c79f9e7463d58921da6e36e4edda01e858414c"
KIT_MANIFEST_EXPECTED = "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8"

IDENTITY_TOKENS = {
    "source-identity-snapshot2",
    "plan-identity-plan2",
    "fact-identity-fact2",
    "coverage-v3",
}
SOURCE_BYTE_FRAMES = {
    "DependencySourceChunk",
    "DependencySourceManifest",
    "OpenUniverse",
    "PreparedOutputChunk",
    "PreparedOutputManifest",
    "SnapshotFileChunk",
    "SnapshotManifest",
}
STEP_FIELDS = ("traceId", "phaseAfter", "identityNegotiated", "sourceBytesSent", "terminalKind")
FINAL_FIELDS = (
    "phase",
    "dependencyMode",
    "preparedMode",
    "identityNegotiated",
    "stageIndex",
    "stageCount",
    "terminalKind",
    "sourceBytesSent",
    "stagesCompleted",
)


def sha256_file(p: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest(), p.stat().st_size


def load(p: Path):
    return json.loads(p.read_text())


def protocol_step(doc: dict, state: dict, event: dict) -> tuple[str, dict]:
    frame = event["frame"]
    phase = state["phase"]
    wild = doc["wildcards"]
    pre_complete = set(wild["*PRE_COMPLETE"]["phases"])
    process_fault = set(wild["*PROCESS_FAULT"]["frames"])

    if phase == "FAULT":
        return "FAULT-absorb", state

    if phase in {"WAIT_ZERO_EXIT", "WAIT_EOF", "DONE"}:
        if frame not in {"zero-exit", "eof"} and frame not in process_fault:
            st = dict(state)
            st["phase"] = "FAULT"
            return "post-terminal-frame", st

    if frame in process_fault:
        st = dict(state)
        st["phase"] = "FAULT"
        return "P3-33", st

    st = dict(state)
    matched = None
    for row in doc["rules"]:
        if row["id"] in {"P3-33", "P3-34"}:
            continue
        row_phase = row["phase"]
        phase_ok = (row_phase == phase) or (row_phase == "*PRE_COMPLETE" and phase in pre_complete)
        if not phase_ok:
            continue
        if row["frame"] != frame:
            continue
        guard = row.get("guard") or {}
        if all(st.get(k) == v for k, v in guard.items()):
            matched = row
            break

    if matched is None:
        st["phase"] = "FAULT"
        return "P3-34", st

    # stateUpdates apply only after a successful row match.
    _apply_frame_updates(st, event)

    nxt = matched["next"]
    if nxt == "ANALYZING_OR_READY_COMPLETE":
        st["stageIndex"] = st.get("stageIndex", 0) + 1
        st["stagesCompleted"] = st.get("stagesCompleted", 0) + 1
        nxt = "READY_COMPLETE" if st["stageIndex"] == st.get("stageCount", 0) else "ANALYZING"
    if "terminal" in matched:
        st["terminalKind"] = matched["terminal"]
    st["phase"] = nxt
    return matched["id"], st


def _apply_frame_updates(st: dict, event: dict) -> None:
    frame = event["frame"]
    if frame == "HelloAck":
        caps = set(event.get("capabilities") or [])
        st["identityNegotiated"] = IDENTITY_TOKENS.issubset(caps)
    if frame == "OpenUniverse":
        st["dependencyMode"] = bool(event.get("dependencyMode", False))
        st["preparedMode"] = bool(event.get("preparedMode", False))
    if frame == "Analyze":
        st["stageCount"] = int(event.get("stageCount", 0))
        st["stageIndex"] = 0
    if frame in SOURCE_BYTE_FRAMES:
        st["sourceBytesSent"] = True


def run_trace(doc: dict, events: list[dict]) -> tuple[list[dict], dict]:
    state = copy.deepcopy(doc["initialState"])
    steps = []
    for ev in events:
        tid, state = protocol_step(doc, state, ev)
        steps.append(
            {
                "event": ev,
                "traceId": tid,
                "phaseAfter": state["phase"],
                "identityNegotiated": state["identityNegotiated"],
                "sourceBytesSent": state["sourceBytesSent"],
                "terminalKind": state["terminalKind"],
                "computedState": {
                    k: state[k]
                    for k in FINAL_FIELDS
                },
            }
        )
    return steps, state


def compare_trace(name: str, path: Path, doc: dict, expect_terminal=None, expect_phase=None) -> dict:
    ex = load(path)
    events = [step["event"] for step in ex["trace"]]
    steps, final = run_trace(doc, events)
    step_mismatches = []
    for claimed, got in zip(ex["trace"], steps):
        for fld in STEP_FIELDS:
            if claimed.get(fld) != got.get(fld):
                step_mismatches.append(
                    {
                        "event": claimed["event"]["frame"],
                        "field": fld,
                        "claimed": claimed.get(fld),
                        "computed": got.get(fld),
                    }
                )
        labeled = claimed.get("executedVsHost")
        if not labeled:
            step_mismatches.append(
                {
                    "event": claimed["event"]["frame"],
                    "field": "executedVsHost",
                    "claimed": labeled,
                    "computed": "required-label",
                }
            )
    if len(ex["trace"]) != len(steps):
        step_mismatches.append(
            {"field": "nSteps", "claimed": len(ex["trace"]), "computed": len(steps)}
        )
    final_cmp = []
    claimed_final = ex.get("final") or {}
    all_final_ok = True
    for k in FINAL_FIELDS:
        claimed_v = claimed_final.get(k, "__missing__")
        computed_v = final.get(k)
        match = claimed_v == computed_v
        if not match:
            all_final_ok = False
        final_cmp.append(
            {
                "field": k,
                "claimed": claimed_final.get(k),
                "computed": computed_v,
                "match": match,
            }
        )
    extra_claimed = sorted(set(claimed_final) - set(FINAL_FIELDS))
    missing_claimed = sorted(set(FINAL_FIELDS) - set(claimed_final))
    terminal_ok = expect_terminal is None or final.get("terminalKind") == expect_terminal
    phase_ok = expect_phase is None or final.get("phase") == expect_phase
    ok = (
        not step_mismatches
        and all_final_ok
        and not extra_claimed
        and not missing_claimed
        and terminal_ok
        and phase_ok
    )
    return {
        "name": name,
        "path": str(path.relative_to(HERE)),
        "sha256": sha256_file(path)[0],
        "bytes": path.stat().st_size,
        "ok": ok,
        "nEvents": len(events),
        "eventFrames": [e["frame"] for e in events],
        "stepMismatches": step_mismatches,
        "finalComparisons": final_cmp,
        "allFinalFieldsMatch": all_final_ok,
        "extraClaimedFinalFields": extra_claimed,
        "missingClaimedFinalFields": missing_claimed,
        "computedFinal": {k: final[k] for k in FINAL_FIELDS},
        "claimedFinal": claimed_final,
        "executedVsHost": ex.get("executedVsHost"),
        "classification": ex.get("classification"),
        "expectedTerminalClaim": ex.get("expectedTerminal") or ex.get("expectedPhase") or ex.get("expectedTraceId"),
        "independentTerminalKind": final.get("terminalKind"),
        "independentPhase": final.get("phase"),
        "selector": ex.get("selector"),
        "analyzeSent": any(e.get("frame") == "Analyze" for e in events),
    }


def main() -> int:
    protocol_path = KIT / "docs/coop/design-corrections/native/protocol3-transitions.v1.json"
    protocol = load(protocol_path)
    kit_man_sha, _ = sha256_file(KIT / "consumer-input-manifest.json")

    man_path = HERE / "data-manifest.json"
    man_sha, man_bytes = sha256_file(man_path)
    man = load(man_path)
    file_rows = []
    for rec in man["files"]:
        p = HERE / rec["path"]
        actual, size = sha256_file(p)
        file_rows.append(
            {
                "path": rec["path"],
                "expected_sha256": rec["sha256"],
                "actual_sha256": actual,
                "expected_bytes": rec["bytes"],
                "actual_bytes": size,
                "match": actual == rec["sha256"] and size == rec["bytes"],
            }
        )

    prior_review = load(PREV / "output/foundation-data-review.json")
    prior_finding = None
    for issue in prior_review.get("newShouldIssues") or []:
        if issue.get("id") == "FD-SHOULD-TRACE-STAGECOUNT-WITHOUT-ANALYZE":
            prior_finding = issue
            break

    traces_dir = DATA / "traces"
    complete = compare_trace("complete", traces_dir / "complete.json", protocol, expect_terminal="complete", expect_phase="DONE")
    unavailable = compare_trace("unavailable", traces_dir / "unavailable.json", protocol, expect_terminal="unavailable", expect_phase="DONE")
    cancel = compare_trace("cancel", traces_dir / "cancel.json", protocol, expect_terminal="cancelled", expect_phase="DONE")
    fault = compare_trace("fault", traces_dir / "fault.json", protocol, expect_terminal=None, expect_phase="FAULT")
    terminal = compare_trace("terminal", traces_dir / "terminal.json", protocol, expect_terminal="complete", expect_phase="FAULT")

    # Discriminatory identity-before-source
    ibs = load(traces_dir / "identity-before-source.json")
    psteps, pfinal = run_trace(protocol, ibs["complete"]["inputEventsPrefix"])
    prefix_computed = {
        "helloAckBeforeOpenUniverse": psteps[1]["traceId"] == "P3-02" and psteps[2]["traceId"] == "P3-03",
        "identityNegotiatedBeforeSource": (
            psteps[1]["identityNegotiated"] is True
            and psteps[1]["sourceBytesSent"] is False
            and psteps[2]["sourceBytesSent"] is True
        ),
        "helloAckSourceBytesSent": psteps[1]["sourceBytesSent"],
        "openUniverseSourceBytesSent": psteps[2]["sourceBytesSent"],
    }
    prefix_claimed = {
        "helloAckBeforeOpenUniverse": ibs["complete"]["helloAckBeforeOpenUniverse"],
        "identityNegotiatedBeforeSource": ibs["complete"]["identityNegotiatedBeforeSource"],
        "helloAckSourceBytesSent": ibs["complete"]["helloAckSourceBytesSent"],
        "openUniverseSourceBytesSent": ibs["complete"]["openUniverseSourceBytesSent"],
    }
    prefix = {
        **prefix_computed,
        "computedPrefixFinal": {k: pfinal[k] for k in FINAL_FIELDS},
        "computedHelloAck": {
            "traceId": psteps[1]["traceId"],
            "identityNegotiated": psteps[1]["identityNegotiated"],
            "sourceBytesSent": psteps[1]["sourceBytesSent"],
        },
        "computedOpenUniverse": {
            "traceId": psteps[2]["traceId"],
            "identityNegotiated": psteps[2]["identityNegotiated"],
            "sourceBytesSent": psteps[2]["sourceBytesSent"],
        },
        "claimed": prefix_claimed,
        "matchClaimed": prefix_computed == prefix_claimed,
    }
    nsteps, nfinal = run_trace(protocol, ibs["openUniverseWithoutIdentity"]["inputEvents"])
    neg = {
        "computedPhase": nfinal["phase"],
        "computedTraceId": nsteps[-1]["traceId"] if nsteps else None,
        "computedSourceBytesSent": nfinal["sourceBytesSent"],
        "computedIdentityNegotiated": nfinal["identityNegotiated"],
        "computedStageCount": nfinal["stageCount"],
        "computedFinal": {k: nfinal[k] for k in FINAL_FIELDS},
        "claimed": {
            "finalPhase": ibs["openUniverseWithoutIdentity"]["finalPhase"],
            "traceId": ibs["openUniverseWithoutIdentity"]["traceId"],
            "sourceBytesSent": ibs["openUniverseWithoutIdentity"]["sourceBytesSent"],
            "finalStageCount": ibs["openUniverseWithoutIdentity"].get("finalStageCount"),
        },
        "matchClaimed": (
            nfinal["phase"] == ibs["openUniverseWithoutIdentity"]["finalPhase"]
            and nsteps[-1]["traceId"] == ibs["openUniverseWithoutIdentity"]["traceId"]
            and nfinal["sourceBytesSent"] is ibs["openUniverseWithoutIdentity"]["sourceBytesSent"]
            and nfinal["stageCount"] == ibs["openUniverseWithoutIdentity"].get("finalStageCount")
        ),
    }
    ibs_ok = prefix["matchClaimed"] and prefix["identityNegotiatedBeforeSource"] and neg["matchClaimed"]
    ibs_sha, ibs_bytes = sha256_file(traces_dir / "identity-before-source.json")

    evh = load(traces_dir / "executed-vs-host.json")
    every_labeled = all(
        t.get("executedVsHost") for t in (complete, unavailable, cancel, fault, terminal)
    ) and all(s.get("executedVsHost") for s in load(traces_dir / "complete.json")["trace"])
    evh_ok = bool(
        evh.get("everyTraceLabeled") is True
        and evh.get("executed")
        and evh.get("futureHostAssumption")
        and every_labeled
        and complete.get("executedVsHost")
        and unavailable.get("executedVsHost")
        and cancel.get("executedVsHost")
        and fault.get("executedVsHost")
        and terminal.get("executedVsHost")
        and ibs.get("executedVsHost")
    )

    # Prior finding disposition: existing-law correction of claimed stageCount.
    unav_sc = next(x for x in unavailable["finalComparisons"] if x["field"] == "stageCount")
    fault_sc = next(x for x in fault["finalComparisons"] if x["field"] == "stageCount")
    prior_disposition = {
        "priorIssueId": "FD-SHOULD-TRACE-STAGECOUNT-WITHOUT-ANALYZE",
        "priorSelector": (prior_finding or {}).get("selector"),
        "priorFinding": (prior_finding or {}).get("finding"),
        "law": "protocol3-transitions.v1.json initialState.stageCount=0; Analyze is the only stateUpdate that writes stageCount.",
        "classification": "existing-law-correction",
        "notMissingLaw": True,
        "unavailable": {
            "analyzeSent": unavailable["analyzeSent"],
            "claimedStageCount": unav_sc["claimed"],
            "computedStageCount": unav_sc["computed"],
            "match": unav_sc["match"],
        },
        "fault": {
            "analyzeSent": fault["analyzeSent"],
            "claimedStageCount": fault_sc["claimed"],
            "computedStageCount": fault_sc["computed"],
            "match": fault_sc["match"],
        },
        "identityBeforeSourceNegative": {
            "claimedFinalStageCount": ibs["openUniverseWithoutIdentity"].get("finalStageCount"),
            "computedStageCount": nfinal["stageCount"],
            "match": ibs["openUniverseWithoutIdentity"].get("finalStageCount") == nfinal["stageCount"],
        },
        "closed": bool(unav_sc["match"] and fault_sc["match"] and nfinal["stageCount"] == 0),
    }

    kinds_ok = all(t["ok"] for t in (complete, unavailable, cancel, fault, terminal))
    hashes_ok = man_sha == MANIFEST_EXPECTED and all(r["match"] for r in file_rows)
    kit_ok = kit_man_sha == KIT_MANIFEST_EXPECTED

    failed = []
    if not complete["ok"]:
        failed.append("R-TRACE-COMPLETE")
    if not unavailable["ok"]:
        failed.append("R-TRACE-UNAVAILABLE")
    if not cancel["ok"]:
        failed.append("R-TRACE-CANCEL")
    if not fault["ok"]:
        failed.append("R-TRACE-FAULT")
    if not ibs_ok:
        failed.append("R-TRACE-IDENTITY-BEFORE-SOURCE")
    if not terminal["ok"]:
        failed.append("R-TRACE-TERMINAL")
    if not evh_ok:
        failed.append("R-TRACE-EXECUTED-VS-HOST")

    if not hashes_ok or not kit_ok:
        verdict = "TRACE_DATA_INCOMPLETE"
    elif failed:
        verdict = "TRACE_DATA_REFUSED"
    else:
        verdict = "TRACE_DATA_ADMITS"

    results = {
        "checker": "trace_recheck.py",
        "command": f"{PY} -I -B {OUT / 'trace_recheck.py'}",
        "verdict": verdict,
        "scope": "Bounded successor recheck of original phase-3 standalone traces only. Not a full Run, not whole-consumer ACCEPT. Unchanged other foundation data retains previous scoped standing.",
        "hashVerification": {
            "dataManifest": {
                "expected": MANIFEST_EXPECTED,
                "actual": man_sha,
                "bytes": man_bytes,
                "match": man_sha == MANIFEST_EXPECTED,
            },
            "kitManifest": {
                "expected": KIT_MANIFEST_EXPECTED,
                "actual": kit_man_sha,
                "match": kit_ok,
            },
            "files": file_rows,
            "allMatch": hashes_ok and kit_ok,
        },
        "changedVsPriorReview": {
            "unavailable": "stageCount claimed 1 -> 0",
            "fault": "stageCount claimed 1 -> 0",
            "identity-before-source": "added finalStageCount=0 on openUniverseWithoutIdentity",
            "unchangedByteIdentical": [
                "data/traces/complete.json",
                "data/traces/cancel.json",
                "data/traces/terminal.json",
                "data/traces/executed-vs-host.json",
            ],
        },
        "priorFindingDisposition": prior_disposition,
        "traces": {
            "complete": complete,
            "unavailable": unavailable,
            "cancel": cancel,
            "fault": fault,
            "terminal": terminal,
        },
        "discriminatory": {
            "identityBeforeSource": {
                "ok": ibs_ok,
                "sha256": ibs_sha,
                "bytes": ibs_bytes,
                "prefix": prefix,
                "openUniverseWithoutIdentity": neg,
                "executedVsHost": ibs.get("executedVsHost"),
            },
            "executedVsHostFile": evh,
            "executedVsHostOk": evh_ok,
        },
        "requirementMapping": {
            "R-TRACE-COMPLETE": complete["ok"],
            "R-TRACE-UNAVAILABLE": unavailable["ok"],
            "R-TRACE-CANCEL": cancel["ok"],
            "R-TRACE-FAULT": fault["ok"],
            "R-TRACE-IDENTITY-BEFORE-SOURCE": ibs_ok,
            "R-TRACE-TERMINAL": terminal["ok"],
            "R-TRACE-EXECUTED-VS-HOST": evh_ok,
        },
        "failedIds": failed,
        "existingLawMisses": [],
        "missingOrContradictoryNorm": [],
        "limitations": [
            "Frame payload schema validation, OS pipes, and native process spawn remain future-host assumptions.",
            "This recheck does not re-run unchanged non-trace foundation exhibits; they retain previous scoped standing only.",
            "Standalone traces are not upgraded to complete Runs or whole-consumer ACCEPT.",
            "S-* author-process custody remains external-root-custody-required from the prior review.",
        ],
    }

    (OUT / "trace-recheck-results.json").write_text(json.dumps(results, indent=2, default=str) + "\n")
    print(json.dumps({"verdict": verdict, "failed": failed, "priorClosed": prior_disposition["closed"]}, indent=2))
    return 0 if verdict == "TRACE_DATA_ADMITS" else 1


if __name__ == "__main__":
    sys.exit(main())
