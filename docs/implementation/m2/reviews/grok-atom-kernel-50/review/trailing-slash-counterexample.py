"""Demonstrate pinned rust under_prefix vs selected N/_path_in_scope.

Uses native-case15 reference interpreter and actual selected modules.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

FOUND = Path(
    "/tmp/opensip-implementation/m2-reconstruction-subject-48/reference/archroot/docs/coop/design-corrections/foundation"
)
OUT = Path(
    "/tmp/opensip-implementation/m2-grok-atom-kernel-50-advisory/review/trailing-slash-counterexample.json"
)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


A = load("atom_model_v1_selected", FOUND / "atom_model.v1.py")
N = A.N
C = load("identity_canonical", FOUND / "canonical.py")
identity_v2 = json.loads((FOUND / "identity-schemas.v2.json").read_text(encoding="utf-8"))
imported_ev = json.loads(
    (FOUND.parent / "workflows" / "schemas" / "imported-evidence.schema.json").read_text(encoding="utf-8")
)
native_schemas = json.loads(
    (FOUND.parent / "native" / "native-evidence.schemas.v2.json").read_text(encoding="utf-8")
)


def rust_under_prefix(path: str, root: str) -> bool:
    """Pinned atoms.rs under_prefix (lines 93-96)."""
    root = "" if root == "." else root
    return root == "" or path == root or (
        path.startswith(root) and path[len(root) :].startswith("/")
    )


def rust_path_in_scope(scope: dict, path: str) -> bool:
    """Pinned atoms.rs path_in_scope using rust_under_prefix."""
    for e in scope.get("excludedPathPrefixes") or []:
        if rust_under_prefix(path, e):
            return False
    roots = scope.get("workspaceRoots") or []
    if not any(rust_under_prefix(path, r) for r in roots):
        return False
    prefixes = scope.get("pathPrefixes") or []
    if not prefixes:
        return True
    return any(rust_under_prefix(path, p) for p in prefixes)


def schema_ok(schema: dict, inst) -> dict:
    try:
        Draft202012Validator(schema).validate(inst)
        return {"accepted": True}
    except ValidationError as exc:
        return {"accepted": False, "message": exc.message}


def identity_scope_logical_path_refuses(path: str) -> bool:
    """identity-model.v3 payload() extra check for scope-descriptor members."""
    return path != "." and (
        path.startswith("/")
        or "\\" in path
        or "\x00" in path
        or any(v in ["", ".", ".."] for v in path.split("/"))
    )


def main() -> int:
    path = "src/foo"
    root = "src/"
    scope = {
        "schemaVersion": 2,
        "workspaceRoots": [root],
        "pathPrefixes": [],
        "excludedPathPrefixes": [],
    }
    selected = A._path_in_scope(scope, path)
    rust = rust_path_in_scope(scope, path)
    n_unit = N._under_unit(path, root)
    a_prefix = A._under_prefix(path, root)

    prefix_scope = {
        "schemaVersion": 2,
        "workspaceRoots": ["."],
        "pathPrefixes": [root],
        "excludedPathPrefixes": [],
    }
    excluded_scope = {
        "schemaVersion": 2,
        "workspaceRoots": ["."],
        "pathPrefixes": [],
        "excludedPathPrefixes": [root],
    }

    canon_dir = native_schemas["$defs"]["CanonicalRelativeDirV1"]
    text_schema = {"$ref": "#/$defs/Text", "$defs": identity_v2["$defs"]}
    scope_desc = {
        "type": "object",
        "additionalProperties": False,
        "required": ["schemaVersion", "workspaceRoots", "pathPrefixes", "excludedPathPrefixes"],
        "properties": identity_v2["$defs"]["scope-descriptor"]["properties"],
        "$defs": identity_v2["$defs"],
    }
    import_scope = imported_ev["$defs"]["ImportScopeDescriptor"]

    report = {
        "interpreter": sys.executable,
        "version": sys.version,
        "ucd": __import__("unicodedata").unidata_version,
        "jsonschemaStubbed": False,
        "loadsActualAtomModel": True,
        "loadsActualNativeUnderUnit": True,
        "counterexample": {
            "path": path,
            "root": root,
            "selected_path_in_scope": selected,
            "selected_under_prefix": a_prefix,
            "N_under_unit": n_unit,
            "pinned_rust_path_in_scope": rust,
            "pinned_rust_under_prefix": rust_under_prefix(path, root),
            "diverges": selected != rust,
        },
        "sameHelperOnPrefixesAndExclusions": {
            "pathPrefixes_src_slash": {
                "selected": A._path_in_scope(prefix_scope, path),
                "rust": rust_path_in_scope(prefix_scope, path),
            },
            "excludedPathPrefixes_src_slash": {
                "selected": A._path_in_scope(excluded_scope, path),
                "rust": rust_path_in_scope(excluded_scope, path),
            },
        },
        "nonTrailingControl": {
            "root": "src",
            "selected": A._path_in_scope(
                {"schemaVersion": 2, "workspaceRoots": ["src"], "pathPrefixes": [], "excludedPathPrefixes": []},
                path,
            ),
            "rust": rust_path_in_scope(
                {"schemaVersion": 2, "workspaceRoots": ["src"], "pathPrefixes": [], "excludedPathPrefixes": []},
                path,
            ),
        },
        "admission": {
            "atom_model_SCOPE_SCHEMA": schema_ok(A.SCOPE_SCHEMA, scope),
            "identity_schemas_v2_scope_descriptor": schema_ok(scope_desc, scope),
            "imported_evidence_ImportScopeDescriptor": schema_ok(import_scope, scope),
            "identity_schemas_v2_Text_src_slash": schema_ok({"type": "string", "minLength": 1, "maxLength": 4096}, root),
            "native_CanonicalRelativeDirV1_src_slash": schema_ok(canon_dir, root),
            "identity_model_SCOPE_LOGICAL_PATH_would_refuse": identity_scope_logical_path_refuses(root),
            "identity_model_SCOPE_LOGICAL_PATH_split": root.split("/"),
            "atom_import_scope_uses_SCOPE_SCHEMA_only": True,
            "workflow_import_validates_identity_scope_descriptor_schema_not_payload_extra": True,
        },
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["counterexample"], indent=2))
    print("admission", json.dumps(report["admission"], indent=2))
    print("prefix/exclude", json.dumps(report["sameHelperOnPrefixesAndExclusions"], indent=2))
    assert report["counterexample"]["diverges"] is True
    assert selected is True and rust is False
    assert n_unit is True and a_prefix is True
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
