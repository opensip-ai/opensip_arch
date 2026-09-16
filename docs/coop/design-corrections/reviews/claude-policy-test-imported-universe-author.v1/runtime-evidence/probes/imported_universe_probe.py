"""Imported-atom universe join discrimination through the public policy.test route (READ-ONLY over --source; -I -B).

Each scenario is one explicitly constructed PolicyTestSuiteV2 (one rule, subject src/h.ts, complete Coverage, rule universe
typescript) run through workflows_model.v3.run_admitted_policy_test. Observed: route, observed verdict, finding subjects, and
whether the rule is listed in indeterminateRules. `law` is the expectation from the PolicyTestSuiteV2
x-opensip-fixture-representation factUniverse / importedLaw / nativeLaw / ruleLaw and composition contract sections 3 and 5:
a fact of another registered universe never occupies the evaluated subject (neither known nor uncertain); representable
imported absence never proves absence; native absence under complete Coverage decides. Group W is a white-box occupancy
trace over the model's own imported occupancy helper when present. BOUNDED fixture reference only: no full Run, provider or
native admission. Usage: --source ROOT --out OUT_JSON
"""
import argparse
import copy
import importlib.util
import json
import sys
import traceback
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--source", required=True, type=Path)
ap.add_argument("--out", required=True, type=Path)
a = ap.parse_args()
WF = a.source.resolve() / "docs/coop/design-corrections/workflows"
spec = importlib.util.spec_from_file_location("iu_workflows3", WF / "workflows_model.v3.py")
W = importlib.util.module_from_spec(spec)
sys.modules["iu_workflows3"] = W
spec.loader.exec_module(W)
T = W.policy_test_model()
ROWS = []
H = "src/h.ts"


def fact(relation, universe, resolution, **extra):
    return dict({"relation": relation, "subject": H, "target": H, "resolution": resolution, "universe": universe, "confidenceMillionths": 1000000}, **extra)


def rt(universe, observability="observed-hit"):
    return fact("runtime-observation", universe, "observed", observability=observability)


def hist(universe):
    return fact("history-change", universe, "observed")


def native_file(universe):
    return fact("file", universe, "enumerated")


def test_row(universe):
    return fact("test-execution", universe, "observed")


HIT = [{"field": "observability", "cmp": "eq", "value": "observed-hit"}]
ATOMS = {
    "rt-exists": ({"op": "exists", "relation": "runtime-observation", "minResolution": "observed", "filters": HIT, "evidence": "runtime"}, "runtime"),
    "rt-none": ({"op": "none", "relation": "runtime-observation", "minResolution": "observed", "filters": HIT, "evidence": "runtime"}, "runtime"),
    "rt-count0": ({"op": "count-at-most", "relation": "runtime-observation", "minResolution": "observed", "filters": HIT, "n": 0, "evidence": "runtime"}, "runtime"),
    "hist-exists": ({"op": "exists", "relation": "history-change", "minResolution": "observed", "filters": [], "evidence": "history"}, "history"),
    "hist-none": ({"op": "none", "relation": "history-change", "minResolution": "observed", "filters": [], "evidence": "history"}, "history"),
    "file-exists": ({"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": []}, None),
    "test-exists": ({"op": "exists", "relation": "test-execution", "minResolution": "observed", "filters": [], "evidence": "test"}, "test"),
}


