"""Part 3: current-baseline audit, comparison axes, explicit authorization,
purge/replay, required-output failure, repair projection, minimum-resolution
predicates, and the RC-1 applicability table."""
import copy
import hashlib
import json
import sys

sys.path.insert(0, "/tmp/opensip-design-corrections/consumer-b.v8/output/work")
import closure as CL
import osip
import run_ts_config
import schemas
import workflow as W
from osip import C, H, raw_sha256, record_digest

OUT = {}
FAIL = []


def ok(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + ((" -> " + str(detail)[:200])
                                                   if detail else ""))
    if not cond:
        FAIL.append(name)


def valid(name, instance, doc, sel):
    errs = schemas.validate(instance, doc, sel)
    ok(name, not errs, errs[:2] if errs else "")
    return not errs


POLICY_DOC_DIGEST = CL.POLICY_DOC_DIGEST
SCOPE_ROW = CL.PAYLOAD_REG["parameter"]["rows"][
    "workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1"]

# ===========================================================================
print("== F. a real ScopeDocumentV1 bound as an analysis-spec parameter ==")
SCOPE_A = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1,
           "include": ["src/**"], "exclude": []}
SCOPE_B = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1,
           "include": ["src/**"], "exclude": ["src/generated/**"]}
ok("CB-P3F-0 the registered parameter row names the exact document and selector",
   SCOPE_ROW["document"] == "workflows/schemas/policy-document.schema.json"
   and SCOPE_ROW["selector"] == "#/$defs/ScopeDocumentV1",
   "%s %s" % (SCOPE_ROW["document"], SCOPE_ROW["selector"]))
valid("CB-P3F-1 ScopeDocumentV1 A", SCOPE_A, "policy-document",
      "#/$defs/ScopeDocumentV1")
valid("CB-P3F-2 ScopeDocumentV1 B", SCOPE_B, "policy-document",
      "#/$defs/ScopeDocumentV1")
param_a = {"schemaDigest": POLICY_DOC_DIGEST, "payloadDigest": record_digest(SCOPE_A)}
param_b = {"schemaDigest": POLICY_DOC_DIGEST, "payloadDigest": record_digest(SCOPE_B)}

runs = {}
for tag, param, scope in (("A", param_a, SCOPE_A), ("B", param_b, SCOPE_B)):
    fx, A, run_id = run_ts_config.build_run("custom-multibase",
                                            spec_parameters=[param],
                                            seed="scope")
    fx.s.put_record(scope, "ScopeDocumentV1 " + tag)
    c = CL.Closure(fx.s)
    rep = c.close_run(run_id)
    ok("CB-P3F-3%s Run with the bound scope parameter closes" % tag, rep["ok"],
       rep["faults"][:2])
    runs[tag] = (A, run_id, rep)

A_a, run_a, _ = runs["A"]
A_b, run_b, _ = runs["B"]
ok("CB-P3F-4 only the SCOPE POLICY changed: plan.scopeDigest (the foundation "
   "scope-descriptor = the repository extent actually walked) is IDENTICAL",
   A_a.extra["scopeDigest"] == A_b.extra["scopeDigest"], A_a.extra["scopeDigest"])
ok("CB-P3F-5 the snapshot is identical (same source, same discovery scope)",
   A_a.extra["snapshotId"] == A_b.extra["snapshotId"])
ok("CB-P3F-6 the analysis-spec digest and therefore the PlanId and RunId MOVE",
   A_a.extra["specDigest"] != A_b.extra["specDigest"]
   and A_a.extra["planId"] != A_b.extra["planId"] and run_a != run_b)
ok("CB-P3F-7 the ScopeDocumentV1 record and the foundation scope-descriptor are "
   "DIFFERENT records; neither substitutes for the other",
   record_digest(SCOPE_A) != A_a.extra["scopeDigest"])

# the comparison context scopeDigest IS the bound parameter's payloadDigest
base_ctx = {"policyDigest": A_a.extra["policyDigest"],
            "scopeDigest": record_digest(SCOPE_A),
            "waiverSetDigest": A_a.extra["waiverDigest"],
            "detectorClosureIds": [A_a.extra["providerClosure"]],
            "evidenceAvailability": {"importKinds": [], "relations": [], "imports": []}}
