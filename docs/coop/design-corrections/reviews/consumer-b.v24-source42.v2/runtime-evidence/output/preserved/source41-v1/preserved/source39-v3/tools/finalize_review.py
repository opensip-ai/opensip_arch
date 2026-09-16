"""Phase 10/11 finalization from measured source39 standing.

python3 tools/finalize_review.py            -> records phase-10 standing, writes checkpoint 10 and blind-review.json
python3 tools/finalize_review.py --phase11  -> verifies blind-review.md/json against the charter rules, records phase-11 standing,
                                               writes checkpoint 11 and refreshes blind-review.json requirementStatus
The verdict is derived: ACCEPT-RECONSTRUCTABLE only with no MUST/SHOULD issue, no unexecuted accept-blocking ID, no failed ID and every
claimed complete positive admitted with replay and export; otherwise CHANGES_REQUIRED (BLOCKED is reserved for an unbuildable promised vector).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import hc_v2 as HC  # noqa: E402
import status as S  # noqa: E402

OUT = S.OUT
REVIEW_JSON = OUT + "blind-review.json"
REVIEW_MD = OUT + "blind-review.md"
STANDING = ("Additional self-audit of this origin's existing reconstruction against the unchanged normative source39 kit, begun in runtime consumer-b.v24-source39.v2 "
            "and completed in runtime consumer-b.v24-source39.v3 from its exact copied output (copied results are prior measured work, reused only as recorded in "
            "notes/12-v3-completion.md), "
            "continuing origin 9d3dfb70-b2d3-498c-a3c1-f8de9e488514; fresh-origin independence is not claimed anew, and this is not a new design kit, acceptance or a "
            "replacement for the source39.v1 finding s39-M1. The original consumer-b.v24 and source39.v1 results are preserved as immutable own history. This review "
            "reports its own executed admission, independent retained closure, replay and vectors; it makes no product qualification claim and grants no "
            "implementation authorization. External root admission of the exported bytes is a separate gate whose outcome is unobserved here. Real "
            "OS/compiler/crypto/SQLite measurement, native compiler/provider execution as enforcement proof, host authentication and synthetic TCB enforcement are "
            "future qualification: explicitly unperformed and not counted as design omissions.")


def issue(i, sev, title, selectors, measured, gap, choice):
    return {"id": i, "severity": sev, "title": title, "selectors": selectors, "measured": measured, "gap": gap, "reconstructionChoice": choice}


MUST = [
    issue("s39-M1", "MUST", "U-4b assigns no unitKind to a tsjs unit although UnitMembershipV1 is identity",
          ["docs/v2/contracts/product-v1/native-evidence.md lines 730-732 (U-4b: membershipDigest enters PlanId; every choice is identity, none left to an implementation)",
           "docs/v2/contracts/product-v1/native-evidence.md lines 744-748 (U-4b.2 tsjs unit: marker, mode, recognizerId, recognizerVersion; no unitKind)",
           "docs/v2/contracts/product-v1/native-evidence.md lines 739-740 and 854-855 (rust and fallback unitKind assigned)",
           "docs/v2/contracts/product-v1/native-evidence.md line 622; docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/$defs/WorkspaceUnitV2/properties/unitKind (enum ts-program|js-program, no mapping)",
           "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json membershipDigest -> analysis-spec parameter -> plan analysisSpecDigest"],
          ["vectors/discovery-membership.json#u4b-tsjs-unit-kind-not-assigned: one js-allowjs unit spelled js-program and ts-program; both schema-valid, both pass "
           "ENUMERATION_MEMBERSHIP_ORDER/_ROW_DERIVATION, membershipDigest 34d0e48f... vs 52a0e505..."],
          "Two conforming hosts mint different PlanIds for one repository (sharpest for a tsconfig with allowJs); the U-4b completeness claim does not hold for this field.",
          "cb24: ts-tsconfig -> ts-program; js-allowjs and js-synthesized -> js-program (ref/membership.py); alternative spelling measured beside it.")]
SHOULD = []
# source39.v2: disposition of the source39.v1 findings under the unchanged kit (v1's own prior-issue table is preserved in
# preserved/source39-v1/blind-review.json#/priorIssueDisposition and is not restated as current evidence).
PRIOR_V1 = [
    {"id": "s39-M1", "disposition": "carried unresolved - MUST, CHANGES_REQUIRED; no new normative owner was provided and no mapping is invented",
     "selector": "native-evidence.md lines 730-748, 739-740, 854-855, 622", "measured": "vectors/discovery-membership.json#u4b-tsjs-unit-kind-not-assigned re-executed, equal to v1 (34d0e48f... vs 52a0e505...)"},
    {"id": "A-c1", "disposition": "carried", "selector": "unchanged kit", "measured": "vectors/graph-query.json, envelopes/*"},
    {"id": "A-c2", "disposition": "carried", "selector": "native s10 lines 3285-3299", "measured": "vectors/d9-extension-precedence.json"},
    {"id": "A-c3", "disposition": "carried", "selector": "workflows s3 lines 440-449", "measured": "runs/cmp-code-det2"},
    {"id": "A-n1", "disposition": "carried", "selector": "workflows s3 lines 402-411", "measured": "vectors/baseline-e0-e3.json"},
    {"id": "A-n2", "disposition": "carried", "selector": "run-termination-contract lines 168-176", "measured": "vectors/run-termination.json"},
    {"id": "A-n3", "disposition": "carried", "selector": "run-termination-contract lines 84-85", "measured": "vectors/run-termination.json"},
    {"id": "A-n4", "disposition": "carried", "selector": "run-termination-contract lines 242-249", "measured": "vectors/run-termination.json"},
    {"id": "A-n5", "disposition": "carried", "selector": "native U-4b.2 lines 741-743", "measured": "not measured (Cargo rejects nested workspaces)"},
    {"id": "A-n6", "disposition": "carried", "selector": "native lines 165-166", "measured": "restatement note"},
    {"id": "source39.v1 27 claimed positives", "disposition": "helper defect found: exported without the subject3 descriptors composition s7 requires; v1 closure admitted them because output references were closed only by replay over the emitter's own subset (HC-33..HC-35)",
     "selector": "evaluator-composition-contract.v3.md s7 lines 72-76", "measured": "selfcheck/pre-summary.json; selfcheck/prepost-matrix.json"}]
PRIOR = [
    {"id": "M1", "disposition": "resolved", "selector": "identity bodyEligibilityLaw; execution-inputs s5; native lines 931-945",
     "measured": "ts-clones-required and syntax-mixed-omitted seal pass; rust-mixed-clones-required pass"},
    {"id": "M2", "disposition": "resolved", "selector": "identity-schemas.v3 program-predicate.nodeDigest -> policy-document.v2 Predicate",
     "measured": "runs/syntax-code~explicit-endpoint-source ADMIT"},
    {"id": "M3", "disposition": "resolved except the tsjs unitKind remainder (s39-M1)", "selector": "native U-4b lines 730-787",
     "measured": "runs/syntax-code~membership-reordered refuses ENUMERATION_MEMBERSHIP_ORDER:rows; vectors/discovery-membership.json"},
    {"id": "M4", "disposition": "resolved", "selector": "workflows lines 277-287; projection contract s11 line 192", "measured": "vectors/baseline-audit.json"},
    {"id": "M5", "disposition": "resolved", "selector": "workflows lines 1197-1239; command-envelope querySurface/queryResponse; inventory parityPaths",
     "measured": "vectors/graph-query.json#/measuredQueryResponseCarrier"},
    {"id": "S1", "disposition": "resolved", "selector": "identity lines 1303-1325; stage-spec outputSchemaDigest.registeredBy",
     "measured": "runs/syntax-code~stage-output-schema-relation-doc refuses STAGE_OUTPUT_SCHEMA_REGISTRATION_MISMATCH"},
    {"id": "S2", "disposition": "resolved", "selector": "identity lines 1065-1089; normalizationSpecificationLaw",
     "measured": "runs/syntax-code~clone-level-spec-not-in-grammar refuses BODY_NORMALIZATION_SPECIFICATION_NOT_IN_CLOSURE"},
    {"id": "S3", "disposition": "resolved", "selector": "native U-9 lines 851-877", "measured": "vectors/discovery-membership.json#u9-*; syntax Runs"},
    {"id": "S4", "disposition": "resolved", "selector": "execution-inputs s5; NativeCoverageAccountV1.targetUniverse type null",
     "measured": "logs/s39-original-closure.0.from_scratch.log (original refusal), corrected Runs admit"},
    {"id": "S5", "disposition": "resolved", "selector": "workflows lines 1056-1064; security line 1074", "measured": "vectors/test-prep-repair-authorization.json"},
    {"id": "S6", "disposition": "resolved", "selector": "command-inventory.v3 goldens", "measured": "envelopes/public-termination.json 45/45"},
    {"id": "S7", "disposition": "resolved", "selector": "workflows s3 lines 376-411; evaluator3 comparison-result IndeterminateReason, RuleCoverage, PivotPresence",
     "measured": "vectors/comparison-absence-knowledge.json"},
    {"id": "A1", "disposition": "resolved", "selector": "execution-inputs.schema.v1 / incoming-search.schema.v1 digest annotations", "measured": "runs/<run>.records.json"},
    {"id": "A2", "disposition": "resolved", "selector": "no identity-schemas.v2 owner names remain", "measured": "kit search"},
    {"id": "A3", "disposition": "resolved", "selector": "charter counts requirements; manifest 104 files", "measured": "runs/final-custody.json"},
    {"id": "A4", "disposition": "resolved", "selector": "identity lines 548-593; security lines 266-279", "measured": "runs/ts-pass read row; ts-pass~pruned-read-*"},
    {"id": "A5", "disposition": "resolved", "selector": "native lines 537-540", "measured": "HC-20"},
    {"id": "A6", "disposition": "resolved", "selector": "composition s4 single first-applicable correspondence cause", "measured": "replay of every positive"},
    {"id": "A7", "disposition": "resolved", "selector": "execution-inputs.schema.v1 CellProgramOutcomeV1.viewDigests description", "measured": "closure XI.admit"},
    {"id": "A8", "disposition": "partly carried (A-c1)", "selector": "query projectId row published in query-projection-contract s7", "measured": "vectors/graph-query.json"},
    {"id": "A9", "disposition": "resolved", "selector": "composition s5", "measured": "vectors/comparison-missing.json"},
    {"id": "A10", "disposition": "carried (A-c2)", "selector": "native s10 lines 3285-3299", "measured": "vectors/d9-extension-precedence.json"},
    {"id": "A11", "disposition": "resolved", "selector": "workflows lines 1070-1074", "measured": "-"},
    {"id": "A12", "disposition": "resolved", "selector": "evaluator3 comparison-result gateReason; workflows lines 460-463", "measured": "vectors/pivot-only-fingerprints.json"},
    {"id": "A13", "disposition": "resolved", "selector": "workflows lines 1130, 1207-1208, 1372; DELIVERY.REQUIRED_PROJECTION_FAILED", "measured": "envelopes/purge-replay-output-failure.json"},
    {"id": "A14", "disposition": "carried (A-c3)", "selector": "workflows s3 lines 440-449; line 508", "measured": "runs/cmp-code-det2"}]
ADVISORIES = [
    {"id": "A-c1", "title": "Unpublished internal refusal names still carried as cb24: syntax grammar-capability scope mismatch/undisclosed variants, E0 pivot joins, detector listing refusals, test consent relabel, native-preparation grant joins"},
    {"id": "A-c2", "title": "Inherited d9-exit-contract.v1.14 alone refuses the selected host-invariant termination; live successor-artifact obligation (native s10 lines 3285-3299)"},
    {"id": "A-c3", "title": "Exact-snapshot import correspondence changes import2 on every source change, so gating evidence rules attribute INDETERMINATE evidence-content-changed (workflows s3 lines 440-449)"},
    {"id": "A-n1", "title": "Closed per-entry IndeterminateReason order (workflows s3 lines 402-411): reason (3) detector disposition is unreachable for entries because an indeterminate detector leaves the changed-detector E0 presence null and (1) applies first (vectors/baseline-e0-e3.json)"},
    {"id": "A-n2", "title": "run-termination-contract s6 lines 168-176 vs s1 lines 34-35: errorCode/faultCause/signal can be read as UNKNOWN_FIELD (step 2) or NOT_DERIVED (step 3); both refuse"},
    {"id": "A-n3", "title": "run-termination-contract: non-object candidate has no published key; RUN_TERMINATION_UNEXPLAINED_INDETERMINATE_* is a wildcard (lines 84-85)"},
    {"id": "A-n4", "title": "run-termination-contract s7.3 lines 242-249: commit_inventory member set fixed 'as the reference commit path inventories them'; operational and excluded from Run identity"},
    {"id": "A-n5", "title": "native U-4b.2 lines 741-743: 'folded into the DEEPEST such workspace' is self-referential for a workspace below a workspace (Cargo rejects nested workspaces; unmeasured)"},
    {"id": "A-n6", "title": "native U-4b does not restate a rust unit's languageMode (rust-cargo vs rust-cargo-prepared), derivable from the mode table lines 165-166"},
    {"id": "A-v2-1", "title": "Composition s7 closes typed-prefix references of OUTPUTS; the kit does not state whether schema-declared typed-prefix values inside workflow-owned Plan input documents (WaiverSetV1 target.fingerprint finding-key2, PolicyDocumentV2 import addresses) are closure references. A literal all-owning-schemas reading makes lawful Runs unclosable (cmp-empty, cmp-budget: a fingerprint waiver with no occurrence; logs/v2-build.4.from_scratch.log). Deterministic reading adopted from s7 'these outputs', s5 waiver equality and identity s3 lines 597-600/627-631 (HC-36); one sentence in s7 would remove the ambiguity."},
    {"id": "A-v2-2", "title": "policy-derivation3 is a composition output (s7 line 70, s9.7) that no run3/seal3/evidence3/proof3 field references, so exact reachable output-set equality (s7 line 76) cannot include it and its retention is not required by the reachable-set law; exported stores retain it as an unreachable non-authoritative frame (runs/<run>.replay.fromscratch.json#/retainedClosure/unreachableRetained)."},
    {"id": "A-v2-3", "title": "identity-and-evidence.md s3 lines 441-467 call the four representations and four retention modes 'closed' and close derived to capabilityManifestId and owner-retained to owner-source-set[].ownerFileManifestSha256, while the retained native and relation bundles publish their own x-opensip-digest-law vocabularies: native-evidence.schemas.v2 has h-identity/derived (3 SourceUnitOwnershipV1 unitId positions), owner-retained (9 raw-artifact, 2 canonical-record), preimage-frame (31) and closure-tree-member (10); relation-payload-schemas.v2 adds representations snapshot-path and framed-body-identity with retentions snapshot-inventoried, provider-output-retained and not-joined (vectors/reference-census.json). Each bundle's own law is the deterministic owner for its positions (the identity sentence is scoped to identity-schemas.v3 fields), but a literal cross-bundle reading of 'closed to' would refuse lawful native and relation fields; one scoping sentence in s3 would remove it."}]
LIMITATIONS = [
    "run-termination s7.5 row 2 and s5 stage-terminal carriers are not exercised on built Runs (no provider-unavailable primary or retained stage terminal); vectors/run-termination.json#/notConstructedFromBuiltRuns",
    "docs/coop/design-corrections/discovery-defaults.py is a reference implementation the native U-4a text governs; its absence is not a custody gap",
    "Future qualification unperformed: real OS/compiler/crypto/SQLite, provider execution as enforcement, host authentication, synthetic TCB enforcement",
    "The independent retained-closure walker (ref/retained_graph.py) executes retention, identity, schema and registry joins, closure membership/kinds, selected-import membership (HC-37) and the SourceUnitOwnershipV1 unitId derivation (HC-38); owner-semantic admissions it names as delegated (languageVersionBinding derivation, clones framed-body-identity parse joins, native context/universe admission and binding - including the rust universe configProjectionSha256 join, which the domainSets registry does not list - enumeration and execution-input derivation) stay with owner graph admission, which runs as its own stage",
    "Census classes no constructed claimed-positive graph contains (canonical-record/owner-retained, raw-artifact/owner-retained, snapshot-path/not-joined) have no negative and are not claimed (vectors/retention-negatives.json#/censusPairsNotReachedByConstructedPositives)",
    "Negatives are closed in-process by the post-correction code and in fresh processes by the pre-correction code (preserved/pre-hc33)",
    "Results that do not run the retained-closure stage and were measured in runtime source39.v2 after the last change to the code they use (store builds, phases 1-4 and 6, discovery/prepared-mode vectors, phase8_compare, the pre-correction self-check) are reused from the exact copied output with mtime evidence; every closure-dependent result (replay-all, from-scratch, tamper, replay export, admission log, retention negatives, pre/post matrix, phases 5/7 vectors, phase 8 envelopes, graph query, run termination), provenance, custody, checkpoints 4-11 and this review were executed in source39.v3 after HC-37/HC-38 (notes/12-v3-completion.md)"]


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
    pm = json.load(open(OUT + "selfcheck/prepost-matrix.json"))
    walk_ok = all((r.get("retainedClosure") or {}).get("result") == "ADMIT" and (r.get("reachableOutputSet") or {}).get("equal")
                  for r in fs["runs"] if r["role"] == "claimed-positive")
    positives_ok = fs["allClaimedPositivesAdmitted"] and fs["allDesignedNegativesRefused"] and ex["allExportedAndEqual"] and \
        {r["run"] for r in ex["runs"]} == set(positives) and walk_ok
    custody_ok = cust["result"] == "PASS"
    if MUST or SHOULD or unexecuted or failed or not positives_ok or not custody_ok or not neg["allPass"]:
        verdict = "CHANGES_REQUIRED"
    else:
        verdict = "ACCEPT-RECONSTRUCTABLE"
    counts = {"requirements (R-*)": sum(1 for r in rows if r["id"].startswith("R-")),
              "standingRules (S-*)": sum(1 for r in rows if r["id"].startswith("S-")),
              "futureQualification (F-*)": sum(1 for r in rows if r["id"].startswith("F-")),
              "executed": sum(1 for r in rows if r["status"] == "executed"), "unexecuted": sum(1 for r in rows if r["status"] == "unexecuted"),
              "failed": len(failed), "claimedCompletePositives": len(positives)}
    return {"consumerId": S.CONSUMER, "runtime": "consumer-b.v24-source39.v3", "selfAuditBegunIn": "consumer-b.v24-source39.v2", "origin": "9d3dfb70-b2d3-498c-a3c1-f8de9e488514 (continuation; independence not claimed anew)",
            "verdict": verdict, "standing": STANDING,
            "verdictBasis": {"newMustIssues": len(MUST), "newShouldIssues": len(SHOULD), "unexecutedAcceptBlocking": unexecuted, "failed": failed,
                             "claimedCompletePositivesAllAdmittedReplayedExported": positives_ok,
                             "claimedCompletePositivesRetainedClosureAdmittedAndReachableSetEqual": walk_ok,
                             "retentionNegativesAllPass": neg["allPass"], "finalCustody": cust["result"],
                             "mustIssuesCarriedFromSource39V1": [m["id"] for m in MUST]},
            "kitCustody": cust, "newMustIssues": MUST, "newShouldIssues": SHOULD, "advisories": ADVISORIES,
            "priorIssueDisposition": PRIOR_V1,
            "priorHistory": {"source39.v1": "preserved/source39-v1/blind-review.json (verdict CHANGES_REQUIRED; its own prior-issue table)",
                             "consumer-b.v24": "preserved/consumer-b.v24-output.manifest.json (hash manifest only)",
                             "v1PriorIssueTableCarriedVerbatim": PRIOR},
            "selfAudit": {"preCorrectionSelfCheck": "selfcheck/pre-summary.json", "prePostMatrix": {k: v for k, v in pm.items() if k != "rows"},
                          "referenceCensus": "vectors/reference-census.json", "retainedClosureWalker": "ref/retained_graph.py",
                          "retentionNegatives": {"file": "vectors/retention-negatives.json", "constructed": neg["constructed"], "allPass": neg["allPass"],
                                                 "notConstructed": neg["notConstructed"],
                                                 "censusPairsNotReached": neg["censusPairsNotReachedByConstructedPositives"]},
                          "provenance": "selfcheck/v1-v2-provenance.json", "notes": ["notes/11-v2-self-audit.md", "notes/12-v3-completion.md"],
                          "v3Completion": {"copiedOutputManifest": "preserved/v2-copied-output.manifest.json", "portManifest": "port-manifest-v3.json",
                                           "reuseLedger": "notes/12-v3-completion.md"}},
            "limitations": LIMITATIONS,
            "claimedCompletePositives": [{"run": p, "runId": run_ids[p], "store": f"runs/{p}.store.json", "replay": f"runs/{p}.replay.json",
                                          "fromScratch": f"runs/{p}.replay.fromscratch.json", "replayExport": f"runs/{p}.replay-export.json",
                                          "recordLog": f"runs/{p}.records.json"} for p in positives],
            "fromScratchCommand": "cd /private/tmp/opensip-design-corrections/consumer-b.v24-source39.v3/output && /tmp/opensip-architecture-review-env/bin/python -I -B tools/from_scratch.py && "
                                  "/tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_export.py",
            "rootAdmission": "unobserved; exact exported object tables and blobs are exposed for root admission",
            "futureQualificationUnperformed": [r["id"] for r in rows if r["status"] == "futureQualification"],
            "helperCorrections": HC.all_entries(), "helperCorrectionsCarried": HC.CARRIED, "counts": counts,
            "requirementStatus": [{k: r[k] for k in ("id", "phase", "kind", "acceptBlocking", "status", "artifact", "firstRefusal", "notes")} for r in rows]}


def main():
    phase11 = "--phase11" in sys.argv
    st, rows = status_rows()
    if not phase11:
        for rid, notes in (("R-IDENTIFY-GAPS", f"{len(MUST)} MUST (s39-M1 carried unresolved), {len(SHOULD)} SHOULD, {len(ADVISORIES)} advisories (A-v2-1, A-v2-2 new) "
                                               f"with exact source39 selectors, and a disposition for every source39.v1 finding, after all acceptBlocking items "
                                               f"executed (source39.v2 measurements completed in source39.v3; notes/10-gaps.md, notes/11-v2-self-audit.md, "
                                               f"notes/12-v3-completion.md)."),
                           ("R-FREEDOM-VS-MISSING", "adjudication rules separate algorithm freedom from missing/contradictory contracts (notes/10-gaps.md#adjudication-rules)."),
                           ("R-BLOCKER-NOT-ADJUST", "CHANGES_REQUIRED with selectors; every promised vector built; cb24 choices named with measured alternatives; no meaning adjusted; "
                                                    "no author code imported.")):
            S.set_status(st, rid, "executed", "notes/10-gaps.md", None, notes)
        S.save_status(st)
        review = build_review(st["rows"])
        json.dump(review, open(REVIEW_JSON, "w"), indent=1)
        cp = S.write_checkpoint(10, st, ["notes/10-gaps.md", "notes/11-v2-self-audit.md", "notes/12-v3-completion.md", "blind-review.json", "tools/finalize_review.py",
                                         "runs/final-custody.json", "vectors/discovery-membership.json", "vectors/retention-negatives.json",
                                         "selfcheck/prepost-matrix.json", "selfcheck/pre-summary.json", "selfcheck/v1-v2-provenance.json"], HC.all_entries(),
                                f"Phase 10 adjudicated in runtime source39.v3 on the unchanged kit: verdict basis {json.dumps(review['verdictBasis'])}. " + HC.CARRIED)
        print(json.dumps({"verdict": review["verdict"], "basis": review["verdictBasis"], "checkpointUnexecuted": cp["requirementIdsUnexecuted"],
                          "checkpointFailed": cp["requirementIdsFailed"], "counts": review["counts"]}, indent=1))
        return 0
    review = json.load(open(REVIEW_JSON))
    md = open(REVIEW_MD).read() if os.path.exists(REVIEW_MD) else ""
    enum_ok = review["verdict"] in ("ACCEPT-RECONSTRUCTABLE", "CHANGES_REQUIRED", "BLOCKED")
    gaps_consistent = (review["verdict"] != "ACCEPT-RECONSTRUCTABLE") == bool(review["newMustIssues"] or review["newShouldIssues"] or review["verdictBasis"]["unexecutedAcceptBlocking"]
                                                                                or review["verdictBasis"]["failed"] or not review["verdictBasis"]["claimedCompletePositivesAllAdmittedReplayedExported"])
    md_ok = review["verdict"] in md and "no product qualification claim" in md.lower() and \
        all(i["id"] in md for i in review["newMustIssues"] + review["newShouldIssues"] + review["advisories"])
    shaped = isinstance(review["newMustIssues"], list) and isinstance(review["newShouldIssues"], list) and \
        all(i["selectors"] and i["measured"] for i in review["newMustIssues"] + review["newShouldIssues"]) and bool(review["advisories"])
    for rid, ok, art, notes in (
            ("R-DELIVER-MD-JSON", bool(md) and os.path.exists(REVIEW_JSON) and md_ok, "blind-review.md", "blind-review.md and blind-review.json with retained sources, runs and vectors."),
            ("R-VERDICT-ENUM", enum_ok, "blind-review.json", f"verdict {review['verdict']}; derived from issues and measured standing."),
            ("R-MUST-SHOULD-ADVISORY", shaped, "blind-review.json",
             f"newMustIssues ({len(review['newMustIssues'])}) and newShouldIssues ({len(review['newShouldIssues'])}) carry selectors and measurements; "
             f"{len(review['advisories'])} advisories reported separately."),
            ("R-NO-ACCEPT-IF-INCOMPLETE", gaps_consistent, "blind-review.json", "verdict is not ACCEPT while any gap, unexecuted accept-blocking ID or failed positive exists."),
            ("R-NO-QUALIFICATION-CLAIM", "no product qualification claim" in review["standing"].lower() and "no product qualification claim" in md.lower(), "blind-review.md",
             "standing text in both files.")):
        S.set_status(st, rid, "executed" if ok else "failed", art, None, notes)
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
