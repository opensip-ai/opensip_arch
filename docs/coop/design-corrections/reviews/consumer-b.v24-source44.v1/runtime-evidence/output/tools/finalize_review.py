"""Phase 10/11 finalization from measured source44 standing (runtime consumer-b.v24-source44.v1, continuing source43.v1 and source42.v1-.v3).

python3 tools/finalize_review.py            -> records phase-10 standing, writes checkpoint 10 and blind-review.json
python3 tools/finalize_review.py --phase11  -> verifies blind-review.md/json against the charter rules, records phase-11 standing,
                                               writes checkpoint 11 and refreshes blind-review.json requirementStatus
The verdict is derived. ACCEPT-RECONSTRUCTABLE requires all of: no MUST/SHOULD issue; no unexecuted accept-blocking ID; no failed ID; final custody
PASS; all retention negatives passing; every closure control refused by the corrected code; every claimed complete positive admitted by owner
admission, the independent retained closure and replay with reachable-set equality, and exported; the provider wire/trace law executed without
failure; and reuse custody holding. Otherwise the verdict is CHANGES_REQUIRED (BLOCKED is reserved for an unbuildable promised vector). The source43
bytes of this tool are preserved at preserved/s43-final/tools/finalize_review.py.
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
import hc_source44 as HC44  # noqa: E402
import status as S  # noqa: E402

OUT = S.OUT
REVIEW_JSON = OUT + "blind-review.json"
REVIEW_MD = OUT + "blind-review.md"
PRIOR_STANDING = json.load(open(OUT + "preserved/s43-final/blind-review.json"))["standing"]
STANDING = ("Independent reconstruction of the source44 normative kit (manifest a3a5fba8..., parent e873c8db...) in runtime consumer-b.v24-source44.v1. It "
            "continues the same blind origin from the exact source43.v1 output. Against my own source43 custody rows, six kit members changed and three were "
            "added, all provider wire, startup and attribution owners. An AST read-census finds that only the provider-trace reconstruction reads them "
            "(selfcheck/s44-provenance.json). The unchanged source43 phase-3 helpers were executed on the source44 kit first (preserved/s44-original/). They "
            "did not detect the new law, and were then corrected from the kit: per-language historical FactBatch (HC-57), and the TypeScript protocol-2 "
            "machine, handshake and startup payload admission, derived Rust modes and the pre-Analyze host conversion (HC-58). Executed fresh on the source44 "
            "runtime: the from-scratch closure and complete proof replay of every claimed positive, the export replay, admission log, graph query, reference "
            "census and retention negatives. Every other measurement is reused as an exact prior measurement with custody. Source43 history: " + PRIOR_STANDING)

MUST = [
    {"id": "M-s44-1",
     "title": ("The pre-Analyze Unavailable host conversion does not determine the closedWorld of the CoverageResultV3 it commits. native-evidence s9.7 and "
               "provider-startup hostConversion fix every other member, but give closedWorld only as closed_world_v2(no manifest, entry points none, no "
               "edges, externalConsumers unknown), a function no kit owner publishes. s4.5 decides exportsClosed=closed and deadCodeRepairEligible only; "
               "FR-3 supports exportsClosed unknown. dynamicDispatch (resolved or not-applicable) and reasons are published nowhere for this input. These are "
               "committed coverage2 bytes, so two conforming hosts mint different coverage2 identities (and everything citing them) for the same clean "
               "native-context-mismatch terminal."),
     "selectors": ["docs/v2/contracts/product-v1/native-evidence.md s9.7 lines 3234-3249 (closedWorld: closed_world_v2 ..., line 3241)",
                   "docs/coop/design-corrections/native/provider-startup.schemas.v1.json#/x-opensip-startup-law/preAnalyzeUnavailable/hostConversion",
                   "docs/v2/contracts/product-v1/native-evidence.md s4.5 lines 2208-2242 and FR-3 lines 2768-2777",
                   "docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/$defs/ClosedWorldV2 (reasons: free strings, no vocabulary)"],
     "measured": ("traces/startup-vectors.json#/conversion: for both languages, four closedWorld candidates each admit (CoverageResultV3 schema, RC-1/RC-2/RC-6, "
                  "cause registry, s4.5 ingredient rules; stage_authority unavailable admits StageAuthorityV1), and every requested key gets four distinct coverage2 "
                  "identities (conversion.languages.*.distinctCoverage2ForEveryKey). Controls: exportsClosed closed and deadCodeRepairEligible true refuse. "
                  "The traces apply reading A (unknown, not-applicable, no reasons) and label it; logs/s44-p3b.0 and its rerun."),
     "requiredChange": ("Publish closed_world_v2's result for the conversion input (every ClosedWorldV2 member, including dynamicDispatch and the exact reasons "
                        "array), or publish the closedWorld value of the minted entry directly in s9.7 and the startup law.")}]
SHOULD = []
PHASE11_IDS = ("R-DELIVER-MD-JSON", "R-VERDICT-ENUM", "R-MUST-SHOULD-ADVISORY", "R-NO-ACCEPT-IF-INCOMPLETE", "R-NO-QUALIFICATION-CLAIM")


def cb24_keys():
    keys = set()
    for p in sorted(glob.glob(OUT + "ref/*.py")):
        keys |= set(re.findall(r'["(]cb24\.([A-Za-z][A-Za-z0-9_.-]*)', open(p).read()))
    return sorted(keys)


PRIOR = json.load(open(OUT + "preserved/s43-final/blind-review.json"))["priorIssueDisposition"] + [
    {"id": "own source43.v1 advisory A-s42v3-1: typescript-semantic token-absent payload read as FactBatchV2, and TypeScript Hello/HelloAck admitted on "
           "HelloV3/HelloAckV3 with protocolMajor substituted",
     "disposition": ("withdrawn (source44.v1). The source44 kit now publishes both: the typescript-semantic historical payload is delivery.v2 FactBatchV1 with "
                     "batchCommitment, and TypeScriptHelloV2/TypeScriptHelloAckV2 exist. The reading is superseded by the current owners, and the helper is "
                     "corrected (HC-57, HC-58). It is not a gap in the current kit."),
     "selector": ("native-evidence.md s9.1 and s9.4; native/fact-batch.schema.v3.json#/x-opensip-negotiation/whenAbsent; native/provider-handshake.schemas.v1.json#"
                  "/x-opensip-wire-law/factBatch and #/$defs/TypeScriptHelloV2,TypeScriptHelloAckV2,TypeScriptFactBatchV1Vector"),
     "measured": "traces/payload-vectors.json#SEL-ts-unnegotiated-v1 (ADMIT) and #SEL-ts-unnegotiated-v2 (REFUSE cb24.FACT_BATCH_V1_SCHEMA); logs/s44-original.0 (unchanged helper)"},
    {"id": "own source43.v1 review: ACCEPT-RECONSTRUCTABLE with R-TRACE-* executed on protocol3-table traces with Hello/HelloAck and FactBatch payloads only",
     "disposition": ("superseded for the provider traces under the source44 owners (HC-57, HC-58). On the source44 kit the unchanged helper exits 0 and "
                     "detects none of the following: TypeScript exchanges belong on typescript-protocol2-order.v1.json (a TypeScript Unavailable after output and a "
                     "TypeScript ProviderFault fault there); Rust modes are derived from the admitted OpenUniverseV3; startup, coverage, terminal and cancellation "
                     "payloads are admitted; the pre-Analyze host conversion. Every other source43 result is either unaffected and reused, or re-executed fresh with "
                     "equal outcomes."),
     "selector": ("native/typescript-protocol2-order.v1.json; native/protocol3-transitions.v1.json#/derivedObservations,rowPayloads; "
                  "native/provider-startup.schemas.v1.json; native-evidence.md s9.7"),
     "measured": "preserved/s44-original/traces/ and logs/s44-original.1 (unchanged); traces/*.json, traces/abstract.json, logs/s44-p3.2 (corrected)"}]


def advisories():
    prior = [a for a in json.load(open(OUT + "preserved/s43-final/blind-review.json"))["advisories"] if a["id"] != "A-s42v3-1"]
    # native-evidence.md changed in source44. Carried native line selectors were re-located in the source44 bytes: +11 before s9, confirmed at lines
    # 173-174, 535-537, 573-574, 661 and 667-670; the D9 composition passage is at 3565-3600.
    relocated = {"A-c2": ["native-evidence.md lines 3565-3600 (source43: 3313-3327)"],
                 "A-n6": ["native-evidence.md lines 176-183, 752-757, 808-810, 1081-1083, 1853-1858 (source43: 165-172, 741-746, 797-799, 1070-1072, 1842-1847)"],
                 "A-s41-2": ["native-evidence.md lines 667-670 (source43: 656-659)", "native-evidence.md lines 535-537 and 573-574 (source43: 524-526, 562-563)",
                             "native-evidence.md line 173-174 (source43: 162)"]}
    for a in prior:
        if a["id"] == "A-c1":
            keys = cb24_keys()
            a["measured"] = f"{len(keys)} distinct cb24.* keys emitted by ref/*.py: {keys}"
        if a["id"] in relocated:
            a["selectors"] = relocated[a["id"]]
        if a["id"] == "A-s42-2":
            a["selectors"] = [s.replace("native-evidence.md line 650", "native-evidence.md line 661 (source43: 650)") for s in a["selectors"]]
    return prior + [
        {"id": "A-s44-1", "title": ("The return law's summary sentences still name historical FactBatchV2 for any token-absent worker. The same document's "
                                    "per-mode worker rows, native s9.1/s9.2/s9.6, fact-batch v3 whenAbsent, the occupancy companion x-opensip-wire and the "
                                    "provider-handshake wire law are all per-language (typescript-semantic FactBatchV1). Advisory, not SHOULD: the capture result "
                                    "the return law owns is language-independent (token absent: no companion capture, occupancy unknown except exact-id "
                                    "ephemeral), and payload selection has explicit per-language owners."),
         "selectors": ["foundation/provider-target-attribution-return.schema.v2.json#/x-opensip-return-law/standing (line 65)",
                       "#/x-opensip-return-law/boundary/compilerWorkerTransport (line 67)", "#/x-opensip-return-law/missingAndIncomplete/missingToken (line 117)",
                       "#/x-opensip-return-law/producerSupply/modes (lines 138, 149)", "native-evidence.md lines 2801-2810, 2883, 3065-3067"],
         "measured": "traces/payload-vectors.json#SEL-ts-unnegotiated-v1 ADMIT, #SEL-ts-unnegotiated-v2 REFUSE cb24.FACT_BATCH_V1_SCHEMA, #SEL-rust-unnegotiated-v2 ADMIT"},
        {"id": "A-s44-2", "title": ("native/source-pins.v2.json is cited as the pin authority for expectedProtocolContractSha256 and for the superseded "
                                    "selectors, but it is not a member of the frozen subject. The Hello value stays determined, because the wire law states the "
                                    "digest and it equals the raw SHA-256 of rust-provider-protocol.v2.json."),
         "selectors": ["native/provider-handshake.schemas.v1.json#/x-opensip-wire-law/expectedProtocolContractSha256/rule (line 64)",
                       "native-evidence.md s0 table header (line 112)", "native-evidence.md s12 (line 4069)"],
         "measured": "traces/startup-vectors.json#/wireControls (citedPinDocumentInSubject absent; pinnedInWireLaw equals contractSha256); first-run control logs/s44-p3.1"}]


LIMITATIONS = [l for l in json.load(open(OUT + "preserved/s43-final/blind-review.json"))["limitations"]
               if not l.startswith(("Provider-trace payload law (source42.v3", "Reuse in source43"))] + [
    ("Provider wire and trace law (source42.v3 HC-53; source44 HC-57, HC-58). Executed on constructed payloads joined to my retained ts-pass/rust-mixed Run "
     "values, in the payload-carrying traces and in traces/payload-vectors.json and traces/startup-vectors.json: negotiated FactBatchV3 or the language's "
     "historical payload, exact deterministic-CBOR bytes, the TypeScript batchCommitment, DispatchBindingV1 correlation, companions, handshake/startup/"
     "coverage/terminal/cancellation payloads, and the pre-Analyze host conversion. Not executed: snapshot, dependency-source and prepared custody "
     "payloads (abstract events, as in the kit's s9.7 reference scope); coverage/stream commitment recomputation; descriptor signatures (synthetic trusted "
     "descriptors and rust-v1 row); Rust CancelledV2 observedPhase vocabulary; post-terminal bind_worker_occupancy; anchor admission of constructed "
     "candidates. The fixture Plan (PLAN_ID with a language's retained snapshot2 and native context digests), the synthetic prepared-output set and the "
     "placeholder commitments are host inputs, not a verified Plan or Run. Conversion entries use closedWorld reading A pending M-s44-1. No actual "
     "worker-process enforcement is claimed."),
    ("Reuse in source44 (selfcheck/s44-provenance.json). Executed fresh: phase 3, closure/replay/export/admission log, graph query, census and negatives. "
     "Every other measurement is an exact prior measurement, reused because no helper outside phase 3 reads a changed or added kit member, no unchanged kit "
     "document references a changed $id, helper bytes are rebound-only and stores are byte-identical. It was not re-executed in source44.")]


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
    ts = json.load(open(OUT + "traces/startup-vectors.json"))
    ta = json.load(open(OUT + "traces/abstract.json"))
    machines = tc["machines"]
    trace_payload_ok = (tc["assertionFailures"] == [] and tv["assertionFailures"] == [] and ts["assertionFailures"] == [] and tc["factBatchPayloads"]["validated"] > 0
                        and all(v > 0 for v in tc["factBatchPayloads"]["admittedBySelectedPayload"].values())
                        and all(m["rowsNotExercised"] == [] and m["pairwiseDisjointOverlaps"] == [] for m in machines.values())
                        and all(t["matchesExpected"] for t in ta["tests"]))
    orig_tc = json.load(open(OUT + "preserved/s44-original/traces/controls.json"))
    orig_tv = json.load(open(OUT + "preserved/s44-original/traces/payload-vectors.json"))
    payload_law = {"machines": machines, "traceFactBatchPayloads": tc["factBatchPayloads"], "payloadAdmissions": tc["payloadAdmissions"],
                   "abstractTableTests": [{k: t[k] for k in ("name", "provider", "matchesExpected", "law")} for t in ta["tests"]],
                   "payloadVectors": {"vectors": len(tv["vectors"]), "groups": tv["groups"], "decoderVectors": len(tv["decoderVectors"]),
                                      "encoderVectors": len(tv["encoderVectors"]), "violationKeysExercised": tv["violationKeysExercised"],
                                      "hc51": {k: tv["hc51"][k] for k in ("correctedSchemaAdmitted", "unchangedKitRefusedOrderAnnotationUnknown", "tokenCensus")},
                                      "kitVectorCrossCheck": tv["kitVectorCrossCheck"]},
                   "startupVectors": {"vectors": len(ts["vectors"]), "groups": ts["groups"], "faultKeysExercised": ts["faultKeysExercised"],
                                      "wireControls": ts["wireControls"], "wireCbor": ts["wireCbor"], "determinacyGap": ts["conversion"]["determinacyGap"]},
                   "unchangedSource43HelpersOnSource44Kit": {"tracesAssertionFailures": orig_tc["assertionFailures"], "tracesRowsExercised": orig_tc["rulesExercised"],
                                                             "payloadVectorsAssertionFailures": orig_tv["assertionFailures"],
                                                             "logs": ["logs/s44-original.0.run_preserved_s43.log", "logs/s44-original.1.run_preserved_s43.log"]},
                   "assertionFailures": tc["assertionFailures"] + tv["assertionFailures"] + ts["assertionFailures"]}
    gq = json.load(open(OUT + "vectors/graph-query.json"))
    prov = json.load(open(OUT + "selfcheck/s44-provenance.json"))
    ra = gq["source43ReAudit"]
    query_ok = gq["assertionFailures"] == [] and all(p["differs"] == (p["expected"] == "differ") for p in ra["prePost"])
    rd = json.load(open(OUT + "selfcheck/s44-result-diffs.json"))
    reuse_ok = prov["reusePreconditionsHold"] and fs.get("everyResultMatchesOriginal") is True and rd["result"] == "PASS"
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
    return {"consumerId": S.CONSUMER, "runtime": "consumer-b.v24-source44.v1",
            "copiedFromRuntime": "consumer-b.v24-source43.v1 (continued from consumer-b.v24-source42.v3, .v2 and .v1)",
            "origin": "9d3dfb70-b2d3-498c-a3c1-f8de9e488514 (continuation; independence not claimed anew)",
            "kit": {"consumerInputManifestSha256": cust["manifestSha256"], "parentSubjectSha256": cust["parentSubjectSha256"]},
            "verdict": verdict, "standing": STANDING,
            "verdictBasis": {"newMustIssues": len(MUST), "newShouldIssues": len(SHOULD), "unexecutedAcceptBlocking": unexecuted, "failed": failed,
                             "claimedCompletePositivesAllAdmittedReplayedExported": positives_ok,
                             "claimedCompletePositivesRetainedClosureAdmittedAndReachableSetEqual": walk_ok,
                             "retentionNegativesAllPass": neg["allPass"], "finalCustody": cust["result"],
                             "closureControlsRefusedByCorrectedCode": controls_ok,
                             "providerWireAndTraceLawExecutedWithoutFailure": trace_payload_ok,
                             "graphQueryExecutedWithoutFailure": query_ok,
                             "priorMeasurementReuseCustodyHolds": reuse_ok,
                             "ownSource41ExportDefectCorrected": "HC-47", "ownSource42v2TraceOmissionCorrected": "HC-53",
                             "ownSource42v3QueryOmissionCorrected": "HC-54", "ownSource43TraceReadingsSupersededBySource44Owners": "HC-57, HC-58"},
            "kitCustody": cust, "newMustIssues": MUST, "newShouldIssues": SHOULD, "advisories": advisories(),
            "priorIssueDisposition": PRIOR,
            "source44Continuation": {
                "kitDelta": prov["kitDelta"], "memberReaders": prov["memberReaders"], "nonPhase3Readers": prov["nonPhase3Readers"],
                "genericKitReaders": prov["genericKitReaders"], "changedIdsReferencedByUnchangedKitDocuments": prov["changedIdsReferencedByUnchangedKitDocuments"],
                "rebind": "rebind-s44-manifest.json (104 files, 123 occurrences; HC-56)", "source43FinalBytesOfChangedFiles": "preserved/s43-final/manifest.json",
                "source43ResultHashes": "preserved/s43-final/results-manifest.json", "provenance": "selfcheck/s44-provenance.json",
                "storesByteIdenticalToSource43": not prov["storeByteDifferences"],
                "resultByteDifferencesFromSource43": {k: v for k, v in rd.items() if k != "rows"}, "resultByteDifferenceRows": "selfcheck/s44-result-diffs.json#/rows",
                "providerWireAndTraceLaw": payload_law, "executedFresh": prov["freshInSource44"], "reusedExactPriorMeasurements": prov["reusedExactPriorMeasurements"],
                "supersededInSource44": prov["supersededInSource44"], "notes": "notes/13-source44-provider-wire.md"},
            "source43Continuation": {"review": "preserved/s43-final/blind-review.json", "provenance": "selfcheck/s43-provenance.json (written in runtime source43.v1)",
                                     "graphQueryReaudit": {"contract": ra["contract"], "counts": gq["counts"], "assertionFailures": gq["assertionFailures"],
                                                           "prePostAllAsExpected": query_ok}},
            "priorHistory": {"source43.v1": "preserved/s43-final/blind-review.json (ACCEPT-RECONSTRUCTABLE on the source43 kit; its R-TRACE-* standing superseded "
                                            "under source44 by HC-57/HC-58; exact final bytes of changed files at preserved/s43-final/)",
                             "source42.v3": "ACCEPT-RECONSTRUCTABLE on the source42 kit; R-GRAPH-QUERY standing superseded by HC-54 (preserved/s42-v3-final/)",
                             "source42.v2": "ACCEPT-RECONSTRUCTABLE; R-TRACE-* standing rested on transition-only traces; superseded by HC-53 (preserved/s42-v2-final/)",
                             "source42.v1": "incomplete pass, no review",
                             "source41.v1": "preserved/source41-v1/blind-review.json (ACCEPT-RECONSTRUCTABLE on the source41 kit; superseded by HC-47)",
                             "source39.v3 and earlier": "preserved/source41-v1/preserved/ (copied non-store history and hash manifests)"},
            "limitations": LIMITATIONS,
            "claimedCompletePositives": [{"run": p, "runId": run_ids[p], "store": f"runs/{p}.store.json", "replay": f"runs/{p}.replay.json",
                                          "fromScratch": f"runs/{p}.replay.fromscratch.json", "replayExport": f"runs/{p}.replay-export.json",
                                          "recordLog": f"runs/{p}.records.json"} for p in positives],
            "fromScratchCommand": ("cd /private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/output && for s in tools/from_scratch.py tools/replay_export.py "
                                   "tools/phase9_admission_log.py vectors/phase3_payload_vectors.py vectors/phase3_startup_vectors.py vectors/phase3_traces.py; do "
                                   "/tmp/opensip-architecture-review-env/bin/python -I -B $s || exit 1; done"),
            "rootAdmission": "unobserved; exact exported object tables and blobs are exposed for root admission",
            "futureQualificationUnperformed": [r["id"] for r in rows if r["status"] == "futureQualification"],
            "helperCorrections": HC.all_entries() + HC43.all_entries() + HC44.all_entries(), "helperCorrectionsCarried": HC44.CARRIED, "counts": counts,
            "requirementStatus": [{k: r[k] for k in ("id", "phase", "kind", "acceptBlocking", "status", "artifact", "firstRefusal", "notes")} for r in rows]}


def main():
    phase11 = "--phase11" in sys.argv
    st, rows = status_rows()
    if not phase11:
        adv = advisories()
        for rid, notes in (("R-IDENTIFY-GAPS", f"{len(MUST)} MUST ({', '.join(m['id'] for m in MUST)}), {len(SHOULD)} SHOULD and {len(adv)} advisories with exact "
                                               f"selectors. M-s44-1: the pre-Analyze host conversion leaves closedWorld of committed coverage2 bytes undetermined, "
                                               f"measured by four admitted candidates with distinct identities. New advisories: A-s44-1 (return-law generic "
                                               f"FactBatchV2 wording) and A-s44-2 (cited pin document not a subject member). Withdrawn: A-s42v3-1, superseded by the "
                                               f"source44 owners. Dispositions: my source43 trace standing (HC-57, HC-58). All acceptBlocking items executed "
                                               f"(notes/10-gaps.md, notes/13-source44-provider-wire.md)."),
                           ("R-FREEDOM-VS-MISSING", "adjudication rules separate algorithm freedom from missing or contradictory contracts (notes/10-gaps.md#adjudication-rules). "
                                                    "closedWorld of a minted CoverageResultV3 is committed bytes, not algorithm freedom, so M-s44-1 is a missing contract."),
                           ("R-BLOCKER-NOT-ADJUST", "Every promised vector was built. The host conversion is executed under four measured closedWorld candidates and "
                                                    "reported as M-s44-1, not adjusted. cb24 names are declared reconstruction keys. Readings adopted where text "
                                                    "is ambiguous are named with measured alternatives (A-s42-1, A-s42-2, A-s41-1, A-s41-2, A-v2-1, A-s43-1, "
                                                    "closedWorld reading A under M-s44-1). Internal payload-law keys record kit-text, key-name or cb24 binding "
                                                    "per key. No meaning was adjusted and no author code imported.")):
            S.set_status(st, rid, "executed", "notes/10-gaps.md", None, notes)
        S.save_status(st)
        review = build_review(st["rows"])
        json.dump(review, open(REVIEW_JSON, "w"), indent=1)
        cp = S.write_checkpoint(10, st, ["notes/10-gaps.md", "notes/01-source42-law-deltas.md", "notes/11-provider-trace-payload-law.md",
                                         "notes/12-source43-query-contract.md", "notes/13-source44-provider-wire.md", "blind-review.json", "tools/finalize_review.py",
                                         "tools/hc_source42.py", "tools/hc_source43.py", "tools/hc_source44.py", "runs/final-custody.json",
                                         "vectors/discovery-membership.json", "vectors/retention-negatives.json", "selfcheck/s42-prepost-matrix.json",
                                         "selfcheck/s42-provenance.json", "selfcheck/s43-provenance.json", "selfcheck/s44-provenance.json",
                                         "traces/payload-vectors.json", "traces/startup-vectors.json", "traces/abstract.json", "traces/controls.json",
                                         "vectors/graph-query.json", "preserved/s44-original/traces/"],
                                HC.all_entries() + HC43.all_entries() + HC44.all_entries(),
                                f"Phase 10 adjudicated in runtime source44.v1 on the source44 kit: verdict basis {json.dumps(review['verdictBasis'])}. " + HC44.CARRIED)
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
                                                                                or not basis["providerWireAndTraceLawExecutedWithoutFailure"]
                                                                                or not basis["graphQueryExecutedWithoutFailure"]
                                                                                or not basis["priorMeasurementReuseCustodyHolds"])
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
            ("R-NO-ACCEPT-IF-INCOMPLETE", gaps_consistent, "blind-review.json", "verdict is ACCEPT exactly when no gap, unexecuted accept-blocking ID, failed ID, failed positive, custody failure, failed negative, failed wire/trace law or unrefused control exists."),
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
