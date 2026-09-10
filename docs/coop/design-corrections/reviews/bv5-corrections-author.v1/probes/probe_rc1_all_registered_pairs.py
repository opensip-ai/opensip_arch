"""SHOULD-1 reference control: RC-1 applicability over EVERY registered (relation, rung) pair.

Driven through the HOST producer boundary `admit_coverage_result_v3`, not through the
`completeness_from_stage` helper alone, so what is exercised is the admission the contract
names. The corrected RC-1 prose claims:

  * applicability is decided by membership of the RUNG in the closed five-member resolved set,
    never by the relation's ladder length;
  * the five resolved pairs must never claim `not-applicable`;
  * every OTHER registered pair - including `unresolved-edge@observed`, `types@annotated` and
    the syntactic rungs - is `not-applicable` with attempted=false, count 0, classes [];
  * `reachability@from-resolved-calls` is a ONE-RUNG relation that is nevertheless resolved;
  * an unregistered relation or rung refuses and `not-applicable` is not a fallback for it.

Every pair is enumerated from the single ladder authority
`foundation/relation-payload-schemas.v2.json#/x-opensip-relation-registry`, so the sweep cannot
silently miss a relation the registry adds.

Usage: /tmp/opensip-architecture-review-env/bin/python -I -B probe_rc1_all_registered_pairs.py <work-root>
"""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

WORK = Path(sys.argv[1]).resolve()
NATIVE = WORK / "docs/coop/design-corrections/native"
FOUNDATION = WORK / "docs/coop/design-corrections/foundation"

spec = importlib.util.spec_from_file_location("nm", NATIVE / "native_evidence_model.v2.py")
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)

REGISTRY = json.loads((FOUNDATION / "relation-payload-schemas.v2.json").read_text(encoding="utf-8"))
LADDERS = REGISTRY["x-opensip-relation-registry"]["relations"]
FIXTURES = json.loads((NATIVE / "native-cases.v2.json").read_text(encoding="utf-8"))["fixtures"]

