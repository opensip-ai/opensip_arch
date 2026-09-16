"""Discrimination probe for nested Cargo workspace folding (native section 1.4 U-2 / U-4b.2), standalone reference.

Trusted marker observations only: no Cargo, compiler or repository code runs; nothing here says a marker set is a
valid Cargo layout. Loads the native model (and the enumeration model/checker helpers) from SOURCE_ROOT, never writes
under it. Usage: discriminate.py OUT_JSON SOURCE_ROOT

Parts
  named     hand-spelled expectations: ordinary, nested depth, siblings, prefix traps, ordering, explicit inner/outer
            selections, admitted boundaries, pruning, membership rows, scope, enumeration order law and derivation.
  sweep     every Cargo marker assignment {absent, package, workspace} over six directories, automatic and every
            explicit selection of one or two present directories, compared with an oracle written from the published
            law (not from the model); plus the P22 equality and the "exactly one enclosing workspace unit" count.
  digests   per sweep input the sha256 of the exact output (or the escaping exception type), for pre/post comparison.
"""
import hashlib
import importlib.util
import itertools
import json
import sys
import time
import traceback
from pathlib import Path

OUT = Path(sys.argv[1])
SRC = Path(sys.argv[2])
KIT = SRC / "docs/coop/design-corrections"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


NV = load("probe_native_model", KIT / "native/native_evidence_model.v2.py")
ENUM = load("probe_enumeration_model", KIT / "foundation/enumeration_model.v1.py")
DD = NV.DD
WS = {"sha256": "a" * 64, "isCargoWorkspace": True}
PKG = {"sha256": "a" * 64, "isCargoWorkspace": False}


def mk(spec):
    return {(d + "/" if d else "") + "Cargo.toml": dict(WS if k == "ws" else PKG) for d, k in spec.items()}


def call(fn, *a, **kw):
    try:
        return {"raised": False, "value": fn(*a, **kw)}
    except Exception as e:  # noqa: BLE001 - the point is to record what escapes
        tb = traceback.extract_tb(e.__traceback__)[-1]
        return {"raised": True, "exceptionType": type(e).__name__, "message": str(e)[:300],
                "at": "%s:%d" % (Path(tb.filename).name, tb.lineno)}


def summary(out):
    return [[u["rootPath"], u["languageFamily"], u["unitKind"], u["provenance"], u["memberPackageRoots"]] for u in out["units"]]


def ordinals_ok(out):
    return all(u["unitOrdinal"] == i for i, u in enumerate(out["units"]))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def inventory(markers, nested_projects=(), nested_repositories=()):
    return {"schemaVersion": 2, "source": "security.discovery", "selectedRoot": "/home/alice/repo",
            "nestedRepositories": list(nested_repositories), "nestedProjects": list(nested_projects),
            "custodyExcludedUnits": [], "prunedTrees": DD.enumerate_units(list(markers), enforce_limit=False)["prunedTrees"]}


NAMED = []


def named(case_id, law, markers, roots=None, bounds=None, units=None, excluded=None, refused=None, pruned=None):
    r = call(NV.discover_units, markers, roots, bounds)
    row = {"id": case_id, "law": law, "markers": sorted(markers), "explicitRoots": roots,
           "boundaries": None if bounds is None else {k: bounds[k] for k in ("nestedRepositories", "nestedProjects")}}
    if r["raised"]:
        row.update(observed={k: r[k] for k in ("exceptionType", "message", "at")}, holds=False)
    else:
        out = r["value"]
        observed = {"units": summary(out), "ordinalsAreIndex": ordinals_ok(out),
                    "refused": None if out["refused"] is None else out["refused"]["detail"],
                    "excludedUnits": [[x["path"], x["reason"], x["anchor"]] for x in out["boundaries"]["excludedUnits"]],
                    "prunedTrees": sorted(t["path"] for t in out["prunedTrees"])}
        holds = observed["ordinalsAreIndex"] and observed["refused"] == refused
        if units is not None:
            holds = holds and observed["units"] == units
        if excluded is not None:
            holds = holds and observed["excludedUnits"] == excluded
        if pruned is not None:
            holds = holds and observed["prunedTrees"] == pruned
        row.update(observed=observed, holds=holds)
        row["_out"] = out
    row["expected"] = {"units": units, "refused": refused, "excludedUnits": excluded, "prunedTrees": pruned}
    NAMED.append(row)
    return row


def ws_unit(root, members, prov="DISCOVERED"):
    return [root, "rust", "cargo-workspace", prov, members]


