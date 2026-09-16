"""Assemble review.json for the imported-universe follow-up from actual custody, delta manifests, receipts and probe outputs.
Recomputable claims are recomputed; the builder refuses (exit 1) when one does not hold."""
import hashlib
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parent
V1 = Path("/private/tmp/opensip-design-corrections/claude-policy-test-known-hit-author.v1")
ROOT = Path("/tmp/opensip-design-corrections/root-policy-test-imported-universe-probe.v1")
load = lambda p: json.loads(Path(p).read_text()) if Path(p).is_absolute() else json.loads((R / p).read_text())
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
V1_PATCH = "8fe83cd122eefeec384f4d48aebc2c2eaa505a5c1a1bac5958c6fe74672a9f28"
capture, applied, recheck = load("custody/frozen39-capture.json"), load("custody/v1-delta-application.json"), load("custody/end-of-work-recheck.json")
combined, incremental = load("custody/combined-delta-manifest.json"), load("custody/incremental-delta-manifest.json")
require("capture-verified", capture["manifestSha256"] == F39 and capture["memberCount"] == 12909 and not capture["copyFaults"]
        and not capture["verifyBefore"]["faults"] and not capture["verifyAfter"]["faults"] and not capture["verifyBefore"]["unlisted"])
require("v1-delta-applied-exactly", applied["applied"] and not applied["faults"] and applied["v1PatchSha256"] == V1_PATCH
        and applied["regeneratedPatchEqualsV1Patch"] and len(applied["changes"]) == 6
        and all(c["beforeVerified"] and c["afterVerified"] for c in applied["changes"]))
require("nothing-outside-runtime-altered", recheck["faults"] == [])
V1_SIX = {c["path"] for c in applied["changes"]}
require("combined-delta-is-the-six-v1-files-only", {c["path"] for c in combined["changes"]} == V1_SIX
        and {c["status"] for c in combined["changes"]} == {"modified"} and combined["pycacheDirectories"] == [])
INCREMENTAL = {"docs/coop/design-corrections/workflows/policy_test_model.v3.py", "docs/coop/design-corrections/workflows/policy-test-cases.v3.json",
               "docs/coop/design-corrections/workflows/check-workflow-projection.v3.py"}
require("incremental-delta-is-model-cases-checker-only", {c["path"] for c in incremental["changes"]} == INCREMENTAL
        and {c["status"] for c in incremental["changes"]} == {"modified"})
v1_after = {c["path"]: c["afterSha256"] for c in applied["changes"]}
require("v1-schema-owner-contract-bytes-preserved", all(c["afterSha256"] == v1_after[c["path"]] for c in combined["changes"] if c["path"] not in INCREMENTAL))

# reproduction, correction, regressions
pre_root, post_root = load("probes/root-adapted/pre-fix/report.json"), load("probes/root-adapted/post-fix/report.json")
root_report = load(str(ROOT / "report.json"))
require("root-failure-reproduced-exactly", pre_root["rows"] == root_report["rows"] and pre_root["confirmedWrongUniverseKnownHit"] is True)
inputs_same = all((R / "probes/root-adapted" / phase / n).read_bytes() == (ROOT / n).read_bytes()
                  for phase in ("pre-fix", "post-fix") for n in ("frozen39-typescript-suite.json", "frozen39-rust-suite.json",
                                                                 "author-correction-typescript-suite.json", "author-correction-rust-suite.json"))
require("root-suite-inputs-byte-identical-in-both-runs", inputs_same)
corrected = {r["factUniverse"]: r["result"] for r in post_root["rows"] if r["source"] == "author-correction"}
require("root-probe-corrected-outcomes", corrected["typescript"]["outcome"] == "passed" and corrected["typescript"]["observedVerdict"] == "fail"
        and corrected["rust"]["findings"] == [] and corrected["rust"]["observedVerdict"] == "indeterminate" and "unmet" not in corrected["rust"]["expectationOutcomes"])
frozen = {r["factUniverse"]: r["result"] for r in post_root["rows"] if r["source"] == "frozen39"}
require("frozen39-still-shows-the-defect-in-post-run", frozen["rust"]["findings"] != [])
pre_iu, post_iu = load("probes/output/pre-fix-imported-universe.json"), load("probes/output/post-fix-imported-universe.json")
require("discrimination-probe-pre-fix-failures", [c for _, c in pre_iu["lawFailures"]] == [
    "runtime-exists-foreign-rust-hit-only-is-unknown", "runtime-exists-foreign-syntax-hit-only-is-unknown", "runtime-none-foreign-hit-is-unknown-not-false",
    "runtime-count0-foreign-hit-is-unknown-not-false", "history-exists-foreign-row-only-is-unknown", "history-none-foreign-row-is-unknown-not-false",
    "imported-occupancy-helper-present"], pre_iu["lawFailures"])
