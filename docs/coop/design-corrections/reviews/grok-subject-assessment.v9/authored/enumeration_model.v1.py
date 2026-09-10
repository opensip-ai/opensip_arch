"""Enumeration plan/inventory reference admission (design evidence, not a host runtime).

Preconditions: plan, analysis_spec, scope_descriptor, membership, native context
descriptors, universe resolved-input descriptors, and closure kind map are already
owner-admitted. This module does not call admit_native_context, bind_*, or symbol
extraction, and does not re-hash native universe H (that is the native owner's
admission). ADMIT is enumeration-join admission only — not a Run.

evaluation-subject uses identity-model.v3 identifier (PREFIX already maps
evaluation-subject → subject3). Plan/inventory records do not store that descriptor.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import tomllib
from pathlib import Path

from jsonschema.exceptions import ValidationError

HERE = Path(__file__).resolve().parent
NATIVE = HERE.parent / "native"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


C = _load("enum_canonical", HERE / "canonical.py")
NV = _load("enum_native_model", NATIVE / "native_evidence_model.v2.py")
IM = _load("enum_identity_v3", HERE / "identity-model.v3.py")

PLAN_SCHEMA = json.loads((HERE / "enumeration-plan.schema.v1.json").read_text(encoding="utf-8"))
INV_SCHEMA = json.loads((HERE / "subject-inventory.schema.v1.json").read_text(encoding="utf-8"))
KIND_MAP = PLAN_SCHEMA["x-opensip-kind-derivation"]
LANG_TABLE = INV_SCHEMA["x-opensip-subject-language-table"]["members"]
CAUSE_REG = json.loads((NATIVE / "native-evidence.schemas.v2.json").read_text(encoding="utf-8"))[
    "x-opensip-deficiency-cause-registry"
]["deficiencies"]
OWNER_DEF = json.loads((NATIVE / "native-evidence.schemas.v2.json").read_text(encoding="utf-8"))["$defs"]["DeficiencyV2"]["enum"]
OWNER_CAUSE = json.loads((NATIVE / "native-evidence.schemas.v2.json").read_text(encoding="utf-8"))["$defs"]["NativeCause"]["enum"]
ENGINE = json.loads((HERE / "identity-schemas.v2.json").read_text(encoding="utf-8"))[
    "x-opensip-digest-domains"
]["languageModes"]["map"]

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
    "ENUMERATION_BINDING_ENGINE_DOMAIN",
    "ENUMERATION_BINDING_DUPLICATE_UNIVERSE",
    "ENUMERATION_BINDING_PROGRAM_ENTRY",
    "ENUMERATION_BINDING_EXTENT_KINDS",
    "ENUMERATION_BINDING_EXTENT_PATHS",
    "ENUMERATION_BINDING_UNAVAILABLE_INVENTORY",
    "ENUMERATION_BINDING_CAUSE",
    "ENUMERATION_ADMISSION_PRECONDITION",
    "ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION",
    "ENUMERATION_SCOPE_EXCLUDE_ALL",
    "ENUMERATION_PROJECTION_DETECTOR",
    "ENUMERATION_PACKAGE_PARSE",
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
DERIVATION_ALLOWED = {"markers", "files", "explicit_workspace_roots", "boundaries", "mode"}
DERIVATION_REQUIRED = {"markers", "files", "mode"}


def raw_digest(obj: dict) -> str:
    return hashlib.sha256(C.canonical(obj)).hexdigest()


def canon_str_list(values: list[str]) -> list[str]:
    uniq = list(dict.fromkeys(values))
    return sorted(uniq, key=lambda s: C.canonical(s))


def evaluation_subject_id(universe: str, kind: str, native_subject_id: str) -> str:
    desc = {"schemaVersion": 3, "universe": universe, "kind": kind, "nativeSubjectId": native_subject_id}
    minted = IM.identifier("evaluation-subject", desc)
    parity = "subject3:" + C.identity("evaluation-subject", desc)
    if minted != parity:
        raise AdmissionError("ENUMERATION_EVALUATION_SUBJECT_RECIPE")
    return minted


def _cap_kinds(capability_id: str) -> list[str]:
    raw = KIND_MAP.get(capability_id)
    if not isinstance(raw, list):
        return []
    return canon_str_list([k for k in raw if isinstance(k, str)])


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


def _in_scope(path: str, scope: dict, faults: list[str] | None = None) -> bool:
    excluded = scope.get("excludedPathPrefixes") or []
    if "." in excluded:
        if faults is not None:
            _add(faults, "ENUMERATION_SCOPE_EXCLUDE_ALL")
        return False
    for ex in excluded:
        if _under(path, _internal_root(ex) if ex != "." else ""):
            return False
    prefixes = scope.get("pathPrefixes") or []
    if not prefixes:
        return True
    return any(_under(path, "" if p == "." else p) for p in prefixes)


def _logical_path(value: str) -> bool:
    if value in (".", ""):
        return False
    return bool(LOGICAL_PATH_RE.match(value)) and not any(seg in (".", "..", "") for seg in value.split("/"))


def _add(faults: list[str], key: str) -> None:
    if key not in faults:
        faults.append(key)


def check_copied_enums() -> None:
    if (PLAN_SCHEMA["$defs"]["DeficiencyV2"]["enum"] != OWNER_DEF
            or INV_SCHEMA["$defs"]["DeficiencyV2"]["enum"] != OWNER_DEF
            or PLAN_SCHEMA["$defs"]["NativeCause"]["enum"] != OWNER_CAUSE
            or INV_SCHEMA["$defs"]["NativeCause"]["enum"] != OWNER_CAUSE):
        raise AdmissionError("ENUMERATION_INVENTORY_CAUSE_ENUM_DRIFT")


def _carrier(deficiency, native_cause, faults: list[str]) -> None:
    if deficiency is None:
        if native_cause is not None:
            _add(faults, "ENUMERATION_INVENTORY_CAUSE_CARRIER")
        return
    row = CAUSE_REG.get(deficiency)
    if row is None:
        _add(faults, "ENUMERATION_INVENTORY_CAUSE_CARRIER")
        return
    rule = row.get("nativeCause")
    allowed = row.get("allowedCauses") or []
    if rule == "must-be-null":
        if native_cause is not None:
            _add(faults, "ENUMERATION_INVENTORY_CAUSE_CARRIER")
    elif rule == "required":
        if native_cause not in allowed:
            _add(faults, "ENUMERATION_INVENTORY_CAUSE_CARRIER")
    elif rule == "optional":
        if native_cause is not None and native_cause not in allowed:
            _add(faults, "ENUMERATION_INVENTORY_CAUSE_CARRIER")


def _unit_for_cell(membership: dict, workspace_root: str, language_mode: str):
    want = _internal_root(workspace_root)
    for u in membership["units"]:
        if u["rootPath"] == want and u["languageMode"] == language_mode:
            return u
    return None


def _first_party_scoped(membership: dict, snapshot_paths: list[str], scope: dict, workspace_root: str, faults: list[str]) -> list[str]:
    root = _internal_root(workspace_root)
    by_path = {r["path"]: r for r in membership["rows"]}
    out = []
    for path in snapshot_paths:
        if not _under(path, root):
            continue
        if not _in_scope(path, scope, faults):
            continue
        row = by_path.get(path)
        if row is None or _excluded_row(row):
            continue
        out.append(path)
    return canon_str_list(out)


def host_file_extent(membership, snapshot_paths, scope, workspace_root, faults) -> list[str]:
    """Inventory exemption: all scoped first-party paths, including data/unsupported/Cargo.toml."""
    return _first_party_scoped(membership, snapshot_paths, scope, workspace_root, faults)


def host_symbol_extent(membership, snapshot_paths, scope, workspace_root, language_mode, universe, retained, faults) -> list[str]:
    """Compiler/syntax selected program scope from owner-admitted resolved inputs, not default membership."""
    scoped = set(_first_party_scoped(membership, snapshot_paths, scope, workspace_root, faults))
    by_path = {r["path"]: r for r in membership["rows"]}
    if language_mode == "syntax-only":
        out = [p for p in scoped if p.endswith(CODE_SUFFIX)]
        return canon_str_list(out)
    if language_mode in ("ts-tsconfig", "js-allowjs", "js-synthesized"):
        if not isinstance(universe, dict) or "programRootFiles" not in universe:
            _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
            return []
        roots = universe["programRootFiles"]
        out = []
        for p in roots:
            if p not in snapshot_paths:
                _add(faults, "ENUMERATION_BINDING_EXTENT_PATHS")
                continue
            if p in scoped and p.endswith(CODE_SUFFIX):
                out.append(p)
        return canon_str_list(out)
    if language_mode.startswith("rust"):
        own = (retained or {}).get("sourceUnitOwnership")
        if not isinstance(own, dict):
            _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
            return []
        selected = set(own.get("selectedUnitIds") or [])
        out = []
        for rel in own.get("ownership") or []:
            if rel.get("unitId") in selected and rel.get("path") in scoped:
                out.append(rel["path"])
        return canon_str_list(out)
    return []


def project_named_packages(snapshot_paths, scope, workspace_root, membership, source_blobs, faults) -> dict:
    """Host projection from retained snapshot bytes. Not a caller oracle list."""
    scoped = _first_party_scoped(membership, snapshot_paths, scope, workspace_root, faults)
    named, unnamed, failed = [], [], []
    for path in scoped:
        name = path.rsplit("/", 1)[-1]
        if name not in ("package.json", "Cargo.toml"):
            continue
        blob = source_blobs.get(path)
        if blob is None:
            _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
            failed.append({"path": path, "reason": "missing-bytes"})
            continue
        if name == "package.json":
            try:
                data = json.loads(blob.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                failed.append({"path": path, "reason": "json"})
                continue
            pkg = data.get("name") if isinstance(data, dict) else None
            if isinstance(pkg, str) and pkg:
                named.append({"path": path, "packageName": pkg, "format": "json"})
            else:
                unnamed.append({"path": path, "reason": "no-name"})
        else:
            try:
                data = tomllib.loads(blob.decode("utf-8"))
            except (UnicodeDecodeError, tomllib.TOMLDecodeError):
                failed.append({"path": path, "reason": "toml"})
                continue
            pkg = data.get("package", {}).get("name") if isinstance(data, dict) else None
            if isinstance(pkg, str) and pkg:
                named.append({"path": path, "packageName": pkg, "format": "toml"})
            else:
                unnamed.append({"path": path, "reason": "workspace-only" if "workspace" in (data or {}) else "no-name"})
    named.sort(key=lambda r: C.canonical(r["path"]))
    return {
        "named": named,
        "unnamed": unnamed,
        "parseFailed": failed,
        "namedPaths": canon_str_list([r["path"] for r in named]),
    }


def _u1_entry(unit: dict | None, language_mode: str):
    if language_mode in ("js-synthesized", "rust-cargo", "rust-cargo-prepared", "syntax-only"):
        return None
    if unit is None:
        return None
    return unit.get("markerPath")


def _ncid_suffix(value) -> str | None:
    if not isinstance(value, str):
        return None
    return value[len("sha256:"):] if value.startswith("sha256:") else value


def admit_enumeration(
    *,
    plan: dict,
    plan_id: str,
    analysis_spec: dict,
    scope_descriptor: dict,
    membership: dict,
    enumeration_plan: dict,
    inventories: list[dict],
    native_contexts: dict,
    universes: dict,
    closures: dict,
    snapshot_inventory: list | None = None,
    snapshot_paths: list | None = None,
    source_blobs: dict | None = None,
    retained_inputs: dict | None = None,
    membership_derivation: dict | None = None,
    policy_document: dict | None = None,
) -> dict:
    """Join-admit inventories against Plan-bound expected population.

    universes/native_contexts maps: actual owner-admitted descriptors keyed by
    bare H suffix. No bindResult flags. source_blobs: path -> exact snapshot
    bytes for package projection. retained_inputs[universe]: {configGraph?,
    sourceUnitOwnership?} nested owner records.
    """
    faults: list[str] = []
    empty = {"result": "REFUSE", "refusals": faults, "index": [], "population": {},
             "evaluationSubjects": [], "subjects": {}, "packageProjection": None,
             "expectedRecords": 0, "internalFaults": list(INTERNAL_FAULTS),
             "standing": "enumeration-join admission only; not a Run"}
    try:
        check_copied_enums()
    except AdmissionError as exc:
        empty["refusals"] = [str(exc)]
        return empty

    try:
        C.validate(PLAN_SCHEMA, enumeration_plan)
    except (AdmissionError, ValidationError):
        empty["refusals"] = ["ENUMERATION_PLAN_SCHEMA"]
        return empty

    if snapshot_inventory is not None:
        derived_paths = [row["path"] if isinstance(row, dict) else row for row in snapshot_inventory]
        if snapshot_paths is not None and snapshot_paths != derived_paths:
            _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
        snapshot_paths = derived_paths
    if snapshot_paths is None:
        empty["refusals"] = ["ENUMERATION_ADMISSION_PRECONDITION"]
        return empty

    if enumeration_plan["snapshotId"] != plan["snapshotId"]:
        _add(faults, "ENUMERATION_PLAN_SNAPSHOT_MISMATCH")
    if enumeration_plan["scopeDigest"] != raw_digest(scope_descriptor) or enumeration_plan["scopeDigest"] != plan["scopeDigest"]:
        _add(faults, "ENUMERATION_PLAN_SCOPE_DIGEST_MISMATCH")
    if enumeration_plan["membershipDigest"] != raw_digest(membership):
        _add(faults, "ENUMERATION_PLAN_MEMBERSHIP_DIGEST_MISMATCH")

    if membership_derivation is not None:
        if not isinstance(membership_derivation, dict):
            _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
        else:
            keys = set(membership_derivation)
            if not DERIVATION_REQUIRED <= keys or not keys <= DERIVATION_ALLOWED:
                _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
            elif membership_derivation["mode"] not in ("standalone-fixture", "operational"):
                _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
            elif membership_derivation["mode"] == "operational" and "boundaries" not in membership_derivation:
                _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
            else:
                bounds = membership_derivation.get("boundaries")
                if membership_derivation["mode"] == "standalone-fixture":
                    bounds = membership_derivation.get("boundaries")
                disc = NV.discover_units(
                    membership_derivation["markers"],
                    membership_derivation.get("explicit_workspace_roots"),
                    bounds,
                )
                if disc.get("refused"):
                    _add(faults, "ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION")
                else:
                    recomputed = NV.assign_membership(
                        disc["units"], membership_derivation["files"], bounds
                    )
                    if not C.equal_typed(recomputed, membership):
                        _add(faults, "ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION")

    requested = list(analysis_spec["requestedCapabilities"])
    cells = enumeration_plan["cells"]
    req_tuples = [(r["capabilityId"], r["languageMode"], r["workspaceRoot"], r["required"]) for r in requested]
    cell_tuples = [(c["capabilityId"], c["languageMode"], c["workspaceRoot"], c["required"]) for c in cells]
    if len(cells) != len(requested) or sorted(req_tuples) != sorted(cell_tuples):
        _add(faults, "ENUMERATION_PLAN_CELL_TUPLE_MISMATCH")

    needs_package = any("package" in c["kinds"] for c in cells)
    if needs_package and not isinstance(source_blobs, dict):
        _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
        source_blobs = {}

    retained_inputs = retained_inputs or {}
    package_proj_by_root = {}

    expected_keys = []
    binding_by = {}
    host_by = {}

    for cell in cells:
        expected_kinds = _cap_kinds(cell["capabilityId"])
        if not C.equal_typed(cell["kinds"], expected_kinds):
            _add(faults, "ENUMERATION_PLAN_KIND_MAP")
        if len(cell["programBindings"]) > 128:
            _add(faults, "ENUMERATION_PLAN_PROGRAM_BINDINGS_OVERFLOW")
        defaults = [b for b in cell["programBindings"] if b.get("provenance") == "default-unit"]
        if len(defaults) > 1 or (defaults and defaults[0]["ordinal"] != 0):
            _add(faults, "ENUMERATION_PLAN_DEFAULT_UNIT")
        seen_u = []
        root_key = cell["workspaceRoot"]
        if root_key not in package_proj_by_root and needs_package:
            package_proj_by_root[root_key] = project_named_packages(
                snapshot_paths, scope_descriptor, root_key, membership, source_blobs, faults
            )
        for b in cell["programBindings"]:
            en = b["enumerator"]
            if en.get("status") != "selected" or not en.get("closureId"):
                _add(faults, "ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR")
                continue
            if en["closureId"] not in plan["semanticClosures"] or en["closureId"] not in closures:
                _add(faults, "ENUMERATION_BINDING_ENUMERATOR_NOT_IN_PLAN")
            elif closures[en["closureId"]].get("kind") != "provider":
                _add(faults, "ENUMERATION_BINDING_ENUMERATOR_KIND")
            ctx = b.get("nativeContextDigest")
            uni = b.get("universe")
            available = uni is not None
            if ctx is not None:
                if ctx not in plan["nativeContextDigests"] or ctx not in native_contexts:
                    _add(faults, "ENUMERATION_BINDING_CONTEXT_NOT_IN_PLAN")
            ext_kinds = canon_str_list([e["kind"] for e in b["extents"]])
            if not C.equal_typed(ext_kinds, expected_kinds):
                _add(faults, "ENUMERATION_BINDING_EXTENT_KINDS")
            if available:
                if uni in seen_u:
                    _add(faults, "ENUMERATION_BINDING_DUPLICATE_UNIVERSE")
                seen_u.append(uni)
                urec = universes.get(uni)
                if not isinstance(urec, dict):
                    _add(faults, "ENUMERATION_BINDING_UNIVERSE_NOT_IN_INPUTS")
                    urec = {}
                if "bindResult" in urec:
                    _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
                ncid = _ncid_suffix(urec.get("nativeContextId"))
                if ctx is None or ncid != ctx:
                    _add(faults, "ENUMERATION_BINDING_UNIVERSE_NOT_BOUND_TO_SELECTED_CONTEXT")
                engine = ENGINE.get(cell["languageMode"])
                if urec.get("languageMode") not in (None, cell["languageMode"]):
                    _add(faults, "ENUMERATION_BINDING_ENGINE_DOMAIN")
                ctxrec = native_contexts.get(ctx) if ctx else None
                if isinstance(ctxrec, dict) and ctxrec.get("languageMode") not in (None, cell["languageMode"]):
                    _add(faults, "ENUMERATION_BINDING_ENGINE_DOMAIN")
                if engine is None:
                    _add(faults, "ENUMERATION_BINDING_ENGINE_DOMAIN")
                nested = retained_inputs.get(uni) or {}
                mode = cell["languageMode"]
                entry = b.get("programEntry")
                if entry is not None:
                    if not _logical_path(entry) or entry not in snapshot_paths:
                        _add(faults, "ENUMERATION_BINDING_PROGRAM_ENTRY")
                    if b.get("provenance") == "default-unit":
                        _add(faults, "ENUMERATION_BINDING_PROGRAM_ENTRY")
                if mode in ("ts-tsconfig", "js-allowjs", "js-synthesized"):
                    graph = nested.get("configGraph")
                    if graph is None:
                        _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
                    else:
                        derived = _u1_entry(_unit_for_cell(membership, cell["workspaceRoot"], mode), mode)
                        expected_entry = entry if entry is not None else derived
                        if graph.get("entryConfigPath") != expected_entry:
                            _add(faults, "ENUMERATION_BINDING_PROGRAM_ENTRY")
                file_ext = host_file_extent(membership, snapshot_paths, scope_descriptor, cell["workspaceRoot"], faults)
                sym_ext = host_symbol_extent(
                    membership, snapshot_paths, scope_descriptor, cell["workspaceRoot"],
                    cell["languageMode"], urec, nested, faults,
                ) if "symbol" in expected_kinds else []
                pkg_proj = package_proj_by_root.get(root_key)
                pkg_ext = pkg_proj["namedPaths"] if pkg_proj else []
                derived_ext = {"file": file_ext, "symbol": sym_ext, "package": pkg_ext}
                for e in b["extents"]:
                    if pkg_proj and e["kind"] == "package" and pkg_proj["parseFailed"]:
                        continue
                    if not C.equal_typed(e["paths"], derived_ext.get(e["kind"], [])):
                        _add(faults, "ENUMERATION_BINDING_EXTENT_PATHS")
                host_by[(cells.index(cell), b["ordinal"])] = derived_ext
            else:
                _carrier(b.get("deficiency"), b.get("nativeCause"), faults)
                if b.get("deficiency") is None:
                    _add(faults, "ENUMERATION_BINDING_CAUSE")
                entry = b.get("programEntry")
                if entry is not None and (not _logical_path(entry) or entry not in snapshot_paths):
                    _add(faults, "ENUMERATION_BINDING_PROGRAM_ENTRY")
                file_ext = host_file_extent(membership, snapshot_paths, scope_descriptor, cell["workspaceRoot"], faults)
                host_by[(cells.index(cell), b["ordinal"])] = {
                    "file": file_ext, "symbol": [],
                    "package": (package_proj_by_root.get(root_key) or {}).get("namedPaths") or [],
                }
        for b in cell["programBindings"]:
            for kind in cell["kinds"]:
                ci = cells.index(cell)
                expected_keys.append((ci, b["ordinal"], kind))
                binding_by[(ci, b["ordinal"], kind)] = (cell, b)

    seen_inv = {}
    schema_failed = set()
    subjects = {}
    for inv in inventories:
        try:
            C.validate(INV_SCHEMA, inv)
        except (AdmissionError, ValidationError):
            _add(faults, "ENUMERATION_INVENTORY_SCHEMA")
            loc = (inv.get("cellOrdinal"), inv.get("programOrdinal"), inv.get("kind"))
            if loc in binding_by:
                schema_failed.add(loc)
            continue
        if inv["parameterDigest"] != raw_digest(enumeration_plan) or inv["planId"] != plan_id:
            _add(faults, "ENUMERATION_INVENTORY_ORDINAL_UNBOUND")
        key = (inv["cellOrdinal"], inv["programOrdinal"], inv["kind"])
        if key in seen_inv:
            _add(faults, "ENUMERATION_INVENTORY_DUPLICATE")
        seen_inv[key] = inv
        if key not in binding_by:
            _add(faults, "ENUMERATION_INVENTORY_UNEXPECTED_RECORD")
            continue
        cell, binding = binding_by[key]
        extent = next((e["paths"] for e in binding["extents"] if e["kind"] == inv["kind"]), None)
        if extent is None:
            _add(faults, "ENUMERATION_BINDING_EXTENT_KINDS")
            continue
        extent_set = set(extent)
        uni = binding.get("universe")
        if uni is None:
            if inv["state"] != "unavailable":
                _add(faults, "ENUMERATION_BINDING_UNAVAILABLE_INVENTORY")
            if inv.get("deficiency") != binding.get("deficiency") or inv.get("nativeCause") != binding.get("nativeCause"):
                _add(faults, "ENUMERATION_BINDING_CAUSE")
        pkg_proj = package_proj_by_root.get(cell["workspaceRoot"])
        if inv["kind"] == "package" and pkg_proj and pkg_proj["parseFailed"]:
            if inv["state"] != "unavailable":
                _add(faults, "ENUMERATION_PACKAGE_PARSE")
            _carrier(inv.get("deficiency"), inv.get("nativeCause"), faults)
        examined = inv["examinedPaths"]
        if any(p not in extent_set for p in examined):
            _add(faults, "ENUMERATION_INVENTORY_EXAMINED_OUTSIDE_EXTENT")
        if inv["state"] == "complete":
            if inv["deficiency"] is not None or inv["nativeCause"] is not None:
                _add(faults, "ENUMERATION_INVENTORY_CAUSE_CARRIER")
            if not C.equal_typed(examined, extent):
                if inv["kind"] == "file":
                    _add(faults, "ENUMERATION_INVENTORY_FILE_TOTALITY")
                elif inv["kind"] == "symbol":
                    _add(faults, "ENUMERATION_INVENTORY_SYMBOL_EXAMINED")
                else:
                    _add(faults, "ENUMERATION_INVENTORY_PACKAGE_TOTALITY")
        else:
            if inv["deficiency"] is None:
                _add(faults, "ENUMERATION_INVENTORY_CAUSE_CARRIER")
            _carrier(inv["deficiency"], inv["nativeCause"], faults)
        if inv["state"] == "unavailable":
            if inv["rows"] or inv["examinedPaths"]:
                _add(faults, "ENUMERATION_INVENTORY_ROW_PATH")
            continue
        if inv["state"] == "complete" and inv["kind"] == "file":
            if set(r["path"] for r in inv["rows"]) != extent_set:
                _add(faults, "ENUMERATION_INVENTORY_FILE_TOTALITY")
        if inv["state"] == "complete" and inv["kind"] == "package":
            if set(r["path"] for r in inv["rows"]) != extent_set:
                _add(faults, "ENUMERATION_INVENTORY_PACKAGE_TOTALITY")
            if pkg_proj:
                by_path = {n["path"]: n["packageName"] for n in pkg_proj["named"]}
                for r in inv["rows"]:
                    expected_name = by_path.get(r["path"])
                    if expected_name is None or r["nativeSubjectId"] != expected_name or r["qualifiedName"] != expected_name:
                        _add(faults, "ENUMERATION_INVENTORY_PACKAGE_NAME")
        ids = []
        paths = []
        for r in inv["rows"]:
            if r["kind"] != inv["kind"]:
                _add(faults, "ENUMERATION_INVENTORY_ROW_PATH")
            if r["path"] not in extent_set or r["path"] not in examined:
                _add(faults, "ENUMERATION_INVENTORY_ROW_PATH")
            if r["path"] not in snapshot_paths:
                _add(faults, "ENUMERATION_INVENTORY_EXTERNAL_PATH")
            if r["nativeSubjectId"] in ids:
                _add(faults, "ENUMERATION_INVENTORY_DUPLICATE")
            ids.append(r["nativeSubjectId"])
            if inv["kind"] in ("file", "package"):
                if r["path"] in paths:
                    _add(faults, "ENUMERATION_INVENTORY_DUPLICATE")
                paths.append(r["path"])
            want_lang = _suffix_language(r["path"])
            if inv["kind"] == "package":
                if r["subjectLanguage"] not in ("json", "toml") or r["subjectLanguage"] != want_lang:
                    _add(faults, "ENUMERATION_INVENTORY_LANGUAGE")
            elif inv["kind"] == "file":
                if r["qualifiedName"] != r["path"] or r["nativeSubjectId"] != r["path"]:
                    _add(faults, "ENUMERATION_INVENTORY_FILE_NAME")
                if r["subjectLanguage"] != want_lang:
                    _add(faults, "ENUMERATION_INVENTORY_LANGUAGE")
            else:
                if not SUBJECT_ID_RE.match(r["nativeSubjectId"]):
                    _add(faults, "ENUMERATION_INVENTORY_SYMBOL_ID")
                if r["subjectLanguage"] != want_lang:
                    _add(faults, "ENUMERATION_INVENTORY_LANGUAGE")
            proj_ids = []
            for p in r.get("projections") or []:
                if p["closureId"] in proj_ids:
                    _add(faults, "ENUMERATION_INVENTORY_DUPLICATE")
                proj_ids.append(p["closureId"])
                if p["closureId"] not in plan["semanticClosures"] or closures.get(p["closureId"], {}).get("kind") != "detector":
                    _add(faults, "ENUMERATION_PROJECTION_DETECTOR")
            if uni:
                rk = (uni, inv["kind"], r["nativeSubjectId"])
                loc = {"cellOrdinal": inv["cellOrdinal"], "programOrdinal": inv["programOrdinal"],
                       "kind": inv["kind"], "state": inv["state"], "planId": inv["planId"]}
                payload = {k: r[k] for k in r}
                slot = subjects.setdefault(rk, {"payloads": [], "inventoryRefs": [], "evaluationSubject": None})
                slot["inventoryRefs"].append(loc)
                if slot["payloads"] and not any(C.equal_typed(prev, payload) for prev in slot["payloads"]):
                    _add(faults, "ENUMERATION_INVENTORY_RECONCILE")
                if not any(C.equal_typed(prev, payload) for prev in slot["payloads"]):
                    slot["payloads"].append(payload)
                if slot["evaluationSubject"] is None:
                    slot["evaluationSubject"] = evaluation_subject_id(uni, inv["kind"], r["nativeSubjectId"])

    for key in expected_keys:
        if key not in seen_inv and key not in schema_failed:
            _add(faults, "ENUMERATION_INVENTORY_MISSING_RECORD")

    if faults:
        empty["refusals"] = faults
        return empty

    by_kind = {"file": 0, "symbol": 0, "package": 0}
    collisions = []
    index = []
    for rk, slot in subjects.items():
        by_kind[rk[1]] += 1
        if len(slot["payloads"]) > 1:
            collisions.append({"universe": rk[0], "kind": rk[1], "nativeSubjectId": rk[2],
                               "inventoryRefs": slot["inventoryRefs"]})
        index.append({"universe": rk[0], "kind": rk[1], "nativeSubjectId": rk[2],
                      "evaluationSubject": slot["evaluationSubject"],
                      "inventoryRefs": slot["inventoryRefs"], "state": slot["inventoryRefs"][0]["state"]})
    eval_ids = canon_str_list([s["evaluationSubject"] for s in subjects.values() if s["evaluationSubject"]])
    return {
        "result": "ADMIT",
        "refusals": [],
        "index": sorted(index, key=lambda r: (r["universe"], r["kind"], r["nativeSubjectId"])),
        "population": {"distinct": len(subjects), "byKind": by_kind, "collisions": collisions},
        "evaluationSubjects": eval_ids,
        "subjects": {str(k): v for k, v in subjects.items()},
        "packageProjection": package_proj_by_root,
        "expectedRecords": len(expected_keys),
        "internalFaults": list(INTERNAL_FAULTS),
        "standing": "enumeration-join admission only; not a Run",
    }
