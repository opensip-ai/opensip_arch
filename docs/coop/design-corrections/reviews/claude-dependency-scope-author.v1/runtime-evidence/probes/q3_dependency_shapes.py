"""Q3 — dependency-scope selection on the REAL atom API, one tree at a time.

argv[1] = frozen35 | successor selects the atom_model. Builders always come from FROZEN35
check-atoms.v1.py so only the model differs. STANDING: atom-api over synthetic inputs; the `synthetic
graph` case additionally patches DEPENDS_ON in-process and is helper-graph evidence only.
"""
import copy
import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path

TREES = {
    "frozen35": Path("/tmp/opensip-design-corrections/candidate-subject.v35"),
    "successor": Path("/tmp/opensip-design-corrections/dependency-scope-successor.v1/source"),
}
FOUND = "docs/coop/design-corrections/foundation"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


K = load("chk_frozen35", TREES["frozen35"] / FOUND / "check-atoms.v1.py")
AM = load("atom_under_test", TREES[sys.argv[1]] / FOUND / "atom_model.v1.py")
U1, U2, F_SYM, G_SYM = K.U1, K.U2, K.F_SYM, K.G_SYM
REACH = {"relation": "reachability", "minResolution": "from-resolved-calls", "filters": []}


def ev(atom, inputs, subj=None):
    try:
        r = AM.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(subj or K.F_SUBJ), copy.deepcopy(inputs))
    except AM.AtomAdmissionError as e:
        return {"admission": "REFUSE", "key": e.key, "detail": str(e)[:140]}
    return {"admission": "ADMIT", "value": r["value"],
            "causes": sorted(([c["code"], c.get("universe"), c.get("nativeCause")] for c in r["causes"]),
                             key=lambda t: tuple(x or "" for x in t)),
            "nativeDeficiencies": r["nativeDeficiencies"], "coverageIds": r["coverageIds"],
            "scopeIds": r["scopeIds"], "known": r["knownFactIds"]}


def base():
    i = K.base_inputs(enumerationPlan=K.plan_one(cap="reachability"))
    K.install_pair(i, *K.paired("reachability", "from-resolved-calls", U1, U1, [F_SYM], tag="1"))
    K.install_pair(i, *K.paired("calls", "resolved-callee", U1, U1, [F_SYM], tag="2"))
    return i


def mutate(i, field, mode, other):
    sc = i["scopes"][K.scope2("2")]
    if mode == "absent":
        sc.pop(field)
    else:
        sc[field] = None if mode == "null" else other
    return i


OUT = {"model": sys.argv[1],
       "modelSha256": hashlib.sha256((TREES[sys.argv[1]] / FOUND / "atom_model.v1.py").read_bytes()).hexdigest()}
OUT["baseline"] = {ep: ev(dict(REACH, op="all-covered", endpoint=ep), base()) for ep in ("source", "target")}
deleted = base()
deleted["scopes"].pop(K.scope2("2"))
deleted["coverageScopes"].pop(K.cov2("2"))
OUT["deletedDependencyScope"] = {ep: ev(dict(REACH, op="all-covered", endpoint=ep), deleted) for ep in ("source", "target")}
dep_cov_gone = base()
dep_cov_gone["coverages"].pop(K.cov2("2"))
dep_cov_gone["coverageScopes"].pop(K.cov2("2"))
OUT["noDependencyCoverage"] = {ep: ev(dict(REACH, op="all-covered", endpoint=ep), dep_cov_gone) for ep in ("source", "target")}

# 1. mutation matrix, no exact dependency scope remains
OUT["mutations"] = {}
for field, others in (("sourceUniverse", [U2]), ("relation", ["references"]),
                      ("resolution", ["resolved-binding", "syntactic-callee-name"])):
    for mode in ("absent", "null", "different"):
        for other in (others if mode == "different" else [None]):
            label = f"{field}/{mode}" + (f"={other}" if other else "")
            OUT["mutations"][label] = {ep: ev(dict(REACH, op="all-covered", endpoint=ep), mutate(base(), field, mode, other))
                                       for ep in ("source", "target")}

