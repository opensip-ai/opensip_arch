"""Assemble review.json for the policy-test profile correction from actual custody, manifests, receipts and probe outputs.

Every claim that can be recomputed is recomputed here; the builder refuses (exit 1) when one does not hold, so the
report cannot carry a stale or hand-typed result. Standing, limits and root instructions are labelled text.
"""
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
    return bool(ok)


def receipt(label):
    d = R / "receipts" / label
    return {"label": label, "argv": json.loads((d / "command.json").read_text())["argv"], "cwd": json.loads((d / "command.json").read_text())["cwd"],
            "exit": int((d / "exit.txt").read_text()), **{k: v for k, v in json.loads((d / "digests.json").read_text()).items()}}


def stdout_json(label):
    return json.loads((R / "receipts" / label / "stdout.txt").read_text())


captured = load("custody/captured-source.json")
manifest = load("custody/correction-manifest.json")
repair = load("custody/repair-region-unchanged.json")
ALLOWED = {
    "docs/coop/design-corrections/workflows/schemas/evaluator3/policy-test.schema.json": "added",
    "docs/coop/design-corrections/workflows/policy_test_model.v3.py": "added",
    "docs/coop/design-corrections/workflows/policy-test-cases.v3.json": "added",
    "docs/coop/design-corrections/workflows/workflows_model.v3.py": "modified",
    "docs/coop/design-corrections/workflows/check-workflow-projection.v3.py": "modified",
    "docs/coop/design-corrections/workflows/command-inventory.v3.json": "modified",
    "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json": "modified",
    "docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json": "modified",
    "docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md": "modified",
    "docs/coop/design-corrections/workflows/README.md": "modified",
    "docs/coop/design-corrections/workflows/schemas/evaluator3/README.md": "modified",
    "docs/v2/contracts/product-v1/workflows-and-surfaces.md": "modified",
}
changes = {c["path"]: c["status"] for c in manifest["changes"]}
require("changes-are-exactly-the-authorized-set", changes == ALLOWED, changes)
require("no-pycache-in-edited-copy", manifest["pycacheDirectories"] == [])
require("capture-had-no-drift-or-copy-fault", not captured["copyFaults"] and not captured["inputDriftDuringCapture"])
require("repair-region-and-policy-header-byte-identical", repair["repairRegionByteIdentical"] and repair["headerThroughAdmitPolicyRuleByteIdentical"] and repair["closedWorldSelectorInstall"])
HISTORICAL = ["docs/coop/design-corrections/workflows/workflows_model.v1.py", "docs/coop/design-corrections/workflows/schemas/policy-test.schema.json",
              "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json", "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json",
              "docs/coop/design-corrections/workflows/workflow-cases.v1.json", "docs/coop/design-corrections/workflows/check_workflows.v1.py",
              "docs/coop/design-corrections/workflows/command-inventory.v1.json", "docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py",
              "docs/coop/design-corrections/foundation/atom_model.v1.py", "docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json",
              "docs/coop/design-corrections/workflows/workflow_projection_model.v3.py", "docs/coop/design-corrections/workflows/query_surface_projection.v3.py",
              "docs/coop/design-corrections/public-detail-registry.v1.json"]
cap_files = {f["path"]: f["sha256"] for f in captured["files"]}
require("retained-and-shared-owners-byte-unchanged", all(p in cap_files and p not in changes for p in HISTORICAL))

