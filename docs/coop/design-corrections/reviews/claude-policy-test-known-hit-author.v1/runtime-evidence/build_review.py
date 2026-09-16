"""Assemble review.json for the policy-test known-hit / universe-token correction from actual custody, delta manifest,
receipts and probe outputs. Recomputable claims are recomputed; the builder refuses (exit 1) when one does not hold."""
import hashlib
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parent
load = lambda p: json.loads((R / p).read_text())
fsha = lambda p: hashlib.sha256((R / p).read_bytes()).hexdigest()
failures = []


def require(cid, ok, detail=None):
    if not ok:
        failures.append({"id": cid, "detail": detail})


def receipt(label):
    d = R / "receipts" / label
    return {"label": label, "argv": json.loads((d / "command.json").read_text())["argv"], "cwd": json.loads((d / "command.json").read_text())["cwd"],
            "exit": int((d / "exit.txt").read_text()), **json.loads((d / "digests.json").read_text())}


def stdout_json(label):
    return json.loads((R / "receipts" / label / "stdout.txt").read_text())


F39 = "f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009"
capture, recheck, delta = load("custody/frozen39-capture.json"), load("custody/end-of-work-recheck.json"), load("custody/delta-manifest.json")
require("capture-verified", capture["manifestSha256"] == F39 and capture["memberCount"] == 12909 and not capture["verifyBefore"]["faults"]
        and not capture["verifyAfter"]["faults"] and not capture["copyFaults"] and not capture["verifyBefore"]["unlisted"])
require("frozen39-and-counterexample-unaltered-at-end", recheck["manifestSha256"] == F39 and not recheck["mismatch"] and not recheck["unlisted"]
        and recheck["originalProbeMatchesRecorded"] and recheck["adaptedProbeMatchesRecorded"])
ALLOWED = {"docs/coop/design-corrections/workflows/policy_test_model.v3.py", "docs/coop/design-corrections/workflows/workflows_model.v3.py",
           "docs/coop/design-corrections/workflows/policy-test-cases.v3.json", "docs/coop/design-corrections/workflows/schemas/evaluator3/policy-test.schema.json",
           "docs/coop/design-corrections/workflows/check-workflow-projection.v3.py", "docs/v2/contracts/product-v1/workflows-and-surfaces.md"}
changes = {c["path"]: c["status"] for c in delta["changes"]}
require("delta-is-exactly-the-six-modified-owners", set(changes) == ALLOWED and set(changes.values()) == {"modified"} and delta["pycacheDirectories"] == [], changes)
HISTORICAL = ["docs/coop/design-corrections/workflows/workflows_model.v1.py", "docs/coop/design-corrections/workflows/schemas/policy-test.schema.json",
              "docs/coop/design-corrections/workflows/workflow-cases.v1.json", "docs/coop/design-corrections/workflows/check_workflows.v1.py",
              "docs/coop/design-corrections/foundation/evaluator_composition_model.v3.py", "docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md",
              "docs/coop/design-corrections/foundation/identity-schemas.v3.json", "docs/coop/design-corrections/foundation/atom_model.v1.py",
              "docs/coop/design-corrections/public-detail-registry.v1.json"]
require("historical-and-shared-owners-byte-identical", not any(p in changes for p in HISTORICAL))

# reproduction and correction
pre_orig, post_orig = stdout_json("pre-correction-original-probe"), stdout_json("post-correction-original-probe.2")
require("original-probe-failure-reproduced", pre_orig["total"] == 50 and pre_orig["failed"] == [["P1", "known-native-hit-under-missing-required-evidence-agrees-with-composition"]])
require("original-probe-passes-after-correction", post_orig["total"] == 50 and post_orig["failed"] == [])
pre1, pre2 = load("probes/output/pre-correction-known-hit-universe.json"), load("probes/output/pre-correction-known-hit-universe.v2.json")
post = load("probes/output/post-correction-known-hit-universe.final.json")
require("comparison-probe-pre-correction-v2-discriminates", len(pre2["rows"]) == 37 and len(pre2["lawFailures"]) == 16)
require("comparison-probe-post-correction-clean", len(post["rows"]) == 37 and post["lawFailures"] == [])
k_post = [r for r in post["rows"] if r["group"] == "K"]
require("all-composition-comparisons-agree", len(k_post) == 22 and all(r["observed"]["agree"] and all(r["observed"]["agree"].values()) for r in k_post))

