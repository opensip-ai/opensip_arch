"""Phase 10/11 finalization from measured source43 standing (runtime consumer-b.v24-source43.v1, continuing source42.v1-.v3).

python3 tools/finalize_review.py            -> records phase-10 standing, writes checkpoint 10 and blind-review.json
python3 tools/finalize_review.py --phase11  -> verifies blind-review.md/json against the charter rules, records phase-11 standing,
                                               writes checkpoint 11 and refreshes blind-review.json requirementStatus
The verdict is derived: ACCEPT-RECONSTRUCTABLE only with no MUST/SHOULD issue, no unexecuted accept-blocking ID, no failed ID, final custody
PASS, all retention negatives passing, every closure control refused by the corrected code, and every claimed complete positive admitted by
owner admission, the independent retained closure and replay with reachable-set equality, and exported; otherwise CHANGES_REQUIRED (BLOCKED is
reserved for an unbuildable promised vector). The source41 version of this tool is preserved at preserved/source41-v1/tools/finalize_review.py.
"""
import copy
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import hc_source42 as HC  # noqa: E402
import hc_source43 as HC43  # noqa: E402
import status as S  # noqa: E402

OUT = S.OUT
REVIEW_JSON = OUT + "blind-review.json"
REVIEW_MD = OUT + "blind-review.md"
STANDING = ("Independent reconstruction of the source43 normative kit (manifest 6d8912f4..., parent db43ee76...) in runtime consumer-b.v24-source43.v1, "
            "continuing the same blind origin from the exact source42.v3 output. Against my own source42 custody rows exactly one kit member changed, the "
            "query projection contract (workflows/query-projection-contract.v3.md). Its only helper consumer, the graph-query reconstruction, was re-audited "
            "law by law and corrected from the kit (HC-54). The unchanged helper's results are preserved and measured on every new vector. The from-scratch "
            "closure and complete proof replay of every claimed positive, the export replay and the admission log were executed fresh on the source43 "
            "runtime. Every other measurement is reused as an exact source42 measurement with custody (selfcheck/s43-provenance.json). "
            "Source42 history: "
            "Independent reconstruction of the source42 normative kit, continuing the same blind origin 9d3dfb70-b2d3-498c-a3c1-f8de9e488514 in "
            "runtime consumer-b.v24-source42.v1 (incomplete: it ended without checkpoints or review) and completed in consumer-b.v24-source42.v2 "
            "from that runtime's byte-identical copied output, with measurements reused from v1 labelled as reuse and the pending steps executed "
            "fresh. In consumer-b.v24-source42.v3, starting from the byte-identical v2 output, the same charter was finished for the "
            "provider-trace payload obligation of 'Current incorporated correction owners'. The v2 review had called that obligation read but not "
            "exercised while marking R-TRACE-* executed on transition-only traces (HC-53). The negotiated payload selection, exact payload bytes and "
            "request/batch correlation law are now executed in the traces and standalone vectors. Unaffected v2 measurements are reused unchanged, "
            "and fresh-origin independence is not claimed anew. The consumer-b.v24, source39.v1-v3 and source41.v1 "
            "results are preserved as immutable own history and establish nothing about the source42 kit; this runtime found that my source41 exports "
            "carried a helper omission of a published schema law (HC-47), so the source41 recommendation rested on defective exports. Own helpers were "
            "ported from source41.v1, executed unchanged against source42 first (preserved), and corrected only from this kit (HC-47..HC-50). This "
            "review reports its own executed admission, independent retained closure, replay, exports and vectors; it makes no product qualification "
            "claim, grants no implementation authorization and implies no acceptance. External root admission of the exported bytes is a separate gate "
            "whose outcome is unobserved here. Real OS/compiler/crypto/SQLite measurement, native compiler/provider execution as enforcement proof, host "
            "authentication and synthetic TCB enforcement are future qualification: explicitly unperformed and not counted as design omissions.")

MUST = []
SHOULD = []
PHASE11_IDS = ("R-DELIVER-MD-JSON", "R-VERDICT-ENUM", "R-MUST-SHOULD-ADVISORY", "R-NO-ACCEPT-IF-INCOMPLETE", "R-NO-QUALIFICATION-CLAIM")


def cb24_keys():
    keys = set()
    for p in sorted(glob.glob(OUT + "ref/*.py")):
        keys |= set(re.findall(r'["(]cb24\.([A-Za-z][A-Za-z0-9_.-]*)', open(p).read()))
    return sorted(keys)


