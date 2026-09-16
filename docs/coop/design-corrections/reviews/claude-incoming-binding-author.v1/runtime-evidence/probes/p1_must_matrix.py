"""P1 — MUST-34-01 matrix on the REAL atom API: frozen34 versus successor.

argv[1] = frozen34 | successor chooses which atom_model.v1.py answers. Builders come from FROZEN34
check-atoms.v1.py in both runs, so only the model under test differs.

STANDING: atom-api — global atom-input admission (incl. IncomingSearchV1 schema/joins) plus
evaluate_atom, over SYNTHETIC inputs. Cases marked `synthetic-only` use a shape a stock schema would
refuse (e.g. an unregistered languageMode) and say so. Nothing here is enumeration closed-world
admission, a retained Run, or qualification.
"""
import copy
import hashlib
import importlib.util
import itertools
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
U1, U2, UR = K.U1, K.U2, K.UR
F_SYM = K.F_SYM
G_SYM = "ts-symbol:pkg-b/src/b.ts#g"
H_SYM = "ts-symbol:pkg-c/src/c.ts#h"
C_PROV3 = "closure2:" + "dd" * 32
SUBJ = {"universe": U1, "kind": "symbol", "nativeSubjectId": F_SYM}


def cell(cap, mode, universe, root, closure, paths, kinds=("symbol",)):
    return K.ref_cell(cap, mode, universe, root, closure, list(paths), kinds=list(kinds))


def build(cells, extra_scopes=(), u1_evidence=False, u2_evidence=False, u3_evidence=False,
          facts=None, attributions=None, reverse=False):
    """cells: list of (key, cell). The subject f always has a real inventory row at U1 through a
    `calls` cell, so f is inventoried even when U1 has no binding for the atom relation."""
    cells = [("subject-calls", cell("calls", "ts-tsconfig", U1, "pkg-a", K.C_PROV, ["src/a.ts"]))] + list(cells)
    cells.sort(key=lambda kc: (kc[1]["capabilityId"], kc[1]["languageMode"], kc[1]["workspaceRoot"]))
    plan = K.plan_one(cap="calls")
    plan["cells"] = [c for _, c in cells]
    ordinal = {k: n for n, (k, _) in enumerate(cells)}
    inv_f = K.inv_symbol()
    inv_f["cellOrdinal"] = ordinal["subject-calls"]
    invs = [inv_f]
    for key, uni, sym, path in (("u2", U2, G_SYM, "pkg-b/src/b.ts"), ("u2b", U2, H_SYM, "pkg-c/src/c.ts")):
        if key in ordinal:
            inv = K.inv_symbol(universe=uni, nid=sym, path=path, qn=sym.rsplit("#", 1)[1])
            inv["cellOrdinal"] = ordinal[key]
            invs.append(inv)
    i = K.base_inputs(enumerationPlan=plan, inventories=invs)
    i["closures"][C_PROV3] = {"kind": "provider"}
    if facts:
        i["facts"] = copy.deepcopy(facts)
    if attributions:
        i["targetAttributions"] = copy.deepcopy(attributions)
    rel, rung = REL["relation"], REL["minResolution"]
    if u1_evidence:
        K.install_pair(i, *K.paired(rel, rung, U1, U1, [F_SYM], tag="1"))
    if u2_evidence:
        s, sc = K.scope(rel, rung, U2, U1, [G_SYM], sid="2")
        sc["enumeratorClosure"] = K.C_PROV2
        K.install_pair(i, s, sc, *K.coverage(rel, rung, U2, U1, cid="2"))
    if u3_evidence:
        s, sc = K.scope(rel, rung, U2, U1, [H_SYM], sid="3")
        sc["enumeratorClosure"] = C_PROV3
        K.install_pair(i, s, sc, *K.coverage(rel, rung, U2, U1, cid="3"))
    if reverse:
        # Only orders that are NOT fixed by an admitted shape are varied. Plan cells are schema-sorted
        # and inventories address them by cellOrdinal, so reversing cells would corrupt the inputs
        # (the first run of this probe did exactly that; its receipt is kept).
        for key in ("scopes", "coverages", "coverageScopes", "facts", "targetAttributions"):
            i[key] = dict(reversed(list(i[key].items())))
        i["inventories"] = list(reversed(i["inventories"]))
    return i


