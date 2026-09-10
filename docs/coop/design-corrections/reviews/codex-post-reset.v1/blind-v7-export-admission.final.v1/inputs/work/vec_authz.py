"""Test-execution / native-preparation / repair authorization, the current-
baseline audit comparison cases, and the purge/replay boundary.

Every effect value is COPIED from the pinned permission truth table, in the
child-process execution mode those owners run in; nothing here asserts an
enforced value of its own.
"""

import json

import oslib as O
import graph as G
import build as B
from oslib import C, H, sha256hex, raw_digest

PROJECT = B.PROJECT
REQ = "req1_" + "b3" * 16
EXEC = "exec1_" + "d7" * 16

PT = O.doc("permission-truth")
EFFECT_TOKEN = {"subprocess": "PT-PROC-EXEC-DECLARED",
                "filesystemWrite": "PT-FS-WRITE-HOST-STATE",
                "network": "PT-NET-EGRESS",
                "environment": "PT-ENV-READ"}


def truth_table(platform, mode="child-process"):
    fam = "macos" if platform.startswith("macos") else "linux"
    tab = [t for t in PT["truthTables"]["tables"] if t["platform"] == fam][0]
    return {r["token"]: r["ENFORCED"]["byExecutionMode"][mode]["enforced"]
            for r in tab["rows"]}


def effects_for(platform):
    tt = truth_table(platform)
    return {name: tt[tok] for name, tok in EFFECT_TOKEN.items()}


