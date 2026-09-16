"""Shape probe 2: dependency-view fold carrier, and incoming accumulation with no early stop.

Reuses the reference checker's builders. Prints actual results; nothing asserted here.
AUTHOR/REFERENCE evidence.
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


def carry(covr, deficiency, native_cause):
    covr["entry"]["deficiency"] = deficiency
    covr["entry"]["nativeCause"] = native_cause
    return covr


def dump(label, r):
    return {"case": label, "value": r["value"],
            "causes": [{k: v for k, v in c.items() if v is not None} for c in r["causes"]],
            "scopeIds": r["scopeIds"], "coverageIds": r["coverageIds"],
            "nativeDeficiencies": r["nativeDeficiencies"],
            "known": r["knownFactIds"], "uncertain": r["uncertainFactIds"]}


rows = []

# A. Two `calls@resolved-callee` dep partitions of one reachability subject, different carriers.
sr, scr, cr, covr = K.paired("reachability", "from-resolved-calls", K.U1, K.U1, [FSYM], tag="1")
sa, sca, ca, cova = K.paired("calls", "resolved-callee", K.U1, K.U1, [FSYM], tag="2", cov="unknown")
sb, scb, cb, covb = K.paired("calls", "resolved-callee", K.U1, K.U1, [FSYM], tag="3", cov="unknown")
carry(cova, "input-closure-incomplete", "lockfile-missing")
carry(covb, "input-closure-incomplete", "no-program-unit")
inputs = K.base_inputs(enumerationPlan=K.plan_one(cap="reachability"))
K.install_pair(inputs, sr, scr, cr, covr)
K.install_pair(inputs, sa, sca, ca, cova)
K.install_pair(inputs, sb, scb, cb, covb)
atom = {"op": "all-covered", "relation": "reachability", "minResolution": "from-resolved-calls",
        "filters": []}
try:
    rows.append(dump("dep-fold-lower-id-carries",
                     AM.evaluate_atom(atom, {"universe": K.U1, "kind": "symbol",
                                             "nativeSubjectId": FSYM}, inputs)))
except Exception as exc:  # noqa: BLE001
    rows.append({"case": "dep-fold-lower-id-carries", "error": f"{type(exc).__name__}: {exc}"})

# A'. Same evidence, carriers swapped between the two ids: the emitted cause must swap with them.
sa2, sca2, ca2, cova2 = K.paired("calls", "resolved-callee", K.U1, K.U1, [FSYM], tag="2",
                                 cov="unknown")
sb2, scb2, cb2, covb2 = K.paired("calls", "resolved-callee", K.U1, K.U1, [FSYM], tag="3",
                                 cov="unknown")
carry(cova2, "input-closure-incomplete", "no-program-unit")
carry(covb2, "input-closure-incomplete", "lockfile-missing")
inputs2 = K.base_inputs(enumerationPlan=K.plan_one(cap="reachability"))
K.install_pair(inputs2, sr, scr, cr, covr)
K.install_pair(inputs2, sa2, sca2, ca2, cova2)
K.install_pair(inputs2, sb2, scb2, cb2, covb2)
try:
    rows.append(dump("dep-fold-carriers-swapped",
                     AM.evaluate_atom(atom, {"universe": K.U1, "kind": "symbol",
                                             "nativeSubjectId": FSYM}, inputs2)))
except Exception as exc:  # noqa: BLE001
    rows.append({"case": "dep-fold-carriers-swapped", "error": f"{type(exc).__name__}: {exc}"})

# B. Incoming: two owed source universes, each failing differently; nothing may stop the other.
g = "ts-symbol:src/b.ts#g"
plan = K.plan_one(cap="references")
plan["cells"].append({
    "capabilityId": "references", "languageMode": "ts-tsconfig", "workspaceRoot": "pkg-b",
    "required": True, "kinds": ["symbol"],
    "programBindings": [{
        "ordinal": 0, "provenance": "explicit-plan-selection",
        "enumerator": {"status": "selected", "closureId": K.C_PROV2},
        "nativeContextDigest": K.H("0"), "universe": K.U2, "programEntry": None,
        "extents": [{"kind": "symbol", "paths": ["src/b.ts"]}],
    }],
})
inv_a = K.inv_symbol()
inv_b = K.inv_symbol(universe=K.U2, nid=g, path="src/b.ts", qn="g")
inv_b["cellOrdinal"] = 1
s1, sc1 = K.scope("references", "resolved-binding", K.U1, K.U1, [FSYM], sid="1")
inputs3 = K.base_inputs(enumerationPlan=plan, inventories=[inv_a, inv_b], scopes={s1: sc1})
try:
    rows.append(dump("incoming-two-universes-both-reported",
                     AM.evaluate_atom({"op": "none", "relation": "references",
                                       "minResolution": "resolved-binding",
                                       "endpoint": "target", "filters": []},
                                      {"universe": K.U1, "kind": "symbol",
                                       "nativeSubjectId": FSYM}, inputs3)))
except Exception as exc:  # noqa: BLE001
    rows.append({"case": "incoming-two-universes-both-reported",
                 "error": f"{type(exc).__name__}: {exc}"})

print(json.dumps(rows, indent=2, default=str))
