"""Enumeration plan/inventory reference admission (design evidence, not a host runtime).

Preconditions (ALL caller-supplied records are already owner-admitted except the
two enumeration schemas this module validates):
- plan, analysis_spec, scope_descriptor, membership, native context descriptors,
  universe descriptors, bind results, and closure kind map are trusted owner outputs.
- This module does not call admit_native_context / bind_* / symbol extraction.
- membership_derivation, if provided, is an explicit typed adapter that re-runs
  discover_units/assign_membership and requires equality; omitting it is not a
  silent True. Host extents then come from the admitted membership rows.
- policy_document is never used to drop required cells.
- Returning result=ADMIT is enumeration-join admission only. It is not a Run,
  not full graph closure, and not native extraction qualification.

Evaluation-subject identities are computed here as
subject3: + H("evaluation-subject", {schemaVersion:3, universe, kind, nativeSubjectId}).
They are NOT stored on EnumerationPlanV1 or SubjectInventoryV1. identity-model.v3
PREFIX registration is a root follow-up.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
NATIVE = HERE.parent / "native"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


C = _load("enum_canonical", HERE / "canonical.py")
NV = _load("enum_native_model", NATIVE / "native_evidence_model.v2.py")

PLAN_SCHEMA = json.loads((HERE / "enumeration-plan.schema.v1.json").read_text(encoding="utf-8"))
INV_SCHEMA = json.loads((HERE / "subject-inventory.schema.v1.json").read_text(encoding="utf-8"))
KIND_MAP = PLAN_SCHEMA["x-opensip-kind-derivation"]
LANG_TABLE = INV_SCHEMA["x-opensip-subject-language-table"]["members"]
CAUSE_REG = json.loads((NATIVE / "native-evidence.schemas.v2.json").read_text(encoding="utf-8"))[
    "x-opensip-deficiency-cause-registry"
]["deficiencies"]
OWNER_DEF = json.loads((NATIVE / "native-evidence.schemas.v2.json").read_text(encoding="utf-8"))["$defs"]["DeficiencyV2"]["enum"]
OWNER_CAUSE = json.loads((NATIVE / "native-evidence.schemas.v2.json").read_text(encoding="utf-8"))["$defs"]["NativeCause"]["enum"]

SUBJECT_ID_RE = re.compile(r"^[a-z][a-z0-9-]*:[^\u0000-\u001f\u007f-\u009f]+$")
LOGICAL_PATH_RE = re.compile(r"^[^/\\\u0000]{1,255}(/[^/\\\u0000]{1,255})*$")
CODE_SUFFIX = (".ts", ".tsx", ".mts", ".cts", ".js", ".jsx", ".mjs", ".cjs", ".rs")

INTERNAL_FAULTS = (
    "ENUMERATION_PLAN_SCHEMA",
    "ENUMERATION_INVENTORY_SCHEMA",
    "ENUMERATION_PLAN_SNAPSHOT_MISMATCH",
    "ENUMERATION_PLAN_SCOPE_DIGEST_MISMATCH",
    "ENUMERATION_PLAN_MEMBERSHIP_DIGEST_MISMATCH",
    "ENUMERATION_PLAN_CELL_TUPLE_MISMATCH",
    "ENUMERATION_PLAN_KIND_MAP",
    "ENUMERATION_PLAN_PROGRAM_BINDINGS_OVERFLOW",
    "ENUMERATION_PLAN_DEFAULT_UNIT",
    "ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR",
    "ENUMERATION_BINDING_ENUMERATOR_NOT_IN_PLAN",
    "ENUMERATION_BINDING_ENUMERATOR_KIND",
    "ENUMERATION_BINDING_CONTEXT_NOT_IN_PLAN",
    "ENUMERATION_BINDING_UNIVERSE_NOT_IN_INPUTS",
    "ENUMERATION_BINDING_UNIVERSE_NOT_BOUND_TO_SELECTED_CONTEXT",
    "ENUMERATION_BINDING_DUPLICATE_UNIVERSE",
    "ENUMERATION_BINDING_PROGRAM_ENTRY",
    "ENUMERATION_BINDING_EXTENT_KINDS",
    "ENUMERATION_BINDING_EXTENT_PATHS",
    "ENUMERATION_BINDING_CORRUPT",
    "ENUMERATION_ADMISSION_PRECONDITION",
    "ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION",
    "ENUMERATION_INVENTORY_MISSING_RECORD",
    "ENUMERATION_INVENTORY_ORDINAL_UNBOUND",
    "ENUMERATION_INVENTORY_FILE_TOTALITY",
    "ENUMERATION_INVENTORY_PACKAGE_TOTALITY",
    "ENUMERATION_INVENTORY_SYMBOL_EXAMINED",
    "ENUMERATION_INVENTORY_EXAMINED_OUTSIDE_EXTENT",
    "ENUMERATION_INVENTORY_ROW_PATH",
    "ENUMERATION_INVENTORY_DUPLICATE",
    "ENUMERATION_INVENTORY_LANGUAGE",
    "ENUMERATION_INVENTORY_FILE_NAME",
    "ENUMERATION_INVENTORY_PACKAGE_NAME",
    "ENUMERATION_INVENTORY_SYMBOL_ID",
    "ENUMERATION_INVENTORY_RECONCILE",
    "ENUMERATION_INVENTORY_CAUSE_CARRIER",
    "ENUMERATION_INVENTORY_CAUSE_ENUM_DRIFT",
    "ENUMERATION_INVENTORY_EXTERNAL_PATH",
    "ENUMERATION_INVENTORY_UNEXPECTED_RECORD",
)

AdmissionError = C.AdmissionError


def raw_digest(obj: dict) -> str:
    return hashlib.sha256(C.canonical(obj)).hexdigest()


def evaluation_subject_id(universe: str, kind: str, native_subject_id: str) -> str:
    """subject3: prefix. Not registered in identity-model.v3 PREFIX (root follow-up)."""
    desc = {"schemaVersion": 3, "universe": universe, "kind": kind, "nativeSubjectId": native_subject_id}
    return "subject3:" + C.identity("evaluation-subject", desc)


def _cap_kinds(capability_id: str) -> list[str]:
    raw = KIND_MAP.get(capability_id)
    if raw is None or not isinstance(raw, list):
        return []
    return sorted(raw)


def _suffix_language(path: str) -> str:
    name = path.rsplit("/", 1)[-1]
    best = ""
    lang = "unspecified"
    for row in LANG_TABLE:
        for suf in row["suffixes"]:
            if name.endswith(suf) and len(suf) >= len(best):
                best = suf
                lang = row["languageId"]
    return lang


def _internal_root(workspace_root: str) -> str:
    return "" if workspace_root == "." else workspace_root


def _under(path: str, root: str) -> bool:
    return NV._under_unit(path, root)


def _excluded_row(row: dict) -> bool:
    if row["membership"] == "outside-project-boundary":
        return True
    return row["reason"] in {
        "host-ignore-convention",
        "nested-repository",
        "nested-project",
        "custody-excluded",
    }


def _in_scope(path: str, scope: dict) -> bool:
    for ex in scope.get("excludedPathPrefixes") or []:
        if ex in (".", ""):
            continue
        if _under(path, ex):
            return False
    prefixes = scope.get("pathPrefixes") or []
    if not prefixes:
        return True
    return any(_under(path, "" if p == "." else p) for p in prefixes)


def _logical_path(value: str) -> bool:
    if value in (".", ""):
        return False
    return bool(LOGICAL_PATH_RE.match(value)) and not any(seg in (".", "..", "") for seg in value.split("/"))


def check_copied_enums() -> None:
    plan_def = PLAN_SCHEMA["$defs"]["DeficiencyV2"]["enum"]
    inv_def = INV_SCHEMA["$defs"]["DeficiencyV2"]["enum"]
    plan_c = PLAN_SCHEMA["$defs"]["NativeCause"]["enum"]
    inv_c = INV_SCHEMA["$defs"]["NativeCause"]["enum"]
    if plan_def != OWNER_DEF or inv_def != OWNER_DEF or plan_c != OWNER_CAUSE or inv_c != OWNER_CAUSE:
        raise AdmissionError("ENUMERATION_INVENTORY_CAUSE_ENUM_DRIFT")


def _carrier(deficiency, native_cause, faults: list[str]) -> None:
    if deficiency is None:
        if native_cause is not None:
            faults.append("ENUMERATION_INVENTORY_CAUSE_CARRIER")
        return
    row = CAUSE_REG.get(deficiency)
    if row is None:
        faults.append("ENUMERATION_INVENTORY_CAUSE_CARRIER")
        return
    rule = row.get("nativeCause")
    allowed = row.get("allowedCauses") or []
    if rule == "must-be-null":
        if native_cause is not None:
            faults.append("ENUMERATION_INVENTORY_CAUSE_CARRIER")
    elif rule == "required":
        if native_cause not in allowed:
            faults.append("ENUMERATION_INVENTORY_CAUSE_CARRIER")
    elif rule == "optional":
        if native_cause is not None and native_cause not in allowed:
            faults.append("ENUMERATION_INVENTORY_CAUSE_CARRIER")


def _unit_for_cell(membership: dict, workspace_root: str, language_mode: str):
    want = _internal_root(workspace_root)
    fam = "rust" if language_mode.startswith("rust") else ("tsjs" if language_mode != "syntax-only" else None)
    for u in membership["units"]:
        if u["rootPath"] == want and u["languageMode"] == language_mode:
            return u
        if fam and u["rootPath"] == want and u["languageFamily"] == fam and language_mode != "syntax-only":
            if u["languageMode"] == language_mode:
                return u
    return None


def host_extents(membership: dict, snapshot_paths: list[str], scope: dict, workspace_root: str, language_mode: str) -> dict[str, list[str]]:
    """Deterministic extents from admitted membership + snapshot paths. No facts."""
    root = _internal_root(workspace_root)
    unit = _unit_for_cell(membership, workspace_root, language_mode)
    by_path = {r["path"]: r for r in membership["rows"]}
    files: list[str] = []
    symbols: list[str] = []
    packages: list[str] = []
    for path in snapshot_paths:
        if not _under(path, root):
            continue
        if not _in_scope(path, scope):
            continue
        row = by_path.get(path)
        if row is None or _excluded_row(row):
            continue
        files.append(path)
        name = path.rsplit("/", 1)[-1]
        if language_mode == "syntax-only":
            if row["membership"] in ("syntax-only", "unsupported-file") or row["reason"] in ("grammar-only", "no-program-unit-for-language"):
                if path.endswith(CODE_SUFFIX):
                    symbols.append(path)
        elif unit is not None and row["membership"] == "program-member" and row.get("unitOrdinal") == unit["unitOrdinal"]:
            if path.endswith(CODE_SUFFIX):
                symbols.append(path)
        if name == "package.json":
            packages.append(path)
    if unit is not None and unit["languageFamily"] == "rust":
        if unit["unitKind"] == "cargo-package":
            manifest = "Cargo.toml" if unit["rootPath"] == "" else unit["rootPath"].rstrip("/") + "/Cargo.toml"
            if manifest in snapshot_paths and manifest not in packages:
                row = by_path.get(manifest)
                if row is not None and not _excluded_row(row):
                    packages.append(manifest)
        for member in unit.get("memberPackageRoots") or []:
            manifest = member.rstrip("/") + "/Cargo.toml" if member else "Cargo.toml"
            if manifest in snapshot_paths:
                row = by_path.get(manifest)
                if row is not None and not _excluded_row(row) and manifest not in packages:
                    packages.append(manifest)
    return {
        "file": sorted(set(files)),
        "symbol": sorted(set(symbols)),
        "package": sorted(set(packages)),
    }


def _u1_entry(unit: dict | None, language_mode: str):
    if language_mode in ("js-synthesized", "rust-cargo", "rust-cargo-prepared", "syntax-only"):
        return None
    if unit is None:
        return None
    return unit.get("markerPath")


def admit_enumeration(
    *,
    plan: dict,
    plan_id: str,
    analysis_spec: dict,
    scope_descriptor: dict,
    membership: dict,
    enumeration_plan: dict,
    inventories: list[dict],
    snapshot_paths: list[str],
    native_contexts: dict,
    universes: dict,
    closures: dict,
    config_graphs: dict | None = None,
    membership_derivation: dict | None = None,
    policy_document: dict | None = None,
) -> dict:
    """Verify enumeration joins over already owner-admitted native/Plan inputs.

    Required kwargs have no defaults. config_graphs is required for available
    TypeScript bindings (typed omission -> ENUMERATION_ADMISSION_PRECONDITION),
    not a silent skip. membership_derivation is optional and explicit.
    policy_document is ignored for cell population.
    """
    faults: list[str] = []
    check_copied_enums()

    try:
        C.validate(PLAN_SCHEMA, enumeration_plan)
    except Exception:
        return {"result": "REFUSE", "refusals": ["ENUMERATION_PLAN_SCHEMA"], "index": [], "population": {},
                "evaluationSubjects": []}

    if enumeration_plan["snapshotId"] != plan["snapshotId"]:
        faults.append("ENUMERATION_PLAN_SNAPSHOT_MISMATCH")
    if enumeration_plan["scopeDigest"] != raw_digest(scope_descriptor) or enumeration_plan["scopeDigest"] != plan["scopeDigest"]:
        faults.append("ENUMERATION_PLAN_SCOPE_DIGEST_MISMATCH")
    if enumeration_plan["membershipDigest"] != raw_digest(membership):
        faults.append("ENUMERATION_PLAN_MEMBERSHIP_DIGEST_MISMATCH")

    if membership_derivation is not None:
        required = {"markers", "files"}
        if set(membership_derivation) < required:
            faults.append("ENUMERATION_ADMISSION_PRECONDITION")
        else:
            disc = NV.discover_units(
                membership_derivation["markers"],
                membership_derivation.get("explicit_workspace_roots"),
                membership_derivation.get("boundaries"),
            )
            if disc.get("refused"):
                faults.append("ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION")
            else:
                recomputed = NV.assign_membership(disc["units"], membership_derivation["files"], membership_derivation.get("boundaries"))
                if not C.equal_typed(recomputed, membership):
                    faults.append("ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION")

    requested = list(analysis_spec["requestedCapabilities"])
    cells = enumeration_plan["cells"]
    req_tuples = [(r["capabilityId"], r["languageMode"], r["workspaceRoot"], r["required"]) for r in requested]
    cell_tuples = [(c["capabilityId"], c["languageMode"], c["workspaceRoot"], c["required"]) for c in cells]
    if len(cells) != len(requested) or sorted(req_tuples) != sorted(cell_tuples):
        faults.append("ENUMERATION_PLAN_CELL_TUPLE_MISMATCH")
    for cell in cells:
        expected_kinds = _cap_kinds(cell["capabilityId"])
        if cell["kinds"] != expected_kinds:
            faults.append("ENUMERATION_PLAN_KIND_MAP")
        if len(cell["programBindings"]) > 128:
            faults.append("ENUMERATION_PLAN_PROGRAM_BINDINGS_OVERFLOW")
        defaults = [b for b in cell["programBindings"] if b.get("provenance") == "default-unit"]
        if len(defaults) > 1 or (defaults and defaults[0]["ordinal"] != 0):
            faults.append("ENUMERATION_PLAN_DEFAULT_UNIT")
        seen_u = []
        for b in cell["programBindings"]:
            en = b["enumerator"]
            if en.get("status") != "selected" or not en.get("closureId"):
                faults.append("ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR")
                continue
            if en["closureId"] not in plan["semanticClosures"] or en["closureId"] not in closures:
                faults.append("ENUMERATION_BINDING_ENUMERATOR_NOT_IN_PLAN")
            elif closures[en["closureId"]].get("kind") != "provider":
                faults.append("ENUMERATION_BINDING_ENUMERATOR_KIND")
            ctx = b.get("nativeContextDigest")
            if ctx is not None:
                if ctx not in plan["nativeContextDigests"] or ctx not in native_contexts:
                    faults.append("ENUMERATION_BINDING_CONTEXT_NOT_IN_PLAN")
            ext_kinds = [e["kind"] for e in b["extents"]]
            if sorted(ext_kinds) != expected_kinds:
                faults.append("ENUMERATION_BINDING_EXTENT_KINDS")
            host = host_extents(membership, snapshot_paths, scope_descriptor, cell["workspaceRoot"], cell["languageMode"])
            for e in b["extents"]:
                if e["paths"] != host.get(e["kind"], []):
                    faults.append("ENUMERATION_BINDING_EXTENT_PATHS")
            entry = b.get("programEntry")
            if entry is not None:
                if not _logical_path(entry) or entry not in snapshot_paths:
                    faults.append("ENUMERATION_BINDING_PROGRAM_ENTRY")
                if b.get("provenance") == "default-unit":
                    faults.append("ENUMERATION_BINDING_PROGRAM_ENTRY")
            uni = b.get("universe")
            if uni is not None:
                if uni in seen_u:
                    faults.append("ENUMERATION_BINDING_DUPLICATE_UNIVERSE")
                seen_u.append(uni)
                rec = universes.get(uni)
                if rec is None:
                    faults.append("ENUMERATION_BINDING_UNIVERSE_NOT_IN_INPUTS")
                else:
                    ncid = rec.get("nativeContextId") or rec.get("descriptor", {}).get("nativeContextId")
                    if isinstance(ncid, str) and ncid.startswith("sha256:"):
                        ncid = ncid[len("sha256:"):]
                    if ctx is not None and ncid != ctx:
                        faults.append("ENUMERATION_BINDING_UNIVERSE_NOT_BOUND_TO_SELECTED_CONTEXT")
                    if rec.get("bindResult") not in (None, "ADMIT"):
                        faults.append("ENUMERATION_BINDING_CORRUPT")
                    mode = cell["languageMode"]
                    if mode in ("ts-tsconfig", "js-allowjs", "js-synthesized"):
                        if config_graphs is None or uni not in config_graphs:
                            faults.append("ENUMERATION_ADMISSION_PRECONDITION")
                        else:
                            graph = config_graphs[uni]
                            derived = _u1_entry(_unit_for_cell(membership, cell["workspaceRoot"], mode), mode)
                            expected_entry = entry if entry is not None else derived
                            if graph.get("entryConfigPath") != expected_entry:
                                faults.append("ENUMERATION_BINDING_PROGRAM_ENTRY")

    expected_keys = []
    binding_by = {}
    for ci, cell in enumerate(cells):
        for b in cell["programBindings"]:
            for kind in cell["kinds"]:
                expected_keys.append((ci, b["ordinal"], kind))
                binding_by[(ci, b["ordinal"], kind)] = (cell, b)

    seen_inv = {}
    index = []
    eval_subjects = []
    row_index = {}
    for inv in inventories:
        try:
            C.validate(INV_SCHEMA, inv)
        except Exception:
            faults.append("ENUMERATION_INVENTORY_SCHEMA")
            continue
        if inv["parameterDigest"] != raw_digest(enumeration_plan) or inv["planId"] != plan_id:
            faults.append("ENUMERATION_INVENTORY_ORDINAL_UNBOUND")
        key = (inv["cellOrdinal"], inv["programOrdinal"], inv["kind"])
        if key in seen_inv:
            faults.append("ENUMERATION_INVENTORY_DUPLICATE")
        seen_inv[key] = inv
        if key not in binding_by:
            faults.append("ENUMERATION_INVENTORY_UNEXPECTED_RECORD")
            continue
        cell, binding = binding_by[key]
        extent = next((e["paths"] for e in binding["extents"] if e["kind"] == inv["kind"]), None)
        if extent is None:
            faults.append("ENUMERATION_BINDING_EXTENT_KINDS")
            continue
        extent_set = set(extent)
        examined = inv["examinedPaths"]
        if any(p not in extent_set for p in examined):
            faults.append("ENUMERATION_INVENTORY_EXAMINED_OUTSIDE_EXTENT")
        if inv["state"] == "complete":
            if inv["deficiency"] is not None or inv["nativeCause"] is not None:
                faults.append("ENUMERATION_INVENTORY_CAUSE_CARRIER")
        else:
            if inv["deficiency"] is None:
                faults.append("ENUMERATION_INVENTORY_CAUSE_CARRIER")
            _carrier(inv["deficiency"], inv["nativeCause"], faults)
        if inv["state"] == "unavailable":
            if inv["rows"] or inv["examinedPaths"]:
                faults.append("ENUMERATION_INVENTORY_ROW_PATH")
        if inv["state"] == "complete" and inv["kind"] in ("file", "symbol"):
            if set(examined) != extent_set:
                faults.append("ENUMERATION_INVENTORY_SYMBOL_EXAMINED" if inv["kind"] == "symbol" else "ENUMERATION_INVENTORY_FILE_TOTALITY")
        if inv["state"] == "complete" and inv["kind"] == "file":
            row_paths = [r["path"] for r in inv["rows"]]
            if set(row_paths) != extent_set:
                faults.append("ENUMERATION_INVENTORY_FILE_TOTALITY")
        if inv["state"] == "complete" and inv["kind"] == "package":
            row_paths = [r["path"] for r in inv["rows"]]
            if set(row_paths) != extent_set:
                faults.append("ENUMERATION_INVENTORY_PACKAGE_TOTALITY")
        ids = []
        paths = []
        proj_ids = []
        for r in inv["rows"]:
            if r["kind"] != inv["kind"]:
                faults.append("ENUMERATION_INVENTORY_ROW_PATH")
            if r["path"] not in extent_set or r["path"] not in examined:
                faults.append("ENUMERATION_INVENTORY_ROW_PATH")
            if r["path"] not in snapshot_paths:
                faults.append("ENUMERATION_INVENTORY_EXTERNAL_PATH")
            if r["nativeSubjectId"] in ids or r["path"] in paths:
                faults.append("ENUMERATION_INVENTORY_DUPLICATE")
            ids.append(r["nativeSubjectId"])
            paths.append(r["path"])
            want_lang = _suffix_language(r["path"])
            if inv["kind"] == "package":
                if r["subjectLanguage"] not in ("json", "toml") or r["subjectLanguage"] != want_lang:
                    faults.append("ENUMERATION_INVENTORY_LANGUAGE")
                if r["nativeSubjectId"] != r["qualifiedName"] or not r["nativeSubjectId"]:
                    faults.append("ENUMERATION_INVENTORY_PACKAGE_NAME")
            elif inv["kind"] == "file":
                if r["qualifiedName"] != r["path"] or r["nativeSubjectId"] != r["path"]:
                    faults.append("ENUMERATION_INVENTORY_FILE_NAME")
                if r["subjectLanguage"] != want_lang:
                    faults.append("ENUMERATION_INVENTORY_LANGUAGE")
            else:
                if not SUBJECT_ID_RE.match(r["nativeSubjectId"]):
                    faults.append("ENUMERATION_INVENTORY_SYMBOL_ID")
                if r["subjectLanguage"] != want_lang:
                    faults.append("ENUMERATION_INVENTORY_LANGUAGE")
            for p in r.get("projections") or []:
                if p["closureId"] in proj_ids:
                    faults.append("ENUMERATION_INVENTORY_DUPLICATE")
                proj_ids.append(p["closureId"])
            uni = binding.get("universe")
            if uni and inv["state"] != "unavailable":
                rk = (uni, inv["kind"], r["nativeSubjectId"])
                payload = {k: r[k] for k in r}
                if rk in row_index and not C.equal_typed(row_index[rk], payload):
                    faults.append("ENUMERATION_INVENTORY_RECONCILE")
                row_index[rk] = payload
                eval_subjects.append(evaluation_subject_id(uni, inv["kind"], r["nativeSubjectId"]))
        index.append({"cellOrdinal": inv["cellOrdinal"], "programOrdinal": inv["programOrdinal"],
                      "kind": inv["kind"], "state": inv["state"], "rowCount": len(inv["rows"]),
                      "universe": binding.get("universe")})

    for key in expected_keys:
        if key not in seen_inv:
            faults.append("ENUMERATION_INVENTORY_MISSING_RECORD")

    faults = sorted(set(faults))
    pop = {"file": 0, "symbol": 0, "package": 0}
    for inv in seen_inv.values():
        if inv["state"] != "unavailable":
            pop[inv["kind"]] = pop.get(inv["kind"], 0) + len(inv["rows"])
    return {
        "result": "ADMIT" if not faults else "REFUSE",
        "refusals": faults,
        "index": sorted(index, key=lambda r: (r["cellOrdinal"], r["programOrdinal"], r["kind"])),
        "population": pop,
        "evaluationSubjects": sorted(set(eval_subjects)),
        "expectedRecords": len(expected_keys),
        "internalFaults": list(INTERNAL_FAULTS),
        "standing": "enumeration-join admission only; not a Run",
    }