def build_authorization_vectors():
    out = {}
    plats = ["linux-x86_64-gnu", "linux-aarch64-gnu", "macos-aarch64",
             "macos-x86_64"]
    out["effectSelectionFromPinnedTable"] = {p: effects_for(p) for p in plats}
    out["brokeredTokenDeliberatelyUnprojected"] = {
        "token": "PT-HOST-EFFECT-BROKERED",
        "childProcessValue": truth_table("macos-aarch64")["PT-HOST-EFFECT-BROKERED"],
        "projectedByAnyEffectName": any(
            t == "PT-HOST-EFFECT-BROKERED" for t in EFFECT_TOKEN.values())}
    out["readOnlyTokensUnprojected"] = [
        t for t in truth_table("macos-aarch64")
        if t not in EFFECT_TOKEN.values()]

    snapshot = "snapshot2:" + "31" * 32
    tool_closure = "closure2:" + "42" * 32
    dep_set = "sha256:" + "53" * 32
    owner_rows = sorted(
        [{"ownerKey": "serde_derive 1.0.0 (proc-macro)",
          "source": "dependency-closure-member",
          "ownerFileManifestSha256": sha256hex(b"serde_derive-manifest")},
         {"ownerKey": "build.rs@wsroot", "source": "snapshot-member",
          "ownerFileManifestSha256": sha256hex(b"wsroot-build-manifest")}],
        key=lambda r: r["ownerKey"].encode("utf-8"))
    owner_source_digest = raw_digest(owner_rows)

    # --- a build-script / proc-macro preparation grant --------------------
    grant = {"grantSchema": 2, "principalClass": "repository-code",
             "semanticPrincipalKind": "trusted-repository-code",
             "projectId": PROJECT, "snapshotId": snapshot,
             "argvDigest": sha256hex(b"cargo check --offline --frozen --locked"),
             "executionClass": "build-script",
             "owners": owner_rows, "ownerSourceDigest": owner_source_digest,
             "runner": {"kind": "toolchain-closure", "member": "bin/cargo"},
             "dependencySourceSetId": dep_set.split(":", 1)[1],
             "toolClosureId": tool_closure, "platformId": "macos-aarch64",
             "effects": effects_for("macos-aarch64"),
             "authorization": {"mode": "interactive-explicit",
                               "policyRecordId": None, "ci": False},
             "expiry": "operation-end", "inherited": False}
    out["preparationGrant"] = {
        "record": grant,
        "schemaErrors": O.validate("security", "#/schemas/RepoExecutionGrantV2",
                                   grant),
        "securityGrantRef": "security.repo-execution-grant.v2:"
                            + H("security.repo-execution-grant.v2", grant),
        "ownerSourceDigestIsRawSha256OfCanonicalOwnerArray":
            owner_source_digest == raw_digest(owner_rows)}

    # a TEST-RUNNER grant: owners is [] and ownerSourceDigest is the digest of
    # the CANONICAL EMPTY owner array (security S10)
    empty_owner_digest = raw_digest([])
    test_grant = dict(grant, executionClass="test-runner", owners=[],
                      ownerSourceDigest=empty_owner_digest,
                      dependencySourceSetId=None,
                      runner={"kind": "snapshot-member",
                              "member": "scripts/run-tests.sh"},
                      argvDigest=sha256hex(b"scripts/run-tests.sh --ci"),
                      authorization={"mode": "policy-record",
                                     "policyRecordId": sha256hex(b"policy-rec"),
                                     "ci": True})
    out["testRunnerGrant"] = {
        "record": test_grant,
        "schemaErrors": O.validate("security", "#/schemas/RepoExecutionGrantV2",
                                   test_grant),
        "canonicalEmptyOwnerArrayDigest": empty_owner_digest,
        "consentMapping": {"security": "policy-record",
                           "workflowTestExecution": "pre-existing-policy",
                           "workflowRepairApply": "policy"},
        "interactiveConsentInCiRefuses": True}

    # a CI invocation with interactive consent must refuse
    bad_ci = dict(test_grant, authorization={"mode": "interactive-explicit",
                                             "policyRecordId": None, "ci": True})
    out["interactiveConsentInCi"] = {
        "schemaErrors": O.validate("security", "#/schemas/RepoExecutionGrantV2",
                                   bad_ci),
        "schemaAdmitsShape": O.validate(
            "security", "#/schemas/RepoExecutionGrantV2", bad_ci) == [],
        "refusedBy": "security S10 semantic admission "
                     "(TEST.INTERACTIVE_CONSENT_IN_CI), not by the schema"}

    # an over-claimed enforcement value must refuse
    over = dict(grant, effects=dict(effects_for("macos-aarch64"),
                                    network="ENFORCED-PLATFORM:seatbelt"))
    out["overClaimedEnforcement"] = {
        "schemaErrors": O.validate("security", "#/schemas/RepoExecutionGrantV2",
                                   over),
        "equalsPinnedTable": over["effects"] == effects_for("macos-aarch64"),
        "refusedBy": "security S10 / native S5.2: every effect value must EQUAL "
                     "the pinned truth-table entry; a stronger claim refuses"}

    # a display alias as a platform id must refuse
    alias = dict(grant, platformId="macos-arm64")
    out["platformDisplayAlias"] = {
        "schemaErrors": O.validate("security", "#/schemas/RepoExecutionGrantV2",
                                   alias)}

    # --- AuthorizedExecutionV2 preflight ---------------------------------
    tool_chain = {"rustCommitHash": "9d" * 20, "rustcVersion": "1.83.0",
                  "cargoVersion": "1.83.0",
                  "sysrootDigest": sha256hex(b"sysroot"),
                  "rustcDevLlvmDigest": "aa" * 32,
                  "standardLibraryComponentDigests": [],
                  "targetTriple": "aarch64-apple-darwin"}
    tool_cl = {"rustc": "01" * 32, "cargo": "02" * 32, "linker": "03" * 32,
               "ar": "04" * 32, "procMacroServer": "05" * 32,
               "closureId": tool_closure}
    ae = {"schemaVersion": 2, "operation": "native.prepare",
          "principalClass": "repository-code", "projectId": PROJECT,
          "snapshotId": snapshot, "dependencySourceSetId": dep_set,
          "toolchain": tool_chain, "toolClosure": tool_cl,
          "cfgSetId": "primary",
          "owners": sorted([
              {"ownerKey": "build.rs@wsroot", "kind": "build-script",
               "ownerFileManifestSha256": sha256hex(b"wsroot-build-manifest"),
               "provenanceAssurance": "in-snapshot", "source": "snapshot-member"},
              {"ownerKey": "serde_derive 1.0.0 (proc-macro)", "kind": "proc-macro",
               "ownerFileManifestSha256": sha256hex(b"serde_derive-manifest"),
               "provenanceAssurance": "declared",
               "source": "dependency-closure-member"}],
              key=lambda r: r["ownerKey"].encode("utf-8")),
          "effects": {k: {"requested": k, "enforcement": v}
                      for k, v in effects_for("macos-aarch64").items()},
          "authorization": {"mode": "interactive-explicit",
                            "policyRecordId": None, "ci": False},
          "liveBoundaries": {"revocationCheck": "before-each-owner",
                             "cancellation": "process-group-kill",
                             "trustClockRequired": True},
          "bounds": {"maxOwners": 4096, "maxWallMilliseconds": 3600000,
                     "maxOutDirBytes": 4294967296,
                     "maxOutputBytesPerOwner": 268435456},
          "authorizationRef": "security.repo-execution-grants.v2:"
                              + H("security.repo-execution-grants.v2",
                                  {"schemaVersion": 2,
                                   "grantRefs": sorted([
                                       "security.repo-execution-grant.v2:"
                                       + H("security.repo-execution-grant.v2",
                                           grant)])}),
          "semanticGrantPrincipalKind": "trusted-repository-code",
          "workflowPrincipalSpelling": "P-TRUSTED-REPO"}
    out["authorizedExecution"] = {
        "record": ae,
        "schemaErrors": O.validate("native", "#/$defs/AuthorizedExecutionV2", ae),
        "effectsEqualPinnedTable":
            {k: v["enforcement"] for k, v in ae["effects"].items()}
            == effects_for("macos-aarch64"),
        "authorizationRefIsOperationalAndNotInPlan": True,
        "declaredProvenanceDisclosed":
            [o["ownerKey"] for o in ae["owners"]
             if o["provenanceAssurance"] == "declared"],
        "preExecutionSentence":
            "Build scripts and procedural macros from 2 packages will run with "
            "your user's authority. OpenSIP does not prevent network access or "
            "other effects on this platform. Packages with declared "
            "(unauthenticated) provenance: serde_derive 1.0.0 (proc-macro)."}

    # --- repair apply authorization --------------------------------------
    repair_plan_id = "repairplan2:" + "7e" * 32
    ra = {"authorizationSchema": 1, "kind": "repair-apply",
          "projectId": PROJECT, "repairPlanId": repair_plan_id,
          "baseSnapshotId": snapshot,
          "recipeClosureId": "closure2:" + "6a" * 32,
          "consent": {"mode": "interactive-explicit", "policyRecordId": None,
                      "ci": False},
          "expiry": "operation-end", "leaseMode": "EXCLUSIVE",
          "repositoryExecution": False}
    out["repairApplyAuthorization"] = {
        "record": ra,
        "schemaErrors": O.validate("security",
                                   "#/schemas/RepairApplyAuthorizationV1", ra),
        "authorizationRef": "security.repair-apply-authorization.v1:"
                            + H("security.repair-apply-authorization.v1", ra),
        "boundToExactRepairPlanId": repair_plan_id,
        "repositoryExecutionIsConstantFalse": ra["repositoryExecution"] is False}
    # any edit to the descriptor mints a different repairPlanId that no
    # authorization names
    out["repairPlanEditBreaksAuthorization"] = {
        "authorizationNamesPlan": repair_plan_id,
        "editedPlanId": "repairplan2:" + "7f" * 32,
        "authorizationDoesNotName": True}
    return out


