"""P2 v2: do the maintained run-termination goldens discriminate, including the v2 combined and projection rows?

Runs the MAINTAINED `check-semantic-replay.v3.run_termination_goldens` from THIS runtime's source copy over the
same exported closed Runs, once with the reference model and once per mutant. A mutant replaces one law in a
freshly loaded model instance handed to the checker through its own `load` hook; the checker body, goldens and
closed Runs are unchanged. Writes nothing into any tree; stdout only.
"""
import importlib.util
import json
import sys
from pathlib import Path

SRC = Path("/private/tmp/opensip-design-corrections/claude-source37-host-finalizer-author.v2/source")
FOUNDATION = SRC / "docs/coop/design-corrections/foundation"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


SR = load("p2v2_semantic_replay", FOUNDATION / "check-semantic-replay.v3.py")
exports = {
    "references-incoming-incomplete-unknown": SR.case_incoming_incomplete_unknown()[1],
    "missing-required-inventory-execution": SR.case_missing_inventory_execution()[1],
}
original_load = SR.load


def fresh_model(tag):
    return load("p2v2_run_termination_" + tag, FOUNDATION / "run_termination_model.v1.py")


def wrap_reduce(T, change):
    reduce = T.reduce

    def mutated(conds):
        r = reduce(conds)
        change(r, conds)
        return r
    T.reduce = mutated


def least_deficient_anywhere(T):
    def change(r, conds):
        pool = sorted({cid for c in conds for cid in c["declaredCarriers"] + c["stageCarriers"]}, key=str.encode)
        r["coverageId"] = pool[0] if pool else None
    wrap_reduce(T, change)


def ignore_stage_terminals(T):
    conditions = T.conditions
    T.conditions = lambda population, objects, blobs, xi: [c for c in conditions(population, objects, blobs, xi) if c["origin"] != "stage-terminal"]


def work_budget_not_reused(T):
    route = T.cause_route
    T.cause_route = lambda cause: ({"rank": T.EVALUATOR_ONLY_RANK, "d9Deficiency": "verdict-indeterminate"}
                                   if cause == T.WORK_BUDGET else route(cause))


def discovery_order_primary(T):
    def change(r, conds):
        first = conds[0]
        r["reasonCodes"] = T.d9_concurrent_reducer([c["d9Deficiency"] for c in conds])
        r["deficiency"] = first["d9Deficiency"]
        r["secondaryDeficiencies"] = [d for d in dict.fromkeys(c["d9Deficiency"] for c in conds) if d != first["d9Deficiency"]]
        r["coverageId"] = (first["declaredCarriers"] + first["stageCarriers"] + [None])[0]
    wrap_reduce(T, change)


def carrier_always_omitted(T):
    wrap_reduce(T, lambda r, conds: r.update(coverageId=None))


def omit_carrier_when_work_budget_present(T):
    """v1 section 5 sentence 3 read literally: omission 'for work-budget-exhausted' whatever else shares its rank."""
    def change(r, conds):
        if any(c["cause"] == T.WORK_BUDGET and T.CODE_MAP[c["d9Deficiency"]] == r["reasonCodes"][0] for c in conds):
            r["coverageId"] = None
            r["carrierKind"] = None
    wrap_reduce(T, change)


def whole_termination_equality(T):
    """v1 check_candidate: exact equality of the whole StepTermination (bans every delegated member)."""
    def strict(candidate, derived, validate_shape=None):
        if candidate != derived:
            raise T.RunTerminationError("RUN_TERMINATION_NOT_DERIVED:strict")
        return {"projection": derived, "delegated": {}, "delegatedOwners": {}, "delegatedStanding": None}
    T.check_projection = strict


def delegated_members_unvalidated(T):
    """Admit delegated members without any shape validation."""
    check = T.check_projection
    T.check_projection = lambda candidate, derived, validate_shape=None: check(candidate, derived, lambda _c: None)


def delegated_members_reported_lawful(T):
    check = T.check_projection

    def lawful(candidate, derived, validate_shape=None):
        got = check(candidate, derived, validate_shape)
        if got["delegated"]:
            got["delegatedStanding"] = "lawful"
        return got
    T.check_projection = lawful


def unknown_members_passed_through(T):
    """Treat any non-projection member as delegated (arbitrary extras)."""
    check = T.check_projection

    def loose(candidate, derived, validate_shape=None):
        extra = {k: v for k, v in candidate.items() if k not in T.PROJECTION_FIELDS and k not in T.DELEGATED_FIELDS}
        trimmed = {k: v for k, v in candidate.items() if k not in extra}
        got = check(trimmed, derived, validate_shape)
        got["delegated"].update(extra)
        return got
    T.check_projection = loose


MUTANTS = {"reference": None, "least-deficient-anywhere": least_deficient_anywhere,
           "ignore-stage-terminals": ignore_stage_terminals, "work-budget-not-reused": work_budget_not_reused,
           "discovery-order-primary": discovery_order_primary, "carrier-always-omitted": carrier_always_omitted,
           "omit-carrier-when-work-budget-present": omit_carrier_when_work_budget_present,
           "whole-termination-equality": whole_termination_equality,
           "delegated-members-unvalidated": delegated_members_unvalidated,
           "delegated-members-reported-lawful": delegated_members_reported_lawful,
           "unknown-members-passed-through": unknown_members_passed_through}
out = {}
for name, mutate in MUTANTS.items():
    T = fresh_model(name.replace("-", "_"))
    if mutate:
        mutate(T)
    SR.load = lambda n, f, _T=T: _T if f == "run_termination_model.v1.py" else original_load(n, f)
    try:
        rows = SR.run_termination_goldens(exports)
    finally:
        SR.load = original_load
    failing = {r["case"]: (r.get("faults") or [])[:2] for r in rows if r.get("faults")}
    out[name] = {"rows": len(rows), "failingRows": sorted(failing), "firstFaults": failing}
out["discriminating"] = {name: bool(v["failingRows"]) for name, v in out.items() if name != "reference"}
out["referencePasses"] = not out["reference"]["failingRows"]
print(json.dumps(out, indent=1))
