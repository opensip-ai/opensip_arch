import json, hashlib, glob, os
O = "/tmp/opensip-design-corrections/post-reset-review.v14"
W = O + "/work"
SUBJ = "/tmp/opensip-design-corrections/candidate-subject.v14"

def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

probes = {}
total = 0
for f in sorted(glob.glob(O + "/evidence/probe-*.json")):
    if f.endswith("probe-attempts.md"): continue
    d = json.load(open(f))
    probes[os.path.basename(f)] = {"cases": len(d["probes"]), "allHold": d["allHold"],
                                   "failed": [r["id"] for r in d["failed"]]}
    total += len(d["probes"])
BOUND = json.load(open(O + "/evidence/probe-cb4-must-1.json"))["boundSources"]

AR_BASIS = ("Independently recomputed the v13->v14 delta over correction-crosswalk.proposed.json: "
            "all 16 AR rows are present in both, none added or removed, and every one of the 16 "
            "differs ONLY in the four review-provenance fields (historicalReviews, "
            "historicalBlindReviews, latestCompletedReview, latestCompletedBlindReview). No "
            "requirement, owner, selector or disposition field changed. CARRIED-UNCHANGED is a "
            "statement about preservation across this delta and is not a new discharge, a closure "
            "or an application grade.")
FW_BASIS = ("All 15 FW rows are published in current-source-map.proposed.md, which I verified is "
            "BYTE-IDENTICAL between candidate-subject.v13 and candidate-subject.v14 (cmp) and which "
            "does not appear in the recomputed 35-file modified set. Preservation only; not a new "
            "discharge.")
RES_BASIS = ("inherited-residuals.proposed.md, inherited-row-sources.proposed.json and "
             "v2/architecture/08-decision-and-readiness-register.md are byte-identical between v13 "
             "and v14 (cmp) and none appears in the 35-file modified set. CARRIED-UNCHANGED records "
             "preservation across this delta only; it closes nothing and grades nothing.")

residual_ids = (["DR-%03d" % i for i in range(1, 12)] +
                ["DR-011-R%02d" % i for i in range(1, 17)])
assert len(residual_ids) == 27