def pkg_unit(root, prov="DISCOVERED"):
    return [root, "rust", "cargo-package", prov, []]


t0 = time.time()
U2 = "U-2/U-4b.2"
S3 = {"": "ws", "nested": "ws", "nested/pkg": "pkg"}
named("ordinary-workspace-and-package", U2, mk({"": "ws", "pkg": "pkg"}), units=[ws_unit("", ["pkg"])])
named("nested-workspace-leaf", U2, mk({"": "ws", "nested": "ws"}), units=[ws_unit("", ["nested"])])
named("nested-workspace-with-package", U2, mk(S3), units=[ws_unit("", ["nested", "nested/pkg"])])
named("depth-three-workspaces-and-package", U2, mk({"": "ws", "a": "ws", "a/b": "ws", "a/b/c": "pkg"}),
      units=[ws_unit("", ["a", "a/b", "a/b/c"])])
named("depth-package-between-workspaces", U2, mk({"": "ws", "a": "pkg", "a/b": "ws", "a/b/c": "pkg"}),
      units=[ws_unit("", ["a", "a/b", "a/b/c"])])
named("nested-without-root-manifest", U2, mk({"a": "ws", "a/b": "ws", "a/b/c": "pkg"}), units=[ws_unit("a", ["a/b", "a/b/c"])])
named("sibling-outer-workspaces-keep-their-own-subtrees", U2,
      mk({"w1": "ws", "w1/inner": "ws", "w1/inner/p": "pkg", "w2": "ws", "w2/q": "pkg"}),
      units=[ws_unit("w1", ["w1/inner", "w1/inner/p"]), ws_unit("w2", ["w2/q"])])
named("segment-prefix-is-not-an-ancestor", "U-4b.2 strictly below by segment",
      mk({"nested": "ws", "nested/pkg": "pkg", "nestedx/pkg": "pkg", "nested-x": "pkg"}),
      units=[ws_unit("nested", ["nested/pkg"]), pkg_unit("nested-x"), pkg_unit("nestedx/pkg")])
named("member-roots-strict-utf8-order", "U-4b.3", mk({"": "ws", "nested": "ws", "nested/pkg": "pkg", "nested-x": "pkg"}),
      units=[ws_unit("", ["nested", "nested-x", "nested/pkg"])])
named("package-under-package-is-not-folded", "U-4b.2 only a workspace folds", mk({"a": "pkg", "a/b": "pkg"}),
      units=[pkg_unit("a"), pkg_unit("a/b")])
named("workspace-under-root-package-is-its-own-unit", "U-4b.2 only a workspace folds",
      mk({"": "pkg", "nested": "ws", "nested/pkg": "pkg"}), units=[pkg_unit(""), ws_unit("nested", ["nested/pkg"])])

m = mk(S3)
named("explicit-outer-root-equals-automatic", "P22", m, ["."], units=[ws_unit("", ["nested", "nested/pkg"], "EXPLICIT")])
named("explicit-inner-workspace", "P22", m, ["nested"], units=[ws_unit("nested", ["nested/pkg"], "EXPLICIT")])
named("explicit-inner-package-alone", "P22", m, ["nested/pkg"], units=[pkg_unit("nested/pkg", "EXPLICIT")])
named("explicit-outer-and-inner-workspace", "P22 + U-4b.2", m, [".", "nested"], units=[ws_unit("", ["nested", "nested/pkg"], "EXPLICIT")])
named("explicit-outer-and-inner-package", "P22 + U-4b.2", m, [".", "nested/pkg"], units=[ws_unit("", ["nested", "nested/pkg"], "EXPLICIT")])
named("explicit-inner-workspace-and-its-package", "P22 + U-4b.2", m, ["nested", "nested/pkg"], units=[ws_unit("nested", ["nested/pkg"], "EXPLICIT")])
named("explicit-middle-workspace-depth", "P22", mk({"": "ws", "a": "pkg", "a/b": "ws", "a/b/c": "pkg"}), ["a/b"],
      units=[ws_unit("a/b", ["a/b/c"], "EXPLICIT")])

b2 = mk({"": "ws", "nested": "ws", "nested/a": "pkg", "nested/b": "pkg"})
named("boundary-at-nested-workspace-excludes-its-subtree", "U-8", m, None, inventory(m, ["nested"]),
      units=[ws_unit("", [])], excluded=[["nested", "nested-project", "nested"], ["nested/pkg", "nested-project", "nested"]])
