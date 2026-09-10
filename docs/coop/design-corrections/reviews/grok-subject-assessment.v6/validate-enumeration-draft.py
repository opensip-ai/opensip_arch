#!/usr/bin/env python3
"""Shape validation for isolated EnumerationPlanV1 / SubjectInventoryV1 drafts.

Not Run admission, not native extraction, not frozen21 mutation.
Uses ExactValidator (const/enum/order) from the successor tree copy of canonical.py.
"""
import hashlib
import json
import sys
from pathlib import Path

PY = sys.executable
ROOT = Path("/tmp/opensip-design-corrections/evaluator-successor.v1/docs/coop/design-corrections/foundation")
sys.path.insert(0, str(ROOT))
from canonical import AdmissionError, ExactValidator, canonical, parse, typed  # noqa: E402

PLAN_PATH = ROOT / "enumeration-plan.schema.v1.json"
INV_PATH = ROOT / "subject-inventory.schema.v1.json"
OUT = Path("/tmp/opensip-design-corrections/grok-subject-assessment.v6/validation-report.json")

HEX = "a" * 64
CTX = "b" * 64
UNI = "c" * 64
SNAP = "snapshot2:" + "d" * 64
PLAN = "plan2:" + "e" * 64
CLO = "closure2:" + "f" * 64


def load(path):
    return json.loads(path.read_text())