# ---------------------------------------------------------------------------
# Current-baseline audit: missing pivot / evidence changed / EMPTY result
# ---------------------------------------------------------------------------
def _base_descriptor(**over):
    det = "closure2:" + "aa" * 32
    ctx = {"policyDigest": sha256hex(b"policy"),
           "scopeDigest": sha256hex(b"scope"),
           "waiverSetDigest": sha256hex(b"waivers"),
           "detectorClosureIds": [det],
           "evidenceAvailability": {"importKinds": [], "relations": [],
                                    "imports": []}}
    d = {"schemaFamily": "opensip.product.comparison", "schemaMajor": 1,
         "baselineId": "baseline2:" + "bb" * 32,
         "currentRunId": "run2:" + "cc" * 32,
         "currentSnapshotId": "snapshot2:" + "dd" * 32,
         "auditProfile": {"name": "code-regression", "gateCodeNetNew": True,
                          "gateNewlyLiveByPolicyAxes": False,
                          "gateAllCurrentLive": False,
                          "newWaiverSuppressesCodeNetNew": False,
                          "gateRuleUnder": "baseline-or-current"},
         "projectCorrespondence": "same-project", "comparisonPerformed": True,
         "baselineContext": ctx, "currentContext": dict(ctx),
         "contextDelta": {"codeChanged": True, "detectorChanged": False,
                          "policyChanged": False, "scopeChanged": False,
                          "waiversChanged": False,
                          "evidenceAvailabilityChanged": False},
         "pivotsAvailable": {"E0": "not-needed", "E1": "not-needed",
                             "E2": "not-needed", "E3": "not-needed"},
         "detectors": [{"detectorId": "unused-export",
                        "baselineClosureId": det, "currentClosureId": det,
                        "baselineSemanticsMajor": 1, "currentSemanticsMajor": 1,
                        "method": "identical-closure"}],
         "ruleDeficiencies": [], "entries": [],
         "counts": {"UNCHANGED": 0, "CODE-NET-NEW": 0, "CODE-FIXED": 0,
                    "DETECTION-DELTA": 0, "POLICY-DELTA": 0, "SCOPE-DELTA": 0,
                    "WAIVER-DELTA": 0, "EVIDENCE-DELTA": 0, "INDETERMINATE": 0,
                    "gating": 0},
         "verdict": "pass"}
    d.update(over)
    return d