def ev(atom, inputs, subj=SUBJ):
    try:
        r = AM.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(subj), copy.deepcopy(inputs))
    except AM.AtomAdmissionError as e:
        return {"admission": "REFUSE", "key": e.key}
    return {"admission": "ADMIT", "value": r["value"],
            "causes": sorted(([c["code"], c.get("universe")] for c in r["causes"]),
                             key=lambda t: (t[0], t[1] or "")),
            "known": r["knownFactIds"], "coverageIds": r["coverageIds"], "scopeIds": r["scopeIds"]}


def digest(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()


OUT = {"standing": "atom-api over synthetic inputs; not enumeration closed-world admission, not a "
                   "retained Run, not qualification", "model": WHICH,
       "modelSha256": hashlib.sha256((TREES[WHICH] / FOUND / "atom_model.v1.py").read_bytes()).hexdigest()}

# ---------------------------------------------------------------- 1. references matrix, no facts
REL = {"relation": "references", "minResolution": "resolved-binding"}
R_TS2 = ("u2", cell("references", "ts-tsconfig", U2, "pkg-b", K.C_PROV2, ["pkg-b/src/b.ts"]))
R_TS1 = ("u1-ref", cell("references", "ts-tsconfig", U1, "pkg-a", K.C_PROV, ["src/a.ts"]))
R_TS1_UNAV = ("u1-unav", cell("references", "ts-tsconfig", None, "pkg-a", K.C_PROV, ["src/a.ts"]))
R_RS = ("rs", cell("references", "rust-cargo", UR, "crate", K.C_PROV2, ["crate/src/lib.rs"]))
R_RS_UNAV = ("rs-unav", cell("references", "rust-cargo", None, "crate-u", K.C_PROV2, ["crate-u/src/lib.rs"]))
R_UNKFAM_UNAV = ("unk-unav", cell("references", "unregistered-mode", None, "odd", K.C_PROV2, ["odd/x"]))

MATRIX = {
    "U1-unbound + U2-same-family-evidenced": build([R_TS2], u2_evidence=True),
    "U1-unbound + foreign-available-only": build([R_RS]),
    "U1-unbound + foreign-unavailable-only": build([R_RS_UNAV]),
    "U1-unbound + foreign-available-and-unavailable": build([R_RS, R_RS_UNAV]),
    "no-references-binding-anywhere": build([]),
    "U1-available-evidenced + U2-evidenced": build([R_TS1, R_TS2], u1_evidence=True, u2_evidence=True),
    "U1-available-evidenced only": build([R_TS1], u1_evidence=True),
    "U1-available-evidenced + foreign-available-and-unavailable": build([R_TS1, R_RS, R_RS_UNAV], u1_evidence=True),
    "U1-available-unevidenced + U2-evidenced": build([R_TS1, R_TS2], u2_evidence=True),
    "U1-unavailable-same-family + U2-evidenced": build([R_TS1_UNAV, R_TS2], u2_evidence=True),
    "U1-available-evidenced + unknown-family-unavailable (synthetic-only)": build([R_TS1, R_UNKFAM_UNAV], u1_evidence=True),
    "U1-unbound + unknown-family-unavailable (synthetic-only)": build([R_UNKFAM_UNAV]),
}
OPS = [("none", {}), ("exists", {}), ("count-at-most-0", {"n": 0}), ("all-covered", {})]
OUT["references"] = {}
for label, inp in MATRIX.items():
    row = {}
    for ep in ("target", "source"):
        for op, extra in OPS:
            atom = dict(REL, op=op.split("-0")[0] if op.startswith("count") else op, endpoint=ep, filters=[], **extra)
            row[f"{'in' if ep == 'target' else 'out'}/{op}"] = ev(atom, inp)
    OUT["references"][label] = row

# ---------------------------------------------------------------- 2. known incoming matches (imports)
REL = {"relation": "imports", "minResolution": "resolved-target"}
FILE_SUBJ = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}


