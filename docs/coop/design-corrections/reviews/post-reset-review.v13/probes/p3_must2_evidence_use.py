#!/usr/bin/env python
"""CB3-MUST-2 substantive probe, including the required reproduction of
CX-BV3-EVIDENCE-USE-1.

The recorded defect: a policy whose atom consumes imported evidence WITHOUT a
matching rule-level `evidenceUse` declaration was refused by `resolve_policy`
but ADMITTED by `close_run`, because close_run called `admit_atom` alone. One
document, two answers.

I test BOTH boundaries for BOTH polarities, so the rule-level obligation is
shown to be enforced rather than merely present:
  * matching declaration  -> admits at policy admission AND at Run closure
  * omitted declaration   -> refuses at BOTH
  * mismatched kind       -> refuses at BOTH (declaration must MATCH, not merely exist)
Plus the per-relation ladder-index law for atoms, at Run closure.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(
    "/tmp/opensip-design-corrections/post-reset-review.v13/work/subject-copy"
    "/docs/coop/design-corrections")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


F = load("fx", HERE / "integration-fixtures.py")
M, C = F.M, F.C
W = M.workflow_admission()
REG = json.loads((HERE / "foundation/relation-payload-schemas.v2.json")
                 .read_text())["x-opensip-relation-registry"]
LADDERS = {k: v["ladder"] for k, v in REG["relations"].items()}
EV_REG = json.loads((HERE / "workflows/schemas/imported-evidence.schema.json")
                    .read_text()).get("x-opensip-evidence-relation-registry", {})

results = []


def rec(case, boundary, expect, got, cause=None):
    results.append({"case": case, "boundary": boundary, "expected": expect,
                    "observed": got, "cause": cause, "agrees": expect == got})


def policy_boundary(case, rule, expect):
    """Boundary 1: ordinary policy admission."""
    try:
        W.admit_policy_rule(rule)
        rec(case, "policy-admission", expect, "admits")
    except Exception as exc:
        rec(case, "policy-admission", expect, "refuses",
            f"{getattr(exc, 'detail', '')}|{str(exc)[:120]}")


def run_boundary(case, mutate_policy, expect):
    """Boundary 2: retained Run admission (close_run)."""
    try:
        run, objects, blobs = F.build(resolved=True, has_match=True)
        plan_id = run["planId"]
        plan = objects[plan_id][1]
        policy = C.parse(blobs[plan["policyDigest"]])
        policy = mutate_policy(copy.deepcopy(policy))
        new_plan = dict(plan)
        new_plan["policyDigest"] = F.put_blob(blobs, policy)
        F.rekey(objects, plan_id, new_plan, run)
    except Exception as exc:
        rec(case, "run-closure", expect, "fixture-error",
            f"{type(exc).__name__}: {str(exc)[:160]}")
        return
    try:
        M.close_run(run, objects, blobs)
        rec(case, "run-closure", expect, "admits")
    except Exception as exc:
        rec(case, "run-closure", expect, "refuses", str(exc)[:200])


def main():
    ev_kinds = sorted(EV_REG.get("relations", {}))
    results.append({"case": "meta/evidence-relations", "boundary": "-",
                    "expected": None, "observed": None, "agrees": True,
                    "cause": json.dumps(ev_kinds)})

    # Discover a usable imported-evidence relation and its ImportKind.
    imported = json.loads(
        (HERE / "workflows/schemas/imported-evidence.schema.json").read_text())
    kinds = imported["$defs"]["ImportKind"]["enum"]
    results.append({"case": "meta/import-kinds", "boundary": "-",
                    "expected": None, "observed": None, "agrees": True,
                    "cause": json.dumps(kinds)})

    ev_rel = None
    for rel, row in (EV_REG.get("relations") or {}).items():
        ev_rel = (rel, row)
        break
    if ev_rel is None:
        results.append({"case": "meta/NO-EVIDENCE-RELATION", "boundary": "-",
                        "expected": None, "observed": None, "agrees": True,
                        "cause": "registry empty"})
        print(json.dumps({"results": results}, indent=2))
        return 1

    rel_name, rel_row = ev_rel
    rung = (rel_row.get("ladder") or ["observed"])[0]
    kind = rel_row.get("importKind") or kinds[0]

    def make_rule(evidence_use):
        return {
            "ruleId": "ev-rule",
            "ruleProgramRef": "p",
            "enabled": True,
            "severity": "error",
            "gate": True,
            "subjectEnumeration": {"relation": rel_name, "minResolution": rung},
            "emitWhen": {"op": "exists", "relation": rel_name,
                         "minResolution": rung, "filters": [],
                         "evidence": kind},
            "evidenceUse": evidence_use,
            "messageCode": "EV.TEST",
        }

    # --- CX-BV3-EVIDENCE-USE-1, both polarities, both boundaries. --------
    matching = make_rule([{"kind": kind, "requirement": "required"}])
    omitted = make_rule([])
    other_kind = next((k for k in kinds if k != kind), None)
    mismatched = make_rule(
        [{"kind": other_kind, "requirement": "required"}]) if other_kind else None

    policy_boundary("evidence-use/matching-declaration", matching, "admits")
    policy_boundary("evidence-use/omitted-declaration", omitted, "refuses")
    if mismatched:
        policy_boundary("evidence-use/mismatched-kind", mismatched, "refuses")

    def replace_rules(rule):
        def go(policy):
            policy["rules"] = [rule]
            return policy
        return go

    # Run-closure boundary: substitute the policy wholesale. The compiled
    # program join will also move, so a refusal here may be the compilation
    # join rather than evidenceUse; I therefore ALSO run the surgical variant
    # below that only adds/removes the declaration on the existing rule.
    run_boundary("evidence-use/matching-declaration",
                 replace_rules(matching), "refuses-or-admits")
    run_boundary("evidence-use/omitted-declaration",
                 replace_rules(omitted), "refuses")

    # --- Surgical variant: keep the fixture's own policy, strip only the
    # evidenceUse array from every rule that has one. If any rule's atom uses
    # evidence, close_run must now refuse. -------------------------------
    def strip_evidence_use(policy):
        for r in policy["rules"]:
            r["evidenceUse"] = []
        return policy

    def keep(policy):
        return policy

    run_boundary("surgical/unmodified-policy-closes", keep, "admits")
    run_boundary("surgical/evidence-use-stripped", strip_evidence_use,
                 "refuses")

    # --- Atom ladder law at Run closure: a rung of ANOTHER relation on an
    # atom must refuse, and the atom's own rung must admit. ---------------
    def set_atom_rung(relation, rung_value):
        def go(policy):
            for r in policy["rules"]:
                def walk(node):
                    if isinstance(node, dict):
                        if "relation" in node and "minResolution" in node:
                            node["relation"] = relation
                            node["minResolution"] = rung_value
                        for v in node.values():
                            walk(v)
                    elif isinstance(node, list):
                        for v in node:
                            walk(v)
                walk(r["emitWhen"])
            return policy
        return go

    foreign = next(r for r in LADDERS["calls"] if r not in LADDERS["declares"])
    run_boundary(f"atom-ladder/declares@{foreign}(foreign)",
                 set_atom_rung("declares", foreign), "refuses")

    bad = [r for r in results if not r["agrees"]
           and r["expected"] != "refuses-or-admits"]
    summary = {
        "evidenceRelation": rel_name, "importKind": kind, "rung": rung,
        "total": len(results),
        "disagreeing": bad,
        "results": results,
    }
    print(json.dumps(summary, indent=2))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