RESOLVED = {"resolved-target", "resolved-binding", "resolved-callee", "checked", "from-resolved-calls"}
NOT_APPLICABLE = {"state": "not-applicable", "attempted": False, "examinedExhaustive": True,
                  "stageTerminal": None, "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}
RESOLVED_COMPLETE = {"state": "complete", "attempted": True, "examinedExhaustive": True,
                     "stageTerminal": "complete", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}


def attempt(relation, rung, completeness):
    """One full producer-boundary admission for one (relation, rung) with one completeness record."""
    scope = copy.deepcopy(FIXTURES["scopeDescriptor"])
    scope["relation"], scope["resolution"] = relation, rung
    commitment = N.subject_scope_commitment(scope)
    payload = copy.deepcopy(FIXTURES["coveragePayload"])
    payload["key"]["relation"] = payload["entry"]["relation"] = relation
    payload["key"]["resolution"] = payload["entry"]["resolution"] = rung
    payload["key"]["subjectScopeCommitment"] = commitment["subjectScopeCommitment"]
    payload["entry"]["examinedUniverse"]["subjectScopeCommitment"] = commitment["subjectScopeCommitment"]
    payload["entry"]["resolutionCompleteness"] = copy.deepcopy(completeness)
    try:
        out = N.admit_coverage_result_v3(payload, scope, [])
    except Exception as exc:                       # a typed admission refusal, not a fixture error
        return {"result": "RAISED", "error": type(exc).__name__ + ":" + str(exc)[:200],
                "refusals": [], "faults": [], "coverageId": None}
    return {"result": out["result"], "refusals": out["refusals"],
            "faults": [f["fault"] for f in out["faults"]], "coverageId": out["coverageId"]}


results = {"probe": "rc1-applicability-over-every-registered-relation-rung-pair",
           "host_entry_point": "native_evidence_model.v2.admit_coverage_result_v3",
           "ladder_authority": "foundation/relation-payload-schemas.v2.json#/x-opensip-relation-registry",
           "registeredRelations": len(LADDERS), "registeredPairs": 0, "pairs": [], "controls": [],
           "failures": []}

for relation in sorted(LADDERS):
    for rung in LADDERS[relation]["ladder"]:
        results["registeredPairs"] += 1
        is_resolved = rung in RESOLVED
        expected_state = "complete" if is_resolved else "not-applicable"
        record = RESOLVED_COMPLETE if is_resolved else NOT_APPLICABLE
        contract = attempt(relation, rung, record)
        # the counterfactual: the state RC-1 forbids for this pair
        other = attempt(relation, rung, NOT_APPLICABLE if is_resolved else RESOLVED_COMPLETE)
        row = {"pair": relation + "@" + rung, "rungIsResolved": is_resolved,
               "ladderLength": len(LADDERS[relation]["ladder"]),
               "contractStateAdmits": {"state": expected_state, "result": contract["result"],
                                       "faults": contract["faults"], "refusals": contract["refusals"]},
               "forbiddenStateRefuses": {"state": record is RESOLVED_COMPLETE and "not-applicable" or "complete",
                                         "result": other["result"], "faults": other["faults"]}}
        results["pairs"].append(row)
        if contract["result"] != "ADMIT":
            results["failures"].append("contract state refused for " + row["pair"] + ": " + json.dumps(contract))
        if other["result"] != "REFUSE":
            results["failures"].append("forbidden state admitted for " + row["pair"] + ": " + json.dumps(other))

# --- explicit named controls the corrected prose calls out by name --------------------------
observed = [r for r in results["pairs"] if r["pair"] == "unresolved-edge@observed"]
reachability = [r for r in results["pairs"] if r["pair"] == "reachability@from-resolved-calls"]
results["controls"].append({"control": "unresolved-edge@observed is registered and IS covered by the sweep",
                            "present": bool(observed), "row": observed[0] if observed else None})
results["controls"].append({"control": "reachability is one-rung AND resolved: not-applicable must refuse",
                            "row": reachability[0] if reachability else None})
if reachability and (reachability[0]["ladderLength"] != 1 or not reachability[0]["rungIsResolved"]):
    results["failures"].append("reachability control lost its shape")

# a generic 'one rung => not-applicable' rule would have admitted not-applicable here; it must not
one_rung_not_applicable = attempt("reachability", "from-resolved-calls", NOT_APPLICABLE)
results["controls"].append({"control": "one-rung-count is NOT the rule: reachability@from-resolved-calls "
                                       "with not-applicable must refuse",
                            "result": one_rung_not_applicable["result"],
                            "faults": one_rung_not_applicable["faults"]})
if one_rung_not_applicable["result"] != "REFUSE":
    results["failures"].append("a one-rung resolved relation accepted not-applicable")

# unknown relation and unknown rung: refuse, and never fall back to not-applicable
for label, relation, rung in (("unknown-relation", "no-such-relation", "observed"),
                              ("unknown-rung", "unresolved-edge", "no-such-rung"),
                              ("cross-relation-rung", "unresolved-edge", "resolved-binding")):
    out = attempt(relation, rung, NOT_APPLICABLE)
    results["controls"].append({"control": label + " refuses; not-applicable is not a fallback",
                                "pair": relation + "@" + rung, "result": out["result"],
                                "refusals": out["refusals"], "faults": out["faults"],
                                "error": out.get("error")})
    if out["result"] == "ADMIT":
        results["failures"].append("unregistered pair admitted: " + relation + "@" + rung)

# RC-2 must be untouched for the resolved rungs: a zero count with a non-complete stage stays partial
rc2 = {"state": "complete", "attempted": True, "examinedExhaustive": True,
       "stageTerminal": "budget-exhausted", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}
out = attempt("references", "resolved-binding", rc2)
results["controls"].append({"control": "RC-2 preserved: complete with a non-complete stage still refuses",
                            "result": out["result"], "faults": out["faults"]})
if out["result"] != "REFUSE":
    results["failures"].append("RC-2 weakened")

# examined-vs-resolution distinction preserved: coverage=complete with state=incomplete (RC-3) admits
scope = copy.deepcopy(FIXTURES["scopeDescriptor"])
commitment = N.subject_scope_commitment(scope)
payload = copy.deepcopy(FIXTURES["coveragePayload"])
payload["entry"]["resolutionCompleteness"] = {"state": "incomplete", "attempted": True,
                                              "examinedExhaustive": True, "stageTerminal": "complete",
                                              "unresolvedEdgeCount": 1,
                                              "unresolvedEdgeClasses": ["unresolved-module-specifier"]}
facts = [{"relation": "references", "referrer": "src/a.ts#foo",
          "edgeKind": "unresolved-module-specifier"}]
rc3 = N.admit_coverage_result_v3(payload, scope, facts)
results["controls"].append({"control": "RC-3 preserved: coverage=complete with state=incomplete admits",
                            "result": rc3["result"], "faults": [f["fault"] for f in rc3["faults"]],
                            "refusals": rc3["refusals"]})
if rc3["result"] != "ADMIT":
    results["failures"].append("RC-3 honest entry no longer admits")

results["ok"] = not results["failures"]
print(json.dumps(results, indent=1))
sys.exit(0 if results["ok"] else 1)