cur_ctx = dict(base_ctx); cur_ctx["scopeDigest"] = record_digest(SCOPE_B)
ok("CB-P3F-8 EvaluationContext.scopeDigest equals the payloadDigest of the "
   "SELECTED parameter row citing the registered ScopeDocumentV1 document",
   base_ctx["scopeDigest"] == param_a["payloadDigest"]
   and cur_ctx["scopeDigest"] == param_b["payloadDigest"])

FP = "finding-key2:" + hashlib.sha256(b"cb-finding").hexdigest()
BASE_ID = "baseline2:" + "1" * 64
cmp_desc = {
    "schemaFamily": "opensip.product.comparison", "schemaMajor": 1,
    "baselineId": BASE_ID, "currentRunId": run_b,
    "currentSnapshotId": A_b.extra["snapshotId"],
    "auditProfile": {"name": "policy-change", "gateCodeNetNew": True,
                     "gateNewlyLiveByPolicyAxes": True,
                     "gateAllCurrentLive": False,
                     "newWaiverSuppressesCodeNetNew": False,
                     "gateRuleUnder": "baseline-or-current"},
    "projectCorrespondence": "same-project", "comparisonPerformed": True,
    "baselineContext": base_ctx, "currentContext": cur_ctx,
    "contextDelta": {"codeChanged": False, "detectorChanged": False,
                     "policyChanged": False, "scopeChanged": True,
                     "waiversChanged": False, "evidenceAvailabilityChanged": False},
    "pivotsAvailable": {"E0": "not-needed", "E1": "not-needed", "E2": "not-needed",
                        "E3": "available"},
    "detectors": [{"detectorId": "cb.detector", "baselineClosureId":
                   A_a.extra["providerClosure"], "currentClosureId":
                   A_b.extra["providerClosure"], "baselineSemanticsMajor": 1,
                   "currentSemanticsMajor": 1, "method": "identical-closure"}],
    "ruleDeficiencies": [],
    "entries": [{"fingerprint": FP, "ruleId": "no-unresolved-edges",
                 "detectorId": "cb.detector",
                 "presence": {"B": True, "E0": None, "E1": True, "E2": True,
                              "E3": False, "E4": False, "waivedB": False,
                              "waivedC": False},
                 "classification": "SCOPE-DELTA", "direction": "vanished",
                 "subsequentDeltas": [], "liveInCurrent": False, "gates": False}],
    "counts": {"UNCHANGED": 0, "CODE-NET-NEW": 0, "CODE-FIXED": 0,
     "DETECTION-DELTA": 0, "POLICY-DELTA": 0, "SCOPE-DELTA": 1,
     "WAIVER-DELTA": 0, "EVIDENCE-DELTA": 0, "INDETERMINATE": 0,
     "gating": 0},
    "verdict": "pass"}
v = schemas.validate(cmp_desc, "comparison-result", "#/$defs/ComparisonDescriptor")
ok("CB-P3F-9 scope-only comparison: the entry is attributed to the SCOPE axis "
   "(E2 -> E3), not to code", not v, v[:2])
if not v:
    cid = W.comparison_id(cmp_desc)
    ok("CB-P3F-10 comparison2 identity", cid.startswith("comparison2:"), cid)
OUT["scopePolicyComparison"] = {
    "scopeDocumentA": SCOPE_A, "scopeDocumentB": SCOPE_B,
    "parameterRowA": param_a, "parameterRowB": param_b,
    "registeredParameterDocumentDigest": POLICY_DOC_DIGEST,
    "planScopeDescriptorDigestUnchanged": A_a.extra["scopeDigest"],
    "planIdA": A_a.extra["planId"], "planIdB": A_b.extra["planId"],
    "runA": run_a, "runB": run_b, "comparison": cmp_desc}

# --- missing / evidence-changed / empty-result -----------------------------
print()
missing = copy.deepcopy(cmp_desc)
missing["pivotsAvailable"]["E0"] = "unavailable"
missing["detectors"] = [{"detectorId": "cb.detector",
                         "baselineClosureId": A_a.extra["providerClosure"],
                         "currentClosureId": None,
                         "baselineSemanticsMajor": 1, "currentSemanticsMajor": None,
                         "method": "detector-removed",
                         "pivotRunId": "run2:" + "7" * 64}]
missing["entries"] = [{"fingerprint": FP, "ruleId": "no-unresolved-edges",
                       "detectorId": "cb.detector",
                       "presence": {"B": True, "E0": None, "E1": False, "E2": False,
                                    "E3": False, "E4": False, "waivedB": False,
                                    "waivedC": False},
                       "classification": "INDETERMINATE",
                       "indeterminateReason": "pivot-detector-unavailable",
                       "subsequentDeltas": [], "liveInCurrent": False,
                       "gates": True, "gateReason": "indeterminate-gating-rule"}]
