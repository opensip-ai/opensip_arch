import json, os, glob, hashlib
O = "/tmp/opensip-design-corrections/consumer-b.v8/output"
KIT = "/tmp/opensip-design-corrections/consumer-b.v8/subject"
man = json.load(open(KIT + "/consumer-input-manifest.json"))
ok = 0
for f in man["files"]:
    b = open(os.path.join(KIT, f["path"]), "rb").read()
    if hashlib.sha256(b).hexdigest() == f["sha256"] and len(b) == f["bytes"]:
        ok += 1
ob = json.load(open(O + "/object-table.json"))
bl = json.load(open(O + "/blobs.b64.json"))
gaps = json.load(open(O + "/vectors-gaps.json"))
log = open(O + "/run-all.log").read()
npass = sum(1 for l in log.splitlines() if l.startswith("PASS "))
nfail = sum(1 for l in log.splitlines() if l.startswith("FAIL "))

def vec(name):
    p = O + "/vectors-%s.json" % name
    return json.load(open(p)) if os.path.exists(p) else None

must = [g for g in gaps if g["severity"] == "MUST"]
should = [g for g in gaps if g["severity"] == "SHOULD"]

out = {
 "artifact": "opensip.dr-011-r10.blind-consumer-b.reconstruction",
 "verdict": "CHANGES_REQUIRED",
 "standing": ("Independent blind consumer-B reconstruction from the 46-file kit "
              "alone. Disposable design-reference evidence. NOT product "
              "qualification, NOT a readiness grade, NOT implementation "
              "authorization. No author model, fixture, golden, report or prior "
              "review was read; no historical/review link was followed."),
 "inputManifest": {
   "path": "subject/consumer-input-manifest.json",
   "declaredFiles": len(man["files"]),
   "verifiedByteExact": ok,
   "mismatched": len(man["files"]) - ok,
   "unlistedFilesOnDisk": 0,
   "parentSubjectSha256Asserted": man["parentSubjectSha256"],
   "parentSubjectVerifiable": False,
   "parentSubjectNote": ("this kit is a declared SUBSET of that parent, so the "
                         "parent aggregate is not recomputable from these bytes; "
                         "recorded as an unverified custody assertion, not a "
                         "defect")},
 "execution": {
   "command": "sh /tmp/opensip-design-corrections/consumer-b.v8/output/run-all.sh",
   "interpreter": "/tmp/opensip-architecture-review-env/bin/python -I -B",
   "exitCode": 0, "passAssertions": npass, "failAssertions": nfail,
   "log": "run-all.log",
   "nothingExecutedExternally": ("no compiler, cargo, provider, renderer, "
                                 "repository, filesystem, SQLite, crypto or "
                                 "network operation ran")},
 "completePositiveRuns": {
   "count": len(ob["runs"]),
   "totalClosureChecks": sum(r["closureChecks"] for r in ob["runs"]),
   "allClosed": all(r["closureOk"] for r in ob["runs"]),
   "reVerifiedFromBase64ExportAlone": True,
   "runs": [{"label": r["label"], "runId": r["runId"], "planId": r["planId"],
             "snapshotId": r["snapshotId"], "projectId": r["projectId"],
             "closureChecks": r["closureChecks"], "objectCount": r["objectCount"],
             "hIdentityCount": r["hIdentityCount"],
             "canonicalRecordCount": r["canonicalRecordCount"],
             "rawArtifactCount": r["rawArtifactCount"]} for r in ob["runs"]]},
 "retainedEvidence": {
   "objectTable": "object-table.json (typed identity, domain, kind, descriptor)",
   "blobExport": "blobs.b64.json (base64 of every retained blob and every H "
                 "preimage frame, keyed by raw SHA-256)",
   "distinctRetainedObjects": bl["count"],
   "fromScratchCommand": "run-all.sh (step 14 re-verifies every graph from the "
                         "export ALONE)",
   "source": "work/ (osip.py, schemas.py, closure.py, capman.py, protocol.py, "
             "workflow.py, build.py, assemble.py, run_*.py, t_*.py, export.py)"},
 "advertisedModesCovered": ["ts-tsconfig", "js-allowjs", "js-synthesized",
                            "rust-cargo", "rust-cargo-prepared", "syntax-only"],
 "nativeUniversesCovered": ["native.semantic-universe.typescript.v2",
                            "native.semantic-universe.rust.v2",
                            "native.semantic-universe.syntax.v2"],
 "vectorSets": {
   "capabilityManifest": vec("capability-manifest"),
   "typescriptRun": vec("typescript-run"),
   "typescriptConfig": vec("typescript-config"),
   "rustRun": vec("rust-run"),
   "rustNativeHPreimages": vec("rust-preimages"),
   "preparedMode": vec("prepared"),
   "syntaxOnlyRuns": vec("syntax-run"),
   "importedEvidence": vec("import"),
   "findings": vec("finding"),
   "protocol3Traces": vec("protocol3"),
   "workflowSurfaces": vec("workflow-surfaces"),
   "baselineComparisonRepairAndRC1": vec("part3")},
 "newMustIssues": [
   {"id": g["id"], "severity": "MUST", "title": g["title"],
    "observedResult": g["observedResult"],
    "whatWouldCloseIt": g["whatAClosedContractWouldHaveDone"],
    "selectors": g["detail"].get("selectors") if isinstance(g.get("detail"), dict)
                 else None,
    "evidence": g["detail"]} for g in must],
 "newShouldIssues": [
   {"id": g["id"], "severity": "SHOULD", "title": g["title"],
    "observedResult": g["observedResult"],
    "whatWouldCloseIt": g["whatAClosedContractWouldHaveDone"],
    "selectors": g["detail"].get("selectors") if isinstance(g.get("detail"), dict)
                 else None,
    "evidence": g["detail"]} for g in should],
 "advisories": [
   {"id": "CB-ADV-1",
    "title": "view.schemaDigests states membership but the required SET is not "
             "mechanically derivable from the retained record, while the value "
             "reaches RunId",
    "selector": "foundation/identity-schemas.v2.json#/$defs/view/properties/"
                "schemaDigests",
    "disposition": "determined by what the view actually admitted; a "
                   "checkability gap, not an ambiguity. I listed the relation "
                   "payload document and the native document (plus the "
                   "imported-evidence document for the import Run)."},
   {"id": "CB-ADV-2",
    "title": "no published join between semantic-evidence.importIds and "
             "plan.importIds",
    "selector": "foundation/identity-schemas.v2.json#/$defs/semantic-evidence/"
                "properties/importIds",
    "disposition": "identity section 3 requires every EVALUATED import to be "
                   "Plan-selected and listed in evaluationInputRefs (enforced "
                   "here); equality of the evidence list is unstated. I set them "
                   "equal."},
   {"id": "CB-ADV-3",
    "title": "the single content-addressed store means a byte-identical artifact "
             "reachable by two joins yields ONE first refusal on loss, masking "
             "the second",
    "selector": "identity-and-evidence.md section 3, the closing digest law "
                "(`ONE content-addressed store keyed by raw SHA256`)",
    "measuredAt": "CB-RS-N7: dropping the vendored dependency member reports "
                  "EVIDENCE_UNAVAILABLE naming the SNAPSHOT source blob and "
                  "masks the dependency-file-manifest blobJoin, which would have "
                  "produced the same code",
    "disposition": "a consequence of the contract's own single-store design; "
                   "noted so the refusal name is not read as the only join"},
   {"id": "CB-ADV-4",
    "title": "the disclosed D9 successor-artifact obligation remains live",
    "selector": "native/native-evidence.schemas.v2.json#/x-opensip-public-route-"
                "registry/successorArtifactObligation",
    "measured": {"inheritedFaultCauseEnumSize": 11,
                 "inheritedContainsHostInvariant": False,
                 "selectedFaultCauseEnumSize": 12,
                 "addedMembers": ["host-invariant"],
                 "mappedToExistingErrorCode": "SYSTEM.OUTCOME.ILLEGAL_STATE",
                 "classesExitCodesReasonCodesUnchanged": True},
    "disposition": "already disclosed and attributed by the kit; recorded as a "
                   "live cross-unit obligation, not a new finding"}],
 "helperBugsCorrectedAgainstTheKit": [
   {"id": "CB-FIX-1",
    "originalFailure": "the ADM-TYPE gate typed ABSENT keys, so a missing "
                       "required key on AbsentCapability reported ADM-TYPE",
    "normativeAnswer": "ADM-TYPE types a PRESENT scalar before its content is "
                       "compared; ADM-CLOSED owns the key set "
                       "(capability-manifest-domains.v2.json#/admission)",
    "correction": "presence is passed to the type gate; CB-CM-5 now observes "
                  "ADM-CLOSED",
    "isANewDesignGap": False},
   {"id": "CB-FIX-2",
    "originalFailure": "native contexts were discovered by reading "
                       "plan.nativeContextDigests, so a hidden retained context "
                       "was invisible (CB-TS-N12 returned no fault)",
    "normativeAnswer": "identity section 3: `the set of retained context frames "
                       "must equal plan.nativeContextDigests exactly, so a "
                       "context reached by no Plan is refused`",
    "correction": "the set is scanned from the STORE; CB-TS-N12 now observes "
                  "PLAN_CONTEXT_SET_MISMATCH",
    "isANewDesignGap": False},
   {"id": "CB-FIX-3",
    "originalFailure": "universes were discovered by scanning for well-formed "
                       "frames, so a raw canonical payload offered where a frame "
                       "is required was skipped and CB-TS-N10 reported a "
                       "downstream SCOPE_UNIVERSE_NOT_RETAINED",
    "normativeAnswer": "identity section 3: `a raw canonical payload is never "
                       "admissible there, because C(X) does not begin with the "
                       "framing prefix`",
    "correction": "universes are RESOLVED BY DIGEST from the scopes and facts "
                  "that name them; CB-TS-N10 now observes FRAME_PREFIX",
    "isANewDesignGap": False}],
 "myExpectationsThatWereWrongAndTheKitRight": [
   {"id": "CB-EXP-1",
    "expected": "a byte flip inside a retained frame refuses at the identity "
                "check",
    "observed": "it refuses at frame PARSING (LEX_SYNTAX), which MASKS the "
                "identity check; a mutation that keeps the payload canonical is "
                "needed to reach H_IDENTITY_MISMATCH",
    "disposition": "the kit's ordering is right; the vector was rewritten"},
   {"id": "CB-EXP-2",
    "expected": "15 registered (relation, rung) pairs",
    "observed": "17 pairs over a 15-token flat rung vocabulary; 5 resolved and "
                "12 not-applicable, exactly as RC-1 enumerates",
    "disposition": "schema vocabulary is not relation membership; the "
                   "expectation was wrong"},
   {"id": "CB-EXP-3",
    "expected": "a retained hash-valid fact referenced by no view refuses",
    "observed": "it does not, and must not: identity section 3 says "
                "`Unreferenced CAS blobs are not evaluation inputs`. The "
                "discriminating control is the same fact CITED by a predicate "
                "witness, which refuses "
                "(WITNESS_FACT_OUTSIDE_EVALUATED_VIEW).",
    "disposition": "a deliberate asymmetry with plan.nativeContextDigests, which "
                   "IS a set equality; both controls are retained"}],
 "whatRequiredInvention": {
   "authoringFreedomNoContractMissing": [
     "message codes and remedy texts",
     "SubjectIdV1 spellings for symbol subjects (opaque by design)",
     "ownerKey and cfgSetId tokens",
     "repository shapes, file bytes and level-specification bytes",
     "the declaration-signature token projection (the contract fixes the "
     "ENCODING and leaves the projection to the selected detector closure)"],
   "forcedByAMissingOrAmbiguousContract": [
     "CB-GAP-1 which of two ScopeDocumentV1 parameters is the Plan's scope policy",
     "CB-GAP-3 the coverage / examinedExhaustive join",
     "CB-GAP-4 the stage-spec.operation and outputDomains vocabulary",
     "CB-GAP-5 the plan.semanticClosures membership set"],
   "assumedNeverProved": [
     "every TCB observation: closure signatures and manifests, custody results, "
     "provider frame emissions, enforcement values, grammar-bundle contents, "
     "ledger pin inventories, dependency checksums, and the existence of the "
     "artifacts my inventories name",
     "that a real worker emits the protocol frames in the order the table states",
     "OS process exit/EOF, fsync, SQLite, flock, ACL/O_NOFOLLOW custody, "
     "signature verification and cancellation bounds"]},
 "limitations": [
   "no product qualification, readiness grade or implementation authorization",
   "no compiler, Cargo, provider, renderer, OS, SQLite, crypto or network "
   "operation was performed; real measurements remain future qualification work",
   "not built: CloneCandidateGroupV2 near/cross-tsjs candidate records; a full "
   "BaselineArtifactV1 instance; the security unit's own signed records "
   "(RootV1/V2, RepoExecutionGrantV2, InstallationTransitionJournalV1, the "
   "trust-recovery epoch) beyond the workflow-side projections; the "
   "HTML/SARIF/agent renderers; the policy-test suite; the graph-query surface",
   "my closure checker is STRICTER than the contract in applying snapshot and "
   "relation joins to every retained fact frame, including unreferenced ones; "
   "that is conservative and does not refuse them",
   "the public detail registry has 287 members and I exercised a named subset",
   "matrix coverage is by MODE and UNIVERSE, not by cell: at least one closing "
   "Run per language mode and per native universe, exercising the inventory, "
   "syntax, clones-fact, references and unresolved-edge capabilities"],
 "noClaimOfQualification": ("Passing this reconstruction is not product "
                            "qualification and authorizes no implementation. No "
                            "cell is QUALIFIED; SUPPORTED-DESIGN is unchanged. "
                            "Synthetic TCB observations are assumptions, never "
                            "native enforcement proof.")}
with open(O + "/blind-review.json", "w") as f:
    json.dump(out, f, indent=1, sort_keys=False)
print("verdict:", out["verdict"])
print("MUST:", [i["id"] for i in out["newMustIssues"]])
print("SHOULD:", [i["id"] for i in out["newShouldIssues"]])
print("advisories:", [i["id"] for i in out["advisories"]])
print("runs:", out["completePositiveRuns"]["count"],
      "checks:", out["completePositiveRuns"]["totalClosureChecks"],
      "pass:", out["execution"]["passAssertions"],
      "fail:", out["execution"]["failAssertions"])
