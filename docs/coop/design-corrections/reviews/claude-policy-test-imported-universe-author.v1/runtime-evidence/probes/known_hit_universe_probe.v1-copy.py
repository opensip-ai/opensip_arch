"""Bounded fixture-vs-composition known-hit comparison and policy-universe controls (READ-ONLY over --source; -I -B).

K: for each discriminating scenario, the SAME logical rule is evaluated
   (a) by the public policy.test route workflows_model.v3.run_admitted_policy_test over an authored PolicyTestSuiteV2
       facts fixture, and
   (b) by the evaluator composition owner evaluator_composition_model.v3.compose with a scanner returning the atom values
       that fixture represents (native `exists file enumerated`: true = fact present, false = absent under complete
       Coverage, unknown = absent under partial Coverage with a blocking native cause; imported `exists test-execution`
       with required/optional declared evidence absent: indeterminate with an `evidence-kind-unavailable` import cause and
       the §9.5 required-evidence deficiency when required).
   Compared: sealed verdict (fixture `advisory` is the derived display of composition `pass`), finding subjects, waived
   subjects, and whether the rule is unknown (fixture `indeterminateRules` vs composition required-evidence rows or an
   indeterminate root with a §5 blocking cause). BOUNDED COMPOSITION ONLY, exactly like check-composition.v3: synthesized
   population/Plan/closure locators, no native input admission, no full retained Run. Scenarios where the fixture carries
   a representation unknown that production would evaluate (evidence available but unrepresentable) are NOT compared.
E: expectation-law controls over the fixture only (workflows section 5 and 14; policy-test schema expectationLaw).
U: policy universe token controls against composition contract section 2 and the evaluator profile policyUniverseMap.
Every row records raw observations; `lawOk` states the law-derived expectation. Usage: --source ROOT --out OUT_JSON
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import sys
import traceback
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--source", required=True, type=Path)
ap.add_argument("--out", required=True, type=Path)
a = ap.parse_args()
DC = a.source.resolve() / "docs/coop/design-corrections"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


W = load("khu_workflows3", DC / "workflows/workflows_model.v3.py")
E = load("khu_composition3", DC / "foundation/evaluator_composition_model.v3.py")
UMAP = json.loads((DC / "foundation/identity-schemas.v3.json").read_text())["x-opensip-evaluator-profile"]["policyUniverseMap"]
NONBLOCKING = set(E.M.SCHEMA["x-opensip-evaluator-deficiency-registry"]["nonBlockingDisclosures"])
ROWS = []
TOKEN = "typescript"
WAIVERS_EMPTY = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": []}
N = {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": []}
T = {"op": "exists", "relation": "test-execution", "minResolution": "observed", "filters": [], "evidence": "test"}


def row(group, case, law_ok, observed, law):
    ROWS.append({"group": group, "case": case, "lawOk": bool(law_ok), "law": law, "observed": observed})


def tree(shape):
    return {"N": N, "or": {"op": "or", "operands": [N, T]}, "and": {"op": "and", "operands": [N, T]}, "notT": {"op": "not", "operand": T}}[shape]


def rule(shape, requirement, gate=True, severity="error", enabled=True, universe=TOKEN):
    atom = tree(shape)
    return {"ruleId": "r", "ruleProgramRef": {"contributionId": "fixture", "ruleStableId": "r", "semanticsMajor": 2, "programDigest": E.sha(atom)},
            "enabled": enabled, "severity": severity, "gate": gate, "subjectEnumeration": {"universe": universe, "subjectKind": "file"},
            "emitWhen": atom, "evidenceUse": [] if requirement is None else [{"kind": "test", "requirement": requirement}]}


def waivers(paths):
    return {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1,
            "waivers": [{"waiverId": "w-%02d" % i, "target": {"ruleId": "r", "subjectPath": p}, "reason": "accepted", "expires": None} for i, p in enumerate(sorted(paths))]}


def fixture_suite(r, truth, available, waived=(), expectations=None, coverage=None, fact_universe=TOKEN):
    subjects = sorted(truth)
    partial = any(v is None for v in truth.values())
    facts = [{"relation": "file", "subject": p, "target": p, "resolution": "enumerated", "universe": fact_universe, "confidenceMillionths": 1000000}
             for p in subjects if truth[p] is True]
    policy = {"schemaFamily": "opensip.product.policy", "schemaMajor": 2, "gateSeverityAtLeast": "warning", "rules": [r]}
    return {"schemaFamily": "opensip.product.policy-test", "schemaMajor": 2, "candidatePolicy": policy, "waivers": waivers(waived),
            "asOfDate": "2026-09-05",
            "cases": [{"id": "c", "subject": {"kind": "facts", "subjects": subjects, "facts": facts,
                                              "coverage": coverage or ("partial" if partial else "complete"), "evidenceAvailable": ["test"] if available else []},
                       "expectations": expectations or [{"kind": "verdict", "verdict": "pass"}]}]}


def run_fixture(suite):
    try:
        res, refusal = W.run_admitted_policy_test(copy.deepcopy(suite))
    except W.Refusal as exc:
        return {"route": "REFUSED", "errorCode": exc.error_code, "detail": exc.detail, "remedy": str(exc.remedy), "subject": exc.subject}
    except Exception as exc:  # recorded, never read as a lawful refusal
        return {"route": "EXCEPTION", "error": type(exc).__name__ + ": " + str(exc)[:300], "trace": traceback.format_exc()[-800:]}
    if refusal is not None:
        return {"route": "RESOLVER-REFUSED", "errorCode": refusal.error_code, "detail": refusal.detail, "remedy": str(refusal.remedy), "subject": refusal.subject}
    c = res["results"][0]
    return {"route": "RETURNED", "summary": res["summary"], "verdict": c["observedVerdict"], "outcome": c["outcome"],
            "findings": sorted([f["subject"], f["waived"]] for f in c["findings"]), "indeterminateRules": c["indeterminateRules"],
            "expectationOutcomes": c["expectationOutcomes"]}


def token(text):
    return hashlib.sha256(text.encode()).hexdigest()


def run_composition(r, truth, available, waived=()):
    policy = {"schemaFamily": "opensip.product.policy", "schemaMajor": 2, "gateSeverityAtLeast": "warning", "rules": [r]}
    effective = waivers(waived)
    detector = "closure2:" + token("fixture-detector")
    universe = token("one")
    population = {}
    for path in sorted(truth):
        sid = E.M.identifier("evaluation-subject", {"schemaVersion": 3, "universe": universe, "kind": "file", "nativeSubjectId": path})
        population[sid] = {"subjectId": sid, "universe": universe, "kind": "file", "collisionPopulationComplete": True,
                           "row": {"nativeSubjectId": path, "kind": "file", "path": path, "qualifiedName": path, "subjectLanguage": "typescript",
                                   "signatureTokens": [], "projections": []}}
    required_missing = [{"source": "import", "cause": "evidence-kind-unavailable", "subjectId": None, "predicateId": None, "inputRefs": [],
                         "evidenceKind": "test", "nativeCause": None, "universe": None}] \
        if any(u["requirement"] == "required" for u in r["evidenceUse"]) and not available else []
    plan = {"policyDigest": E.sha(policy), "waiverDigest": E.sha(effective), "semanticClosures": [detector], "budget": {"unit": "work-units", "limit": 100000}}
    enumeration = ({"state": "disabled", "inventoryRefs": [], "selectedSubjectIds": [], "unresolvedSubjectIds": [], "incompleteInventoryRefs": []} if not r["enabled"]
                   else {"state": "complete", "inventoryRefs": [], "selectedSubjectIds": E.cset(population), "unresolvedSubjectIds": [], "incompleteInventoryRefs": []})
    inputs = {"plan": plan, "planId": "plan2:" + token("plan"), "executionPlanId": "exec-plan2:" + token("exec"), "evaluatorClosure": "closure2:" + token("eval"),
              "policy": policy, "effectiveWaivers": effective,
              "emissionPlan": {"schemaVersion": 1, "policyDigest": plan["policyDigest"], "rules": [{"ruleId": "r", "contributionId": "fixture", "ruleStableId": "r",
                               "semanticsMajor": 2, "detectorClosure": detector, "stabilityClass": "path-stable", "emissionProfile": "declarative-subject-v1"}]},
              "population": population, "enumerations": {"r": enumeration}, "enumerationDeficiencies": {"r": []},
              "requiredEvidenceDeficiencies": {"r": required_missing}, "executionDeficiencies": [],
              "executionInputsDigest": "e" * 64, "evaluationInputRefs": [{"domain": "execution-inputs", "digest": "e" * 64}],
              "inventoryRowCount": len(population), "inventoryLocatorCount": len(population), "factCount": 0, "observationCount": 0, "coverageCount": 0,
              "importKinds": {}, "closures": {detector: {"kind": "detector"}}}

    def scan(rule_, subject, node, pid):
        path = subject["row"]["path"]
        if node["relation"] == "test-execution":
            # available: a lawful production unknown observation (only compared where the root is decided by the native atom);
            # absent: the §9.5 evidence-kind-unavailable import cause.
            cause = "incomplete-observation" if available else "evidence-kind-unavailable"
            ds = [{"source": "import", "cause": cause, "subjectId": subject["subjectId"], "predicateId": pid, "inputRefs": [],
                   "evidenceKind": "test", "nativeCause": None, "universe": None}]
            return {"kind": "imported-atom", "value": "indeterminate", "matchingFactIds": [], "uncertainFactIds": [], "matchingImportRows": [],
                    "uncertainImportRows": [], "coverageIds": [], "scopeIds": [], "inputRefs": [], "deficiencies": ds}
        v = truth[path]
        ds = [] if v is not None else [{"source": "native", "cause": "required-relation-missing", "subjectId": subject["subjectId"], "predicateId": pid,
                                        "inputRefs": [], "evidenceKind": None, "nativeCause": None, "universe": None}]
        return {"kind": "native-atom", "value": {True: "true", False: "false", None: "indeterminate"}[v], "matchingFactIds": [], "uncertainFactIds": [],
                "matchingImportRows": [], "uncertainImportRows": [], "coverageIds": [], "scopeIds": [], "inputRefs": [], "deficiencies": ds}
    out = E.compose(inputs, scan)
    proof = out["proof"]
    required = {u["kind"] for u in r["evidenceUse"] if u["requirement"] == "required"}

    def blocks(d):
        if d["cause"] in NONBLOCKING:
            return False
        if d["source"] != "import":
            return d["source"] in ("native", "enumeration", "execution")
        return d["evidenceKind"] in required
    blocked_root = False
    for p in proof["predicateProofs"]:
        if p["predicateId"] == "p" and p["value"] == "indeterminate":
            witness = json.loads(out["blobs"][p["witnessDigest"]])
            blocked_root = blocked_root or any(blocks(d) for d in witness["deficiencies"])
    waived_ids = set(proof["waivedFindingIds"])
    findings = sorted([v["subject"]["logicalPath"], k in waived_ids] for k, (dom, v) in out["objects"].items() if dom == "finding")
    # §9.5: required-import deficiencies apply to ENABLED rules only; a disabled rule keeps outcome disabled.
    return {"verdict": proof["verdict"], "ruleOutcome": proof["ruleResults"][0]["outcome"], "findings": findings,
            "ruleUnknown": r["enabled"] and (bool(required_missing) or blocked_root)}


SCENARIOS = [
    # name, shape, requirement, available, truth, waived, rule kwargs
    ("or-known-true-required-absent-gating-unwaived", "or", "required", False, {"src/a.ts": True}, (), {}),
    ("or-known-true-required-present-gating", "or", "required", True, {"src/a.ts": True}, (), {}),
    ("or-known-true-optional-absent-gating", "or", "optional", False, {"src/a.ts": True}, (), {}),
    ("and-known-false-required-absent-gating", "and", "required", False, {"src/a.ts": False}, (), {}),
    ("and-known-false-optional-absent-gating", "and", "optional", False, {"src/a.ts": False}, (), {}),
    ("and-known-true-optional-absent-complete", "and", "optional", False, {"src/a.ts": True}, (), {}),
    ("and-known-true-optional-absent-partial-coverage", "and", "optional", False, {"src/a.ts": True, "src/u.ts": None}, (), {}),
    ("or-known-false-optional-absent-gating", "or", "optional", False, {"src/a.ts": False}, (), {}),
    ("or-known-false-required-absent-gating", "or", "required", False, {"src/a.ts": False}, (), {}),
    ("not-unknown-required-absent-gating", "notT", "required", False, {"src/a.ts": False}, (), {}),
    ("no-selected-subjects-required-absent-gating", "or", "required", False, {}, (), {}),
    ("no-selected-subjects-no-evidence-gating", "N", None, False, {}, (), {}),
    ("waived-known-true-required-absent-gating", "or", "required", False, {"src/a.ts": True}, ("src/a.ts",), {}),
    ("unwaived-known-true-required-absent-nongating", "or", "required", False, {"src/a.ts": True}, (), {"gate": False}),
    ("unwaived-known-true-required-absent-below-threshold", "or", "required", False, {"src/a.ts": True}, (), {"severity": "note"}),
    ("waived-known-true-required-present-gating", "or", "required", True, {"src/a.ts": True}, ("src/a.ts",), {}),
    ("two-subjects-true-and-false-required-absent-gating", "or", "required", False, {"src/a.ts": True, "src/b.ts": False}, (), {}),
    ("native-unknown-partial-no-evidence-gating", "N", None, False, {"src/a.ts": None}, (), {}),
    ("native-known-true-and-unknown-partial-no-evidence-gating", "N", None, False, {"src/a.ts": True, "src/u.ts": None}, (), {}),
    ("disabled-rule-required-absent", "or", "required", False, {"src/a.ts": True}, (), {"enabled": False}),
    # partial Coverage where every native atom is nevertheless KNOWN: isolates the optional-absent-only disclosure law
    ("and-known-true-optional-absent-partial-coverage-all-native-known", "and", "optional", False, {"src/a.ts": True}, (), {"coverage": "partial"}),
    ("or-known-true-required-absent-partial-coverage-all-native-known", "or", "required", False, {"src/a.ts": True}, (), {"coverage": "partial"}),
]
for name, shape, requirement, available, truth, waived, kw in SCENARIOS:
    kw = dict(kw)
    coverage = kw.pop("coverage", None)
    r = rule(shape, requirement, **kw)
    fx = run_fixture(fixture_suite(r, truth, available, waived, coverage=coverage))
    if available and not (shape == "or" and all(v is True for v in truth.values())):
        raise SystemExit("scenario %s: an available-but-unrepresentable test atom is compared only under a native-decided root" % name)
    try:
        comp = run_composition(r, truth, available, waived)
    except Exception:
        comp = {"error": traceback.format_exc()[-800:]}
    agree = None
    if fx.get("route") == "RETURNED" and "verdict" in comp:
        fixture_sealed = "pass" if fx["verdict"] == "advisory" else fx["verdict"]
        agree = {"verdict": fixture_sealed == comp["verdict"], "findings": fx["findings"] == comp["findings"],
                 "ruleUnknown": ("r" in fx["indeterminateRules"]) == comp["ruleUnknown"]}
    row("K", name, agree is not None and all(agree.values()), {"fixture": fx, "composition": comp, "agree": agree},
        "fixture sealed verdict, finding/waived subjects and rule unknown accounting equal the composition owner's (§5, §9.5)")

# ----------------------------------------------------------------------------------------------- expectation law (fixture)
def expectation_case(name, shape, requirement, available, truth, expectations, want, waived=(), law=""):
    fx = run_fixture(fixture_suite(rule(shape, requirement), truth, available, waived, expectations))
    row("E", name, fx.get("route") == "RETURNED" and fx["expectationOutcomes"] == want, fx, law + " -> " + json.dumps(want))


expectation_case("known-hit-under-required-absent-is-a-met-finding", "or", "required", False, {"src/a.ts": True},
                 [{"kind": "finding", "ruleId": "r", "minCount": 1, "maxCount": 1, "subjects": ["src/a.ts"]}, {"kind": "verdict", "verdict": "fail"},
                  {"kind": "indeterminate", "ruleId": "r"}],
                 ["met", "met", "met"], law="known finding preserved, fail dominates, required-evidence deficiency still accounted")
expectation_case("known-false-under-required-absent-is-not-an-authoritative-no-match", "and", "required", False, {"src/a.ts": False},
                 [{"kind": "no-finding", "ruleId": "r"}, {"kind": "verdict", "verdict": "indeterminate"}], ["indeterminate", "met"],
                 law="workflows §14: missing required evidence never silently becomes an authoritative no-match")
expectation_case("mixed-subjects-under-required-absent", "or", "required", False, {"src/a.ts": True, "src/b.ts": False},
                 [{"kind": "finding", "ruleId": "r", "minCount": 1, "maxCount": 1, "subjects": ["src/a.ts"]},
                  {"kind": "finding", "ruleId": "r", "minCount": 1, "maxCount": 1}, {"kind": "no-finding", "ruleId": "r"}],
                 ["met", "indeterminate", "unmet"], law="a.ts decided by its known hit; b.ts stays open; a known hit decides no-finding")
expectation_case("zero-subjects-under-required-absent", "or", "required", False, {},
                 [{"kind": "no-finding", "ruleId": "r"}, {"kind": "indeterminate", "ruleId": "r"}, {"kind": "verdict", "verdict": "indeterminate"}],
                 ["met", "met", "met"], law="no enumerated subject can hold a finding; the rule-level deficiency remains")
expectation_case("waived-known-hit-under-required-absent", "or", "required", False, {"src/a.ts": True},
                 [{"kind": "finding", "ruleId": "r", "minCount": 1}, {"kind": "verdict", "verdict": "indeterminate"}], ["met", "met"],
                 waived=("src/a.ts",), law="a waived finding is still a finding; a waiver never cures the required-evidence unknown")
expectation_case("optional-absent-only-no-finding-is-disclosed-met", "and", "optional", False, {"src/a.ts": True},
                 [{"kind": "no-finding", "ruleId": "r"}, {"kind": "indeterminate", "ruleId": "r"}, {"kind": "verdict", "verdict": "pass"}],
                 ["met", "unmet", "met"], law="optional evidence absent alone is disclosed, not a deficiency (historical §5 distinction)")

# ----------------------------------------------------------------------------------------------- universe tokens
def universe_case(name, rule_universe, fact_universe, want_route, want_detail=None, law="", enabled=True):
    r = rule("N", None, universe=rule_universe, enabled=enabled)
    fx = run_fixture(fixture_suite(r, {"src/a.ts": True, "src/b.ts": False}, False, (), fact_universe=fact_universe,
                                   expectations=[{"kind": "finding", "ruleId": "r", "minCount": 1, "maxCount": 1, "subjects": ["src/a.ts"]}]))
    ok = fx.get("route") == want_route and (want_detail is None or fx.get("detail") == want_detail)
    row("U", name, ok, fx, law + " -> " + json.dumps([want_route, want_detail]))


for tok in sorted(UMAP):
    universe_case("registered-token-%s-admitted" % tok, tok, tok, "RETURNED", law="policyUniverseMap token")
universe_case("historical-token-typescript-v2-rule-refused", "typescript-v2", TOKEN, "RESOLVER-REFUSED", "POLICY.UNKNOWN_RULE",
              law="composition §2: unknown tokens refuse; typescript-v2 is not an implicit alias")
universe_case("arbitrary-token-rule-refused", "no-such-universe", TOKEN, "RESOLVER-REFUSED", "POLICY.UNKNOWN_RULE", law="composition §2 closed token map")
universe_case("disabled-rule-with-unknown-token-refused", "no-such-universe", TOKEN, "RESOLVER-REFUSED", "POLICY.UNKNOWN_RULE",
              law="evaluator input admission checks every rule's token", enabled=False)
universe_case("fixture-fact-with-unknown-token-refused", TOKEN, "typescript-v2", "REFUSED", "CONFIG.INVALID",
              law="a fixture fact names a registered policy universe token (no silent cross-token no-match)")
universe_case("rule-and-facts-both-unknown-token-refused-at-fixture-admission", "no-such-universe", "no-such-universe", "REFUSED", "CONFIG.INVALID",
              law="admission precedence: fixture faults precede the resolver")
cases = json.loads((DC / "workflows/policy-test-cases.v3.json").read_text())
tokens = sorted({r["subjectEnumeration"]["universe"] for r in cases["currentSuite"]["candidatePolicy"]["rules"]})
authored = run_fixture(cases["currentSuite"])
row("U", "authored-current-suite-uses-registered-tokens-and-is-admitted", all(t in UMAP for t in tokens) and authored.get("route") == "RETURNED",
    {"tokens": tokens, "route": authored.get("route"), "summary": authored.get("summary")}, "authored fixture uses the closed token map")

report = {"standing": "bounded fixture/composition comparison and universe controls; not a full Run, provider or product qualification",
          "source": str(a.source.resolve()), "rows": ROWS, "lawFailures": [(r["group"], r["case"]) for r in ROWS if not r["lawOk"]]}
a.out.parent.mkdir(parents=True, exist_ok=True)
a.out.write_text(json.dumps(report, indent=1, default=str) + "\n")
print(json.dumps({"rows": len(ROWS), "lawFailures": report["lawFailures"]}, indent=1))