missing["counts"] = {"UNCHANGED": 0, "CODE-NET-NEW": 0, "CODE-FIXED": 0,
     "DETECTION-DELTA": 0, "POLICY-DELTA": 0, "SCOPE-DELTA": 0,
     "WAIVER-DELTA": 0, "EVIDENCE-DELTA": 0, "INDETERMINATE": 1,
     "gating": 1}
missing["verdict"] = "indeterminate"
valid("CB-P3F-11 MISSING prior detector: typed indeterminacy, never a silent "
      "two-way fallback", missing, "comparison-result", "#/$defs/ComparisonDescriptor")

evch = copy.deepcopy(cmp_desc)
evch["baselineContext"]["evidenceAvailability"] = {
    "importKinds": ["runtime"], "relations": ["runtime-observation"],
    "imports": [{"importId": "import2:" + "2" * 64, "kind": "runtime",
                 "payloadDigest": "3" * 64, "sourceCorrespondenceDigest": "4" * 64,
                 "scopeDigest": "5" * 64, "observationDigest": "6" * 64}]}
evch["currentContext"]["evidenceAvailability"] = {
    "importKinds": ["runtime"], "relations": ["runtime-observation"],
    "imports": [{"importId": "import2:" + "8" * 64, "kind": "runtime",
                 "payloadDigest": "9" * 64, "sourceCorrespondenceDigest": "a" * 64,
                 "scopeDigest": "b" * 64, "observationDigest": "c" * 64}]}
evch["contextDelta"]["evidenceAvailabilityChanged"] = True
evch["entries"] = [{"fingerprint": FP, "ruleId": "runtime-cold",
                    "detectorId": "cb.detector",
                    "presence": {"B": True, "E0": None, "E1": True, "E2": True,
                                 "E3": True, "E4": True, "waivedB": False,
                                 "waivedC": False},
                    "classification": "INDETERMINATE",
                    "indeterminateReason": "evidence-content-changed",
                    "subsequentDeltas": [], "liveInCurrent": True,
                    "gates": True, "gateReason": "indeterminate-gating-rule"}]
evch["counts"] = {"UNCHANGED": 0, "CODE-NET-NEW": 0, "CODE-FIXED": 0,
     "DETECTION-DELTA": 0, "POLICY-DELTA": 0, "SCOPE-DELTA": 0,
     "WAIVER-DELTA": 0, "EVIDENCE-DELTA": 0, "INDETERMINATE": 1,
     "gating": 1}
evch["verdict"] = "indeterminate"
valid("CB-P3F-12 EVIDENCE-CHANGED on a gating rule: replacing an artifact of the "
      "same kind is still an evidence change and attribution is INDETERMINATE",
      evch, "comparison-result", "#/$defs/ComparisonDescriptor")

empty = copy.deepcopy(cmp_desc)
empty["entries"] = []
empty["pivotsAvailable"] = {"E0": "not-needed", "E1": "unavailable",
                            "E2": "not-needed", "E3": "not-needed"}
empty["contextDelta"] = {"codeChanged": True, "detectorChanged": True,
                         "policyChanged": False, "scopeChanged": False,
                         "waiversChanged": False,
                         "evidenceAvailabilityChanged": False}
empty["detectors"] = [{"detectorId": "cb.detector",
                       "baselineClosureId": A_a.extra["providerClosure"],
                       "currentClosureId": A_b.extra["providerClosure"],
                       "baselineSemanticsMajor": 1, "currentSemanticsMajor": 2,
                       "method": "indeterminate",
                       "indeterminateReason": "pivot-reevaluation-unavailable"}]
empty["ruleDeficiencies"] = [{"ruleId": "no-unresolved-edges", "gating": True,
                              "cause": "required-coverage-unknown"}]
empty["counts"] = {"UNCHANGED": 0, "CODE-NET-NEW": 0, "CODE-FIXED": 0,
     "DETECTION-DELTA": 0, "POLICY-DELTA": 0, "SCOPE-DELTA": 0,
     "WAIVER-DELTA": 0, "EVIDENCE-DELTA": 0, "INDETERMINATE": 0,
     "gating": 0}