# checks
wp_base, wp_fail, wp_post = stdout_json("baseline-check-workflow-projection-v3"), stdout_json("post-correction-check-workflow-projection-v3"), stdout_json("post-correction-check-workflow-projection-v3.2")
ia, ib = {r["id"]: r["ok"] for r in wp_base["results"]}, {r["id"]: r["ok"] for r in wp_post["results"]}
added = sorted(set(ib) - set(ia))
require("workflow-projection-baseline-passed", wp_base["passed"] and wp_base["count"] == 838)
require("workflow-projection-first-post-run-retained-failure", not wp_fail["passed"] and [f["id"] for f in wp_fail["failed"]] == ["pt2-admitted-current-suite-reaches-the-authored-outcomes"])
require("workflow-projection-final-passed-no-removed-or-flipped", wp_post["passed"] and wp_post["count"] == 852 and set(ia) <= set(ib)
        and all(ib[k] == v for k, v in ia.items()) and len(added) == 14 and all(a.startswith("pt2-") for a in added))
comp_base, comp_post = stdout_json("baseline-check-composition-v3"), stdout_json("post-correction-check-composition-v3")
require("composition-checker-passed-before-and-after", comp_base["passed"] and comp_post["passed"] and comp_base["count"] == comp_post["count"] == 30)
q_base, q_post = load("work/baseline-checks/query-projection-report.json"), load("work/post-correction-checks/query-projection-report.json")
require("query-checker-passed-before-and-after", q_base["passed"] and q_post["passed"] and q_base["count"] == q_post["count"] == 204)
v1_base = (R / "receipts/baseline-check-workflows-v1/stdout.txt").read_bytes()
v1_post = (R / "receipts/post-correction-check-workflows-v1.2/stdout.txt").read_bytes()
v1_rep_a, v1_rep_b = load("work/baseline-checks/workflows-report.v1.json"), load("work/post-correction-checks/workflows-report.v1.final.json")
require("historical-workflow1-stdout-identical-and-report-differs-only-in-hashes", v1_base == v1_post
        and {k: v for k, v in v1_rep_a.items() if k != "sourceSha256"} == {k: v for k, v in v1_rep_b.items() if k != "sourceSha256"})
arr = stdout_json("post-correction-check-array-orders")
require("array-orders-passed", arr["failed"] == [] and arr["checks"] == arr["passed"])
p4 = {r["case"]: r for r in load("work/repro-original/receipts/probes/policy-test.json")["rows"] if r["probe"] == "P4"}

if failures:
    print(json.dumps({"refused": failures}, indent=1, default=str))
    sys.exit(1)