require("discrimination-probe-post-fix-clean", post_iu["lawFailures"] == [] and len(post_iu["rows"]) == 23)
require("v1-comparison-probe-still-clean", stdout_json("post-fix-v1-known-hit-universe-probe") == {"rows": 37, "lawFailures": []})
require("original-independent-probe-still-clean", stdout_json("post-fix-original-independent-probe") == {"total": 50, "failed": []})

# checks
wp_pre = stdout_json("pre-fix-check-workflow-projection-v3-with-new-controls")
wp_post = stdout_json("post-fix-check-workflow-projection-v3")
wp_v1 = json.loads((V1 / "receipts/post-correction-check-workflow-projection-v3.2/stdout.txt").read_text())
ia, ib = {r["id"]: r["ok"] for r in wp_v1["results"]}, {r["id"]: r["ok"] for r in wp_post["results"]}
added = sorted(set(ib) - set(ia))
require("pre-fix-checker-fails-exactly-the-new-discriminating-controls", sorted(f["id"] for f in wp_pre["failed"]) == sorted([
    "pt2-imported-universe-suite-reaches-the-authored-outcomes", "pt2-foreign-universe-runtime-and-history-rows-establish-no-known-match",
    "pt2-foreign-universe-imported-rows-behave-exactly-like-imported-absence", "pt2-foreign-uncertain-row-neither-occupies-nor-weakens-a-same-universe-hit",
    "pt2-imported-occupancy-requires-the-evaluated-subject-and-universe"]) and wp_pre["count"] == 860)
require("post-fix-checker-passes-no-removed-or-flipped-vs-v1", wp_post["passed"] and wp_post["count"] == 860 and set(ia) <= set(ib)
        and all(ib[k] == v for k, v in ia.items()) and len(added) == 8 and all(a.startswith("pt2-") for a in added))
comp = stdout_json("post-fix-check-composition-v3")
require("composition-checker", comp["passed"] and comp["count"] == 30)
q = load("work/post-fix-checks/query-projection-report.json")
require("query-checker", q["passed"] and q["count"] == 204)
v1_out = (R / "receipts/post-fix-check-workflows-v1/stdout.txt").read_bytes()
require("historical-workflow1-stdout-identical-to-frozen39-baseline", v1_out == (V1 / "receipts/baseline-check-workflows-v1/stdout.txt").read_bytes())
rep_a, rep_b = load(str(V1 / "work/baseline-checks/workflows-report.v1.json")), load("work/post-fix-checks/workflows-report.v1.json")
require("historical-workflow1-report-differs-only-in-hashes", {k: v for k, v in rep_a.items() if k != "sourceSha256"} == {k: v for k, v in rep_b.items() if k != "sourceSha256"})
arr = stdout_json("post-fix-check-array-orders")
require("array-orders", arr["failed"] == [] and arr["checks"] == arr["passed"])

if failures:
    print(json.dumps({"refused": failures}, indent=1, default=str))
    sys.exit(1)

