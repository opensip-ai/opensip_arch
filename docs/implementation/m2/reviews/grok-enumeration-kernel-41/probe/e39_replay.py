#!/usr/bin/env python3
"""Independent E39 replay of kernel-check cases plus discriminating mutations.

Does not mutate the selected overlay. Requires CPython 3.12 with
-I -B -X int_max_str_digits=0.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
import traceback
from pathlib import Path

PROBE = Path(__file__).resolve().parent
CASES = PROBE / "cases.json"
OVERLAY = Path(
    "/tmp/opensip-implementation/m2-enumeration-join-trial-41/reference/"
    "archroot/docs/coop/design-corrections/foundation/enumeration_model.v1.py"
)
OUT = PROBE / "e39_replay.json"
MUTATIONS = PROBE / "mutations.json"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def hex_blobs(src: dict) -> dict:
    out = {}
    for path, value in (src or {}).items():
        if not isinstance(value, str):
            raise TypeError(f"source_blobs[{path!r}] is {type(value).__name__}")
        out[path] = bytes.fromhex(value)
    return out


def call_e39(model, inp: dict):
    kwargs = {
        "plan": inp["plan"],
        "plan_id": inp["plan_id"],
        "analysis_spec": inp["analysis_spec"],
        "scope_descriptor": inp["scope_descriptor"],
        "membership": inp["membership"],
        "enumeration_plan": inp["enumeration_plan"],
        "inventories": inp["inventories"],
        "native_contexts": inp["native_contexts"],
        "universes": inp["universes"],
        "closures": inp["closures"],
        "universe_domains": inp["universe_domains"],
        "snapshot_inventory": inp.get("snapshot_inventory"),
        "snapshot_paths": inp.get("snapshot_paths"),
        "source_blobs": hex_blobs(inp.get("source_blobs") or {}),
        "retained_inputs": inp.get("retained_inputs"),
        "membership_derivation": inp.get("membership_derivation"),
        "policy_document": inp.get("policy_document"),
    }
    return model.admit_enumeration(**kwargs)


def outcome(model, inp: dict) -> dict:
    try:
        result = call_e39(model, inp)
        return {"ok": True, "result": result}
    except Exception as exc:
        return {
            "ok": False,
            "errorType": type(exc).__name__,
            "error": str(exc),
            "trace": traceback.format_exc(limit=8),
        }


def mutate_base(base: dict, path, value):
    out = copy.deepcopy(base)
    cur = out
    for key in path[:-1]:
        cur = cur[key]
    cur[path[-1]] = value
    return out


def build_mutations(base: dict) -> list[dict]:
    file_inv = base["inventories"][0]
    pkg_inv = base["inventories"][1]
    cell = base["enumeration_plan"]["cells"][0]
    binding = cell["programBindings"][0]
    mutations = []

    def add(name, inp, note):
        mutations.append({"id": name, "note": note, "input": inp})

    # Error order: PLAN_SCHEMA aborts before UNIT_ROOT.
    p = copy.deepcopy(base)
    p["enumeration_plan"]["schemaVersion"] = 99
    p["membership"]["units"][0]["rootPath"] = "."
    add("plan-schema-and-unit-root", p, "PLAN_SCHEMA early abort must hide UNIT_ROOT")

    # Error order: UNIT_ROOT aborts before inventory totality.
    p = copy.deepcopy(base)
    p["membership"]["units"][0]["rootPath"] = "."
    p["inventories"][0]["examinedPaths"] = list(file_inv["examinedPaths"][:-1])
    add("unit-root-and-file-totality", p, "UNIT_ROOT early abort must hide FILE_TOTALITY")

    # Normalization: complete examinedPaths permutation of the same set.
    p = copy.deepcopy(base)
    exam = list(file_inv["examinedPaths"])
    p["inventories"][0]["examinedPaths"] = list(reversed(exam))
    add("examined-paths-reversed", p, "complete examinedPaths is sequence-equal, not set-equal")

    # Duplicate nativeSubjectId on file rows (first-seen vs uniqueness).
    p = copy.deepcopy(base)
    rows = copy.deepcopy(file_inv["rows"])
    rows[1] = copy.deepcopy(rows[0])
    rows[1]["path"] = rows[0]["path"]
    p["inventories"][0]["rows"] = rows
    add("duplicate-file-native-id", p, "duplicate file nativeSubjectId/path")

    # Duplicate universe within one cell.
    p = copy.deepcopy(base)
    extra = copy.deepcopy(binding)
    extra["ordinal"] = 1
    extra["provenance"] = "explicit-plan-selection"
    extra["programEntry"] = "tsconfig.json"
    p["enumeration_plan"]["cells"][0]["programBindings"] = [copy.deepcopy(binding), extra]
    add("duplicate-universe-same-cell", p, "same universe H on two bindings of one cell")

    # Default-unit ordinal not 0.
    p = copy.deepcopy(base)
    p["enumeration_plan"]["cells"][0]["programBindings"][0]["ordinal"] = 1
    add("default-unit-ordinal-1", p, "single default-unit binding with ordinal 1")

    # Kind map order vs canonical unique sort.
    p = copy.deepcopy(base)
    p["enumeration_plan"]["cells"][0]["kinds"] = ["package", "file"]
    add("kinds-swapped-order", p, "cell kinds order vs registry [file, package]")

    # Malformed: inventories not a list.
    p = copy.deepcopy(base)
    p["inventories"] = {"0": file_inv, "1": pkg_inv}
    add("inventories-not-list", p, "E39 ADMISSION_PRECONDITION; kernel JoinInputs is always Vec")

    # Malformed: inventory element not a dict.
    p = copy.deepcopy(base)
    p["inventories"] = ["not-an-inventory", pkg_inv]
    add("inventory-not-dict", p, "non-object inventory element")

    # Malformed: snapshot_inventory not a list, with UNIT_ROOT.
    p = copy.deepcopy(base)
    p["snapshot_inventory"] = {"path": "Cargo.toml"}
    p["membership"]["units"][0]["rootPath"] = "."
    add(
        "malformed-snapshot-inventory-and-unit-root",
        p,
        "E39 may collect PRECONDITION then UNIT_ROOT; complete_join ignores unused snapshot_inventory field",
    )

    # Duplicate snapshot_inventory paths.
    p = copy.deepcopy(base)
    row = {
        "path": "Cargo.toml",
        "sha256": "00" * 32,
        "bytes": 1,
    }
    p["snapshot_inventory"] = [row, dict(row)]
    add("duplicate-snapshot-inventory-path", p, "E39 PRECONDITION; map complete_join does not re-walk inventory rows")

    # bindResult on universe (join-time, not reader).
    p = copy.deepcopy(base)
    uni = next(iter(p["universes"]))
    p["universes"][uni]["bindResult"] = True
    add("universe-bindresult", p, "bindResult must be ADMISSION_PRECONDITION")

    # universe_domains not a dict.
    p = copy.deepcopy(base)
    p["universe_domains"] = ["native.semantic-universe.typescript.v2"]
    add("universe-domains-not-dict", p, "E39 early ADMISSION_PRECONDITION")

    # Type: string ordinal on inventory after schema.
    p = copy.deepcopy(base)
    p["inventories"][0]["cellOrdinal"] = "0"
    add("string-cell-ordinal", p, "typed schema vs Law on locator")

    # File vs package totality: drop one complete file row path, keep examined.
    p = copy.deepcopy(base)
    p["inventories"][0]["rows"] = list(file_inv["rows"][:-1])
    add("complete-file-rows-missing-one", p, "FILE_TOTALITY on complete row set vs extent")

    # Package totality: drop examined path but keep rows.
    p = copy.deepcopy(base)
    p["inventories"][1]["examinedPaths"] = list(pkg_inv["examinedPaths"][:-1])
    add("complete-package-examined-short", p, "PACKAGE_TOTALITY on complete examined vs extent")

    # Unexpected extra inventory record.
    p = copy.deepcopy(base)
    extra_inv = copy.deepcopy(file_inv)
    extra_inv["cellOrdinal"] = 9
    extra_inv["programOrdinal"] = 9
    p["inventories"] = [file_inv, pkg_inv, extra_inv]
    add("unexpected-inventory-record", p, "cell/program not in plan")

    # Wrong parameterDigest.
    p = copy.deepcopy(base)
    p["inventories"][0]["parameterDigest"] = "00" * 32
    add("wrong-parameter-digest", p, "ORDINAL_UNBOUND")

    # Missing enumerator status.
    p = copy.deepcopy(base)
    p["enumeration_plan"]["cells"][0]["programBindings"][0]["enumerator"] = {}
    add("empty-enumerator", p, "REQUIRED_UNSELECTED_ENUMERATOR")

    # Program bindings overflow.
    p = copy.deepcopy(base)
    bindings = []
    for i in range(129):
        b = copy.deepcopy(binding)
        b["ordinal"] = i
        if i:
            b["provenance"] = "explicit-plan-selection"
            b["universe"] = None
            b["deficiency"] = "source-syntax-invalid"
            b["nativeCause"] = None
            b["extents"] = copy.deepcopy(binding["extents"])
        bindings.append(b)
    p["enumeration_plan"]["cells"][0]["programBindings"] = bindings
    add("program-bindings-overflow", p, "129 bindings -> OVERFLOW plus follow-on faults")

    # Duplicate identical cells (cells.index vs enumerate).
    p = copy.deepcopy(base)
    cell0 = copy.deepcopy(p["enumeration_plan"]["cells"][0])
    p["enumeration_plan"]["cells"] = [cell0, copy.deepcopy(cell0)]
    p["analysis_spec"]["requestedCapabilities"] = [
        copy.deepcopy(p["analysis_spec"]["requestedCapabilities"][0]),
        copy.deepcopy(p["analysis_spec"]["requestedCapabilities"][0]),
    ]
    add("duplicate-identical-cells", p, "E39 cells.index vs rust enumerate cellOrdinal")

    # Reconcile: second payload extra key for same population key.
    p = copy.deepcopy(base)
    extra_inv = copy.deepcopy(file_inv)
    extra_inv["kind"] = "file"
    # cannot easily add a second inventory for same locator; mutate a row payload clone via duplicate binding
    rows = copy.deepcopy(file_inv["rows"])
    rows[0] = dict(rows[0])
    rows[0]["signatureTokens"] = ["mutated"]
    # same native id different payload in same inventory is still one row; need two inventories
    # Use clones: add second binding with same universe so same population key two payloads.
    extra_b = copy.deepcopy(binding)
    extra_b["ordinal"] = 1
    extra_b["provenance"] = "explicit-plan-selection"
    extra_b["programEntry"] = "tsconfig.json"
    extra_b["universe"] = "d" * 64
    p["enumeration_plan"]["cells"][0]["programBindings"] = [copy.deepcopy(binding), extra_b]
    inv2 = copy.deepcopy(file_inv)
    inv2["programOrdinal"] = 1
    inv2["rows"] = rows
    p["inventories"] = [copy.deepcopy(file_inv), copy.deepcopy(pkg_inv), inv2]
    add("reconcile-divergent-payload", p, "same file id two payloads; second universe is different so may not reconcile — keep as control")

    # Language mismatch on file row.
    p = copy.deepcopy(base)
    rows = copy.deepcopy(file_inv["rows"])
    for r in rows:
        if r["path"].endswith(".ts"):
            r["subjectLanguage"] = "markdown"
            break
    p["inventories"][0]["rows"] = rows
    add("file-language-mismatch", p, "LANGUAGE")

    # File name mismatch.
    p = copy.deepcopy(base)
    rows = copy.deepcopy(file_inv["rows"])
    rows[0]["qualifiedName"] = "other"
    p["inventories"][0]["rows"] = rows
    add("file-name-mismatch", p, "FILE_NAME")

    # Membership derivation witness (kernel API does not accept this).
    p = copy.deepcopy(base)
    p["membership_derivation"] = {"mode": "standalone-fixture"}
    add("membership-derivation-incomplete", p, "E39 PRECONDITION on derivation keys; kernel inspect API never takes derivation")

    # Candidate paths on inventory capability (must be null).
    p = copy.deepcopy(base)
    p["enumeration_plan"]["cells"][0]["programBindings"][0]["candidateSourcePaths"] = ["src/a.ts"]
    add("candidate-paths-on-inventory-cap", p, "CANDIDATE_SOURCE_PATHS")

    # Schema-failed inventory whose locator still matches: suppress MISSING_RECORD.
    p = copy.deepcopy(base)
    bad = copy.deepcopy(file_inv)
    bad["schemaVersion"] = 99
    p["inventories"] = [bad]
    add("schema-failed-matching-locator", p, "SCHEMA; package record also missing unless suppressed only for failed loc")

    # Extra property on plan after schema (additionalProperties).
    p = copy.deepcopy(base)
    p["enumeration_plan"]["notAField"] = True
    add("plan-additional-property", p, "PLAN_SCHEMA")

    # Integer-looking string in examinedPaths.
    p = copy.deepcopy(base)
    p["inventories"][0]["examinedPaths"] = list(file_inv["examinedPaths"]) + [0]
    add("examined-path-integer", p, "type: non-string examined path")

    # Duplicate projection closure within a row.
    p = copy.deepcopy(base)
    rows = copy.deepcopy(file_inv["rows"])
    det = "closure2:2222222222222222222222222222222222222222222222222222222222222222"
    rows[4]["projections"] = [{"closureId": det, "kind": "detector"}, {"closureId": det, "kind": "detector"}]
    p["inventories"][0]["rows"] = rows
    add("duplicate-projection-closure", p, "DUPLICATE projection id within row")

    # External path row.
    p = copy.deepcopy(base)
    rows = copy.deepcopy(file_inv["rows"])
    rows[0]["path"] = "outside/abs.txt"
    rows[0]["nativeSubjectId"] = "outside/abs.txt"
    rows[0]["qualifiedName"] = "outside/abs.txt"
    p["inventories"][0]["rows"] = rows
    p["inventories"][0]["examinedPaths"] = list(file_inv["examinedPaths"])
    add("row-path-outside-extent", p, "ROW_PATH / EXTERNAL_PATH")

    # Membership row derivation: corrupt reason on an in-scope row.
    p = copy.deepcopy(base)
    p["membership"]["rows"][0]["reason"] = "host-ignore-convention"
    add("membership-row-reason-corrupt", p, "ROW_DERIVATION then digest mismatch; not UNIT_ROOT")

    # Membership order: swap two unit-less row paths' order by reversing rows.
    p = copy.deepcopy(base)
    p["membership"]["rows"] = list(reversed(p["membership"]["rows"]))
    add("membership-rows-reversed", p, "MEMBERSHIP_ORDER")

    return mutations


def main() -> int:
    if sys.flags.int_max_str_digits != 0 or sys.get_int_max_str_digits() != 0:
        print("reference integer profile required", file=sys.stderr)
        return 2
    model = _load(OVERLAY, "enumeration_model_e39")
    cases = json.loads(CASES.read_text(encoding="utf-8"))
    mismatches = []
    replay = []
    for i, row in enumerate(cases):
        got = outcome(model, row["input"])
        expected = row["expected"]
        if not got["ok"]:
            mismatches.append({"case": i, "kind": "e39-exception", "error": got})
            replay.append({"case": i, "match": False, "got": got})
            continue
        equal = model.C.equal_typed(got["result"], expected)
        replay.append(
            {
                "case": i,
                "match": equal,
                "expectedResult": expected.get("result"),
                "gotResult": got["result"].get("result"),
                "gotRefusals": got["result"].get("refusals"),
            }
        )
        if not equal:
            mismatches.append(
                {
                    "case": i,
                    "kind": "value-mismatch",
                    "expectedResult": expected.get("result"),
                    "expectedRefusals": expected.get("refusals"),
                    "gotResult": got["result"].get("result"),
                    "gotRefusals": got["result"].get("refusals"),
                    "expectedRecords": got["result"].get("expectedRecords"),
                }
            )

    mut_rows = []
    for spec in build_mutations(cases[0]["input"]):
        got = outcome(model, spec["input"])
        mut_rows.append(
            {
                "id": spec["id"],
                "note": spec["note"],
                "input": spec["input"],
                "e39": got,
            }
        )

    report = {
        "python": sys.version,
        "int_max_str_digits": sys.flags.int_max_str_digits,
        "overlay": str(OVERLAY),
        "overlaySha256": hashlib.sha256(OVERLAY.read_bytes()).hexdigest(),
        "overlayBytes": OVERLAY.stat().st_size,
        "cases": len(cases),
        "matches": sum(1 for r in replay if r["match"]),
        "mismatches": mismatches,
        "replay": replay,
        "mutationCount": len(mut_rows),
    }
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    MUTATIONS.write_text(json.dumps(mut_rows) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("cases", "matches", "mutationCount")} | {"mismatchCount": len(mismatches)}, indent=2))
    if mismatches:
        print("MISMATCHES", json.dumps(mismatches, indent=2)[:4000])
    return 0 if not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