# Disposition of my own source41.v1 results under the source42 kit (the source41 review is preserved at preserved/source41-v1/blind-review.json).
PRIOR_S41 = [
    {"id": "source41 claimed positives (27) and their ACCEPT-RECONSTRUCTABLE recommendation",
     "disposition": "own helper defect found; superseded. The exports carried programEntry 'tsconfig.json'/'Cargo.toml' on default-unit enumeration "
                    "bindings (and labelled the U-9 syntax default explicit-plan-selection), which the schema description published since source41 "
                    "refuses; my source41 enumeration admission omitted that law, so the recommendation rested on exports a conforming admission "
                    "refuses. Corrected here (HC-47) and every positive rebuilt and re-closed.",
     "selector": "foundation/enumeration-plan.schema.v1.json#/$defs/AvailableProgramBindingV1/properties/programEntry/description; "
                 "foundation/enumeration-contract.v1.md s1 lines 20-47",
     "measured": "logs/s42-original.7.from_scratch.log (unchanged helpers admit all 27; run ids identical to the source41 exports); "
                 "selfcheck/s42-prepost-matrix.json (corrected code over those original bytes); runs/*~default-unit-program-entry controls"},
    {"id": "source41 execution-inputs view attribution (HC-42)", "disposition": "tightened by the source42 kit text (candidate views from complete receipts only; HC-48)",
     "selector": "foundation/execution-inputs-contract.v1.md s3 line 53", "measured": "runs/syntax-code~selected-view-not-on-receipt"},
    {"id": "source41 newMustIssues / newShouldIssues", "disposition": "none were raised; none reopened", "selector": "-", "measured": "-"},
    {"id": "A-c1, A-c2, A-c3, A-n1, A-n6, A-v2-1, A-v2-2, A-v2-3, A-s41-1, A-s41-2", "disposition": "carried as advisories; their owner documents are unchanged in source42",
     "selector": "as listed in advisories", "measured": "as listed in advisories"},
    {"id": "own source42.v2 review: limitation 'No Run negotiates target-attribution-v2 or FactBatchV3 occupancy companions (native s9.6); no claim is made about "
           "them' and 'Not constructed by any original requirement; read but not exercised', while R-TRACE-* stood executed",
     "disposition": "withdrawn as inaccurate, found in source42.v3 (HC-53). The charter's current incorporated correction owners make the negotiated payload selection, "
                    "exact payload-byte representation and request/batch correlation law part of the existing provider-trace requirements. The v2 traces "
                    "negotiated the token but carried frame names only and listed payload schema validation as a future-host item, so they executed no payload "
                    "law. The v2 R-TRACE-* standing rested on transition-only evidence. Executed in source42.v3; the v2 trace bytes are preserved.",
     "selector": "charter.md line 248; native-evidence.md s9.1 lines 2785-2791 and s9.6 lines 2896-3018; native/fact-batch.schema.v3.json; native/dispatch-binding.schema.v1.json",
     "measured": "traces/payload-vectors.json; traces/{complete,unavailable,cancel,fault,terminal}.json#/traces/*/payloadResults; logs/s42v3-p3b.*; preserved/s42-v2-final/"},
    {"id": "own source42.v3 review: ACCEPT-RECONSTRUCTABLE with R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR executed on 53 graph-query vectors",
     "disposition": "R-GRAPH-QUERY standing superseded (found in source43.v1, HC-54). Re-audited against the current query projection contract, that helper "
                    "omitted the s4 traversal-hop edge law, the s7 closed availability vocabulary (missing, reference precondition, host-adapter route, retained "
                    "availability record), the s7 typed close_run outcomes (evidence.regeneration-mismatch; non-typed exception -> HOST.INVARIANT_VIOLATED; no "
                    "message-text routing) and the carrier remedies. The source42 bytes of the contract are not in my custody. The net change is +579 bytes, "
                    "far less than the corrected law text, so at least part of these laws was already present in the source42 bytes and the source42.v3 standing "
                    "rested on a helper omission. Every other source42.v3 result is unaffected by the kit delta and is reused with custody.",
     "selector": "workflows/query-projection-contract.v3.md s2, s4 graph.path row paragraph, s7 availability/host-adapter/close_run paragraphs and table; "
                 "foundation/evaluator-fault-observation.schema.v3.json#/x-opensip-routes",
     "measured": "vectors/graph-query.json#/source43ReAudit/prePost (unchanged helper vs corrected helper on every source43 vector); logs/s43-original.0; logs/s43-hc54c.0"}]


