#!/usr/bin/env python3
"""Discriminating enumeration-join checks. Not full Run replay.

Receipt path is an explicit CLI argument. Default is a scratch directory, never a
historical grok-subject-assessment.v7–v11 review folder.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("enumeration_model_v1", HERE / "enumeration_model.v1.py")
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)

HISTORICAL_REVIEW_FOLDERS = (
    "grok-subject-assessment.v7",
    "grok-subject-assessment.v8",
    "grok-subject-assessment.v9",
    "grok-subject-assessment.v10",
    "grok-subject-assessment.v11",
)
DEFAULT_SCRATCH = Path("/tmp/opensip-enumeration-check-scratch")


def _refuse_historical(path: Path) -> None:
    parts = set(path.resolve().parts)
    for name in HISTORICAL_REVIEW_FOLDERS:
        if name in parts:
            raise SystemExit("refusing to write historical review folder: " + str(path.resolve()))


def output_paths(argv=None):
    parser = argparse.ArgumentParser(description="Enumeration-join checks; not a Run.")
    parser.add_argument("--receipt", default=None, help="Receipt JSON path. Default: scratch, not a historical review folder.")
    parser.add_argument("--hashes", default=None, help="Owned-file hashes JSON path.")
    parser.add_argument("--stdout", action="store_true", help="Print the full receipt JSON to stdout.")
    ns = parser.parse_args(argv)
    receipt = Path(ns.receipt) if ns.receipt else DEFAULT_SCRATCH / "check-receipt.json"
    hashes = Path(ns.hashes) if ns.hashes else receipt.with_name("hashes.json")
    _refuse_historical(receipt)
    _refuse_historical(hashes)
    return receipt, hashes, ns.stdout

HEX = "a" * 64
CTX = "b" * 64
U1 = "c" * 64
U2 = "d" * 64
SNAP = "snapshot2:" + "e" * 64
PLAN_ID = "plan2:" + "f" * 64
PROV = "closure2:" + "1" * 64
DET = "closure2:" + "2" * 64
TS_DOMAIN = "native.semantic-universe.typescript.v2"
RUST_DOMAIN = "native.semantic-universe.rust.v2"

SNAPSHOT = ["tsconfig.json", "tsconfig.build.json", "src/a.ts", "src/b.ts", "src/extra.js",
            "package.json", "Cargo.toml", "README.md", "notes.xyz"]

HISTORICAL_BOUNDED = (
    "positive-complete-default-unit",
    "missing-expected-inventory",
    "two-configs-same-context-different-U",
    "dropped-file-complete-refused",
    "complete-empty-package-no-name-manifests",
    "complete-package-omits-known-manifest",
    "partial-all-paths-known-rows",
    "two-symbols-same-file-same-detector",
    "duplicate-native-id-refused",
    "duplicate-projection-closure-within-row",
    "evaluation-subject-m3-identifier",
    "alternate-program-symbol-extents",
    "universe-null-complete-rows-refused",
)


def membership(paths=None):
    paths = paths or SNAPSHOT
    rows = []
    for p in paths:
        if p.endswith((".ts", ".tsx", ".js")):
            rows.append({"path": p, "languageFamily": "tsjs", "unitOrdinal": 0,
                         "membership": "program-member", "reason": "deepest-unit-in-language"})
        elif p.endswith(".xyz"):
            rows.append({"path": p, "languageFamily": "none", "unitOrdinal": None,
                         "membership": "unsupported-file", "reason": "no-bundled-grammar"})
        else:
            rows.append({"path": p, "languageFamily": "none", "unitOrdinal": None,
                         "membership": "syntax-only", "reason": "grammar-only"})
    # native section 1.4 U-4b (consumer24 M3): rows strictly ascending by UTF-8 path and the projections in row
    # order. Enumeration admission now enforces this on every membership, so the fixture states it.
    rows.sort(key=lambda r: r["path"].encode("utf-8"))
    return {
        "schemaVersion": 1,
        "units": [{
            "unitOrdinal": 0, "rootPath": "", "languageFamily": "tsjs", "languageMode": "ts-tsconfig",
            "unitKind": "ts-program", "markerPath": "tsconfig.json", "markerSha256": "1" * 64,
            "recognizerId": "typescript-config", "recognizerVersion": 1, "provenance": "DISCOVERED",
            "memberPackageRoots": [],
        }],
        "rows": rows, "unsupportedFiles": [r["path"] for r in rows if r["membership"] == "unsupported-file"],
        "outsideBoundaryFiles": [], "erasedFiles": [],
    }


def scope(excluded=None, roots=None):
    return {"schemaVersion": 2, "workspaceRoots": roots or ["."], "pathPrefixes": [],
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


def blobs(pkg_json=b'{"name":"app"}', cargo=b'[package]\nname="rs-app"\n', extra=None):
    out = {"package.json": pkg_json, "Cargo.toml": cargo}
    if extra:
        out.update(extra)
    return out


def binding(ordinal, universe, entry, extents, provenance="default-unit", candidate_source_paths=None):
    rec = {
        "ordinal": ordinal, "provenance": provenance,
        "enumerator": {"status": "selected", "closureId": PROV},
        "nativeContextDigest": CTX, "universe": universe, "programEntry": entry, "extents": extents,
    }
    if candidate_source_paths is not None:
        rec["candidateSourcePaths"] = M.canon_str_list(candidate_source_paths)
    return rec


def unavail_binding(ordinal, extents, enumerator=None):
    return {
        "ordinal": ordinal, "provenance": "default-unit",
        "enumerator": enumerator or {"status": "selected", "closureId": PROV},
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


def sort_files(rows):
    return sorted(rows, key=lambda r: r["nativeSubjectId"].encode("utf-8"))


def sort_pkgs(rows):
    return sorted(rows, key=lambda r: (r["nativeSubjectId"].encode("utf-8"), r["path"].encode("utf-8")))


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
        if type(i) is dict:
            i["parameterDigest"] = pdigest
    domains = kw.pop("universe_domains", {U1: TS_DOMAIN, U2: TS_DOMAIN})
    return M.admit_enumeration(
        plan=plan_obj(sc), plan_id=PLAN_ID, analysis_spec=spec_obj or spec(),
        scope_descriptor=sc, membership=memb, enumeration_plan=enum, inventories=inventories,
        native_contexts={CTX: {"languageMode": "ts-tsconfig"}}, universes=universes,
        closures={PROV: {"kind": "provider"}, DET: {"kind": "detector"}},
        snapshot_paths=kw.pop("snapshot_paths", list(SNAPSHOT)), source_blobs=source,
        retained_inputs=retained, policy_document=policy, universe_domains=domains, **kw,
    )


def owned_hashes():
    names = [
        "enumeration-plan.schema.v1.json",
        "subject-inventory.schema.v1.json",
        "enumeration-contract.v1.md",
        "enumeration_model.v1.py",
        "check-enumeration.v1.py",
    ]
    rows = []
    for name in names:
        raw = (HERE / name).read_bytes()
        rows.append({"path": str(HERE / name), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    return rows


def main(argv=None):
    OUT, HASHES, to_stdout = output_paths(argv)
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
    files = sort_files([file_row(p) for p in file_ext])
    pkgs = sort_pkgs([pkg_row(n["path"], n["packageName"]) for n in pkg_proj["named"]])
    cases = []

    def rec(name, result):
        cases.append({"case": name, "result": result["result"], "refusals": result["refusals"],
                      "population": result.get("population"),
                      "subjectKeys": sorted(result.get("subjects") or {})})

    rec("positive-complete-default-unit", admit(ep, [
        inv("file", "complete", files, file_ext),
        inv("package", "complete", pkgs, pkg_ext),
    ], memb, sc, universes, retained, source))

    # Internal root representation is admitted before path slicing / program binding.
    # Keep a valid enumeration baseline, change only the host membership root spelling,
    # and rebind its digest so a digest mismatch cannot mask the root-specific refusal.
    # This exercises the enumeration boundary, not structural custody or a whole Run.
    unit_root_cases = []
    for label, root, members, expected, diagnostic in [
        ("project-empty", "", [], "ADMIT", None),
        ("project-dot", ".", [], "REFUSE", "units[0].rootPath:#/$defs/InternalUnitRootV1"),
        ("project-dot-slash", "./", [], "REFUSE", "units[0].rootPath:#/$defs/InternalUnitRootV1"),
        ("member-dot", "", ["."], "REFUSE", "units[0].memberPackageRoots[0]:#/$defs/CanonicalRelativeDirV1"),
        ("member-empty", "", [""], "REFUSE", "units[0].memberPackageRoots[0]:#/$defs/CanonicalRelativeDirV1"),
    ]:
        changed_membership = copy.deepcopy(memb)
        changed_membership["units"][0].update(rootPath=root, memberPackageRoots=members)
        changed_plan = copy.deepcopy(ep)
        changed_plan["membershipDigest"] = M.raw_digest(changed_membership)
        native_refusal = None
        try:
            M.NV.admit_unit_roots(changed_membership["units"])
            native_result = "ADMIT"
        except M.NV.AdmissionError as exc:
            native_result = "REFUSE"
            native_refusal = str(exc)
        result = admit(changed_plan, [
            inv("file", "complete", copy.deepcopy(files), file_ext),
            inv("package", "complete", copy.deepcopy(pkgs), pkg_ext),
        ], changed_membership, sc, universes, retained, source)
        exact_faults = [] if expected == "ADMIT" else ["ENUMERATION_MEMBERSHIP_UNIT_ROOT"]
        passed = (native_result == expected and result["result"] == expected
                  and result["refusals"] == exact_faults
                  and (native_refusal is None if diagnostic is None else
                       native_refusal.startswith("NATIVE_UNIT_ROOT_REPRESENTATION:" + diagnostic + ":")))
        unit_root_cases.append({"case": label, "expected": expected,
                               "nativeResult": native_result, "nativeRefusal": native_refusal,
                               "enumerationResult": result["result"], "refusals": result["refusals"],
                               "passed": passed})

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
    ext_nn = [{"kind": "file", "paths": file_ext}, {"kind": "package", "paths": proj_nn["candidatePaths"]}]
    ep_nn = copy.deepcopy(ep)
    ep_nn["cells"][0]["programBindings"] = [binding(0, U1, None, ext_nn)]
    rec("complete-empty-package-no-name-manifests", admit(ep_nn, [
        inv("file", "complete", files, file_ext),
        inv("package", "complete", [], proj_nn["candidatePaths"]),
    ], memb, sc, universes, retained, src_noname))

    rec("complete-package-omits-known-manifest", admit(ep, [
        inv("file", "complete", files, file_ext),
        inv("package", "complete", [], pkg_ext),
    ], memb, sc, universes, retained, source))

    rec("partial-all-paths-known-rows", admit(ep, [
        inv("file", "partial", files, file_ext, extra={"deficiency": "budget-exhausted", "nativeCause": None}),
        inv("package", "complete", pkgs, pkg_ext),
    ], memb, sc, universes, retained, source))

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
        "subjects": {},
    })

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
        "refusals": [], "subjects": {},
    })
    rec("unknown-extension-unspecified", {
        "result": "ADMIT" if M._suffix_language("notes.xyz") == "unspecified" else "REFUSE",
        "refusals": [], "subjects": {},
    })

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

    bad_json = blobs(pkg_json=b'{"name":', cargo=b'[package]\nname="rs-app"\n')
    proj_bad = M.project_named_packages(SNAPSHOT, sc, ".", memb, bad_json, [])
    cand_bad = proj_bad["candidatePaths"]
    good_pkgs = sort_pkgs([pkg_row(n["path"], n["packageName"]) for n in proj_bad["named"]])
    rec("package-parse-error-partial-keeps-named", admit(
        {"schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": M.raw_digest(sc),
         "membershipDigest": M.raw_digest(memb),
         "cells": [{"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
                    "required": True, "kinds": M._cap_kinds("inventory"),
                    "programBindings": [binding(0, U1, None, [
                        {"kind": "file", "paths": file_ext},
                        {"kind": "package", "paths": cand_bad}])]}]},
        [inv("file", "complete", files, file_ext),
         inv("package", "partial", good_pkgs, cand_bad,
             extra={"deficiency": "source-syntax-invalid", "nativeCause": None})],
        memb, sc, universes, retained, bad_json,
    ))

    all_bad = blobs(pkg_json=b'{"name":', cargo=b'package = "not-a-table"\n')
    proj_all = M.project_named_packages(SNAPSHOT, sc, ".", memb, all_bad, [])
    rec("all-bad-package-partial-zero-rows", admit(
        {"schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": M.raw_digest(sc),
         "membershipDigest": M.raw_digest(memb),
         "cells": [{"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
                    "required": True, "kinds": M._cap_kinds("inventory"),
                    "programBindings": [binding(0, U1, None, [
                        {"kind": "file", "paths": file_ext},
                        {"kind": "package", "paths": proj_all["candidatePaths"]}])]}]},
        [inv("file", "complete", files, file_ext),
         inv("package", "partial", [], proj_all["candidatePaths"],
             extra={"deficiency": "source-syntax-invalid", "nativeCause": None})],
        memb, sc, universes, retained, all_bad,
    ))

    FOO_SNAP = ["tsconfig.json", "src/a.ts", "package.json", "other/package.json"]
    foo_memb = membership(FOO_SNAP)
    foo_source = blobs(pkg_json=b'{"name":"foo"}', extra={"other/package.json": b'{"name":"foo"}'})
    foo_file_ext = M.host_file_extent(foo_memb, FOO_SNAP, sc, ".", [])
    foo_proj = M.project_named_packages(FOO_SNAP, sc, ".", foo_memb, foo_source, [])
    foo_pkg_ext = foo_proj["candidatePaths"]
    foo_files = sort_files([file_row(p) for p in foo_file_ext])
    foo_pkgs = sort_pkgs([pkg_row(n["path"], n["packageName"]) for n in foo_proj["named"]])
    foo_u = uni("ts-tsconfig", ["src/a.ts"])
    foo_ep = {"schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": M.raw_digest(sc),
              "membershipDigest": M.raw_digest(foo_memb),
              "cells": [{"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
                         "required": True, "kinds": M._cap_kinds("inventory"),
                         "programBindings": [binding(0, U1, None, [
                             {"kind": "file", "paths": foo_file_ext},
                             {"kind": "package", "paths": foo_pkg_ext}])]}]}
    foo_result = admit(foo_ep, [
        inv("file", "complete", foo_files, foo_file_ext),
        inv("package", "complete", foo_pkgs, foo_pkg_ext),
    ], foo_memb, sc, {U1: foo_u, U2: u2}, {U1: {"configGraph": graph("tsconfig.json")}}, foo_source,
        snapshot_paths=FOO_SNAP)
    rec("two-manifests-same-name-foo", foo_result)
    foo_subjects = [v for v in (foo_result.get("subjects") or {}).values() if v.get("kind") == "package"]
    ids = [s.get("evaluationSubject") for s in foo_subjects]
    paths = [s.get("packageManifestPath") for s in foo_subjects]
    rec("two-foo-distinct-subject3", {
        "result": "ADMIT" if (
            foo_result.get("result") == "ADMIT" and len(ids) == 2 and len(set(ids)) == 2
            and len(set(paths)) == 2 and all(i.startswith("subject3:") for i in ids)
        ) else "REFUSE",
        "refusals": [] if len(set(ids)) == 2 else ["same-fingerprint-or-count"],
        "population": {"ids": ids, "paths": paths},
        "subjects": {},
    })

    rec("universe-domain-mismatch-rust-on-ts-cell", admit(ep, [
        inv("file", "complete", files, file_ext),
        inv("package", "complete", pkgs, pkg_ext),
    ], memb, sc, universes, retained, source, universe_domains={U1: RUST_DOMAIN, U2: TS_DOMAIN}))

    rec("non-object-inventory-schema", admit(ep, [
        None,
        inv("file", "complete", files, file_ext),
        inv("package", "complete", pkgs, pkg_ext),
    ], memb, sc, universes, retained, source))

    rec("toml-malformed-package-table-classification", {
        "result": "ADMIT" if (
            any(f["path"] == "Cargo.toml" and f["reason"] == "classification" for f in proj_all["parseFailed"])
            and not any(n["path"] == "Cargo.toml" for n in proj_all["named"])
        ) else "REFUSE",
        "refusals": [], "subjects": {},
    })

    dup_json = blobs(pkg_json=b'{"name":"a","name":"b"}', cargo=b'[package]\nname="rs-app"\n')
    proj_dup = M.project_named_packages(SNAPSHOT, sc, ".", memb, dup_json, [])
    rec("json-duplicate-key-syntax-invalid", {
        "result": "ADMIT" if any(f["path"] == "package.json" and f["reason"] == "syntax" for f in proj_dup["parseFailed"]) else "REFUSE",
        "refusals": [], "subjects": {},
    })

    rec("package-parse-partial-drops-named-refused", admit(
        {"schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": M.raw_digest(sc),
         "membershipDigest": M.raw_digest(memb),
         "cells": [{"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
                    "required": True, "kinds": M._cap_kinds("inventory"),
                    "programBindings": [binding(0, U1, None, [
                        {"kind": "file", "paths": file_ext},
                        {"kind": "package", "paths": cand_bad}])]}]},
        [inv("file", "complete", files, file_ext),
         inv("package", "partial", [], cand_bad,
             extra={"deficiency": "source-syntax-invalid", "nativeCause": None})],
        memb, sc, universes, retained, bad_json,
    ))

    rec("unavailable-binding-matching-extents", admit(
        {"schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": M.raw_digest(sc),
         "membershipDigest": M.raw_digest(memb),
         "cells": [{"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
                    "required": True, "kinds": M._cap_kinds("inventory"),
                    "programBindings": [unavail_binding(0, inv_ext)]}]},
        [inv("file", "unavailable", [], [], extra={"deficiency": "provider-unavailable", "nativeCause": None}),
         inv("package", "unavailable", [], [], extra={"deficiency": "provider-unavailable", "nativeCause": None})],
        memb, sc, universes, retained, source,
    ))

    rec("unavailable-binding-wrong-extents", admit(
        {"schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": M.raw_digest(sc),
         "membershipDigest": M.raw_digest(memb),
         "cells": [{"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
                    "required": True, "kinds": M._cap_kinds("inventory"),
                    "programBindings": [unavail_binding(0, [
                        {"kind": "file", "paths": ["src/a.ts"]},
                        {"kind": "package", "paths": []}])]}]},
        [inv("file", "unavailable", [], [], extra={"deficiency": "provider-unavailable", "nativeCause": None}),
         inv("package", "unavailable", [], [], extra={"deficiency": "provider-unavailable", "nativeCause": None})],
        memb, sc, universes, retained, source,
    ))

    rec("membership-snapshot-coverage-gap", admit(ep, [
        inv("file", "complete", files, file_ext),
        inv("package", "complete", pkgs, pkg_ext),
    ], memb, sc, universes, retained, source, snapshot_paths=list(SNAPSHOT) + ["ghost/file.ts"]))

    dummy_bytes = {p: b"x" for p in SNAPSHOT}
    dummy_bytes["package.json"] = b'{"name":"app"}'
    dummy_bytes["Cargo.toml"] = b'[package]\nname="rs-app"\n'
    full_inv = [{"path": p, "sha256": hashlib.sha256(dummy_bytes[p]).hexdigest(),
                 "bytes": len(dummy_bytes[p])} for p in SNAPSHOT]
    mismatched = dict(dummy_bytes)
    mismatched["package.json"] = b'{"name":"app"} '
    rec("source-bytes-mismatch-full-inventory", admit(ep, [
        inv("file", "complete", files, file_ext),
        inv("package", "complete", pkgs, pkg_ext),
    ], memb, sc, universes, retained, mismatched,
        snapshot_inventory=full_inv, snapshot_paths=list(SNAPSHOT)))

    rec("invalid-boundaries-native-admission-error", admit(ep, [
        inv("file", "complete", files, file_ext),
        inv("package", "complete", pkgs, pkg_ext),
    ], memb, sc, universes, retained, source, membership_derivation={
        "markers": {"tsconfig.json": {"sha256": "1" * 64}},
        "files": list(SNAPSHOT),
        "mode": "operational",
        "boundaries": {"schemaVersion": 1.5},
    }))

    # native section 1.4 U-4b.2: a nested Cargo workspace below a workspace unit is a folded member, never a fold
    # target. The derivation witness re-runs discover_units inside the typed admission handler, so looking the
    # folded manifest up as a unit (StopIteration) escaped admission instead of being decided.
    nested_markers = {"Cargo.toml": {"sha256": "1" * 64, "isCargoWorkspace": True},
                      "nested/Cargo.toml": {"sha256": "2" * 64, "isCargoWorkspace": True},
                      "nested/pkg/Cargo.toml": {"sha256": "3" * 64, "isCargoWorkspace": False},
                      "tsconfig.json": {"sha256": "1" * 64}}
    rec("nested-cargo-workspace-derivation-differs-refused", admit(ep, [
        inv("file", "complete", files, file_ext),
        inv("package", "complete", pkgs, pkg_ext),
    ], memb, sc, universes, retained, source, membership_derivation={
        "markers": nested_markers, "files": list(SNAPSHOT), "mode": "standalone-fixture"}))
    nested_paths = list(SNAPSHOT) + ["nested/Cargo.toml", "nested/pkg/Cargo.toml", "nested/pkg/src/lib.rs"]
    nested_units = M.NV.discover_units(nested_markers)["units"]
    nested_rust_units = [[u["rootPath"], u["unitKind"], u["memberPackageRoots"]] for u in nested_units if u["languageFamily"] == "rust"]
    nested_memb = M.NV.assign_membership(nested_units, nested_paths)
    nested_file_ext = M.host_file_extent(nested_memb, nested_paths, sc, ".", [])
    nested_source = blobs(cargo=b'[workspace]\nmembers=["nested/pkg"]\n', extra={
        "nested/Cargo.toml": b'[workspace]\nmembers=["pkg"]\n', "nested/pkg/Cargo.toml": b'[package]\nname="nested-pkg"\n'})
    nested_pkg_proj = M.project_named_packages(nested_paths, sc, ".", nested_memb, nested_source, [])
    nested_ep = copy.deepcopy(ep)
    nested_ep["membershipDigest"] = M.raw_digest(nested_memb)
    nested_ep["cells"][0]["programBindings"] = [binding(0, U1, None, [
        {"kind": "file", "paths": nested_file_ext}, {"kind": "package", "paths": nested_pkg_proj["namedPaths"]}])]
    rec("nested-cargo-workspace-derivation-folds-into-surviving-unit", admit(nested_ep, [
        inv("file", "complete", sort_files([file_row(p) for p in nested_file_ext]), nested_file_ext),
        inv("package", "complete", sort_pkgs([pkg_row(n["path"], n["packageName"]) for n in nested_pkg_proj["named"]]),
            nested_pkg_proj["namedPaths"]),
    ], nested_memb, sc, universes, retained, nested_source, snapshot_paths=nested_paths, membership_derivation={
        "markers": nested_markers, "files": nested_paths, "mode": "standalone-fixture"}))

    rec("native-admission-error-class-distinct", {
        "result": "ADMIT" if M.AdmissionError is not M.NV.AdmissionError else "REFUSE",
        "refusals": [], "subjects": {},
    })

    unsel = {"status": "unselected", "reason": "optional-unselected"}
    opt_spec = spec([{"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": False}])
    opt_ep = {"schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": M.raw_digest(sc),
              "membershipDigest": M.raw_digest(memb),
              "cells": [{"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
                         "required": False, "kinds": M._cap_kinds("inventory"),
                         "programBindings": [unavail_binding(0, inv_ext, unsel)]}]}
    rec("optional-unselected-unavailable-admitted", admit(opt_ep, [
        inv("file", "unavailable", [], [], extra={"deficiency": "provider-unavailable", "nativeCause": None}),
        inv("package", "unavailable", [], [], extra={"deficiency": "provider-unavailable", "nativeCause": None}),
    ], memb, sc, universes, retained, source, spec_obj=opt_spec))

    req_ep = copy.deepcopy(opt_ep)
    req_ep["cells"][0]["required"] = True
    rec("required-unselected-refused", admit(req_ep, [
        inv("file", "unavailable", [], [], extra={"deficiency": "provider-unavailable", "nativeCause": None}),
        inv("package", "unavailable", [], [], extra={"deficiency": "provider-unavailable", "nativeCause": None}),
    ], memb, sc, universes, retained, source))

    avail_unsel = copy.deepcopy(ep)
    avail_unsel["cells"][0]["programBindings"][0] = dict(b0, enumerator=unsel)
    rec("available-unselected-refused", admit(avail_unsel, [
        inv("file", "complete", files, file_ext),
        inv("package", "complete", pkgs, pkg_ext),
    ], memb, sc, universes, retained, source))

    missing_ptr = copy.deepcopy(opt_ep)
    missing_ptr["cells"][0]["programBindings"] = [unavail_binding(0, inv_ext, {"status": "selected"})]
    rec("selected-missing-closure-structural", admit(missing_ptr, [
        inv("file", "unavailable", [], [], extra={"deficiency": "provider-unavailable", "nativeCause": None}),
        inv("package", "unavailable", [], [], extra={"deficiency": "provider-unavailable", "nativeCause": None}),
    ], memb, sc, universes, retained, source, spec_obj=opt_spec))

    rec("optional-unselected-wrong-extents", admit(
        {"schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": M.raw_digest(sc),
         "membershipDigest": M.raw_digest(memb),
         "cells": [{"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
                    "required": False, "kinds": M._cap_kinds("inventory"),
                    "programBindings": [unavail_binding(0, [
                        {"kind": "file", "paths": ["src/a.ts"]},
                        {"kind": "package", "paths": []}], unsel)]}]},
        [inv("file", "unavailable", [], [], extra={"deficiency": "provider-unavailable", "nativeCause": None}),
         inv("package", "unavailable", [], [], extra={"deficiency": "provider-unavailable", "nativeCause": None})],
        memb, sc, universes, retained, source, spec_obj=opt_spec,
    ))

    near_spec = spec([{"capabilityId": "clones-near", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": True}])
    near_missing = {"schemaVersion": 1, "snapshotId": SNAP, "scopeDigest": M.raw_digest(sc),
                    "membershipDigest": M.raw_digest(memb),
                    "cells": [{"capabilityId": "clones-near", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
                               "required": True, "kinds": [],
                               "programBindings": [binding(0, U1, None, [])]}]}
    rec("clones-near-missing-candidate-source-paths", admit(near_missing, [], memb, sc, universes, retained, source, spec_obj=near_spec))
    near_ok = copy.deepcopy(near_missing)
    near_ok["cells"][0]["programBindings"] = [binding(0, U1, None, [], candidate_source_paths=["src/a.ts"])]
    rec("clones-near-plan-rooted-source-paths", admit(near_ok, [], memb, sc, universes, retained, source, spec_obj=near_spec))
    near_two = copy.deepcopy(near_missing)
    near_two["cells"][0]["programBindings"] = [
        binding(0, U1, None, [], candidate_source_paths=["src/a.ts"]),
        binding(1, U2, "tsconfig.build.json", [], "explicit-plan-selection", candidate_source_paths=["src/b.ts"]),
    ]
    rec("clones-near-two-programs-disjoint-extents", admit(near_two, [], memb, sc, universes, retained, source, spec_obj=near_spec))
    near_outside = copy.deepcopy(near_ok)
    near_outside["cells"][0]["programBindings"] = [binding(0, U1, None, [], candidate_source_paths=["not-in-snapshot.ts"])]
    rec("clones-near-source-paths-outside-snapshot", admit(near_outside, [], memb, sc, universes, retained, source, spec_obj=near_spec))
    inv_extra = copy.deepcopy(ep)
    inv_extra["cells"][0]["programBindings"] = [binding(0, U1, None, inv_ext, candidate_source_paths=["src/a.ts"])]
    rec("inventory-cell-rejects-candidate-source-paths", admit(inv_extra, [
        inv("file", "complete", files, file_ext),
        inv("package", "complete", pkgs, pkg_ext),
    ], memb, sc, universes, retained, source))

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
        "universe-null-complete-rows-refused": "REFUSE",
        "available-binding-unavailable-inventory": "ADMIT",
        "corrupt-selected-binding-context": "REFUSE",
        "disabled-policy-does-not-delete-required-cell": "ADMIT",
        "javascript-under-TS-engine": "ADMIT",
        "unknown-extension-unspecified": "ADMIT",
        "exclude-dot-excludes-all": "ADMIT",
        "package-parse-error-partial-keeps-named": "ADMIT",
        "all-bad-package-partial-zero-rows": "ADMIT",
        "two-manifests-same-name-foo": "ADMIT",
        "two-foo-distinct-subject3": "ADMIT",
        "universe-domain-mismatch-rust-on-ts-cell": "REFUSE",
        "non-object-inventory-schema": "REFUSE",
        "toml-malformed-package-table-classification": "ADMIT",
        "json-duplicate-key-syntax-invalid": "ADMIT",
        "package-parse-partial-drops-named-refused": "REFUSE",
        "unavailable-binding-matching-extents": "ADMIT",
        "unavailable-binding-wrong-extents": "REFUSE",
        "membership-snapshot-coverage-gap": "REFUSE",
        "source-bytes-mismatch-full-inventory": "REFUSE",
        "invalid-boundaries-native-admission-error": "REFUSE",
        "native-admission-error-class-distinct": "ADMIT",
        "optional-unselected-unavailable-admitted": "ADMIT",
        "required-unselected-refused": "REFUSE",
        "available-unselected-refused": "REFUSE",
        "selected-missing-closure-structural": "REFUSE",
        "optional-unselected-wrong-extents": "REFUSE",
        "clones-near-missing-candidate-source-paths": "REFUSE",
        "clones-near-plan-rooted-source-paths": "ADMIT",
        "clones-near-two-programs-disjoint-extents": "ADMIT",
        "clones-near-source-paths-outside-snapshot": "REFUSE",
        "inventory-cell-rejects-candidate-source-paths": "REFUSE",
        "nested-cargo-workspace-derivation-differs-refused": "REFUSE",
        "nested-cargo-workspace-derivation-folds-into-surviving-unit": "ADMIT",
    }
    mismatches = []
    for c in cases:
        exp = want.get(c["case"])
        if exp and c["result"] != exp:
            mismatches.append({"case": c["case"], "got": c["result"], "want": exp, "refusals": c.get("refusals")})
    mismatches.extend({"case": "internal-root-" + row["case"], "observed": row}
                      for row in unit_root_cases if not row["passed"])
    nested_refusals = next(c["refusals"] for c in cases if c["case"] == "nested-cargo-workspace-derivation-differs-refused")
    if (nested_refusals != ["ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION"]
            or nested_rust_units != [["", "cargo-workspace", ["nested", "nested/pkg"]]]):
        mismatches.append({"case": "nested-cargo-workspace-derivation", "refusals": nested_refusals, "rustUnits": nested_rust_units})
    historical = [c["case"] for c in cases if c["case"] in HISTORICAL_BOUNDED]
    hashes = owned_hashes()
    report = {
        "standing": "enumeration-join checks; not full Run. Historical v7–v11 receipts are preserved and are not this checker's default output. Default receipt is scratch; this run's path is explicit --receipt.",
        "v8ReceiptMisplaced": "/tmp/opensip-design-corrections/grok-subject-assessment.v7/check-receipt.json",
        "historicalBounded": list(HISTORICAL_BOUNDED),
        "historicalBoundedCount": "%d/20" % len(HISTORICAL_BOUNDED),
        "v10ReceiptPreserved": "/tmp/opensip-design-corrections/grok-subject-assessment.v10/check-receipt.json",
        "nativeAdmissionErrorDistinct": M.AdmissionError is not M.NV.AdmissionError,
        "internalFaults": list(M.INTERNAL_FAULTS),
        "fileExtent": file_ext, "packageNamed": pkg_proj["named"], "symbolDefaultRoots": roots,
        "packageCandidateOneBad": proj_bad,
        "twoFooIds": ids, "twoFooPaths": paths,
        "internalUnitRootControls": unit_root_cases,
        "cases": cases, "expected": want, "mismatches": mismatches,
        "ownedHashes": hashes,
    }
    report["receiptPath"] = str(OUT)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    HASHES.write_text(json.dumps(hashes, indent=2) + "\n")
    summary = {"n": len(cases), "historicalBounded": "%d/20" % len(historical),
               "mismatches": mismatches, "receiptPath": str(OUT)}
    if to_stdout:
        print(json.dumps(report, indent=2))
    else:
        print(json.dumps(summary, indent=2))
        for c in cases:
            print(c["case"], c["result"], c.get("refusals"))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