named("boundary-below-nested-workspace-keeps-the-rest-folded", "U-8 + U-4b.2", b2, None, inventory(b2, ["nested/b"]),
      units=[ws_unit("", ["nested", "nested/a"])], excluded=[["nested/b", "nested-project", "nested/b"]])
named("nested-repository-at-inner-package", "U-8", m, None, inventory(m, (), ["nested/pkg"]),
      units=[ws_unit("", ["nested"])], excluded=[["nested/pkg", "nested-repository", "nested/pkg"]])
named("explicit-root-under-boundary-still-refuses", "U-8", m, ["nested/pkg"], inventory(m, ["nested"]),
      units=[], refused="native.explicit-root-crosses-boundary")
named("explicit-outer-root-with-inner-boundary", "P22 + U-8", b2, ["."], inventory(b2, ["nested/b"]),
      units=[ws_unit("", ["nested", "nested/a"], "EXPLICIT")], excluded=[["nested/b", "nested-project", "nested/b"]])

p1 = dict(mk(S3), **{"nested/pkg/src/target/Cargo.toml": dict(PKG), "nested/pkg/target/debug/build/x/Cargo.toml": dict(PKG),
                     "nested/target/package/y/Cargo.toml": dict(PKG), "node_modules/z/Cargo.toml": dict(PKG)})
pr = named("pruning-under-nested-roots", "U-4a + U-4b.1/2", p1,
           units=[ws_unit("", ["nested", "nested/pkg", "nested/pkg/src/target"])],
           pruned=["nested/pkg/target", "nested/target", "node_modules"])

MEMBERSHIP = {}
files = ["README.md", "nested/pkg/src/lib.rs", "nested/pkg/src/target/mod.rs", "nested/pkg/target/debug/x.rs",
         "nested/src/main.rs", "nested/target/debug/y.rs", "node_modules/z/src/lib.rs", "src/main.rs", "target/debug/z.rs"]
if "_out" in pr:
    units = pr["_out"]["units"]
    mem = call(NV.assign_membership, units, files)
    if mem["raised"]:
        MEMBERSHIP["rows"] = {k: mem[k] for k in ("exceptionType", "message", "at")}
        MEMBERSHIP["holds"] = False
    else:
        rows = [[r["path"], r["languageFamily"], r["unitOrdinal"], r["membership"], r["reason"]] for r in mem["value"]["rows"]]
        want = [["README.md", "none", None, "syntax-only", "grammar-only"],
                ["nested/pkg/src/lib.rs", "rust", 0, "program-member", "deepest-unit-in-language"],
                ["nested/pkg/src/target/mod.rs", "rust", 0, "program-member", "deepest-unit-in-language"],
                ["nested/pkg/target/debug/x.rs", "rust", None, "syntax-only", "host-ignore-convention"],
                ["nested/src/main.rs", "rust", 0, "program-member", "deepest-unit-in-language"],
                ["nested/target/debug/y.rs", "rust", None, "syntax-only", "host-ignore-convention"],
                ["node_modules/z/src/lib.rs", "rust", None, "syntax-only", "host-ignore-convention"],
                ["src/main.rs", "rust", 0, "program-member", "deepest-unit-in-language"],
                ["target/debug/z.rs", "rust", None, "syntax-only", "host-ignore-convention"]]
        faults = []
        law = call(ENUM._membership_order_law, mem["value"], faults)
        scope = call(NV.unit_scope_descriptor, units, [])
        excluded_prefixes = None if scope["raised"] else scope["value"]["scopeDescriptor"]["excludedPathPrefixes"]
        want_prefixes = [".git", "nested/pkg/src/target/target", "nested/pkg/target", "nested/target", "node_modules", "target"]
        MEMBERSHIP = {"rows": rows, "rowsHold": rows == want, "orderLawFaults": faults, "orderLawRaised": law["raised"],
                      "excludedPathPrefixes": excluded_prefixes, "excludedPathPrefixesHold": excluded_prefixes == want_prefixes,
                      "holds": rows == want and faults == [] and not law["raised"] and excluded_prefixes == want_prefixes}
else:
    MEMBERSHIP = {"notRun": "discovery for pruning-under-nested-roots raised", "holds": False}

