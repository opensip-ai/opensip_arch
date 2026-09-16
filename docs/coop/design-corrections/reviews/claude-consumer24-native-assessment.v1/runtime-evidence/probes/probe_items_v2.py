"""Second probe pass (probe_items.py attempt 1 is retained; its receipts stay). Corrects two probe defects and adds one join.

Attempt-1 defects corrected here:
  * M2: validating a policy fragment with the bare document failed on an unresolved cross-document $ref
    (urn:opensip:product-v1:workflows:common), which is a probe error, not an owner verdict. This pass uses
    the workflows owner's own pinned local-registry validator `workflows_model.validate_import_record`.
  * S3: `default_capability_selection([], registry)` refused on registry ROW ORDER (canonical-set), a probe
    error. This pass sorts the registry by canonical bytes. The attempt-1 syntax-only unit used a
    languageFamily outside the enum; this pass uses the published `none` / `syntax-only` spelling.
Added:
  * M1: the enumeration owner's own `host_file_extent` for a tsjs cell, showing which paths a clones-fact
    (kinds [file]) cell must account for.
Usage: probe_items_v2.py ROOT. Reads the frozen snapshot only; stdout only.
"""
import copy
import hashlib
import importlib.util
import json
import sys
import traceback
from pathlib import Path

ROOT = Path(sys.argv[1])
DC = ROOT / "docs/coop/design-corrections"
F = DC / "foundation"
TAG = "p2_" + ROOT.name.replace("candidate-subject.", "")
OUT = {"root": str(ROOT), "sections": {}}


def load(name, path):
    name = f"{TAG}_{name}"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def section(name):
    def wrap(fn):
        try:
            OUT["sections"][name] = {"result": fn()}
        except Exception as exc:
            OUT["sections"][name] = {"error": type(exc).__name__ + ": " + str(exc)[:600], "traceback": traceback.format_exc()[-2500:]}
        return fn
    return wrap


def attempt(fn):
    try:
        return {"outcome": "ADMIT", "value": fn()}
    except Exception as exc:
        cause = exc.__cause__
        return {"outcome": "REFUSE", "error": type(exc).__name__ + ": " + str(exc).split("\n")[0][:300],
                "cause": (type(cause).__name__ + ": " + str(cause).split("\n")[0][:300]) if cause else None}


INPUTS = ["docs/coop/design-corrections/workflows/workflows_model.v1.py",
          "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json",
          "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json",
          "docs/coop/design-corrections/native/native_evidence_model.v2.py",
          "docs/coop/design-corrections/foundation/enumeration_model.v1.py",
          "docs/coop/design-corrections/foundation/check-semantic-replay.v3.py",
          "docs/coop/design-corrections/native/native-capability-matrix.v2.json"]
OUT["inputSha256"] = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in INPUTS}

SR = load("semantic_replay", F / "check-semantic-replay.v3.py")
C = SR.M.C
W = load("workflows_model", DC / "workflows/workflows_model.v1.py")
N = load("native_model", DC / "native/native_evidence_model.v2.py")
EM = load("enumeration_model", F / "enumeration_model.v1.py")
MATRIX = json.loads((DC / "native/native-capability-matrix.v2.json").read_text())


@section("M2-node-against-each-Predicate-selector")
def m2():
    atoms = {"endpoint-source (v2 program atom, as in the admitted Run)": dict(SR.REFS_EXISTS_SRC),
             "same atom without endpoint": {k: v for k, v in SR.REFS_EXISTS_SRC.items() if k != "endpoint"},
             "endpoint-target (incoming atom)": dict(SR.REFS_NONE_TGT)}
    rows = {}
    for label, atom in atoms.items():
        rows[label] = {doc: attempt(lambda d=doc, a=atom: W.validate_import_record(f"workflows/schemas/{d}", "#/$defs/Predicate", a) or "valid")
                       for doc in ("policy-document.schema.json", "policy-document.v2.schema.json")}
    return {"standing": "schema, via the workflows owner's pinned local-registry validator", "rows": rows}


@section("S3-default-selection-and-syntax-only-unit")
def s3():
    registry = []
    for cap in MATRIX["capabilities"]:
        modes = sorted((c["mode"] for c in MATRIX["cells"] if c["capability"] == cap["id"] and c["state"] != "NOT-SELECTED"),
                       key=str.encode)
        if modes:
            registry.append({"capabilityId": cap["id"], "languageModes": modes})
    registry.sort(key=C.canonical)
    no_units = attempt(lambda: N.default_capability_selection([], registry))
    unit = {"unitOrdinal": 0, "rootPath": "", "languageFamily": "none", "languageMode": "syntax-only",
            "unitKind": "syntax-only", "markerPath": "", "markerSha256": "0" * 64, "recognizerId": "syntax-only",
            "recognizerVersion": 1, "provenance": "DEFAULTED", "memberPackageRoots": []}
    representable = attempt(lambda: N.validate_native("WorkspaceUnitV2", unit) or "valid")
    with_unit = attempt(lambda: N.default_capability_selection([unit], registry)) if representable["outcome"] == "ADMIT" else None

    def rows_of(result):
        if not result or result["outcome"] != "ADMIT":
            return result
        value = result["value"]
        text = json.dumps(value)
        return {"outcome": "ADMIT", "capabilityRows": text.count('"capabilityId"'), "keys": sorted(value) if isinstance(value, dict) else None}
    source = (DC / "native/native_evidence_model.v2.py").read_text()
    return {"standing": "helper + schema",
            "registryRows": len(registry),
            "defaultSelectionNoUnits": rows_of(no_units),
            "syntaxOnlyUnitSchemaRepresentable": representable,
            "defaultSelectionWithHandBuiltSyntaxOnlyUnit": rows_of(with_unit),
            "discoverUnitsEverEmitsSyntaxOnlyUnitKind": '"unitKind": "syntax-only"' in source or "'unitKind': 'syntax-only'" in source}


@section("M1-enumeration-file-extent-for-tsjs-cell")
def m1():
    markers = {"tsconfig.json": {"sha256": "a" * 64}, "package.json": {"sha256": "b" * 64}}
    files = ["tsconfig.json", "package.json", "src/a.ts", "src/b.ts", "README.md", "assets/logo.svg", "LICENSE",
             "node_modules/dep/index.js"]
    units = N.discover_units(markers)["units"]
    membership = N.assign_membership(units, files)
    scope = N.unit_scope_descriptor(units, [], pruned_trees=N.discover_units(markers)["prunedTrees"])["scopeDescriptor"]
    faults = []
    extent = EM.host_file_extent(membership, files, scope, ".", faults)
    return {"standing": "helper (enumeration owner extent derivation)",
            "units": [(u["rootPath"], u["languageMode"]) for u in units], "scope": scope,
            "clonesFactKinds": EM._cap_kinds("clones-fact"), "fileExtentForCellRootDot": extent, "faults": faults}


print(json.dumps(OUT, indent=1, default=str))