def advisories():
    keys = cb24_keys()
    return [
        {"id": "A-c1", "title": "Internal refusal names that no kit owner publishes are still spelled with the reconstruction prefix cb24.",
         "selectors": ["native-evidence.md s10 route registry (x-opensip-public-route-registry)", "identity-schemas.v3.json internal fault lists",
                       "enumeration-plan.schema.v1.json#/x-opensip-new-internal-faults"],
         "measured": f"{len(keys)} distinct cb24.* keys emitted by ref/*.py: {keys}"},
        {"id": "A-c2", "title": "The inherited d9-exit-contract.v1.14 alone refuses the selected host-invariant termination; the successor D9 artifact is a live cross-unit obligation",
         "selectors": ["native-evidence.md lines 3313-3327"], "measured": "vectors/d9-extension-precedence.json"},
        {"id": "A-c3", "title": "Exact-snapshot import correspondence changes import2 on every source change, so gating evidence rules attribute INDETERMINATE evidence-content-changed",
         "selectors": ["workflows-and-surfaces.md s3 lines 440-449"], "measured": "runs/cmp-code-det2"},
        {"id": "A-n1", "title": "Closed per-entry IndeterminateReason order: reason (3), the detector disposition, is unreachable for entries because an indeterminate detector leaves the changed-detector E0 presence null and (1) applies first",
         "selectors": ["workflows-and-surfaces.md s3 lines 402-411"], "measured": "vectors/baseline-e0-e3.json"},
        {"id": "A-n6", "title": "A rust unit's languageMode (rust-cargo vs rust-cargo-prepared) enters UnitMembershipV1 and the default rows; the mode table decides it but U-4b.2 does not restate it and U-4b.5 publishes no retained-record enforcement for it",
         "selectors": ["native-evidence.md lines 165-172, 741-746, 797-799, 1070-1072, 1842-1847"], "measured": "vectors/mode-rust-cargo-prepared.json"},
        {"id": "A-v2-1", "title": "Composition s7 closes typed-prefix references of OUTPUTS and does not say whether typed-prefix values inside workflow-owned Plan input documents are closure references",
         "selectors": ["evaluator-composition-contract.v3.md s7 line 74", "s5 line 54", "identity-and-evidence.md lines 597-600, 627-631"], "measured": "HC-36 reading; runs/cmp-empty, runs/cmp-budget admitted"},
        {"id": "A-v2-2", "title": "policy-derivation3 is a composition output that no run3/seal3/evidence3/proof3 field references, so reachable output-set equality cannot include it; exports retain it as an unreachable non-authoritative frame",
         "selectors": ["evaluator-composition-contract.v3.md s7 lines 70, 76; s9.7"], "measured": "runs/<run>.replay.fromscratch.json#/retainedClosure/unreachableRetained"},
        {"id": "A-v2-3", "title": "identity-and-evidence s3 calls its representation and retention vocabularies closed while the native and relation bundles publish their own x-opensip-digest-law vocabularies",
         "selectors": ["identity-and-evidence.md s3 lines 441-467"], "measured": "vectors/reference-census.json pairs"},
        {"id": "A-s41-1", "title": "run-termination s7.6 step 1 names no key for a non-object while s6 step 1 publishes RUN_TERMINATION_CANDIDATE_NOT_OBJECT; the s6 key is applied at both boundaries",
         "selectors": ["run-termination-contract.v1.md line 173", "run-termination-contract.v1.md line 330"], "measured": "vectors/run-termination.json#non-object"},
        {"id": "A-s41-2", "title": "U-1's 'an omitted value defaults to false for a tsconfig.json entry' reads against s1.2's derivation of an omitted allowJs from checkJs; the s1.2 derivation is applied",
         "selectors": ["native-evidence.md lines 656-659", "native-evidence.md lines 524-526 and 562-563", "native-evidence.md line 162"],
         "measured": "vectors/discovery-membership.json#s12-effective-allowjs-mode-selection case tsconfig-checkjs-true"},
        {"id": "A-s42-1", "title": "enumeration contract s1 makes provenance=default-unit at most one binding per cell at ordinal 0 but names no refusal key and no schema constraint; the reconstruction refuses with its own cb24.ENUMERATION_DEFAULT_UNIT_CARDINALITY",
         "selectors": ["enumeration-contract.v1.md line 21", "enumeration-plan.schema.v1.json#/$defs/AvailableProgramBindingV1/properties/provenance"],
         "measured": "runs/syntax-code~second-default-unit-binding.replay.json"},
        {"id": "A-s42-2", "title": "enumeration contract s1 names ENUMERATION_BINDING_PROGRAM_ENTRY for a non-null default-unit programEntry; the key for a derived-entry or explicit-entry mismatch against the retained entryConfigPath is not named there, and native U-0 attributes the same join to that key; it is applied to all three",
         "selectors": ["enumeration-contract.v1.md lines 26 and 37", "native-evidence.md line 650", "enumeration-plan.schema.v1.json AvailableProgramBindingV1.programEntry description"],
         "measured": "runs/ts-pass~explicit-entry-not-graph-entry.replay.json"},
        {"id": "A-s42-3", "title": "enumeration contract s1 line 21 says a syntax-only cell's default binding is backed by the U-9 fallback unit and line 22 reserves explicit-plan-selection for extra programs the Plan actually selected, but no published rule or key refuses a sole syntax-only binding spelled explicit-plan-selection with programEntry null; the two spellings mint different EnumerationPlanV1 digests (and PlanIds) for one selection. The reconstruction builds default-unit (HC-47) and invents no refusal",
         "selectors": ["enumeration-contract.v1.md lines 21-22", "enumeration-contract.v1.md line 35", "enumeration-plan.schema.v1.json#/$defs/AvailableProgramBindingV1/properties/provenance"],
         "measured": "selfcheck/s42-prepost-matrix.json: the 4 original syntax positives (explicit-plan-selection) ADMIT under the corrected code and the rebuilt ones (default-unit) ADMIT, with different identities"},
        {"id": "A-s42v3-1", "title": "typescript-semantic major 2 is published only as deltas (native s9.4) over the delivery.v2 major-1 wire, which leaves two gaps. "
                                     "(1) s9.1 names the token-absent FactBatch payload 'historical FactBatchV2' for both majors. The only published FactBatchV2 closed list "
                                     "is rust-provider-protocol.v2, and delivery.v2 still publishes the TypeScript FactBatch payload as FactBatchV1 {facts, "
                                     "batchCommitment}, unlisted in native s0's superseded-selector table. (2) No TypeScript major-2 Hello/HelloAck schema exists: "
                                     "HelloV3/HelloAckV3 fix protocolMajor 3. The explicit current s9.1 sentence and the FactBatchV3 description ('Preserves historical "
                                     "FactBatchV2 field names analysisOrdinal, stageId, batchIndex, candidates'; whenAbsent 'no schemaVersion, no occupancyCompanions') "
                                     "determine the TypeScript unnegotiated payload, and the reconstruction applies it. A TypeScript FactBatchV1-shaped payload therefore "
                                     "refuses, and TypeScript Hello payloads are admitted on the shared HelloV3 members with protocolMajor substituted.",
         "selectors": ["native-evidence.md lines 2774, 2785-2791, 2828, 2879-2888, 2912", "native-evidence.md lines 114-116 (delivery.v2 superseded selectors)",
                       "delivery.v2.json payloadSchemas.FactBatchV1 (line 855) and frameSchemas.FactBatch (line 874)", "rust-provider-protocol.v2.json FactBatchV2 (line 411)",
                       "native/fact-batch.schema.v3.json#/description and #/x-opensip-negotiation/whenAbsent", "native/native-evidence.schemas.v2.json#/$defs/HelloV3/properties/protocolMajor (line 4035)"],
         "measured": "traces/payload-vectors.json#SEL-ts-unnegotiated-delivery-v2-FactBatchV1-shape (refuses cb24.FACT_BATCH_V2_SCHEMA; its member set equals delivery.v2 "
                     "FactBatchV1's required list, so the alternative reading would admit it); traces/controls.json#/helloSchemas (ts entries record the protocolMajor "
                     "substitution); first-run failure logs/s42v3-p3.1.phase3_traces.log"},
        {"id": "A-s43-1", "title": "query-projection-contract s7 makes an omitted availability observation neither a grant nor a purge and reports only an observed "
                                   "retained/partial state 'exactly as observed', while GraphQueryContextV1.availability is required. The value of a successful graph "
                                   "response with no observation is not stated. This is a reference-harness case only: a product host always holds the current "
                                   "availability record (identity-and-evidence: current availability is a separate record; 'A query reports both'). The "
                                   "reconstruction reports 'retained' after close_run admits and otherwise reports the observed state.",
         "selectors": ["workflows/query-projection-contract.v3.md s7 (availability paragraph: 'Omitted availability is not a grant and not a purge')",
                       "workflows/schemas/evaluator3/graph-query.schema.json#/$defs/GraphQueryContextV1/required (availability)",
                       "identity-and-evidence.md lines 1721-1725"],
         "measured": "vectors/graph-query.json vectors without an availability observation report context.availability retained; availability-retained-observed "
                     "and retained-availability-record-partial report the observed state"}]