# Enumeration admission: the derivation witness calls discover_units inside `except (AdmissionError, ValidationError)`.
ENUMERATION = {}
try:
    CE = load("probe_check_enumeration", KIT / "foundation/check-enumeration.v1.py")
    M = CE.M
    derivation_markers = dict(mk(S3), **{"tsconfig.json": {"sha256": "1" * 64}})
    memb = CE.membership()
    sc = CE.scope()
    faults = []
    file_ext = M.host_file_extent(memb, CE.SNAPSHOT, sc, ".", faults)
    u1 = CE.uni("ts-tsconfig", ["src/a.ts", "src/b.ts", "src/extra.js"])
    universes = {CE.U1: u1, CE.U2: CE.uni("ts-tsconfig", ["src/b.ts"])}
    retained = {CE.U1: {"configGraph": CE.graph("tsconfig.json")}, CE.U2: {"configGraph": CE.graph("tsconfig.build.json")}}
    source = CE.blobs()
    pkg_proj = M.project_named_packages(CE.SNAPSHOT, sc, ".", memb, source, [])
    pkg_ext = pkg_proj["namedPaths"]
    inv_ext = [{"kind": "file", "paths": file_ext}, {"kind": "package", "paths": pkg_ext}]
    ep = {"schemaVersion": 1, "snapshotId": CE.SNAP, "scopeDigest": M.raw_digest(sc), "membershipDigest": M.raw_digest(memb),
          "cells": [{"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": True,
                     "kinds": M._cap_kinds("inventory"), "programBindings": [CE.binding(0, CE.U1, None, inv_ext)]}]}
    frows = CE.sort_files([CE.file_row(p) for p in file_ext])
    prows = CE.sort_pkgs([CE.pkg_row(n["path"], n["packageName"]) for n in pkg_proj["named"]])

    def admit_with(derivation):
        return call(CE.admit, ep, [CE.inv("file", "complete", frows, file_ext), CE.inv("package", "complete", prows, pkg_ext)],
                    memb, sc, universes, retained, source, membership_derivation=derivation)

    base = admit_with(None)
    ENUMERATION["baselineWithoutDerivation"] = base if base["raised"] else {"result": base["value"]["result"], "refusals": base["value"]["refusals"]}
    for label, mode in (("nested-markers-standalone-fixture-derivation", "standalone-fixture"),):
        got = admit_with({"markers": derivation_markers, "files": list(CE.SNAPSHOT), "mode": mode})
        ENUMERATION[label] = ({k: got[k] for k in ("raised", "exceptionType", "message", "at")} if got["raised"]
                              else {"raised": False, "result": got["value"]["result"], "refusals": got["value"]["refusals"]})
    control = admit_with({"markers": {"tsconfig.json": {"sha256": "1" * 64}}, "files": list(CE.SNAPSHOT), "mode": "standalone-fixture"})
    ENUMERATION["tsconfig-only-derivation-control"] = ({k: control[k] for k in ("raised", "exceptionType", "message", "at")} if control["raised"]
                                                        else {"raised": False, "result": control["value"]["result"], "refusals": control["value"]["refusals"]})
except Exception as e:  # noqa: BLE001
    ENUMERATION["harnessError"] = "".join(traceback.format_exception_only(type(e), e)).strip()

# ---------------------------------------------------------------------------------------------------- sweep
DIRS = ["", "a", "a/b", "a/b/c", "a-b", "ab/c"]


def below(d, w):
    return d != w and (w == "" or d.startswith(w + "/"))


def oracle(spec, roots):
    """Published law, independent of the model: selection (P22), then U-4b.2 folding into the deepest enclosing
    cargo-workspace UNIT. Returns (units, enclosing-workspace-unit counts for every folded directory)."""
    if roots is None:
        kept, prov = set(spec), "DISCOVERED"
    else:
        sel = set(roots)
        sel_ws = {r for r in sel if spec[r] == "ws"}
        kept, prov = sel | {d for d in spec if any(below(d, w) for w in sel_ws)}, "EXPLICIT"
    ws_dirs = {d for d in kept if spec[d] == "ws"}
    unit_dirs = sorted((d for d in kept if not any(below(d, w) for w in ws_dirs)), key=lambda x: x.encode("utf-8"))
    members = {d: [] for d in unit_dirs}
    counts = []
    for d in kept:
        if d in members:
            continue
        targets = [w for w in unit_dirs if spec[w] == "ws" and below(d, w)]
        counts.append(len(targets))
        if targets:
            members[max(targets, key=len)].append(d)
    return ([[d, "rust", "cargo-workspace" if spec[d] == "ws" else "cargo-package", prov,
              sorted(members[d], key=lambda x: x.encode("utf-8"))] for d in unit_dirs], counts)


