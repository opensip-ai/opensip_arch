"""Probe: drive the new fixture cells through a full retained Run (R.derive -> M.close_run).

Mirrors foundation/check-execution-replay.v3.py's own derive() path; no new admission route.
"""
import importlib.util
import json
from pathlib import Path

SRC = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source/docs/coop/design-corrections/foundation")


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, SRC / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


F = load("p4_graph", "evaluator_graph_fixture.v3.py")
R = load("p4_replay", "evaluator_replay_model.v3.py")
S = load("p4_semantic", "evaluator_semantic_fixture.v3.py")
X = load("p4_capture", "execution_inputs_fixture.v3.py")
M = R.M


def derive(g):
    seed, objects, blobs, _ = F.seal_fixture(g)
    _, owner = M.open_run_closure(seed, objects, blobs)
    i = g["inputs"]
    out = R.derive(i["planId"], i["executionPlanId"], i["evaluatorClosure"],
                   i["evaluationInputRefs"], objects, blobs, owner)
    run, objects, blobs = S.seal_derived(g, out, objects, blobs)
    result = R.replay(run, objects, blobs)
    assert M.close_run(run, objects, blobs) == result["runId"]
    return result, out["proof"]


NONE_ATOM = {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []}

cases = {}
for label, kwargs in [
    ("baseline", {}),
    ("missing-required-package", {"complete_required_native": False}),
    ("unsupported-required", {"unsupported_cell": "required"}),
    ("unsupported-optional", {"unsupported_cell": "optional"}),
    ("optional-unselected", {"optional_unselected_cell": True}),
    ("unsupported-required+optional-unselected+missing-package",
     {"unsupported_cell": "required", "optional_unselected_cell": True,
      "complete_required_native": False}),
    ("census-missing-expected-subjects", {"file_coverage_subjects": ["README.md"]}),
    ("census-missing+missing-package",
     {"file_coverage_subjects": ["README.md"], "complete_required_native": False}),
]:
    row = {"kwargs": kwargs}
    try:
        g = F.build_file_inputs(atom_override=NONE_ATOM, **kwargs)
        result, proof = derive(g)
        row["verdict"] = result["verdict"]
        row["findingCount"] = result["findingCount"]
        row["runId"] = result["runId"]
        row["executionDeficiencies"] = proof["executionDeficiencies"]
    except Exception as exc:  # noqa: BLE001
        row["error"] = f"{type(exc).__name__}: {exc}"
    cases[label] = row

print(json.dumps(cases, indent=2, default=str))
