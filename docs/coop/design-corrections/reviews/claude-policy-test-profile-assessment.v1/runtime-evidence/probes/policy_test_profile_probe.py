"""READ-ONLY owner probe: does the CURRENT evaluator3 policy.test route test a CURRENT PolicyDocumentV2 policy?

Loads the actual selected owners from --source (never writes there; run with -I -B) and records, per input:
schema admission (V1/V2 policy definitions, PolicyTestSuiteV1, evaluator3 EffectivePolicyRecordV1), owner policy
resolution (current v3 resolve_policy and the legacy resolver that run_policy_test actually binds), the selected suite
admission, the public route run_admitted_policy_test, and the grammar classifier.

A clearly labelled DIAGNOSTIC BYPASS calls the legacy run_policy_test directly on inputs the selected admission refuses.
It is NOT a product route. It is used only to observe which evaluator the route binds and whether V2-only atom members
change its behaviour. Probe-authored PolicyDocumentV2 documents are admitted independently by the V2 schema and the
v3 owner; nothing here claims or implements a V1<->V2 conversion.
Usage: policy_test_profile_probe.py --source SOURCE_ROOT --out OUT_JSON
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import traceback
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--source", required=True, type=Path)
ap.add_argument("--out", required=True, type=Path)
a = ap.parse_args()
D = a.source.resolve() / "docs/coop/design-corrections"
W = D / "workflows"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


WF3 = load("probe_workflows_model_v3", W / "workflows_model.v3.py")
LEG = WF3._base
P = WF3.projection_owner()
canonical = WF3.canonical

U3 = "urn:opensip:product-v1:workflows:evaluator3:"
V1DOC = "urn:opensip:product-v1:workflows:policy-document#/$defs/PolicyDocumentV1"
V2DOC = "urn:opensip:product-v1:policy-document:2#/$defs/PolicyDocumentV2"
SUITE_REF = "urn:opensip:product-v1:workflows:policy-test#/$defs/PolicyTestSuiteV1"
RESULT_REF = "urn:opensip:product-v1:workflows:policy-test#/$defs/PolicyTestResultV1"
CARRIER_REF = U3 + "command-envelope:3#/$defs/PolicyTestResultRecordV1"
EFFECTIVE_REF = U3 + "command-envelope:3#/$defs/EffectivePolicyRecordV1"


def validate(ref, value):
    try:
        P.validate_profile(ref, copy.deepcopy(value))
        return {"valid": True}
    except Exception as exc:  # ValidationError or canonical.AdmissionError
        return {"valid": False, "error": type(exc).__name__, "message": str(exc).splitlines()[0][:300]}


def attempt(fn):
    try:
        value = fn()
        return {"outcome": "RETURNED", "value": value}
    except WF3.Refusal as exc:
        row = {"outcome": "REFUSED", "errorCode": exc.error_code, "detail": exc.detail,
               "remedy": str(exc.remedy)[:400], "subject": exc.subject}
        try:
            term = exc.termination()
            row.update(terminationClass=term.get("class"), exitCode=WF3.exit_code(term),
                       domainDetail=(term.get("domainDetail") or {}).get("code"))
        except Exception as texc:
            row["terminationError"] = repr(texc)
        return row
    except Exception as exc:
        return {"outcome": "EXCEPTION", "type": type(exc).__name__, "message": str(exc)[:300],
                "trace": traceback.format_exc().splitlines()[-3:]}


def summarize_result(res):
    return {"resolverAccepted": res.get("resolverAccepted"), "resolverRefusals": [r.get("code") for r in res.get("resolverRefusals", [])],
            "candidatePolicyDigest": res.get("candidatePolicyDigest"), "policyTestResultId": res.get("policyTestResultId"),
            "summary": res.get("summary"),
            "results": [{"id": c["id"], "outcome": c["outcome"], "observedVerdict": c["observedVerdict"],
                         "findings": c["findings"], "indeterminateRules": c["indeterminateRules"],
                         "expectationOutcomes": c["expectationOutcomes"]} for c in res.get("results", [])],
            "resultSchema": validate(RESULT_REF, res),
            "carrierSchema": validate(CARRIER_REF, {"surface": "policy-test-result", "result": res})}


def route_row(fn):
    row = attempt(fn)
    if row["outcome"] == "RETURNED":
        res, refusal = row.pop("value")
        row["result"] = summarize_result(res)
        row["resolverRefusal"] = None if refusal is None else {"errorCode": refusal.error_code, "detail": refusal.detail}
    return row


# ------------------------------------------------------------------ source inputs (exact owner fixtures)
RAW = canonical.parse((W / "workflow-cases.v1.json").read_bytes())
C = dict(RAW["constants"])
C["ARGV"] = WF3.raw_sha(canonical.canonical(["scripts/test.sh", "--ci"]))
C["ARGV2"] = WF3.raw_sha(canonical.canonical(["/usr/bin/bash", "-c", "rm -rf ."]))
C["TOOL0#bin/node"] = C["TOOL0"] + "#bin/node"
C["ARGV4"] = WF3.raw_sha(canonical.canonical(["node", "test.js"]))
C["ARGV3"] = WF3.raw_sha(canonical.canonical(["bin/node", "test.js"]))


def sub(o):
    """Same substitution as check-workflow-projection.v3.py _r2_sub (check_workflows.v1.py sub)."""
    if isinstance(o, str) and o.startswith("$"):
        if o[1:] in C:
            return C[o[1:]]
        if o[1:] in RAW["policyDocs"]:
            return sub(RAW["policyDocs"][o[1:]])
        raise KeyError(o)
    if isinstance(o, dict):
        return {sub(k) if isinstance(k, str) and k.startswith("$") else k: sub(v) for k, v in o.items()}
    if isinstance(o, list):
        return [sub(v) for v in o]
    return o


SUITE_V1 = sub(RAW)["policySuite"]  # the exact suite the current checker routes through run_admitted_policy_test
BASE_V1 = copy.deepcopy(SUITE_V1["candidatePolicy"])
WAIVERS_EMPTY = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": []}

# Probe-authored PolicyDocumentV2 inputs (each independently admitted below; no conversion is claimed).
BASE_V2 = dict(copy.deepcopy(BASE_V1), schemaMajor=2)  # rules byte-identical to basePolicy; Rule defs are identical in both documents
CHECKER_V2 = {"schemaFamily": "opensip.product.policy", "schemaMajor": 2, "gateSeverityAtLeast": "error", "rules": [{
    "ruleId": "r", "ruleProgramRef": {"contributionId": "fixture", "ruleStableId": "r", "semanticsMajor": 2,
                                      "programDigest": hashlib.sha256(b"prog").hexdigest()},
    "enabled": True, "severity": "error", "gate": True, "subjectEnumeration": {"universe": "typescript", "subjectKind": "file"},
    "emitWhen": {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []}, "evidenceUse": []}]}  # check-workflow-projection.v3.py:129-150


def endpoint_policy(major, endpoint, relation="imports", rung="resolved-target"):
    atom = {"op": "exists", "relation": relation, "minResolution": rung, "filters": []}
    if endpoint is not None:
        atom["endpoint"] = endpoint
    return {"schemaFamily": "opensip.product.policy", "schemaMajor": major, "gateSeverityAtLeast": "warning", "rules": [{
        "ruleId": "incoming-import-exists",
        "ruleProgramRef": {"contributionId": "core.rules", "ruleStableId": "incoming-import-exists", "semanticsMajor": 1, "programDigest": "0" * 64},
        "enabled": True, "severity": "error", "gate": True,
        "subjectEnumeration": {"universe": "typescript-v2", "subjectKind": "file", "include": ["src/**"]},
        "emitWhen": atom, "evidenceUse": []}]}


ENDPOINT_TARGET_V2 = endpoint_policy(2, "target")
ENDPOINT_SOURCE_V2 = endpoint_policy(2, None)
ENDPOINT_TARGET_V1_KEY = endpoint_policy(1, "target")  # V1 major carrying the V2-only member: V1-law control
ENDPOINT_SOURCE_V1 = endpoint_policy(1, None)  # lawful V1 control with the same rule
FORBIDDEN_TARGET_V2 = endpoint_policy(2, "target", relation="file", rung="enumerated")  # registry file.endpointTarget=forbidden
TEST_FILTER_V2 = {"schemaFamily": "opensip.product.policy", "schemaMajor": 2, "gateSeverityAtLeast": "warning", "rules": [{
    "ruleId": "failed-test-exit1",
    "ruleProgramRef": {"contributionId": "core.rules", "ruleStableId": "failed-test-exit1", "semanticsMajor": 1, "programDigest": "0" * 64},
    "enabled": True, "severity": "error", "gate": True, "subjectEnumeration": {"universe": "typescript-v2", "subjectKind": "file"},
    "emitWhen": {"op": "exists", "relation": "test-execution", "minResolution": "observed",
                 "filters": [{"field": "testResult", "cmp": "eq", "value": "failed"}, {"field": "exitStatus", "cmp": "eq", "value": 1}],
                 "evidence": "test"},  # atom of foundation/check-atoms.v1.py:653-656
    "evidenceUse": [{"kind": "test", "requirement": "required"}]}]}

INCOMING_CASE = {"id": "incoming-import", "subject": {"kind": "facts", "subjects": ["src/a.ts", "src/b.ts"], "facts": [
    {"relation": "imports", "subject": "src/b.ts", "target": "src/a.ts", "resolution": "resolved-target", "universe": "typescript-v2",
     "confidenceMillionths": 1000000}], "coverage": "complete", "evidenceAvailable": []},
    "expectations": [{"kind": "finding", "ruleId": "incoming-import-exists", "minCount": 1, "subjects": ["src/a.ts"]}]}


def suite_with(policy, cases=None, waivers=None):
    s = copy.deepcopy(SUITE_V1)
    s["candidatePolicy"] = copy.deepcopy(policy)
    if cases is not None:
        s["cases"] = copy.deepcopy(cases)
        s["waivers"] = copy.deepcopy(waivers or WAIVERS_EMPTY)
        s.pop("overrides", None)
    return s


POLICIES = {
    "base-v1-owner-fixture": BASE_V1, "base-v2-probe": BASE_V2, "checker-v2-literal": CHECKER_V2,
    "endpoint-target-v2": ENDPOINT_TARGET_V2, "endpoint-source-v2": ENDPOINT_SOURCE_V2,
    "endpoint-target-v1-key": ENDPOINT_TARGET_V1_KEY, "endpoint-source-v1": ENDPOINT_SOURCE_V1,
    "forbidden-target-v2": FORBIDDEN_TARGET_V2, "test-filter-v2": TEST_FILTER_V2,
}
SUITES = {
    "control-v1-owner-suite": SUITE_V1,
    "base-v2-probe-suite": suite_with(BASE_V2),
    "checker-v2-literal-suite": suite_with(CHECKER_V2, [{"id": "no-file-fact", "subject": {"kind": "facts", "subjects": ["src/a.ts"], "facts": [],
                                                             "coverage": "complete", "evidenceAvailable": []},
                                                         "expectations": [{"kind": "finding", "ruleId": "r", "minCount": 1}]}]),
    # DISCRIMINATION ONLY, not a lawful conversion: the checker V2 literal with only schemaMajor changed, to show whether the
    # major const is the sole cause of the V2 suite refusal (policy-document.v2 x-opensip-profile-major-law forbids relabelling).
    "checker-literal-major1-DISCRIMINATION-ONLY-suite": suite_with(dict(CHECKER_V2, schemaMajor=1), [{"id": "no-file-fact", "subject": {"kind": "facts", "subjects": ["src/a.ts"], "facts": [],
                                                             "coverage": "complete", "evidenceAvailable": []},
                                                         "expectations": [{"kind": "finding", "ruleId": "r", "minCount": 1}]}]),
    "endpoint-target-v2-suite": suite_with(ENDPOINT_TARGET_V2, [INCOMING_CASE]),
    "endpoint-source-v2-suite": suite_with(ENDPOINT_SOURCE_V2, [INCOMING_CASE]),
    "endpoint-target-v1-key-suite": suite_with(ENDPOINT_TARGET_V1_KEY, [INCOMING_CASE]),
    "endpoint-source-v1-suite": suite_with(ENDPOINT_SOURCE_V1, [INCOMING_CASE]),
    "test-filter-v2-suite": suite_with(TEST_FILTER_V2, [{"id": "no-test-evidence", "subject": {"kind": "facts", "subjects": ["src/a.ts"], "facts": [],
                                                           "coverage": "complete", "evidenceAvailable": []},
                                                     "expectations": [{"kind": "indeterminate", "ruleId": "failed-test-exit1"}]}]),
}

report = {"standing": "READ-ONLY coauthor owner probe over the fixed captured source; not acceptance, not product qualification.",
          "source": str(a.source.resolve())}

# ------------------------------------------------------------------ owner bindings actually selected by the route
g = WF3.run_policy_test.__globals__
report["bindings"] = {
    "run_admitted_policy_test.definedIn": WF3.run_admitted_policy_test.__code__.co_filename,
    "run_policy_test.definedIn": WF3.run_policy_test.__code__.co_filename,
    "run_policy_test.isLegacyObject": WF3.run_policy_test is LEG.run_policy_test,
    "run_policy_test.globalsAreLegacyModule": g is vars(LEG),
    "run_policy_test.resolvesLegacyResolvePolicy": g["resolve_policy"] is LEG.resolve_policy,
    "run_policy_test.resolvesCurrentV3ResolvePolicy": g["resolve_policy"] is WF3.resolve_policy,
    "v3.resolve_policy.overridesLegacy": WF3.resolve_policy is not LEG.resolve_policy,
    "v3.admit_atom.overridesLegacy": WF3.admit_atom is not LEG.admit_atom,
    "run_policy_test.evaluate.isLegacy": g["evaluate"] is LEG.evaluate,
    "v3.definesOwnEvaluate": "evaluate" in WF3.__dict__ and WF3.__dict__["evaluate"] is not LEG.evaluate,
    "legacyEvalPredicateSourceMentionsEndpoint": "endpoint" in LEG.eval_pred.__code__.co_names + LEG.eval_pred.__code__.co_consts,
    "grammarClassifier.document$id": WF3._policy_grammar()["$id"],
    "grammarClassifier.rootDefinitionConstants": [c for c in WF3.policy_grammar_violation.__code__.co_consts if isinstance(c, str) and c.startswith("PolicyDocument")],
    "suiteAdmissionRef": WF3.POLICY_TEST_SUITE_REF,
}

# ------------------------------------------------------------------ policy documents
report["policies"] = {}
for name, pol in POLICIES.items():
    eff_waivers = WAIVERS_EMPTY
    effective_record = {"surface": "effective-policy", "policyDigest": WF3.doc_digest(pol), "policy": pol,
                        "waiverSetDigest": WF3.doc_digest(eff_waivers), "effectiveWaivers": eff_waivers,
                        "waiverResolution": {"asOfDate": "2026-09-12", "effectiveCount": 0, "expired": [], "duplicatesRejected": []}}
    v3 = attempt(lambda pol=pol: WF3.resolve_policy(copy.deepcopy(pol)))
    leg = attempt(lambda pol=pol: LEG.resolve_policy(copy.deepcopy(pol)))
    for row in (v3, leg):
        row.pop("value", None)
    report["policies"][name] = {"schemaMajor": pol["schemaMajor"], "policyDigest": WF3.doc_digest(pol),
                                "policyDocumentV2Schema": validate(V2DOC, pol), "policyDocumentV1Schema": validate(V1DOC, pol),
                                "evaluator3EffectivePolicyRecordV1": validate(EFFECTIVE_REF, effective_record),
                                "currentV3ResolvePolicy": v3, "legacyResolvePolicy": leg,
                                "grammarClassifierViolation": attempt(lambda pol=pol: WF3.policy_grammar_violation(copy.deepcopy(pol)))["value"]
                                if attempt(lambda pol=pol: WF3.policy_grammar_violation(copy.deepcopy(pol)))["outcome"] == "RETURNED" else "EXCEPTION"}

# ------------------------------------------------------------------ suites through the selected route
report["suites"] = {}
for name, suite in SUITES.items():
    adm = attempt(lambda suite=suite: WF3.admit_policy_test_suite(copy.deepcopy(suite)))
    adm.pop("value", None)
    report["suites"][name] = {
        "candidateSchemaMajor": suite["candidatePolicy"]["schemaMajor"],
        "suiteSchema": validate(SUITE_REF, suite),
        "selectedAdmission": adm,
        "publicRoute_run_admitted_policy_test": route_row(lambda suite=suite: WF3.run_admitted_policy_test(copy.deepcopy(suite))),
        "DIAGNOSTIC_BYPASS_legacy_run_policy_test_NOT_A_PRODUCT_ROUTE": route_row(lambda suite=suite: WF3.run_policy_test(copy.deepcopy(suite))),
    }

# ------------------------------------------------------------------ derived observations (computed, not asserted)
S = report["suites"]
byp = lambda n: S[n]["DIAGNOSTIC_BYPASS_legacy_run_policy_test_NOT_A_PRODUCT_ROUTE"].get("result", {})
report["observations"] = {
    "controlV1SuiteAdmittedAndCarried": S["control-v1-owner-suite"]["selectedAdmission"]["outcome"] == "RETURNED"
    and S["control-v1-owner-suite"]["publicRoute_run_admitted_policy_test"].get("result", {}).get("carrierSchema", {}).get("valid") is True,
    "everyV2CandidateRefusedAtSelectedAdmission": {n: (S[n]["selectedAdmission"]["outcome"], S[n]["selectedAdmission"].get("detail"))
                                                  for n in S if S[n]["candidateSchemaMajor"] == 2},
    "bypassBaseV2EqualsControlExceptDigests": (
        [ (c["id"], c["outcome"], c["findings"], c["indeterminateRules"], c["expectationOutcomes"]) for c in byp("base-v2-probe-suite").get("results", [])]
        == [ (c["id"], c["outcome"], c["findings"], c["indeterminateRules"], c["expectationOutcomes"]) for c in byp("control-v1-owner-suite").get("results", [])]),
    "bypassEndpointTargetFindingsEqualEndpointSourceFindings": (
        [c["findings"] for c in byp("endpoint-target-v2-suite").get("results", [])]
        == [c["findings"] for c in byp("endpoint-source-v2-suite").get("results", [])]),
    "bypassEndpointTargetResults": byp("endpoint-target-v2-suite").get("results"),
    "forbiddenTargetEndpoint": {"currentV3ResolvePolicy": report["policies"]["forbidden-target-v2"]["currentV3ResolvePolicy"],
                                "legacyResolvePolicy": report["policies"]["forbidden-target-v2"]["legacyResolvePolicy"]},
}

a.out.parent.mkdir(parents=True, exist_ok=True)
a.out.write_text(json.dumps(report, indent=1, sort_keys=False, default=str) + "\n")
print(json.dumps({"bindings": report["bindings"], "observations": report["observations"],
                  "suites": {n: {"admission": (v["selectedAdmission"]["outcome"], v["selectedAdmission"].get("detail")),
                                 "route": v["publicRoute_run_admitted_policy_test"]["outcome"],
                                 "bypass": v["DIAGNOSTIC_BYPASS_legacy_run_policy_test_NOT_A_PRODUCT_ROUTE"]["outcome"]} for n, v in S.items()},
                  "policies": {n: {"v2": v["policyDocumentV2Schema"]["valid"], "v1": v["policyDocumentV1Schema"]["valid"],
                                   "effectiveRecord": v["evaluator3EffectivePolicyRecordV1"]["valid"],
                                   "v3resolve": (v["currentV3ResolvePolicy"]["outcome"], v["currentV3ResolvePolicy"].get("detail")),
                                   "legacyResolve": (v["legacyResolvePolicy"]["outcome"], v["legacyResolvePolicy"].get("detail")),
                                   "grammarViolation": v["grammarClassifierViolation"]} for n, v in report["policies"].items()}},
                 indent=1, default=str))
