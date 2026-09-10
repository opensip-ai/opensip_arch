#!/usr/bin/env python3
"""Discriminating enumeration-join checks. Not full Run replay. Receipt -> v9."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("enumeration_model_v1", HERE / "enumeration_model.v1.py")
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)
OUT = Path("/tmp/opensip-design-corrections/grok-subject-assessment.v9/check-receipt.json")

HEX = "a" * 64
CTX = "b" * 64
U1 = "c" * 64
U2 = "d" * 64
SNAP = "snapshot2:" + "e" * 64
PLAN_ID = "plan2:" + "f" * 64
PROV = "closure2:" + "1" * 64
DET = "closure2:" + "2" * 64

SNAPSHOT = ["tsconfig.json", "tsconfig.build.json", "src/a.ts", "src/b.ts", "src/extra.js",
            "package.json", "Cargo.toml", "README.md", "notes.xyz"]


def membership():
    rows = []
    for p in SNAPSHOT:
        if p.endswith((".ts", ".tsx", ".js")):
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
        "rows": rows, "unsupportedFiles": ["notes.xyz"], "outsideBoundaryFiles": [], "erasedFiles": [],
    }


def scope(excluded=None):
    return {"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": [],
            "excludedPathPrefixes": excluded or []}


def plan_obj(sc):
    return {
        "snapshotId": SNAP, "scopeDigest": M.raw_digest(sc),
        "nativeContextDigests": [CTX], "semanticClosures": [PROV, DET],
        "analysisSpecDigest": HEX, "policyDigest": HEX,
    }


def spec(caps=None):
    return {"requestedCapabilities": caps or [
        {"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": True}
    ]}


def graph(entry):
    nodes = [] if entry is None else [{"path": entry, "contentSha256": HEX, "kind": "tsconfig", "extendsResolved": []}]
    return {"schemaVersion": 1, "entryConfigPath": entry, "nodes": nodes}


def uni(mode, roots):
    return {"nativeContextId": CTX, "languageMode": mode, "programRootFiles": list(roots)}


def blobs(pkg_json=b'{"name":"app"}', cargo=b'[package]\nname="rs-app"\n'):
    return {"package.json": pkg_json, "Cargo.toml": cargo}


def binding(ordinal, universe, entry, extents, provenance="default-unit"):
    return {
        "ordinal": ordinal, "provenance": provenance,
        "enumerator": {"status": "selected", "closureId": PROV},
        "nativeContextDigest": CTX, "universe": universe, "programEntry": entry, "extents": extents,
    }


def unavail_binding(ordinal, extents):
    return {
        "ordinal": ordinal, "provenance": "default-unit",
        "enumerator": {"status": "selected", "closureId": PROV},
        "nativeContextDigest": CTX, "universe": None, "programEntry": None, "extents": extents,
        "deficiency": "provider-unavailable", "nativeCause": None,
    }


def file_row(path):
    return {"nativeSubjectId": path, "kind": "file", "path": path, "qualifiedName": path,
            "subjectLanguage": M._suffix_language(path), "signatureTokens": [], "projections": []}


def pkg_row(path, name):
    return {"nativeSubjectId": name, "kind": "package", "path": path, "qualifiedName": name,
            "subjectLanguage": M._suffix_language(path), "signatureTokens": [], "projections": []}


def sym_row(sid, path, tokens=None):
    return {
        "nativeSubjectId": sid, "kind": "symbol", "path": path, "qualifiedName": sid.split("#")[-1],
        "subjectLanguage": M._suffix_language(path), "exported": "exported",
        "signatureTokens": tokens or [sid],
        "projections": [{"closureId": DET, "signatureTokens": tokens or [sid]}],
    }


def inv(kind, state, rows, examined, cell=0, prog=0, extra=None):
    rec = {
        "schemaVersion": 1, "planId": PLAN_ID, "parameterDigest": HEX,
        "cellOrdinal": cell, "programOrdinal": prog, "kind": kind, "state": state,
        "deficiency": None, "nativeCause": None,
        "examinedPaths": M.canon_str_list(examined), "rows": rows,
    }
    if extra:
        rec.update(extra)
    return rec


def admit(enum, inventories, memb, sc, universes, retained, source, spec_obj=None, policy=None, **kw):
    pdigest = M.raw_digest(enum)
    for i in inventories:
        i["parameterDigest"] = pdigest
    return M.admit_enumeration(
        plan=plan_obj(sc), plan_id=PLAN_ID, analysis_spec=spec_obj or spec(),
        scope_descriptor=sc, membership=memb, enumeration_plan=enum, inventories=inventories,
        native_contexts={CTX: {"languageMode": "ts-tsconfig"}}, universes=universes,
        closures={PROV: {"kind": "provider"}, DET: {"kind": "detector"}},
        snapshot_paths=list(SNAPSHOT), source_blobs=source, retained_inputs=retained,
        policy_document=policy, **kw,
    )


def main():
    memb = membership()
    sc = scope()
    faults = []
    file_ext = M.host_file_extent(memb, SNAPSHOT, sc, ".", faults)
    roots = ["src/a.ts", "src/b.ts", "src/extra.js"]
    u1 = uni("ts-tsconfig", roots)
    u2 = uni("ts-tsconfig", ["src/b.ts"])
    universes = {U1: u1, U2: u2}
    retained = {U1: {"configGraph": graph("tsconfig.json")}, U2: {"configGraph": graph("tsconfig.build.json")}}
    source = blobs()
    pkg_proj = M.project_named_packages(SNAPSHOT, sc, ".", memb, source, [])
    pkg_ext = pkg_proj["namedPaths"]
    inv_ext = [{"kind": "file", "paths": file_ext}, {"kind": "package", "paths": pkg_ext}]
    b0 = binding(0, U1, None, inv_ext)
    ep = {"schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": M.raw_digest(sc),
          "membershipDigest": M.raw_digest(memb),
          "cells": [{"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
                     "required": True, "kinds": M._cap_kinds("inventory"), "programBindings": [b0]}]}
    files = sorted([file_row(p) for p in file_ext], key=lambda r: r["nativeSubjectId"].encode("utf-8"))
    pkgs = sorted([pkg_row(n["path"], n["packageName"]) for n in pkg_proj["named"]],
                  key=lambda r: r["nativeSubjectId"].encode("utf-8"))
    cases = []

    def rec(name, result):
        cases.append({"case": name, "result": result["result"], "refusals": result["refusals"],
                      "population": result.get("population")})

    rec("positive-complete-default-unit", admit(ep, [
        inv("file", "complete", files, file_ext),
        inv("package", "complete", pkgs, pkg_ext),
    ], memb, sc, universes, retained, source))

    rec("missing-expected-inventory", admit(ep, [inv("file", "complete", files, file_ext)], memb, sc, universes, retained, source))

    b1 = binding(1, U2, "tsconfig.build.json", inv_ext, "explicit-plan-selection")
    ep2 = copy.deepcopy(ep)
    ep2["cells"][0]["programBindings"] = [b0, b1]
    rec("two-configs-same-context-different-U", admit(ep2, [
        inv("file", "complete", files, file_ext, prog=0),
        inv("package", "complete", pkgs, pkg_ext, prog=0),
        inv("file", "complete", files, file_ext, prog=1),
        inv("package", "complete", pkgs, pkg_ext, prog=1),
    ], memb, sc, universes, retained, source))

    dropped = [file_row(p) for p in file_ext if p != "src/b.ts"]
    rec("dropped-file-complete-refused", admit(ep, [
        inv("file", "complete", dropped, [p for p in file_ext if p != "src/b.ts"]),
        inv("package", "complete", pkgs, pkg_ext),
    ], memb, sc, universes, retained, source))

    src_noname = blobs(pkg_json=b'{}', cargo=b'[workspace]\nmembers=["x"]\n')
    proj_nn = M.project_named_packages(SNAPSHOT, sc, ".", memb, src_noname, [])
    ext_nn = [{"kind": "file", "paths": file_ext}, {"kind": "package", "paths": proj_nn["namedPaths"]}]
    ep_nn = copy.deepcopy(ep)
    ep_nn["cells"][0]["programBindings"] = [binding(0, U1, None, ext_nn)]
    rec("complete-empty-package-no-name-manifests", admit(ep_nn, [
        inv("file", "complete", files, file_ext),
        inv("package", "complete", [], proj_nn["namedPaths"]),
    ], memb, sc, universes, retained, src_noname))

    rec("complete-package-omits-known-manifest", admit(ep, [
        inv("file", "complete", files, file_ext),
        inv("package", "complete", [], pkg_ext),
    ], memb, sc, universes, retained, source))

    rec("partial-all-paths-known-rows", admit(ep, [
        inv("file", "partial", files, file_ext, extra={"deficiency": "budget-exhausted", "nativeCause": None}),
        inv("package", "complete", pkgs, pkg_ext),
    ], memb, sc, universes, retained, source))

    # syntax cell: two symbols same file, same detector
    sym_paths = M.host_symbol_extent(memb, SNAPSHOT, sc, ".", "ts-tsconfig", u1, retained[U1], [])
    sym_ext = [{"kind": "symbol", "paths": sym_paths}]
    ep_sym = {"schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": M.raw_digest(sc),
              "membershipDigest": M.raw_digest(memb),
              "cells": [{"capabilityId": "syntax", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
                         "required": True, "kinds": M._cap_kinds("syntax"),
                         "programBindings": [binding(0, U1, None, sym_ext)]}]}
    spec_sym = spec([{"capabilityId": "syntax", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": True}])
    two_fn = [
        sym_row("ts-symbol:src/a.ts#f", "src/a.ts", ["f"]),
        sym_row("ts-symbol:src/a.ts#g", "src/a.ts", ["g"]),
    ]
    rec("two-symbols-same-file-same-detector", admit(ep_sym, [
        inv("symbol", "complete", two_fn, sym_paths),
    ], memb, sc, universes, retained, source, spec_obj=spec_sym))

    dup_id = [sym_row("ts-symbol:src/a.ts#f", "src/a.ts"), sym_row("ts-symbol:src/a.ts#f", "src/b.ts")]
    rec("duplicate-native-id-refused", admit(ep_sym, [
        inv("symbol", "complete", dup_id, sym_paths),
    ], memb, sc, universes, retained, source, spec_obj=spec_sym))

    dup_proj = sym_row("ts-symbol:src/a.ts#f", "src/a.ts")
    dup_proj["projections"] = [
        {"closureId": DET, "signatureTokens": ["f"]},
        {"closureId": DET, "signatureTokens": ["f2"]},
    ]
    rec("duplicate-projection-closure-within-row", admit(ep_sym, [
        inv("symbol", "complete", [dup_proj], sym_paths),
    ], memb, sc, universes, retained, source, spec_obj=spec_sym))

    ident = M.evaluation_subject_id(U1, "file", "src/a.ts")
    rec("evaluation-subject-m3-identifier", {
        "result": "ADMIT" if ident.startswith("subject3:") else "REFUSE",
        "refusals": [] if ident.startswith("subject3:") else ["bad-prefix"],
        "population": {"id": ident},
    })

    # different programRootFiles => different symbol extents
    u1a = uni("ts-tsconfig", ["src/a.ts"])
    u2b = uni("ts-tsconfig", ["src/b.ts"])
    ext_a = [{"kind": "symbol", "paths": ["src/a.ts"]}]
    ext_b = [{"kind": "symbol", "paths": ["src/b.ts"]}]
    ep_alt = {"schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": M.raw_digest(sc),
              "membershipDigest": M.raw_digest(memb),
              "cells": [{"capabilityId": "syntax", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
                         "required": True, "kinds": ["symbol"], "programBindings": [
                             binding(0, U1, None, ext_a),
                             binding(1, U2, "tsconfig.build.json", ext_b, "explicit-plan-selection"),
                         ]}]}
    rec("alternate-program-symbol-extents", admit(ep_alt, [
        inv("symbol", "complete", [sym_row("ts-symbol:src/a.ts#f", "src/a.ts")], ["src/a.ts"], prog=0),
        inv("symbol", "complete", [sym_row("ts-symbol:src/b.ts#h", "src/b.ts")], ["src/b.ts"], prog=1),
    ], memb, sc, {U1: u1a, U2: u2b}, retained, source, spec_obj=spec_sym))

    sc_ex = scope(["."])
    rec("exclude-dot-excludes-all", admit(
        {"schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": M.raw_digest(sc_ex),
         "membershipDigest": M.raw_digest(memb),
         "cells": [{"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
                    "required": True, "kinds": M._cap_kinds("inventory"),
                    "programBindings": [binding(0, U1, None, [
                        {"kind": "file", "paths": []}, {"kind": "package", "paths": []}])]}]},
        [inv("file", "complete", [], []), inv("package", "complete", [], [])],
        memb, sc_ex, universes, retained, source,
    ))

    rec("universe-null-complete-rows-refused", admit(
        {"schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": M.raw_digest(sc),
         "membershipDigest": M.raw_digest(memb),
         "cells": [{"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
                    "required": True, "kinds": M._cap_kinds("inventory"),
                    "programBindings": [unavail_binding(0, inv_ext)]}]},
        [inv("file", "complete", files, file_ext), inv("package", "complete", pkgs, pkg_ext)],
        memb, sc, universes, retained, source,
    ))

    rec("available-binding-unavailable-inventory", admit(ep, [
        inv("file", "unavailable", [], [], extra={"deficiency": "provider-unavailable", "nativeCause": None}),
        inv("package", "complete", pkgs, pkg_ext),
    ], memb, sc, universes, retained, source))

    bad_json = blobs(pkg_json=b'{"name":', cargo=b'[package]\nname="rs-app"\n')
    proj_bad = M.project_named_packages(SNAPSHOT, sc, ".", memb, bad_json, [])
    rec("package-parse-error-unavailable", admit(
        {"schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": M.raw_digest(sc),
         "membershipDigest": M.raw_digest(memb),
         "cells": [{"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
                    "required": True, "kinds": M._cap_kinds("inventory"),
                    "programBindings": [binding(0, U1, None, [
                        {"kind": "file", "paths": file_ext},
                        {"kind": "package", "paths": proj_bad["namedPaths"]}])]}]},
        [inv("file", "complete", files, file_ext),
         inv("package", "unavailable", [], [], extra={"deficiency": "provider-unavailable", "nativeCause": None})],
        memb, sc, universes, retained, bad_json,
    ))

    rec("corrupt-selected-binding-context", admit(ep, [
        inv("file", "complete", files, file_ext),
        inv("package", "complete", pkgs, pkg_ext),
    ], memb, sc, {U1: {"nativeContextId": "0" * 64, "languageMode": "ts-tsconfig", "programRootFiles": roots},
                  U2: u2}, retained, source))

    rec("disabled-policy-does-not-delete-required-cell", admit(ep, [
        inv("file", "complete", files, file_ext),
        inv("package", "complete", pkgs, pkg_ext),
    ], memb, sc, universes, retained, source, policy={"schemaFamily": "opensip.product.policy", "schemaMajor": 2,
                                                     "gateSeverityAtLeast": "error",
                                                     "rules": [{"ruleId": "r1", "enabled": False}]}))

    rec("javascript-under-TS-engine", {
        "result": "ADMIT" if M._suffix_language("src/extra.js") == "javascript" else "REFUSE",
        "refusals": [],
    })
    rec("unknown-extension-unspecified", {
        "result": "ADMIT" if M._suffix_language("notes.xyz") == "unspecified" else "REFUSE",
        "refusals": [],
    })

    want = {
        "positive-complete-default-unit": "ADMIT",
        "missing-expected-inventory": "REFUSE",
        "two-configs-same-context-different-U": "ADMIT",
        "dropped-file-complete-refused": "REFUSE",
        "complete-empty-package-no-name-manifests": "ADMIT",
        "complete-package-omits-known-manifest": "REFUSE",
        "partial-all-paths-known-rows": "ADMIT",
        "two-symbols-same-file-same-detector": "ADMIT",
        "duplicate-native-id-refused": "REFUSE",
        "duplicate-projection-closure-within-row": "REFUSE",
        "evaluation-subject-m3-identifier": "ADMIT",
        "alternate-program-symbol-extents": "ADMIT",
        "exclude-dot-excludes-all": "REFUSE",
        "universe-null-complete-rows-refused": "REFUSE",
        "available-binding-unavailable-inventory": "ADMIT",
        "package-parse-error-unavailable": "ADMIT",
        "corrupt-selected-binding-context": "REFUSE",
        "disabled-policy-does-not-delete-required-cell": "ADMIT",
        "javascript-under-TS-engine": "ADMIT",
        "unknown-extension-unspecified": "ADMIT",
    }
    mismatches = []
    for c in cases:
        exp = want.get(c["case"])
        if exp and c["result"] != exp:
            mismatches.append({"case": c["case"], "got": c["result"], "want": exp, "refusals": c.get("refusals")})
    report = {
        "standing": "enumeration-join checks; not full Run. v8 receipt was written into v7; this receipt is v9.",
        "v8ReceiptMisplaced": "/tmp/opensip-design-corrections/grok-subject-assessment.v7/check-receipt.json",
        "internalFaults": list(M.INTERNAL_FAULTS),
        "fileExtent": file_ext, "packageNamed": pkg_proj["named"], "symbolDefaultRoots": roots,
        "cases": cases, "expected": want, "mismatches": mismatches,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"n": len(cases), "mismatches": mismatches}, indent=2))
    for c in cases:
        print(c["case"], c["result"], c.get("refusals"))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
