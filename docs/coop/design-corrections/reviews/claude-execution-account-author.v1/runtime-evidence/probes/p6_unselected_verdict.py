"""Probe: why is the optional-unselected full Run `indeterminate` with no executionDeficiencies?"""
import importlib.util
import json
from pathlib import Path

SRC = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source/docs/coop/design-corrections/foundation")


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, SRC / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


F = load("p6_graph", "evaluator_graph_fixture.v3.py")
R = load("p6_replay", "evaluator_replay_model.v3.py")
S = load("p6_semantic", "evaluator_semantic_fixture.v3.py")
M = R.M

NONE_ATOM = {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []}

out = {}
for label, kwargs in [("baseline", {}), ("optional-unselected", {"optional_unselected_cell": True})]:
    g = F.build_file_inputs(atom_override=NONE_ATOM, **kwargs)
    seed, objects, blobs, _ = F.seal_fixture(g)
    _, owner = M.open_run_closure(seed, objects, blobs)
    i = g["inputs"]
    o = R.derive(i["planId"], i["executionPlanId"], i["evaluatorClosure"],
                 i["evaluationInputRefs"], objects, blobs, owner)
    run, objects, blobs = S.seal_derived(g, o, objects, blobs)
    result = R.replay(run, objects, blobs)
    proof = o["proof"]
    out[label] = {
        "verdict": result["verdict"],
        "evaluationState": proof.get("evaluationState"),
        "executionDeficiencies": proof.get("executionDeficiencies"),
        "ruleResults": proof.get("ruleResults"),
        "enumerationInputs": {
            "enumerations": i["enumerations"],
            "enumerationDeficiencies": i["enumerationDeficiencies"],
        },
        "inventories": [
            {"cell": inv["cellOrdinal"], "kind": inv["kind"], "state": inv["state"]}
            for _d, inv in g["inventoryResults"]
        ],
    }
print(json.dumps(out, indent=2, default=str))
