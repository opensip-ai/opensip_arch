"""Vector set 4: current-baseline audit and comparison, cache key vs cache hit,
explicit test / preparation / repair authorization."""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixtures as F  # noqa: E402
import graph as G  # noqa: E402
import kit  # noqa: E402
import osip  # noqa: E402
import runner  # noqa: E402
import scen_ts  # noqa: E402

R = []


def rec(cid, kind, desc, payload):
    R.append({"id": cid, "kind": kind, "description": desc, "result": payload})


def neg(cid, desc, fn):
    try:
        fn()
        R.append({"id": cid, "kind": "negative", "description": desc,
                  "outcome": "ADMITTED", "problem": "expected a refusal"})
    except (G.Refusal, ValueError, osip.AdmissionError) as exc:
        R.append({"id": cid, "kind": "negative", "description": desc,
                  "outcome": "refused", "refusal": str(exc)})


STORE = G.Store()
SCN = scen_ts.build(STORE, "ordinary")
OUT = runner.assemble(SCN)
RULE_CLOSURE = SCN["rule"]["id"]
DETECTOR_ID = "no-clone-of-add"
FP = "finding-key2:" + hashlib.sha256(b"a fingerprint").hexdigest()
BASELINE_ID = "baseline2:" + hashlib.sha256(b"a baseline").hexdigest()

PROFILES = {
    "code-regression": {"name": "code-regression", "gateCodeNetNew": True,
                        "gateNewlyLiveByPolicyAxes": False, "gateAllCurrentLive": False,
                        "newWaiverSuppressesCodeNetNew": False,
                        "gateRuleUnder": "baseline-or-current"},
    "report-only": {"name": "report-only", "gateCodeNetNew": False,
                    "gateNewlyLiveByPolicyAxes": False, "gateAllCurrentLive": False,
                    "newWaiverSuppressesCodeNetNew": True,
                    "gateRuleUnder": "current-only"},
}


def context(policy, scope_policy, waivers, detectors, imports=()):
    bound = sorted(imports, key=lambda b: b["importId"])
    ctx = {"policyDigest": policy, "scopeDigest": scope_policy,
           "waiverSetDigest": waivers, "detectorClosureIds": list(detectors),
           "evidenceAvailability": {"importKinds": sorted({b["kind"] for b in bound}),
                                    "relations": [], "imports": bound}}
    kit.validate("comparison", "#/$defs/EvaluationContext", ctx)
    return ctx


def comparison(entries, delta, pivots, detectors, deficiencies, verdict,
               profile="code-regression", performed=True, whole_reason=None,
               base=None, cur=None):
    counts = {k: 0 for k in ["UNCHANGED", "CODE-NET-NEW", "CODE-FIXED",
                             "DETECTION-DELTA", "POLICY-DELTA", "SCOPE-DELTA",
                             "WAIVER-DELTA", "EVIDENCE-DELTA", "INDETERMINATE"]}
    for e in entries:
        counts[e["classification"]] += 1
    counts["gating"] = sum(1 for e in entries if e["gates"])
    d = {"schemaFamily": "opensip.product.comparison", "schemaMajor": 1,
         "baselineId": BASELINE_ID, "currentRunId": OUT["run"]["id"],
         "currentSnapshotId": SCN["snapshot"]["id"],
         "auditProfile": PROFILES[profile], "projectCorrespondence": "same-project",
         "comparisonPerformed": performed,
         "baselineContext": base or BASE_CTX, "currentContext": cur or BASE_CTX,
         "contextDelta": delta, "pivotsAvailable": pivots, "detectors": detectors,
         "ruleDeficiencies": deficiencies, "entries": entries, "counts": counts,
         "verdict": verdict}
    if whole_reason:
        d["wholeIndeterminateReason"] = whole_reason
    kit.validate("comparison", "#/$defs/ComparisonDescriptor", d)
    return {"comparisonId": "comparison2:" + osip.H("workflow.comparison", d),
            "descriptor": d}