LIMITATIONS = [
    "run-termination s7.5 row 2 and s5 stage-terminal carriers are not exercised on built Runs (no provider-unavailable primary or retained stage terminal); vectors/run-termination.json#/notConstructedFromBuiltRuns",
    "docs/coop/design-corrections/discovery-defaults.py is a reference implementation the native U-4a text governs; it was not read or used",
    "Future qualification unperformed: real OS/compiler/crypto/SQLite, provider execution as enforcement, host authentication, synthetic TCB enforcement",
    "The independent retained-closure walker (ref/retained_graph.py) executes retention, identity, schema and registry joins, closure membership/kinds, selected-import membership and the SourceUnitOwnershipV1 unitId derivation; owner-semantic admissions it names as delegated (languageVersionBinding derivation, clones framed-body-identity parse joins, native context/universe admission and binding, enumeration and execution-input derivation) stay with owner graph admission, which runs as its own stage",
    "Census classes no constructed claimed-positive graph contains have no negative and are not claimed (vectors/retention-negatives.json#/censusPairsNotReachedByConstructedPositives)",
    "Negatives, positives and controls are closed by the corrected code and, in fresh processes, by the unchanged ported helpers (preserved/pre-s42; selfcheck/s42-prepost-matrix.json)",
    "No Run uses an explicit-plan-selection binding as a positive, a js-synthesized or jsconfig default-unit binding, or a Rust explicit binding; those programEntry branches are exercised only by the explicit-entry control and by reading",
    "PolicyTestSuiteV2 (workflows s5 authoring test) is constructed by no original requirement and by no helper; read, not exercised",
    "The native U-8 (path, reason) superset join between security's admitted boundary inventory and the host marker inventory is pre-Plan and not retained by the Plan; not constructed",
    ("Provider-trace payload law (source42.v3, HC-53): negotiated FactBatchV3 versus historical FactBatchV2 selection, exact deterministic-CBOR payload bytes, "
     "DispatchBindingV1 request/batch correlation and companion association are executed on constructed payloads, in the payload-carrying traces and in "
     "traces/payload-vectors.json. They are not executed on built Runs, which retain no FactBatch frames. The post-terminal bind_worker_occupancy "
     "(fact2 minting, native views, stageReceipts, TargetAttributionV2 projection and capture, C15), payload bodies of other frames, and anchor admission "
     "of the constructed candidates are not constructed by these vectors. No actual worker-process enforcement is claimed. The standing of the retained "
     "Plan fragment is stated in vectors/payload_fixtures.py."),
    ("Graph query typed close_run outcomes (source43, HC-54): identity's typed outcome classes are reconstructed by normalizing my own ref/closure.close_run "
     "structured refusal (refusing stage plus leading typed fault key, never the detail text). The host-adapter route and retained availability-record admission "
     "are exercised as reference vectors, not as an implemented host adapter or evidence store."),
    ("Reuse in source43 (selfcheck/s43-provenance.json): every measurement other than the graph query, from-scratch closure/replay, export replay, admission log, "
     "custody and checkpoints is an exact source42 measurement reused because the only changed kit member is prose read by no other helper, helper bytes are "
     "rebound-only and stores are byte-identical; it was not re-executed in source43.")]


