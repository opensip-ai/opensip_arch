"""Probe: why does the optional-unselected cell fail ENUMERATION_PLAN_SCHEMA?"""
import importlib.util
import json
from pathlib import Path

SRC = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source/docs/coop/design-corrections/foundation")


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, SRC / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


F = load("p5_graph", "evaluator_graph_fixture.v3.py")
EN = load("p5_enum", "enumeration_model.v1.py")
C = F.C

g = F.build_file_inputs(optional_unselected_cell=True)
plan = g["enumerationPlan"]
out = {"cells": [{"cap": c["capabilityId"], "kinds": c["kinds"], "required": c["required"]} for c in plan["cells"]]}
try:
    C.validate(EN.PLAN_SCHEMA, plan)
    out["planSchema"] = "OK"
except Exception as exc:  # noqa: BLE001
    out["planSchema"] = f"{type(exc).__name__}: {exc}"[:4000]

cell = plan["cells"][-1]
schema = {"$defs": EN.PLAN_SCHEMA["$defs"], "allOf": [{"$ref": "#/$defs/CellObligationV1"}]}
try:
    C.validate(schema, cell)
    out["cellSchema"] = "OK"
except Exception as exc:  # noqa: BLE001
    out["cellSchema"] = f"{type(exc).__name__}: {exc}"[:4000]

bschema = {"$defs": EN.PLAN_SCHEMA["$defs"], "allOf": [{"$ref": "#/$defs/UnavailableProgramBindingV1"}]}
try:
    C.validate(bschema, cell["programBindings"][0])
    out["bindingSchema"] = "OK"
except Exception as exc:  # noqa: BLE001
    out["bindingSchema"] = f"{type(exc).__name__}: {exc}"[:4000]

out["cellObligationDef"] = EN.PLAN_SCHEMA["$defs"]["CellObligationV1"]
out["lastCell"] = cell
print(json.dumps(out, indent=2, default=str))