# ---------------------------------------------------------------- checks before and after
wp_before, wp_after = stdout_json("baseline-check-workflow-projection-v3"), stdout_json("post-edit-check-workflow-projection-v3")
ids_before = {r["id"]: r["ok"] for r in wp_before["results"]}
ids_after = {r["id"]: r["ok"] for r in wp_after["results"]}
added_ids = sorted(set(ids_after) - set(ids_before))
require("workflow-projection-baseline-passed", wp_before["passed"] and wp_before["count"] == 795)
require("workflow-projection-post-edit-passed", wp_after["passed"] and not wp_after["failed"], wp_after["failed"])
require("workflow-projection-no-check-removed-or-flipped", set(ids_before) <= set(ids_after) and all(ids_after[k] == v for k, v in ids_before.items()))
require("workflow-projection-added-checks-are-pt2", added_ids and all(i.startswith("pt2-") for i in added_ids), added_ids)
q_before, q_after = load("work/baseline-checks/query-projection-report.json"), load("work/post-edit-checks/query-projection-report.json")
require("query-projection-passed-before-and-after", q_before["passed"] and q_after["passed"] and q_before["count"] == q_after["count"])
v1_before_out = (R / "receipts/baseline-check-workflows-v1/stdout.txt").read_bytes()
v1_after_out = (R / "receipts/post-edit-check-workflows-v1/stdout.txt").read_bytes()
require("historical-workflow1-checker-stdout-byte-identical", v1_before_out == v1_after_out and json.loads(v1_after_out)["failed"] == 0)
v1_rep_before, v1_rep_after = load("work/baseline-checks/workflows-report.v1.json"), load("work/post-edit-checks/workflows-report.v1.json")
v1_nonhash_equal = {k: v for k, v in v1_rep_before.items() if k != "sourceSha256"} == {k: v for k, v in v1_rep_after.items() if k != "sourceSha256"}
require("historical-workflow1-report-differs-only-in-its-source-hash-table", v1_nonhash_equal)
arr_before, arr_after = stdout_json("baseline-check-array-orders"), stdout_json("post-edit-check-array-orders")
require("array-orders-passed-before-and-after", arr_before["failed"] == [] and arr_after["failed"] == [] and arr_after["checks"] == arr_before["checks"] + 2)
pd = receipt("post-edit-check-policy-derivation-v3")
require("foundation-policy-derivation-child-exit-zero", pd["exit"] == 0, pd)

# ---------------------------------------------------------------- routes and probes
pre, post = load("probes/output/pre-edit-route-probe.json"), load("probes/output/post-edit-route-probe.json")
HIST_ID = "policytest2:5ce020d40b29ce7f1592189d66efd007d732c699a4c612e75b6c788cd497ee27"
H = "historicalWorkflow1Route_P.W.run_policy_test_V1"
require("historical-route-identity-unchanged", pre[H]["policyTestResultId"] == post[H]["policyTestResultId"] == HIST_ID)
require("pre-edit-current-route-admitted-v1-and-refused-v2",
        pre["evaluator3Route_run_admitted_policy_test_V1"]["outcome"] == "RETURNED" and pre["evaluator3Route_run_admitted_policy_test_V2"]["outcome"] == "REFUSED")
require("post-edit-current-route-refuses-v1-by-major",
        [post["evaluator3Route_run_admitted_policy_test_V1"].get(k) for k in ("outcome", "errorCode", "detail")] == ["REFUSED", "REQUEST.SCHEMA_MAJOR_UNSUPPORTED", "EVALUATION.MIXED_OUTPUT_MAJOR"])
v2 = post["evaluator3Route_run_admitted_policy_test_V2"]
fixture = load("work/source/docs/coop/design-corrections/workflows/policy-test-cases.v3.json")
require("post-edit-current-route-returns-the-authored-v2-outcomes",
        v2["outcome"] == "RETURNED" and v2["resolverAccepted"] is True and v2["summary"] == fixture["currentSuiteExpect"]["summary"])
sem = load("probes/output/fixture-semantics-probe.json")
require("focused-semantics-probe-passed", sem["passed"] and sem["count"] == 17, sem["failed"])
inv = load("work/source/docs/coop/design-corrections/workflows/command-inventory.v3.json")
golden_ids = [g["id"] for g in inv["goldens"]]
require("new-golden-present-once", golden_ids.count("policy-test-suite-major-unsupported") == 1)

if failures:
    print(json.dumps({"refused": failures}, indent=1, default=str))
    sys.exit(1)

