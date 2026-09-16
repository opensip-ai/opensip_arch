"""Phase 10/11 finalization from measured standing.

python3 tools/finalize_review.py            -> records phase-10 standing, writes checkpoint 10 and blind-review.json
python3 tools/finalize_review.py --phase11  -> verifies blind-review.md/json against the charter rules, records phase-11 standing,
                                               writes checkpoint 11 and refreshes blind-review.json requirementStatus
The verdict is derived: ACCEPT-RECONSTRUCTABLE only with no MUST/SHOULD issue, no unexecuted accept-blocking ID, no failed ID and every
claimed complete positive admitted with replay and export; otherwise CHANGES_REQUIRED (BLOCKED is reserved for an unbuildable promised vector).
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import status as S  # noqa: E402

OUT = S.OUT
REVIEW_JSON = OUT + "blind-review.json"
REVIEW_MD = OUT + "blind-review.md"
STANDING = ("Independent blind consumer reconstruction of the selected kit only. This review reports its own independently executed "
            "admission, closure, replay and vectors; it makes no product qualification claim and grants no implementation authorization. "
            "External root admission of the exported bytes is a separate gate whose outcome is unobserved here. Real OS/compiler/crypto/SQLite "
            "measurement, native compiler/provider execution as enforcement proof, host authentication and synthetic TCB enforcement are future "
            "qualification: explicitly unperformed and not counted as design omissions.")


def issue(i, sev, title, selectors, measured, gap, choice):
    return {"id": i, "severity": sev, "title": title, "selectors": selectors, "measured": measured, "gap": gap, "reconstructionChoice": choice}


MUST = [
    issue("M1", "MUST", "Required clones-fact census makes default TypeScript/syntax Runs permanently indeterminate while Rust passes the same shape",
          ["docs/v2/contracts/product-v1/native-evidence.md line 789 (default selection: every registered capability, required=true)",
           "foundation/enumeration-plan.schema.v1.json#/x-opensip-kind-derivation (clones-fact kinds [file]) and #/x-opensip-file-membership-extent-law/fileKind",
           "foundation/identity-schemas.v3.json#/x-opensip-digest-domains/scopeCapabilityLaw; native-evidence.md s1.2 grammar law",
           "native-evidence.md line 443 ('No syntax Run is made blanket-indeterminate')"],
          ["runs/ts-clones-required.replay.json (ADMIT, sealed indeterminate)", "runs/syntax-mixed-disclosed.replay.json, runs/syntax-mixed-omitted.replay.json (indeterminate)",
           "runs/syntax-mixed-falsecomplete.replay.json (REFUSE)", "runs/rust-mixed-clones-required.replay.json (ADMIT, pass)"],
          "No TypeScript unit and no syntax unit containing a non-code file can seal pass under the default profile; the census law differs by universe.",
          "Runs built both ways and reported; no attempt to redefine the census."),
    issue("M2", "MUST", "program-predicate.nodeDigest names the policy-1 Predicate schema for RuleProgramV2 nodes",
          ["foundation/identity-schemas.v3.json#/$defs/program-predicate/properties/nodeDigest/x-opensip-digest (record workflows/schemas/policy-document.schema.json#/$defs/Predicate, retention fragment)",
           "workflows/schemas/policy-document.v2.schema.json#/$defs/RuleProgramV2, #/$defs/Predicate"],
          ["runs/syntax-code~explicit-endpoint-source.replay.json (REFUSE DIGEST_FRAGMENT_RECORD_REFUSED:$.nodeDigest)", "runs/syntax-code.replay.json (ADMIT without the endpoint spelling)"],
          "Every Run whose program uses a v2-only atom field (endpoint, including incoming target atoms) is unclosable under the published digest law.",
          "Digest law implemented as published; the refusal is reported, not suppressed."),
    issue("M3", "MUST", "UnitMembershipV1 unit/row order and unitOrdinal assignment are unpublished but reach PlanId",
          ["native/native-evidence.schemas.v2.json#/$defs/UnitMembershipV1 (units, rows: x-opensip-order sequence)",
           "native-evidence.md lines 610-646 (U-1..U-4 membership without order); line 649 (U-4a cites docs/coop/design-corrections/discovery-defaults.py, absent from the 102-file kit)",
           "foundation/enumeration-plan.schema.v1.json membershipDigest -> analysis-spec parameter -> plan analysisSpecDigest"],
          ["runs/syntax-code~membership-reordered.replay.json (schema-valid; refused only by cb24.UNIT_MEMBERSHIP_DERIVATION)"],
          "Two conforming hosts mint different PlanIds for one repository.",
          "cb24: units by (rootPath UTF-8, languageFamily); rows by path UTF-8 (ref/membership.py)."),
    issue("M4", "MUST", "detectorId has no derivation but is identity-bearing in portable baselines and the exact E0 detector join",
          ["workflows/schemas/evaluator3/baseline-artifact.schema.json#/$defs/DetectorClosureEntry, #/$defs/BaselineEntry (detectorId beside contributionId, no description)",
           "workflows/schemas/evaluator3/comparison-result.schema.json#/$defs/Entry, #/$defs/DetectorDisposition",
           "workflows/workflow-projection-contract.v3.md s11 line 190 (exact {detectorId -> (closureId, semanticsMajor)} map)",
           "foundation/evaluator-emission-plan.schema.v1.json rules (no detectorId)"],
          ["vectors/baseline-audit.json#/cb24Choices", "vectors/baseline-e0-e3.json"],
          "A baseline minted by one conforming host has a different baselineId and fails the exact E0 join on another; Fresh-CI portability (workflows s2 lines 274-283) is undetermined.",
          "cb24: detectorId = emission contributionId."),
    issue("M5", "MUST", "Query parity field query-response has no carrier in the JSON parity reference CommandEnvelope major 3",
          ["docs/v2/contracts/product-v1/workflows-and-surfaces.md lines 1055-1060", "workflows/command-inventory.v3.json query parityFields and renderers[format=json].parityRule",
           "workflows/schemas/evaluator3/command-envelope.schema.json (additionalProperties false; query is the compact QueryResult)"],
          ["vectors/graph-query.json#/measuredQueryResponseCarrier (every probe refused)"],
          "A conforming JSON renderer cannot emit a required parity field without inventing an envelope field.",
          "cb24 carrier {envelope, queryResponse} for json/agent renderings.")]
SHOULD = [
    issue("S1", "SHOULD", "No closed registry of stage output schema documents",
          ["foundation/identity-schemas.v3.json#/$defs/stage-spec/properties/outputSchemaDigest; identity s3 'registered stage output schema document bytes'; #/x-opensip-payload-registry"],
          ["runs/syntax-code~stage-output-schema-relation-doc.replay.json (same planId, different executionPlanId, both ADMIT)"],
          "Hosts diverge on exec-plan2/proof3/seal3/run3 for one Plan.", "cb24: native-evidence.schemas.v2.json for native view stages."),
    issue("S2", "SHOULD", "Clone level-specification custody join is unnamed",
          ["native SyntaxGrammarBundleV1.normalizer.specificationDigest (singular)", "identity-and-evidence s3 frame levelVersion join"],
          ["runs/syntax-code~clone-level-spec-not-in-grammar.replay.json (refused only by cb24.CLONE_LEVEL_SPEC_NOT_IN_GRAMMAR_CLOSURE)"],
          "A literal reader admits a clone level specification outside the grammar closure.", "cb24 join to the admitted grammar closure tree."),
    issue("S3", "SHOULD", "Zero-config syntax-only unit and scope are not minted by any rule",
          ["enumeration-contract s1 ('one tsjs/rust/syntax-only unit per directory')", "native-evidence.md U-1 (markers only for tsjs/rust), line 178 (unitOrdinal null)"],
          ["runs/syntax-*.store.json (explicit analysis selection)"], "The default syntax-only path is undetermined.", "cb24: explicit selection, workspaceRoots ['.']."),
    issue("S4", "SHOULD", "NativeCoverageAccountV1.targetUniverse carried value is unstated",
          ["foundation/execution-inputs.schema.v1.json NativeCoverageAccountV1; execution-inputs contract s5"], ["ref/execinputs.py derive_accounts"],
          "Identity-bearing inside executionInputsDigest for cross-universe hosts.", "cb24: binding universe, one account per binding x matrix pair."),
    issue("S5", "SHOULD", "argvDigest recipe is unpublished",
          ["security/security-lifecycle.schemas.v1.json#/schemas/RepoExecutionGrantV2/properties/argvDigest", "security-and-lifecycle.md lines 1065, 1115, 1122",
           "workflows/schemas/test-execution.schema.json#/$defs/TestPayloadV1/properties/argvDigest"],
          ["vectors/test-prep-repair-authorization.json#/testExecution/argvDigestRecipe"], "Grant binding between components is not interoperable.", "cb24: raw SHA-256 of C(argv)."),
    issue("S6", "SHOULD", "Failure goldens without DomainDetail although kind=failure requires errors[]",
          ["workflows/command-inventory.v3.json goldens doctor-report-not-producible, query-latest-empty, envelope-major-unsupported",
           "workflows/schemas/evaluator3/command-envelope.schema.json allOf kind=failure", "workflows/query-projection-contract.v3.md s7 (empty latest -> QUERY.VIEW_UNKNOWN)"],
          ["envelopes/public-termination.json#/failureGoldensWithoutDetail"], "Three published goldens cannot form a lawful failure envelope; query-latest-empty disagrees with the query owner.",
          "Reported; no detail invented."),
    issue("S7", "SHOULD", "IndeterminateReason cannot express unknown absence without an evidence or pivot cause",
          ["workflows/schemas/evaluator3/comparison-result.schema.json#/$defs/IndeterminateReason", "workflows-and-surfaces.md lines 348-352"],
          ["tools/phase8_compare.py reasonApproximated"], "Forced mislabel of an INDETERMINATE entry.", "cb24: pivot-reevaluation-unavailable with reasonApproximated=true.")]
ADVISORIES = [
    {"id": "A1", "title": "Unannotated 64-hex fields in execution-inputs.schema.v1 (16) and incoming-search.schema.v1 (3); digest-law reach unstated"},
    {"id": "A2", "title": "enumeration-plan/subject-inventory annotations name identity-schemas.v2 while v3 is selected (byte-identical constraints)"},
    {"id": "A3", "title": "Charter prose '101 kit files' vs 102 hash-exact manifest files (runs/final-custody.json PASS)"},
    {"id": "A4", "title": "Pruned-tree bytes (node_modules/target) capture into snapshot inventory not decided in one place"},
    {"id": "A5", "title": "TypeScript universe jsAdmittedToProgram/jsDiagnosticsEnabled derivation unwritten"},
    {"id": "A6", "title": "finding.correspondence.reason singular while several conditions can co-occur"},
    {"id": "A7", "title": "CellProgramOutcomeV1.viewDigests observation-vs-derived standing"},
    {"id": "A8", "title": "Abbreviated or unnamed internal refusal keys (SYNTAX_CAPABILITY_*, detector listing, E0 joins, test consent relabel, preparation joins, query projectId mismatch) carried as cb24 names"},
    {"id": "A9", "title": "Rule outcome when a required evidenceUse kind is unavailable but the root is decided elsewhere"},
    {"id": "A10", "title": "Inherited d9-exit-contract.v1.14 alone refuses the selected host-invariant termination; kit records a live successorArtifactObligation (vectors/d9-extension-precedence.json)"},
    {"id": "A11", "title": "TestExecutionStepParams.effects enum lacks ENFORCED-PLATFORM:<primitive> admitted by its own description and security EnforcementV1"},
    {"id": "A12", "title": "gateReason has no member for CODE-NET-NEW hidden by a detector-semantics change"},
    {"id": "A13", "title": "Required-projection failure before commit has no registered DomainDetail for failure errors[]"},
    {"id": "A14", "title": "Exact-snapshot import correspondence makes gating evidence rules INDETERMINATE on any source change (kit-disclosed, workflows lines 1395-1405)"}]
EARLY_HELPER_CORRECTIONS = [
    "HC-1 syntax-code replay attempt1 (runs/syntax-code.replay.attempt1.json): missing source-inventory preimage and unregistered framed-body-identity representation; corrected from identity #/$defs/vcs-observation and relation-payload-schemas.v2 digest law.",
    "HC-2 vectors/phase4-tables.attempt1.json: wrong expectation for budget-exhausted without allowedCauses; corrected from native deficiency-cause registry.",
    "HC-3 rust first pass: inventory row order and derived h-identity retention; corrected from subject-inventory order law and identity retention/derived.",
    "HC-4 closure crash on unbound universe: guarded; internal errors reported as cb24.CLOSURE_INTERNAL_ERROR.",
    "HC-5 digest law did not descend into resolved records; transitive execution added (identity s3 closing law).",
    "HC-KEYNAMES vectors/unsupported-grammar.attempt1.json: helper-invented refusal names corrected to published keys, reconstructed names prefixed cb24."]


def status_rows():
    st = S.load_status()
    return st, st["rows"]


def collect_helper_corrections():
    out = list(EARLY_HELPER_CORRECTIONS)
    for p in sorted(glob.glob(OUT + "checkpoints/phase-*.json")):
        if ".attempt" in p:
            continue
        for h in json.load(open(p)).get("helperCorrections", []):
            if h not in out:
                out.append(h)
    return out


def build_review(rows):
    fs = json.load(open(OUT + "runs/from-scratch.summary.json"))
    ex = json.load(open(OUT + "runs/replay-export.summary.json"))
    cust = json.load(open(OUT + "runs/final-custody.json"))
    positives = [r["run"] for r in fs["runs"] if r["role"] == "claimed-positive"]
    run_ids = {p: json.load(open(OUT + f"runs/{p}.replay.fromscratch.json"))["runId"] for p in positives}
    unexecuted = [r["id"] for r in rows if r["status"] == "unexecuted" and r["acceptBlocking"]]
    failed = [r["id"] for r in rows if r["status"] == "failed"]
    positives_ok = fs["allClaimedPositivesAdmitted"] and ex["allExportedAndEqual"] and len(ex["runs"]) == len(positives)
    if MUST or SHOULD or unexecuted or failed or not positives_ok:
        verdict = "CHANGES_REQUIRED"
    else:
        verdict = "ACCEPT-RECONSTRUCTABLE"
    counts = {"requirements (R-*)": sum(1 for r in rows if r["id"].startswith("R-")),
              "standingRules (S-*)": sum(1 for r in rows if r["id"].startswith("S-")),
              "futureQualification (F-*)": sum(1 for r in rows if r["id"].startswith("F-")),
              "requirementsWithKindStandingRule": sum(1 for r in rows if r["kind"] == "standingRule"),
              "executed": sum(1 for r in rows if r["status"] == "executed"), "unexecuted": sum(1 for r in rows if r["status"] == "unexecuted"),
              "failed": len(failed)}
    return {"consumerId": S.CONSUMER, "verdict": verdict, "standing": STANDING,
            "verdictBasis": {"newMustIssues": len(MUST), "newShouldIssues": len(SHOULD), "unexecutedAcceptBlocking": unexecuted, "failed": failed,
                             "claimedCompletePositivesAllAdmittedReplayedExported": positives_ok},
            "kitCustody": cust, "newMustIssues": MUST, "newShouldIssues": SHOULD, "advisories": ADVISORIES,
            "claimedCompletePositives": [{"run": p, "runId": run_ids[p], "store": f"runs/{p}.store.json", "replay": f"runs/{p}.replay.json",
                                          "fromScratch": f"runs/{p}.replay.fromscratch.json", "replayExport": f"runs/{p}.replay-export.json",
                                          "recordLog": f"runs/{p}.records.json"} for p in positives],
            "fromScratchCommand": "cd /private/tmp/opensip-design-corrections/consumer-b.v24-source39.v1/output && /tmp/opensip-architecture-review-env/bin/python -I -B tools/from_scratch.py && "
                                  "/tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_export.py",
            "rootAdmission": "unobserved; exact exported object tables and blobs are exposed for root admission",
            "futureQualificationUnperformed": [r["id"] for r in rows if r["status"] == "futureQualification"],
            "helperCorrections": collect_helper_corrections(), "counts": counts,
            "requirementStatus": [{k: r[k] for k in ("id", "phase", "kind", "acceptBlocking", "status", "artifact", "firstRefusal", "notes")} for r in rows]}


def main():
    phase11 = "--phase11" in sys.argv
    st, rows = status_rows()
    if not phase11:
        for rid, notes in (("R-IDENTIFY-GAPS", "5 MUST, 7 SHOULD, 14 advisories with exact selectors after all acceptBlocking items executed (notes/10-gaps.md)."),
                           ("R-FREEDOM-VS-MISSING", "adjudication rules separate algorithm freedom from missing/contradictory contracts (notes/10-gaps.md#adjudication-rules)."),
                           ("R-BLOCKER-NOT-ADJUST", "CHANGES_REQUIRED with selectors; every promised vector built; cb24 choices named, no meaning adjusted, no author code imported.")):
            S.set_status(st, rid, "executed", "notes/10-gaps.md", None, notes)
        S.save_status(st)
        review = build_review(st["rows"])
        json.dump(review, open(REVIEW_JSON, "w"), indent=1)
        cp = S.write_checkpoint(10, st, ["notes/10-gaps.md", "blind-review.json", "tools/finalize_review.py", "runs/final-custody.json"], [],
                                f"Phase 10 adjudicated: verdict basis {json.dumps(review['verdictBasis'])}")
        print(json.dumps({"verdict": review["verdict"], "basis": review["verdictBasis"], "checkpointUnexecuted": cp["requirementIdsUnexecuted"],
                          "checkpointFailed": cp["requirementIdsFailed"], "counts": review["counts"]}, indent=1))
        return 0
    review = json.load(open(REVIEW_JSON))
    md = open(REVIEW_MD).read() if os.path.exists(REVIEW_MD) else ""
    enum_ok = review["verdict"] in ("ACCEPT-RECONSTRUCTABLE", "CHANGES_REQUIRED", "BLOCKED")
    gaps_consistent = (review["verdict"] != "ACCEPT-RECONSTRUCTABLE") == bool(review["newMustIssues"] or review["newShouldIssues"] or review["verdictBasis"]["unexecutedAcceptBlocking"]
                                                                                or review["verdictBasis"]["failed"])
    md_ok = review["verdict"] in md and "no product qualification claim" in md.lower() and all(i["id"] in md for i in review["newMustIssues"] + review["newShouldIssues"])
    for rid, ok, art, notes in (
            ("R-DELIVER-MD-JSON", bool(md) and os.path.exists(REVIEW_JSON) and md_ok, "blind-review.md", "blind-review.md and blind-review.json with retained sources, runs and vectors."),
            ("R-VERDICT-ENUM", enum_ok, "blind-review.json", f"verdict {review['verdict']}; derived from issues and measured standing."),
            ("R-MUST-SHOULD-ADVISORY", bool(review["newMustIssues"]) and bool(review["newShouldIssues"]) and bool(review["advisories"]), "blind-review.json",
             "newMustIssues/newShouldIssues nonempty with selectors; advisories separate."),
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
