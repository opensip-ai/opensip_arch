"""Shape probe 3: does the SAME coverage-unknown carrier rule fire on the incoming path?

Same dependency evidence as a6 case A, evaluated with endpoint=target. AUTHOR/REFERENCE evidence.
"""
import importlib.util
import json
from pathlib import Path

F = Path("/tmp/opensip-design-corrections/atom-cause-successor.v1/source/"
         "docs/coop/design-corrections/foundation")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


K = load("check_atoms_v1", F / "check-atoms.v1.py")
AM = K.AM
FSYM = "ts-symbol:src/a.ts#f"


def build(low, high, reverse=False):
    sr, scr, cr, covr = K.paired("reachability", "from-resolved-calls", K.U1, K.U1, [FSYM], tag="1")
    sa, sca, ca, cova = K.paired("calls", "resolved-callee", K.U1, K.U1, [FSYM], tag="2",
                                 cov="unknown")
    sb, scb, cb, covb = K.paired("calls", "resolved-callee", K.U1, K.U1, [FSYM], tag="3",
                                 cov="unknown")
    cova["entry"]["deficiency"] = covb["entry"]["deficiency"] = "input-closure-incomplete"
    cova["entry"]["nativeCause"], covb["entry"]["nativeCause"] = low, high
    inputs = K.base_inputs(enumerationPlan=K.plan_one(cap="reachability"))
    pairs = [(sr, scr, cr, covr), (sa, sca, ca, cova), (sb, scb, cb, covb)]
    for p in (reversed(pairs) if reverse else pairs):
        K.install_pair(inputs, *p)
    return inputs


rows = []
for label, reverse in (("ascending-insert", False), ("descending-insert", True)):
    for endpoint in ("source", "target"):
        atom = {"op": "all-covered", "relation": "reachability",
                "minResolution": "from-resolved-calls", "endpoint": endpoint, "filters": []}
        try:
            r = AM.evaluate_atom(atom, {"universe": K.U1, "kind": "symbol",
                                        "nativeSubjectId": FSYM},
                                 build("lockfile-missing", "no-program-unit", reverse))
            rows.append({"case": f"{label}/{endpoint}", "value": r["value"],
                         "causes": [{k: v for k, v in c.items() if v is not None}
                                    for c in r["causes"]],
                         "coverageIds": r["coverageIds"], "scopeIds": r["scopeIds"],
                         "nativeDeficiencies": r["nativeDeficiencies"]})
        except Exception as exc:  # noqa: BLE001
            rows.append({"case": f"{label}/{endpoint}", "error": f"{type(exc).__name__}: {exc}"})

print(json.dumps(rows, indent=2, default=str))
