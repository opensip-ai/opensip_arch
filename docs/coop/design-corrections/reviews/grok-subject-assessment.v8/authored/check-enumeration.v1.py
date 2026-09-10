#!/usr/bin/env python3
"""Discriminating enumeration-join checks. Not full Run replay."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("enumeration_model_v1", HERE / "enumeration_model.v1.py")
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)
OUT = Path("/tmp/opensip-design-corrections/grok-subject-assessment.v7/check-receipt.json")

HEX = "a" * 64
CTX = "b" * 64
U1 = "c" * 64
U2 = "d" * 64
SNAP = "snapshot2:" + "e" * 64
PLAN_ID = "plan2:" + "f" * 64
CLO = "closure2:" + "1" * 64

SNAPSHOT = ["tsconfig.json", "tsconfig.build.json", "src/a.ts", "src/b.ts", "src/extra.js",
            "package.json", "README.md", "notes.xyz"]


def membership():
    rows = []
    for p in SNAPSHOT:
        if p.startswith("node_modules"):
            rows.append({"path": p, "languageFamily": "none", "unitOrdinal": None,
                         "membership": "syntax-only", "reason": "host-ignore-convention"})
        elif p.endswith((".ts", ".tsx", ".js")):
            rows.append({"path": p, "languageFamily": "tsjs", "unitOrdinal": 0,
                         "membership": "program-member", "reason": "deepest-unit-in-language"})
        elif p == "notes.xyz":
            rows.append({"path": p, "languageFamily": "none", "unitOrdinal": None,
                         "membership": "unsupported-file", "reason": "no-bundled-grammar"})
        else:
            rows.append({"path": p, "languageFamily": "none", "unitOrdinal": None,
                         "membership": "syntax-only", "reason": "grammar-only"})
    return {
        "schemaVersion": 1,
        "units": [{
            "unitOrdinal": 0, "rootPath": "", "languageFamily": "tsjs", "languageMode": "ts-tsconfig",
            "unitKind": "ts-program", "markerPath": "tsconfig.json", "markerSha256": "1" * 64,
            "recognizerId": "typescript-config", "recognizerVersion": 1, "provenance": "DISCOVERED",
            "memberPackageRoots": [],
        }],
        "rows": rows,
        "unsupportedFiles": ["notes.xyz"],
        "outsideBoundaryFiles": [],
        "erasedFiles": [],
    }


def scope():
    return {"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": [], "excludedPathPrefixes": []}


def plan_obj(memb, sc):
    return {
        "snapshotId": SNAP,
        "scopeDigest": M.raw_digest(sc),
        "nativeContextDigests": [CTX],
        "semanticClosures": [CLO],
        "analysisSpecDigest": HEX,
        "policyDigest": HEX,
    }


def spec(required=True):
    return {"requestedCapabilities": [
        {"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": required}
    ]}


def graph(entry):
    nodes = []
    if entry is not None:
        nodes = [{"path": entry, "contentSha256": HEX, "kind": "tsconfig", "extendsResolved": []}]
    return {"schemaVersion": 1, "entryConfigPath": entry, "nodes": nodes}


def binding(ordinal, universe, entry, extents, provenance="default-unit", available=True):
    b = {
        "ordinal": ordinal,
        "provenance": provenance,
        "enumerator": {"status": "selected", "closureId": CLO},
        "nativeContextDigest": CTX,
        "universe": universe if available else None,
        "programEntry": entry,
        "extents": extents,
    }
    if not available:
        b["deficiency"] = "provider-unavailable"
        b["nativeCause"] = None
    return b


def enum_plan(memb, sc, bindings, kinds=None, cap="inventory"):
    kinds = kinds if kinds is not None else ["file", "package"]
    return {
        "schemaVersion": 1,
        "snapshotId": SNAP,
        "scopeDigest": M.raw_digest(sc),
        "membershipDigest": M.raw_digest(memb),
        "cells": [{
            "capabilityId": cap,
            "languageMode": "ts-tsconfig",
            "workspaceRoot": ".",
            "required": True,
            "kinds": kinds,
            "programBindings": bindings,
        }],
    }


def file_row(path, lang=None):
    return {
        "nativeSubjectId": path, "kind": "file", "path": path, "qualifiedName": path,
        "subjectLanguage": lang or M._suffix_language(path),
        "signatureTokens": [], "projections": [],
    }


def pkg_row(path, name):
    return {
        "nativeSubjectId": name, "kind": "package", "path": path, "qualifiedName": name,
        "subjectLanguage": M._suffix_language(path),
        "signatureTokens": [], "projections": [],
    }


def inv(kind, state, rows, examined, cell=0, prog=0, pdigest=None, extra=None):
    rec = {
        "schemaVersion": 1, "planId": PLAN_ID, "parameterDigest": pdigest or HEX,
        "cellOrdinal": cell, "programOrdinal": prog, "kind": kind, "state": state,
        "deficiency": None, "nativeCause": None,
        "examinedPaths": sorted(examined), "rows": rows,
    }
    if extra:
        rec.update(extra)
    return rec


def run_one(name, enum, inventories, memb, sc, universes, graphs, spec_obj=None, policy=None):
    pdigest = M.raw_digest(enum)
    for i in inventories:
        i["parameterDigest"] = pdigest
    result = M.admit_enumeration(
        plan=plan_obj(memb, sc),
        plan_id=PLAN_ID,
        analysis_spec=spec_obj or spec(),
        scope_descriptor=sc,
        membership=memb,
        enumeration_plan=enum,
        inventories=inventories,
        snapshot_paths=list(SNAPSHOT),
        native_contexts={CTX: {"schemaVersion": 2}},
        universes=universes,
        closures={CLO: {"kind": "provider"}},
        config_graphs=graphs,
        policy_document=policy,
    )
    return {"case": name, "result": result["result"], "refusals": result["refusals"],
            "population": result["population"], "expectedRecords": result.get("expectedRecords")}


def main():
    memb = membership()
    sc = scope()
    host = M.host_extents(memb, SNAPSHOT, sc, ".", "ts-tsconfig")
    file_ext = [{"kind": "file", "paths": host["file"]}, {"kind": "package", "paths": host["package"]}]
    graphs = {U1: graph("tsconfig.json"), U2: graph("tsconfig.build.json")}
    universes = {
        U1: {"nativeContextId": CTX, "bindResult": "ADMIT", "language": "typescript"},
        U2: {"nativeContextId": CTX, "bindResult": "ADMIT", "language": "typescript"},
    }
    b0 = binding(0, U1, None, file_ext)
    cases = []

    def add(name, enum, inventories, **kw):
        cases.append(run_one(name, enum, inventories, memb, sc, universes, graphs, **kw))

    ep = enum_plan(memb, sc, [b0])
    files = [file_row(p) for p in host["file"]]
    pkgs = [pkg_row("package.json", "app")]
    add("positive-complete-default-unit", ep, [
        inv("file", "complete", files, host["file"]),
        inv("package", "complete", pkgs, host["package"]),
    ])

    add("missing-expected-inventory", ep, [
        inv("file", "complete", files, host["file"]),
    ])

    b1 = binding(1, U2, "tsconfig.build.json", file_ext, "explicit-plan-selection")
    two = enum_plan(memb, sc, [b0, b1])
    add("two-configs-same-context-different-U", two, [
        inv("file", "complete", files, host["file"], prog=0),
        inv("package", "complete", pkgs, host["package"], prog=0),
        inv("file", "complete", files, host["file"], prog=1),
        inv("package", "complete", pkgs, host["package"], prog=1),
    ])

    dropped = [file_row(p) for p in host["file"] if p != "src/b.ts"]
    add("dropped-file-complete-refused", ep, [
        inv("file", "complete", dropped, [p for p in host["file"] if p != "src/b.ts"]),
        inv("package", "complete", pkgs, host["package"]),
    ])

    no_pkg_memb = copy.deepcopy(memb)
    no_pkg_memb["rows"] = [r for r in no_pkg_memb["rows"] if r["path"] != "package.json"]
    snap2 = [p for p in SNAPSHOT if p != "package.json"]
    host2 = M.host_extents(no_pkg_memb, snap2, sc, ".", "ts-tsconfig")
    ext2 = [{"kind": "file", "paths": host2["file"]}, {"kind": "package", "paths": host2["package"]}]
    ep2 = enum_plan(no_pkg_memb, sc, [binding(0, U1, None, ext2)])
    files2 = [file_row(p) for p in host2["file"]]
    r = M.admit_enumeration(
        plan=plan_obj(no_pkg_memb, sc), plan_id=PLAN_ID, analysis_spec=spec(),
        scope_descriptor=sc, membership=no_pkg_memb, enumeration_plan=ep2,
        inventories=[
            inv("file", "complete", files2, host2["file"], pdigest=M.raw_digest(ep2)),
            inv("package", "complete", [], host2["package"], pdigest=M.raw_digest(ep2)),
        ],
        snapshot_paths=snap2, native_contexts={CTX: {}}, universes=universes,
        closures={CLO: {"kind": "provider"}}, config_graphs=graphs,
    )
    cases.append({"case": "complete-empty-package-no-manifest", "result": r["result"], "refusals": r["refusals"],
                  "population": r["population"]})

    r = M.admit_enumeration(
        plan=plan_obj(memb, sc), plan_id=PLAN_ID, analysis_spec=spec(),
        scope_descriptor=sc, membership=memb, enumeration_plan=ep,
        inventories=[
            inv("file", "complete", files, host["file"], pdigest=M.raw_digest(ep)),
            inv("package", "complete", [], host["package"], pdigest=M.raw_digest(ep)),
        ],
        snapshot_paths=list(SNAPSHOT), native_contexts={CTX: {}}, universes=universes,
        closures={CLO: {"kind": "provider"}}, config_graphs=graphs,
    )
    cases.append({"case": "complete-package-omits-known-manifest", "result": r["result"], "refusals": r["refusals"]})

    add("partial-all-paths-known-rows", ep, [
        inv("file", "partial", files, host["file"], extra={"deficiency": "budget-exhausted", "nativeCause": None}),
        inv("package", "complete", pkgs, host["package"]),
    ])

    sym_ext = [{"kind": "symbol", "paths": host["symbol"]}]
    ep_sym = enum_plan(memb, sc, [binding(0, U1, None, sym_ext)], kinds=["symbol"], cap="syntax")
    spec_sym = {"requestedCapabilities": [
        {"capabilityId": "syntax", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": True}
    ]}
    dup = {
        "nativeSubjectId": "ts-symbol:src/a.ts#f", "kind": "symbol", "path": "src/a.ts",
        "qualifiedName": "f", "subjectLanguage": "typescript", "exported": "exported",
        "signatureTokens": ["f"],
        "projections": [
            {"closureId": CLO, "signatureTokens": ["f"]},
            {"closureId": CLO, "signatureTokens": ["f"]},
        ],
    }
    r = M.admit_enumeration(
        plan=plan_obj(memb, sc), plan_id=PLAN_ID, analysis_spec=spec_sym,
        scope_descriptor=sc, membership=memb, enumeration_plan=ep_sym,
        inventories=[inv("symbol", "complete", [dup], host["symbol"], pdigest=M.raw_digest(ep_sym))],
        snapshot_paths=list(SNAPSHOT), native_contexts={CTX: {}}, universes=universes,
        closures={CLO: {"kind": "provider"}}, config_graphs=graphs,
    )
    cases.append({"case": "duplicate-projection-closure", "result": r["result"], "refusals": r["refusals"]})

    spec_two = {"requestedCapabilities": [
        {"capabilityId": "clones-fact", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": False},
        {"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": True},
    ]}
    file_only = [{"kind": "file", "paths": host["file"]}]
    cells_two = [
        {"capabilityId": "clones-fact", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": False,
         "kinds": ["file"], "programBindings": [binding(0, U1, None, file_only)]},
        {"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": True,
         "kinds": ["file", "package"], "programBindings": [binding(0, U1, None, file_ext)]},
    ]
    ep_two = {"schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": M.raw_digest(sc),
              "membershipDigest": M.raw_digest(memb), "cells": cells_two}
    files_bad = [dict(file_row(p), qualifiedName="X"+p) if p == "src/a.ts" else file_row(p) for p in host["file"]]
    r = M.admit_enumeration(
        plan=plan_obj(memb, sc), plan_id=PLAN_ID, analysis_spec=spec_two,
        scope_descriptor=sc, membership=memb, enumeration_plan=ep_two,
        inventories=[
            inv("file", "complete", files, host["file"], cell=1, pdigest=M.raw_digest(ep_two)),
            inv("package", "complete", pkgs, host["package"], cell=1, pdigest=M.raw_digest(ep_two)),
            inv("file", "complete", files_bad, host["file"], cell=0, pdigest=M.raw_digest(ep_two)),
        ],
        snapshot_paths=list(SNAPSHOT), native_contexts={CTX: {}}, universes=universes,
        closures={CLO: {"kind": "provider"}}, config_graphs=graphs,
    )
    cases.append({"case": "contradictory-same-U-rows", "result": r["result"], "refusals": r["refusals"]})

    add("unknown-extension-inventory-unspecified", ep, [
        inv("file", "complete", files, host["file"]),
        inv("package", "complete", pkgs, host["package"]),
    ])
    xyz = [r for r in files if r["path"] == "notes.xyz"][0]
    cases[-1]["notesLanguage"] = xyz["subjectLanguage"]

    js = [r for r in files if r["path"] == "src/extra.js"][0]
    cases.append({"case": "javascript-under-TS-engine", "result": "PASS" if js["subjectLanguage"] == "javascript" else "FAIL",
                  "language": js["subjectLanguage"]})

    corrupt_u = copy.deepcopy(universes)
    corrupt_u[U1] = {"nativeContextId": "0" * 64, "bindResult": "ADMIT"}
    r = M.admit_enumeration(
        plan=plan_obj(memb, sc), plan_id=PLAN_ID, analysis_spec=spec(),
        scope_descriptor=sc, membership=memb, enumeration_plan=ep,
        inventories=[
            inv("file", "complete", files, host["file"], pdigest=M.raw_digest(ep)),
            inv("package", "complete", pkgs, host["package"], pdigest=M.raw_digest(ep)),
        ],
        snapshot_paths=list(SNAPSHOT), native_contexts={CTX: {}}, universes=corrupt_u,
        closures={CLO: {"kind": "provider"}}, config_graphs=graphs,
    )
    cases.append({"case": "corrupt-selected-binding-context", "result": r["result"], "refusals": r["refusals"]})

    policy = {"schemaFamily": "opensip.product.policy", "schemaMajor": 2, "gateSeverityAtLeast": "error",
              "rules": [{"ruleId": "r1", "enabled": False}]}
    r = M.admit_enumeration(
        plan=plan_obj(memb, sc), plan_id=PLAN_ID, analysis_spec=spec(True),
        scope_descriptor=sc, membership=memb, enumeration_plan=ep,
        inventories=[
            inv("file", "complete", files, host["file"], pdigest=M.raw_digest(ep)),
            inv("package", "complete", pkgs, host["package"], pdigest=M.raw_digest(ep)),
        ],
        snapshot_paths=list(SNAPSHOT), native_contexts={CTX: {}}, universes=universes,
        closures={CLO: {"kind": "provider"}}, config_graphs=graphs, policy_document=policy,
    )
    cases.append({"case": "disabled-policy-does-not-delete-required-cell", "result": r["result"],
                  "refusals": r["refusals"], "expectedRecords": r.get("expectedRecords")})

    want = {
        "positive-complete-default-unit": "ADMIT",
        "missing-expected-inventory": "REFUSE",
        "two-configs-same-context-different-U": "ADMIT",
        "dropped-file-complete-refused": "REFUSE",
        "complete-empty-package-no-manifest": "ADMIT",
        "complete-package-omits-known-manifest": "REFUSE",
        "partial-all-paths-known-rows": "ADMIT",
        "duplicate-projection-closure": "REFUSE",
        "contradictory-same-U-rows": "REFUSE",
        "unknown-extension-inventory-unspecified": "ADMIT",
        "javascript-under-TS-engine": "PASS",
        "corrupt-selected-binding-context": "REFUSE",
        "disabled-policy-does-not-delete-required-cell": "ADMIT",
    }
    report = {"standing": "enumeration-join checks; not full Run replay",
              "internalFaults": list(M.INTERNAL_FAULTS),
              "hostFileExtent": host["file"], "hostPackageExtent": host["package"], "hostSymbolExtent": host["symbol"],
              "cases": cases, "expected": want}
    mismatches = []
    for c in cases:
        exp = want.get(c["case"])
        if exp and c["result"] != exp:
            mismatches.append({"case": c["case"], "got": c["result"], "want": exp, "refusals": c.get("refusals")})
    report["mismatches"] = mismatches
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"mismatches": mismatches, "n": len(cases)}, indent=2))
    for c in cases:
        print(c["case"], c["result"], c.get("refusals"))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