# 2. no-exact versus exact-unrelated
unrelated = mutate(base(), "sourceUniverse", "different", U2)
s3, sc3 = K.scope("calls", "resolved-callee", U1, U1, [G_SYM], sid="3")
unrelated["scopes"][s3] = sc3
OUT["wrongCoordinateMappedBesideExactUnrelatedScope"] = ev(dict(REACH, op="all-covered"), unrelated)

# 3. lawful pairing positives
commit_only = base()
commit_only["coverageScopes"].pop(K.cov2("2"))
commit_only["coverages"][K.cov2("2")]["key"]["subjectScopeCommitment"] = AM._derive_scope_commitment(
    commit_only["scopes"][K.scope2("2")])
OUT["exactScopeCommitmentOnly"] = ev(dict(REACH, op="all-covered"), commit_only)
no_pairing = base()
no_pairing["coverageScopes"].pop(K.cov2("2"))
OUT["exactScopeNeitherMappedNorCommitted"] = ev(dict(REACH, op="all-covered"), no_pairing)
other_exact = base()
other_exact["scopes"][K.scope2("2")]["subjects"] = [G_SYM]
OUT["mappedToExactScopeNotContainingSubject"] = ev(dict(REACH, op="all-covered"), other_exact)

# 4. two providers' exact scopes over the subject, every insertion order
two = base()
s4, sc4 = K.scope("calls", "resolved-callee", U1, U1, [F_SYM], sid="4")
sc4["enumeratorClosure"] = K.C_PROV2
c4, cv4 = K.coverage("calls", "resolved-callee", U1, U1, cid="4")
cv4["key"]["subjectScopeCommitment"] = AM._derive_scope_commitment(sc4)
two["scopes"][s4] = sc4
two["coverages"][c4] = cv4
results = set()
for order in itertools.permutations(["scopes", "coverages", "coverageScopes"]):
    for rev in (False, True):
        i = copy.deepcopy(two)
        if rev:
            for key in order:
                i[key] = dict(reversed(list(i[key].items())))
        results.add(json.dumps(ev(dict(REACH, op="all-covered"), i), sort_keys=True))
OUT["twoProvidersExactScopes"] = {"orderings": 12, "distinct": len(results), "sample": json.loads(sorted(results)[0])}

# 4b. LAWFUL multi-scope ordering: incoming primary scope over {f, g}; two DISJOINT exact calls scopes
#     (one partition, no SUBJECT_SCOPE_PARTITION_OVERLAP), one paired by mapping, one by commitment.
def incoming_two_subject(mutate_g=None):
    i = K.base_inputs(enumerationPlan=K.plan_one(cap="reachability"),
                      inventories=[K.inv_symbol(), K.inv_symbol(nid=G_SYM, qn="g")])
    K.install_pair(i, *K.paired("reachability", "from-resolved-calls", U1, U1, [F_SYM, G_SYM], tag="1"))
    K.install_pair(i, *K.paired("calls", "resolved-callee", U1, U1, [F_SYM], tag="2"))
    sg, scg = K.scope("calls", "resolved-callee", U1, U1, [G_SYM], sid="4")
    cg, cvg = K.coverage("calls", "resolved-callee", U1, U1, cid="4")
    cvg["key"]["subjectScopeCommitment"] = AM._derive_scope_commitment(scg)
    i["scopes"][sg] = scg
    i["coverages"][cg] = cvg
    if mutate_g == "wrong-universe":
        scg["sourceUniverse"] = U2
    elif mutate_g == "no-g-dependency":
        i["scopes"].pop(sg)
        i["coverages"].pop(cg)
    return i


results = set()
for order in itertools.permutations(["scopes", "coverages", "coverageScopes"]):
    for rev in (False, True):
        i = incoming_two_subject()
        if rev:
            for key in order:
                i[key] = dict(reversed(list(i[key].items())))
        results.add(json.dumps(ev(dict(REACH, op="all-covered", endpoint="target"), i), sort_keys=True))
