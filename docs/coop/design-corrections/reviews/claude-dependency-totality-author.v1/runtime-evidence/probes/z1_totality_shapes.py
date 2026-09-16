"""Z1 — per-subject dependency totality shapes on the REAL atom API.

argv[1] = previous | successor
  previous  : dependency-scope-successor.v1 atom_model (the completed 95-check model, read-only)
  successor : dependency-totality-successor.v1 atom_model (this authoring tree)
Builders always come from the PREVIOUS tree's check-atoms.v1.py, so only the model differs.

STANDING: synthetic atom-api over synthetic inputs. The `synthetic-graph` rows also patch DEPENDS_ON
in-process (helper-graph evidence only). Nothing here is native-producer, closed-enumeration or
retained-Run evidence.
"""
import copy
import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path

TREES = {
    "previous": Path("/tmp/opensip-design-corrections/dependency-scope-successor.v1/source"),
    "successor": Path("/tmp/opensip-design-corrections/dependency-totality-successor.v1/source"),
}
FOUND = "docs/coop/design-corrections/foundation"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


K = load("chk_previous", TREES["previous"] / FOUND / "check-atoms.v1.py")
AM = load("atom_under_test", TREES[sys.argv[1]] / FOUND / "atom_model.v1.py")
U1, U2, F, G = K.U1, K.U2, K.F_SYM, K.G_SYM
H_SYM = "ts-symbol:src/a.ts#h"
REACH = {"relation": "reachability", "minResolution": "from-resolved-calls", "filters": []}
OPS = (("none", {}), ("exists", {}), ("count-at-most-0", {"n": 0}), ("count-at-most-1", {"n": 1}), ("all-covered", {}))


def ev(atom, inputs, subj=None):
    try:
        r = AM.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(subj or K.F_SUBJ), copy.deepcopy(inputs))
    except AM.AtomAdmissionError as e:
        return {"admission": "REFUSE", "key": e.key, "detail": str(e)[:140]}
    return {"admission": "ADMIT", "value": r["value"],
            "causes": sorted(([c["code"], c.get("universe"), c.get("nativeCause")] for c in r["causes"]),
                             key=lambda t: tuple(x or "" for x in t)),
            "nativeDeficiencies": r["nativeDeficiencies"], "coverageIds": r["coverageIds"], "known": r["knownFactIds"]}


def ops(inputs, endpoint="target", subj=None):
    return {name: ev(dict(REACH, op=name.split("-0")[0].split("-1")[0], endpoint=endpoint, **extra), inputs, subj)
            for name, extra in OPS}


def primary(partitions):
    """partitions: list of subject lists for the reachability primary; each gets its own scope+complete Coverage."""
    # Inventory is exactly {f, g}. The first run of this probe also inventoried h, which no primary scope
    # contains, so every incoming row carried uncovered-expected-source-subject; that receipt is kept.
    i = K.base_inputs(enumerationPlan=K.plan_one(cap="reachability"),
                      inventories=[K.inv_symbol(), K.inv_symbol(nid=G, qn="g")])
    for n, subjects in enumerate(partitions):
        K.install_pair(i, *K.paired("reachability", "from-resolved-calls", U1, U1, subjects, tag="1abc"[n] if n else "1"))
    return i


def dep(i, subjects, tag, cov=True, target=U1, state=None, carrier=None, coverage_state="complete"):
    sid, sc = K.scope("calls", "resolved-callee", U1, target, subjects, sid=tag)
    i["scopes"][sid] = sc
    if cov:
        cid, cv = K.coverage("calls", "resolved-callee", U1, target, cov=coverage_state, cid=tag, state=state)
        if carrier:
            cv["entry"]["deficiency"], cv["entry"]["nativeCause"] = carrier
        i["coverages"][cid] = cv
        i["coverageScopes"][cid] = sid
    return i


OUT = {"model": sys.argv[1],
       "modelSha256": hashlib.sha256((TREES[sys.argv[1]] / FOUND / "atom_model.v1.py").read_bytes()).hexdigest()}

# A. merged {f,g} primary: dependency coverage variants
merged = {
    "no-dependency": primary([[F, G]]),
    "f-only": dep(primary([[F, G]]), [F], "2"),
    "g-only": dep(primary([[F, G]]), [G], "4"),
    "f-and-g-disjoint": dep(dep(primary([[F, G]]), [F], "2"), [G], "4"),
    "one-scope-spanning-f-g": dep(primary([[F, G]]), [F, G], "2"),
    "f + g-scope-without-coverage": dep(dep(primary([[F, G]]), [F], "2"), [G], "4", cov=False),
    "f + g-coverage-at-other-target": dep(dep(primary([[F, G]]), [F], "2"), [G], "4", target=U2),
    "f + g-wrong-universe-scope": None,
    "f + unrelated-h": dep(dep(primary([[F, G]]), [F], "2"), [H_SYM], "5"),
    "f-and-g + unrelated-h": dep(dep(dep(primary([[F, G]]), [F], "2"), [G], "4"), [H_SYM], "5"),
}
w = dep(dep(primary([[F, G]]), [F], "2"), [G], "4")
w["scopes"][K.scope2("4")]["sourceUniverse"] = U2
merged["f + g-wrong-universe-scope"] = w
OUT["merged"] = {k: {"target": ops(v), "source-f": ops(v, "source")} for k, v in merged.items()}

