"""Probe: is a SELECTED-U optional candidate cell with NO retained envelope admissible, and does
it then manufacture a (provider-unavailable, null) pair that no source record carries?

Narrow assessment against actual admission and schema evidence, per root's instruction. Also
re-checks root's cited enumeration_model guards for the binding-carrier fallback.
"""
import copy
import importlib.util
import json
from pathlib import Path

F = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source/docs/coop/design-corrections/foundation")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


K = load("q2_checker", F / "check-execution-inputs.v1.py")
M, H, Fx = K.M, K.H, K.F
out = {}

# --- 0. Root's cited enumeration guards, quoted from the real file -------------------------
lines = (F / "enumeration_model.v1.py").read_text().splitlines()
out["enumerationGuards"] = {
    "lines679_684": [f"{n}: {lines[n-1]}" for n in range(679, 685)],
    "lines752_755": [f"{n}: {lines[n-1]}" for n in range(752, 756)],
}

# --- 1. Does the schema force a typed deficiency on a non-complete candidate envelope? -----
cand_def = M.SCHEMA["$defs"]["CandidateProducerResultV1"]
out["candidateSchema"] = {
    "requiredFields": cand_def["required"],
    "deficiency": cand_def["properties"]["deficiency"],
    "state": cand_def["properties"]["state"],
    "conditionals": cand_def.get("allOf"),
}
probe_env = {
    "schemaVersion": 1, "planId": "plan2:" + "a" * 64, "executionPlanId": "execution2:" + "b" * 64,
    "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "clones-near",
    "languageMode": "syntax-only", "universe": "c" * 64, "producerClosure": "closure2:" + "d" * 64,
    "stageOrdinal": 0, "state": "unavailable", "deficiency": None, "nativeCause": None,
    "authority": "candidate-only", "semanticEquivalenceClaimed": False,
    "automaticDeletionEligible": False, "examinedPaths": [], "groupDigests": [], "sourceBodies": [],
}
schema = {"$defs": M.SCHEMA["$defs"], "allOf": [{"$ref": "#/$defs/CandidateProducerResultV1"}]}
try:
    M.C.validate(schema, probe_env)
    out["unavailableEnvelopeWithNullDeficiencyValidates"] = True
except Exception as exc:  # noqa: BLE001
    out["unavailableEnvelopeWithNullDeficiencyValidates"] = False
    out["unavailableEnvelopeWithNullDeficiencyError"] = f"{type(exc).__name__}: {str(exc)[:300]}"

# --- 2. Admitted control: OPTIONAL clones-near cell, selected U, NO candidate envelope ------
graph = Fx.build_file_inputs()
owner = K.manifest_from_owner(graph)
bodies = [K.source_body(owner, "body-a", "src/index.ts", "c" * 64)]


