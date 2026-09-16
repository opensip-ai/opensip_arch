"""Native-v2 (consumer24) construction laws for the AUTHOR helpers.

Author-side construction of three published laws, read from the declared kit where the law is machine-readable and
from the normative prose where it is not. This module constructs; it does not admit. The frozen owner named by
--source remains the only admission authority and every export must still pass its structural closure and complete
close_run replay.

* S1 stage output registration (identity-schemas.v3 #/$defs/stage-spec/properties/outputSchemaDigest
  x-opensip-digest.registeredBy): the producer closure carries, at treePath with {operation}, a JSON Schema 2020-12
  document declaring x-opensip-stage-output {schemaVersion 1, operation, outputDomains}; outputSchemaDigest is the raw
  SHA-256 of exactly those member bytes.
* S2 per-level normalization map (identity-schemas.v3 #/x-opensip-digest-domains/normalizationSpecificationLaw): the
  closure that INTERPRETS the body span carries C(normalization-specification-map) at closureTreePath, and every mapped
  level specification is itself a member of that closure's tree.
* U-4b / U-9 deterministic membership (native-evidence.md section 1.4): units sorted by (UTF-8 rootPath, UTF-8
  languageFamily) with index ordinals; rows sorted by UTF-8 path; first-match row decision; projections in row order.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

from . import canonical

KIT = Path(os.environ.get("OPENSIP_AUTHOR_KIT", ""))
_IDENTITY = json.loads((KIT / "docs/coop/design-corrections/foundation/identity-schemas.v3.json").read_text())
_REGISTERED_BY = (_IDENTITY["$defs"]["stage-spec"]["properties"]["outputSchemaDigest"]["x-opensip-digest"]["registeredBy"])
_NORMALIZATION_LAW = _IDENTITY["x-opensip-digest-domains"]["normalizationSpecificationLaw"]
STAGE_OUTPUT_TREE_PATH = _REGISTERED_BY["treePath"]
STAGE_OUTPUT_DECLARATION = _REGISTERED_BY["declaration"]
_OPERATION_SEGMENT = re.compile(_REGISTERED_BY["operationSegment"].replace("(?![\\s\\S])", "") + r"\Z")
NORMALIZATION_MAP_PATH = _NORMALIZATION_LAW["closureTreePath"]
NORMALIZATION_LEVELS = ("L0-verbatim", "L1-lexical", "L2-comment-insensitive", "L3-identifier-insensitive")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ------------------------------------------------------------------------------------------------ S1
def stage_output_member(operation: str, output_domains) -> tuple[str, bytes]:
    """(tree path, exact document bytes) the producer closure registers for one operation."""
    if not isinstance(operation, str) or not _OPERATION_SEGMENT.match(operation):
        raise ValueError("stage operation is not one registered path segment: %r" % (operation,))
    domains = sorted(set(output_domains), key=lambda d: d.encode("utf-8"))
    document = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "urn:opensip:author:stage-output:" + operation,
        "title": "Author synthetic stage output: " + operation,
        "type": "object",
        "additionalProperties": False,
        "required": ["outputRefs"],
        "properties": {"outputRefs": {"type": "array", "items": {"type": "object"}}},
        STAGE_OUTPUT_DECLARATION: {"schemaVersion": 1, "operation": operation, "outputDomains": domains},
    }
    return STAGE_OUTPUT_TREE_PATH.replace("{operation}", operation), canonical.encode(document)


def stage_output_schema_digest(operation: str, output_domains) -> str:
    return sha(stage_output_member(operation, output_domains)[1])


def stage_output_members(registrations) -> dict[str, bytes]:
    """{tree path: bytes} for [(operation, outputDomains), ...]; one operation must have one declaration."""
    members = {}
    for operation, domains in registrations:
        path, data = stage_output_member(operation, domains)
        if path in members and members[path] != data:
            raise ValueError("operation %r registered with two different output declarations" % operation)
        members[path] = data
    return members


# ------------------------------------------------------------------------------------------------ S2
def normalization_members(normalizer_id: str, level_specs: dict[str, bytes], *, map_levels=None,
                          include_map=True, spec_directory="normalizers/levels/") -> dict[str, bytes]:
    """Tree members for a body-interpreting closure: each level specification file plus the per-level map.

    `map_levels` defaults to exactly `level_specs`; a control may name a different {level: digest} mapping (for a
    discrimination Run) and `include_map=False` omits the map. Nothing here admits the result."""
    for level in level_specs:
        if level not in NORMALIZATION_LEVELS:
            raise ValueError("unknown normalisation level %r" % level)
    members = {spec_directory + level + ".spec": data for level, data in level_specs.items()}
    if include_map:
        mapping = map_levels if map_levels is not None else {level: sha(data) for level, data in level_specs.items()}
        record = {"schemaVersion": 1, "normalizerId": normalizer_id,
                  "levels": [{"level": level, "specificationDigest": mapping[level]}
                             for level in sorted(mapping, key=lambda x: x.encode("utf-8"))]}
        members[NORMALIZATION_MAP_PATH] = canonical.encode(record)
    return members


# ------------------------------------------------------------------------------------------------ U-4b / U-9
RUST_SUFFIXES = (".rs",)
TSJS_SUFFIXES = (".ts", ".tsx", ".mts", ".cts", ".js", ".mjs", ".cjs", ".jsx")
BUNDLED_GRAMMAR_EXTENSIONS = (".rs", ".ts", ".tsx", ".mts", ".cts", ".js", ".mjs", ".cjs", ".jsx",
                              ".json", ".toml", ".md", ".yaml", ".yml")
DEPENDENCY_SEGMENTS = ("node_modules",)
VCS_SEGMENTS = (".git", ".hg", ".svn", ".jj")


def unit(root, family, mode, kind, marker_path, marker_sha, *, recognizer_id, provenance="DISCOVERED",
         member_package_roots=()):
    """WorkspaceUnitV2 without its ordinal (membership() assigns it)."""
    return {"rootPath": root, "languageFamily": family, "languageMode": mode, "unitKind": kind,
            "markerPath": marker_path, "markerSha256": marker_sha, "recognizerId": recognizer_id,
            "recognizerVersion": 1, "provenance": provenance,
            "memberPackageRoots": sorted(set(member_package_roots), key=lambda s: s.encode("utf-8"))}


def syntax_only_fallback_unit():
    """U-9: the single zero-config unit of a marker-free project."""
    return unit("", "none", "syntax-only", "syntax-only", "", None, recognizer_id="syntax-only-fallback",
                provenance="DEFAULTED")


def _family(path):
    if path.endswith(RUST_SUFFIXES):
        return "rust"
    if path.endswith(TSJS_SUFFIXES):
        return "tsjs"
    return "none"


def _final_extension(path):
    name = path.rsplit("/", 1)[-1]
    return name[name.rfind("."):] if "." in name else ""


def _under(path, root):
    return root == "" or path == root or path.startswith(root + "/")


def _pruned(path, cargo_roots):
    parts = path.split("/")
    for i, seg in enumerate(parts):
        if seg in DEPENDENCY_SEGMENTS or seg in VCS_SEGMENTS:
            return True
    for i, seg in enumerate(parts):
        if seg == "target" and "/".join(parts[:i]) in cargo_roots:
            return True
    return False


def membership(units, paths):
    """UnitMembershipV1 per U-4b: order, ordinals, first-match row decision and row-order projections."""
    ordered = sorted((dict(u) for u in units), key=lambda u: (u["rootPath"].encode("utf-8"), u["languageFamily"].encode("utf-8")))
    for index, u in enumerate(ordered):
        u["unitOrdinal"] = index
    keys = [(u["rootPath"], u["languageFamily"]) for u in ordered]
    if len(set(keys)) != len(keys):
        raise ValueError("two units share (rootPath, languageFamily)")
    cargo_roots = {u["rootPath"] for u in ordered if u["languageFamily"] == "rust"}
    cargo_roots |= {m for u in ordered if u["languageFamily"] == "rust" for m in u["memberPackageRoots"]}
    rows = []
    for path in sorted(set(paths), key=lambda p: p.encode("utf-8")):
        family = _family(path)
        if _pruned(path, cargo_roots):
            rows.append({"path": path, "languageFamily": family, "unitOrdinal": None, "membership": "syntax-only", "reason": "host-ignore-convention"})
            continue
        if family == "none":
            if _final_extension(path) in BUNDLED_GRAMMAR_EXTENSIONS:
                rows.append({"path": path, "languageFamily": "none", "unitOrdinal": None, "membership": "syntax-only", "reason": "grammar-only"})
            else:
                rows.append({"path": path, "languageFamily": "none", "unitOrdinal": None, "membership": "unsupported-file", "reason": "no-bundled-grammar"})
            continue
        candidates = [u for u in ordered if u["languageFamily"] == family and _under(path, u["rootPath"])]
        if not candidates:
            rows.append({"path": path, "languageFamily": family, "unitOrdinal": None, "membership": "syntax-only", "reason": "no-program-unit-for-language"})
            continue
        deepest = max(candidates, key=lambda u: len(u["rootPath"]))
        rows.append({"path": path, "languageFamily": family, "unitOrdinal": deepest["unitOrdinal"], "membership": "program-member", "reason": "deepest-unit-in-language"})
    return {"schemaVersion": 1, "units": ordered, "rows": rows,
            "unsupportedFiles": [r["path"] for r in rows if r["membership"] == "unsupported-file"],
            "outsideBoundaryFiles": [], "erasedFiles": []}