# B. split {f},{g} primary partitions: same dependency variants
split = {
    "f-only": dep(primary([[F], [G]]), [F], "2"),
    "g-only": dep(primary([[F], [G]]), [G], "4"),
    "f-and-g-disjoint": dep(dep(primary([[F], [G]]), [F], "2"), [G], "4"),
}
OUT["split"] = {k: {"target": ops(v)} for k, v in split.items()}

# C. partial actual carrier on f, g uncovered or covered
OUT["partialCarrier"] = {
    "f-unknown-carrier + g-uncovered": ops(dep(primary([[F, G]]), [F], "2", coverage_state="unknown",
                                               carrier=("input-closure-incomplete", "lockfile-missing"))),
    "f-unknown-carrier + g-covered": ops(dep(dep(primary([[F, G]]), [F], "2", coverage_state="unknown",
                                                 carrier=("input-closure-incomplete", "lockfile-missing")), [G], "4")),
}

# D. ordering: f-only and f-and-g across insertion orders
OUT["ordering"] = {}
for label, base in (("f-only", merged["f-only"]), ("f-and-g", merged["f-and-g-disjoint"])):
    results = set()
    for order in itertools.permutations(("scopes", "coverages", "coverageScopes", "inventories")):
        for rev in (False, True):
            i = copy.deepcopy(base)
            if rev:
                for key in order:
                    i[key] = list(reversed(i[key])) if isinstance(i[key], list) else dict(reversed(list(i[key].items())))
            results.add(json.dumps(ev(dict(REACH, op="all-covered", endpoint="target"), i), sort_keys=True))
    OUT["ordering"][label] = {"orderings": 48, "distinct": len(results), "sample": json.loads(sorted(results)[0])}

# E. whole-source attestation route: tagged scope {f,g}, no S->U primary Coverage, qualifying attestation
def attested(dep_subjects):
    i = K.base_inputs(enumerationPlan=K.plan_one(cap="reachability"),
                      inventories=[K.inv_symbol(), K.inv_symbol(nid=G, qn="g")])
    sid, sc = K.scope("reachability", "from-resolved-calls", U1, U1, [F, G], sid="1")
    i["scopes"][sid] = sc
    i["incomingSearchAttestations"] = [K.incoming_att("reachability", "from-resolved-calls", U1, U1, [sid],
                                                      [K.inv_symbol(), K.inv_symbol(nid=G, qn="g")])]
    for n, subj in enumerate(dep_subjects):
        dep(i, subj, "24"[n])
    return i


OUT["attestation"] = {k: ops(attested(v)) for k, v in (("no-dependency", []), ("f-only", [[F]]),
                                                        ("f-and-g", [[F], [G]]), ("spanning", [[F, G]]))}

# F. empty-subject primary scope with complete coverage and no dependency
empty = dep(dep(primary([[F, G]]), [F], "2"), [G], "4")
es, esc = K.scope("reachability", "from-resolved-calls", U1, U1, [], sid="7")
ec, ecv = K.coverage("reachability", "from-resolved-calls", U1, U1, cid="7")
K.install_pair(empty, es, esc, ec, ecv)
OUT["emptySubjectPrimary"] = ops(empty)

# G. known incoming reachability facts (origin g reaches f)
fid1, fid2 = K.fact2("1"), K.fact2("2")


def fact(fid, origin):
    return {"factId": fid, "relation": "reachability", "resolution": "from-resolved-calls", "sourceUniverse": U1,
            "targetUniverse": U1, "producerClosure": K.C_PROV, "confidenceMillionths": 1000000,
            "payload": {"origin": origin, "reachable": F},
            "anchors": [{"path": "src/a.ts", "blobDigest": K.H("0"), "startByte": 0, "endByte": 1}]}


OUT["knownFacts"] = {}
for label, base in (("f-only", merged["f-only"]), ("f-and-g", merged["f-and-g-disjoint"])):
    i = copy.deepcopy(base)
    i["facts"] = {fid1: fact(fid1, G)}
    OUT["knownFacts"][label] = ops(i)

# H. synthetic depth-2 graph (calls -> declares): f,g covered for calls; declares only for f
saved = copy.deepcopy(AM.N.DEPENDS_ON)
try:
    AM.N.DEPENDS_ON["calls"] = [{"relation": "declares", "minResolution": "syntactic"}]
    deep = dep(dep(primary([[F, G]]), [F], "2"), [G], "4")
    K.install_pair(deep, *K.paired("declares", "syntactic", U1, U1, [F], tag="6"))
    full = copy.deepcopy(deep)
    K.install_pair(full, *K.paired("declares", "syntactic", U1, U1, [G], tag="8"))
    OUT["syntheticDepth2"] = {"declares-f-only": ev(dict(REACH, op="all-covered", endpoint="target"), deep),
                              "declares-f-and-g": ev(dict(REACH, op="all-covered", endpoint="target"), full)}
finally:
    AM.N.DEPENDS_ON.clear()
    AM.N.DEPENDS_ON.update(saved)

print(json.dumps(OUT, indent=1, default=str))
