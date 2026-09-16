"""Probe: will the native owner admit an `unknown` package@manifest-declared Coverage, and what
pair does its own derivation put on it? Needed for the discriminating mixed-account control.
"""
import importlib.util
import json
from pathlib import Path

F = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source/docs/coop/design-corrections/foundation")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = load("q3_model", F / "execution_inputs_model.v1.py")
Fx = load("q3_graph", F / "evaluator_graph_fixture.v3.py")
H = Fx.fixture_helpers()

g = Fx.build_file_inputs()
objects, blobs = g["objects"], g["blobs"]
snapshot_id = g["inputs"]["plan"]["snapshotId"]
uni = g["enumerationPlan"]["cells"][0]["programBindings"][0]["universe"]
provider = g["enumerationPlan"]["cells"][0]["programBindings"][0]["enumerator"]["closureId"]
paths = [r["path"] for r in objects[snapshot_id][1]["sourceInventory"]]
cov_schema = H.N.schema_document_digest(H.N.NATIVE_SCHEMA_DOC)

out = {"resolvedRungs": sorted(H.N.RESOLVED_RUNGS)}
for label, resolved in (("complete", True), ("unknown", False)):
    scope = {
        "schemaVersion": 2, "snapshotId": snapshot_id, "sourceUniverse": uni,
        "targetUniverse": uni, "relation": "package", "resolution": "manifest-declared",
        "enumeratorClosure": provider, "subjects": [],
    }
    payload = H.coverage_result(scope, uni, resolved, blobs, paths)
    admitted = H.N.admit_coverage_result_v3(payload, scope, [], cov_schema)
    entry = payload.get("entry") or {}
    out[label] = {
        "admitted": admitted.get("result"),
        "coverage": entry.get("coverage"),
        "deficiency": entry.get("deficiency"),
        "nativeCause": entry.get("nativeCause"),
        "resolutionCompleteness": entry.get("resolutionCompleteness"),
        "detail": None if admitted.get("result") == "ADMIT" else admitted,
    }
    # What would the account summary be?
    recs = [{"id": "a" * 64, "entry": entry}]
    summ = M._summarize_coverage_records(recs, set(), set())
    out[label]["accountSummary"] = {
        k: summ.get(k) for k in ("accountState", "deficiency", "nativeCause", "censusMissing")
    }

print(json.dumps(out, indent=2, default=str))