def status_rows():
    st = S.load_status()
    return st, st["rows"]


def build_review(rows):
    fs = json.load(open(OUT + "runs/from-scratch.summary.json"))
    ex = json.load(open(OUT + "runs/replay-export.summary.json"))
    cust = json.load(open(OUT + "runs/final-custody.json"))
    positives = [r["run"] for r in fs["runs"] if r["role"] == "claimed-positive"]
    run_ids = {p: json.load(open(OUT + f"runs/{p}.replay.fromscratch.json"))["runId"] for p in positives}
    unexecuted = [r["id"] for r in rows if r["status"] == "unexecuted" and r["acceptBlocking"]]
    failed = [r["id"] for r in rows if r["status"] == "failed"]
    neg = json.load(open(OUT + "vectors/retention-negatives.json"))
    pm = json.load(open(OUT + "selfcheck/s42-prepost-matrix.json"))
    walk_ok = all((r.get("retainedClosure") or {}).get("result") == "ADMIT" and (r.get("reachableOutputSet") or {}).get("equal")
                  for r in fs["runs"] if r["role"] == "claimed-positive")
    positives_ok = fs["allClaimedPositivesAdmitted"] and fs["allDesignedNegativesRefused"] and ex["allExportedAndEqual"] and \
        {r["run"] for r in ex["runs"]} == set(positives) and walk_ok
    custody_ok = cust["result"] == "PASS"
    controls_ok = bool(pm["controls"]) and sorted(pm["controlsPostCodeRefuse"]) == sorted(c["control"] for c in pm["controls"])
    tc = json.load(open(OUT + "traces/controls.json"))
    tv = json.load(open(OUT + "traces/payload-vectors.json"))
    trace_payload_ok = tc["assertionFailures"] == [] and tv["assertionFailures"] == [] and tc["factBatchPayloads"]["validated"] > 0 and \
        tc["factBatchPayloads"]["negotiatedV3Admitted"] > 0 and tc["factBatchPayloads"]["unnegotiatedV2Admitted"] > 0
    payload_law = {"traceFactBatchPayloads": tc["factBatchPayloads"], "standaloneVectors": len(tv["vectors"]), "groups": tv["groups"],
                   "decoderVectors": len(tv["decoderVectors"]), "encoderVectors": len(tv["encoderVectors"]), "violationKeysExercised": tv["violationKeysExercised"],
                   "hc51": {k: tv["hc51"][k] for k in ("correctedSchemaAdmitted", "unchangedKitRefusedOrderAnnotationUnknown", "tokenCensus")},
                   "kitVectorCrossCheck": tv["kitVectorCrossCheck"], "assertionFailures": tc["assertionFailures"] + tv["assertionFailures"]}
    gq = json.load(open(OUT + "vectors/graph-query.json"))
    prov = json.load(open(OUT + "selfcheck/s43-provenance.json"))
    ra = gq["source43ReAudit"]
    query_ok = gq["assertionFailures"] == [] and all(p["differs"] == (p["expected"] == "differ") for p in ra["prePost"])
    reuse_ok = prov["reusePreconditionsHold"] and fs.get("everyResultMatchesOriginal") is True
    query_reaudit = {"contract": ra["contract"], "counts": gq["counts"], "lawAudit": [{k: row.get(k) for k in ("selector", "unchangedHelper", "correction")} for row in ra["lawAudit"]],
                     "prePost": [{"vector": p["vector"], "expected": p["expected"], "unchangedSource42v3Helper": p["unchangedSource42v3Helper"],
                                  "correctedHelper": {k: v for k, v in p["correctedHelper"].items() if k != "items"}} for p in ra["prePost"]],
                     "tamperedStoreCloseRun": ra["tamperedStoreCloseRun"], "assertionFailures": gq["assertionFailures"]}
    if MUST or SHOULD or unexecuted or failed or not positives_ok or not custody_ok or not neg["allPass"] or not controls_ok or not trace_payload_ok \
            or not query_ok or not reuse_ok:
        verdict = "CHANGES_REQUIRED"
    else:
        verdict = "ACCEPT-RECONSTRUCTABLE"
    counts = {"requirements (R-*)": sum(1 for r in rows if r["id"].startswith("R-")),
              "standingRules (S-*)": sum(1 for r in rows if r["id"].startswith("S-")),
              "futureQualification (F-*)": sum(1 for r in rows if r["id"].startswith("F-")),
              "executed": sum(1 for r in rows if r["status"] == "executed"), "unexecuted": sum(1 for r in rows if r["status"] == "unexecuted"),
              "failed": len(failed), "claimedCompletePositives": len(positives)}
    return {"consumerId": S.CONSUMER, "runtime": "consumer-b.v24-source43.v1",
            "copiedFromRuntime": "consumer-b.v24-source42.v3 (continued from consumer-b.v24-source42.v2 and .v1)",
            "origin": "9d3dfb70-b2d3-498c-a3c1-f8de9e488514 (continuation; independence not claimed anew)",
            "kit": {"consumerInputManifestSha256": cust["manifestSha256"], "parentSubjectSha256": cust["parentSubjectSha256"]},
            "verdict": verdict, "standing": STANDING,
            "verdictBasis": {"newMustIssues": len(MUST), "newShouldIssues": len(SHOULD), "unexecutedAcceptBlocking": unexecuted, "failed": failed,
                             "claimedCompletePositivesAllAdmittedReplayedExported": positives_ok,
                             "claimedCompletePositivesRetainedClosureAdmittedAndReachableSetEqual": walk_ok,
                             "retentionNegativesAllPass": neg["allPass"], "finalCustody": cust["result"],
                             "closureControlsRefusedByCorrectedCode": controls_ok,
                             "providerTracePayloadLawExecutedWithoutFailure": trace_payload_ok,
                             "graphQueryReauditedAgainstSource43WithoutFailure": query_ok,
                             "source42MeasurementReuseCustodyHolds": reuse_ok,
                             "ownSource41ExportDefectCorrected": "HC-47", "ownSource42v2TraceOmissionCorrected": "HC-53",
                             "ownSource42v3QueryOmissionCorrected": "HC-54"},
            "kitCustody": cust, "newMustIssues": MUST, "newShouldIssues": SHOULD, "advisories": advisories(),
            "priorIssueDisposition": PRIOR_S41,
            "source43Continuation": {
                "kitDelta": prov["kitDelta"], "changedMemberConsumers": prov["changedMemberConsumers"], "kitProseReaders": prov["kitProseReaders"],
                "rebind": "rebind-s43-manifest.json (102 files, 121 occurrences; HC-55)", "source42v3FinalBytesOfChangedFiles": "preserved/s42-v3-final/manifest.json",
                "source42v3ResultHashes": "preserved/s42-v3-final/runs-manifest.json", "provenance": "selfcheck/s43-provenance.json",
                "storesByteIdenticalToSource42v3": not prov["storeByteDifferences"], "graphQueryReaudit": query_reaudit,
                "executedFresh": prov["freshInSource43"], "reusedExactSource42Measurements": prov["reusedExactSource42Measurements"],
                "supersededInSource43": prov["supersededInSource43"]},
            "source42v3Continuation": {
                "rebind": "rebind-v3-manifest.json (100 files, 120 occurrences; HC-52)", "v2FinalBytesOfChangedFiles": "preserved/s42-v2-final/manifest.json",
                "providerTracePayloadLaw": payload_law,
                "executedFresh": ["logs/s42v3-p3.0/.1 (own construction errors, preserved)", "logs/s42v3-p3b.0.phase3_payload_vectors.log", "logs/s42v3-p3b.1.phase3_traces.log",
                                  "phase 0 custody, checkpoints 0-3, final custody, phases 10-11 (logs/s42v3-fin.*)"],
                "reusedUnchanged": ("every other v2 measurement: builds, stores and the 27 exported positives with run ids, from-scratch closure, export replay, "
                                    "admission log, mutation replay, tamper, retention negatives, pre/post matrix, provenance, phases 4-9 vectors and checkpoints 4-9 "
                                    "(no input or helper they execute changed; ref/schemas.py and ref/protocol3.py are byte-unchanged)")},
            "priorHistory": {"source42.v3": "/tmp/opensip-design-corrections/consumer-b.v24-source42.v3/output/blind-review.json (ACCEPT-RECONSTRUCTABLE on the source42 kit; "
                                            "its R-GRAPH-QUERY standing superseded by HC-54; exact bytes of changed files at preserved/s42-v3-final/)",
                             "source42.v2": "/tmp/opensip-design-corrections/consumer-b.v24-source42.v2/output/blind-review.json (ACCEPT-RECONSTRUCTABLE; its R-TRACE-* "
                                            "standing rested on transition-only traces; superseded by HC-53; v2 bytes of changed files at preserved/s42-v2-final/)",
                             "source42.v1": "/tmp/opensip-design-corrections/consumer-b.v24-source42.v1 (incomplete pass, no review)",
                             "source41.v1": "preserved/source41-v1/blind-review.json (ACCEPT-RECONSTRUCTABLE on the source41 kit; superseded by HC-47)",
                             "source39.v3 and earlier": "preserved/source41-v1/preserved/ (copied non-store history and hash manifests)"},
            "source42Continuation": {"portManifest": "port-manifest.json", "unchangedHelperState": "preserved/s42-original-state/manifest.json",
                                     "unchangedHelperExecutionCopy": "preserved/pre-s42/manifest.json",
                                     "prePostMatrix": {k: v for k, v in pm.items() if k not in ("rows", "controls")}, "prePostControls": pm["controls"],
                                     "provenance": "selfcheck/s42-provenance.json", "lawChecks": "notes/01-source42-law-deltas.md",
                                     "referenceCensus": "vectors/reference-census.json", "retainedClosureWalker": "ref/retained_graph.py",
                                     "retentionNegatives": {"file": "vectors/retention-negatives.json", "constructed": neg["constructed"], "allPass": neg["allPass"],
                                                            "notConstructed": neg["notConstructed"],
                                                            "censusPairsNotReached": neg["censusPairsNotReachedByConstructedPositives"]}},
            "limitations": LIMITATIONS,
            "claimedCompletePositives": [{"run": p, "runId": run_ids[p], "store": f"runs/{p}.store.json", "replay": f"runs/{p}.replay.json",
                                          "fromScratch": f"runs/{p}.replay.fromscratch.json", "replayExport": f"runs/{p}.replay-export.json",
                                          "recordLog": f"runs/{p}.records.json"} for p in positives],
            "fromScratchCommand": "cd /private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/output && /tmp/opensip-architecture-review-env/bin/python -I -B tools/from_scratch.py && "
                                  "/tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_export.py",
            "rootAdmission": "unobserved; exact exported object tables and blobs are exposed for root admission",
            "futureQualificationUnperformed": [r["id"] for r in rows if r["status"] == "futureQualification"],
            "helperCorrections": HC.all_entries() + HC43.all_entries(), "helperCorrectionsCarried": HC43.CARRIED, "counts": counts,
            "requirementStatus": [{k: r[k] for k in ("id", "phase", "kind", "acceptBlocking", "status", "artifact", "firstRefusal", "notes")} for r in rows]}