def suite(atom_name, facts, available, requirement="optional"):
    atom, kind = ATOMS[atom_name]
    rule = {"ruleId": "r", "ruleProgramRef": {"contributionId": "core.rules", "ruleStableId": "r", "semanticsMajor": 1, "programDigest": "0" * 64},
            "enabled": True, "severity": "error", "gate": True, "subjectEnumeration": {"universe": "typescript", "subjectKind": "file"},
            "emitWhen": copy.deepcopy(atom), "evidenceUse": [] if kind is None else [{"kind": kind, "requirement": requirement}]}
    return {"schemaFamily": "opensip.product.policy-test", "schemaMajor": 2,
            "candidatePolicy": {"schemaFamily": "opensip.product.policy", "schemaMajor": 2, "gateSeverityAtLeast": "warning", "rules": [rule]},
            "waivers": {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": []}, "asOfDate": "2026-09-05",
            "cases": [{"id": "c", "subject": {"kind": "facts", "subjects": [H], "facts": facts, "coverage": "complete", "evidenceAvailable": available},
                       "expectations": [{"kind": "verdict", "verdict": "pass"}]}]}


def run(s):
    try:
        res, refusal = W.run_admitted_policy_test(copy.deepcopy(s))
    except W.Refusal as exc:
        return {"route": "REFUSED", "detail": exc.detail, "subject": exc.subject}
    except Exception:
        return {"route": "EXCEPTION", "trace": traceback.format_exc()[-800:]}
    if refusal is not None:
        return {"route": "RESOLVER-REFUSED", "detail": refusal.detail, "remedy": refusal.remedy}
    c = res["results"][0]
    return {"route": "RETURNED", "verdict": c["observedVerdict"], "findings": [f["subject"] for f in c["findings"]], "listed": "r" in c["indeterminateRules"]}


def scenario(group, name, atom_name, facts, available, want, law, requirement="optional"):
    obs = run(suite(atom_name, facts, available, requirement))
    ok = obs.get("route") == "RETURNED" and [obs["verdict"], obs["findings"], obs["listed"]] == want
    ROWS.append({"group": group, "case": name, "lawOk": ok, "want": {"verdict": want[0], "findings": want[1], "listed": want[2]}, "observed": obs, "law": law})


KNOWN_FAIL = ["fail", [H], False]
UNKNOWN = ["indeterminate", [], True]
DECIDED_NO = ["pass", [], False]
FOREIGN = "a fact of another registered universe never occupies (factUniverse); imported absence never proves absence (importedLaw)"
for tok in ("rust", "syntax"):
    scenario("R", "runtime-exists-foreign-%s-hit-only-is-unknown" % tok, "rt-exists", [rt(tok)], ["runtime"], UNKNOWN, FOREIGN)
scenario("R", "runtime-exists-same-universe-hit-is-known-fail", "rt-exists", [rt("typescript")], ["runtime"], KNOWN_FAIL, "representable same-universe row is a known match")
scenario("R", "runtime-exists-foreign-hit-beside-same-universe-hit", "rt-exists", [rt("rust"), rt("typescript")], ["runtime"], KNOWN_FAIL, "the same-universe row still decides")
scenario("R", "runtime-exists-foreign-unobservable-only-is-unknown", "rt-exists", [rt("rust", "unobservable")], ["runtime"], UNKNOWN, FOREIGN)
scenario("R", "runtime-exists-foreign-unobservable-beside-same-universe-hit", "rt-exists", [rt("rust", "unobservable"), rt("typescript")], ["runtime"], KNOWN_FAIL,
         "a foreign uncertain row neither occupies nor weakens the same-universe known hit")
scenario("R", "runtime-none-foreign-hit-is-unknown-not-false", "rt-none", [rt("rust")], ["runtime"], UNKNOWN, FOREIGN)
scenario("R", "runtime-none-same-universe-hit-is-known-false", "rt-none", [rt("typescript")], ["runtime"], DECIDED_NO, "none is false on a known match")
scenario("R", "runtime-count0-foreign-hit-is-unknown-not-false", "rt-count0", [rt("rust")], ["runtime"], UNKNOWN, FOREIGN)
scenario("R", "runtime-count0-same-universe-hit-is-known-false", "rt-count0", [rt("typescript")], ["runtime"], DECIDED_NO, "count-at-most is false above N on known matches")
scenario("R", "runtime-absence-with-evidence-available-is-unknown", "rt-exists", [], ["runtime"], UNKNOWN, "imported absence never proves absence")
scenario("R", "runtime-optional-evidence-absent-is-disclosed", "rt-exists", [rt("typescript")], [], DECIDED_NO, "optional evidence absent alone is non-blocking (v1 law)")
scenario("R", "runtime-required-evidence-absent-is-a-deficiency", "rt-exists", [rt("typescript")], [], UNKNOWN, "required evidence absent is a rule deficiency (v1 law)",
         requirement="required")
scenario("H", "history-exists-same-universe-row-is-known-fail", "hist-exists", [hist("typescript")], ["history"], KNOWN_FAIL, "representable same-universe history row")
scenario("H", "history-exists-foreign-row-only-is-unknown", "hist-exists", [hist("rust")], ["history"], UNKNOWN, FOREIGN)
scenario("H", "history-none-foreign-row-is-unknown-not-false", "hist-none", [hist("rust")], ["history"], UNKNOWN, FOREIGN)
scenario("H", "history-none-same-universe-row-is-known-false", "hist-none", [hist("typescript")], ["history"], DECIDED_NO, "none is false on a known match")
scenario("N", "native-file-same-universe-is-known-fail", "file-exists", [native_file("typescript")], [], KNOWN_FAIL, "native positive control")
scenario("N", "native-file-foreign-universe-is-decided-no-match", "file-exists", [native_file("rust")], [], DECIDED_NO, "native occupancy requires equal universe; complete Coverage decides")
for tok in ("typescript", "rust"):
    scenario("X", "test-execution-row-%s-stays-unrepresentable" % tok, "test-exists", [test_row(tok)], ["test"], UNKNOWN,
             "test-execution observations are unrepresentable whatever the fixture row universe")

# ---------------------------------------------------------------- W: white-box occupancy trace (the model's own helper)
helper = getattr(T, "_imported_occupancy", None)
if helper is None:
    ROWS.append({"group": "W", "case": "imported-occupancy-helper-present", "lawOk": False, "observed": "absent", "law": "an explicit imported occupancy join"})
else:
    calls, filtered = [], []
    real_filters = T._filters

    def traced_occupancy(f, subject, universe):
        decision = helper(f, subject, universe)
        calls.append({"universe": f["universe"], "observability": f.get("observability"), "evaluated": universe, "occupies": decision})
        return decision

    def traced_filters(f, atom, plane, kind):
        filtered.append({"universe": f["universe"], "plane": plane})
        return real_filters(f, atom, plane, kind)
    T._imported_occupancy, T._filters = traced_occupancy, traced_filters
    try:
        obs = run(suite("rt-exists", [rt("rust", "unobservable"), rt("rust"), rt("typescript")], ["runtime"]))
    finally:
        T._imported_occupancy, T._filters = helper, real_filters
    ok = (obs.get("verdict") == "fail" and sorted((c["universe"], c["occupies"]) for c in calls) == [("rust", False), ("rust", False), ("typescript", True)]
          and all(x["universe"] == "typescript" for x in filtered if x["plane"] == "imported"))
    ROWS.append({"group": "W", "case": "foreign-known-and-uncertain-rows-never-reach-classification", "lawOk": ok,
                 "observed": {"route": obs, "occupancyCalls": calls, "filterCalls": filtered},
                 "law": "only the same-universe row occupies; foreign rows are rejected before observability or filter classification"})
    direct = [helper(rt("typescript"), H, "typescript"), helper(rt("rust"), H, "typescript"), helper(rt("typescript"), "src/other.ts", "typescript")]
    ROWS.append({"group": "W", "case": "helper-requires-subject-and-universe", "lawOk": direct == [True, False, False], "observed": direct,
                 "law": "occupancy requires the evaluated subject path and universe"})

report = {"standing": "author imported-universe discrimination probe through the public route; bounded fixture reference, not a full Run or provider qualification",
          "source": str(a.source.resolve()), "rows": ROWS, "lawFailures": [(r["group"], r["case"]) for r in ROWS if not r["lawOk"]]}
a.out.parent.mkdir(parents=True, exist_ok=True)
a.out.write_text(json.dumps(report, indent=1, default=str) + "\n")
print(json.dumps({"rows": len(ROWS), "lawFailures": report["lawFailures"]}, indent=1))
