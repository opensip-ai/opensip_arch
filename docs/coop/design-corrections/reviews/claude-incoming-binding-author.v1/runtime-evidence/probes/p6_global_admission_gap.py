"""P6 — does the carrier tightening reach GLOBAL attestation admission, or only consuming evaluation?

An attestation for `calls` names a `calls` scope whose enumeratorClosure KEY IS ABSENT. The evaluated
atom is `references`, which never pairs a calls scope. Then the same inputs are evaluated with a
`calls` incoming atom, which does pair it.

STANDING: atom-api over synthetic inputs. argv[1] = frozen34 | successor.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

TREES = {
    "frozen34": Path("/tmp/opensip-design-corrections/candidate-subject.v34"),
    "successor": Path("/tmp/opensip-design-corrections/incoming-binding-successor.v1/source"),
}
FOUND = "docs/coop/design-corrections/foundation"
WHICH = sys.argv[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


K = load("chk_frozen34", TREES["frozen34"] / FOUND / "check-atoms.v1.py")
AM = load("atom_under_test", TREES[WHICH] / FOUND / "atom_model.v1.py")
U1, F_SYM = K.U1, K.F_SYM

plan = K.plan_one(cap="references")
plan["cells"] = sorted(plan["cells"] + [K.ref_cell("calls", "ts-tsconfig", U1, ".", K.C_PROV, ["src/a.ts"])],
                       key=lambda c: (c["capabilityId"], c["languageMode"], c["workspaceRoot"]))
inv = K.inv_symbol()
inv["cellOrdinal"] = [n for n, c in enumerate(plan["cells"]) if c["capabilityId"] == "calls"][0]
inputs = K.base_inputs(enumerationPlan=plan, inventories=[inv])
K.install_pair(inputs, *K.paired("references", "resolved-binding", U1, U1, [F_SYM], tag="1"))
sid, sc = K.scope("calls", "resolved-callee", U1, U1, [F_SYM], sid="9")
del sc["enumeratorClosure"]
inputs["scopes"][sid] = sc
inputs["incomingSearchAttestations"] = [K.incoming_att("calls", "resolved-callee", U1, U1, [sid], [inv])]


def ev(atom):
    try:
        r = AM.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(K.F_SUBJ), copy.deepcopy(inputs))
    except AM.AtomAdmissionError as e:
        return {"admission": "REFUSE", "key": e.key, "detail": str(e)[:160]}
    return {"admission": "ADMIT", "value": r["value"],
            "causes": sorted(([c["code"], c.get("universe")] for c in r["causes"]), key=lambda t: (t[0], t[1] or ""))}


def admit_only():
    try:
        AM.admit_atom_inputs(copy.deepcopy(inputs))
        return {"admission": "ADMIT"}
    except AM.AtomAdmissionError as e:
        return {"admission": "REFUSE", "key": e.key}


print(json.dumps({
    "model": WHICH,
    "globalAdmissionOnly": admit_only(),
    "referencesIncomingAtom_neverPairsCallsScope": ev({"op": "none", "relation": "references",
                                                      "minResolution": "resolved-binding",
                                                      "endpoint": "target", "filters": []}),
    "callsIncomingAtom_pairsTheScope": ev({"op": "none", "relation": "calls", "minResolution": "resolved-callee",
                                           "endpoint": "target", "filters": []}),
}, indent=1))