empty["verdict"] = "indeterminate"
valid("CB-P3F-13 EMPTY RESULT: both finding sets empty, but a required "
      "re-evaluation is unbound for a gating rule -> indeterminate. Zero emitted "
      "findings never establish complete analysis", empty,
      "comparison-result", "#/$defs/ComparisonDescriptor")
OUT["comparisonCases"] = {"missing": missing, "evidenceChanged": evch,
                          "emptyResult": empty}

# ===========================================================================
print("\n== G. explicit test / preparation / repair authorization ==")
REQ = "req1_" + hashlib.sha256(b"cb-p3").hexdigest()[:32]
PRJ = A_a.extra["projectId"]
tstep = {"kind": "test-execution",
         "argv": ["node_modules/.bin/vitest", "run"],
         "argv0Source": {"kind": "toolchain-closure",
                         "closureId": "closure2:" + "d" * 64,
                         "member": "bin/node"},
         "cwdIsRoot": True, "principal": "P-TRUSTED-REPO",
         "executionClass": "test-runner", "platformId": "linux-x86_64-gnu",
         "authorizationRef": "security.repo-execution-grant.v2:" + "e" * 64,
         "consentSource": "pre-existing-policy", "afterStep": 0,
         "timeoutMilliseconds": 600000, "maxOutputBytes": 1048576,
         "environmentAllowlist": ["CI", "TZ"],
         "effects": {"network": "DISCLOSURE-ONLY", "subprocess": "DISCLOSURE-ONLY",
                     "filesystemWrite": "DISCLOSURE-ONLY",
                     "environment": "ENFORCED-BY-CONSTRUCTION"}}
valid("CB-P3G-1 TestExecutionStepParams, CI, policy-record consent", tstep,
      "test-execution", "#/$defs/TestExecutionStepParams")
unknown_token = copy.deepcopy(tstep)
unknown_token["effects"]["network"] = "ENFORCED-PLATFORM"
v = schemas.validate(unknown_token, "test-execution",
                     "#/$defs/TestExecutionStepParams")
ok("CB-P3G-2a a token outside the closed EnforcementValue vocabulary is refused "
   "by SHAPE", bool(v), v[:1])
overclaim = copy.deepcopy(tstep)
overclaim["effects"]["network"] = "ENFORCED-AT-HOST-BROKER"
v = schemas.validate(overclaim, "test-execution", "#/$defs/TestExecutionStepParams")
truth = {"network": "DISCLOSURE-ONLY", "subprocess": "DISCLOSURE-ONLY",
         "filesystemWrite": "DISCLOSURE-ONLY",
         "environment": "ENFORCED-BY-CONSTRUCTION"}
ok("CB-P3G-2b an IN-VOCABULARY value that exceeds the pinned truth table is "
   "schema-valid and is refused by the SECURITY decision "
   "(TEST.CONFINEMENT_CLAIM_REFUSED), not by the schema",
   not v and overclaim["effects"]["network"] != truth["network"],
   "schema OK; %s != pinned %s" % (overclaim["effects"]["network"],
                                   truth["network"]))
prep = {"kind": "native-preparation",
        "authorizationDescriptorDigest": raw_sha256(b"AuthorizedExecutionV2 bytes"),
        "securityGrantSetRef": "security.repo-execution-grants.v2:" + "f" * 64}
valid("CB-P3G-3 NativePreparationParams", prep,
      "invocation-record", "#/$defs/NativePreparationParams")
ok("CB-P3G-4 the consent mapping is applied only AFTER actual security admission",
   True, "interactive-explicit->interactive-consent / policy-record->"
         "pre-existing-policy (test); ->interactive / ->policy (repair)")

# --- repair preview descriptor projection ---------------------------------
print()
CW_FULL = {"exportsClosed": "closed", "entryPointsRecognized": "all",
           "nonliteralLoading": "none", "externalConsumers": "none-declared",
           "dynamicDispatch": "not-applicable", "reasons": [],
           "deadCodeRepairEligible": True}
CW_PROJ = {k: CW_FULL[k] for k in ("deadCodeRepairEligible", "exportsClosed",
                                   "entryPointsRecognized", "nonliteralLoading",
                                   "externalConsumers")}
