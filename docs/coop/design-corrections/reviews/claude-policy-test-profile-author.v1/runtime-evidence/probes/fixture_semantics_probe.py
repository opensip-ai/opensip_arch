"""Focused PolicyTestSuiteV2 semantics probe through the CORRECTED public route (READ-ONLY; run with -I -B).

Every input starts from the authored policy-test-cases.v3.json suite and changes only the candidate rules and/or cases
named per control; each candidate is admitted by the PolicyTestSuiteV2 schema and the current resolver inside
workflows_model.v3.run_admitted_policy_test. Expected values are this author's reading of the representation law in
schemas/evaluator3/policy-test.schema.json; they are author expectations, not an independent oracle.
Usage: fixture_semantics_probe.py --source ROOT --out OUT_JSON
"""
import argparse
import copy
import importlib.util
import json
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--source", required=True, type=Path)
ap.add_argument("--out", required=True, type=Path)
a = ap.parse_args()
W = a.source.resolve() / "docs/coop/design-corrections/workflows"
spec = importlib.util.spec_from_file_location("semantics_probe_workflows3", W / "workflows_model.v3.py")
WF3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(WF3)
canonical = WF3.canonical
BASE = canonical.parse((W / "policy-test-cases.v3.json").read_bytes())["currentSuite"]
REG = WF3.policy_test_model().REGISTRY
DOMAIN = REG["engineFamilies"]["portableUniverseDomains"][0]
U = "typescript-v2"
ROWS = []


def rule(rule_id, emit, kind="file", evidence_use=(), gate=False, severity="warning"):
    return {"ruleId": rule_id, "ruleProgramRef": {"contributionId": "core.rules", "ruleStableId": rule_id, "semanticsMajor": 1, "programDigest": "0" * 64},
            "enabled": True, "severity": severity, "gate": gate, "subjectEnumeration": {"universe": U, "subjectKind": kind},
            "emitWhen": emit, "evidenceUse": [dict(e) for e in evidence_use]}


def atom(op, relation, rung, endpoint=None, filters=(), evidence=None, n=None):
    node = {"op": op, "relation": relation, "minResolution": rung, "filters": [dict(f) for f in filters]}
    if endpoint:
        node["endpoint"] = endpoint
    if evidence:
        node["evidence"] = evidence
    if n is not None:
        node["n"] = n
    return node


def imp(subject, target, **extra):
    return dict({"relation": "imports", "subject": subject, "target": target, "resolution": "resolved-target", "universe": U, "confidenceMillionths": 1000000}, **extra)


def case(case_id, subjects, facts, expectations, coverage="complete", evidence=()):
    return {"id": case_id, "subject": {"kind": "facts", "subjects": list(subjects), "facts": list(facts), "coverage": coverage, "evidenceAvailable": list(evidence)},
            "expectations": list(expectations)}


def suite(rules, cases):
    s = copy.deepcopy(BASE)
    s["candidatePolicy"]["rules"] = sorted(rules, key=lambda r: r["ruleId"].encode())
    s["cases"] = cases
    s["waivers"] = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": []}
    return s


def run(s):
    try:
        res, ref = WF3.run_admitted_policy_test(copy.deepcopy(s))
        return {"route": "RETURNED", "resolverRefusal": None if ref is None else [ref.error_code, ref.detail, ref.remedy],
                "cases": {c["id"]: {"outcome": c["outcome"], "verdict": c["observedVerdict"], "findings": [[f["ruleId"], f["subject"], f["waived"]] for f in c["findings"]],
                                    "indeterminateRules": c["indeterminateRules"], "expectationOutcomes": c["expectationOutcomes"]} for c in res["results"]},
                "id": res["policyTestResultId"]}
    except WF3.Refusal as exc:
        return {"route": "REFUSED", "errorCode": exc.error_code, "detail": exc.detail, "subject": exc.subject}


def control(cid, s, predicate, why):
    observed = run(s)
    try:
        ok = bool(predicate(observed))
    except Exception as exc:  # a missing key is a failed control, reported
        ok, observed = False, dict(observed, predicateError=repr(exc))
    ROWS.append({"id": cid, "ok": ok, "expectation": why, "observed": observed})


RUNTIME_UNKNOWN = atom("exists", "runtime-observation", "observed", filters=[{"field": "observability", "cmp": "eq", "value": "observed-hit"}], evidence="runtime")
NO_OUTGOING = atom("none", "imports", "resolved-target", endpoint="source")
RUNTIME_USE = [{"kind": "runtime", "requirement": "required"}]

control("count-at-most-known-above-n-is-false",
        suite([rule("count0", atom("count-at-most", "imports", "resolved-target", n=0), kind="export")],
              [case("c", ["src/a.ts"], [imp("src/a.ts", "src/x.ts")], [{"kind": "no-finding", "ruleId": "count0"}])]),
        lambda o: o["cases"]["c"]["expectationOutcomes"] == ["met"] and o["cases"]["c"]["indeterminateRules"] == [],
        "one known outgoing import exceeds n=0: false, a definite no-match")