review = {
 "artifact": "post-reset-review",
 "version": "v14",
 "reviewer": "actual Claude, fresh independent design/reference review; authored none of the subject bytes; "
             "not coauthor 77758b10-d7ba-4868-9d42-ae0b13e84cb6, not prior independent "
             "4e3fe6be-4adf-46bc-b4d9-1b4c68349fe2, not blind consumer 878e4b39-2d21-46b2-87bd-64f8d4db015f",
 "date": "2026-09-07",
 "subjectManifestSha256": "45b1e128ca51d114895f3c406cc92575e6efe95051bf319023dc1f3180c2f92c",
 "overallVerdict": "ACCEPT",
 "verdictBasis":
   "All four Bv4 required findings (2 MUST, 2 SHOULD) are resolved in the frozen v14 bytes, and each "
   "resolution was tested by my own probes against ACTUAL Run admission and the actual producer "
   "boundary rather than against isolated schema fields or the author's own cases. 212 independently "
   "authored probe cases hold, every one of them bound to the exact frozen source SHA256s. All six "
   "recorded reference commands reproduce with the recorded exit codes, byte-identical logs and a "
   "ZERO-byte regenerated-report delta, over 1308 transitive pins I verified fresh before running and "
   "did not re-pin. Custody of the frozen subject is identical before and after (6047/6047 files, exact "
   "byte total, no undeclared file, no symlink). Two NEW ADVISORIES are raised; neither is a MUST or a "
   "SHOULD, neither leaves anything unrepresentable or ambiguous in the machine-readable authorities, "
   "and neither is hidden under this headline. Nothing here is application acceptance, blind "
   "reconstructability, product qualification or implementation authorization.",
 "subject": {"snapshotRoot": SUBJ, "fileCount": 6047, "totalBytes": 373681736,
             "predecessorManifestSha256": "8e6670f74d6e0bbed50b6c4914b3c7b29f627221f1591f4add5567f652f4c023"},
 "custody": {
   "before": "evidence/custody-before.json", "after": "evidence/custody-after.json",
   "manifestSha256Verified": True, "filesVerified": 6047, "hashMismatches": 0,
   "lengthMismatches": 0, "missing": 0, "undeclaredFiles": 0, "symlinksOrNonRegular": 0,
   "identicalBeforeAndAfter": True,
   "note": "Every declared file's SHA256 and byte length was recomputed, and the tree was walked "
           "independently to prove no undeclared file and no non-regular entry exists. The frozen "
           "subject and the original repository were never written to; all work, including the full "
           "disposable copy, is under post-reset-review.v14."},
 "exactDelta": {
   "method": "Recomputed from the v13 and v14 manifests directly, not read from any author account.",
   "filesAdded": 1668, "filesRemoved": 0, "filesModified": 35,
   "normativeModified": [
     "docs/v2/contracts/product-v1/native-evidence.md",
     "docs/v2/contracts/product-v1/identity-and-evidence.md",
     "docs/v2/contracts/product-v1/admission-and-qualification.md",
     "docs/v2/contracts/product-v1/security-and-lifecycle.md",
     "docs/v2/contracts/product-v1/workflows-and-surfaces.md",
     "docs/coop/design-corrections/foundation/identity-schemas.v2.json",
     "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json",
     "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
     "docs/coop/design-corrections/native/native-capability-matrix.v2.json",
     "docs/coop/design-corrections/public-detail-registry.v1.json",
     "docs/coop/design-corrections/workflows/schemas/common.schema.json",
     "docs/coop/design-corrections/workflows/schemas/command-envelope.schema.json"],
   "unchangedLoadBearing": [
     "docs/coop/artifacts/d9-exit-contract.v1.14.json (historical D9, byte-identical)",
     "docs/coop/artifacts/permission-truth-tables.v9.json",
     "docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json",
     "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json",
     "docs/coop/design-corrections/current-source-map.proposed.md",
     "docs/coop/design-corrections/inherited-residuals.proposed.md",
     "docs/coop/design-corrections/qualification-gates.proposed.json",
     "docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json"],
   "addedAreCustodyRecords":
     "The 1668 added files are author/root custody records - before-images, blind-input copies, "
     "check logs, handoffs and probe outputs - not new normative surface. The normative change is "
     "confined to the 12 files listed above."},
 "suiteReproduction": {
   "commandsReproduced": 6, "allExitZero": True, "logsByteIdenticalToRetained": True,
   "regeneratedReportDelta": {"added": 0, "removed": 0, "modified": 0},
   "fullSourceCopyDeltaAfterEverything": {"added": 0, "removed": 0, "modified": 0},
   "pinVerification": {"totalPinsChecked": 1308, "stale": 0, "missing": 0, "rePinnedByMe": False,
     "byFile": {"foundation/source-pins.v1.json": 1099, "workflows/source-pins.v1.json": 65,
                "native/source-pins.v2.json": 71, "security/source-pins.v1.json": 73},
     "note": "Verified BEFORE running anything. The v11 stale-pin failure is historical and did "
             "not recur; I did not re-pin to make this candidate pass."},
   "measuredCounts": {
     "foundationChecksPassed": 1630,
     "identityPassingCalls": 1282, "identityDistinctIds": 1270, "identityDuplicateExtraInstances": 12,
     "securityCases": 456, "securityInvariantSweeps": 10,
     "nativeCases": 347, "nativeMatrixCells": 66,
     "workflowSurfaceChecks": 1598, "integrationChecks": 365},
   "countHonesty":
     "I recounted the identity report myself: 1282 check CALLS over 1270 DISTINCT IDs, the 12 extra "
     "instances coming from exactly two ids at 7 instances each, all passing. The candidate's own "
     "identity-check-counts.v14.json states the same three numbers, so check calls are not presented "
     "as unique case IDs. Neither number is exhaustive coverage.",
   "nondeterminismObserved":
     "None. Every regenerated report was byte-identical to the retained one, so there is no "
     "intended-nondeterministic operational field to report and nothing was normalized away."},
 "independentProbeCaseTotal": total,
 "independentProbes": probes,
 "independentProbeDisagreements": [],
 "boundSourceSha256": BOUND,
 "fixtureProvenance":
   "My probes DRIVE the candidate's own check-identity.py / identity-model.py / "
   "native_evidence_model.v2.py through their real entry points and bind those files' exact SHA256s "
   "(boundSourceSha256). Shared fixture extraction is used only to reach admission; the verdicts are "
   "my own assertions about what admission does. No synthetic re-implementation was used as an oracle.",
 "harnessErrorsCorrectedNotCountedAsDefects": {
   "count": 16,
   "record": "evidence/probe-attempts.md",
   "note": "Every probe that failed first is retained with its exact refusal and an attribution of "
           "whether the fault was mine, a fixture limit, or an unreachable premise. Three are worth "
           "naming because a careless reviewer would have scored them as candidate defects: the "
           "half-matching-universe fact refused at the PRIOR same-only law; my hand-forged RC-3 entry "
           "was correctly refused by RC-2; and my assumption that a syntax-universe empty result WAS "
           "the false-complete graph was wrong - the fixture emits the honest unknown/"
           "language-tier-unsupported/capability-missing answer, so I had to forge the false claim to "
           "test it."},
 "priorFindingDispositions": {},
 "newMustIssues": [],
 "newShouldIssues": [],
 "newAdvisories": [],
 "arDispositions": {}, "fwDispositions": {},
 "inheritedResidualDispositions": {}, "scopedReviewOwnerDispositions": {},
}