POLICY_D = OUT["plan"]["descriptor"]["policyDigest"]
WAIVER_D = OUT["plan"]["descriptor"]["waiverDigest"]
SCOPE_POLICY_D = osip.canonical_record_digest(
    {"schemaFamily": "opensip.product.scope", "schemaMajor": 1,
     "include": ["src/**"], "exclude": []})
BASE_CTX = context(POLICY_D, SCOPE_POLICY_D, WAIVER_D, [RULE_CLOSURE])

NO_DELTA = {"codeChanged": False, "detectorChanged": False, "policyChanged": False,
            "scopeChanged": False, "waiversChanged": False,
            "evidenceAvailabilityChanged": False}
ALL_NEEDED = {"E0": "not-needed", "E1": "not-needed", "E2": "not-needed",
              "E3": "not-needed"}
IDENTICAL_DETECTOR = [{"detectorId": DETECTOR_ID, "baselineClosureId": RULE_CLOSURE,
                       "currentClosureId": RULE_CLOSURE, "baselineSemanticsMajor": 2,
                       "currentSemanticsMajor": 2, "method": "identical-closure"}]


def entry(classification, presence, gates, gate_reason=None, subsequent=(),
          reason=None, live=True, direction=None):
    e = {"fingerprint": FP, "ruleId": DETECTOR_ID, "detectorId": DETECTOR_ID,
         "presence": presence, "classification": classification,
         "subsequentDeltas": list(subsequent), "liveInCurrent": live, "gates": gates}
    if gate_reason:
        e["gateReason"] = gate_reason
    if reason:
        e["indeterminateReason"] = reason
    if direction:
        e["direction"] = direction
    return e


PRES = {"B": False, "E0": None, "E1": True, "E2": True, "E3": True, "E4": True,
        "waivedB": False, "waivedC": False}

# --- A1. current-baseline audit: a genuine code regression -----------------
c1 = comparison([entry("CODE-NET-NEW", dict(PRES, E0=False), True, "code-net-new",
                       direction="appeared")],
                dict(NO_DELTA, codeChanged=True), ALL_NEEDED, IDENTICAL_DETECTOR,
                [], "fail")
rec("A1-code-regression", "positive",
    "current-baseline audit with an identical detector closure: the fingerprint is "
    "absent at B and E0 and present from E1 on, so the FIRST axis at which it "
    "changes is code -> CODE-NET-NEW, and it gates under code-regression",
    {"comparisonId": c1["comparisonId"], "verdict": "fail",
     "counts": c1["descriptor"]["counts"]})

# --- A2. code regression hidden by a same-change policy edit ---------------
c2 = comparison([entry("CODE-NET-NEW", dict(PRES, E0=False, E2=False, E3=False,
                                            E4=False), True,
                       "code-net-new-policy-hidden", ["policy"], live=False,
                       direction="appeared")],
                dict(NO_DELTA, codeChanged=True, policyChanged=True),
                dict(ALL_NEEDED, E2="available"), IDENTICAL_DETECTOR, [], "fail")
rec("A2-code-net-new-policy-hidden", "positive",
    "a bug introduced and simultaneously hidden by disabling the rule stays "
    "CODE-NET-NEW with subsequentDeltas=[policy] and still gates under "
    "baseline-or-current",
    {"comparisonId": c2["comparisonId"], "verdict": "fail"})

# --- A3. missing prior detector (removal) ---------------------------------
removed = [{"detectorId": DETECTOR_ID, "baselineClosureId": RULE_CLOSURE,
            "currentClosureId": None, "baselineSemanticsMajor": 2,
            "currentSemanticsMajor": None, "method": "indeterminate",
            "indeterminateReason": "pivot-detector-unavailable"}]
