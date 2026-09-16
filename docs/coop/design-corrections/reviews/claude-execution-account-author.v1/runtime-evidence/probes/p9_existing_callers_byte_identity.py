"""Probe: do the graph-fixture additions leave every EXISTING caller byte-identical?

Loads the preserved BEFORE image of evaluator_graph_fixture.v3.py in memory and compares the
built graph against the edited module for every option combination existing callers use.
Nothing is written into the source.
"""
import hashlib
import importlib.util
import json
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SRC = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source/docs/coop/design-corrections/foundation")
BEFORE_IMAGE = HERE / "before" / "docs__coop__design-corrections__foundation__evaluator_graph_fixture.v3.py"


def load_after():
    spec = importlib.util.spec_from_file_location("after_graph", SRC / "evaluator_graph_fixture.v3.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_before():
    path = SRC / "evaluator_graph_fixture.v3.py"
    mod = types.ModuleType("before_graph")
    mod.__file__ = str(path)
    mod.__name__ = "before_graph"
    exec(compile(BEFORE_IMAGE.read_text(), str(path), "exec"), mod.__dict__)
    return mod


A = load_after()
B = load_before()
C = A.C


def fingerprint(g):
    return {
        "planId": g["inputs"]["planId"],
        "executionPlanId": g["inputs"]["executionPlanId"],
        "enumerationPlan": hashlib.sha256(C.canonical(g["enumerationPlan"])).hexdigest(),
        "objectKeys": hashlib.sha256(C.canonical(sorted(g["objects"]))).hexdigest(),
        "blobDigests": hashlib.sha256(C.canonical(sorted(g["blobs"]))).hexdigest(),
        "inventoryResults": hashlib.sha256(C.canonical([d for d, _ in g["inventoryResults"]])).hexdigest(),
        "viewIds": hashlib.sha256(C.canonical(list(g["viewIds"]))).hexdigest(),
        "evaluationInputRefs": hashlib.sha256(C.canonical(list(g["inputs"]["evaluationInputRefs"]))).hexdigest(),
    }


CALLS = {
    "default": {},
    "none-atom": {"atom_override": {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []}},
    "missing-required-package": {"complete_required_native": False},
    "multiple-universes": {"multiple_universes": True},
    "symbol-rows": {"symbol_rows": [{"nativeSubjectId": "x"}]},
    "symbol-rows-partial": {"symbol_rows": [{"nativeSubjectId": "x"}], "symbol_state": "partial"},
    "select-exports": {"symbol_rows": [{"nativeSubjectId": "x"}], "select_exports": True},
    "symbol-only-second-program": {"multiple_universes": True, "symbol_rows": [{"nativeSubjectId": "x"}],
                                   "symbol_only_second_program": True},
    "disabled-rule": {"enabled": False},
    "no-gate": {"gate": False},
    "additional-disabled-rule": {"additional_disabled_rule": True},
    "budget": {"budget_limit": 1},
    "waivers": {"waiver_rows": []},
    "enumeration-filter": {"enumeration_filter": {"pathPrefixes": ["src/"]}},
    "two-universes-complete-required": {"multiple_universes": True, "complete_required_native": True},
}

rows = {}
for name, kwargs in CALLS.items():
    try:
        fb = fingerprint(B.build_file_inputs(**kwargs))
    except Exception as exc:  # noqa: BLE001
        fb = {"error": f"{type(exc).__name__}: {exc}"}
    try:
        fa = fingerprint(A.build_file_inputs(**kwargs))
    except Exception as exc:  # noqa: BLE001
        fa = {"error": f"{type(exc).__name__}: {exc}"}
    rows[name] = {
        "identical": fb == fa,
        "differingFields": sorted(k for k in set(fb) | set(fa) if fb.get(k) != fa.get(k)),
        "before": fb if fb != fa else None,
        "after": fa if fb != fa else None,
    }

print(json.dumps({
    "allExistingCallersIdentical": all(r["identical"] for r in rows.values()),
    "calls": rows,
}, indent=2, default=str))