spell = lambda d: "." if d == "" else d
sweep = {"inputs": 0, "raised": {}, "raisedExamples": [], "oracleMismatch": 0, "oracleMismatchExamples": [],
         "ordinalFaults": 0, "refusedUnexpectedly": 0, "oracleEnclosingUnitCounts": {}, "p22Checked": 0, "p22Mismatch": 0,
         "p22Examples": []}
digests = {}
for kinds in itertools.product(("-", "pkg", "ws"), repeat=len(DIRS)):
    spec = {d: k for d, k in zip(DIRS, kinds) if k != "-"}
    if not spec:
        continue
    markers = mk(spec)
    present = sorted(spec, key=lambda x: x.encode("utf-8"))
    selections = [None] + [[d] for d in present] + [list(p) for p in itertools.combinations(present, 2)]
    for roots in selections:
        key = json.dumps([sorted(spec.items()), roots])
        sweep["inputs"] += 1
        r = call(NV.discover_units, markers, None if roots is None else [spell(d) for d in roots])
        if r["raised"]:
            sweep["raised"][r["exceptionType"]] = sweep["raised"].get(r["exceptionType"], 0) + 1
            if len(sweep["raisedExamples"]) < 8:
                sweep["raisedExamples"].append({"spec": spec, "roots": roots, "exceptionType": r["exceptionType"], "at": r["at"]})
            digests[key] = "raise:" + r["exceptionType"]
            continue
        out = r["value"]
        digests[key] = digest(out)
        want, counts = oracle(spec, roots)
        for c in counts:
            sweep["oracleEnclosingUnitCounts"][str(c)] = sweep["oracleEnclosingUnitCounts"].get(str(c), 0) + 1
        if out["refused"] is not None:
            sweep["refusedUnexpectedly"] += 1
        if not ordinals_ok(out):
            sweep["ordinalFaults"] += 1
        if summary(out) != want:
            sweep["oracleMismatch"] += 1
            if len(sweep["oracleMismatchExamples"]) < 8:
                sweep["oracleMismatchExamples"].append({"spec": spec, "roots": roots, "observed": summary(out), "oracle": want})
        if roots is not None and len(roots) == 1 and spec[roots[0]] == "ws":
            w = roots[0]
            restricted = mk({d: k for d, k in spec.items() if d == w or below(d, w)})
            auto = call(NV.discover_units, restricted)
            sweep["p22Checked"] += 1
            if auto["raised"]:
                ok = False
            else:
                a = [u for u in summary(auto["value"]) if u[0] == w]
                e = [u for u in summary(out) if u[0] == w]
                ok = len(a) == len(e) == 1 and a[0][:3] + a[0][4:] == e[0][:3] + e[0][4:] and e[0][3] == "EXPLICIT"
            if not ok:
                sweep["p22Mismatch"] += 1
                if len(sweep["p22Examples"]) < 8:
                    sweep["p22Examples"].append({"spec": spec, "root": w})

report = {
    "artifact": "nested-workspace-author.discrimination-probe", "version": 1,
    "standing": "standalone reference probe over trusted marker observations; no Cargo/compiler/repository execution; no validity of a Cargo layout asserted",
    "sourceRoot": str(SRC),
    "modelSha256": hashlib.sha256((KIT / "native/native_evidence_model.v2.py").read_bytes()).hexdigest(),
    "named": [{k: v for k, v in r.items() if k != "_out"} for r in NAMED],
    "namedHolds": sum(1 for r in NAMED if r["holds"]), "namedTotal": len(NAMED),
    "namedRaised": [r["id"] for r in NAMED if "exceptionType" in r["observed"]],
    "membership": MEMBERSHIP, "enumeration": ENUMERATION, "sweep": sweep, "sweepDigestsSha256": digest(digests),
    "seconds": round(time.time() - t0, 1),
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(report, indent=1) + "\n")
(OUT.parent / (OUT.stem + ".digests.json")).write_text(json.dumps(digests, indent=0, sort_keys=True) + "\n")
print(json.dumps({"namedHolds": "%d/%d" % (report["namedHolds"], report["namedTotal"]), "namedRaised": report["namedRaised"],
                  "membershipHolds": MEMBERSHIP.get("holds"), "enumeration": ENUMERATION,
                  "sweep": {k: sweep[k] for k in ("inputs", "raised", "oracleMismatch", "ordinalFaults", "refusedUnexpectedly",
                                                  "oracleEnclosingUnitCounts", "p22Checked", "p22Mismatch")},
                  "seconds": report["seconds"]}, indent=1))