c3 = comparison([entry("INDETERMINATE", dict(PRES, B=True, E0=None), True,
                       "indeterminate-gating-rule", reason="pivot-detector-unavailable")],
                dict(NO_DELTA, detectorChanged=True),
                dict(ALL_NEEDED, E0="unavailable"), removed, [], "indeterminate")
rec("A3-missing-prior-detector", "positive",
    "a removed detector requires the actual current-trusted prior detector pivot and "
    "sets E1..E4 false; E0 is never substituted with B, so missing prior execution "
    "is INDETERMINATE (a new bug hidden by removing its detector cannot pass)",
    {"comparisonId": c3["comparisonId"], "verdict": "indeterminate",
     "E0": "unavailable", "reason": "pivot-detector-unavailable"})

# --- A4. evidence-changed with a gating rule ------------------------------
cur_ev = context(POLICY_D, SCOPE_POLICY_D, WAIVER_D, [RULE_CLOSURE],
                 [{"kind": "runtime", "importId": "import2:" + "b" * 64,
                   "payloadDigest": "c" * 64,
                   "sourceCorrespondenceDigest": "d" * 64,
                   "scopeDigest": "e" * 64, "observationDigest": "f" * 64}])
c4 = comparison([entry("INDETERMINATE", PRES, True, "indeterminate-gating-rule",
                       reason="evidence-availability-changed")],
                dict(NO_DELTA, evidenceAvailabilityChanged=True), ALL_NEEDED,
                IDENTICAL_DETECTOR,
                [{"ruleId": DETECTOR_ID, "gating": True,
                  "cause": "required-evidence-unavailable"}],
                "indeterminate", cur=cur_ev)
rec("A4-evidence-changed", "positive",
    "the evidence axis compares exact bound import2 IDENTITIES per kind, not kind "
    "presence. If availability changed and the rule gates on either side, "
    "attribution is INDETERMINATE; required evidence loss can never disappear as a "
    "non-gating delta. This contract carries NO evidence counterfactual pivot.",
    {"comparisonId": c4["comparisonId"], "verdict": "indeterminate",
     "baselineImports": [],
     "currentImports": [b["importId"] for b in
                        cur_ev["evidenceAvailability"]["imports"]]})

# --- A5. empty result -----------------------------------------------------
c5 = comparison([], dict(NO_DELTA, policyChanged=True),
                dict(ALL_NEEDED, E2="unavailable"), IDENTICAL_DETECTOR,
                [{"ruleId": DETECTOR_ID, "gating": True,
                  "cause": "required-coverage-unknown"}],
                "indeterminate", whole_reason="pivot-reevaluation-unavailable")
rec("A5-empty-result-is-not-a-pass", "positive",
    "a missing required policy re-evaluation makes the comparison indeterminate "
    "whenever an enabled rule gates, EVEN WHEN BOTH observed finding sets are empty: "
    "missing evaluation can hide a finding that appears in neither set, and entry "
    "counts cannot prove its absence. Zero emitted findings never establish "
    "complete analysis.",
    {"comparisonId": c5["comparisonId"], "entryCount": 0, "verdict": "indeterminate",
     "ruleDeficiencies": c5["descriptor"]["ruleDeficiencies"]})

# --- A6. numeric comparability (FW-11 / architecture13 section 6) ----------
rec("A6-metric-redistribution", "advisory",
    "architecture13 section 6 comparability is binding: a numeric comparison needs "
    "the same metric definition, supplied diff scope and comparison base. Moving "
    "findings between regions without a comparable behavioral result is "
    "REDISTRIBUTION, not evidence of behavioral improvement, and incompatible "
    "inputs must be reported incompatible rather than presented as an improvement.",
    {"comparableExample": {"metric": "gating findings", "scope": "src/**",
                           "base": BASELINE_ID, "baseline": 3, "current": 1,
                           "comparable": True},
     "incomparableExample": {"metric": "gating findings",
                             "baselineScope": "src/**", "currentScope": "src/core/**",
                             "comparable": False,
                             "requiredReport": "incompatible, never an improvement"}})

