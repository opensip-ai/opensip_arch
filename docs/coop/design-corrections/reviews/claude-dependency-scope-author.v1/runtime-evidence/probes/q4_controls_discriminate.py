"""Q4 — every SUCCESSOR check-atoms case against the successor model and the frozen35 model.

Only the atom_model binding changes; the checker is the successor's. frozen35 is read, never written.
"""
import importlib.util
import json
import sys
from pathlib import Path

SUCC = Path("/tmp/opensip-design-corrections/dependency-scope-successor.v1/source/docs/coop/design-corrections/foundation")
FROZ = Path("/tmp/opensip-design-corrections/candidate-subject.v35/docs/coop/design-corrections/foundation")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


K = load("check_atoms_successor", SUCC / "check-atoms.v1.py")
models = {"successor": K.AM, "frozen35": load("atom_model_frozen35", FROZ / "atom_model.v1.py")}
frozen_cases = [fn.__name__ for fn in load("check_atoms_frozen35", FROZ / "check-atoms.v1.py").CASES]
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
    "casesSuccessorChecker": len(K.CASES), "casesFrozen35Checker": len(frozen_cases),
    "originalCasesPreservedByName": all(n in results for n in frozen_cases),
    "addedCases": [fn.__name__ for fn in K.CASES if fn.__name__ not in frozen_cases],
    "failOnSuccessor": sorted(n for n, r in results.items() if not r["successor"]["ok"]),
    "discriminating": sorted(n for n, r in results.items() if r["successor"]["ok"] and not r["frozen35"]["ok"]),
    "addedPassBothModels": sorted(n for n, r in results.items()
                                  if r["successor"]["ok"] and r["frozen35"]["ok"] and n not in frozen_cases),
    "originalCasesOnFrozen35Model": sum(1 for n in frozen_cases if results[n]["frozen35"]["ok"]),
    "frozen35Errors": {n: r["frozen35"]["error"] for n, r in results.items() if not r["frozen35"]["ok"]},
}, indent=1))