OUT["incomingDisjointScopesOrdering"] = {"orderings": 12, "distinct": len(results), "sample": json.loads(sorted(results)[0])}
OUT["incomingPartialDependencyObservation"] = {
    m: ev(dict(REACH, op="all-covered", endpoint="target"), incoming_two_subject(m))
    for m in ("wrong-universe", "no-g-dependency")}

# 5. refusal versus ignore: exact-coordinate dependency scope with a missing carrier field
missing_enc = base()
missing_enc["scopes"][K.scope2("2")].pop("enumeratorClosure")
OUT["exactScopeMissingEnumeratorClosure"] = ev(dict(REACH, op="all-covered"), missing_enc)

# 6. known reachability facts beside a wrong-coordinate dependency scope
fid = K.fact2("1")
fact = {"factId": fid, "relation": "reachability", "resolution": "from-resolved-calls",
        "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": K.C_PROV, "confidenceMillionths": 1000000,
        "payload": {"origin": F_SYM, "reachable": G_SYM},
        "anchors": [{"path": "src/a.ts", "blobDigest": K.H("0"), "startByte": 0, "endByte": 1}]}
OUT["knownFact"] = {}
for label, inputs in (("exact-dependency", base()), ("wrong-coordinate-dependency", mutate(base(), "sourceUniverse", "absent", None))):
    inputs["facts"] = {fid: fact}
    OUT["knownFact"][label] = {op + (str(extra.get("n")) if extra else ""): ev(dict(REACH, op=op, **extra), inputs)
                               for op, extra in (("exists", {}), ("none", {}), ("count-at-most", {"n": 0}),
                                                 ("count-at-most", {"n": 1}), ("all-covered", {}))}

# 7. different-kind whole-source: clones -> declares
def clones_inputs(declares_mapping):
    i = K.base_inputs(enumerationPlan=K.plan_one(cap="clones-fact", kinds=["file"]), inventories=[K.inv_file()])
    K.install_pair(i, *K.paired("clones", "normalized-body-hash", U1, U1, ["src/a.ts"], tag="1"))
    if declares_mapping != "no-declares":
        c, cv = K.coverage("declares", "syntactic", U1, U1, cid="5")
        i["coverages"][c] = cv
        if declares_mapping == "mapped-to-wrong-coordinate-scope":
            s, sc = K.scope("declares", "syntactic", U2, U1, [F_SYM], sid="5")
            i["scopes"][s] = sc
            i["coverageScopes"][c] = s
    return i


FILE_SUBJ = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
OUT["differentKindWholeSource"] = {m: ev({"op": "all-covered", "relation": "clones", "minResolution": "normalized-body-hash",
                                          "filters": []}, clones_inputs(m), FILE_SUBJ)
                                   for m in ("no-declares", "unscoped", "mapped-to-wrong-coordinate-scope")}

# 8. synthetic depth-2 graph: calls -> declares@syntactic (same kind as the symbol subject)
saved = copy.deepcopy(AM.N.DEPENDS_ON)
try:
    AM.N.DEPENDS_ON["calls"] = [{"relation": "declares", "minResolution": "syntactic"}]
    deep = base()
    c6, cv6 = K.coverage("declares", "syntactic", U1, U1, cid="6")
    s6, sc6 = K.scope("declares", "syntactic", U1, U1, [F_SYM], sid="6")
    deep["coverages"][c6] = cv6
    deep["scopes"][s6] = sc6
    deep["coverageScopes"][c6] = s6
    wrong = copy.deepcopy(deep)
    wrong["scopes"][s6]["sourceUniverse"] = U2
    OUT["syntheticDepth2"] = {"exact": ev(dict(REACH, op="all-covered"), deep),
                              "declaresScopeWrongUniverse": ev(dict(REACH, op="all-covered"), wrong)}
finally:
    AM.N.DEPENDS_ON.clear()
    AM.N.DEPENDS_ON.update(saved)

print(json.dumps(OUT, indent=1, default=str))