review = {
    "artifact": "claude-policy-test-known-hit-author.review", "version": 1, "origin": "823bf66b-e92a-4789-ab81-63a1a9dc371d",
    "standing": ("Bounded AUTHOR policy-test reference/design correction in a disposable capture of verified frozen39. Not independent "
                 "acceptance, not the active independent review's verdict, no frozen/LIVE/other-review artifact altered, no successor "
                 "or source40 claimed, no product, commits, pushes, planning, pins or report regeneration."),
    "assigned": ["P1 known hit suppressed when declared required evidence is absent", "P2 policy universe token admission"],
    "custody": {"frozen39": {k: capture[k] for k in ("manifest", "manifestSha256", "snapshotRoot", "capture", "memberCount", "totalBytes", "copyFaults")},
                "captureVerify": {"before": capture["verifyBefore"], "after": capture["verifyAfter"]}, "endOfWorkRecheck": recheck,
                "counterexampleEvidenceRead": sorted(recheck["counterexampleFiles"])},
    "ownersRead": [
        "foundation/evaluator_composition_model.v3.py compose (rule loop lines 153-193: every selected subject evaluated; unknown includes requiredEvidenceDeficiencies; outcome fail if gating and live, else indeterminate if gating and unknown, else pass; blocks())",
        "foundation/evaluator-composition-contract.v3.md section 2 line 26 (closed policy universe token map; unknown tokens refuse; typescript-v2 not an alias), section 3 lines 34/36 (Kleene, known matches preserved, optional imports never acquire gating authority), section 5 line 56 (required-import deficiency makes a gating rule indeterminate whatever its root unless a live unwaived finding makes it fail; optional-only root unknown stays pass; advisory stays pass), section 9.5 lines 168-174",
        "foundation/check-composition.v3.py A9 controls (a9-known-live-failure-dominates-missing-required-import and peers)",
        "foundation/identity-schemas.v3.json x-opensip-evaluator-profile.policyUniverseMap",
        "foundation/evaluator_input_model.v3.py lines 16, 73 (EVALUATOR_POLICY_UNIVERSE_UNREGISTERED for every rule), 134 (token -> portable domain)",
        "workflows/policy_test_model.v3.py, workflows/workflows_model.v3.py policy.test section, workflows/schemas/evaluator3/policy-test.schema.json, workflows/policy-test-cases.v3.json, workflows/check-workflow-projection.v3.py pt2 block",
        "docs/v2/contracts/product-v1/workflows-and-surfaces.md section 5 DSL and authoring test (lines 591-668) and lines 1575-1580 (missing required evidence and incomplete coverage never silently become an authoritative no-match)",
    ],
    "diagnosis": {
        "P1": ("policy_test_model.v3.evaluate returned for a rule before evaluating any predicate whenever a declared required evidence kind was "
               "absent (frozen39 lines 214-218): known true roots emitted no finding, fail dominance was lost, and waived/non-gating/below-threshold "
               "findings were dropped. Composition evaluates every subject and keeps the required-evidence deficiency independent of the root."),
        "P1-adjacent": ("the optional-evidence-absent disclosure additionally required complete Coverage, so with partial Coverage but every native atom "
                        "known the fixture listed the rule and made a gating verdict indeterminate, where composition blocks only on native or "
                        "required-import causes (discriminated by and-known-true-optional-absent-partial-coverage-all-native-known before correction)."),
        "P2": ("composition contract section 2 closes the policy universe token map (typescript, rust, syntax) and the evaluator input admission refuses "
               "any other token for every rule; the policy.test route never applied it, the authored suites used the historical illustrative token "
               "typescript-v2, and arbitrary rule or fact tokens were accepted (a fact-token typo silently becomes a no-match)."),
    },
    "correction": {
        "model": "evaluate every enumerated subject; a required kind absent is a blocking rule-level deficiency (listed, gating unknown) that keeps known findings and fail dominance; subjects without a known finding stay unknown; an unknown root blocks unless its only causes are absent optional evidence (complete-Coverage precondition removed); fixture fact universe must be a registered token; unregistered_universes(policy)",
        "owner": "workflows_model.v3.run_policy_test: after the current resolver, an unregistered rule universe (enabled or not) is a resolver refusal CONFIG.INVALID / POLICY.UNKNOWN_RULE with remedy EVALUATOR_POLICY_UNIVERSE_UNREGISTERED: <token> (existing route; no new code or detail)",
        "schema": "x-opensip-admission-precedence steps 4 and 5; x-opensip-fixture-representation subject, factUniverse and ruleLaw",
        "contract": "workflows-and-surfaces section 5: fixture fact universe fault; universe resolver refusal; required evidence never suppresses a known finding",
        "fixture": "all typescript-v2 selectors -> typescript (12, explicit new construction); new requiredEvidenceSuite with authored expectations; one authored expected value changed: currentSuite case partial-coverage-is-indeterminate-not-finding indeterminateRules no longer lists runtime-hit (optional-only unknown, composition section 5), case outcome/verdict/expectation outcomes unchanged",
        "checker": "14 pt2 checks: required-evidence suite admission and outcomes, known gating hit survives and fails, known false not an authoritative no-match, waived hit keeps unknown, no selected subjects stay indeterminate, optional-only disclosure under partial coverage, closed tokens in authored suites, each registered token same outcomes, cross-universe facts never occupy, typescript-v2 / arbitrary / disabled-rule token resolver refusals, unregistered fact token CONFIG.INVALID",
        "delta": delta,
        "patchSha256": fsha("output/correction.patch"),
        "identityEffects": ["authored currentSuite suiteDigest and policyTestResultId change because the universe selector bytes changed: " + str(p4.get("same-suite-same-result-bytes", {}).get("observed")),
                            "historical workflow1 route id pinned by pt2-historical-workflow1-policy-test-route-unchanged remains unchanged (check passed)",
                            "PolicyTestResultV1 / CaseResult shape unchanged; no new domain detail, error code, golden or schema major"],
    },
    "results": {
        "originalProbe": {"preCorrection": pre_orig, "postCorrection": post_orig},
        "comparisonProbe": {"preCorrectionV1": {"rows": len(pre1["rows"]), "lawFailures": pre1["lawFailures"], "note": "retained failed attempt: harness derived composition rule-unknown for a disabled rule (section 9.5 applies to enabled rules) and its partial-coverage scenario was not discriminating"},
                            "preCorrectionV2": {"rows": len(pre2["rows"]), "lawFailures": pre2["lawFailures"]},
                            "postCorrection": {"rows": len(post["rows"]), "lawFailures": post["lawFailures"],
                                               "rows_": [(r["group"], r["case"], r["lawOk"]) for r in post["rows"]]}},
        "checks": {"workflowProjection": {"baseline": [wp_base["count"], wp_base["passed"]], "firstPostCorrectionRetainedFailure": [f["id"] for f in wp_fail["failed"]],
                                          "final": [wp_post["count"], wp_post["passed"]], "added": added},
                   "composition": [comp_base["count"], comp_post["count"]], "query": [q_base["count"], q_post["count"]],
                   "historicalWorkflow1": {"stdout": json.loads(v1_post), "stdoutByteIdentical": True, "reportDifference": "sourceSha256 of the changed workflow files only"},
                   "arrayOrders": arr},
    },
    "observationsNotChanged": [
        "workflows_model.v3.resolve_policy (also used by policy.show) does not apply the universe token law; Run admission enforces it in evaluator_input_model.v3. Left unchanged as outside the assigned policy.test boundary; root may decide whether policy.show should refuse earlier.",
        "The fixture unrepresentable/imported-absence unknown stays blocking even for an optional kind whose evidence is available, because production could evaluate that observation true; this is a representation limit, not the production optional-unknown law, and is not compared with composition.",
    ],
    "limits": [
        "Bounded harness: fixture = finite path-only fact view; composition side = check-composition-style synthesized population/Plan/closure locators and scanner values; no full retained Run, native admission or provider execution. No claim here depends on a full Run.",
        "The composition comparison maps fixture advisory to composition pass and derives composition rule-unknown from required-evidence rows or an indeterminate root with a section 5 blocking witness cause (all deficiencies of that root witness; sufficient for these scenarios).",
        "PolicyTestResultV1/CaseResult carry no per-rule unknown cause; the optional-evidence-absent disclosure remains internal to the model.",
        "The retained original probe writes a fixed output path, so its detailed pre-correction row file was overwritten by the post-correction rerun; the pre-correction receipt stdout (failed list) and root's retained reproduction remain.",
        "Expected outcomes in policy-test-cases.v3.json are author expectations aligned to the owning laws; independent review is the oracle.",
        "Only the workflow projection, query, composition, historical workflow1 and array-order checkers were run; full launcher and other children were not.",
    ],
    "receipts": [receipt(p.name) for p in sorted((R / "receipts").iterdir())],
}
text = json.dumps(review, indent=1, default=str) + "\n"
(R / "review.json").write_text(text)
print(json.dumps({"review.json": hashlib.sha256(text.encode()).hexdigest(), "receipts": [(r["label"], r["exit"]) for r in review["receipts"]]}, indent=1))
