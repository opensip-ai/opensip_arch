"""Shape probe for root issues 1 and 2, against the current source bytes.

1. Does the no-owed-binding `missing-relation-coverage` return also fire for endpoint=target?
2. Does incoming carry BOTH cross-family shapes (unavailable/null and available/S), and does a
   same-family unavailable binding still block incoming while leaving outgoing alone?

Synthetic atom inputs built with the reference checker's own builders. Not a proof, not a Run.
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
SUBJ = {"universe": K.U1, "kind": "symbol", "nativeSubjectId": FSYM}


def cell(mode, universe, root, closure, paths):
    return {"capabilityId": "references", "languageMode": mode, "workspaceRoot": root,
            "required": True, "kinds": ["symbol"],
            "programBindings": [{
                "ordinal": 0, "provenance": "default-unit",
                "enumerator": {"status": "selected", "closureId": closure},
                "nativeContextDigest": K.H("0"), "universe": universe, "programEntry": None,
                "extents": [{"kind": "symbol", "paths": paths}],
            }]}


def run(label, inputs):
    row = {"case": label}
    for endpoint in ("source", "target"):
        atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding",
                "endpoint": endpoint, "filters": []}
        try:
            r = AM.evaluate_atom(atom, SUBJ, inputs)
            row[endpoint] = {
                "value": r["value"],
                "causes": sorted(((c["code"], c.get("universe")) for c in r["causes"]),
                                 key=lambda t: (t[0], t[1] or "")),
                "scopeIds": r["scopeIds"], "coverageIds": r["coverageIds"],
            }
        except Exception as exc:  # noqa: BLE001
            row[endpoint] = {"error": f"{type(exc).__name__}: {exc}"}
    return row


rows = []

# 1. No owed binding for capabilityForRelation[references] at either endpoint.
rows.append(run("no-owed-binding-both-endpoints",
                K.base_inputs(enumerationPlan=K.plan_one(cap="inventory"))))

# 2. Incoming with BOTH cross-family shapes: an unavailable rust binding (prelude, universe null)
#    and an available rust binding at UR (per-universe accumulation, universe UR).
plan = K.plan_one(cap="references")
plan["cells"].append(cell("rust-cargo", None, "crate-a", K.C_PROV2, ["crate-a/src/lib.rs"]))
plan["cells"].append(cell("rust-cargo", K.UR, "crate-b", K.C_PROV2, ["crate-b/src/lib.rs"]))
inputs2 = K.base_inputs(enumerationPlan=plan)
K.install_pair(inputs2, *K.paired("references", "resolved-binding", K.U1, K.U1, [FSYM], tag="1"))
att = K.incoming_att("references", "resolved-binding", K.U1, K.U1,
                     [K.scope2("1")], [K.inv_symbol()])
inputs2["incomingSearchAttestations"] = [att]
rows.append(run("cross-family-unavailable-and-available", inputs2))

# 3. Same-family (TS) unavailable binding: blocking incoming, not poisoning outgoing.
plan3 = K.plan_one(cap="references")
plan3["cells"].append(cell("ts-tsconfig", None, "pkg-b", K.C_PROV2, ["pkg-b/src/b.ts"]))
inputs3 = K.base_inputs(enumerationPlan=plan3)
K.install_pair(inputs3, *K.paired("references", "resolved-binding", K.U1, K.U1, [FSYM], tag="1"))
inputs3["incomingSearchAttestations"] = [
    K.incoming_att("references", "resolved-binding", K.U1, K.U1,
                   [K.scope2("1")], [K.inv_symbol()])]
rows.append(run("same-family-unavailable", inputs3))

print(json.dumps(rows, indent=2, default=str))