for i in range(1, 17):
    review["arDispositions"]["AR-%02d" % i] = {
        "disposition": "CARRIED-UNCHANGED", "gradedByThisReview": False,
        "selectors": ["docs/coop/design-corrections/correction-crosswalk.proposed.json#/items/AR-%02d" % i],
        "basis": AR_BASIS}
for i in range(1, 16):
    review["fwDispositions"]["FW-%02d" % i] = {
        "disposition": "CARRIED-UNCHANGED", "gradedByThisReview": False,
        "selectors": ["docs/coop/design-corrections/current-source-map.proposed.md#FW-%02d" % i],
        "basis": FW_BASIS}
for rid in residual_ids:
    review["inheritedResidualDispositions"][rid] = {
        "disposition": "CARRIED-UNCHANGED", "closedByThisReview": False,
        "selectors": ["docs/coop/design-corrections/inherited-residuals.proposed.md#" + rid,
                      "docs/v2/architecture/08-decision-and-readiness-register.md"],
        "basis": RES_BASIS}
review["inheritedResidualDispositions"]["DR-011-R10"]["basis"] += (
    " R10 is the row the product-v1 contract set itself sits under and is therefore the one row this "
    "delta actually touches; its underlying register entry is nonetheless byte-unchanged, and the "
    "contract changes are graded above as the four Bv4 dispositions rather than as a residual closure.")

for did in ["DR-201", "DR-202", "DR-203", "DR-204", "DR-205"]:
    review["scopedReviewOwnerDispositions"][did] = {
        "disposition": "ROUTING-ASSESSED-ONLY-NOT-APPLIED",
        "scope": "Owner routing only. I assessed that the routing record exists and is unchanged "
                 "across this delta; I did not grade the owner's substantive answer, and this review "
                 "does not apply it.",
        "authority": "Owner routing is recorded by correction-crosswalk row AR-15, whose only "
                     "v13->v14 change is review-provenance pointers. Five owner routing assessments "
                     "do not grant a final application outcome; the separate application review owns "
                     "that.",
        "selectors": ["docs/coop/design-corrections/correction-crosswalk.proposed.json#/items/AR-15"],
        "gradedByThisReview": False}

json.dump(review, open(O + "/review.partial.json", "w"), indent=1)
print("wrote skeleton;", total, "probe cases;", len(review["arDispositions"]), "AR;",
      len(review["fwDispositions"]), "FW;", len(review["inheritedResidualDispositions"]), "residuals;",
      len(review["scopedReviewOwnerDispositions"]), "scoped")