control("count-at-most-under-partial-coverage-is-unknown",
        suite([rule("count0", atom("count-at-most", "imports", "resolved-target", n=0), kind="export")],
              [case("c", ["src/a.ts"], [], [{"kind": "no-finding", "ruleId": "count0"}], coverage="partial")]),
        lambda o: o["cases"]["c"]["expectationOutcomes"] == ["indeterminate"] and o["cases"]["c"]["indeterminateRules"] == ["count0"],
        "absence under partial Coverage cannot make count-at-most true")
control("or-with-a-true-operand-is-true-despite-an-unknown-operand",
        suite([rule("either", {"op": "or", "operands": [RUNTIME_UNKNOWN, NO_OUTGOING]}, kind="export", evidence_use=RUNTIME_USE)],
              [case("c", ["src/a.ts"], [], [{"kind": "finding", "ruleId": "either", "minCount": 1}], evidence=["runtime"])]),
        lambda o: o["cases"]["c"]["findings"] == [["either", "src/a.ts", False]] and o["cases"]["c"]["indeterminateRules"] == [],
        "strong Kleene: unknown OR true is true")
control("and-with-a-false-operand-is-false-despite-an-unknown-operand",
        suite([rule("both", {"op": "and", "operands": [RUNTIME_UNKNOWN, atom("exists", "imports", "resolved-target", endpoint="source")]}, kind="export", evidence_use=RUNTIME_USE)],
              [case("c", ["src/a.ts"], [], [{"kind": "no-finding", "ruleId": "both"}], evidence=["runtime"])]),
        lambda o: o["cases"]["c"]["expectationOutcomes"] == ["met"] and o["cases"]["c"]["indeterminateRules"] == [],
        "strong Kleene: unknown AND false is false")
control("not-of-unknown-stays-unknown",
        suite([rule("negated", {"op": "not", "operand": RUNTIME_UNKNOWN}, evidence_use=RUNTIME_USE)],
              [case("c", ["src/a.ts"], [], [{"kind": "no-finding", "ruleId": "negated"}], evidence=["runtime"])]),
        lambda o: o["cases"]["c"]["expectationOutcomes"] == ["indeterminate"] and o["cases"]["c"]["indeterminateRules"] == ["negated"],
        "absence of runtime rows is unknown; NOT unknown is unknown")
control("universe-filter-is-unrepresentable-unknown",
        suite([rule("domain", atom("none", "imports", "resolved-target", endpoint="source", filters=[{"field": "universe", "cmp": "eq", "value": DOMAIN}]), kind="export")],
              [case("c", ["src/a.ts"], [imp("src/a.ts", "src/x.ts")], [{"kind": "no-finding", "ruleId": "domain"}])]),
        lambda o: o["cases"]["c"]["expectationOutcomes"] == ["indeterminate"] and o["cases"]["c"]["indeterminateRules"] == ["domain"],
        "the fixture does not carry the endpoint universe domain: the matching fact is uncertain, so none is unknown, never true or false")
control("confidence-filter-is-representable",
        suite([rule("lowconf", atom("exists", "imports", "resolved-target", endpoint="source", filters=[{"field": "confidenceMillionths", "cmp": "lte", "value": 500000}]), kind="export")],
              [case("c", ["src/a.ts"], [imp("src/a.ts", "src/x.ts", confidenceMillionths=400000)], [{"kind": "finding", "ruleId": "lowconf", "minCount": 1}])]),
        lambda o: o["cases"]["c"]["expectationOutcomes"] == ["met"],
        "confidenceMillionths is a FactRecordCandidate member and is compared with the atom owner's integer comparator")
control("mixed-optional-absent-and-unrepresentable-causes-are-indeterminate-not-disclosed",
        suite([rule("mixed", {"op": "and", "operands": [atom("exists", "history-change", "observed", evidence="history"),
                                                         atom("exists", "test-execution", "observed", evidence="test")]},
                    evidence_use=[{"kind": "history", "requirement": "optional"}, {"kind": "test", "requirement": "required"}])],
              [case("c", ["src/a.ts"], [], [{"kind": "indeterminate", "ruleId": "mixed"}], evidence=["test"])]),
        lambda o: o["cases"]["c"]["expectationOutcomes"] == ["met"],
        "only an optional-evidence-absent unknown is the disclosed non-gating case; an unrepresentable cause keeps the rule indeterminate")
control("optional-evidence-absent-alone-is-disclosed-not-indeterminate",
        suite([rule("hist", atom("exists", "history-change", "observed", evidence="history"), evidence_use=[{"kind": "history", "requirement": "optional"}])],
              [case("c", ["src/a.ts"], [], [{"kind": "indeterminate", "ruleId": "hist"}, {"kind": "no-finding", "ruleId": "hist"}])]),
        lambda o: o["cases"]["c"]["expectationOutcomes"] == ["unmet", "met"] and o["cases"]["c"]["indeterminateRules"] == [],
        "historical §5 law preserved: optional evidence absent under complete Coverage is disclosed, not a deficiency")
