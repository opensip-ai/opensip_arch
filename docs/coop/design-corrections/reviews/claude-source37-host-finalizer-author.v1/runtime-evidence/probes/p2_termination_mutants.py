"""P2: do the maintained run-termination goldens discriminate? Mutated derivation laws must each fail them.

Runs the MAINTAINED `check-semantic-replay.v3.run_termination_goldens` from THIS runtime's source copy over the
same exported closed Runs, once with the reference model and once per mutant. A mutant replaces one law in a
freshly loaded model instance handed to the checker through its own `load` hook; the checker body, goldens and
closed Runs are unchanged. Writes nothing into any tree; stdout only.
"""
import importlib.util
import json
import sys
from pathlib import Path

SRC = Path("/private/tmp/opensip-design-corrections/claude-source37-host-finalizer-author.v1/source")
FOUNDATION = SRC / "docs/coop/design-corrections/foundation"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


SR = load("p2_semantic_replay", FOUNDATION / "check-semantic-replay.v3.py")
exports = {
    "references-incoming-incomplete-unknown": SR.case_incoming_incomplete_unknown()[1],
    "missing-required-inventory-execution": SR.case_missing_inventory_execution()[1],
}
original_load = SR.load


def fresh_model(tag):
    return load("p2_run_termination_" + tag, FOUNDATION / "run_termination_model.v1.py")


def least_deficient_anywhere(T):
    """coverageId = least coverage2 whose entry declares ANY deficiency among the population's originating records."""
    reduce = T.reduce

    def mutated(conds):
        r = reduce(conds)
        pool = sorted({cid for c in conds for cid in c["declaredCarriers"] + c["stageCarriers"]}, key=str.encode)
        r["coverageId"] = pool[0] if pool else None
        return r
    T.reduce = mutated


def ignore_stage_terminals(T):
    conditions = T.conditions
    T.conditions = lambda population, objects, blobs, xi: [c for c in conditions(population, objects, blobs, xi) if c["origin"] != "stage-terminal"]


def work_budget_not_reused(T):
    route = T.cause_route
    T.cause_route = lambda cause: ({"rank": T.EVALUATOR_ONLY_RANK, "d9Deficiency": "verdict-indeterminate"}
                                   if cause == T.WORK_BUDGET else route(cause))


def discovery_order_primary(T):
    """The verbatim D9 reducer over conditions in the order they were discovered; coverageId from that first condition."""
    reduce = T.reduce

    def mutated(conds):
        r = reduce(conds)
        codes = T.d9_concurrent_reducer([c["d9Deficiency"] for c in conds])
        first = conds[0]
        r["reasonCodes"] = codes
        r["deficiency"] = first["d9Deficiency"]
        r["secondaryDeficiencies"] = [d for d in dict.fromkeys(c["d9Deficiency"] for c in conds) if d != first["d9Deficiency"]]
        r["coverageId"] = (first["declaredCarriers"] + first["stageCarriers"] + [None])[0]
        return r
    T.reduce = mutated


def carrier_always_omitted(T):
    reduce = T.reduce

    def mutated(conds):
        r = reduce(conds)
        r["coverageId"] = None
        return r
    T.reduce = mutated


MUTANTS = {"reference": None, "least-deficient-anywhere": least_deficient_anywhere,
           "ignore-stage-terminals": ignore_stage_terminals, "work-budget-not-reused": work_budget_not_reused,
           "discovery-order-primary": discovery_order_primary, "carrier-always-omitted": carrier_always_omitted}
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