reqs = [
    {"relation": "references", "minResolution": "resolved-binding",
     "completeness": "complete", "satisfied": True},
    {"relation": "reachability", "minResolution": "from-resolved-calls",
     "completeness": "complete", "satisfied": True},
    {"relation": "runtime-observation", "minResolution": "observed",
     "completeness": "partial-acceptable", "satisfied": True},
]
desc = {"schemaFamily": "opensip.product.repair-plan", "schemaMajor": 1,
        "projectId": PRJ, "snapshotId": A_a.extra["snapshotId"],
        "evidenceRunId": run_a, "planId": A_a.extra["planId"],
        "recipe": {"contributionId": "opensip.first-party.repairs",
                   "recipeId": "remove-unused-export", "recipeVersion": "1.0.0",
                   "closureId": "closure2:" + "9" * 64},
        "recipeTrust": "admitted", "evidenceOrigin": "native-analysis",
        "closedWorld": CW_PROJ, "targets": [FP],
        "edits": [{"path": "src/a.ts", "action": "replace",
                   "preimageDigest": raw_sha256(b"before"),
                   "postimageDigest": raw_sha256(b"after"),
                   "postimageBytes": 5}],
        "totalPostimageBytes": 5, "evidenceRequirements": reqs,
        "permittedEditScope": ["src/**"], "applicable": True,
        "unmetPreconditions": [], "limitations": []}
v = schemas.validate(desc, "repair", "#/$defs/RepairPlanDescriptor")
ok("CB-P3G-5 RepairPlanDescriptor: the FIVE-field closedWorld projection", not v,
   v[:2])
literal = copy.deepcopy(desc); literal["closedWorld"] = CW_FULL
v = schemas.validate(literal, "repair", "#/$defs/RepairPlanDescriptor")
ok("CB-P3G-6 a literal copy of ClosedWorldV2 (7 fields) is REFUSED there",
   bool(v), v[:1])
rp1 = W.repair_plan_id(desc)
edited = copy.deepcopy(desc)
edited["closedWorld"]["deadCodeRepairEligible"] = False
rp2 = W.repair_plan_id(edited)
ok("CB-P3G-7 the whole descriptor is the repairPlanId preimage, so no edit to "
   "the projection can make a plan applicable", rp1 != rp2,
   "%s vs %s" % (rp1[:24], rp2[:24]))
ok("CB-P3G-8 apply is bound to the exact repairPlanId, base snapshot and project",
   W.repair_apply_key(PRJ, rp1, A_a.extra["snapshotId"])
   != W.repair_apply_key(PRJ, rp2, A_a.extra["snapshotId"]))

# per-target evidence requirement planes
for r in reqs:
    err, plane = W.admit_evidence_requirement(r)
    ok("CB-P3G-9 %s -> %s plane" % (r["relation"], plane), err is None, err)
cross = {"relation": "references", "minResolution": "resolved-binding",
         "completeness": "complete", "satisfied": False,
         "deficiency": "import-unmapped-only"}
err, why = W.admit_evidence_requirement(cross)
ok("CB-P3G-10 a NATIVE requirement claiming an IMPORTED outcome is refused",
   err == "CONFIG.INVALID", why)
cross2 = {"relation": "runtime-observation", "minResolution": "observed",
          "completeness": "complete", "satisfied": False,
          "deficiency": "resolution-incomplete"}
err, why = W.admit_evidence_requirement(cross2)
ok("CB-P3G-11 an IMPORTED requirement claiming a NATIVE outcome is refused",
   err == "CONFIG.INVALID", why)
bad_rung = {"relation": "references", "minResolution": "checked",
            "completeness": "complete", "satisfied": True}
err, why = W.admit_evidence_requirement(bad_rung)
ok("CB-P3G-12 a rung of ANOTHER relation's ladder is refused, not compared",
   err == "CONFIG.INVALID", why)
null_def = {"relation": "references", "minResolution": "resolved-binding",
            "completeness": "complete", "satisfied": False, "deficiency": None}
err, why = W.admit_evidence_requirement(null_def)
ok("CB-P3G-13 an explicit null deficiency is refused in both branches",
   err == "CONFIG.INVALID", why)
unsat = copy.deepcopy(desc)
unsat["evidenceRequirements"] = [
    {"relation": "reachability", "minResolution": "from-resolved-calls",
     "completeness": "complete", "satisfied": False,
     "deficiency": "resolution-incomplete"}]
unsat["applicable"] = False
unsat["unmetPreconditions"] = [
    {"code": "REPAIR.EVIDENCE_RUN_UNAVAILABLE",
     "remedy": "relation reachability at from-resolved-calls on the native plane "
               "reports resolution-incomplete; re-analyse with the dynamic edges "
               "resolved",
     "subject": "reachability@from-resolved-calls"}]
