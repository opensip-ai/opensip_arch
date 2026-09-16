"""Probe: why is censusMissing empty on the rebuilt typed-census control?"""
import importlib.util
import json
from pathlib import Path

SRC = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source/docs/coop/design-corrections/foundation")
spec = importlib.util.spec_from_file_location("chk", SRC / "check-execution-inputs.v1.py")
K = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K)

M, F, H = K.M, K.F, K.H

graph_missing = F.build_file_inputs(complete_required_native=False)
owner_missing = K.manifest_from_owner(graph_missing)
kw = K.replace_file_view_with_one_subject(owner_missing, complete=False, rebuild=True)

out = {}
out["cellOutcomes"] = kw["execution_inputs"]["cellOutcomes"]
out["accounts"] = kw["execution_inputs"]["nativeCoverageAccounts"]
out["inventoryKeys"] = sorted(kw["inventories"])
out["inventoryRows"] = {
    d: {"kind": inv["kind"], "cell": inv["cellOrdinal"], "rows": [r["nativeSubjectId"] for r in inv["rows"]]}
    for d, inv in kw["inventories"].items()
}
scopes = {k: v for k, (dom, v) in kw["objects"].items() if dom == "subject-scope"}
out["scopes"] = {k: {"relation": v["relation"], "subjects": v["subjects"]} for k, v in scopes.items()}
out["views"] = {
    k: {"scopeIds": v["scopeIds"], "coverageIds": v["coverageIds"]}
    for k, (dom, v) in kw["objects"].items() if dom == "view"
}
adm = M.admit_execution_inputs(**kw)
out["result"] = adm["result"]
out["refusals"] = adm["refusals"]
out["derivedAccounts"] = adm["derivedAccounts"]

cell = kw["enumeration_plan"]["cells"][0]
binding = cell["programBindings"][0]
row = kw["execution_inputs"]["cellOutcomes"][0]
out["expectedCensus"] = sorted(M.expected_source_census(
    "file", cell, binding, kw["inventories"], row["inventoryDigests"]))
out["rowInventoryDigests"] = row["inventoryDigests"]
print(json.dumps(out, indent=2, default=str))