def main():
    phase11 = "--phase11" in sys.argv
    st, rows = status_rows()
    if not phase11:
        adv = advisories()
        for rid, notes in (("R-IDENTIFY-GAPS", f"{len(MUST)} MUST, {len(SHOULD)} SHOULD and {len(adv)} advisories with exact selectors. Dispositions: my source41 "
                                               f"results (HC-47), my source42.v2 provider-trace limitation (HC-53; A-s42v3-1), and my source42.v3 graph-query standing "
                                               f"under the changed source43 query projection contract (HC-54; A-s43-1 added). All acceptBlocking items executed "
                                               f"(notes/10-gaps.md, notes/01-source42-law-deltas.md, notes/11-provider-trace-payload-law.md, notes/12-source43-query-contract.md)."),
                           ("R-FREEDOM-VS-MISSING", "adjudication rules separate algorithm freedom from missing/contradictory contracts (notes/10-gaps.md#adjudication-rules)."),
                           ("R-BLOCKER-NOT-ADJUST", "every promised vector built; cb24 names are declared reconstruction keys; readings adopted where text is ambiguous are "
                                                    "named with measured alternatives (A-s42-1, A-s42-2, A-s41-1, A-s41-2, A-v2-1, A-s42v3-1, A-s43-1); internal payload-law keys "
                                                    "record kit-text, key-name or cb24 binding per key; no meaning adjusted; no author code imported.")):
            S.set_status(st, rid, "executed", "notes/10-gaps.md", None, notes)
        S.save_status(st)
        review = build_review(st["rows"])
        json.dump(review, open(REVIEW_JSON, "w"), indent=1)
        cp = S.write_checkpoint(10, st, ["notes/10-gaps.md", "notes/01-source42-law-deltas.md", "notes/11-provider-trace-payload-law.md",
                                         "notes/12-source43-query-contract.md", "blind-review.json", "tools/finalize_review.py", "tools/hc_source42.py",
                                         "tools/hc_source43.py", "runs/final-custody.json", "vectors/discovery-membership.json", "vectors/retention-negatives.json",
                                         "selfcheck/s42-prepost-matrix.json", "selfcheck/s42-provenance.json", "selfcheck/s43-provenance.json",
                                         "traces/payload-vectors.json", "traces/controls.json", "vectors/graph-query.json"], HC.all_entries() + HC43.all_entries(),
                                f"Phase 10 adjudicated in runtime source43.v1 on the source43 kit: verdict basis {json.dumps(review['verdictBasis'])}. " + HC43.CARRIED)
        print(json.dumps({"verdict": review["verdict"], "basis": review["verdictBasis"], "checkpointUnexecuted": cp["requirementIdsUnexecuted"],
                          "checkpointFailed": cp["requirementIdsFailed"], "counts": review["counts"]}, indent=1))
        return 0
    md = open(REVIEW_MD).read() if os.path.exists(REVIEW_MD) else ""
    # HC-46 (carried): judge the review the phase-11 standing would yield, not the interim phase-10 JSON
    prospective_status = copy.deepcopy(st)
    for rid in PHASE11_IDS:
        S.set_status(prospective_status, rid, "executed")
    review = build_review(prospective_status["rows"])
    enum_ok = review["verdict"] in ("ACCEPT-RECONSTRUCTABLE", "CHANGES_REQUIRED", "BLOCKED")
    basis = review["verdictBasis"]
    gaps_consistent = (review["verdict"] != "ACCEPT-RECONSTRUCTABLE") == bool(review["newMustIssues"] or review["newShouldIssues"] or basis["unexecutedAcceptBlocking"]
                                                                                or basis["failed"] or not basis["claimedCompletePositivesAllAdmittedReplayedExported"]
                                                                                or basis["finalCustody"] != "PASS" or not basis["retentionNegativesAllPass"]
                                                                                or not basis["closureControlsRefusedByCorrectedCode"]
                                                                                or not basis["providerTracePayloadLawExecutedWithoutFailure"]
                                                                                or not basis["graphQueryReauditedAgainstSource43WithoutFailure"]
                                                                                or not basis["source42MeasurementReuseCustodyHolds"])
    md_ok = review["verdict"] in md and "no product qualification claim" in md.lower() and \
        all(i["id"] in md for i in review["newMustIssues"] + review["newShouldIssues"] + review["advisories"])
    shaped = isinstance(review["newMustIssues"], list) and isinstance(review["newShouldIssues"], list) and \
        all(i["selectors"] and i["measured"] for i in review["newMustIssues"] + review["newShouldIssues"] + review["advisories"]) and bool(review["advisories"])
    for rid, ok, art, notes in (
            ("R-DELIVER-MD-JSON", bool(md) and os.path.exists(REVIEW_JSON) and md_ok, "blind-review.md", "blind-review.md and blind-review.json with retained sources, runs and vectors."),
            ("R-VERDICT-ENUM", enum_ok, "blind-review.json", f"verdict {review['verdict']}; derived from issues and measured standing."),
            ("R-MUST-SHOULD-ADVISORY", shaped, "blind-review.json",
             f"newMustIssues ({len(review['newMustIssues'])}) and newShouldIssues ({len(review['newShouldIssues'])}); "
             f"{len(review['advisories'])} advisories reported separately, each with selectors and a measurement."),
            ("R-NO-ACCEPT-IF-INCOMPLETE", gaps_consistent, "blind-review.json", "verdict is ACCEPT exactly when no gap, unexecuted accept-blocking ID, failed ID, failed positive, custody failure, failed negative or unrefused control exists."),
            ("R-NO-QUALIFICATION-CLAIM", "no product qualification claim" in review["standing"].lower() and "no product qualification claim" in md.lower(), "blind-review.md",
             "standing text in both files.")):
        S.set_status(st, rid, "executed" if ok else "failed", art, None, notes)
    S.save_status(st)
    refreshed = build_review(st["rows"])
    if refreshed["verdict"] not in md:
        S.set_status(st, "R-DELIVER-MD-JSON", "failed", "blind-review.md", None, f"blind-review.md does not state the derived verdict {refreshed['verdict']}")
        S.save_status(st)
        refreshed = build_review(st["rows"])
    json.dump(refreshed, open(REVIEW_JSON, "w"), indent=1)
    cp = S.write_checkpoint(11, st, ["blind-review.md", "blind-review.json", "requirement-status.json"], [],
                            f"Final verdict {refreshed['verdict']}; counts {json.dumps(refreshed['counts'])}")
    print(json.dumps({"verdict": refreshed["verdict"], "basis": refreshed["verdictBasis"], "checkpointUnexecuted": cp["requirementIdsUnexecuted"],
                      "checkpointFailed": cp["requirementIdsFailed"], "counts": refreshed["counts"]}, indent=1))
    return 0 if not cp["requirementIdsUnexecuted"] and not cp["requirementIdsFailed"] else 1


if __name__ == "__main__":
    sys.exit(main())