def digest_of(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def check(schema, instance):
    typed(instance)
    ExactValidator(schema).validate(instance)
    raw = canonical(instance)
    if len(raw) > 4 * 1024 * 1024:
        raise AdmissionError("BYTE_LIMIT")
    return raw


def should_fail(schema, instance, name):
    try:
        check(schema, instance)
    except Exception as exc:
        return {"case": name, "result": "REFUSED", "error": str(exc)[:300]}
    return {"case": name, "result": "UNEXPECTED_PASS"}


def extent(kind, paths):
    return {"kind": kind, "paths": sorted(paths)}


def available_binding(ordinal=0, kinds_ext=None, provenance="default-unit", entry=None):
    if kinds_ext is None:
        kinds_ext = [extent("file", ["src/a.ts"]), extent("package", ["package.json"])]
    return {
        "ordinal": ordinal,
        "provenance": provenance,
        "enumerator": {"status": "selected", "closureId": CLO},
        "nativeContextDigest": CTX,
        "universe": UNI,
        "programEntry": entry,
        "extents": kinds_ext,
    }


def unavailable_binding(ordinal=0, selected=True):
    en = {"status": "selected", "closureId": CLO} if selected else {
        "status": "unselected", "reason": "optional-unselected"
    }
    return {
        "ordinal": ordinal,
        "provenance": "default-unit",
        "enumerator": en,
        "nativeContextDigest": None,
        "universe": None,
        "programEntry": None,
        "extents": [extent("file", ["README.md"])],
        "deficiency": "provider-unavailable",
        "nativeCause": None,
    }


def cell(cap, mode, root, required, kinds, bindings):
    return {
        "capabilityId": cap,
        "languageMode": mode,
        "workspaceRoot": root,
        "required": required,
        "kinds": sorted(kinds),
        "programBindings": bindings,
    }


def plan(cells):
    return {
        "schemaVersion": 1,
        "snapshotId": SNAP,
        "scopeDigest": HEX,
        "membershipDigest": HEX,
        "cells": cells,
    }


def inventory(kind, state, rows, examined, extra=None):
    rec = {
        "schemaVersion": 1,
        "planId": PLAN,
        "parameterDigest": HEX,
        "cellOrdinal": 0,
        "programOrdinal": 0,
        "kind": kind,
        "state": state,
        "deficiency": None,
        "nativeCause": None,
        "examinedPaths": sorted(examined),
        "rows": rows,
    }
    if extra:
        rec.update(extra)
    return rec


def file_row(path):
    return {
        "nativeSubjectId": path,
        "kind": "file",
        "path": path,
        "qualifiedName": path,
        "subjectLanguage": "typescript",
        "signatureTokens": [],
        "projections": [],
    }


def symbol_row(sid, path, projections=None):
    return {
        "nativeSubjectId": sid,
        "kind": "symbol",
        "path": path,
        "qualifiedName": "f",
        "subjectLanguage": "javascript",
        "exported": "unknown",
        "signatureTokens": ["f"],
        "projections": projections if projections is not None else [],
    }


def main():
    plan_schema = load(PLAN_PATH)
    inv_schema = load(INV_PATH)
    cases = []

    def ok(name, schema, inst):
        raw = check(schema, inst)
        cases.append({"case": name, "result": "PASS", "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})

    p1 = plan([cell("inventory", "ts-tsconfig", ".", True, ["file", "package"], [available_binding()])])
    ok("plan-default-unit-dot-root", plan_schema, p1)
    param_digest = digest_of(p1)

    p2 = plan([
        cell("inventory", "ts-tsconfig", ".", True, ["file", "package"], [available_binding()]),
        cell("syntax", "ts-tsconfig", ".", False, ["symbol"], [available_binding(
            kinds_ext=[extent("symbol", ["src/a.ts"])]
        )]),
    ])
    ok("plan-two-cells-sorted", plan_schema, p2)

    extra = available_binding(1, [extent("file", ["src/b.ts"])], "explicit-plan-selection", "tsconfig.build.json")
    p3 = plan([cell("inventory", "js-allowjs", "packages/web", True, ["file", "package"], [
        available_binding(0, [extent("file", ["packages/web/a.js"]), extent("package", ["packages/web/package.json"])]),
        extra,
    ])])
    ok("plan-two-program-bindings", plan_schema, p3)

    ok("plan-unavailable-optional-unselected", plan_schema, plan([
        cell("syntax", "syntax-only", ".", False, ["symbol"], [unavailable_binding(selected=False)])
    ]))

    unsorted = plan([
        cell("syntax", "ts-tsconfig", ".", False, ["symbol"], [available_binding(kinds_ext=[extent("symbol", ["src/a.ts"])])]),
        cell("inventory", "ts-tsconfig", ".", True, ["file", "package"], [available_binding()]),
    ])
    cases.append(should_fail(plan_schema, unsorted, "plan-cells-unsorted-refused"))

    overflow_bindings = [available_binding(i, [extent("file", ["src/a.ts"])], "explicit-plan-selection" if i else "default-unit") for i in range(129)]
    overflow = plan([cell("inventory", "ts-tsconfig", ".", True, ["file"], overflow_bindings)])
    cases.append(should_fail(plan_schema, overflow, "plan-129-bindings-refused"))

    required_unselected = plan([
        cell("inventory", "ts-tsconfig", ".", True, ["file"], [unavailable_binding(selected=False)])
    ])
    cases.append(should_fail(plan_schema, required_unselected, "plan-required-unselected-enumerator-refused"))

    inv_complete = inventory("file", "complete", [file_row("src/a.ts")], ["src/a.ts"])
    inv_complete["parameterDigest"] = param_digest
    ok("inventory-complete-file", inv_schema, inv_complete)

    ok("inventory-complete-empty-symbol", inv_schema, inventory("symbol", "complete", [], []))

    pkg = inventory("package", "complete", [{
        "nativeSubjectId": "app",
        "kind": "package",
        "path": "package.json",
        "qualifiedName": "app",
        "subjectLanguage": "json",
        "signatureTokens": [],
        "projections": [],
    }], ["package.json"])
    ok("inventory-package-json-language", inv_schema, pkg)

    partial = inventory("symbol", "partial", [symbol_row("ts-symbol:src/a.ts#f", "src/a.ts", [{
        "closureId": CLO,
        "signatureTokens": ["f", "(i32)"],
    }])], ["src/a.ts", "src/b.ts"])
    ok("inventory-partial-known-row-with-projection", inv_schema, partial)

    unav = inventory("symbol", "unavailable", [], [], extra={"deficiency": "provider-unavailable", "nativeCause": None})
    ok("inventory-unavailable-empty", inv_schema, unav)

    bad_tokens = inventory("file", "complete", [dict(file_row("src/a.ts"), signatureTokens=["nope"])], ["src/a.ts"])
    cases.append(should_fail(inv_schema, bad_tokens, "file-nonempty-signature-refused"))

    bad_pkg_lang = inventory("package", "complete", [{
        "nativeSubjectId": "app",
        "kind": "package",
        "path": "package.json",
        "qualifiedName": "app",
        "subjectLanguage": "javascript",
        "signatureTokens": [],
        "projections": [],
    }], ["package.json"])
    cases.append(should_fail(inv_schema, bad_pkg_lang, "package-ecosystem-language-refused"))

    missing_def = inventory("symbol", "unavailable", [], [])
    cases.append(should_fail(inv_schema, missing_def, "unavailable-null-deficiency-refused"))

    report = {
        "standing": "Shape validation of isolated draft schemas. Not Run admission.",
        "python": PY,
        "planSchema": str(PLAN_PATH),
        "inventorySchema": str(INV_PATH),
        "planSchemaSha256": hashlib.sha256(PLAN_PATH.read_bytes()).hexdigest(),
        "inventorySchemaSha256": hashlib.sha256(INV_PATH.read_bytes()).hexdigest(),
        "contractSha256": hashlib.sha256((ROOT / "enumeration-contract.v1.md").read_bytes()).hexdigest(),
        "cases": cases,
        "passCount": sum(1 for c in cases if c["result"] == "PASS"),
        "refuseCount": sum(1 for c in cases if c["result"] == "REFUSED"),
        "unexpectedPass": [c["case"] for c in cases if c["result"] == "UNEXPECTED_PASS"],
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("passCount", "refuseCount", "unexpectedPass", "planSchemaSha256", "inventorySchemaSha256", "contractSha256")}, indent=2))
    for c in cases:
        print(c["case"], c["result"])
    if report["unexpectedPass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
