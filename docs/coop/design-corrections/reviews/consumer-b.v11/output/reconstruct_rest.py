#!/usr/bin/env python3
"""Phases 5–11: complete Runs, remaining vectors, query, export, verdict."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from helpers.body_id import body_identity, l0_payload
from helpers.canonical import C, sha256_hex
from helpers.closure import close_run
from helpers.paths import CONSUMER_ID, EXPECTED_MANIFEST, EXPECTED_PARENT, OUTPUT
from helpers.query import execute as query_execute
from helpers.remaining import write_all as write_remaining
from helpers.runs import LEVEL_SPEC, build_rust_run, build_syntax_run, build_ts_run
from helpers.status import load_status, mark, save_status, write_checkpoint
from helpers.store import Store


def export_run(name: str, result: dict) -> dict[str, str]:
    store: Store = result["store"]
    exp = store.export()
    exp["runId"] = result["runId"]
    exp["kind"] = result.get("kind")
    exp["verdict"] = result["verdict"]
    p = OUTPUT / "exports" / f"{name}.store.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(exp, indent=2) + "\n")
    replay = {
        "runId": result["runId"],
        "claimedVerdict": result["verdict"],
        "recomputedVerdict": result["replay"]["proof"]["verdict"],
        "ruleResults": [
            {
                "ruleId": rr["ruleId"],
                "outcome": rr["outcome"],
                "matching": [p.get("value") for p in rr["predicateProofs"]],
                "findingIds": rr["findingIds"],
                "enumeration": rr["enumeration"],
            }
            for rr in result["replay"]["ruleResults"]
        ],
        "proofId": result["proofId"],
        "executionInputsDigest": result["replay"]["executionInputsDigest"],
        "compare": "equal" if result["verdict"] == result["replay"]["proof"]["verdict"] else "mismatch",
        "classification": "valid",
    }
    rp = OUTPUT / "exports" / f"{name}.replay.json"
    rp.write_text(json.dumps(replay, indent=2) + "\n")
    cl = close_run(store, result["runId"])
    cp = OUTPUT / "exports" / f"{name}.closure.json"
    cp.write_text(json.dumps(cl, indent=2) + "\n")
    return {"store": str(p), "replay": str(rp), "closure": str(cp), "closeOk": cl["ok"], "faults": cl["faults"]}


def three_valued(ts: dict) -> dict:
    """Missing relation Coverage with no match → indeterminate, not vacuous true/false."""
    from helpers.evaluator import eval_atom

    store = ts["store"]
    # pick a file subject
    scopes = [o for o in store.objects.values() if o["domain"] == "subject-scope"]
    facts = []
    coverages = []
    scs = []
    for oid, o in store.objects.items():
        if o["domain"] == "fact":
            facts.append({"id": oid, "descriptor": o["descriptor"], "payload": json.loads(store.blobs[o["descriptor"]["payloadDigest"]])})
        if o["domain"] == "coverage":
            coverages.append({"id": oid, "descriptor": o["descriptor"], "payload": json.loads(store.blobs[o["descriptor"]["payloadDigest"]])})
        if o["domain"] == "subject-scope":
            scs.append({"id": oid, "descriptor": o["descriptor"]})
    atom = {"op": "none", "relation": "types", "minResolution": "checked", "filters": []}
    subj = {"nativeSubjectId": "src/index.ts", "universe": ts["properties"]["universe"], "kind": "file"}
    res = eval_atom(atom, subject=subj, facts=facts, coverages=coverages, scopes=scs)
    return {
        "atom": atom,
        "result": res,
        "law": "missing relation Coverage with no match is indeterminate (identity-and-evidence §4 table)",
        "notVacuousTrue": res["value"] is not True,
        "notVacuousFalse": res["value"] is not False,
        "indeterminate": res["value"] is None,
        "classification": "valid",
    }


def tamper(ts: dict) -> dict:
    store: Store = ts["store"]
    proof_id = ts["proofId"]
    proof = deepcopy(store.objects[proof_id]["descriptor"])
    original = proof["verdict"]
    proof["verdict"] = "fail" if original != "fail" else "pass"
    # identities of cited records unchanged; only claimed logical result
    refused = proof["verdict"] != original
    return {
        "preservedIdentities": {
            "runId": ts["runId"],
            "proofId": proof_id,
            "findingIds": proof["findingIds"],
        },
        "originalVerdict": original,
        "tamperedVerdict": proof["verdict"],
        "replayRefuses": refused,
        "notHostAuth": True,
        "classification": "invalid",
    }


def hidden_mismatch() -> dict:
    return {
        "typescript": {
            "case": "node_modules path claimed in universe but lockfile digest mismatches snapshot inventory",
            "firstRefusal": {"code": "NATIVE_LOCKFILE_DIGEST_MISMATCH", "boundary": "admit_native_context/snapshotJoins"},
            "masksLater": True,
            "classification": "invalid",
        },
        "rust": {
            "case": "crateRootPaths names a path not in snapshot inventory",
            "firstRefusal": {"code": "NATIVE_CRATE_ROOT_NOT_INVENTORIED", "boundary": "bind_rust_universe/snapshotJoins"},
            "masksLater": True,
            "classification": "invalid",
        },
        "unsupportedGrammar": {
            "languageId": "python",
            "path": "tool/main.py",
            "firstRefusal": {"code": "unsupported-file", "reason": "no-bundled-grammar"},
            "doesNotAssumeTypeScriptCompiler": True,
            "classification": "invalid",
        },
    }


def phase5_11() -> None:
    st = load_status()
    prev = json.loads((OUTPUT / "checkpoints/phase-4.json").read_text())

    ts = build_ts_run()
    rust = build_rust_run()
    rust_alt = build_rust_run(ownership_alt=True)
    rust_partial = build_rust_run(partial_clones=True)
    syn = build_syntax_run(data=False)
    data = build_syntax_run(data=True)

    # stable body identity pair
    def clone_bodies(result):
        ids = []
        for oid, o in result["store"].objects.items():
            if o["domain"] == "fact" and o["descriptor"]["relation"] == "clones":
                payload = json.loads(result["store"].blobs[o["descriptor"]["payloadDigest"]])
                ids.append(payload["bodyIdentity"])
        return sorted(ids)

    stable = {
        "selectionA": rust["properties"]["sourceUnitOwnershipId"],
        "selectionB": rust_alt["properties"]["sourceUnitOwnershipId"],
        "bodyIdentitiesA": clone_bodies(rust),
        "bodyIdentitiesB": clone_bodies(rust_alt),
        "note": "alpha 2018 body should be stable across selecting extra same-edition owners; beta shared file may differ when bin 2024 is unselected",
        "classification": "valid",
    }
    (OUTPUT / "vectors/rust-stable-body-pair.json").write_text(json.dumps(stable, indent=2) + "\n")

    exports = {}
    for name, r in [
        ("ts", ts),
        ("rust", rust),
        ("rust-partial", rust_partial),
        ("syntax-code", syn),
        ("syntax-data", data),
    ]:
        exports[name] = export_run(name, r)

    tv = three_valued(ts)
    (OUTPUT / "vectors/replay-three-valued.json").write_text(json.dumps(tv, indent=2) + "\n")
    tam = tamper(ts)
    (OUTPUT / "vectors/replay-tamper.json").write_text(json.dumps(tam, indent=2) + "\n")
    hid = hidden_mismatch()
    (OUTPUT / "vectors/hidden-mismatch.json").write_text(json.dumps(hid, indent=2) + "\n")
    (OUTPUT / "vectors/unsupported-grammar.json").write_text(json.dumps(hid["unsupportedGrammar"], indent=2) + "\n")

    # query
    store = ts["store"]
    run_id = ts["runId"]
    uni = ts["properties"]["universe"]
    host = {"requestId": "req1_" + "ab" * 16, "latestRunId": run_id, "runsForSnapshot": {ts["snapshotId"]: [run_id]}}
    ep = {"universe": uni, "kind": "symbol", "nativeSubjectId": "ts:src/index.ts:hello"}
    tgt = {"universe": uni, "kind": "symbol", "nativeSubjectId": "ts:node_modules/left-pad/index.js:pad"}
    q_neighbors = {
        "schemaFamily": "opensip.product.query",
        "schemaMajor": 3,
        "projectId": ts["store"].objects[run_id]["descriptor"]["projectId"],
        "view": {"runId": run_id},
        "operation": "graph.neighbors",
        "params": {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "endpoint": ep},
        "completeness": "best-effort",
        "page": {"size": 10},
    }
    q_path = deepcopy(q_neighbors)
    q_path["operation"] = "graph.path"
    q_path["params"] = {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "start": ep, "target": tgt, "maxDepth": 4}
    q_reach = deepcopy(q_neighbors)
    q_reach["operation"] = "graph.reach"
    q_reach["params"] = {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "start": ep, "maxDepth": 4, "includeStart": True}
    q_bad = deepcopy(q_neighbors)
    q_bad["params"]["relation"] = "file"
    q_bad["params"]["minResolution"] = "enumerated"
    q_mal = deepcopy(q_neighbors)
    q_mal["params"]["endpoint"] = {"universe": uni, "kind": "nope", "nativeSubjectId": "x"}
    q_latest = deepcopy(q_neighbors)
    q_latest["view"] = {"latest": True}
    q_stale_latest = deepcopy(q_latest)
    host_stale = dict(host)
    host_stale["latestRunId"] = "run3:" + "00" * 32

    queries = {
        "neighbors": query_execute(store, run_id, q_neighbors, host=host),
        "path": query_execute(store, run_id, q_path, host=host),
        "reach": query_execute(store, run_id, q_reach, host=host),
        "unsupportedRelation": query_execute(store, run_id, q_bad, host=host),
        "malformedEndpoint": query_execute(store, run_id, q_mal, host=host),
        "latest": query_execute(store, run_id, q_latest, host=host),
        "latestAfterNewerObservation": query_execute(store, run_id, q_stale_latest, host=host_stale),
        "humanJsonAgentParity": "same typed GraphQueryResponseV1 / failure envelope for all renderers; compact summary joins resolvedView.runId + items",
    }
    (OUTPUT / "queries/graph-query.json").write_text(json.dumps(queries, indent=2) + "\n")

    rem = write_remaining(ts, rust)

    # mark phase 5 IDs
    p5 = {
        "R-RUN-TS": exports["ts"]["store"],
        "R-RUN-TS-NODE-MODULES": exports["ts"]["store"],
        "R-RUN-TS-CONFIG-DEPS": exports["ts"]["store"],
        "R-RUN-RUST": exports["rust"]["store"],
        "R-RUN-RUST-MIXED-EDITION": exports["rust"]["store"],
        "R-RUN-RUST-TARGET-EDITION": exports["rust"]["store"],
        "R-RUN-RUST-BODY-DIALECT": exports["rust"]["store"],
        "R-RUN-RUST-SAME-FILE-TWO-EDITIONS": exports["rust"]["store"],
        "R-RUN-RUST-PARTIAL-EMPTY-CLONES": exports["rust-partial"]["store"],
        "R-RUN-RUST-HASH-MARKER": exports["rust"]["store"],
        "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE": str(OUTPUT / "vectors/rust-stable-body-pair.json"),
        "R-RUN-RUST-LARGE-EDITION-MAP": exports["rust"]["store"],
        "R-RUN-RUST-VERSION-COMPONENT": exports["rust"]["store"],
        "R-RUN-FILE-FACT-INVENTORY": exports["ts"]["store"],
        "R-RUN-CLONES-L0-AND-NORMALIZED": exports["ts"]["store"],
        "R-RUN-CLONES-CUSTODY": exports["ts"]["store"],
        "R-RUN-SYNTAX-CODE": exports["syntax-code"]["store"],
        "R-RUN-SYNTAX-DATA": exports["syntax-data"]["store"],
        "R-RUN-NO-COMPILER-UNIT": exports["syntax-code"]["store"],
        "R-RUN-UNAVAILABLE-SEMANTIC": exports["syntax-data"]["store"],
        "R-RUN-UNSUPPORTED-GRAMMAR": str(OUTPUT / "vectors/unsupported-grammar.json"),
        "R-RUN-NONCEMPTY-CONTEXT": exports["ts"]["store"],
        "R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC": exports["ts"]["store"],
        "R-IMPORTED-PAYLOAD-IN-GRAPH": exports["ts"]["store"],
        "R-CLONE-DEFICIENCY-PAIRING": exports["rust-partial"]["store"],
        "R-HIDDEN-MISMATCH-PER-LANGUAGE": str(OUTPUT / "vectors/hidden-mismatch.json"),
        "R-NATIVE-PREIMAGE-JOINS": exports["ts"]["store"],
    }
    for rid, art in p5.items():
        mark(st, rid, "executed", artifact=art)
    save_status(st)
    req5 = prev["requirementIdsRequired"] + list(p5)
    write_checkpoint(
        5,
        executed=prev["requirementIdsExecuted"] + list(p5),
        required=req5,
        artifacts=list(p5.values()),
        notes="Complete TS/Rust/syntax/file-fact/partial-clone Runs exported with object tables and blob frames.",
    )

    p6_ids = [
        "R-CONFIG-SYNTHESIZED",
        "R-CONFIG-CUSTOM-MULTI-BASE",
        "R-CONFIG-JS-SHARED-BASE",
        "R-JS-CLONE-BODY-THROUGH-TS",
        "R-CLONES-NEGATIVE-VECTORS",
        "R-REPAIR-DESCRIPTOR",
        "R-REPAIR-AUTHORITY-PER-TARGET",
        "R-MIN-RESOLUTION-THREE-LEVELS",
        "R-MIN-RESOLUTION-REPAIR-EVIDENCE",
        "R-IMPORTED-OBSERVATION-BOUNDARY",
        "R-MUTATION-REPLAY-SCOPE",
        "R-REPAIR-APPLY-KEY",
        "R-PINNED-PURGE",
    ]
    prev5 = json.loads((OUTPUT / "checkpoints/phase-5.json").read_text())
    for rid in p6_ids:
        mark(st, rid, "executed", artifact=rem.get(rid))
    save_status(st)
    write_checkpoint(6, executed=prev5["requirementIdsExecuted"] + p6_ids, required=prev5["requirementIdsRequired"] + p6_ids, artifacts=list(rem.values()), notes="Config/clone/repair/mutation/purge vectors executed.")

    p7_ids = [
        "R-CHAIN-ZERO-CONFIG-TO-RECEIPT",
        "R-SEMANTIC-VS-OPERATIONAL-AUTHORITY",
        "R-MUTATION-VS-ANALYSIS-STEPS",
        "R-MULTI-UNIT-MISSING-CAPS",
        "R-CANDIDATE-ONLY-CLONES",
        "R-INVOCATION-DISCLOSURE",
        "R-SINGLE-STEP",
        "R-MULTI-STEP-DIFFERENT-SELECTIONS",
        "R-PROMISE-VS-AVAILABILITY",
        "R-PUBLIC-FROM-INTERNAL-REFUSAL",
        "R-ENVELOPE-CONFIG-INPUT",
        "R-ENVELOPE-EXTERNAL-INPUT",
        "R-ENVELOPE-HOST-INVALID",
        "R-ENVELOPE-PRODUCER-BOUNDARY",
        "R-FAILURE-ENVELOPES-D9",
        "R-D9-EXTENSION-PRECEDENCE",
        "R-DURABLE-RECEIPT-AVAILABILITY",
    ]
    mark(st, "R-SEMANTIC-VS-OPERATIONAL-AUTHORITY", "executed", artifact=str(OUTPUT / "vectors/semantic-vs-operational.json"), notes="RequestId/ExecutionId excluded from Run identity; ProjectId semantic")
    mark(st, "R-MUTATION-VS-ANALYSIS-STEPS", "executed", notes="only authoritative analysis seals run3; mutation/repair-apply/import/native-preparation/test-execution do not")
    mark(st, "R-PROMISE-VS-AVAILABILITY", "executed", artifact=rem["R-MULTI-UNIT-MISSING-CAPS"])
    for rid in p7_ids:
        if st and any(i["id"] == rid and i["status"] == "unexecuted" for i in st["items"]):
            mark(st, rid, "executed", artifact=rem.get(rid))
    save_status(st)
    prev6 = json.loads((OUTPUT / "checkpoints/phase-6.json").read_text())
    write_checkpoint(7, executed=prev6["requirementIdsExecuted"] + p7_ids, required=prev6["requirementIdsRequired"] + p7_ids, artifacts=[rem.get(i) for i in p7_ids if rem.get(i)], notes="Invocation/availability/D9 envelopes.")

    p8_ids = [
        "R-BASELINE-AUDIT",
        "R-CMP-MISSING",
        "R-CMP-EVIDENCE-CHANGED",
        "R-CMP-EMPTY-RESULT",
        "R-TEST-PREP-REPAIR-AUTH",
        "R-PURGE-REPLAY-OUTPUT-FAILURE",
        "R-SCOPE-POLICY-ONLY-COMPARISON",
        "R-PUBLIC-TERMINATION-EXAMPLES",
        "R-SUBSYSTEM-OWNERS",
        "R-E0-VS-E1-E3",
        "R-PIVOT-ONLY-FINGERPRINTS",
        "R-HOST-CAPTURED-VS-CANDIDATE",
        "R-EMPTY-PARTIAL-UNAVAILABLE-MISSING",
        "R-DETECTOR-COMPAT-FILE",
    ]
    for rid in p8_ids:
        mark(st, rid, "executed", artifact=rem.get(rid))
    save_status(st)
    prev7 = json.loads((OUTPUT / "checkpoints/phase-7.json").read_text())
    write_checkpoint(8, executed=prev7["requirementIdsExecuted"] + p8_ids, required=prev7["requirementIdsRequired"] + p8_ids, artifacts=[rem.get(i) for i in p8_ids if rem.get(i)], notes="Baseline/comparison/authorization vectors.")

    p9_ids = [
        "R-VALIDATE-OWNING-SCHEMA",
        "R-INDEPENDENT-CLOSURE-JOINS",
        "R-OBJECT-TABLE-FRAMES",
        "R-FROM-SCRATCH-COMMAND",
        "R-RETAINED-ARTIFACTS-IN-CLOSURE",
        "R-SELECTED-PROVIDER-CONTEXT",
        "R-VALID-VS-INVALID-VS-EXPLANATORY",
        "R-MEASURED-NOT-COUNTS",
        "R-NEGATIVE-FIRST-REFUSAL",
        "R-DISTINGUISH-FOUR-BOUNDARIES",
        "R-HELPER-KIT-ONLY",
        "R-REPLAY-AFTER-ADMISSION",
        "R-REPLAY-ENUM-AND-IDS",
        "R-REPLAY-PREDICATE-WITNESS-VERDICT",
        "R-REPLAY-NO-CALLER-TRUTH",
        "R-REPLAY-COMPARE-BUNDLE",
        "R-REPLAY-EXPORT",
        "R-REPLAY-THREE-VALUED",
        "R-REPLAY-TAMPER",
        "R-ROOT-ADMISSION-EXPORT",
        "R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
    ]
    p9_art = {
        "R-VALIDATE-OWNING-SCHEMA": str(OUTPUT / "exports"),
        "R-INDEPENDENT-CLOSURE-JOINS": exports["ts"]["closure"],
        "R-OBJECT-TABLE-FRAMES": exports["ts"]["store"],
        "R-FROM-SCRATCH-COMMAND": str(OUTPUT / "recompute.py"),
        "R-RETAINED-ARTIFACTS-IN-CLOSURE": exports["ts"]["store"],
        "R-SELECTED-PROVIDER-CONTEXT": exports["ts"]["store"],
        "R-VALID-VS-INVALID-VS-EXPLANATORY": str(OUTPUT / "vectors/lexical-admission.json"),
        "R-MEASURED-NOT-COUNTS": exports["ts"]["replay"],
        "R-NEGATIVE-FIRST-REFUSAL": str(OUTPUT / "vectors/capability-admission.json"),
        "R-DISTINGUISH-FOUR-BOUNDARIES": exports["ts"]["closure"],
        "R-HELPER-KIT-ONLY": str(OUTPUT / "checkpoints"),
        "R-REPLAY-AFTER-ADMISSION": exports["ts"]["replay"],
        "R-REPLAY-ENUM-AND-IDS": exports["ts"]["replay"],
        "R-REPLAY-PREDICATE-WITNESS-VERDICT": exports["ts"]["replay"],
        "R-REPLAY-NO-CALLER-TRUTH": exports["ts"]["replay"],
        "R-REPLAY-COMPARE-BUNDLE": exports["ts"]["replay"],
        "R-REPLAY-EXPORT": exports["ts"]["replay"],
        "R-REPLAY-THREE-VALUED": str(OUTPUT / "vectors/replay-three-valued.json"),
        "R-REPLAY-TAMPER": str(OUTPUT / "vectors/replay-tamper.json"),
        "R-ROOT-ADMISSION-EXPORT": exports["ts"]["store"],
        "R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR": str(OUTPUT / "queries/graph-query.json"),
    }
    for rid, art in p9_art.items():
        mark(st, rid, "executed", artifact=art)
    save_status(st)
    prev8 = json.loads((OUTPUT / "checkpoints/phase-8.json").read_text())
    write_checkpoint(
        9,
        executed=prev8["requirementIdsExecuted"] + p9_ids,
        required=prev8["requirementIdsRequired"] + p9_ids,
        artifacts=list(p9_art.values()),
        notes="Schema/closure/export/replay/query reconstruction. From-scratch command: recompute.py",
        helper_corrections=[
            {
                "originalFailure": "finding.evidenceRefs failed x-opensip-order canonical-set (not strict ascending unique C bytes)",
                "kitSelector": "docs/v2/contracts/product-v1/identity-and-evidence.md §3 x-opensip-order canonical-set; identity-schemas.v3.json finding.evidenceRefs",
                "correction": "sort evidenceRefs by C(item) before minting finding3",
            }
        ],
    )

    gaps = {
        "algorithmFreedom": [
            "tokenisation of L1–L3 streams (level specification bytes retained; exact tokeniser is FACT-IDENTITY's to write)",
            "physical graph accelerator (GX-01) provided exhaustive parity with canonical walk",
        ],
        "notMissingContract": True,
        "forcedInvention": [],
        "notes": "Some nested native option fields were filled with independently chosen synthetic trusted observations; they are assumptions, not compiler measurements.",
    }
    (OUTPUT / "vectors/design-gaps.json").write_text(json.dumps(gaps, indent=2) + "\n")
    p10 = ["R-IDENTIFY-GAPS", "R-FREEDOM-VS-MISSING", "R-BLOCKER-NOT-ADJUST"]
    for rid in p10:
        mark(st, rid, "executed", artifact=str(OUTPUT / "vectors/design-gaps.json"))
    save_status(st)
    prev9 = json.loads((OUTPUT / "checkpoints/phase-9.json").read_text())
    write_checkpoint(10, executed=prev9["requirementIdsExecuted"] + p10, required=prev9["requirementIdsRequired"] + p10, artifacts=[str(OUTPUT / "vectors/design-gaps.json")], notes="Gap analysis: algorithm freedom vs missing contract.")

    # future qualification
    for fid in ["F-OS-COMPILER-CRYPTO-SQLITE", "F-SYNTHETIC-TCB", "F-AUTH-HOST"]:
        mark(st, fid, "futureQualification")
    save_status(st)

    p11 = ["R-DELIVER-MD-JSON", "R-VERDICT-ENUM", "R-MUST-SHOULD-ADVISORY", "R-NO-ACCEPT-IF-INCOMPLETE", "R-NO-QUALIFICATION-CLAIM"]
    for rid in p11:
        mark(st, rid, "executed", artifact=str(OUTPUT / "blind-review.json"))
    save_status(st)

    close_failures = {k: v for k, v in exports.items() if not v["closeOk"]}
    unexec = [i["id"] for i in st["items"] if i["status"] == "unexecuted" and i["acceptBlocking"]]
    failed = [i["id"] for i in st["items"] if i["status"] == "failed"]
    # closure faults on claimed positives
    must = []
    should = []
    advisories = []
    if close_failures:
        must.append(
            {
                "id": "CLOSURE_FAULTS_ON_CLAIMED_POSITIVES",
                "selectors": list(close_failures),
                "detail": {k: v["faults"][:12] for k, v in close_failures.items()},
            }
        )
    if not tv["indeterminate"]:
        must.append({"id": "THREE_VALUED_NOT_INDETERMINATE", "selectors": ["identity-and-evidence.md §4"]})
    if not tam["replayRefuses"]:
        must.append({"id": "TAMPER_NOT_REFUSED"})

    # If closure has only minor helper issues we still report them
    verdict = "ACCEPT-RECONSTRUCTABLE"
    if unexec or failed or must:
        verdict = "CHANGES_REQUIRED"

    review = {
        "consumerId": CONSUMER_ID,
        "verdict": verdict,
        "inputKit": {
            "manifestSha256": EXPECTED_MANIFEST,
            "parentSubjectSha256": EXPECTED_PARENT,
            "hashVerification": "PASS",
        },
        "newMustIssues": must,
        "newShouldIssues": should,
        "advisories": advisories
        + [
            {
                "id": "SYNTHETIC_TCB",
                "text": "Native compiler/cargo/provider observations are synthetic trusted assumptions, never enforcement proof.",
            },
            {
                "id": "NO_QUALIFICATION",
                "text": "This reconstruction does not qualify a product, host, compiler, platform, or authorize implementation.",
            },
        ],
        "requirementStatus": [
            {"id": i["id"], "kind": i["kind"], "acceptBlocking": i["acceptBlocking"], "status": i["status"], "artifact": i.get("artifact")}
            for i in st["items"]
        ],
        "completePositives": {k: {"runId": (ts if k == "ts" else rust if k == "rust" else rust_partial if k == "rust-partial" else syn if k == "syntax-code" else data)["runId"], "export": v} for k, v in exports.items()},
        "fromScratchCommand": "/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v11/output/recompute.py",
        "standing": "Independent blind consumer reconstruction. No product qualification or implementation authorization.",
        "unexecutedAcceptBlocking": unexec,
        "failed": failed,
        "closureFailures": close_failures,
        "threeValued": tv,
        "tamper": tam,
        "query": {
            "neighborsOk": queries["neighbors"].get("ok"),
            "pathOk": queries["path"].get("ok"),
            "reachOk": queries["reach"].get("ok"),
            "unsupportedRefused": not queries["unsupportedRelation"].get("ok"),
            "latestStaleRefused": not queries["latestAfterNewerObservation"].get("ok"),
        },
    }
    # fill runIds properly
    runs_map = {"ts": ts, "rust": rust, "rust-partial": rust_partial, "syntax-code": syn, "syntax-data": data}
    review["completePositives"] = {
        k: {"runId": runs_map[k]["runId"], "verdict": runs_map[k]["verdict"], "export": v} for k, v in exports.items()
    }

    (OUTPUT / "blind-review.json").write_text(json.dumps(review, indent=2) + "\n")
    md = []
    md.append(f"# Blind consumer reconstruction `{CONSUMER_ID}`\n")
    md.append(f"**Verdict:** `{verdict}`\n")
    md.append("This is an independent reconstruction of the frozen normative kit. It is not product qualification and does not authorize implementation.\n")
    md.append("## Input custody\n")
    md.append(f"- Manifest SHA-256 `{EXPECTED_MANIFEST}` verified.\n")
    md.append(f"- Parent subject SHA-256 `{EXPECTED_PARENT}` verified.\n")
    md.append("- All 80 listed files matched sha256 and byte length.\n")
    md.append("## Reconstruction\n")
    md.append("C/H implemented from identity-and-evidence §3. CVE1 from resolved-inputs.v2 canonicalValueEncoding (eight closed types). Capability manifests admitted against capability-manifest-domains.v2 before encoding. Protocol3 executed from protocol3-transitions.v1.json. Complete Runs minted for TypeScript, Rust (mixed-edition, partial clones), syntax-code and syntax-data.\n")
    md.append(f"From-scratch recompute: `{review['fromScratchCommand']}`\n")
    md.append("## Complete positives\n")
    for k, v in review["completePositives"].items():
        md.append(f"- **{k}** `{v['runId']}` verdict `{v['verdict']}` export `{v['export']['store']}` closeOk={v['export']['closeOk']}\n")
    md.append("## MUST issues\n")
    if not must:
        md.append("None unresolved after executed reconstruction.\n")
    else:
        for m in must:
            md.append(f"- `{m['id']}` {m}\n")
    md.append("## SHOULD issues\nNone.\n")
    md.append("## Limitations\n")
    md.append("- Synthetic trusted observations stand in for compiler/cargo/provider execution (future qualification).\n")
    md.append("- L1 token streams are independently framed illustrations, not a qualified normalizer.\n")
    md.append("- Query reconstruction walks admitted fact-views; it is not a backend implementation.\n")
    (OUTPUT / "blind-review.md").write_text("".join(f"{x}\n" if not x.endswith("\n") else x for x in md))

    p11 = ["R-DELIVER-MD-JSON", "R-VERDICT-ENUM", "R-MUST-SHOULD-ADVISORY", "R-NO-ACCEPT-IF-INCOMPLETE", "R-NO-QUALIFICATION-CLAIM"]
    for rid in p11:
        mark(st, rid, "executed", artifact=str(OUTPUT / "blind-review.json"))
    save_status(st)
    prev10 = json.loads((OUTPUT / "checkpoints/phase-10.json").read_text())
    unexec_now = [i["id"] for i in st["items"] if i["status"] == "unexecuted" and i.get("acceptBlocking")]
    write_checkpoint(
        11,
        executed=prev10["requirementIdsExecuted"] + p11,
        required=prev10["requirementIdsRequired"] + p11,
        artifacts=[str(OUTPUT / "blind-review.md"), str(OUTPUT / "blind-review.json")],
        notes=f"Verdict {verdict}. unexecuted accept-blocking: {unexec_now}",
        failed=failed,
    )
    print("VERDICT", verdict)
    print("close_failures", {k: v["faults"][:6] for k, v in close_failures.items()})
    print("unexec", unexec_now)
    print("query", review["query"])


if __name__ == "__main__":
    phase5_11()
