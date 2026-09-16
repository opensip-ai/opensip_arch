"""P2 — A-12 admission boundaries, measured at THREE separate standings. Nothing is promoted between them.

  stock-schema   : jsonschema Draft 2020-12 over incoming-search.schema.v1.json alone
  native-carrier : native_evidence_model.v2.subject_scope_commitment over a subject-scope descriptor
  atom-api       : admit_atom_inputs + evaluate_atom over synthetic inputs

argv[1] = frozen34 | successor chooses the atom model. Builders come from frozen34 check-atoms.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

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
N = AM.N
U1, U2, F_SYM = K.U1, K.U2, K.F_SYM
REF = {"op": "none", "relation": "references", "minResolution": "resolved-binding", "endpoint": "target", "filters": []}
OUT = {"model": WHICH}


def ev(inputs, atom=REF):
    try:
        r = AM.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(K.F_SUBJ), copy.deepcopy(inputs))
    except AM.AtomAdmissionError as e:
        return {"standing": "atom-api", "admission": "REFUSE", "key": e.key, "detail": str(e)[:160]}
    return {"standing": "atom-api", "admission": "ADMIT", "value": r["value"],
            "causes": sorted([c["code"], c.get("universe")] for c in r["causes"]),
            "coverageIds": r["coverageIds"], "scopeIds": r["scopeIds"]}


def with_empty_program(scope_mode, attest=False):
    """U1 fully evidenced; a second same-family selected program at U2 whose inventory is empty."""
    p = K.plan_one(cap="references")
    p["cells"].append(K.ref_cell("references", "ts-tsconfig", U2, "pkg-empty", K.C_PROV2, ["pkg-empty/src/index.ts"]))
    empty = K.inv_symbol(universe=U2, nid="ts-symbol:pkg-empty/src/index.ts#unused", path="pkg-empty/src/index.ts", qn="unused")
    empty.update({"cellOrdinal": 1, "rows": [], "examinedPaths": ["pkg-empty/src/index.ts"]})
    i = K.base_inputs(enumerationPlan=p, inventories=[K.inv_symbol(), empty])
    K.install_pair(i, *K.paired("references", "resolved-binding", U1, U1, [F_SYM], tag="1"))
    if scope_mode in ("empty-scope", "empty-scope-paired"):
        s, sc = K.scope("references", "resolved-binding", U2, U1, [], sid="7")
        sc["enumeratorClosure"] = K.C_PROV2
        i["scopes"][s] = sc
        if scope_mode == "empty-scope-paired":
            c, cv = K.coverage("references", "resolved-binding", U2, U1, cid="7")
            i["coverages"][c] = cv
            i["coverageScopes"][c] = s
    if attest:
        refs = [K.scope2("7")] if scope_mode.startswith("empty-scope") else []
        i["incomingSearchAttestations"] = [
            K.incoming_att("references", "resolved-binding", U2, U1, refs, [empty], providerClosure=K.C_PROV2)]
    return i


# ---- A-12(1): a scope-less provider group and IncomingSearchV1
schema = json.loads((TREES[WHICH] / FOUND / "incoming-search.schema.v1.json").read_text())
att_empty = K.incoming_att("references", "resolved-binding", U2, U1, [], [K.inv_symbol()], providerClosure=K.C_PROV2)
OUT["A12-1"] = {
    "stock-schema/emptyScopeRefs": sorted(e.message[:120] for e in Draft202012Validator(schema).iter_errors(att_empty)),
    "atom-api/noScope-noAttestation": ev(with_empty_program("none")),
    "atom-api/noScope-attestationEmptyScopeRefs": ev(with_empty_program("none", attest=True)),
    "atom-api/emptySubjectScope-unpaired": ev(with_empty_program("empty-scope")),
    "atom-api/emptySubjectScope-pairedCompleteCoverage": ev(with_empty_program("empty-scope-paired")),
    "atom-api/emptySubjectScope-qualifyingAttestation": ev(with_empty_program("empty-scope", attest=True)),
}
desc = {"schemaVersion": 2, "snapshotId": K.SNAP, "sourceUniverse": U2, "targetUniverse": U1,
        "relation": "references", "resolution": "resolved-binding", "enumeratorClosure": K.C_PROV2, "subjects": []}


def native(d):
    try:
        return {"standing": "native-carrier", "admitted": True, "value": N.subject_scope_commitment(copy.deepcopy(d))}
    except Exception as ex:  # noqa: BLE001
        return {"standing": "native-carrier", "admitted": False, "error": f"{type(ex).__name__}: {str(ex)[:160]}"}


OUT["A12-1"]["native-carrier/emptySubjects"] = native(desc)

# ---- A-12(2): scope without an enumeratorClosure
no_key = {k: v for k, v in desc.items() if k != "enumeratorClosure"}
null_key = dict(desc, enumeratorClosure=None)
OUT["A12-2"] = {
    "native-carrier/keyAbsent": native(dict(no_key, subjects=[F_SYM], sourceUniverse=U1)),
    "native-carrier/keyNull": native(dict(null_key, subjects=[F_SYM], sourceUniverse=U1)),
}


def untagged(mode, paired, attest):
    i = K.base_inputs(enumerationPlan=K.plan_one(cap="references"))
    s, sc = K.scope("references", "resolved-binding", U1, U1, [F_SYM], sid="1")
    if mode == "absent":
        del sc["enumeratorClosure"]
    else:
        sc["enumeratorClosure"] = None
    i["scopes"][s] = sc
    if paired:
        c, cv = K.coverage("references", "resolved-binding", U1, U1, cid="1")
        i["coverages"][c] = cv
        i["coverageScopes"][c] = s
    if attest:
        i["incomingSearchAttestations"] = [K.incoming_att("references", "resolved-binding", U1, U1, [s], [K.inv_symbol()])]
    return i


for mode in ("absent", "null"):
    for paired in (False, True):
        for attest in (False, True):
            OUT["A12-2"][f"atom-api/key{mode.title()}/paired={paired}/attest={attest}"] = ev(untagged(mode, paired, attest))

print(json.dumps(OUT, indent=1, default=str))
