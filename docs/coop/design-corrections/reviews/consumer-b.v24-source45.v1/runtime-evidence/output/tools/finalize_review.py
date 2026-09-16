"""Phase 10/11 finalization from measured source45 standing (runtime consumer-b.v24-source45.v1, continuing source44.v1, source43.v1 and source42.v1-.v3).

python3 tools/finalize_review.py            -> records phase-10 standing, writes checkpoint 10 and blind-review.json
python3 tools/finalize_review.py --phase11  -> verifies blind-review.md/json against the charter rules, records phase-11 standing,
                                               writes checkpoint 11 and refreshes blind-review.json requirementStatus
The verdict is derived. ACCEPT-RECONSTRUCTABLE requires all of the following:
  - no MUST or SHOULD issue, no unexecuted accept-blocking ID, no failed ID;
  - final custody PASS, all retention negatives passing, every closure control refused by the corrected code;
  - every claimed complete positive admitted by owner admission, the independent retained closure and replay with reachable-set equality, and
    exported;
  - the provider wire/trace law and the graph query executed without failure;
  - reuse custody holding, and the re-executed results agreeing with the source44 copy (run ids, retained replay results, classified byte differences);
  - the source44 arithmetic reconciliation passing.
Otherwise CHANGES_REQUIRED (BLOCKED is reserved for an unbuildable promised vector). The source44 bytes of this tool are preserved at
preserved/s44-final/tools/finalize_review.py.
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
import hc_source45 as HC45  # noqa: E402
import status as S  # noqa: E402

OUT = S.OUT
REVIEW_JSON = OUT + "blind-review.json"
REVIEW_MD = OUT + "blind-review.md"
S44 = json.load(open(OUT + "preserved/s44-final/blind-review.json"))
STANDING = ("Independent reconstruction of the source45 normative kit (manifest 70771536..., parent 8b4efbb0...) in runtime consumer-b.v24-source45.v1. It "
            "continues the same blind origin from the exact source44.v1 output, whose final bytes are preserved at preserved/s44-final/. Against my own "
            "source44 custody rows, three kit members changed and none were added or removed: native-evidence.md, native/provider-startup.schemas.v1.json "
            "and foundation/provider-target-attribution-return.schema.v2.json. They publish the pre-Analyze host-conversion closedWorld (my source44 "
            "M-s44-1) and state the return law's historical payload per language (my source44 A-s44-1). An AST read-census finds that only the "
            "provider-trace reconstruction reads them (selfcheck/s45-provenance.json). The source44 phase-3 helpers were executed first on the source45 "
            "kit, unchanged apart from the runtime root (preserved/s45-original/). They did not detect the new law and were corrected from the kit "
            "(HC-60). Executed fresh on the source45 runtime: the from-scratch closure and complete proof replay of every claimed positive, export replay, "
            "admission log, graph query, reference census and retention negatives. Every other measurement is reused as an exact prior measurement with "
            "custody. The source44 result-comparison arithmetic is reconciled from retained files (selfcheck/s45-s44-arithmetic-reconciliation.json). "
            "Source44 history: " + S44["standing"])

MUST = []
SHOULD = []
PHASE11_IDS = ("R-DELIVER-MD-JSON", "R-VERDICT-ENUM", "R-MUST-SHOULD-ADVISORY", "R-NO-ACCEPT-IF-INCOMPLETE", "R-NO-QUALIFICATION-CLAIM")


def cb24_keys():
    keys = set()
    for p in sorted(glob.glob(OUT + "ref/*.py")):
        keys |= set(re.findall(r'["(]cb24\.([A-Za-z][A-Za-z0-9_.-]*)', open(p).read()))
    return sorted(keys)


PRIOR = S44["priorIssueDisposition"] + [
    {"id": "own source44.v1 MUST M-s44-1: the pre-Analyze host conversion leaves the committed closedWorld undetermined",
     "disposition": ("resolved by the source45 bytes. native-evidence s9.7 now publishes one complete closedWorld for both languages, and "
                     "provider-startup#/x-opensip-startup-law/preAnalyzeUnavailable/hostConversionClosedWorld publishes the same value machine-readably, "
                     "referenced by hostConversion: exportsClosed unknown, entryPointsRecognized none, nonliteralLoading none, externalConsumers unknown, "
                     "dynamicDispatch not-applicable, reasons ['no-manifest'], deadCodeRepairEligible false. It keeps every member my source44 reading found "
                     "determined, and it equals none of my four source44 candidates (A differs only in reasons). The helper is corrected (HC-60)."),
     "selector": ("native-evidence.md s9.7 lines 3241-3261; native/provider-startup.schemas.v1.json#/x-opensip-startup-law/preAnalyzeUnavailable/hostConversion "
                  "(line 58) and hostConversionClosedWorld (lines 59-69)"),
     "measured": ("traces/startup-vectors.json#/conversion (both owners agree; the value admits ClosedWorldV2; conversion faults [] with stable coverage2 identities "
                  "in both languages; every source44 candidate refuses cb24.CONVERSION_CLOSED_WORLD_NOT_PUBLISHED); logs/s45-p3.1; unchanged helper logs/s45-original.1/.2")},
    {"id": "own source44.v1 advisory A-s44-1: return-law summary sentences named historical FactBatchV2 for any token-absent worker",
     "disposition": ("resolved by the source45 bytes. The standing (line 65), boundary.compilerWorkerTransport (line 67) and missingAndIncomplete.missingToken "
                     "(line 117) now name delivery.v2 FactBatchV1 for typescript-semantic and rust-provider-protocol.v2 FactBatchV2 for rust-semantic. An "
                     "editorial duplication remains at line 117 (A-s45-1)."),
     "selector": "foundation/provider-target-attribution-return.schema.v2.json#/x-opensip-return-law/standing, boundary/compilerWorkerTransport, missingAndIncomplete/missingToken",
     "measured": "traces/payload-vectors.json re-executed on the source45 bytes (logs/s45-p3.0, 78 vectors, 0 failures; key bindings still resolve)"},
    {"id": "own source44.v1 report: 'Result bytes against the source43 copy: 251 of 473 retained result files are byte-identical' (blind-review.md; also notes/13)",
     "disposition": ("own reporting error, corrected from retained files. 251 is the identical count within the 347-file determinism-probe subset (runs/, "
                     "negatives/, vectors/ non-store files), not within the 473-file manifest. Correct: 370 of 473 identical and 103 differing (89 "
                     "process-id-bearing, 10 expected content, 4 helper sources edited in source44). Within the 347-file subset, 251 are identical and 96 "
                     "differ (89 differ between two source44 executions; 7 are stable but differ from source43); the other 7 differing files are the "
                     "phase-3 traces outside that subset. The source44 report bytes are preserved unchanged."),
     "selector": "preserved/s44-final/blind-review.md ('Result bytes against the source43 copy'); preserved/s44-final/notes/13-source44-provider-wire.md",
     "measured": "selfcheck/s45-s44-arithmetic-reconciliation.json (every check true; current copied bytes also give 370 identical and 103 differing)"}]


def advisories():
    prior = [a for a in S44["advisories"] if a["id"] != "A-s44-1"]
    for a in prior:
        if a["id"] == "A-c1":
            keys = cb24_keys()
            a["measured"] = f"{len(keys)} distinct cb24.* keys emitted by ref/*.py: {keys}"
        if a["id"] == "A-c2":
            a["selectors"] = ["native-evidence.md lines 3584-3619 (source44: 3565-3600; +19 after the source45 s9.7 insertion)"]
        if a["id"] == "A-s44-2":
            a["selectors"] = [s.replace("(line 4069)", "(line 4088; source44: 4069)") for s in a["selectors"]]
    return prior + [
        {"id": "A-s45-1", "title": ("Editorial: the return law's missingAndIncomplete.missingToken begins 'Historical the historical per-language payload (...)'; "
                                    "the duplicated word does not change the per-language rule it states"),
         "selectors": ["foundation/provider-target-attribution-return.schema.v2.json#/x-opensip-return-law/missingAndIncomplete/missingToken (line 117)"],
         "measured": "read in the source45 bytes; no helper reads this sentence (traces/payload-vectors.json key bindings cite invocation/inputs selectors)"}]


LIMITATIONS = [l for l in S44["limitations"] if not l.startswith(("Provider wire and trace law (source42.v3", "Reuse in source44"))] + [
    ("Provider wire and trace law (source42.v3 HC-53; source44 HC-57, HC-58; source45 HC-60). Executed on constructed payloads joined to my retained "
     "ts-pass/rust-mixed Run values, in the payload-carrying traces, traces/payload-vectors.json and traces/startup-vectors.json:"
     " negotiated FactBatchV3 or the language's historical payload; exact deterministic-CBOR bytes; the TypeScript batchCommitment; "
     "DispatchBindingV1 correlation; companions; handshake/startup/coverage/terminal/cancellation payloads; and the pre-Analyze host conversion with the "
     "published closedWorld. Not executed: snapshot, dependency-source and prepared custody payloads (abstract events, as in the kit's s9.7 reference "
     "scope); coverage/stream commitment recomputation; descriptor signatures (synthetic trusted descriptors and rust-v1 row); Rust CancelledV2 "
     "observedPhase vocabulary; post-terminal bind_worker_occupancy; anchor admission of constructed candidates. The fixture Plan, the synthetic "
     "prepared-output set and the placeholder commitments are host inputs, not a verified Plan or Run. No actual worker-process enforcement is claimed."),
    ("Reuse in source45 (selfcheck/s45-provenance.json). Executed fresh: phase 3, closure/replay/export/admission log, graph query, census and negatives. "
     "Every other measurement is an exact prior measurement, reused because no helper outside phase 3 reads a changed kit member, no unchanged kit "
     "document references a changed $id, helper bytes are rebound-only and stores are byte-identical. It was not re-executed in source45. The "
     "process-id nondeterminism of replay outputs is the source44 two-execution measurement, reused."),
    ("Kit-delta localization. My custody keeps member hashes, not the bytes of earlier kits. The changes inside the three members were therefore located "
     "by content and section structure: native-evidence.md sections before s9.7 keep their line positions and every later heading moved by +19, which "
     "matches the new s9.7 closedWorld block. Every selector my helpers and issues cite was re-read in the source45 bytes. A same-length wording change "
     "elsewhere in these members that no helper reads and no issue cites would not have been located.")]


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
    conv = ts["conversion"]
    conversion_ok = conv["ownersAgree"] and conv["publishedAdmitsClosedWorldV2"] and all(conv["determinacyResolution"]["measured"].values())
    trace_payload_ok = (tc["assertionFailures"] == [] and tv["assertionFailures"] == [] and ts["assertionFailures"] == [] and tc["factBatchPayloads"]["validated"] > 0
                        and all(v > 0 for v in tc["factBatchPayloads"]["admittedBySelectedPayload"].values())
                        and all(m["rowsNotExercised"] == [] and m["pairwiseDisjointOverlaps"] == [] for m in machines.values())
                        and all(t["matchesExpected"] for t in ta["tests"]) and conversion_ok)
    orig = {name: json.load(open(OUT + f"preserved/s45-original/traces/{name}.json")) for name in ("controls", "payload-vectors", "startup-vectors")}
    payload_law = {"machines": machines, "traceFactBatchPayloads": tc["factBatchPayloads"], "payloadAdmissions": tc["payloadAdmissions"],
                   "abstractTableTests": [{k: t[k] for k in ("name", "provider", "matchesExpected", "law")} for t in ta["tests"]],
                   "payloadVectors": {"vectors": len(tv["vectors"]), "groups": tv["groups"], "decoderVectors": len(tv["decoderVectors"]),
                                      "encoderVectors": len(tv["encoderVectors"]), "violationKeysExercised": tv["violationKeysExercised"],
                                      "hc51": {k: tv["hc51"][k] for k in ("correctedSchemaAdmitted", "unchangedKitRefusedOrderAnnotationUnknown", "tokenCensus")},
                                      "kitVectorCrossCheck": tv["kitVectorCrossCheck"]},
                   "startupVectors": {"vectors": len(ts["vectors"]), "groups": ts["groups"], "faultKeysExercised": ts["faultKeysExercised"],
                                      "wireControls": ts["wireControls"], "wireCbor": ts["wireCbor"],
                                      "conversion": {k: conv[k] for k in ("publishedClosedWorld", "ownersAgree", "publishedAdmitsClosedWorldV2", "determinacyResolution")}},
                   "unchangedSource44HelpersOnSource45Kit": {
                       "tracesAssertionFailures": orig["controls"]["assertionFailures"], "payloadVectorsAssertionFailures": orig["payload-vectors"]["assertionFailures"],
                       "startupVectorsAssertionFailures": orig["startup-vectors"]["assertionFailures"],
                       "startupVectorsStillReportedDeterminacyGap": orig["startup-vectors"]["conversion"].get("determinacyGap", {}).get("measured"),
                       "logs": ["logs/s45-original.0.run_unchanged_s44.log", "logs/s45-original.1.run_unchanged_s44.log", "logs/s45-original.2.run_unchanged_s44.log"]},
                   "assertionFailures": tc["assertionFailures"] + tv["assertionFailures"] + ts["assertionFailures"]}
    gq = json.load(open(OUT + "vectors/graph-query.json"))
    prov = json.load(open(OUT + "selfcheck/s45-provenance.json"))
    rd = json.load(open(OUT + "selfcheck/s45-result-diffs.json"))
    arith = json.load(open(OUT + "selfcheck/s45-s44-arithmetic-reconciliation.json"))
    ra = gq["source43ReAudit"]
    query_ok = gq["assertionFailures"] == [] and all(p["differs"] == (p["expected"] == "differ") for p in ra["prePost"])
    reuse_ok = prov["reusePreconditionsHold"] and fs.get("everyResultMatchesOriginal") is True and rd["result"] == "PASS"
    arith_ok = arith["result"] == "PASS"
    if MUST or SHOULD or unexecuted or failed or not positives_ok or not custody_ok or not neg["allPass"] or not controls_ok or not trace_payload_ok \
            or not query_ok or not reuse_ok or not arith_ok:
        verdict = "CHANGES_REQUIRED"
    else:
        verdict = "ACCEPT-RECONSTRUCTABLE"
    counts = {"requirements (R-*)": sum(1 for r in rows if r["id"].startswith("R-")),
              "standingRules (S-*)": sum(1 for r in rows if r["id"].startswith("S-")),
              "futureQualification (F-*)": sum(1 for r in rows if r["id"].startswith("F-")),
              "executed": sum(1 for r in rows if r["status"] == "executed"), "unexecuted": sum(1 for r in rows if r["status"] == "unexecuted"),
              "failed": len(failed), "claimedCompletePositives": len(positives)}
    return {"consumerId": S.CONSUMER, "runtime": "consumer-b.v24-source45.v1",
            "copiedFromRuntime": "consumer-b.v24-source44.v1 (continued from consumer-b.v24-source43.v1 and source42.v3, .v2, .v1)",
            "origin": "9d3dfb70-b2d3-498c-a3c1-f8de9e488514 (continuation; independence not claimed anew)",
            "kit": {"consumerInputManifestSha256": cust["manifestSha256"], "parentSubjectSha256": cust["parentSubjectSha256"]},
            "verdict": verdict, "standing": STANDING,
            "verdictBasis": {"newMustIssues": len(MUST), "newShouldIssues": len(SHOULD), "unexecutedAcceptBlocking": unexecuted, "failed": failed,
                             "claimedCompletePositivesAllAdmittedReplayedExported": positives_ok,
                             "claimedCompletePositivesRetainedClosureAdmittedAndReachableSetEqual": walk_ok,
                             "retentionNegativesAllPass": neg["allPass"], "finalCustody": cust["result"],
                             "closureControlsRefusedByCorrectedCode": controls_ok,
                             "providerWireAndTraceLawExecutedWithoutFailure": trace_payload_ok,
                             "hostConversionClosedWorldPublishedAndApplied": conversion_ok,
                             "graphQueryExecutedWithoutFailure": query_ok,
                             "priorMeasurementReuseCustodyHolds": reuse_ok,
                             "source44ArithmeticReconciled": arith_ok,
                             "ownSource41ExportDefectCorrected": "HC-47", "ownSource42v2TraceOmissionCorrected": "HC-53",
                             "ownSource42v3QueryOmissionCorrected": "HC-54", "ownSource43TraceReadingsSupersededBySource44Owners": "HC-57, HC-58",
                             "ownSource44ConversionReadingSupersededBySource45Owners": "HC-60"},
            "kitCustody": cust, "newMustIssues": MUST, "newShouldIssues": SHOULD, "advisories": advisories(),
            "priorIssueDisposition": PRIOR,
            "source45Continuation": {
                "kitDelta": prov["kitDelta"], "memberReaders": prov["memberReaders"], "nonPhase3Readers": prov["nonPhase3Readers"],
                "genericKitReaders": prov["genericKitReaders"], "changedIdsReferencedByUnchangedKitDocuments": prov["changedIdsReferencedByUnchangedKitDocuments"],
                "rebind": "rebind-s45-manifest.json (113 files, 132 occurrences; HC-59)", "source44FinalBytes": "preserved/s44-final/manifest.json",
                "source44ResultHashes": "preserved/s44-final/results-manifest.json", "provenance": "selfcheck/s45-provenance.json",
                "storesByteIdenticalToSource44": not prov["storeByteDifferences"],
                "resultByteDifferencesFromSource44": {k: v for k, v in rd.items() if k != "rows"}, "resultByteDifferenceRows": "selfcheck/s45-result-diffs.json#/rows",
                "source44ArithmeticReconciliation": {k: arith[k] for k in ("reconciliation", "differingOutsideDeterminismSubset", "currentCopiedBytes", "result")},
                "providerWireAndTraceLaw": payload_law, "executedFresh": prov["freshInSource45"], "reusedExactPriorMeasurements": prov["reusedExactPriorMeasurements"],
                "supersededInSource45": prov["supersededInSource45"], "notes": "notes/14-source45-closed-world.md"},
            "source44Continuation": {"review": "preserved/s44-final/blind-review.json", "reviewMarkdown": "preserved/s44-final/blind-review.md",
                                     "provenance": "selfcheck/s44-provenance.json (written in runtime source44.v1)"},
            "priorHistory": {"source44.v1": "preserved/s44-final/blind-review.json (CHANGES_REQUIRED on the source44 kit: M-s44-1; resolved by the source45 bytes)",
                             "source43.v1": "preserved/s43-final/blind-review.json (ACCEPT-RECONSTRUCTABLE on the source43 kit; R-TRACE-* superseded under source44 by HC-57/HC-58)",
                             "source42.v3": "ACCEPT-RECONSTRUCTABLE on the source42 kit; R-GRAPH-QUERY standing superseded by HC-54 (preserved/s42-v3-final/)",
                             "source42.v2": "ACCEPT-RECONSTRUCTABLE; R-TRACE-* standing rested on transition-only traces; superseded by HC-53 (preserved/s42-v2-final/)",
                             "source42.v1": "incomplete pass, no review",
                             "source41.v1": "preserved/source41-v1/blind-review.json (ACCEPT-RECONSTRUCTABLE on the source41 kit; superseded by HC-47)",
                             "source39.v3 and earlier": "preserved/source41-v1/preserved/ (copied non-store history and hash manifests)"},
            "limitations": LIMITATIONS,
            "claimedCompletePositives": [{"run": p, "runId": run_ids[p], "store": f"runs/{p}.store.json", "replay": f"runs/{p}.replay.json",
                                          "fromScratch": f"runs/{p}.replay.fromscratch.json", "replayExport": f"runs/{p}.replay-export.json",
                                          "recordLog": f"runs/{p}.records.json"} for p in positives],
            "fromScratchCommand": ("cd /private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/output && for s in tools/from_scratch.py tools/replay_export.py "
                                   "tools/phase9_admission_log.py vectors/phase3_payload_vectors.py vectors/phase3_startup_vectors.py vectors/phase3_traces.py; do "
                                   "/tmp/opensip-architecture-review-env/bin/python -I -B $s || exit 1; done"),
            "rootAdmission": "unobserved; exact exported object tables and blobs are exposed for root admission",
            "futureQualificationUnperformed": [r["id"] for r in rows if r["status"] == "futureQualification"],
            "helperCorrections": HC.all_entries() + HC43.all_entries() + HC44.all_entries() + HC45.all_entries(), "helperCorrectionsCarried": HC45.CARRIED,
            "counts": counts,
            "requirementStatus": [{k: r[k] for k in ("id", "phase", "kind", "acceptBlocking", "status", "artifact", "firstRefusal", "notes")} for r in rows]}


def main():
    phase11 = "--phase11" in sys.argv
    st, rows = status_rows()
    if not phase11:
        adv = advisories()
        for rid, notes in (("R-IDENTIFY-GAPS", f"{len(MUST)} MUST, {len(SHOULD)} SHOULD and {len(adv)} advisories with exact selectors, after every acceptBlocking item "
                                               f"executed. Source44 M-s44-1 and A-s44-1 are resolved by the source45 bytes, with measured dispositions. New advisory: "
                                               f"A-s45-1 (editorial duplication at return-law line 117). Carried advisory selectors were re-located in the "
                                               f"source45 bytes. The empty MUST/SHOULD arrays are justified in notes/10-gaps.md and notes/14-source45-closed-world.md."),
                           ("R-FREEDOM-VS-MISSING", "adjudication rules separate algorithm freedom from missing or contradictory contracts (notes/10-gaps.md#adjudication-rules). "
                                                    "The conversion closedWorld, a missing contract in source44, is now published, so no choice remains."),
                           ("R-BLOCKER-NOT-ADJUST", "Every promised vector was built. The host conversion now applies the published closedWorld, and my source44 "
                                                    "candidates are kept as refused controls, not adjusted. cb24 names are declared reconstruction keys. Readings "
                                                    "adopted where text is ambiguous are named with measured alternatives (A-s42-1, A-s42-2, A-s41-1, A-s41-2, "
                                                    "A-v2-1, A-s43-1). No meaning was adjusted and no author code imported.")):
            S.set_status(st, rid, "executed", "notes/10-gaps.md", None, notes)
        S.save_status(st)
        review = build_review(st["rows"])
        json.dump(review, open(REVIEW_JSON, "w"), indent=1)
        cp = S.write_checkpoint(10, st, ["notes/10-gaps.md", "notes/13-source44-provider-wire.md", "notes/14-source45-closed-world.md", "blind-review.json",
                                         "tools/finalize_review.py", "tools/hc_source42.py", "tools/hc_source43.py", "tools/hc_source44.py", "tools/hc_source45.py",
                                         "runs/final-custody.json", "vectors/retention-negatives.json", "selfcheck/s42-prepost-matrix.json",
                                         "selfcheck/s44-provenance.json", "selfcheck/s45-provenance.json", "selfcheck/s45-result-diffs.json",
                                         "selfcheck/s45-s44-arithmetic-reconciliation.json", "traces/payload-vectors.json", "traces/startup-vectors.json",
                                         "traces/abstract.json", "traces/controls.json", "vectors/graph-query.json", "preserved/s45-original/traces/",
                                         "preserved/s44-final/manifest.json"],
                                HC.all_entries() + HC43.all_entries() + HC44.all_entries() + HC45.all_entries(),
                                f"Phase 10 adjudicated in runtime source45.v1 on the source45 kit: verdict basis {json.dumps(review['verdictBasis'])}. " + HC45.CARRIED)
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
                                                                                or not basis["priorMeasurementReuseCustodyHolds"]
                                                                                or not basis["source44ArithmeticReconciled"])
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
            ("R-NO-ACCEPT-IF-INCOMPLETE", gaps_consistent, "blind-review.json", "verdict is ACCEPT exactly when no gap, unexecuted accept-blocking ID, failed ID, failed positive, custody failure, failed negative, failed wire/trace law, failed reuse custody, unreconciled arithmetic or unrefused control exists."),
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