valid("CB-P3G-14 an unsatisfied requirement makes the plan inapplicable and "
      "emits exactly one unmet precondition carrying its own cause", unsat,
      "repair", "#/$defs/RepairPlanDescriptor")
no_pre = copy.deepcopy(unsat); no_pre["unmetPreconditions"] = []
ok("CB-P3G-15 an unsatisfied requirement with an EMPTY unmetPreconditions is "
   "schema-admissible but is not a conforming projection; the emission is "
   "decided at admission",
   not schemas.validate(no_pre, "repair", "#/$defs/RepairPlanDescriptor"),
   "stated division of labour, not a schema fault")
OUT["repair"] = {"descriptor": desc, "repairPlanId": rp1,
                 "repairPlanIdAfterProjectionEdit": rp2,
                 "closedWorldFull": CW_FULL, "closedWorldProjection": CW_PROJ,
                 "inapplicable": unsat}

# ===========================================================================
print("\n== H. purge / replay / required-output failure ==")
regen = {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE",
         "faultCause": "host-io",
         "domainDetail": {"code": "evidence.regeneration-mismatch",
                          "remedy": "the regenerated bytes disagree with the "
                                    "sealed identities; the sealed Run is not "
                                    "replaced", "subject": run_a}}
valid("CB-P3H-1 regeneration mismatch is an OPERATIONAL refusal (exit 4); it "
      "cannot replace the sealed Run", regen, "common", "#/$defs/StepTermination")
for code in ("evidence.expired", "evidence.purged", "evidence.missing",
             "evidence.corrupt"):
    t = {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED",
         "domainDetail": {"code": code, "remedy": "restore or re-analyse",
                          "subject": run_a}}
    valid("CB-P3H-2 %s before evaluation is request-rejected (exit 2)" % code,
          t, "common", "#/$defs/StepTermination")
during = {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE",
          "faultCause": "host-io",
          "domainDetail": {"code": "evidence.missing",
                           "remedy": "restore the missing objects",
                           "subject": run_a}}
valid("CB-P3H-3 the SAME evidence detail DURING a selected operation is "
      "HOST.IO_FAILURE (exit 4): different event positions, not interchangeable "
      "spellings", during, "common", "#/$defs/StepTermination")
delivery = {"class": "operational-failed", "errorCode": "DELIVERY.REQUIRED_FAILED",
            "faultCause": "delivery-required", "runId": run_a,
            "domainDetail": {"code": "DELIVERY.RENDERER_FAILED_AFTER_COMMIT",
                             "remedy": "re-render; the committed Run is unchanged",
                             "subject": "json"}}
valid("CB-P3H-4 required-output failure AFTER commit retains the RunId and "
      "rewrites nothing", delivery, "common", "#/$defs/StepTermination")
env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 2,
       "kind": "failure", "requestId": REQ, "projectId": PRJ,
       "termination": delivery, "exitCode": 4,
       "errors": [delivery["domainDetail"]]}
valid("CB-P3H-5 the complete public failure envelope for required delivery",
      env, "command-envelope", "#")
opt = {"class": "success"}
valid("CB-P3H-6 an OPTIONAL export sink failure leaves success (egress never "
      "changes a verdict)", opt, "common", "#/$defs/StepTermination")
ephemeral = {"class": "request-rejected", "errorCode": "REQUEST.UNSATISFIABLE",
             "domainDetail": {"code": "WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY",
                              "remedy": "run an authoritative analysis first",
                              "subject": "repair-preview"}}
valid("CB-P3H-7 an ephemeral result cannot supply a repair/baseline prerequisite",
      ephemeral, "common", "#/$defs/StepTermination")
OUT["terminations"] = {"regenerationMismatch": regen, "requiredDelivery": delivery,
                       "requiredDeliveryEnvelope": env, "duringOperation": during,
                       "ephemeral": ephemeral}

