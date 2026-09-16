"""Enumeration-admission probe for programEntry x provenance, on the maintained check-enumeration harness.

Tree: env VA_TREE (repo root); default is the verified frozen41 snapshot, loaded read-only (-I -B).
Standing: admit_enumeration only (the enumeration owner join), NOT a Run. Every world reuses the
check-enumeration fixture helpers (membership, scope, uni, graph, binding, unavail_binding, inv, admit);
each case changes the named binding fields and nothing else. Receipt name: argv[1].
"""
import copy
import hashlib
import importlib.util
import json
import os
import sys
import traceback
from pathlib import Path

TREE = Path(os.environ.get("VA_TREE", "/tmp/opensip-design-corrections/candidate-subject.v41"))
RT = Path("/private/tmp/opensip-design-corrections/claude-program-entry-enforcement.v1")
_spec = importlib.util.spec_from_file_location("pe_check_enum", TREE / "docs/coop/design-corrections/foundation/check-enumeration.v1.py")
E = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(E)
M = E.M
SYNTAX_DOMAIN = "native.semantic-universe.syntax.v2"

sc = E.scope()
source = E.blobs()
roots = ["src/a.ts", "src/b.ts", "src/extra.js"]


def world(mode="ts-tsconfig", unit_patch=None):
    memb = E.membership()
    if unit_patch:
        memb["units"][0].update(unit_patch)
    file_ext = M.host_file_extent(memb, E.SNAPSHOT, sc, ".", [])
    proj = M.project_named_packages(E.SNAPSHOT, sc, ".", memb, source, [])
    pkg_ext = proj["namedPaths"]
    return {
        "mode": mode, "memb": memb, "file_ext": file_ext, "pkg_ext": pkg_ext,
        "inv_ext": [{"kind": "file", "paths": file_ext}, {"kind": "package", "paths": pkg_ext}],
        "files": E.sort_files([E.file_row(p) for p in file_ext]),
        "pkgs": E.sort_pkgs([E.pkg_row(n["path"], n["packageName"]) for n in proj["named"]]),
    }


def plan(w, bindings):
    return {"schemaVersion": 1, "snapshotId": E.SNAP, "scopeDigest": M.raw_digest(sc),
            "membershipDigest": M.raw_digest(w["memb"]),
            "cells": [{"capabilityId": "inventory", "languageMode": w["mode"], "workspaceRoot": ".",
                       "required": True, "kinds": M._cap_kinds("inventory"), "programBindings": bindings}]}


def invs(w, programs, state="complete"):
    out = []
    for p in range(programs):
        if state == "complete":
            out += [E.inv("file", "complete", copy.deepcopy(w["files"]), w["file_ext"], prog=p),
                    E.inv("package", "complete", copy.deepcopy(w["pkgs"]), w["pkg_ext"], prog=p)]
        else:
            carrier = {"deficiency": "provider-unavailable", "nativeCause": None}
            out += [E.inv("file", "unavailable", [], [], prog=p, extra=dict(carrier)),
                    E.inv("package", "unavailable", [], [], prog=p, extra=dict(carrier))]
    return out


def unavail(ordinal, w, provenance, entry):
    b = E.unavail_binding(ordinal, w["inv_ext"])
    b["provenance"] = provenance
    b["programEntry"] = entry
    return b


results, order = {}, []


def case(name, w, bindings, universes, retained, domains, note, state="complete"):
    order.append(name)
    try:
        spec_obj = E.spec([{"capabilityId": "inventory", "languageMode": w["mode"], "workspaceRoot": ".", "required": True}])
        res = E.admit(plan(w, bindings), invs(w, len(bindings), state), w["memb"], sc, universes, retained, source,
                      spec_obj=spec_obj, universe_domains=domains)
        results[name] = {"note": note, "standing": "admit_enumeration (not a Run)",
                         "bindings": [{k: b[k] for k in ("ordinal", "provenance", "universe", "programEntry")} for b in bindings],
                         "result": res["result"], "refusals": res["refusals"]}
    except Exception as exc:  # noqa: BLE001 - preserved verbatim
        results[name] = {"note": note, "probeError": type(exc).__name__ + ":" + str(exc)[:500],
                         "traceback": traceback.format_exc()[-1500:]}


ts = world()
TSU = {E.U1: E.uni("ts-tsconfig", roots), E.U2: E.uni("ts-tsconfig", ["src/b.ts"])}
TSR = {E.U1: {"configGraph": E.graph("tsconfig.json")}, E.U2: {"configGraph": E.graph("tsconfig.build.json")}}
TSD = {E.U1: E.TS_DOMAIN, E.U2: E.TS_DOMAIN}
b = E.binding