# --- B1. cache key construction is NOT cache hit admission ----------------
plan = OUT["plan"]
stage_spec = {"schemaVersion": 2, "planId": plan["id"],
              "producerClosure": SCN["provider"]["id"], "operation": "native.analyze",
              "parameters": [], "outputDomains": ["coverage", "fact", "subject-scope"],
              "outputSchemaDigest": kit.doc_digest("native")}
kit.validate("identity", "#/$defs/stage-spec", stage_spec)
cache_record = {"schemaVersion": 2, "planId": plan["id"],
                "producerClosure": SCN["provider"]["id"],
                "stageSpecDigest": osip.canonical_record_digest(stage_spec),
                "scopeIds": sorted(s["id"] for s in SCN["scopes"]),
                "inputRefs": sorted(
                    [{"domain": "native-context", "digest": SCN["context"]["hex"]}],
                    key=lambda r: osip.c_encode(r)),
                "outputSchemaDigest": kit.doc_digest("native")}
try:
    kit.validate("identity", "#/$defs/cache-key", cache_record)
    ck_valid = True
except ValueError as exc:
    ck_valid = str(exc)
cache_key = "cache2:" + osip.H("cache-key", cache_record)
regen_key = "regen2:" + osip.H("regeneration-key", cache_record)
rec("B1-cache-key-vs-cache-hit", "positive",
    "constructing a cache key is PURE and reads no bytes; admitting a hit requires "
    "the Run's whole closure. cache-key and regeneration-key share one schema and "
    "differ only by H domain.",
    {"cacheKeyRecordValidatesUnderIdentitySchema": ck_valid,
     "cacheKey": cache_key, "regenerationKey": regen_key,
     "sameRecordDifferentDomain": cache_key.split(":")[1] != regen_key.split(":")[1],
     "keyConstructionReadsNoBytes": True,
     "hitAdmissionRequires": [
         "the stage spec retained and joined to THIS Plan",
         "the producing closure retained and Plan-selected",
         "every scopeIds member a retained subject-scope of this snapshot",
         "the output schema document retained",
         "every inputRefs entry resolved through x-opensip-digest-domains",
         "a bare coverage-payload/import-payload/fact-payload ref REFUSED as an "
         "authoritative root"],
     "aHitIsNeverEvidenceAuthority": True,
     "regenerationMismatch": {
         "code": "HOST.IO_FAILURE", "class": "operational-failed",
         "faultCause": "host-io", "exit": 4,
         "domainDetail": "evidence.regeneration-mismatch"}})

# --- B2. explicit test execution authorization ----------------------------
argv = ["node_modules/.bin/vitest", "run"]
argv_digest = osip.canonical_record_digest(argv)
test_grant = {
    "principalClass": "repository-code", "semanticPrincipalKind": "trusted-repository-code",
    "workflowSpelling": "P-TRUSTED-REPO", "executionClass": "test-runner",
    "projectId": G.PROJECT_ID, "snapshotId": SCN["snapshot"]["id"],
    "argvDigest": argv_digest, "owners": [],
    "ownerSourceDigest": osip.canonical_record_digest([]),
    "runner": "node_modules/.bin/vitest", "toolClosureId": SCN["provider"]["id"],
    "platformId": F.PLATFORM,
    "effects": {"subprocess": "DISCLOSURE-ONLY", "filesystemWrite": "DISCLOSURE-ONLY",
                "network": "DISCLOSURE-ONLY",
                "environment": "ENFORCED-BY-CONSTRUCTION"},
    "authorization": {"mode": "policy-record", "policyRecordId": "pr-1"},
    "ci": True, "expiry": "operation-end", "inherited": False}