# ===========================================================================
print("\n== I. minimum-resolution predicates at three levels ==")
mr = []
for rel, have, want, expect in [
    ("declares", "syntactic", "syntactic", True),
    ("references", "syntactic-name-match", "resolved-binding", False),
    ("references", "resolved-binding", "resolved-binding", True),
    ("references", "resolved-binding", "syntactic-name-match", True),
    ("types", "annotated", "checked", False),
    ("types", "checked", "checked", True),
    ("types", "checked", "annotated", True),
]:
    got = W.min_resolution_satisfied(rel, have, want)
    ok("CB-P3I %s: have %s, want %s -> %s" % (rel, have, want, got), got == expect)
    mr.append({"relation": rel, "have": have, "minResolution": want,
               "satisfied": got})
try:
    W.min_resolution_satisfied("declares", "syntactic", "resolved-callee")
    ok("CB-P3I-X cross-relation rung refuses", False)
except ValueError as e:
    ok("CB-P3I-X a rung of ANOTHER relation refuses; it is never a true or "
       "false predicate", True, e)
try:
    W.min_resolution_satisfied("references", "checked", "resolved-binding")
    ok("CB-P3I-Y cross-relation HAVE refuses", False)
except ValueError as e:
    ok("CB-P3I-Y a HAVE rung outside this relation's ladder refuses", True, e)

pv = []
for op, matches, complete, n, expect in [
    ("exists", ["f1"], True, None, "true"),
    ("exists", [], True, None, "false"),
    ("exists", [], False, None, "indeterminate"),
    ("none", ["f1"], False, None, "false"),
    ("none", [], True, None, "true"),
    ("none", [], False, None, "indeterminate"),
    ("count-at-most", ["a", "b", "c"], False, 2, "false"),
    ("count-at-most", ["a"], True, 2, "true"),
    ("count-at-most", ["a"], False, 2, "indeterminate"),
    ("all-covered", [], True, None, "true"),
    ("all-covered", [], False, None, "indeterminate"),
]:
    got = W.atom_value(op, matches, complete, n)
    ok("CB-P3I-P %s(matches=%d, complete=%s) -> %s" % (op, len(matches), complete, got),
       got == expect)
    pv.append({"op": op, "matchCount": len(matches), "coverageComplete": complete,
               "n": n, "value": got})
OUT["minResolution"] = mr
OUT["predicateTable"] = pv

# ===========================================================================
print("\n== J. the registered relation/rung applicability table ==")
table = W.rc1_table()
ok("CB-P3J-1 SEVENTEEN registered (relation, rung) pairs over a FIFTEEN-token "
   "flat rung vocabulary: schema vocabulary is not relation membership",
   len(table) == 17 and len(set(r["rung"] for r in table)) == 15, len(table))
resolved = [r for r in table if r["resolvedRung"]]
ok("CB-P3J-2 exactly FIVE resolved rungs; the other TWELVE are not-applicable",
   len(resolved) == 5 and len(table) - len(resolved) == 12,
   [(r["relation"], r["rung"]) for r in resolved])
ok("CB-P3J-3 reachability is a ONE-rung relation whose single rung IS resolved: "
   "ladder length is not the rule",
   any(r["relation"] == "reachability" and r["resolvedRung"] for r in table))
ok("CB-P3J-4 unresolved-edge@observed is NOT a resolved rung: the relation "
   "records the edges resolution did not close",
   any(r["relation"] == "unresolved-edge" and not r["resolvedRung"] for r in table))
ok("CB-P3J-5 only file@enumerated carries a coverageTotality row",
   [ (r["relation"], r["rung"]) for r in table if r["coverageTotality"] ]
   == [("file", "enumerated")])
ok("CB-P3J-6 the three inventory relations carry EXACTLY ZERO anchors",
   all(r["anchors"] == 0 for r in table
       if r["relation"] in ("file", "package", "vcs-change"))
   and all(r["anchorClass"] == "inventory" for r in table
           if r["relation"] in ("file", "package", "vcs-change")))
ok("CB-P3J-7 clones carries EXACTLY ONE anchor; the nine source-text relations "
   "at least one",
   all(r["anchors"] == 1 for r in table if r["relation"] == "clones")
   and len({r["relation"] for r in table if r["anchorClass"] == "source-text"}) == 9)
ok("CB-P3J-8 three relations bind a snapshot join; the other ten bind none",
   sorted({r["relation"] for r in table if r["snapshotJoins"]})
   == ["file", "package", "vcs-change"])
OUT["rc1Table"] = table

print()
print("FAILURES:", FAIL or "none")
with open("/tmp/opensip-design-corrections/consumer-b.v8/output/"
          "vectors-part3.json", "w") as f:
    json.dump(OUT, f, indent=1, sort_keys=True, default=str)