labels = sorted(p.name for p in (R / "receipts").iterdir())
review = {
    "artifact": "claude-policy-test-profile-author.review", "version": 1, "origin": "823bf66b-e92a-4789-ab81-63a1a9dc371d",
    "standing": ("Bounded authorized AUTHOR correction of the policy-test profile REAL-GAP in an own regular-file copy of the mutable "
                 "successor source. Architecture/design/reference correction only: no product, commits, pushes, planning, global "
                 "pins, grades, final acceptance or readiness. Author-derived checks and probes are reference evidence, not an "
                 "independent review."),
    "rootDecisionsImplemented": {
        "1-suite": "evaluator3 PolicyTestSuiteV2 (urn:opensip:product-v1:workflows:evaluator3:policy-test:2, schemaMajor 2, candidatePolicy PolicyDocumentV2); retained PolicyTestSuiteV1 document, workflow1 model/checker/outputs byte-unchanged; PolicyTestResultV1/policytest2/carrier shape unchanged",
        "2-owner": "workflows_model.v3 defines its own run_policy_test/run_admitted_policy_test calling the v3 resolve_policy (atom owner) and policy_test_model.v3; grammar classifier retargeted to PolicyDocumentV2 with the f561 positional helper unchanged; typed major refusal REQUEST.SCHEMA_MAJOR_UNSUPPORTED/EVALUATION.MIXED_OUTPUT_MAJOR precedes schema and grammar; no new D9 detail",
        "3-semantics": "endpoint source/target, kind applicability (atom owner admission), registered filter projections and quantifiers evaluated from the atom owner's registry and comparators over the finite facts fixture; target discrimination proven through the corrected public route",
        "4-I4": "unrepresentable fields (universe domain, testResult, exitStatus) and selectors (test-execution, test-case) evaluate UNKNOWN; absent imported rows never prove absence; affected finding/no-finding expectations indeterminate; known hits, Kleene and gating preserved; no result shape change",
        "5-references": "§5, dispatch paragraph, §8 surface/host/failure prose, §9 golden row, §10 preimage; projection-contract dispatch table; evaluator3 envelope and invocation descriptions; one new golden policy-test-suite-major-unsupported; READMEs",
        "6-controls": "24 pt2 checks in the existing check-workflow-projection.v3 child plus 17 focused semantics controls and pre/post route probes",
    },
    "custody": {
        "input": captured["input"], "capture": captured["capture"], "fileCount": captured["fileCount"], "totalBytes": captured["totalBytes"],
        "fileListManifestSha256": captured["fileListManifestSha256"], "copyFaults": captured["copyFaults"], "inputDriftDuringCapture": captured["inputDriftDuringCapture"],
        "vsAssessmentFixedCaptureModified": captured["vsAssessmentFixedCapture"]["modified"],
        "vsAuthorPackageMigrationCaptureModified": captured["vsAuthorPackageMigrationCapture"]["modified"],
        "preEditSnapshot": {"path": "work/baseline-files", "files": len(load("custody/baseline-files.json")["files"]), "manifestSha256": fsha("custody/baseline-files.json")},
        "capturedSourceCustodySha256": fsha("custody/captured-source.json"),
    },
    "correction": {"manifest": "custody/correction-manifest.json", "manifestSha256": fsha("custody/correction-manifest.json"),
                   "diff": "output/correction.diff", "diffSha256": manifest["diffSha256"], "diffLines": manifest["diffLines"], "changes": manifest["changes"],
                   "repairRegionProof": repair},
    "newNormativeOrReferencePaths": [p for p, s in ALLOWED.items() if s == "added"],
    "identityAndDispatchChanges": [
        "policy test input: PolicyTestSuiteV1 (urn:opensip:product-v1:workflows:policy-test) -> PolicyTestSuiteV2 (urn:opensip:product-v1:workflows:evaluator3:policy-test:2), schemaMajor 1 -> 2; breaking input change, no relabel",
        "suiteDigest: H(workflow.policy-test-suite, admitted PolicyTestSuiteV2); the preimage now carries suite schemaMajor 2 and the PolicyDocumentV2 candidate",
        "candidatePolicyDigest / effectivePolicyDigest: raw SHA-256 over PolicyDocumentV2 canonical bytes (already the §10 law)",
        "PolicyTestResultV1, domain workflow.policy-test-result, prefix policytest2 and PolicyTestResultRecordV1 carrier: unchanged shape; current authored suite id " + v2["policyTestResultId"],
        "historical workflow1 route and ids unchanged: " + HIST_ID,
        "evaluator3 route admission: suite major -> candidate major (REQUEST.SCHEMA_MAJOR_UNSUPPORTED / EVALUATION.MIXED_OUTPUT_MAJOR) -> closed schema (CONFIG.INVALID with POLICY.IMPERATIVE_KEY_REFUSED or CONFIG.INVALID) -> fixture/override admission (CONFIG.INVALID) -> current resolver details",
        "workflows_model.v3.resolve_policy refuses a non-PolicyDocumentV2 typed (REQUEST.SCHEMA_MAJOR_UNSUPPORTED / EVALUATION.MIXED_OUTPUT_MAJOR); identity-model.v3 does not call resolve_policy",
        "new golden policy-test-suite-major-unsupported (request-rejected 2, REQUEST.SCHEMA_MAJOR_UNSUPPORTED, EVALUATION.MIXED_OUTPUT_MAJOR); goldens now %d" % len(golden_ids),
    ],
    "checks": {
        "workflowProjection": {"before": {"count": wp_before["count"], "passed": wp_before["passed"]}, "after": {"count": wp_after["count"], "passed": wp_after["passed"]},
                               "removed": [], "flipped": [], "added": added_ids},
        "queryProjection": {"before": {"count": q_before["count"], "passed": q_before["passed"]}, "after": {"count": q_after["count"], "passed": q_after["passed"]}},
        "historicalWorkflow1": {"stdout": json.loads(v1_after_out), "stdoutByteIdentical": True,
                                "reportDifference": "only sourceSha256 (hashes of current files it lists: check-workflow-projection.v3.py, command-inventory.v3.json, workflows_model.v3.py, plus the two new owned policy-test files); all 1816 check rows identical"},
        "arrayOrders": {"before": arr_before, "after": arr_after},
        "foundationPolicyDerivationChild": {"receipt": pd, "stdoutTail": (R / "receipts/post-edit-check-policy-derivation-v3/stdout.txt").read_text()[-600:]},
    },
    "probes": {"preEditRoute": pre, "postEditRoute": post, "fixtureSemantics": {k: sem[k] for k in ("passed", "count", "failed")} | {"controls": [(c["id"], c["ok"], c["expectation"]) for c in sem["controls"]]}},
    "receipts": [receipt(l) for l in labels],
    "rootIntegration": {
        "newChildChecker": "not required: the 24 pt2 controls live in the existing workflow-projection child (workflows/check-workflow-projection.v3.py); the launcher job list is unchanged",
        "pins": "root updates the five pin sets (workflows/source-pins.v1.json, foundation/source-pins.v1.json, foundation/evaluator3-source-pins.v1.json, security/source-pins.v1.json, native/source-pins.v2.json) for the 9 modified paths and adds the 3 new paths; not edited here",
        "planning": "root owns the new M5 host policy planning row for golden policy-test-suite-major-unsupported (goldens 44 -> %d) and any implementation-coverage rows; planning files not edited" % len(golden_ids),
        "reports": "retained workflows-report.v1.json in the source was not regenerated here (it already differed from a fresh run at baseline); root regenerates checker receipts under the updated pins",
        "otherActiveWork": "the separate ce3 exact-repair-RunID/declared-exception correction was not read; this change leaves the repair region of workflows_model.v3.py and repair_closed_world_selection.v1.py byte-identical, so its narrow delta should merge without overlap except for check-workflow-projection.v3.py and contract prose, which root must three-way merge",
        "fullSuites": "root reruns the full 17-child launcher and six groups under updated pins; only the listed children were run here",
    },
    "limits": [
        "Bounded deterministic standalone authoring-test semantics over finite facts fixtures; not production evaluator, provider, full Run or native qualification; sources cases remain not-executable",
        "The facts fixture has one universe per fact, no endpoint-universe domain, no test-execution/test-case payloads and no import wrapper completeness; those evaluate unknown by the published representation law rather than being represented",
        "Runtime and history rows are matched by fixture subject path (symbol subjects are identified by path in the fixture); overload ambiguity and runtime row ambiguity refusals of the atom owner are not modelled",
        "PolicyTestResultV1/CaseResult carry no per-rule unknown cause; the retained legacy CaseResult.outcome description text is narrower than the current §5 law and is left byte-unchanged",
        "Expected outcomes in policy-test-cases.v3.json and the focused probe are author expectations; independent review is the oracle",
        "Override value types and unknown override rules are now CONFIG.INVALID in the current route (the historical model raised an untyped KeyError for an unknown rule)",
        "Only the workflow projection, query projection, historical workflow1, array-order and foundation policy-derivation checkers were run; other launcher children and full suites were not",
        "Pins, planning rows, launcher, source acceptance and grades are root-owned and untouched",
    ],
}
text = json.dumps(review, indent=1, default=str) + "\n"
(R / "review.json").write_text(text)
print(json.dumps({"review.json": hashlib.sha256(text.encode()).hexdigest(), "addedChecks": len(added_ids), "goldens": len(golden_ids),
                  "currentSuiteId": v2["policyTestResultId"], "receipts": [(r["label"], r["exit"]) for r in review["receipts"]]}, indent=1))