def near_cell_without_envelope(owner, required):
    """Optional/required clones-near cell with a selected non-null-U binding and NO envelope."""
    kw = copy.deepcopy(owner)
    prov = next(k for k, v in kw["closures"].items() if v.get("kind") == "provider")
    uni = kw["enumeration_plan"]["cells"][0]["programBindings"][0]["universe"]
    enum = copy.deepcopy(kw["enumeration_plan"])
    enum["cells"] = [{
        "capabilityId": "clones-near", "languageMode": "syntax-only", "workspaceRoot": ".",
        "required": required, "kinds": [],
        "programBindings": [{
            "ordinal": 0, "provenance": "default-unit",
            "enumerator": {"status": "selected", "closureId": prov},
            "nativeContextDigest": kw["enumeration_plan"]["cells"][0]["programBindings"][0]["nativeContextDigest"],
            "universe": uni, "programEntry": None, "extents": [],
            "candidateSourcePaths": ["src/index.ts"],
        }],
    }]
    spec = {"requestedCapabilities": [{"capabilityId": "clones-near", "languageMode": "syntax-only",
                                       "workspaceRoot": ".", "required": required}]}
    plan = dict(kw["plan"])
    plan["analysisSpecDigest"] = M.raw_digest(spec)
    stage_d = kw["execution_plan"]["stages"][0]["stageSpecDigest"]
    row = {
        "ordinal": 0, "cellOrdinal": 0, "programOrdinal": 0, "capabilityId": "clones-near",
        "languageMode": "syntax-only", "workspaceRoot": ".", "required": required, "kinds": [],
        "universe": uni, "enumeratorStatus": "selected", "enumeratorClosure": prov,
        "state": "unavailable", "deficiency": "provider-unavailable", "nativeCause": None,
        "stageOrdinal": 0, "stageOrdinalNullReason": None,
        "inventoryDigests": [], "viewDigests": [], "candidateResultDigest": None,
    }
    manifest = {
        "schemaVersion": 1, "planId": kw["plan_id"], "executionPlanId": kw["execution_plan_id"],
        "evaluatorClosure": kw["execution_inputs"]["evaluatorClosure"],
        "enumerationPlanDigest": M.raw_digest(enum), "analysisSpecDigest": plan["analysisSpecDigest"],
        "hostCapture": {
            "custody": "host-tcb-evidence-store", "observation": "stage-return",
            "stageReceipts": [{
                "ordinal": 0, "stageSpecDigest": stage_d,
                "producerClosure": kw["stage_specs"][stage_d]["producerClosure"],
                "outputDomains": list(kw["stage_specs"][stage_d]["outputDomains"]),
                "outputRefs": [], "state": "complete", "unavailableReason": None,
            }],
            "hostDerivedRefs": [],
        },
        "selectedRefs": [], "cellOutcomes": [row], "nativeCoverageAccounts": [],
        "candidateResultRefs": [],
    }
    return {
        "plan_id": kw["plan_id"], "plan": plan, "execution_plan_id": kw["execution_plan_id"],
        "execution_plan": kw["execution_plan"], "enumeration_plan": enum, "analysis_spec": spec,
        "execution_inputs": manifest, "objects": kw["objects"], "blobs": kw["blobs"],
        "store_pointers": K.pointers_of(kw["objects"], kw["blobs"]), "inventories": {},
        "imports": {}, "target_attributions": {}, "incoming_searches": {},
        "candidate_results": {}, "groups": {}, "closures": kw["closures"],
        "stage_specs": kw["stage_specs"], "vcs_observation": kw["vcs_observation"],
    }


for label, required in (("optional", False), ("required", True)):
    kw = near_cell_without_envelope(owner, required)
    adm = M.admit_execution_inputs(**kw)
    out[f"selectedU_{label}_candidate_no_envelope"] = {
        "result": adm["result"], "refusals": adm["refusals"],
        "derivedOutcomes": [
            {k: v for k, v in d.items() if k in ("state", "deficiency", "nativeCause", "inputRefs")}
            for d in adm.get("derivedOutcomes") or []
        ],
        "derivedSources": [
            [(s.get("source"), s.get("deficiency"), s.get("nativeCause"), s.get("inputRefs"))
             for s in (d.get("sources") or [])]
            for d in adm.get("derivedOutcomes") or []
        ],
        "requiredCellDeficiencies": [
            {k: v for k, v in d.items() if k in ("cause", "deficiency", "nativeCause", "inputRefs")}
            for d in adm.get("requiredCellDeficiencies") or []
        ],
    }

# --- 3. Does the binding even have a `deficiency` key on the available shape? --------------
plan_schema = M.PLAN_SCHEMA["$defs"]
out["availableBindingHasDeficiencyProperty"] = (
    "deficiency" in plan_schema["AvailableProgramBindingV1"]["properties"])
out["availableBindingAdditionalProperties"] = plan_schema["AvailableProgramBindingV1"].get(
    "additionalProperties")
out["binding_carrier_on_available_binding"] = list(M._binding_carrier(
    {"ordinal": 0, "enumerator": {"status": "selected", "closureId": "closure2:" + "d" * 64},
     "universe": "c" * 64, "extents": []}))

print(json.dumps(out, indent=2, default=str))
