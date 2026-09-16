"""Run ONLY the new native case through the checker's own run_case, against the model of a given run copy.

Why: in the control copy (frozen39 model), check_native_evidence.v2.py aborted with TypeError in resolve(): the case's
discover_units step faulted (recorded inside run_case, never printed) and a later step then resolved "$auto.units" on
the None it bound, which the existing harness does outside its try. This shows the recorded step faults.

Usage: native_case_diagnosis.py RUN_COPY_ROOT OUT_JSON
  full       run_case on the case as published (an escaping exception is recorded with its type)
  discovery  run_case on the case with only its discover_units steps and only the expectations over their bindings
"""
import importlib.util
import json
import sys
import traceback
from pathlib import Path

root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
native = root / "docs/coop/design-corrections/native"
spec = importlib.util.spec_from_file_location("diag_check_native_evidence", native / "check_native_evidence.v2.py")
CHK = importlib.util.module_from_spec(spec)
spec.loader.exec_module(CHK)
model = CHK.load_model()
doc = model.C.parse(CHK.CASES_PATH.read_bytes())
case = next(c for c in doc["cases"] if c["id"] == "units-nested-cargo-workspace-folds-into-the-deepest-surviving-workspace-unit")
result = {"runCopy": str(root)}
try:
    result["full"] = CHK.run_case(case, model, doc["fixtures"])
except Exception as e:  # noqa: BLE001
    tb = traceback.extract_tb(e.__traceback__)[-1]
    result["full"] = {"escaped": type(e).__name__, "message": str(e)[:200], "at": "%s:%d" % (Path(tb.filename).name, tb.lineno)}
steps = [s for s in case["steps"] if s["fn"] == "discover_units"]
binds = {s["bind"] for s in steps}
discovery = dict(case, steps=steps, expect={k: v for k, v in case["expect"].items() if k[1:].split(".")[0] in binds})
result["discovery"] = CHK.run_case(discovery, model, doc["fixtures"])
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=1) + "\n")
print(json.dumps(result, indent=1))
