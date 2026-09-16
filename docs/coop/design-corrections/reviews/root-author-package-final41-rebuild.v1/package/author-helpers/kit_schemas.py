"""Load every kit JSON Schema into a Draft 2020-12 referencing Registry."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

KIT = Path(os.environ.get("OPENSIP_AUTHOR_KIT",
                          "/tmp/opensip-design-corrections/consumer-b.v13/subject"))

PREFIX_TO_IDENTITY_DEF = {
    "snapshot2": "snapshot",
    "plan2": "plan",
    "run3": "run",
    "proof3": "proof-bundle",
    "evidence3": "semantic-evidence",
    "seal3": "evaluation-seal",
    "view2": "view",
    "fact2": "fact",
    "coverage2": "coverage",
    "scope2": "subject-scope",
    "import2": "import",
    "closure2": "closure",
    "exec-plan2": "execution-plan",
    "finding3": "finding",
    "subject3": "evaluation-subject",
    "finding-key2": "finding-fingerprint",
    "cache2": "cache-key",
    "regen2": "regeneration-key",
    "policy-derivation3": "policy-derivation",
}

REL_TO_PAYLOAD_DEF = {
    "calls": "CallsPayloadV1",
    "clones": "ClonesPayloadV1",
    "control-flow": "ControlFlowPayloadV1",
    "declares": "DeclaresPayloadV1",
    "file": "FilePayloadV1",
    "imports": "ImportsPayloadV1",
    "literal": "LiteralPayloadV1",
    "package": "PackagePayloadV1",
    "reachability": "ReachabilityPayloadV1",
    "references": "ReferencesPayloadV1",
    "types": "TypesPayloadV1",
    "unresolved-edge": "UnresolvedEdgePayloadV1",
    "vcs-change": "VcsChangePayloadV1",
}


def _load_all() -> list[tuple[str, Path, dict]]:
    out = []
    for p in KIT.rglob("*.json"):
        try:
            d = json.loads(p.read_text())
        except Exception:
            continue
        if isinstance(d, dict) and isinstance(d.get("$id"), str):
            out.append((d["$id"], p, d))
    return out


def build_registry() -> tuple[Registry, dict[str, dict], dict[str, Path]]:
    resources = []
    by_id: dict[str, dict] = {}
    paths: dict[str, Path] = {}
    for sid, p, d in _load_all():
        by_id[sid] = d
        paths[sid] = p
        resources.append((sid, Resource.from_contents(d, default_specification=DRAFT202012)))
    registry = Registry().with_resources(resources)
    return registry, by_id, paths


REGISTRY, SCHEMAS, SCHEMA_PATHS = build_registry()


def identity_schema() -> dict:
    return SCHEMAS["urn:opensip:product-v1:identity:v3"]


def native_schema() -> dict:
    return SCHEMAS["urn:opensip:product-v1:native:evidence-schemas:v2"]


def relation_schema() -> dict:
    return SCHEMAS["opensip.product.relation-payload.2"]


def wrap_def(schema_id: str, def_name: str | None = None) -> dict:
    """A validator schema that $ref's a $defs member (or the document root)."""
    if def_name:
        return {"$ref": f"{schema_id}#/$defs/{def_name}"}
    return {"$ref": schema_id}


def schema_id_for_document(document: str | None) -> str | None:
    """Map a nestedRecords document path or $id onto a registered schema $id."""
    if not document:
        return None
    if document in SCHEMAS:
        return document
    for sid, p in SCHEMA_PATHS.items():
        posix = p.as_posix()
        if posix.endswith("/" + document) or posix.endswith(document):
            return sid
    return None


def load_rel(rel: str) -> dict:
    return json.loads((KIT / rel).read_text())