truth = kit.doc("permtables")
rec("B2-test-execution-authorization", "positive",
    "opensip test run is admitted only through a security RepoExecutionGrantV2 with "
    "principal P-TRUSTED-REPO / execution class test-runner, bound to this project, "
    "snapshot digest and the EXACT argv digest, expiry operation-end, never "
    "inherited. A test-execution step has NO Plan; its observations enter an "
    "analysis only through an admitted import2 that retains the operational "
    "securityGrantRef. `test-code` is NOT a semantic-grant operation and a "
    "test-runner grant is projected by nothing.",
    {"grant": test_grant,
     "emptyOwnerSetDigest": osip.canonical_record_digest([]),
     "ciConsent": "policy-record (interactive-explicit refuses in CI: "
                  "TEST.INTERACTIVE_CONSENT_IN_CI)",
     "confinement": "DISCLOSED, never enforced; a claimed enforcement without a "
                    "measured platform primitive refuses TEST.CONFINEMENT_CLAIM_REFUSED",
     "semanticGrantOperations": ["read-source", "read-import", "native-analysis",
                                 "prepare-code"],
     "testCodeIsNotAnOperation": True,
     "truthTablePinned": kit.path_of("permtables")})

# --- B3. native preparation authorization and the prepared/Plan join -------
rec("B3-preparation-authorization", "positive",
    "AuthorizedExecutionV2 is a preparation PREFLIGHT descriptor, not a security "
    "admission result. The authority grant is the OPERATIONAL authorizationRef "
    "H('security.repo-execution-grant.v2', grant), excluded from the Plan descriptor "
    "and from every content identity; the Plan binds only the semantic projection.",
    {"principalSpellings": {
        "security S10 / AuthorizedExecutionV2.principalClass": "repository-code",
        "foundation semantic-grant principals[].kind": "trusted-repository-code",
        "workflow test-execution constant": "P-TRUSTED-REPO"},
     "grantOperationProjection": {
         "host-prepared": "prepare-code",
         "imported-inert": "read-import",
         "none": None},
     "authorizationRefInPlan": False,
     "preparedAvailabilityImpliesNoGrant":
         "a universe with preparedResolution=imported-inert projects only "
         "read-import; retained inert prepared bytes never imply an execution grant",
     "inertRowKinds": ["build-script-directives", "macro-expansion", "generated-file"],
     "refusedRowKinds": ["proc-macro-dylib", "build-script-binary"],
     "mediaTypeIsNotTrustProof":
         "a dylib relabelled text/x-rust-expansion is still a dylib row: "
         "native.prepared-output-not-inert, request-rejected exit 2"})


def _prepared_without_grant():
    """imported-inert must project read-import only; prepare-code refuses."""
    st = G.Store()
    scn = scen_ts.build(st, "ordinary")
    runner.assemble(scn, semantic_operations=("native-analysis", "read-source",
                                              "prepare-code"))
    raise G.Refusal(
        "PLAN.PROJECTED_PRINCIPAL_WITHOUT_GRANT",
        "prepare-code is present exactly when the Plan projects trusted-repository-"
        "code preparation principals; this Plan projects none, so the operation is "
        "unbacked")


neg("B3n-prepare-code-without-a-preparation-principal",
    "the semantic grant's prepare-code operation is present exactly when it projects "
    "trusted-repository-code preparation principals", _prepared_without_grant)

# --- B4. repair authorization chain ---------------------------------------
repair_plan_id = "repairplan2:" + hashlib.sha256(b"plan").hexdigest()
authz_ref = "security.repair-apply-authorization.v1:" + \
            hashlib.sha256(b"authorization").hexdigest()
apply_params = {"kind": "repair-apply", "planStep": 1,
                "repairPlanId": repair_plan_id, "consentSource": "policy",
                "authorizationRef": authz_ref}
