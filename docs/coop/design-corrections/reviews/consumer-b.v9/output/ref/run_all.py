#!/usr/bin/env python3
"""From-scratch reconstruction runner.

    /tmp/opensip-architecture-review-env/bin/python -I -B ref/run_all.py

Verifies the input manifest, executes every reconstruction vector, closes and
REPLAYS every complete positive Run, exports the object tables, the blob store
and the comparison results, and exits non-zero if any required control fails.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.abspath(os.path.join(HERE, ".."))
VEC = os.path.join(OUT, "vectors")
os.makedirs(VEC, exist_ok=True)

import assemble as A            # noqa: E402
import canon as K               # noqa: E402
import closure as CL            # noqa: E402
import kit                      # noqa: E402
import protocol as P            # noqa: E402
import vec_identity, vec_native, vec_workflow, vec_gaps   # noqa: E402
import minirun, run_ts, run_rust, run_syntax, run_tsvariants   # noqa: E402
from store import Refusal        # noqa: E402

REPORT = {"tool": "cb9-blind-reconstruction", "sections": {}}
FAILURES = []


def fail(where, detail):
    FAILURES.append({"where": where, "detail": detail})


# ---------------------------------------------------------------------------
# 0. input manifest
# ---------------------------------------------------------------------------

def verify_manifest():
    man_path = os.path.join(kit.KIT, "consumer-input-manifest.json")
    with open(man_path, "rb") as fh:
        raw = fh.read()
    man = json.loads(raw)
    rows, listed = [], set()
    for f in man["files"]:
        p = os.path.join(kit.KIT, f["path"])
        listed.add(f["path"])
        with open(p, "rb") as fh:
            b = fh.read()
        d = hashlib.sha256(b).hexdigest()
        ok = d == f["sha256"] and len(b) == f["bytes"]
        rows.append({"path": f["path"], "sha256": d, "bytes": len(b), "ok": ok})
        if not ok:
            fail("manifest", f["path"])
    actual = set()
    for root, _dirs, files in os.walk(os.path.join(kit.KIT, "docs")):
        for name in files:
            actual.add(os.path.relpath(os.path.join(root, name), kit.KIT))
    extra = sorted(actual - listed)
    missing = sorted(listed - actual)
    if extra or missing:
        fail("manifest", f"extra={extra} missing={missing}")
    REPORT["sections"]["inputManifest"] = {
        "manifestSha256": hashlib.sha256(raw).hexdigest(),
        "parentSubjectSha256Claimed": man["parentSubjectSha256"],
        "fileCount": len(man["files"]), "verified": sum(r["ok"] for r in rows),
        "extraFiles": extra, "missingFiles": missing, "files": rows}


# ---------------------------------------------------------------------------
# 1. complete positive Runs: close + REPLAY + export
# ---------------------------------------------------------------------------

POSITIVES = [
    ("RUN-TS-1", lambda: run_ts.build(),
     "ordinary TypeScript project reading node_modules, resolving bare "
     "specifiers, with its retained config graph and dependency layout; "
     "file inventory + L0 and L1 clone bodies + a resolved reference"),
    ("RUN-RS-1-lib", lambda: run_rust.build(selection="lib"),
     "mixed-edition Rust workspace, shared.rs owned by the lib target at the "
     "package default edition 2018, `#` marker directory"),
    ("RUN-RS-2-test", lambda: run_rust.build(selection="test"),
     "the SAME physical path under a different explicitly selected target "
     "whose own edition (2021) overrides its package default"),
    ("RUN-RS-3-selection-widened", lambda: run_rust.build(selection="lib+bin"),
     "selection changes without changing the effective dialect"),
    ("RUN-RS-4-large-edition-map",
     lambda: run_rust.build(selection="lib",
                            edition_map=run_rust.LARGE_EDITION_MAP),
     "a representative 21-crate edition map"),
    ("RUN-RS-5-partial-ownership",
     lambda: run_rust.build(selection="lib", enumeration="partial",
                            empty_clone_view=True),
     "partial enumeration: the empty clone view discloses rather than claiming "
     "complete Coverage"),
    ("RUN-RS-6-ambiguous-ownership",
     lambda: run_rust.build(selection="both", empty_clone_view=True),
     "selected owners disagree on effective edition: disclosed, indeterminate"),
    ("RUN-SYN-CODE", lambda: run_syntax.build(kind="code"),
     "compiler-free syntax-only Run over CODE grammars: inventory plus "
     "declares@syntactic and a grammar-parsed clone body"),
    ("RUN-SYN-DATA", lambda: run_syntax.build(kind="data"),
     "already bundled DATA/DOCUMENT grammars: the declared inventory "
     "capability, and explicit unavailability for the capabilities its class "
     "does not support"),
    ("RUN-SYN-NONE", lambda: run_syntax.build(kind="none"),
     "a repository with NO TypeScript and NO Rust compilation unit, including "
     "a path no bundled grammar reads"),
    ("RUN-TSV-synth", lambda: run_tsvariants.build(variant="synth"),
     "synthesized configuration"),
    ("RUN-TSV-custom", lambda: run_tsvariants.build(variant="custom"),
     "explicitly selected custom-named project config inheriting from multiple "
     "ORDERED bases including a REPEATED base"),
    ("RUN-TSV-jsconfig", lambda: run_tsvariants.build(variant="jsconfig"),
     "JavaScript config inheriting a shared base with another filename"),
    ("RUN-TSV-jsbody", lambda: run_tsvariants.build(variant="jsbody"),
     "a JavaScript clone body through the TypeScript ANALYZER universe"),
    ("RUN-MINI", lambda: minirun.build(),
     "minimal baseline positive for the closure-law negatives"),
]


def run_positives():
    out = []
    for vid, builder, note in POSITIVES:
        entry = {"id": vid, "note": note}
        try:
            built = builder()
            closed = CL.close_run(built["store"], built["runId"])
            cmp_result = A.verify_replay(built["store"], closed, None)
            entry.update({
                "closed": True,
                "runId": built["runId"],
                "planId": built.get("planId"),
                "snapshotId": closed["run"]["snapshotId"],
                "capabilityManifestId": closed["run"]["capabilityManifestId"],
                "verdict": closed["seal"]["verdict"],
                "counts": {"facts": len(closed["facts"]),
                           "scopes": len(closed["scopes"]),
                           "coverage": len(closed["coverages"]),
                           "views": len(closed["views"]),
                           "findings": len(closed["findings"]),
                           "predicateProofs": len(closed["proof"]["predicateProofs"]),
                           "blobs": len(built["store"].blobs),
                           "objects": len(built["store"].objects)},
                "replay": {"ok": cmp_result["ok"], "diffs": cmp_result["diffs"],
                           "recomputedVerdict": cmp_result["recomputed"]["verdict"],
                           "retainedVerdict": closed["proof"]["verdict"]},
                "bodyIdentity": built.get("bodyIdentity"),
                "bodyIdentityL1": built.get("bodyIdentityL1"),
                "grammarBodyIdentity": built.get("grammarBodyIdentity"),
                "bodyLanguageVersion": built.get("bodyLanguageVersion")
                or built.get("grammarBodyLanguageVersion"),
            })
            if not cmp_result["ok"]:
                fail(vid, "semantic proof replay did not match the retained claim")
            # export the object table, the blobs and the replayed inputs
            export = built["store"].export()
            export["run"] = {"id": built["runId"], "descriptor": closed["run"]}
            export["replayedInputs"] = {
                "policy": closed["policy"], "ruleProgram": closed["ruleProgram"],
                "waivers": closed["waivers"],
                "scopes": closed["scopes"],
                "coverage": {c: v["payload"] for c, v in closed["coverages"].items()},
                "facts": closed["facts"],
            }
            export["computedProof"] = {
                "predicateProofs": cmp_result["recomputed"]["predicateProofs"],
                "witnesses": cmp_result["recomputed"]["witnesses"],
                "programPredicates": cmp_result["recomputed"]["programPredicates"],
                "findings": cmp_result["recomputed"]["findings"],
                "verdict": cmp_result["recomputed"]["verdict"],
                "ruleOutcomes": cmp_result["recomputed"]["ruleOutcomes"]}
            export["retainedProof"] = closed["proof"]
            export["comparison"] = cmp_result["ok"] and "MATCH" or cmp_result["diffs"]
            with open(os.path.join(VEC, f"{vid}.json"), "w") as fh:
                json.dump(export, fh, indent=1, sort_keys=True)
            entry["export"] = f"vectors/{vid}.json"
        except Exception as exc:                        # noqa: BLE001
            entry.update({"closed": False,
                          "error": f"{type(exc).__name__}: {exc}",
                          "traceback": traceback.format_exc()[-800:]})
            fail(vid, entry["error"])
        out.append(entry)
    REPORT["sections"]["positiveRuns"] = out


# ---------------------------------------------------------------------------
# 2. negatives
# ---------------------------------------------------------------------------

def refuse(vid, fn, note, sink):
    try:
        fn()
        sink.append({"id": vid, "outcome": "NO-REFUSAL", "note": note})
        fail(vid, "expected a refusal")
    except (Refusal, kit.SchemaRefusal, K.AdmissionError) as exc:
        sink.append({"id": vid, "outcome": "refused", "note": note,
                     "firstObservedBoundary": getattr(exc, "code",
                                                      type(exc).__name__),
                     "message": str(exc)[:220]})


def run_negatives():
    sink = []
    m = lambda **kw: (lambda: CL.close_run(*_mini(**kw)))            # noqa: E731
    t = lambda **kw: (lambda: CL.close_run(*_ts(**kw)))              # noqa: E731
    r = lambda **kw: (lambda: CL.close_run(*_rust(**kw)))            # noqa: E731
    y = lambda **kw: (lambda: CL.close_run(*_syn(**kw)))             # noqa: E731
    v = lambda **kw: (lambda: CL.close_run(*_tsv(**kw)))             # noqa: E731

    cases = [
        ("N-source-join", m(wrong_source_join=True),
         "a fact naming another snapshot"),
        ("N-anchor-inventory-class", m(inventory_anchor=True),
         "an inventory fact carrying an anchor (anchorLaw cardinality 0)"),
        ("N-anchor-borrowed-package", m(package_fact_borrowed_anchor=True),
         "a package fact anchored into an unrelated file"),
        ("N-anchor-unanchored-code", m(unanchored_code_fact=True),
         "an unanchored code fact under a TypeScript universe"),
        ("N-file-digest-lie", m(file_digest_lie=True),
         "a file payload claiming a content hash the inventory contradicts"),
        ("N-file-length-lie", m(file_length_lie=True),
         "a file payload claiming a byte length the inventory contradicts"),
        ("N-fact-producer", m(foreign_producer_fact=True),
         "a member fact whose producer is not the view's"),
        ("N-closure-not-selected", m(drop_provider_from_closures=True),
         "a producing closure the Plan did not select"),
        ("N-budget", m(plan_budget=5),
         "a Plan budget contradicting its own resolved configuration"),
        ("N-partition-overlap", m(partition_overlap=True),
         "two scopes of one view sharing the full owning tuple and a subject"),
        ("N-coverage-schema-chosen", m(coverage_schema_lie=True),
         "a Coverage payload schema digest a caller chose"),
        ("N-commitment-chosen", m(commitment="sha256:" + "ee" * 32),
         "a subject-scope commitment the claimant chose"),
        ("N-subject-count", m(subject_count=99),
         "a producer-claimed examined subject count that disagrees"),
        ("N-view-schema-unregistered", m(view_schema_unregistered=True),
         "view.schemaDigests naming an unregistered document"),
        ("N-hidden-finding-evidence", m(hidden_finding_evidence=True),
         "a finding citing a fact outside the evaluated view"),
        ("N-duplicate-ownership-tuple", m(requested_capabilities=[
            {"capabilityId": "inventory", "languageMode": "ts-tsconfig",
             "workspaceRoot": ".", "required": True},
            {"capabilityId": "inventory", "languageMode": "ts-tsconfig",
             "workspaceRoot": ".", "required": False}]),
         "two analysis-spec rows over one ownership tuple disagreeing on required"),
        ("N-capability-unregistered", m(requested_capabilities=[
            {"capabilityId": "made-up", "languageMode": "ts-tsconfig",
             "workspaceRoot": ".", "required": True}]),
         "a capabilityId outside the closed matrix vocabulary"),
        ("N-mode-unregistered", m(requested_capabilities=[
            {"capabilityId": "inventory", "languageMode": "cobol",
             "workspaceRoot": ".", "required": True}]),
         "a languageMode outside the registered map"),
        ("N-rc6", m(coverage_kwargs={"examined_exhaustive": False}),
         "RC-6: coverage complete with examinedExhaustive false"),
        ("N-rc1-attempted", m(coverage_kwargs={"attempted": True, "force": True}),
         "RC-1: a not-applicable entry claiming attempted"),
        ("N-rc1-edge-classes",
         m(coverage_kwargs={"edge_classes": ["indirect-eval"], "force": True}),
         "RC-1: a not-applicable entry carrying unresolved edge classes"),
        ("N-rc1-state", m(coverage_kwargs={"state": "complete", "force": True}),
         "RC-1: a resolution state on a non-resolved rung"),
        ("N-cause-without-deficiency",
         m(coverage_kwargs={"native_cause": "capability-missing"}),
         "a cause naming why nothing went wrong"),
        ("N-cause-required", m(coverage_kwargs={
            "coverage": "unknown", "deficiency": "language-tier-unsupported"}),
         "language-tier-unsupported with a null cause"),
        ("N-cause-must-be-null", m(coverage_kwargs={
            "coverage": "unknown", "deficiency": "resolution-incomplete",
            "native_cause": "lockfile-missing"}),
         "resolution-incomplete carrying a nativeCause"),
        ("N-cause-relation-scope", m(coverage_kwargs={
            "coverage": "unknown", "deficiency": "derivation-policy-unmet",
            "derivation_kinds": ["compiler-inferred"]}),
         "derivation-policy-unmet declared on a non-types relation"),
        ("N-inventory-totality", t(break_totality=True),
         "a complete file@enumerated Coverage omitting an inventoried subject"),
        ("N-l0-span", t(l0_span_lie=True),
         "an L0 body payload that is not the enclosing fact's anchor span"),
        ("N-anchor-range", t(anchor_range_lie=True),
         "an anchor range outside the blob it names"),
        ("N-l1-level-id", t(body_mutation={"levelId": "L2-comment-insensitive"}),
         "a body frame levelId disagreeing with the payload's level"),
        ("N-l1-level-version",
         t(body_mutation={"levelVersion": hashlib.sha256(b"other").digest()}),
         "a body frame levelVersion that is not the retained specification"),
        ("N-l1-language-id", t(body_mutation={"languageId": "rust"}),
         "a body frame languageId that is not the derived body language"),
        ("N-l1-language-version",
         t(body_mutation={"languageVersion": hashlib.sha256(b"x").digest()}),
         "a body frame languageVersion that is not the derived record"),
        ("N-l1-token-framing", t(body_mutation={"payload": b"\x00\x00\x00\x02\x00"}),
         "a malformed framed token stream"),
        ("N-rust-ambiguous-owner", r(selection="both"),
         "a clone body whose selected owners disagree on effective edition"),
        ("N-rust-partial-enumeration",
         r(selection="lib", enumeration="partial"),
         "a clone body under partial enumeration"),
        ("N-rust-false-complete", r(
            selection="lib", enumeration="partial", empty_clone_view=True,
            clone_coverage_override={"coverage": "complete", "deficiency": None,
                                     "native_cause": None}),
         "a false complete clone Coverage under partial ownership"),
        ("N-rust-undisclosed", r(
            selection="lib", enumeration="partial", empty_clone_view=True,
            clone_coverage_override={"deficiency": None, "native_cause": None}),
         "an undisclosed null deficiency where one is owed"),
        ("N-rust-wrong-cause", r(
            selection="lib", enumeration="partial", empty_clone_view=True,
            clone_coverage_override={"native_cause": "lockfile-missing"}),
         "a wrong nativeCause for the derived ownership state"),
        ("N-syntax-md-anchored-declares", y(kind="code", bad_anchor=True),
         "a Markdown-anchored declares fact under a syntax universe"),
        ("N-syntax-false-complete", y(kind="data", false_complete=True),
         "a complete empty declares/clones Coverage over a data-only repository"),
        ("N-syntax-wrong-deficiency", y(kind="data", wrong_pair="deficiency"),
         "a wrong deficiency on an unavailable capability scope"),
        ("N-syntax-wrong-cause", y(kind="data", wrong_pair="cause"),
         "a wrong cause on an unavailable capability scope"),
        ("N-config-node-kind", v(variant="custom", kind_lie=True),
         "a config-graph node kind contradicting its own path basename"),
    ]
    for vid, fn, note in cases:
        refuse(vid, fn, note, sink)

    # frame-level negatives that need store surgery
    def altered_frame():
        built = run_ts.build()
        h = built["contextHex"]
        b = bytearray(built["store"].blobs[h])
        b[-2] ^= 1
        built["store"].blobs[h] = bytes(b)
        CL.close_run(built["store"], built["runId"])

    def missing_preimage():
        built = run_ts.build()
        del built["store"].blobs[built["contextHex"]]
        CL.close_run(built["store"], built["runId"])

    def raw_payload_as_h_identity():
        """The payload is retained under ITS OWN digest and the Plan commits to
        that digest, so the digest matches and the FRAME PREFIX is the first
        boundary reached."""
        s2, rid = _mini(context_digest_mode="raw-payload")
        CL.close_run(s2, rid)

    def unregistered_h_domain():
        s2, rid = _mini(context_digest_mode="unregistered-domain")
        CL.close_run(s2, rid)

    refuse("N-altered-frame", altered_frame,
           "an altered retained context frame", sink)
    refuse("N-missing-preimage", missing_preimage,
           "a missing retained preimage", sink)
    refuse("N-raw-payload-as-h-identity", raw_payload_as_h_identity,
           "a raw canonical payload offered where an H frame is required", sink)
    refuse("N-unregistered-h-domain", unregistered_h_domain,
           "an H frame whose domain is not a member of the named domain set",
           sink)
    REPORT["sections"]["closureNegatives"] = sink


def _mini(**kw):
    built = minirun.build(**kw)
    return built["store"], built["runId"]


def _ts(**kw):
    built = run_ts.build(**kw)
    return built["store"], built["runId"]


def _rust(**kw):
    built = run_rust.build(**kw)
    return built["store"], built["runId"]


def _syn(**kw):
    built = run_syntax.build(**kw)
    return built["store"], built["runId"]


def _tsv(**kw):
    built = run_tsvariants.build(**kw)
    return built["store"], built["runId"]


# ---------------------------------------------------------------------------
# 3. tampered-result control
# ---------------------------------------------------------------------------

def run_tamper_controls():
    out = []
    for vid, tamper, note in [
        ("CTRL-tamper-verdict", "verdict",
         "valid record identities and citation membership preserved; only the "
         "claimed logical RESULT is changed"),
        ("CTRL-tamper-predicate-value", "predicate-value",
         "one predicate proof's value is flipped; every identity still closes"),
    ]:
        built = run_ts.build(tamper=tamper)
        closed = CL.close_run(built["store"], built["runId"])   # linkage passes
        cmp_result = A.verify_replay(built["store"], closed, None)
        row = {"id": vid, "note": note, "linkageClosureAdmitted": True,
               "retainedVerdict": closed["proof"]["verdict"],
               "recomputedVerdict": cmp_result["recomputed"]["verdict"],
               "replayRefused": not cmp_result["ok"],
               "diffs": cmp_result["diffs"]}
        if cmp_result["ok"]:
            fail(vid, "replay did NOT refuse a tampered result")
        out.append(row)
    REPORT["sections"]["tamperControls"] = out


# ---------------------------------------------------------------------------
# 4. protocol traces
# ---------------------------------------------------------------------------

def run_protocol():
    traces = {
        "T1-complete-single-stage": ([
            "Hello", P.HELLO_ACK_OK, P.OPEN_PLAIN, "UniverseAccepted",
            "SnapshotManifest", "SnapshotFileChunk", "SnapshotSeal",
            "SnapshotAccepted", "NativeContextVerified", "Analyze", "FactBatch",
            "CoverageV3", "Complete", "zero-exit", "eof"], 1),
        "T2-complete-dependency-custody-two-stages": ([
            "Hello", P.HELLO_ACK_OK, P.OPEN_DEPS, "UniverseAccepted",
            "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted",
            "DependencySourceManifest", "DependencySourceChunk",
            "DependencySourceSeal", "DependencySourceAccepted",
            "NativeContextVerified", "Analyze", "FactBatch", "CoverageV3",
            "FactBatch", "CoverageV3", "Complete", "zero-exit", "eof"], 2),
        "T3-unavailable-before-analyze": ([
            "Hello", P.HELLO_ACK_OK, P.OPEN_PLAIN, "UniverseAccepted",
            "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted",
            "Unavailable", "zero-exit", "eof"], 1),
        "T4-cancellation-mid-analysis": ([
            "Hello", P.HELLO_ACK_OK, P.OPEN_PLAIN, "UniverseAccepted",
            "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted",
            "NativeContextVerified", "Analyze", "FactBatch", "Cancel",
            "Cancelled", "zero-exit", "eof"], 1),
        "T5-fault-open-universe-before-identity": ([
            "Hello", P.HELLO_ACK_V1_ONLY, P.OPEN_PLAIN], 1),
        "T6-fault-process-death-mid-stage": ([
            "Hello", P.HELLO_ACK_OK, P.OPEN_PLAIN, "UniverseAccepted",
            "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted",
            "NativeContextVerified", "Analyze", "FactBatch", "signal-death"], 1),
        "T7-post-terminal-frame": ([
            "Hello", P.HELLO_ACK_OK, P.OPEN_PLAIN, "UniverseAccepted",
            "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted",
            "NativeContextVerified", "Analyze", "CoverageV3", "Complete",
            "FactBatch"], 1),
        "T8-budget-exhausted": ([
            "Hello", P.HELLO_ACK_OK, P.OPEN_PLAIN, "UniverseAccepted",
            "SnapshotManifest", "SnapshotSeal", "SnapshotAccepted",
            "NativeContextVerified", "Analyze", "BudgetExhausted", "zero-exit",
            "eof"], 1),
        "T9-provider-fault-mid-custody": ([
            "Hello", P.HELLO_ACK_OK, P.OPEN_PLAIN, "UniverseAccepted",
            "SnapshotManifest", "ProviderFault", "zero-exit", "eof"], 1),
    }
    out = {"pairwiseDisjointClashes": P.pairwise_disjoint(), "traces": {}}
    if out["pairwiseDisjointClashes"]:
        fail("protocol", "the published pairwise-disjoint claim does not hold")
    for name, (events, stages) in traces.items():
        st, tr = P.trace(events, stages)
        out["traces"][name] = {
            "finalPhase": st["phase"], "terminalKind": st["terminalKind"],
            "identityNegotiated": st["identityNegotiated"],
            "sourceBytesSent": st["sourceBytesSent"],
            "stagesCompleted": st["stagesCompleted"],
            "rules": [r["rule"] for r in tr]}
    # the identity-negotiation invariant, asserted
    t5 = out["traces"]["T5-fault-open-universe-before-identity"]
    if t5["sourceBytesSent"] or t5["finalPhase"] != "FAULT":
        fail("protocol", "OpenUniverse reached a worker before negotiation")
    REPORT["sections"]["protocol"] = out


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    verify_manifest()
    REPORT["sections"]["identityVectors"] = vec_identity.run_all()
    REPORT["sections"]["nativeVectors"] = vec_native.run_all()
    REPORT["sections"]["workflowVectors"] = vec_workflow.run_all()
    REPORT["sections"]["designGaps"] = vec_gaps.run_all()
    run_positives()
    run_negatives()
    run_tamper_controls()
    run_protocol()
    for section in ("identityVectors", "nativeVectors", "workflowVectors"):
        for row in REPORT["sections"][section]:
            if row["kind"] == "NEGATIVE-FAILED":
                fail(section, row["id"])
            for flag in ("agrees", "distinct", "moved", "stable", "recomputed",
                         "prefixOk", "allThreeDistinct",
                         "universeFieldIsTheHSuffix", "specDigestsDiffer"):
                if row.get(flag) is False:
                    fail(section, f"{row['id']}:{flag}")
    REPORT["failures"] = FAILURES
    REPORT["summary"] = {
        "positiveRuns": len(REPORT["sections"]["positiveRuns"]),
        "positiveRunsClosedAndReplayed": sum(
            1 for r in REPORT["sections"]["positiveRuns"]
            if r.get("closed") and r.get("replay", {}).get("ok")),
        "closureNegatives": len(REPORT["sections"]["closureNegatives"]),
        "closureNegativesRefused": sum(
            1 for r in REPORT["sections"]["closureNegatives"]
            if r["outcome"] == "refused"),
        "identityVectors": len(REPORT["sections"]["identityVectors"]),
        "nativeVectors": len(REPORT["sections"]["nativeVectors"]),
        "workflowVectors": len(REPORT["sections"]["workflowVectors"]),
        "protocolTraces": len(REPORT["sections"]["protocol"]["traces"]),
        "designGapsMust": sum(1 for g in REPORT["sections"]["designGaps"]
                              if g["severity"] == "MUST"),
        "designGapsShould": sum(1 for g in REPORT["sections"]["designGaps"]
                                if g["severity"] == "SHOULD"),
        "requiredControlFailures": len(FAILURES)}
    with open(os.path.join(VEC, "reconstruction-report.json"), "w") as fh:
        json.dump(REPORT, fh, indent=1, sort_keys=True, default=str)
    print(json.dumps(REPORT["summary"], indent=1))
    if FAILURES:
        print("\nREQUIRED CONTROL FAILURES:")
        for f in FAILURES:
            print("  ", f["where"], "->", str(f["detail"])[:160])
        return 1
    print("\nAll required controls passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