case("TS-default-null-control", ts, [b(0, E.U1, None, ts["inv_ext"])], TSU, TSR, TSD,
     "maintained positive: default-unit, null, U-1 marker tsconfig.json = graph entry")
case("TS-explicit-extra-program-nonnull-control", ts,
     [b(0, E.U1, None, ts["inv_ext"]), b(1, E.U2, "tsconfig.build.json", ts["inv_ext"], "explicit-plan-selection")],
     TSU, TSR, TSD, "maintained two-configs shape")
case("TS-explicit-selects-marker-config-nonnull", ts,
     [b(0, E.U1, "tsconfig.json", ts["inv_ext"], "explicit-plan-selection")], TSU, TSR, TSD,
     "semantic-fixture shape: explicit selection naming the marker config")
case("TS-provenance-only-explicit-null", ts,
     [b(0, E.U1, None, ts["inv_ext"], "explicit-plan-selection")], TSU, TSR, TSD,
     "QUESTION: default control with ONLY provenance changed to explicit-plan-selection")
case("TS-explicit-null-graph-differs-from-marker", ts,
     [b(0, E.U1, None, ts["inv_ext"]), b(1, E.U2, None, ts["inv_ext"], "explicit-plan-selection")],
     TSU, TSR, TSD, "explicit null whose retained graph entry is tsconfig.build.json")
case("TS-default-nonnull-marker", ts, [b(0, E.U1, "tsconfig.json", ts["inv_ext"])], TSU, TSR, TSD,
     "default-unit carrying the marker path")

syn = world("js-synthesized", {"languageMode": "js-synthesized", "unitKind": "js-program", "markerPath": "package.json",
                               "recognizerId": "node-package"})
SYU = {E.U1: E.uni("js-synthesized", roots)}
SYR = {E.U1: {"configGraph": E.graph(None)}}
case("JSSYN-default-null-control", syn, [b(0, E.U1, None, syn["inv_ext"])], SYU, SYR, {E.U1: E.TS_DOMAIN},
     "js-synthesized default: null, graph entry null")
case("JSSYN-provenance-only-explicit-null", syn, [b(0, E.U1, None, syn["inv_ext"], "explicit-plan-selection")], SYU, SYR,
     {E.U1: E.TS_DOMAIN}, "js-synthesized with ONLY provenance changed")

for fam, mode, dom in (("RUST", "rust-cargo", E.RUST_DOMAIN), ("SYNTAX", "syntax-only", SYNTAX_DOMAIN)):
    w = world(mode)
    U = {E.U1: {"nativeContextId": E.CTX}}
    case(fam + "-default-null", w, [b(0, E.U1, None, w["inv_ext"])], U, {}, {E.U1: dom}, mode + " default null")
    case(fam + "-explicit-null", w, [b(0, E.U1, None, w["inv_ext"], "explicit-plan-selection")], U, {}, {E.U1: dom},
         mode + " explicit null (preservation)")
    case(fam + "-explicit-nonnull", w, [b(0, E.U1, "Cargo.toml" if fam == "RUST" else "README.md", w["inv_ext"], "explicit-plan-selection")],
         U, {}, {E.U1: dom}, mode + " explicit with a snapshot path")

for prov, entry in (("default-unit", None), ("explicit-plan-selection", None), ("default-unit", "tsconfig.json"),
                    ("explicit-plan-selection", "tsconfig.build.json")):
    case("UNAVAILABLE-" + prov + "-" + str(entry), ts, [unavail(0, ts, prov, entry)], TSU, TSR, TSD,
         "unavailable binding (universe null), provider-unavailable inventories", state="unavailable")

label = sys.argv[1] if len(sys.argv) > 1 else "probe-admission-base.json"
path = RT / "receipts" / label
path.parent.mkdir(parents=True, exist_ok=True)
if path.exists():
    raise SystemExit("refusing to overwrite " + str(path))
raw = json.dumps({"tree": str(TREE), "order": order, "cases": results}, indent=2).encode() + b"\n"
path.write_bytes(raw)
for n in order:
    r = results[n]
    print(n, "->", r.get("result") or "PROBE ERROR " + r.get("probeError", ""), r.get("refusals"))
print("receipt", label, hashlib.sha256(raw).hexdigest())