def fact(fid, src_u, importer):
    return {"factId": fid, "relation": "imports", "resolution": "resolved-target",
            "sourceUniverse": src_u, "targetUniverse": U1, "producerClosure": K.C_PROV,
            "confidenceMillionths": 1000000,
            "payload": {"importer": importer, "specifier": "./a", "resolvedTarget": "file:src/a.ts"},
            "anchors": [{"path": "src/a.ts", "blobDigest": K.H("0"), "startByte": 0, "endByte": 1}]}


F1, F2 = K.fact2("1"), K.fact2("2")
FACTS = {F1: fact(F1, U1, F_SYM), F2: fact(F2, U1, "ts-symbol:src/a.ts#f2")}
ATTR = {fid: K.sidecar(fid, "file:src/a.ts", kind="file", occupancy="first-party", evaluation="src/a.ts")
        for fid in FACTS}


def imports_inputs(bound_u1, with_facts):
    cells = [("u2", cell("imports", "ts-tsconfig", U2, "pkg-b", K.C_PROV2, ["pkg-b/src/b.ts"], kinds=("symbol", "file")))]
    if bound_u1:
        cells.append(("u1-imp", cell("imports", "ts-tsconfig", U1, "pkg-a", K.C_PROV, ["src/a.ts"], kinds=("symbol", "file"))))
    i = build(cells, u1_evidence=bound_u1, u2_evidence=True,
              facts=FACTS if with_facts else None, attributions=ATTR if with_facts else None)
    i["inventories"].append(K.inv_file())
    i["inventories"][-1]["cellOrdinal"] = [n for n, c in enumerate(i["enumerationPlan"]["cells"])
                                           if c["capabilityId"] == "calls"][0]
    return i


OUT["importsKnownMatches"] = {}
for label, bound, with_facts in (("U1-unbound + 2 known facts", False, True),
                                 ("U1-unbound + no facts", False, False),
                                 ("U1-bound-evidenced + 2 known facts", True, True),
                                 ("U1-bound-evidenced + no facts", True, False)):
    inp = imports_inputs(bound, with_facts)
    row = {}
    for op, extra in (("none", {}), ("exists", {}), ("count-at-most", {"n": 1}),
                      ("count-at-most", {"n": 2}), ("all-covered", {})):
        key = op + (f"-{extra['n']}" if extra else "")
        row[key] = ev(dict(REL, op=op, endpoint="target", filters=[], **extra), inp, FILE_SUBJ)
    OUT["importsKnownMatches"][label] = row

# ---------------------------------------------------------------- 3. multi-provider, order independence
REL = {"relation": "references", "minResolution": "resolved-binding"}
MP_CELLS = [R_TS2, ("u2b", cell("references", "ts-tsconfig", U2, "pkg-c", C_PROV3, ["pkg-c/src/c.ts"])), R_RS]
OUT["multiProvider"] = {}
for label, kwargs in (("U1-unbound, provider2 evidenced, provider3 unevidenced", dict(u2_evidence=True)),
                      ("U1-unbound, both U2 providers evidenced", dict(u2_evidence=True, u3_evidence=True)),
                      ("U1-bound-evidenced, both U2 providers evidenced",
                       dict(u1_evidence=True, u2_evidence=True, u3_evidence=True))):
    cells = MP_CELLS + ([R_TS1] if kwargs.get("u1_evidence") else [])
    results = set()
    sample = None
    for perm in itertools.permutations(cells):
        for reverse in (False, True):
            r = ev(dict(REL, op="none", endpoint="target", filters=[]), build(list(perm), reverse=reverse, **kwargs))
            results.add(digest(r))
            sample = r
    OUT["multiProvider"][label] = {"orderings": 2 * len(list(itertools.permutations(cells))),
                                   "distinctResults": len(results), "sample": sample}

print(json.dumps(OUT, indent=1, default=str))