def build_comparison_vectors():
    out = {}
    fp = "finding-key2:" + "9a" * 32
    det = "closure2:" + "aa" * 32

    # (1) a MISSING required prior detector pivot: the detector was REMOVED, so
    #     E1..E4 are false and E0 must never be substituted with B.
    d = _base_descriptor()
    d["detectors"] = [{"detectorId": "unused-export",
                       "baselineClosureId": det, "currentClosureId": None,
                       "baselineSemanticsMajor": 1, "currentSemanticsMajor": 1,
                       "method": "detector-removed",
                       "pivotRunId": "run2:" + "ee" * 32,
                       "indeterminateReason": "pivot-detector-unavailable"}]
    d["pivotsAvailable"] = {"E0": "unavailable", "E1": "not-needed",
                            "E2": "not-needed", "E3": "not-needed"}
    d["entries"] = [{"fingerprint": fp, "ruleId": "unused-export",
                     "detectorId": "unused-export",
                     "presence": {"B": True, "E0": None, "E1": False,
                                  "E2": False, "E3": False, "E4": False,
                                  "waivedB": False, "waivedC": False},
                     "classification": "INDETERMINATE",
                     "indeterminateReason": "pivot-detector-unavailable",
                     "subsequentDeltas": [], "liveInCurrent": False,
                     "gates": True, "gateReason": "indeterminate-gating-rule"}]
    d["counts"]["INDETERMINATE"] = 1
    d["counts"]["gating"] = 1
    d["verdict"] = "indeterminate"
    out["missing-prior-detector-pivot"] = {
        "descriptor": d,
        "schemaErrors": O.validate("comparison-result", "#",
                                   {"comparisonResultId":
                                        "comparison2:" + H("workflow.comparison", d),
                                    "descriptor": d}),
        "note": "a vanished finding whose prior detector cannot be run is "
                "INDETERMINATE, never CODE-FIXED"}

    # (2) EVIDENCE CHANGED on a gating rule -> INDETERMINATE, never a
    #     non-gating EVIDENCE-DELTA
    imp_a = {"kind": "runtime", "importId": "import2:" + "11" * 32,
             "payloadDigest": sha256hex(b"p1"),
             "sourceCorrespondenceDigest": sha256hex(b"c1"),
             "scopeDigest": sha256hex(b"s1"),
             "observationDigest": sha256hex(b"o1")}
    imp_b = dict(imp_a, importId="import2:" + "22" * 32,
                 payloadDigest=sha256hex(b"p2"))
    d2 = _base_descriptor()
    d2["baselineContext"]["evidenceAvailability"] = {
        "importKinds": ["runtime"], "relations": ["runtime-observation"],
        "imports": [imp_a]}
    d2["currentContext"] = dict(d2["baselineContext"])
    d2["currentContext"]["evidenceAvailability"] = {
        "importKinds": ["runtime"], "relations": ["runtime-observation"],
        "imports": [imp_b]}
    d2["contextDelta"] = dict(d2["contextDelta"], codeChanged=False,
                              evidenceAvailabilityChanged=True)
    d2["ruleDeficiencies"] = [{"ruleId": "unused-export", "gating": True,
                               "cause": "required-evidence-unavailable"}]
    d2["entries"] = [{"fingerprint": fp, "ruleId": "unused-export",
                      "detectorId": "unused-export",
                      "presence": {"B": True, "E0": None, "E1": True,
                                   "E2": True, "E3": True, "E4": True,
                                   "waivedB": False, "waivedC": False},
                      "classification": "INDETERMINATE",
                      "indeterminateReason": "evidence-content-changed",
                      "subsequentDeltas": [], "liveInCurrent": True,
                      "gates": True, "gateReason": "indeterminate-gating-rule"}]
    d2["counts"]["INDETERMINATE"] = 1
    d2["counts"]["gating"] = 1
    d2["verdict"] = "indeterminate"
    out["evidence-content-changed-on-a-gating-rule"] = {
        "descriptor": d2,
        "schemaErrors": O.validate("comparison-result", "#",
                                   {"comparisonResultId":
                                        "comparison2:" + H("workflow.comparison", d2),
                                    "descriptor": d2}),
        "note": "replacing an artifact with another of the same kind is still "
                "an evidence change; attribution is INDETERMINATE, not "
                "EVIDENCE-DELTA, because the rule gates"}

    # (3) EMPTY RESULT on both sides with a missing required re-evaluation:
    #     zero entries never establish that nothing regressed.
    d3 = _base_descriptor()
    d3["contextDelta"] = dict(d3["contextDelta"], codeChanged=False,
                              policyChanged=True)
    d3["currentContext"] = dict(d3["currentContext"],
                                policyDigest=sha256hex(b"policy-v2"))
    d3["pivotsAvailable"] = {"E0": "not-needed", "E1": "not-needed",
                             "E2": "unavailable", "E3": "not-needed"}
    d3["ruleDeficiencies"] = [{"ruleId": "unused-export", "gating": True,
                               "cause": "required-coverage-unknown"}]
    d3["entries"] = []
    d3["counts"]["gating"] = 0
    d3["verdict"] = "indeterminate"
    out["empty-result-with-a-missing-required-re-evaluation"] = {
        "descriptor": d3,
        "schemaErrors": O.validate("comparison-result", "#",
                                   {"comparisonResultId":
                                        "comparison2:" + H("workflow.comparison", d3),
                                    "descriptor": d3}),
        "note": "both observed finding sets are empty and the comparison is "
                "still INDETERMINATE, because a missing E2 re-evaluation can "
                "hide a finding that appears in neither set"}

    # (4) whole-comparison indeterminacy: unmapped project, ZERO entries
    d4 = _base_descriptor(projectCorrespondence="unmapped",
                          comparisonPerformed=False,
                          wholeIndeterminateReason="baseline-project-unmapped",
                          remedy={"code": "BASELINE.PROJECT_UNMAPPED",
                                  "remedy": "re-adopt the baseline in this "
                                            "project, or pass --accept-origin"},
                          verdict="indeterminate")
    out["whole-comparison-unmapped-project"] = {
        "descriptor": d4,
        "schemaErrors": O.validate("comparison-result", "#",
                                   {"comparisonResultId":
                                        "comparison2:" + H("workflow.comparison", d4),
                                    "descriptor": d4}),
        "entryCount": len(d4["entries"])}
    return out


