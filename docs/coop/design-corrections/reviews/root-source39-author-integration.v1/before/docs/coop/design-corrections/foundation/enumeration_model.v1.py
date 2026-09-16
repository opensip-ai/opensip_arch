"""Enumeration plan/inventory reference admission (design evidence, not a host runtime).

Preconditions: plan, analysis_spec, scope_descriptor, membership, native context
descriptors, universe resolved-input descriptors, and closure kind map are already
owner-admitted. This module does not call admit_native_context, bind_*, or symbol
extraction, and does not re-hash native universe H (that is the native owner's
admission). ADMIT is enumeration-join admission only — not a Run.

evaluation-subject uses identity-model.v3 identifier (PREFIX already maps
evaluation-subject → subject3). Kind package additionally requires
packageManifestPath (M3). Plan/inventory records do not store that descriptor.
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
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
ENGINE = IM.DIGESTS["languageModes"]["map"]
UNIVERSE_DOMAIN = {
    mode: "native.semantic-universe." + engine + ".v2"
    for mode, engine in ENGINE.items()
    if engine is not None
}
TS_MODES = ("ts-tsconfig", "js-allowjs", "js-synthesized")
CANDIDATE_CAPS = frozenset({"clones-near", "clones-cross-tsjs"})

SUBJECT_ID_RE = re.compile(r"^[a-z][a-z0-9-]*:[^\u0000-\u001f\u007f-\u009f]+$")
LOGICAL_PATH_RE = re.compile(r"^[^/\\\u0000]{1,255}(/[^/\\\u0000]{1,255})*$")
CODE_SUFFIX = (".ts", ".tsx", ".mts", ".cts", ".js", ".jsx", ".mjs", ".cjs", ".rs")
LOCAL_DEFICIENCY = "source-syntax-invalid"

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
    "ENUMERATION_CANDIDATE_SOURCE_PATHS",
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
    "ENUMERATION_MEMBERSHIP_UNIT_ROOT",
    "ENUMERATION_SCOPE_WORKSPACE_ROOT",
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


def evaluation_subject_id(universe: str, kind: str, native_subject_id: str, package_manifest_path=None) -> str:
    desc = {"schemaVersion": 3, "universe": universe, "kind": kind, "nativeSubjectId": native_subject_id}
    if kind == "package":
        if type(package_manifest_path) is not str or not package_manifest_path:
            raise AdmissionError("ENUMERATION_ADMISSION_PRECONDITION")
        desc["packageManifestPath"] = package_manifest_path
    elif package_manifest_path is not None:
        raise AdmissionError("ENUMERATION_ADMISSION_PRECONDITION")
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
        return False
    for ex in excluded:
        if _under(path, _internal_root(ex) if ex != "." else ""):
            return False
    prefixes = scope.get("pathPrefixes") or []
    if not prefixes:
        return True
    return any(_under(path, "" if p == "." else p) for p in prefixes)


def _workspace_root_under_scope(cell_root: str, scope: dict) -> bool:
    selected = scope.get("workspaceRoots") or []
    cell_int = _internal_root(cell_root)
    for wr in selected:
        wr_int = _internal_root(wr)
        if wr_int == "":
            return True
        if cell_int == wr_int or (cell_int != "" and _under(cell_int, wr_int)):
            return True
    return False


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
    if deficiency == LOCAL_DEFICIENCY:
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
        if row is None:
            _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
            continue
        if _excluded_row(row):
            continue
        out.append(path)
    return canon_str_list(out)


def host_file_extent(membership, snapshot_paths, scope, workspace_root, faults) -> list[str]:
    """Inventory exemption: all scoped first-party paths, including data/unsupported/Cargo.toml."""
    return _first_party_scoped(membership, snapshot_paths, scope, workspace_root, faults)


def host_symbol_extent(membership, snapshot_paths, scope, workspace_root, language_mode, universe, retained, faults) -> list[str]:
    """Compiler/syntax selected program scope from owner-admitted resolved inputs, not default membership.

    Unknown program (no universe record): membership-fallback code extent, never caller paths.
    """
    scoped = set(_first_party_scoped(membership, snapshot_paths, scope, workspace_root, faults))
    by_path = {r["path"]: r for r in membership["rows"]}

    def fallback() -> list[str]:
        out = []
        for p in scoped:
            row = by_path.get(p)
            if row is None or not p.endswith(CODE_SUFFIX):
                continue
            if language_mode == "syntax-only":
                out.append(p)
            elif row.get("membership") == "program-member":
                out.append(p)
        return canon_str_list(out)

    if not isinstance(universe, dict):
        return fallback()
    if language_mode == "syntax-only":
        return canon_str_list([p for p in scoped if p.endswith(CODE_SUFFIX)])
    if language_mode in TS_MODES:
        if "programRootFiles" not in universe:
            _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
            return []
        roots = universe["programRootFiles"]
        if not isinstance(roots, list):
            _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
            return []
        out = []
        for p in roots:
            if p not in snapshot_paths or p not in scoped:
                _add(faults, "ENUMERATION_BINDING_EXTENT_PATHS")
                continue
            if p.endswith(CODE_SUFFIX):
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
            p = rel.get("path")
            if rel.get("unitId") in selected and p in scoped:
                out.append(p)
        return canon_str_list(out)
    return []


def _manifest_bytes(path, source_blobs, faults, snapshot_blob_index=None):
    if not isinstance(source_blobs, dict):
        _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
        return None
    if path not in source_blobs:
        _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
        return None
    blob = source_blobs[path]
    if type(blob) is not bytes:
        _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
        return None
    if snapshot_blob_index is not None:
        row = snapshot_blob_index.get(path)
        if not isinstance(row, dict):
            _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
            return None
        sha = row.get("sha256")
        nbytes = row.get("bytes")
        if type(sha) is not str or type(nbytes) is not int:
            _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
            return None
        if hashlib.sha256(blob).hexdigest() != sha or len(blob) != nbytes:
            _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
            return None
    return blob


def project_named_packages(snapshot_paths, scope, workspace_root, membership, source_blobs, faults,
                           snapshot_blob_index=None) -> dict:
    """Host projection from retained snapshot bytes. Not a caller oracle list.

    Candidate package extent = named manifest paths UNION parse/classification failures.
    Known nameless / workspace-only manifests are not subjects and are not in the candidate
    extent. Missing bytes are a structural retention/precondition refusal, not syntax-invalid.
    """
    scoped = _first_party_scoped(membership, snapshot_paths, scope, workspace_root, faults)
    named, unnamed, failed = [], [], []
    for path in scoped:
        name = path.rsplit("/", 1)[-1]
        if name not in ("package.json", "Cargo.toml"):
            continue
        blob = _manifest_bytes(path, source_blobs, faults, snapshot_blob_index)
        if blob is None:
            continue
        if name == "package.json":
            try:
                data = C.parse(blob)
            except AdmissionError:
                failed.append({"path": path, "reason": "syntax"})
                continue
            if type(data) is not dict:
                failed.append({"path": path, "reason": "classification"})
                continue
            if "name" not in data:
                unnamed.append({"path": path, "reason": "no-name"})
                continue
            pkg = data["name"]
            if type(pkg) is str and pkg:
                named.append({"path": path, "packageName": pkg, "format": "json"})
            else:
                failed.append({"path": path, "reason": "classification"})
        else:
            try:
                data = tomllib.load(io.BytesIO(blob))
            except tomllib.TOMLDecodeError:
                failed.append({"path": path, "reason": "syntax"})
                continue
            if type(data) is not dict:
                failed.append({"path": path, "reason": "classification"})
                continue
            pkg = data.get("package") if "package" in data else None
            if pkg is None:
                unnamed.append({"path": path, "reason": "workspace-only" if "workspace" in data else "no-name"})
                continue
            if type(pkg) is not dict:
                failed.append({"path": path, "reason": "classification"})
                continue
            if "name" not in pkg:
                unnamed.append({"path": path, "reason": "workspace-only" if "workspace" in data else "no-name"})
                continue
            pkg_name = pkg["name"]
            if type(pkg_name) is str and pkg_name:
                named.append({"path": path, "packageName": pkg_name, "format": "toml"})
            else:
                failed.append({"path": path, "reason": "classification"})
    named.sort(key=lambda r: C.canonical(r["path"]))
    named_paths = canon_str_list([r["path"] for r in named])
    failed_paths = canon_str_list([r["path"] for r in failed])
    return {
        "named": named,
        "unnamed": unnamed,
        "parseFailed": failed,
        "namedPaths": named_paths,
        "candidatePaths": canon_str_list(named_paths + failed_paths),
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


def _population_key(universe, kind, native_id, path):
    if kind == "package":
        return (universe, kind, native_id, path)
    return (universe, kind, native_id)


def _snapshot_index(snapshot_inventory, snapshot_paths, faults):
    """Full snapshot_inventory is host TCB Blob rows. snapshot_paths-only is standalone fixture."""
    if snapshot_inventory is None:
        if snapshot_paths is None:
            _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
            return [], None, "missing"
        if not isinstance(snapshot_paths, list) or any(type(p) is not str for p in snapshot_paths):
            _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
            return [], None, "standalone"
        return snapshot_paths, None, "standalone"
    if type(snapshot_inventory) is not list:
        _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
        return snapshot_paths or [], None, "full"
    derived = []
    by_path = {}
    for row in snapshot_inventory:
        if type(row) is not dict:
            _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
            continue
        path, sha, nbytes = row.get("path"), row.get("sha256"), row.get("bytes")
        if type(path) is not str or type(sha) is not str or type(nbytes) is not int:
            _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
            continue
        if path in by_path:
            _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
            continue
        derived.append(path)
        by_path[path] = row
    if snapshot_paths is not None and snapshot_paths != derived:
        _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
    return derived, by_path, "full"


def _membership_covers_snapshot(membership, snapshot_paths, faults) -> None:
    if not isinstance(membership, dict) or not isinstance(membership.get("rows"), list):
        _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
        return
    paths = []
    for row in membership["rows"]:
        if type(row) is not dict or type(row.get("path")) is not str:
            _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
            return
        paths.append(row["path"])
    if len(paths) != len(set(paths)) or set(paths) != set(snapshot_paths):
        _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")


def _admit_membership_unit_roots(membership, faults: list[str]) -> bool:
    """Decide the INTERNAL root representation of the membership units BEFORE any binding join.

    The single authority is the native selector (NV.admit_unit_roots, reading
    #/$defs/InternalUnitRootV1 and #/$defs/CanonicalRelativeDirV1); this function only translates
    that decision into this model's internal fault vocabulary. Without it, a unit whose root is
    spelled with the EXTERNAL sentinel '.' reaches _unit_for_cell, which then matches no unit, so
    _u1_entry derives None and the mismatch against the retained
    TypeScriptConfigGraphV1.entryConfigPath is reported as ENUMERATION_BINDING_PROGRAM_ENTRY: a
    real refusal attributed to the wrong field. ENUMERATION_MEMBERSHIP_UNIT_ROOT is an INTERNAL
    fault key only; it adds no public D9 code and no public route.
    """
    units = membership.get('units') if isinstance(membership, dict) else None
    if units is None:
        return True
    try:
        NV.admit_unit_roots(units)
    except NV.AdmissionError:
        _add(faults, 'ENUMERATION_MEMBERSHIP_UNIT_ROOT')
        return False
    return True


def admit_enumeration(
    *,
    plan: dict,
    plan_id: str,
    analysis_spec: dict,
    scope_descriptor: dict,
    membership: dict,
    enumeration_plan: dict,
    inventories: list,
    native_contexts: dict,
    universes: dict,
    closures: dict,
    universe_domains: dict,
    snapshot_inventory: list | None = None,
    snapshot_paths: list | None = None,
    source_blobs: dict | None = None,
    retained_inputs: dict | None = None,
    membership_derivation: dict | None = None,
    policy_document: dict | None = None,
) -> dict:
    """Join-admit inventories against Plan-bound expected population.

    universes/native_contexts maps: actual owner-admitted descriptors keyed by
    bare H suffix. universe_domains: same keys to owner H class
    native.semantic-universe.<engine>.v2 from the M3 closure. No bindResult
    flags. source_blobs: path -> exact snapshot bytes for package projection.
    retained_inputs[universe]: {configGraph?, sourceUnitOwnership?} nested
    owner records. snapshot_inventory is the full Blob inventory (sha/bytes
    checked for used manifests). snapshot_paths-only is a standalone fixture.
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

    if not isinstance(universe_domains, dict):
        empty["refusals"] = ["ENUMERATION_ADMISSION_PRECONDITION"]
        return empty

    snapshot_paths, snapshot_blob_index, snap_mode = _snapshot_index(
        snapshot_inventory, snapshot_paths, faults
    )
    if not snapshot_paths and "ENUMERATION_ADMISSION_PRECONDITION" in faults and snap_mode == "missing":
        empty["refusals"] = faults
        return empty

    if not _admit_membership_unit_roots(membership, faults):
        empty["refusals"] = faults
        return empty

    _membership_covers_snapshot(membership, snapshot_paths, faults)

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
            else:
                bounds = membership_derivation.get("boundaries")
                if membership_derivation["mode"] == "operational" and not isinstance(bounds, dict):
                    _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
                else:
                    if membership_derivation["mode"] == "standalone-fixture":
                        bounds = membership_derivation.get("boundaries")
                    try:
                        disc = NV.discover_units(
                            membership_derivation["markers"],
                            membership_derivation.get("explicit_workspace_roots"),
                            bounds,
                        )
                    except (NV.AdmissionError, AdmissionError, ValidationError):
                        _add(faults, "ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION")
                    else:
                        if disc.get("refused"):
                            _add(faults, "ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION")
                        else:
                            try:
                                recomputed = NV.assign_membership(
                                    disc["units"], membership_derivation["files"], bounds
                                )
                            except (NV.AdmissionError, AdmissionError, ValidationError):
                                _add(faults, "ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION")
                            else:
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
        if not _workspace_root_under_scope(cell["workspaceRoot"], scope_descriptor):
            _add(faults, "ENUMERATION_SCOPE_WORKSPACE_ROOT")
        if len(cell["programBindings"]) > 128:
            _add(faults, "ENUMERATION_PLAN_PROGRAM_BINDINGS_OVERFLOW")
        defaults = [b for b in cell["programBindings"] if b.get("provenance") == "default-unit"]
        if len(defaults) > 1 or (defaults and defaults[0]["ordinal"] != 0):
            _add(faults, "ENUMERATION_PLAN_DEFAULT_UNIT")
        seen_u = []
        root_key = cell["workspaceRoot"]
        if root_key not in package_proj_by_root and needs_package:
            package_proj_by_root[root_key] = project_named_packages(
                snapshot_paths, scope_descriptor, root_key, membership, source_blobs, faults,
                snapshot_blob_index=snapshot_blob_index if snap_mode == "full" else None,
            )
        file_ext = host_file_extent(membership, snapshot_paths, scope_descriptor, cell["workspaceRoot"], faults)
        fp_set = set(file_ext)
        pkg_proj = package_proj_by_root.get(root_key)
        pkg_ext = pkg_proj["candidatePaths"] if pkg_proj else []
        for b in cell["programBindings"]:
            en = b["enumerator"] if isinstance(b.get("enumerator"), dict) else {}
            ctx = b.get("nativeContextDigest")
            uni = b.get("universe")
            available = uni is not None
            status = en.get("status")
            if status == "unselected":
                if en.get("reason") != "optional-unselected":
                    _add(faults, "ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR")
                if cell.get("required") is True or available:
                    _add(faults, "ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR")
            elif status == "selected":
                if not en.get("closureId"):
                    _add(faults, "ENUMERATION_BINDING_ENUMERATOR_NOT_IN_PLAN")
                elif en["closureId"] not in plan["semanticClosures"] or en["closureId"] not in closures:
                    _add(faults, "ENUMERATION_BINDING_ENUMERATOR_NOT_IN_PLAN")
                elif closures[en["closureId"]].get("kind") != "provider":
                    _add(faults, "ENUMERATION_BINDING_ENUMERATOR_KIND")
            else:
                _add(faults, "ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR")
            if ctx is not None:
                if ctx not in plan["nativeContextDigests"] or ctx not in native_contexts:
                    _add(faults, "ENUMERATION_BINDING_CONTEXT_NOT_IN_PLAN")
            ext_kinds = canon_str_list([e["kind"] for e in b["extents"]])
            if not C.equal_typed(ext_kinds, expected_kinds):
                _add(faults, "ENUMERATION_BINDING_EXTENT_KINDS")
            csp = b.get("candidateSourcePaths")
            if cell["capabilityId"] in CANDIDATE_CAPS:
                if not isinstance(csp, list) or not C.equal_typed(csp, canon_str_list([p for p in csp if isinstance(p, str)])):
                    _add(faults, "ENUMERATION_CANDIDATE_SOURCE_PATHS")
                else:
                    for p in csp:
                        if p not in snapshot_paths or p not in fp_set:
                            _add(faults, "ENUMERATION_CANDIDATE_SOURCE_PATHS")
            elif csp is not None:
                _add(faults, "ENUMERATION_CANDIDATE_SOURCE_PATHS")
            urec = {}
            nested = {}
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
                expected_domain = UNIVERSE_DOMAIN.get(cell["languageMode"])
                actual_domain = universe_domains.get(uni)
                if expected_domain is None or actual_domain != expected_domain:
                    _add(faults, "ENUMERATION_BINDING_ENGINE_DOMAIN")
                if cell["languageMode"] in TS_MODES:
                    if urec.get("languageMode") != cell["languageMode"]:
                        _add(faults, "ENUMERATION_BINDING_ENGINE_DOMAIN")
                    ctxrec = native_contexts.get(ctx) if ctx else None
                    if isinstance(ctxrec, dict) and ctxrec.get("languageMode") not in (None, cell["languageMode"]):
                        _add(faults, "ENUMERATION_BINDING_ENGINE_DOMAIN")
                nested = retained_inputs.get(uni) or {}
                entry = b.get("programEntry")
                if entry is not None:
                    if not _logical_path(entry) or entry not in snapshot_paths:
                        _add(faults, "ENUMERATION_BINDING_PROGRAM_ENTRY")
                    if b.get("provenance") == "default-unit":
                        _add(faults, "ENUMERATION_BINDING_PROGRAM_ENTRY")
                mode = cell["languageMode"]
                if mode in TS_MODES:
                    graph = nested.get("configGraph")
                    if graph is None:
                        _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
                    else:
                        derived = _u1_entry(_unit_for_cell(membership, cell["workspaceRoot"], mode), mode)
                        expected_entry = entry if entry is not None else derived
                        if graph.get("entryConfigPath") != expected_entry:
                            _add(faults, "ENUMERATION_BINDING_PROGRAM_ENTRY")
            else:
                _carrier(b.get("deficiency"), b.get("nativeCause"), faults)
                if b.get("deficiency") is None:
                    _add(faults, "ENUMERATION_BINDING_CAUSE")
                entry = b.get("programEntry")
                if entry is not None and (not _logical_path(entry) or entry not in snapshot_paths):
                    _add(faults, "ENUMERATION_BINDING_PROGRAM_ENTRY")
            if available and "symbol" in expected_kinds:
                sym_ext = host_symbol_extent(
                    membership, snapshot_paths, scope_descriptor, cell["workspaceRoot"],
                    cell["languageMode"], urec, nested, faults,
                )
            elif "symbol" in expected_kinds:
                sym_ext = host_symbol_extent(
                    membership, snapshot_paths, scope_descriptor, cell["workspaceRoot"],
                    cell["languageMode"], None, None, faults,
                )
            else:
                sym_ext = []
            derived_ext = {"file": file_ext, "symbol": sym_ext, "package": pkg_ext}
            for e in b["extents"]:
                for p in e["paths"]:
                    if p not in snapshot_paths or p not in fp_set:
                        _add(faults, "ENUMERATION_BINDING_EXTENT_PATHS")
                if not C.equal_typed(e["paths"], derived_ext.get(e["kind"], [])):
                    _add(faults, "ENUMERATION_BINDING_EXTENT_PATHS")
            host_by[(cells.index(cell), b["ordinal"])] = derived_ext
        for b in cell["programBindings"]:
            for kind in cell["kinds"]:
                ci = cells.index(cell)
                expected_keys.append((ci, b["ordinal"], kind))
                binding_by[(ci, b["ordinal"], kind)] = (cell, b)

    seen_inv = {}
    schema_failed = set()
    subjects = {}
    if not isinstance(inventories, list):
        _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")
        inventories = []
    for inv in inventories:
        if type(inv) is not dict:
            _add(faults, "ENUMERATION_INVENTORY_SCHEMA")
            continue
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
        parse_bad = bool(pkg_proj and pkg_proj["parseFailed"])
        if inv["kind"] == "package" and pkg_proj and uni is not None:
            if parse_bad:
                if inv["state"] != "partial" or inv.get("deficiency") != LOCAL_DEFICIENCY:
                    _add(faults, "ENUMERATION_PACKAGE_PARSE")
            elif inv.get("deficiency") == LOCAL_DEFICIENCY:
                _add(faults, "ENUMERATION_PACKAGE_PARSE")
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
        if inv["kind"] == "package" and pkg_proj:
            named_set = set(pkg_proj["namedPaths"])
            row_paths = set(r["path"] for r in inv["rows"])
            if inv["state"] == "complete" and row_paths != extent_set:
                _add(faults, "ENUMERATION_INVENTORY_PACKAGE_TOTALITY")
            if parse_bad and uni is not None:
                if not named_set <= row_paths or not named_set <= set(examined):
                    _add(faults, "ENUMERATION_PACKAGE_PARSE")
            by_path = {n["path"]: n["packageName"] for n in pkg_proj["named"]}
            for r in inv["rows"]:
                expected_name = by_path.get(r["path"])
                if expected_name is None or r["nativeSubjectId"] != expected_name or r["qualifiedName"] != expected_name:
                    _add(faults, "ENUMERATION_INVENTORY_PACKAGE_NAME")
                if r["path"] not in named_set:
                    _add(faults, "ENUMERATION_INVENTORY_PACKAGE_NAME")
        ids = []
        paths = []
        inv_digest = raw_digest(inv)
        for row_i, r in enumerate(inv["rows"]):
            if r["kind"] != inv["kind"]:
                _add(faults, "ENUMERATION_INVENTORY_ROW_PATH")
            if r["path"] not in extent_set or r["path"] not in examined:
                _add(faults, "ENUMERATION_INVENTORY_ROW_PATH")
            if r["path"] not in snapshot_paths:
                _add(faults, "ENUMERATION_INVENTORY_EXTERNAL_PATH")
            if inv["kind"] != "package":
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
                rk = _population_key(uni, inv["kind"], r["nativeSubjectId"], r["path"])
                loc = {
                    "cellOrdinal": inv["cellOrdinal"],
                    "programOrdinal": inv["programOrdinal"],
                    "kind": inv["kind"],
                    "state": inv["state"],
                    "planId": inv["planId"],
                    "parameterDigest": inv["parameterDigest"],
                    "inventoryDigest": inv_digest,
                    "rowIndex": row_i,
                }
                payload = {k: r[k] for k in r}
                slot = subjects.setdefault(rk, {"payloads": [], "inventoryRefs": [], "evaluationSubject": None,
                                               "universe": uni, "kind": inv["kind"],
                                               "nativeSubjectId": r["nativeSubjectId"],
                                               "packageManifestPath": r["path"] if inv["kind"] == "package" else None})
                slot["inventoryRefs"].append(loc)
                if slot["payloads"] and not any(C.equal_typed(prev, payload) for prev in slot["payloads"]):
                    _add(faults, "ENUMERATION_INVENTORY_RECONCILE")
                if not any(C.equal_typed(prev, payload) for prev in slot["payloads"]):
                    slot["payloads"].append(payload)
                if slot["evaluationSubject"] is None:
                    try:
                        slot["evaluationSubject"] = evaluation_subject_id(
                            uni, inv["kind"], r["nativeSubjectId"],
                            r["path"] if inv["kind"] == "package" else None,
                        )
                    except (AdmissionError, ValidationError):
                        _add(faults, "ENUMERATION_ADMISSION_PRECONDITION")

    for key in expected_keys:
        if key not in seen_inv and key not in schema_failed:
            _add(faults, "ENUMERATION_INVENTORY_MISSING_RECORD")

    if faults:
        empty["refusals"] = faults
        return empty

    by_kind = {"file": 0, "symbol": 0, "package": 0}
    index = []
    subjects_out = {}
    for rk, slot in subjects.items():
        by_kind[slot["kind"]] += 1
        states = [ref["state"] for ref in slot["inventoryRefs"]]
        if states and all(s == "complete" for s in states):
            agg = "complete"
        elif "partial" in states:
            agg = "partial"
        else:
            agg = states[0] if states else "unavailable"
        sid = slot["evaluationSubject"]
        item = {
            "evaluationSubject": sid,
            "universe": slot["universe"],
            "kind": slot["kind"],
            "nativeSubjectId": slot["nativeSubjectId"],
            "inventoryRefs": slot["inventoryRefs"],
            "state": agg,
        }
        if slot["kind"] == "package":
            item["packageManifestPath"] = slot["packageManifestPath"]
        index.append(item)
        subjects_out[sid] = {
            **item,
            "payloads": slot["payloads"],
        }
    eval_ids = canon_str_list([s["evaluationSubject"] for s in index if s["evaluationSubject"]])
    return {
        "result": "ADMIT",
        "refusals": [],
        "index": sorted(index, key=lambda r: C.canonical(r["evaluationSubject"])),
        "population": {"distinct": len(subjects), "byKind": by_kind, "collisions": []},
        "evaluationSubjects": eval_ids,
        "subjects": subjects_out,
        "packageProjection": package_proj_by_root,
        "expectedRecords": len(expected_keys),
        "internalFaults": list(INTERNAL_FAULTS),
        "standing": "enumeration-join admission only; not a Run",
    }
