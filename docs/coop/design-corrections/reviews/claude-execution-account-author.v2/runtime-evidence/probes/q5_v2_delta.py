"""Probe: the exact v1->v2 behavioural delta, and existing-caller byte identity.

Loads the preserved v2 BEFORE images (= the v1 handoff bytes) in memory and compares them to the
edited modules. Writes nothing into the source.
"""
import hashlib
import importlib.util
import json
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
F = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source/docs/coop/design-corrections/foundation")
B_MODEL = HERE / "before" / "docs__coop__design-corrections__foundation__execution_inputs_model.v1.py"
B_GRAPH = HERE / "before" / "docs__coop__design-corrections__foundation__evaluator_graph_fixture.v3.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_image(image, real_path, name):
    mod = types.ModuleType(name)
    mod.__file__ = str(real_path)
    mod.__name__ = name
    exec(compile(Path(image).read_text(), str(real_path), "exec"), mod.__dict__)
    return mod


A = load("v2_model", F / "execution_inputs_model.v1.py")
B = load_image(B_MODEL, F / "execution_inputs_model.v1.py", "v1_model")
AG = load("v2_graph", F / "evaluator_graph_fixture.v3.py")
BG = load_image(B_GRAPH, F / "evaluator_graph_fixture.v3.py", "v1_graph")
C = A.C
out = {}

# --- 1. derive_outcome: enumerate the source shapes and diff the row pair -----------------
UNI = "c" * 64
AVAIL = {"ordinal": 0, "enumerator": {"status": "selected", "closureId": "closure2:" + "d" * 64},
         "universe": UNI, "extents": []}
UNAVAIL = {"ordinal": 0, "enumerator": {"status": "selected", "closureId": "closure2:" + "d" * 64},
           "universe": None, "extents": [], "deficiency": "input-closure-incomplete",
           "nativeCause": "lockfile-missing"}
UNSEL = {"ordinal": 0, "enumerator": {"status": "unselected", "reason": "optional-unselected"},
         "universe": None, "extents": [], "deficiency": "provider-unavailable", "nativeCause": None}


def acc(rel, deficiency, cause, records):
    return {"accountState": "incomplete", "relation": rel, "resolution": "r",
            "deficiency": deficiency, "nativeCause": cause,
            "coverageRecords": records, "inputRefs": []}


def rec(deficiency, cause):
    return {"deficiency": deficiency, "nativeCause": cause,
            "inputRef": {"domain": "coverage", "digest": "a" * 64}, "coverageId": "a" * 64}


def inv(state, deficiency, cause):
    return {"state": state, "deficiency": deficiency, "nativeCause": cause, "digest": "b" * 64}


CASES = {
    "untyped-account-then-typed-account": dict(
        account_summaries=[acc("file", None, None, []),
                           acc("package", "budget-exhausted", None, [rec("budget-exhausted", None)])]),
    "typed-account-then-untyped-account": dict(
        account_summaries=[acc("file", "budget-exhausted", None, [rec("budget-exhausted", None)]),
                           acc("package", None, None, [])]),
    "all-untyped-accounts": dict(account_summaries=[acc("file", None, None, []),
                                                    acc("package", None, None, [])]),
    "typed-inventory-then-untyped-account": dict(
        inventories=[inv("partial", "budget-exhausted", None)],
        account_summaries=[acc("file", None, None, [])]),
    "untyped-inventory-then-typed-account": dict(
        inventories=[inv("partial", None, None)],
        account_summaries=[acc("file", "budget-exhausted", None, [rec("budget-exhausted", None)])]),
    "unselected-binding-with-inventory": dict(
        enumerator_status="unselected", universe=None, binding=UNSEL,
        inventories=[inv("unavailable", "provider-unavailable", None)], account_summaries=[]),
    "null-universe-binding-with-inventory": dict(
        universe=None, binding=UNAVAIL,
        inventories=[inv("partial", "budget-exhausted", None)], account_summaries=[]),
    "candidate-absent-available-binding": dict(candidate_cap=True, candidate_rec=None,
                                               account_summaries=[]),
    "candidate-unavailable-typed-envelope": dict(
        candidate_cap=True, candidate_digest="e" * 64,
        candidate_rec={"state": "unavailable", "deficiency": "budget-exhausted", "nativeCause": None},
        account_summaries=[]),
    "candidate-unavailable-untyped-envelope": dict(
        candidate_cap=True, candidate_digest="e" * 64,
        candidate_rec={"state": "unavailable", "deficiency": None, "nativeCause": None},
        account_summaries=[]),
    "all-complete": dict(account_summaries=[]),
}
rows = []
for name, over in CASES.items():
    kw = dict(enumerator_status="selected", universe=UNI, required=True, inventories=[],
              account_summaries=[], candidate_rec=None, candidate_digest=None,
              candidate_cap=False, binding=AVAIL)
    kw.update(over)
    rb = B.derive_outcome(**json.loads(json.dumps(kw)))
    ra = A.derive_outcome(**json.loads(json.dumps(kw)))
    same_sources = ([(s.get("source"), s.get("deficiency"), s.get("nativeCause"), s.get("inputRefs"))
                     for s in rb["sources"]]
                    == [(s.get("source"), s.get("deficiency"), s.get("nativeCause"), s.get("inputRefs"))
                        for s in ra["sources"]])
    rows.append({
        "case": name,
        "state": [rb["state"], ra["state"]],
        "stateUnchanged": rb["state"] == ra["state"],
        "rowPairBefore": [rb["deficiency"], rb["nativeCause"]],
        "rowPairAfter": [ra["deficiency"], ra["nativeCause"]],
        "rowPairChanged": (rb["deficiency"], rb["nativeCause"]) != (ra["deficiency"], ra["nativeCause"]),
        "sourcesUnchanged": same_sources,
        "inputRefsUnchanged": rb["inputRefs"] == ra["inputRefs"],
        "nativeCausesUnchanged": rb["nativeCauses"] == ra["nativeCauses"],
    })
out["deriveOutcome"] = {
    "rows": rows,
    "everyStateUnchanged": all(r["stateUnchanged"] for r in rows),
    "everySourceListUnchanged": all(r["sourcesUnchanged"] for r in rows),
    "everyInputRefListUnchanged": all(r["inputRefsUnchanged"] for r in rows),
    "everyNativeCauseListUnchanged": all(r["nativeCausesUnchanged"] for r in rows),
    "changedRowPairs": [r["case"] for r in rows if r["rowPairChanged"]],
}

# --- 2. graph fixture: every existing caller shape byte-identical --------------------------
def fingerprint(g):
    return {
        "planId": g["inputs"]["planId"],
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
    "symbol-only-second-program": {"multiple_universes": True, "symbol_rows": [{"nativeSubjectId": "x"}],
                                   "symbol_only_second_program": True},
    "v1-unsupported-required": {"unsupported_cell": "required"},
    "v1-optional-unselected": {"optional_unselected_cell": True},
    "v1-file-coverage-subjects": {"file_coverage_subjects": ["README.md"]},
    "disabled-rule": {"enabled": False},
    "additional-disabled-rule": {"additional_disabled_rule": True},
}
calls = {}
for name, kwargs in CALLS.items():
    fb = fingerprint(BG.build_file_inputs(**kwargs))
    fa = fingerprint(AG.build_file_inputs(**kwargs))
    calls[name] = {"identical": fb == fa,
                   "differing": sorted(k for k in fb if fb[k] != fa.get(k))}
out["graphFixtureCallers"] = {
    "allIdentical": all(v["identical"] for v in calls.values()),
    "calls": calls,
}

print(json.dumps(out, indent=2, default=str))
