"""Shape probe: build each outgoing early-stop branch with a KNOWN matching fact present.

Reuses the reference checker's own builders so the eventual controls use existing idioms.
Prints the actual result of each construction; nothing is asserted here. AUTHOR/REFERENCE evidence.
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

SUBJ = {"universe": K.U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}
FID = K.fact2("1")


def imports_fact():
    return {FID: {
        "factId": FID, "relation": "imports", "resolution": "resolved-target",
        "sourceUniverse": K.U1, "targetUniverse": K.U1, "producerClosure": K.C_PROV,
        "confidenceMillionths": 1000000,
        "payload": {"importer": "ts-symbol:src/a.ts#f", "specifier": "./b",
                    "resolvedTarget": "file:src/b.ts"},
        "anchors": [{"path": "src/a.ts", "blobDigest": K.H("0"), "startByte": 0, "endByte": 1}],
    }}


def atom(op, **extra):
    a = {"op": op, "relation": "imports", "minResolution": "resolved-target", "filters": []}
    a.update(extra)
    return a


def shape(label, inputs, subj=None):
    row = {"case": label}
    for op in ("exists", "none"):
        try:
            r = AM.evaluate_atom(atom(op), subj or SUBJ, inputs)
            row[op] = {"value": r["value"], "known": r["knownFactIds"],
                       "uncertain": r["uncertainFactIds"],
                       "causes": [{k: v for k, v in c.items() if v is not None} for c in r["causes"]],
                       "scopeIds": r["scopeIds"], "coverageIds": r["coverageIds"],
                       "nativeDeficiencies": r["nativeDeficiencies"]}
        except Exception as exc:  # noqa: BLE001 - shape probe
            row[op] = {"error": f"{type(exc).__name__}: {exc}"}
    try:
        r = AM.evaluate_atom(atom("count-at-most", n=0), subj or SUBJ, inputs)
        row["count-at-most-0"] = r["value"]
    except Exception as exc:  # noqa: BLE001
        row["count-at-most-0"] = f"{type(exc).__name__}: {exc}"
    return row


rows = []

# 1. No owed binding at all for capabilityForRelation[imports]: plan has a different capability.
i1 = K.base_inputs(enumerationPlan=K.plan_one(cap="inventory", kinds=["symbol"]),
                   facts=imports_fact())
rows.append(shape("no-owed-binding", i1))

# 2. Owed bindings exist, none available at U1 (binding universe is U2).
i2 = K.base_inputs(enumerationPlan=K.plan_one(universe=K.U2, cap="imports"), facts=imports_fact())
rows.append(shape("bindings-but-none-at-U", i2))

# 3. Binding at U1, but no retained scope contains the current subject.
sg, scg = K.scope("imports", "resolved-target", K.U1, K.U1, ["ts-symbol:src/a.ts#g"], sid="2")
cg, covg = K.coverage("imports", "resolved-target", K.U1, K.U1, cid="2")
i3 = K.base_inputs(enumerationPlan=K.plan_one(cap="imports"), facts=imports_fact(),
                   inventories=[K.inv_symbol(), K.inv_symbol(nid="ts-symbol:src/a.ts#g", qn="g")])
K.install_pair(i3, sg, scg, cg, covg)
rows.append(shape("no-containing-scope", i3))

# 4. Two containing scopes, only one paired -> scope-without-coverage, both scopes, no coverage.
sa, sca, ca, cova = K.paired("imports", "resolved-target", K.U1, K.U1,
                             ["ts-symbol:src/a.ts#f"], tag="1")
sb, scb = K.scope("imports", "resolved-target", K.U1, K.U1,
                  ["ts-symbol:src/a.ts#f", "ts-symbol:src/a.ts#g"], sid="2")
i4 = K.base_inputs(enumerationPlan=K.plan_one(cap="imports"), facts=imports_fact(),
                   inventories=[K.inv_symbol(), K.inv_symbol(nid="ts-symbol:src/a.ts#g", qn="g")])
K.install_pair(i4, sa, sca, ca, cova)
i4["scopes"][sb] = scb
rows.append(shape("unmatched-scope-beside-paired", i4))

# 5. Cross-family unavailable binding accumulated before a no-binding/selector decision.
plan_x = K.plan_one(cap="imports", mode="rust-cargo")
plan_x["cells"][0]["programBindings"][0]["universe"] = None
i5 = K.base_inputs(enumerationPlan=plan_x, facts=imports_fact())
rows.append(shape("cross-family-unavailable-only", i5))

plan_y = K.plan_one(cap="imports")
plan_y["cells"].append({
    "capabilityId": "imports", "languageMode": "rust-cargo", "workspaceRoot": ".",
    "required": True, "kinds": ["symbol"],
    "programBindings": [{
        "ordinal": 0, "provenance": "default-unit",
        "enumerator": {"status": "selected", "closureId": K.C_PROV2},
        "nativeContextDigest": K.H("0"), "universe": None, "programEntry": None,
        "extents": [{"kind": "symbol", "paths": ["src/a.rs"]}],
    }],
})
plan_y["cells"][0]["programBindings"][0]["universe"] = K.U2
i6 = K.base_inputs(enumerationPlan=plan_y, facts=imports_fact())
rows.append(shape("cross-family-then-selector-unbound", i6))

print(json.dumps(rows, indent=2, default=str))