# ---------------------------------------------------------------------------
# purge / replay boundary and required-output failure
# ---------------------------------------------------------------------------
def purge_and_replay():
    return {
        "queryAfterPurgeOfRetainedManifest": {
            "class": "success", "exitCode": 0,
            "statement": "query of the retained manifest is allowed after purge "
                         "and states evidence unavailable"},
        "queryRequiringActualProof": {
            "class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED",
            "exitCode": 2, "domainDetailCandidates":
                ["evidence.expired", "evidence.purged", "evidence.missing",
                 "evidence.corrupt"],
            "position": "BEFORE evaluation"},
        "inabilityDuringASelectedOperation": {
            "class": "operational-failed", "errorCode": "HOST.IO_FAILURE",
            "faultCause": "host-io", "exitCode": 4,
            "position": "DURING the selected operation"},
        "admittedPartialNativeInputs": {
            "class": "indeterminate", "exitCode": 3,
            "statement": "successfully admitted but incomplete inputs seal an "
                         "AUTHORITATIVE Run and terminate indeterminate"},
        "regenerationMismatch": {
            "class": "operational-failed", "errorCode": "HOST.IO_FAILURE",
            "faultCause": "host-io", "exitCode": 4,
            "domainDetail": "evidence.regeneration-mismatch",
            "statement": "a regeneration whose result disagrees cannot replace "
                         "the sealed Run"},
        "ephemeralCannotSupplyAuthority": {
            "class": "request-rejected", "errorCode": "REQUEST.UNSATISFIABLE",
            "exitCode": 2,
            "domainDetail": "WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY"},
        "theseAreDifferentEventPositions": True,
    }