review = {
    "artifact": "claude-policy-test-imported-universe-author.review", "version": 1, "origin": "823bf66b-e92a-4789-ab81-63a1a9dc371d",
    "standing": ("Bounded AUTHOR follow-up to the completed known-hit v1 correction, in a fresh capture of verified frozen39 plus the exact v1 delta. "
                 "Not independent acceptance; independent85 review and blind9d3d remain active and are not claimed; no frozen40; no product, commits, "
                 "pushes, pins, planning, registry or detail additions; frozen39, root and v1 artifacts unaltered."),
    "assigned": "imported-atom universe join: a registered foreign-universe runtime fixture row produced a known finding for a typescript rule",
    "custody": {"frozen39Capture": {k: capture[k] for k in ("manifest", "manifestSha256", "snapshotRoot", "capture", "memberCount", "totalBytes", "copyFaults")},
                "v1DeltaApplication": applied, "beforeImages": {"v39": "work/before-images-v39", "v1": "custody/before-images-v1.json"},
                "endOfWorkRecheck": recheck,
                "rootEvidenceRead": ["probe.py", "command.json", "report.json", "stdout.json", "stderr.txt", "frozen39-typescript-suite.json", "frozen39-rust-suite.json",
                                     "author-correction-typescript-suite.json", "author-correction-rust-suite.json", "initial-observation/report.json"]},
    "diagnosis": ("policy_test_model.v3._atom evaluated representable imported selectors (runtime-subject, history-subject) by subject path only: "
                  "_native_occupancy requires fact.universe == evaluated universe but the imported loop did not. A runtime or history fixture row "
                  "of another registered universe therefore became a known match (exists true, none false, count-at-most false above N) or an "
                  "uncertain row for the typescript subject, contradicting x-opensip-fixture-representation.factUniverse ('occupancy requires it "
                  "to equal the evaluated subject universe, so a fact of another registered universe never occupies'). Present in frozen39 and "
                  "unchanged by v1 (v1 only restricted tokens to the closed map)."),
    "correction": {
        "model": "new _imported_occupancy(fact, subject, universe) = subject path and universe equality; the imported atom loop skips any row that does not occupy before observability classification, filters or keys, so a foreign row is neither known nor uncertain; absence semantics unchanged (never proves absence)",
        "cases": "explicitly authored importedUniverseSuite (4 rules: native file-exists control, history-change-exists, runtime-hit-exists, runtime-hit-none; 5 cases) with expected outcomes",
        "checker": "8 pt2 checks: suite admission and outcomes, same-universe runtime/history known matches, foreign rows establish no known match, foreign rows behave exactly like imported absence, foreign uncertain row neither occupies nor weakens a same-universe hit, optional evidence absent stays disclosed, occupancy helper requires subject and universe",
        "normative": "none: the published factUniverse law already requires universe equality for every fixture fact; the model now honours it",
        "combinedDelta": combined, "combinedPatchSha256": fsha("output/combined.patch"),
        "incrementalDelta": incremental, "incrementalPatchSha256": fsha("output/incremental.patch"),
    },
    "results": {
        "rootProbe": {"preFix": {r["source"] + ":" + r["factUniverse"]: {k: r["result"][k] for k in ("outcome", "observedVerdict", "findings", "indeterminateRules", "expectationOutcomes")} for r in pre_root["rows"]},
                      "postFix": {r["source"] + ":" + r["factUniverse"]: {k: r["result"][k] for k in ("outcome", "observedVerdict", "findings", "indeterminateRules", "expectationOutcomes")} for r in post_root["rows"]},
                      "inputsByteIdenticalToRoot": inputs_same},
        "discriminationProbe": {"preFix": pre_iu["lawFailures"], "postFix": {"rows": len(post_iu["rows"]), "lawFailures": post_iu["lawFailures"]},
                                "rows": [(r["group"], r["case"], r["lawOk"]) for r in post_iu["rows"]]},
        "v1Regression": {"comparisonProbe": stdout_json("post-fix-v1-known-hit-universe-probe"), "originalIndependentProbe": stdout_json("post-fix-original-independent-probe")},
        "checks": {"workflowProjection": {"v1Final": wp_v1["count"], "preFixWithNewControls": {"count": wp_pre["count"], "failed": [f["id"] for f in wp_pre["failed"]]},
                                          "postFix": {"count": wp_post["count"], "passed": wp_post["passed"]}, "addedVsV1": added},
                   "composition": comp["count"], "query": q["count"], "historicalWorkflow1": json.loads(v1_out), "arrayOrders": arr},
    },
    "limits": [
        "Bounded fixture reference: finite path-only fact rows with a declared universe token; no full Run, provider, native admission or wrapper completeness. No claim depends on a full Run.",
        "Foreign uncertain rows cannot change a three-valued imported atom value in this model (imported atoms decide only from known rows), so their exclusion is proven by the white-box occupancy trace and the helper check, not by route values alone.",
        "test-execution and test-case selectors stay unrepresentable, so no fixture row of any universe can occupy them; their controls show that unchanged.",
        "The authored importedUniverseSuite expectations are author expectations aligned to the published factUniverse/importedLaw; independent review is the oracle.",
        "Checks run: workflow projection, query, composition, historical workflow1, array-order; the full launcher and other children were not run.",
    ],
    "receipts": [receipt(p.name) for p in sorted((R / "receipts").iterdir())],
}
text = json.dumps(review, indent=1, default=str) + "\n"
(R / "review.json").write_text(text)
print(json.dumps({"review.json": hashlib.sha256(text.encode()).hexdigest(), "combinedPatch": combined["patchSha256"], "incrementalPatch": incremental["patchSha256"],
                  "receipts": [(r["label"], r["exit"]) for r in review["receipts"]]}, indent=1))