control("target-kind-export-evaluates-as-symbol",
        suite([rule("incoming", atom("exists", "imports", "resolved-target", endpoint="target"), kind="symbol")],
              [case("c", ["src/a.ts"], [imp("src/b.ts", "src/a.ts", targetKind="export")], [{"kind": "finding", "ruleId": "incoming", "minCount": 1}])]),
        lambda o: o["cases"]["c"]["expectationOutcomes"] == ["met"],
        "export is not a stored kind: an export target occupies a symbol subject")
control("target-kind-external-never-matches",
        suite([rule("incoming", atom("exists", "imports", "resolved-target", endpoint="target"))],
              [case("c", ["src/a.ts"], [imp("src/b.ts", "src/a.ts", targetKind="external")], [{"kind": "no-finding", "ruleId": "incoming"}])]),
        lambda o: o["cases"]["c"]["expectationOutcomes"] == ["met"] and o["cases"]["c"]["indeterminateRules"] == [],
        "an external target is a definite no-match under complete Coverage")
control("fact-of-another-universe-does-not-occupy",
        suite([rule("incoming", atom("exists", "imports", "resolved-target", endpoint="target"))],
              [case("c", ["src/a.ts"], [imp("src/b.ts", "src/a.ts", targetKind="file", universe="rust-v2")], [{"kind": "no-finding", "ruleId": "incoming"}])]),
        lambda o: o["cases"]["c"]["expectationOutcomes"] == ["met"],
        "the single fixture universe must equal the evaluated subject universe")
control("max-count-with-an-unknown-subject-is-indeterminate-min-only-is-met",
        suite([rule("unimported", atom("none", "imports", "resolved-target", endpoint="target"))],
              [case("c", ["src/a.ts", "src/b.ts"], [imp("src/x.ts", "src/b.ts")],
                    [{"kind": "finding", "ruleId": "unimported", "minCount": 1, "maxCount": 1}, {"kind": "finding", "ruleId": "unimported", "minCount": 1}])]),
        lambda o: o["cases"]["c"]["findings"] == [["unimported", "src/a.ts", False]] and o["cases"]["c"]["expectationOutcomes"] == ["indeterminate", "met"],
        "b.ts is unknown (no targetKind): a known a.ts finding meets minCount, but maxCount cannot be decided")
control("no-finding-with-a-known-finding-is-unmet-even-with-unknown-subjects",
        suite([rule("unimported", atom("none", "imports", "resolved-target", endpoint="target"))],
              [case("c", ["src/a.ts", "src/b.ts"], [imp("src/x.ts", "src/b.ts")], [{"kind": "no-finding", "ruleId": "unimported"}])]),
        lambda o: o["cases"]["c"]["expectationOutcomes"] == ["unmet"],
        "a known hit decides no-finding; unknowns elsewhere cannot rescue it")
_string_major = copy.deepcopy(BASE)
_string_major["schemaMajor"] = "1"
control("non-integer-major-is-a-schema-refusal-not-the-major-route", _string_major,
        lambda o: o["route"] == "REFUSED" and [o["errorCode"], o["detail"]] == ["CONFIG.INVALID", "CONFIG.INVALID"],
        "only an integer major of the policy-test family is the typed major dispatch")
_unregistered = copy.deepcopy(BASE)
_unregistered["cases"][0]["subject"]["facts"][0]["relation"] = "not-a-relation"
control("unregistered-fixture-relation-is-config-invalid", _unregistered,
        lambda o: o["route"] == "REFUSED" and [o["errorCode"], o["detail"]] == ["CONFIG.INVALID", "CONFIG.INVALID"] and "unregistered relation" in o["subject"],
        "fixture facts name registered relations")
_reordered = json.loads(json.dumps(BASE, sort_keys=True))
control("result-identity-is-deterministic-and-key-order-independent", _reordered,
        lambda o: o["route"] == "RETURNED" and o["id"] == run(BASE)["id"] == run(BASE)["id"],
        "the same admitted suite yields the same policytest2 identity")

report = {"standing": "author focused semantics probe through the corrected public route; author expectations, not independent oracle",
          "source": str(a.source.resolve()), "passed": all(r["ok"] for r in ROWS), "count": len(ROWS), "failed": [r["id"] for r in ROWS if not r["ok"]], "controls": ROWS}
a.out.parent.mkdir(parents=True, exist_ok=True)
a.out.write_text(json.dumps(report, indent=1, default=str) + "\n")
print(json.dumps({"passed": report["passed"], "count": report["count"], "failed": [(r["id"], r["observed"]) for r in ROWS if not r["ok"]]}, indent=1, default=str))
raise SystemExit(0 if report["passed"] else 1)
