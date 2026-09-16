"""Probe: can the owner fixture helper mint a LAWFUL native unknown Coverage for a
selected-U UNSUPPORTED-TYPED capability, admitted by the native owner itself?

Read-only against the successor source; writes nothing outside this runtime.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

SRC = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source/docs/coop/design-corrections/foundation")


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, SRC / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = load("p1_model", "execution_inputs_model.v1.py")
F = load("p1_graph", "evaluator_graph_fixture.v3.py")

out = {}

# 1. Matrix cells that are UNSUPPORTED-TYPED, with their relation pairs and kinds.
rows = []
for (cap, mode), row in M.CELL_STATE.items():
    if row.get("state") == "UNSUPPORTED-TYPED":
        rows.append({
            "capability": cap, "mode": mode, "deficiency": row.get("deficiency"),
            "matrixCause": M._matrix_cause(row.get("deficiency")),
            "pairs": M._matrix_pairs(cap), "kinds": M._cap_kinds(cap),
        })
out["unsupportedTypedCells"] = rows
out["kindMapKeys"] = sorted(M.KIND_MAP)

# 2. Mint a references@resolved-binding scope in the fixture's own syntax universe and let the
#    native owner decide the pair.
g = F.build_file_inputs()
H = F.fixture_helpers()
objects, blobs = g["objects"], g["blobs"]
snapshot_id = g["inputs"]["plan"]["snapshotId"]
uni = g["enumerationPlan"]["cells"][0]["programBindings"][0]["universe"]
provider = g["enumerationPlan"]["cells"][0]["programBindings"][0]["enumerator"]["closureId"]
paths = [r["path"] for r in objects[snapshot_id][1]["sourceInventory"]]
cov_schema = H.N.schema_document_digest(H.N.NATIVE_SCHEMA_DOC)

probe_pairs = [
    ("references", "resolved-binding", ["x"]),
    ("imports", "resolved-target", []),
    ("unresolved-edge", "observed", []),
]
minted = []
for rel, rung, subjects in probe_pairs:
    scope = {
        "schemaVersion": 2, "snapshotId": snapshot_id, "sourceUniverse": uni,
        "targetUniverse": uni, "relation": rel, "resolution": rung,
        "enumeratorClosure": provider, "subjects": subjects,
    }
    try:
        payload = H.coverage_result(scope, uni, True, blobs, paths)
    except Exception as exc:  # noqa: BLE001
        minted.append({"relation": rel, "resolution": rung, "mintError": repr(exc)})
        continue
    admitted = H.N.admit_coverage_result_v3(payload, scope, [], cov_schema)
    entry = payload.get("entry") or {}
    minted.append({
        "relation": rel, "resolution": rung,
        "admitted": admitted.get("result"),
        "coverage": entry.get("coverage"),
        "deficiency": entry.get("deficiency"),
        "nativeCause": entry.get("nativeCause"),
        "resolutionCompleteness": entry.get("resolutionCompleteness"),
        "admittedDetail": None if admitted.get("result") == "ADMIT" else admitted,
    })
out["mintedUnsupportedCoverage"] = minted

# 3. The relation registry subject kinds for those relations.
out["subjectKinds"] = {
    rel: (M.RELATIONS.get(rel) or {}).get("subjectKind")
    for rel in ("references", "imports", "unresolved-edge", "file", "package", "vcs-change", "clones")
}

# 4. Current first-match applicability table (BEFORE the correction).
cases = [
    ("vcs-change", None, "unselected", "UNSUPPORTED-TYPED", "none"),
    ("file", None, "unselected", "UNSUPPORTED-TYPED", "git"),
    ("file", None, "unselected", "SUPPORTED-DESIGN", "git"),
    ("file", None, "selected", "SUPPORTED-DESIGN", "git"),
    ("file", "a" * 64, "selected", "SUPPORTED-DESIGN", "git"),
    ("vcs-change", "a" * 64, "selected", "SUPPORTED-DESIGN", "none"),
    ("vcs-change", "a" * 64, "selected", "SUPPORTED-DESIGN", "git"),
]
out["applicabilityBefore"] = [
    {"args": list(c), "token": M.derived_applicability(*c)} for c in cases
]

print(json.dumps(out, indent=2, default=str))