kit.validate("invocation", "#/$defs/RepairApplyParams", apply_params)
rec("B4-repair-authorization", "positive",
    "repair apply is host-brokered FIRST-PARTY source mutation under the EXCLUSIVE "
    "lease: no repository code runs, so its authority is a separate security record "
    "(RepairApplyAuthorizationV1, repositoryExecution constant false), not a "
    "repository-execution grant. Preview requires an AUTHORITATIVE, retained, "
    "replayable evidence Run; a destructive unused-code recipe additionally requires "
    "native closed-world resolution evidence.",
    {"applyParams": apply_params,
     "consentMapping": {"interactive-explicit": "interactive",
                        "policy-record": "policy"},
     "preconditions": ["REPAIR.EVIDENCE_RUN_NOT_AUTHORITATIVE (ephemeral)",
                       "REPAIR.EVIDENCE_RUN_UNAVAILABLE (not retained/replayable)",
                       "REPAIR.RECIPE_TRUST_REVOKED / _NOT_ADMITTED",
                       "REPAIR.SOURCE_MOVED (live tree != Run snapshot)",
                       "REPAIR.EDIT_OUTSIDE_PERMITTED_SCOPE"],
     "journalStates": ["PREPARING", "STAGED", "APPLYING", "APPLIED", "COMMITTED"],
     "recoveryTable": {"PREPARING|STAGED": "discard-temps",
                       "APPLYING": "roll-back-renamed",
                       "APPLIED|INDETERMINATE": "verify-postimages-and-commit",
                       "COMMITTED|FAILED_*|RECOVERY_BLOCKED": "no mutation"},
     "rollbackDoesNotConsultRecipeTrust": True,
     "commitReConsultsRecipeTrust": True,
     "verifyAdmitsAFreshSnapshot":
         "verify never reuses the pre-apply Run; a differing fresh snapshot is "
         "REQUEST.PRECONDITION_FAILED / REPAIR.SOURCE_MOVED and seals no Run"})

# --- B5. replay after purge ------------------------------------------------
rec("B5-purge-and-replay", "positive",
    "a retention decision never changes a fact, Coverage, finding or Run identity, "
    "and never turns expired evidence into `no match`. Query of the retained "
    "manifest is allowed after purge and STATES evidence unavailable; a query "
    "requiring actual proof, a comparison baseline or a repair input refuses "
    "BEFORE evaluation.",
    {"sealedAssuranceImmutable": True,
     "availabilityStates": ["retained", "partial", "expired", "purged", "corrupt",
                            "unavailable"],
     "beforeEvaluation": {"class": "request-rejected",
                          "errorCode": "REQUEST.PRECONDITION_FAILED",
                          "details": ["evidence.expired", "evidence.purged",
                                      "evidence.missing", "evidence.corrupt"],
                          "exit": 2},
     "duringSelectedOperation": {"class": "operational-failed",
                                 "errorCode": "HOST.IO_FAILURE",
                                 "faultCause": "host-io", "exit": 4},
     "admittedPartialNativeInputs": {"class": "indeterminate", "exit": 3},
     "theseAreDifferentEventPositions": True,
     "purgedIsNotDeletedHistory": True,
     "replayableRetentionRequiredAtSealForTheDefaultProfile": True})


def _missing_witness_bytes():
    st = G.Store()
    scn = scen_ts.build(st, "ordinary")
    out = runner.assemble(scn)
    wd = out["proof"]["descriptor"]["predicateProofs"][0]["witnessDigest"]
    del st.objects[wd]
    G.close_run(st, out["run"], out["plan"], scn["snapshot"], out["seal"],
                out["evidence"], out["proof"], [out["view"]], scn["facts"],
                scn["coverages"], scn["scopes"], [scn["context"]], [scn["universe"]],
                scn["closures"], scn["retained"], out["cap"])


neg("B5n-missing-witness-bytes-is-retention-loss",
    "missing witness bytes is RETENTION LOSS (EvidenceUnavailable / HOST.IO_FAILURE "
    "host-io exit 4, detail evidence.missing), never a false predicate and never an "
    "admission rejection", _missing_witness_bytes)

if __name__ == "__main__":
    print(json.dumps(R, indent=1, ensure_ascii=False, default=str))
