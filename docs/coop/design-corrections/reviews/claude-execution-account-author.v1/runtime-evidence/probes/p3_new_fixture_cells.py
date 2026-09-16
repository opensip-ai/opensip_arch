"""Probe: do the new default-OFF graph-fixture cells build, admit and derive as intended?"""
import importlib.util
import json
from pathlib import Path

SRC = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source/docs/coop/design-corrections/foundation")


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, SRC / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = load("p3_model", "execution_inputs_model.v1.py")
F = load("p3_graph", "evaluator_graph_fixture.v3.py")
H = load("p3_capture", "execution_inputs_fixture.v3.py")

out = {}

# Byte-identity of the untouched default caller.
base = F.build_file_inputs()
out["defaultCellCount"] = len(base["enumerationPlan"]["cells"])
out["defaultPlanId"] = base["inputs"]["planId"]

for label, kwargs in [
    ("unsupported-required", {"unsupported_cell": "required"}),
    ("unsupported-optional", {"unsupported_cell": "optional"}),
    ("optional-unselected", {"optional_unselected_cell": True}),
    ("both", {"unsupported_cell": "required", "optional_unselected_cell": True}),
]:
    row = {"kwargs": kwargs}
    try:
        g = F.build_file_inputs(**kwargs)
        kw = H.admission_kwargs(g)
        adm = M.admit_execution_inputs(**kw)
        row["result"] = adm.get("result")
        row["refusals"] = adm.get("refusals")
        row["accounts"] = [
            {"cell": a["cellOrdinal"], "po": a["programOrdinal"], "rel": a["relation"],
             "rung": a["resolution"], "state": a.get("accountState"),
             "def": a.get("deficiency"), "cause": a.get("nativeCause"),
             "records": len(a.get("coverageRecords") or [])}
            for a in adm.get("derivedAccounts") or []
        ]
        row["manifestAccounts"] = [
            {"cell": a["cellOrdinal"], "rel": a["relation"], "app": a["applicability"],
             "srcU": a["sourceUniverse"], "tgtU": a["targetUniverse"], "covIds": a["coverageIds"]}
            for a in kw["execution_inputs"]["nativeCoverageAccounts"]
        ]
        row["outcomes"] = [
            {"cell": o["cellOrdinal"], "cap": o["capabilityId"], "state": o["state"],
             "def": o["deficiency"], "cause": o["nativeCause"],
             "stageOrdinal": o["stageOrdinal"], "nullReason": o["stageOrdinalNullReason"]}
            for o in kw["execution_inputs"]["cellOutcomes"]
        ]
        row["requiredCellDeficiencies"] = [
            {"cause": d.get("cause"), "rel": d.get("relation"), "def": d.get("deficiency"),
             "nativeCause": d.get("nativeCause"), "refs": d.get("inputRefs")}
            for d in adm.get("requiredCellDeficiencies") or []
        ]
        sel = kw["execution_inputs"]["selectedRefs"]
        row["selectedCoverageCount"] = sum(1 for r in sel if r["domain"] == "coverage")
        named = {c for a in kw["execution_inputs"]["nativeCoverageAccounts"] for c in a["coverageIds"]}
        row["selectedCoverageNotNamedByAnyAccount"] = sorted(
            r["digest"] for r in sel if r["domain"] == "coverage" and r["digest"] not in named
        )
    except Exception as exc:  # noqa: BLE001
        row["error"] = f"{type(exc).__name__}: {exc}"
    out[label] = row

print(json.dumps(out, indent=2, default=str))
