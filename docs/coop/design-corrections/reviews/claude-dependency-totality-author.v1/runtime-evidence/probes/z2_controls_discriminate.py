"""Z2 — every SUCCESSOR check-atoms case against the successor model and the PREVIOUS (95-check) model.

previous = dependency-scope-successor.v1 atom_model (read-only). Only the atom_model binding changes.
"""
import importlib.util
import json
import sys
from pathlib import Path

SUCC = Path("/tmp/opensip-design-corrections/dependency-totality-successor.v1/source/docs/coop/design-corrections/foundation")
PREV = Path("/tmp/opensip-design-corrections/dependency-scope-successor.v1/source/docs/coop/design-corrections/foundation")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


K = load("check_atoms_successor", SUCC / "check-atoms.v1.py")
models = {"successor": K.AM, "previous": load("atom_model_previous", PREV / "atom_model.v1.py")}
previous_cases = [fn.__name__ for fn in load("check_atoms_previous", PREV / "check-atoms.v1.py").CASES]
results = {}
for label, model in models.items():
    K.AM = model
    for fn in K.CASES:
        try:
            fn()
            results.setdefault(fn.__name__, {})[label] = {"ok": True}
        except Exception as exc:  # noqa: BLE001
            results.setdefault(fn.__name__, {})[label] = {"ok": False, "error": f"{type(exc).__name__}: {exc}"[:300]}
print(json.dumps({
    "casesSuccessorChecker": len(K.CASES), "casesPreviousChecker": len(previous_cases),
    "previousCasesPreservedByName": all(n in results for n in previous_cases),
    "addedCases": [fn.__name__ for fn in K.CASES if fn.__name__ not in previous_cases],
    "failOnSuccessor": sorted(n for n, r in results.items() if not r["successor"]["ok"]),
    "discriminating": sorted(n for n, r in results.items() if r["successor"]["ok"] and not r["previous"]["ok"]),
    "addedPassBothModels": sorted(n for n, r in results.items()
                                  if r["successor"]["ok"] and r["previous"]["ok"] and n not in previous_cases),
    "previousCasesOnPreviousModel": sum(1 for n in previous_cases if results[n]["previous"]["ok"]),
    "previousCasesOnSuccessorModel": sum(1 for n in previous_cases if results[n]["successor"]["ok"]),
    "previousModelErrors": {n: r["previous"]["error"] for n, r in results.items() if not r["previous"]["ok"]},
}, indent=1))
