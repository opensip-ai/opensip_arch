#!/usr/bin/env python3
"""Retained executable checker for the fact-plane contract (C-1 made buildable).

C-1 sealed a PRINCIPLE — sufficiency is predicate-relative, no global tier
ordering. A principle cannot be built against, so this checks the contract that
implements it, and specifically checks the two things most likely to be got wrong:

  * that no GLOBAL ordering sneaks back in (F6, F7). The natural way to write a
    "minimum resolution" field is a global ladder, which contradicts C-1 outright.
  * that a one-rung relation is satisfied OUTRIGHT (F8). "A syntax fact is
    authoritative, not a degraded semantic fact" is C-1's central claim; F8 is
    the only place it becomes mechanical rather than rhetorical.

F9 reads the LIVE D9 artifact rather than restating its vocabulary, so a
fact-plane deficiency that D9 cannot express is caught at the seam instead of
becoming a Coverage state with no way to terminate.

  F1  fact envelope is fully declared, and forbids global-judgment fields
  F2  every relation has a non-empty duplicate-free ladder
  F3  every requirement's minResolution is a rung of its own relation's ladder
  F4  sufficiency yields exactly one deficiency when unsatisfied, none when satisfied
  F5  completeness=complete is never satisfied by coverage=unknown
  F6  no resolution value is comparable across relations
  F7  layers carry no rank and are never ordered
  F8  top rung of a one-rung ladder is satisfied outright, never with a deficiency
  F9  deficiency vocabulary is a subset of D9's deficiency enum (live cross-check)
  F10 profiles may raise a floor, never lower one; labels do not materialise
  F11 derived relations require their dependencies at the declared rungs

Usage: python3 artifacts/check-fact-plane.py [contract]   ·   --selftest
Exit:  0 clean · 1 findings · 2 IO error
"""
from __future__ import annotations
import copy, hashlib, json, re, struct, sys, pathlib, unicodedata

BINDING = "fact-plane.v1.json"
D9 = "d9-exit-contract.v1.6.json"
RESOLVED_INPUTS = "resolved-inputs.v2.json"
FORBIDDEN_ENVELOPE = {"quality", "tier", "degraded", "rank"}
REQUIRED_ENVELOPE = {
    "factId", "snapshotId", "relation", "layer", "producer",
    "producerVersion", "schemaVersion", "resolution", "confidence",
}
OPTIONAL_ENVELOPE = {"span", "language"}
# declared precedence: most specific actionable remedy first
PRECEDENCE = ["language-tier-unsupported", "provider-unavailable",
              "budget-exhausted", "confidence-floor-unmet",
              "required-relation-missing"]
REASON_TO_DEFICIENCY = {"language-tier": "language-tier-unsupported",
                        "provider-not-installed": "provider-unavailable",
                        "budget": "budget-exhausted"}
REQUEST_ID_RE = re.compile(r"^req1_[0-9a-f]{32}$")
SNAPSHOT_ID_RE = re.compile(r"^snap1:sha256:[0-9a-f]{64}$")
FACT_ID_RE = re.compile(r"^fact:sha256:[0-9a-f]{64}$")
SHA256_TEXT_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
SUBJECT_NAMESPACE_RE = re.compile(r"^[a-z][a-z0-9-]*$")
PROVIDER_PROFILES = [
    {"providerId": "rust-semantic", "language": "rust"},
    {"providerId": "typescript-semantic", "language": "typescript"},
]
CANDIDATE_FIELDS = {
    "candidateOrdinal", "relation", "resolution", "layer", "producer",
    "producerVersion", "schemaVersion", "language", "sourceUniverseId",
    "targetUniverseId", "confidenceMillionths", "relationSchemaId",
    "canonicalRelationPayload", "anchors",
}
VECTOR_CANDIDATE_FIELDS = (CANDIDATE_FIELDS - {"canonicalRelationPayload"}) | {
    "canonicalRelationPayloadHex", "decodedRelationPayload",
}
TOTALITY_ROOT_CASES = (
    ("string", "hostile-root"),
    ("null", None),
    ("list", []),
    ("empty-object", {}),
)
MALFORMED_SHAPE_EXCEPTIONS = (
    AttributeError, IndexError, KeyError, StopIteration, TypeError, ValueError,
)
CONTEXT_FIELDS = {
    "requestId", "snapshotId", "stageId", "providerId", "providerVersion",
    "language", "sourceUniverseId", "requestedRelations",
    "allowedTargetUniverseIds", "snapshotFiles", "alreadyAdmittedFactIds",
}
ANCHOR_FIELDS = {
    "kind", "snapshotId", "path", "contentSha256", "startByte", "endByte", "factId",
}
FACT_ID_FIELDS = [
    (1, "snapshotId"), (2, "relation"), (3, "layer"), (4, "producer"),
    (5, "producerVersion"), (6, "schemaVersion"), (7, "resolution"),
    (8, "confidenceMillionths"), (9, "language"), (10, "sourceUniverseId"),
    (11, "targetUniverseId"), (12, "relationSchemaId"),
    (13, "canonicalRelationPayload"), (14, "anchors"),
]
FACT_RECORD_COMPONENT_IDS = {
    "factCandidate": "opensip.fact-candidate.v1",
    "relationPayloadRegistry": "opensip.relation-payload-registry.v1",
    "candidateAdmission": "opensip.fact-candidate-admission.v1",
    "factId": "opensip.fact-id.v1",
    "sourceSpan": "opensip.source-span.v1",
    "anchorRef": "opensip.anchor-ref.v1",
}
RELATION_SPECS = {
    "file": {
        "required": ["path", "contentSha256", "byteLength"], "optional": [],
        "fields": {"path": "CanonicalPath", "contentSha256": "DigestHex",
                   "byteLength": "UInt64"}, "universeRule": "same-only",
        "resolutionRules": {},
    },
    "package": {
        "required": ["packageName", "packageVersion", "manifestPath"], "optional": [],
        "fields": {"packageName": "CanonicalText", "packageVersion": "CanonicalText",
                   "manifestPath": "CanonicalPath"}, "universeRule": "same-only",
        "resolutionRules": {},
    },
    "vcs-change": {
        "required": ["path", "changeKind"], "optional": ["previousPath"],
        "fields": {"path": "CanonicalPath", "changeKind": "ChangeKindV1",
                   "previousPath": "CanonicalPath"},
        "enums": {"ChangeKindV1": ["added", "modified", "deleted", "renamed"]},
        "fieldRules": ["previousPath is required exactly when changeKind=renamed and forbidden otherwise"],
        "universeRule": "same-only", "resolutionRules": {},
    },
    "declares": {
        "required": ["container", "declared", "declarationKind"], "optional": [],
        "fields": {"container": "SubjectIdV1", "declared": "SubjectIdV1",
                   "declarationKind": "DeclarationKindV1"},
        "enums": {"DeclarationKindV1": ["module", "namespace", "type", "function",
                                          "method", "field", "variable", "parameter"]},
        "universeRule": "same-only", "resolutionRules": {},
    },
    "literal": {
        "required": ["owner", "literalKind", "valueText"], "optional": [],
        "fields": {"owner": "SubjectIdV1", "literalKind": "LiteralKindV1",
                   "valueText": "CanonicalText"},
        "enums": {"LiteralKindV1": ["string", "number", "boolean", "null", "regex",
                                      "template"]},
        "universeRule": "same-only", "resolutionRules": {},
    },
    "control-flow": {
        "required": ["from", "to", "edgeKind"], "optional": [],
        "fields": {"from": "SubjectIdV1", "to": "SubjectIdV1",
                   "edgeKind": "ControlFlowEdgeKindV1"},
        "enums": {"ControlFlowEdgeKindV1": ["fallthrough", "branch-true", "branch-false",
                                               "loop", "return", "throw", "exception"]},
        "universeRule": "same-only", "resolutionRules": {},
    },
    "imports": {
        "required": ["importer", "specifier"], "optional": ["resolvedTarget"],
        "fields": {"importer": "SubjectIdV1", "specifier": "CanonicalText",
                   "resolvedTarget": "SubjectIdV1"}, "universeRule": "admitted-target",
        "resolutionRules": {
            "syntactic-specifier": {"required": [], "forbidden": ["resolvedTarget"]},
            "resolved-target": {"required": ["resolvedTarget"], "forbidden": []},
        },
    },
    "references": {
        "required": ["referrer", "name"], "optional": ["resolvedBinding"],
        "fields": {"referrer": "SubjectIdV1", "name": "CanonicalText",
                   "resolvedBinding": "SubjectIdV1"}, "universeRule": "admitted-target",
        "resolutionRules": {
            "syntactic-name-match": {"required": [], "forbidden": ["resolvedBinding"]},
            "resolved-binding": {"required": ["resolvedBinding"], "forbidden": []},
        },
    },
    "calls": {
        "required": ["caller", "calleeText"], "optional": ["resolvedCallee"],
        "fields": {"caller": "SubjectIdV1", "calleeText": "CanonicalText",
                   "resolvedCallee": "SubjectIdV1"}, "universeRule": "admitted-target",
        "resolutionRules": {
            "syntactic-callee-name": {"required": [], "forbidden": ["resolvedCallee"]},
            "resolved-callee": {"required": ["resolvedCallee"], "forbidden": []},
        },
    },
    "types": {
        "required": ["subject", "typeText"], "optional": ["checkedType"],
        "fields": {"subject": "SubjectIdV1", "typeText": "CanonicalText",
                   "checkedType": "SubjectIdV1"}, "universeRule": "same-only",
        "resolutionRules": {
            "annotated": {"required": [], "forbidden": ["checkedType"]},
            "checked": {"required": ["checkedType"], "forbidden": []},
        },
    },
    "reachability": {
        "required": ["origin", "reachable"], "optional": [],
        "fields": {"origin": "SubjectIdV1", "reachable": "SubjectIdV1"},
        "universeRule": "same-only", "resolutionRules": {},
    },
    "clones": {
        "required": ["bodyIdentity", "normalisationLevel", "normalisationVersion"],
        "optional": [],
        "fields": {"bodyIdentity": "Sha256Text",
                   "normalisationLevel": "NormalisationLevelV1",
                   "normalisationVersion": "DigestHex"},
        "enums": {"NormalisationLevelV1": ["L0-verbatim", "L1-lexical",
                                              "L2-comment-insensitive",
                                              "L3-identifier-insensitive"]},
        "universeRule": "same-only", "resolutionRules": {},
    },
}


class DuplicateKeyError(ValueError):
    """A JSON object carried the same key twice. Named, never silently kept."""


def _no_duplicate_keys(pairs):
    """object_pairs_hook that refuses duplicates and NAMES the key.

    json.loads keeps the LAST of a duplicated key, so a contract can read one way
    to a human and another to every F1..F14 gate below while the parsed object
    stays byte-identical to the honest one — a digest check cannot see it, because
    the bytes really are what they claim to be. The gates run on the parsed value.
    The key is named so an operator learns not just that a file is bad but where.
    """
    seen = {}
    for k, v in pairs:
        if k in seen:
            raise DuplicateKeyError(f"duplicate JSON key {k!r}")
        seen[k] = v
    return seen


def loads_strict(text):
    """The only JSON entry point in this file. One place to keep hooked."""
    return json.loads(text, object_pairs_hook=_no_duplicate_keys)


def _is_uint(value, maximum=0xffff_ffff_ffff_ffff) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= maximum


def _is_nfc_text(value, *, nonempty=True) -> bool:
    return isinstance(value, str) and (bool(value) or not nonempty) and \
        unicodedata.normalize("NFC", value) == value and \
        not any(ord(ch) < 32 or 127 <= ord(ch) <= 159 for ch in value)


def _is_path(value) -> bool:
    if not _is_nfc_text(value) or value.startswith("/") or "\\" in value:
        return False
    parts = value.split("/")
    return all(part not in {"", ".", ".."} for part in parts)


def _is_subject(value) -> bool:
    if not _is_nfc_text(value) or ":" not in value:
        return False
    namespace, opaque = value.split(":", 1)
    return bool(opaque) and SUBJECT_NAMESPACE_RE.fullmatch(namespace) is not None


def _cve1(value) -> bytes:
    """Independent FACT-ID-V1 implementation of the shared closed CVE1 grammar."""
    if value is None:
        return b"\x00"
    if value is False:
        return b"\x01"
    if value is True:
        return b"\x02"
    if isinstance(value, int) and not isinstance(value, bool):
        if 0 <= value <= 0xffff_ffff_ffff_ffff:
            return b"\x03" + struct.pack(">Q", value)
        if -(1 << 63) <= value < 0:
            return b"\x07" + struct.pack(">q", value)
        raise ValueError("integer outside CVE1 range")
    if isinstance(value, str):
        if unicodedata.normalize("NFC", value) != value:
            raise ValueError("non-NFC string")
        data = value.encode("utf-8")
        return b"\x04" + struct.pack(">I", len(data)) + data
    if isinstance(value, list):
        return b"\x05" + struct.pack(">I", len(value)) + b"".join(_cve1(x) for x in value)
    if isinstance(value, dict):
        if not all(isinstance(k, str) for k in value):
            raise ValueError("non-string map key")
        keys = sorted(value, key=lambda k: k.encode("utf-8"))
        return b"\x06" + struct.pack(">I", len(keys)) + b"".join(
            _cve1(k) + _cve1(value[k]) for k in keys
        )
    raise ValueError(f"unsupported CVE1 type {type(value).__name__}")


def _cbor_head(major: int, value: int) -> bytes:
    if value < 24:
        return bytes([(major << 5) | value])
    if value <= 0xff:
        return bytes([(major << 5) | 24, value])
    if value <= 0xffff:
        return bytes([(major << 5) | 25]) + struct.pack(">H", value)
    if value <= 0xffff_ffff:
        return bytes([(major << 5) | 26]) + struct.pack(">I", value)
    if value <= 0xffff_ffff_ffff_ffff:
        return bytes([(major << 5) | 27]) + struct.pack(">Q", value)
    raise ValueError("CBOR integer/length out of range")


def _deterministic_cbor(value) -> bytes:
    """Restricted relation-payload encoder; map order follows the binding profile."""
    if value is None:
        return b"\xf6"
    if value is False:
        return b"\xf4"
    if value is True:
        return b"\xf5"
    if isinstance(value, int) and not isinstance(value, bool):
        if value < 0:
            raise ValueError("negative relation payload integer")
        return _cbor_head(0, value)
    if isinstance(value, str):
        if not _is_nfc_text(value, nonempty=False):
            raise ValueError("noncanonical relation payload text")
        data = value.encode("utf-8")
        return _cbor_head(3, len(data)) + data
    if isinstance(value, list):
        return _cbor_head(4, len(value)) + b"".join(_deterministic_cbor(x) for x in value)
    if isinstance(value, dict):
        if not all(isinstance(k, str) for k in value):
            raise ValueError("non-text relation payload map key")
        encoded = [(_deterministic_cbor(k), _deterministic_cbor(v)) for k, v in value.items()]
        encoded.sort(key=lambda pair: pair[0])
        return _cbor_head(5, len(encoded)) + b"".join(k + v for k, v in encoded)
    raise ValueError(f"unsupported relation payload type {type(value).__name__}")


def _type_valid(value, type_name: str, enums: dict) -> bool:
    if type_name == "CanonicalPath":
        return _is_path(value)
    if type_name == "CanonicalText":
        return _is_nfc_text(value)
    if type_name == "SubjectIdV1":
        return _is_subject(value)
    if type_name == "DigestHex":
        return isinstance(value, str) and DIGEST_RE.fullmatch(value) is not None
    if type_name == "Sha256Text":
        return isinstance(value, str) and SHA256_TEXT_RE.fullmatch(value) is not None
    if type_name == "UInt64":
        return _is_uint(value)
    return value in enums.get(type_name, [])


def _payload_errors(payload, relation: str, resolution: str, schemas: dict) -> list[str]:
    schema = schemas.get(relation) or {}
    if not isinstance(payload, dict):
        return ["FACT_RELATION_PAYLOAD_INVALID"]
    required = set(schema.get("required", []))
    optional = set(schema.get("optional", []))
    if set(payload) != required | (set(payload) & optional) or required - set(payload):
        return ["FACT_RELATION_PAYLOAD_INVALID"]
    enums = schema.get("enums") or {}
    for field, value in payload.items():
        if not _type_valid(value, (schema.get("fields") or {}).get(field, ""), enums):
            return ["FACT_RELATION_PAYLOAD_INVALID"]
    rr = (schema.get("resolutionRules") or {}).get(resolution)
    if rr and (set(rr.get("required", [])) - set(payload) or
               set(rr.get("forbidden", [])) & set(payload)):
        return ["FACT_RELATION_PAYLOAD_INVALID"]
    if relation == "vcs-change":
        renamed = payload.get("changeKind") == "renamed"
        if renamed != ("previousPath" in payload):
            return ["FACT_RELATION_PAYLOAD_INVALID"]
    return []


def _anchor_errors(anchor, context: dict, schema: dict) -> list[str]:
    if not isinstance(anchor, dict) or set(anchor) != ANCHOR_FIELDS or \
            schema.get("closed") is not True or schema.get("additionalProperties") is not False:
        return ["FACT_ANCHOR_INVALID"]
    kind = anchor.get("kind")
    if kind == "source-span":
        if anchor.get("factId") is not None or anchor.get("snapshotId") != context.get("snapshotId") or \
                not _is_path(anchor.get("path")) or not isinstance(anchor.get("contentSha256"), str) or \
                DIGEST_RE.fullmatch(anchor["contentSha256"]) is None or \
                not _is_uint(anchor.get("startByte")) or not _is_uint(anchor.get("endByte")) or \
                anchor["startByte"] >= anchor["endByte"]:
            return ["FACT_ANCHOR_INVALID"]
        files = {x.get("path"): x for x in context.get("snapshotFiles", [])}
        file = files.get(anchor["path"]) or {}
        if file.get("contentSha256") != anchor["contentSha256"] or \
                not _is_uint(file.get("byteLength")) or anchor["endByte"] > file.get("byteLength", -1):
            return ["FACT_ANCHOR_INVALID"]
    elif kind == "fact-ref":
        null_fields = {"snapshotId", "path", "contentSha256", "startByte", "endByte"}
        if any(anchor.get(field) is not None for field in null_fields) or \
                not isinstance(anchor.get("factId"), str) or \
                FACT_ID_RE.fullmatch(anchor["factId"]) is None or \
                anchor["factId"] not in context.get("alreadyAdmittedFactIds", []):
            return ["FACT_ANCHOR_INVALID"]
    else:
        return ["FACT_ANCHOR_INVALID"]
    return []


def _fact_id(identity_input: dict, fact_id_contract: dict) -> tuple[bytes, str]:
    fields = fact_id_contract.get("preimageFields", [])
    if [(x.get("tag"), x.get("name")) for x in fields] != FACT_ID_FIELDS or \
            set(identity_input) != {name for _, name in FACT_ID_FIELDS}:
        raise ValueError("FACT-ID-V1 input field set drifted")
    domain = b"opensip.fact-id\0"
    preimage = domain + struct.pack(">H", 1) + struct.pack(">H", len(FACT_ID_FIELDS))
    for tag, name in FACT_ID_FIELDS:
        encoded = _cve1(identity_input[name])
        preimage += bytes([tag]) + struct.pack(">I", len(encoded)) + encoded
    return preimage, "fact:sha256:" + hashlib.sha256(preimage).hexdigest()


def _context_errors(context: dict) -> list[str]:
    if not isinstance(context, dict) or set(context) != CONTEXT_FIELDS:
        return ["FACT_ADMISSION_CONTEXT_INVALID"]
    pair = {"providerId": context.get("providerId"), "language": context.get("language")}
    if pair not in PROVIDER_PROFILES or not _is_nfc_text(context.get("providerVersion")) or \
            not _is_nfc_text(context.get("stageId")) or \
            not isinstance(context.get("requestId"), str) or \
            REQUEST_ID_RE.fullmatch(context["requestId"]) is None or \
            not isinstance(context.get("snapshotId"), str) or \
            SNAPSHOT_ID_RE.fullmatch(context["snapshotId"]) is None or \
            not isinstance(context.get("sourceUniverseId"), str) or \
            SHA256_TEXT_RE.fullmatch(context["sourceUniverseId"]) is None:
        return ["FACT_ADMISSION_CONTEXT_INVALID"]
    for field in ("requestedRelations", "allowedTargetUniverseIds",
                  "snapshotFiles", "alreadyAdmittedFactIds"):
        if not isinstance(context.get(field), list):
            return ["FACT_ADMISSION_CONTEXT_INVALID"]
    if context["requestedRelations"] != sorted(set(context["requestedRelations"])) or \
            context["allowedTargetUniverseIds"] != sorted(set(context["allowedTargetUniverseIds"])) or \
            context["sourceUniverseId"] not in context["allowedTargetUniverseIds"] or \
            not all(_is_nfc_text(x) for x in context["allowedTargetUniverseIds"]):
        return ["FACT_ADMISSION_CONTEXT_INVALID"]
    files = context["snapshotFiles"]
    if [x.get("path") for x in files if isinstance(x, dict)] != \
            sorted(x.get("path") for x in files if isinstance(x, dict)) or any(
                not isinstance(x, dict) or set(x) != {"path", "contentSha256", "byteLength"} or
                not _is_path(x.get("path")) or not isinstance(x.get("contentSha256"), str) or
                DIGEST_RE.fullmatch(x["contentSha256"]) is None or not _is_uint(x.get("byteLength"))
                for x in files):
        return ["FACT_ADMISSION_CONTEXT_INVALID"]
    if context["alreadyAdmittedFactIds"] != sorted(set(context["alreadyAdmittedFactIds"])) or \
            any(not isinstance(x, str) or FACT_ID_RE.fullmatch(x) is None
                for x in context["alreadyAdmittedFactIds"]):
        return ["FACT_ADMISSION_CONTEXT_INVALID"]
    return []


def _admit_vector(vector: dict, contract: dict, rels: dict) -> tuple[list[str], dict | None,
                                                                     bytes | None, str | None]:
    context = vector.get("context") or {}
    candidate = vector.get("candidate") or {}
    errors = _context_errors(context)
    if errors:
        return errors, None, None, None
    if not isinstance(candidate, dict) or set(candidate) != VECTOR_CANDIDATE_FIELDS:
        return ["FACT_CANDIDATE_SCHEMA_INVALID"], None, None, None
    if not _is_uint(candidate.get("candidateOrdinal")):
        return ["FACT_CANDIDATE_SCHEMA_INVALID"], None, None, None
    relation = candidate.get("relation")
    schemas = (contract.get("relationPayloadSchemaRegistryV1") or {}).get("schemas") or {}
    if relation not in rels or relation not in schemas:
        return ["FACT_RELATION_UNKNOWN"], None, None, None
    schema_id = candidate.get("relationSchemaId")
    known_ids = {s.get("schemaId") for s in schemas.values() if isinstance(s, dict)}
    if schema_id not in known_ids:
        return ["FACT_RELATION_SCHEMA_UNKNOWN"], None, None, None
    schema = schemas[relation]
    if schema_id != schema.get("schemaId") or candidate.get("schemaVersion") != \
            schema.get("schemaVersion"):
        return ["FACT_RELATION_SCHEMA_MISMATCH"], None, None, None
    if relation not in context["requestedRelations"]:
        return ["FACT_RELATION_NOT_REQUESTED"], None, None, None
    if candidate.get("resolution") not in rels[relation].get("ladder", []) or \
            candidate.get("layer") != rels[relation].get("layer"):
        return ["FACT_RELATION_OR_RESOLUTION_INVALID"], None, None, None
    pair = {"providerId": candidate.get("producer"), "language": candidate.get("language")}
    if pair not in PROVIDER_PROFILES or candidate.get("producer") != context["providerId"] or \
            candidate.get("producerVersion") != context["providerVersion"] or \
            candidate.get("language") != context["language"]:
        return ["FACT_PROVIDER_CONTEXT_MISMATCH"], None, None, None
    if not _is_uint(candidate.get("confidenceMillionths"), 1_000_000):
        return ["FACT_CANDIDATE_SCHEMA_INVALID"], None, None, None
    payload = candidate.get("decodedRelationPayload")
    payload_errors = _payload_errors(payload, relation, candidate["resolution"], schemas)
    if payload_errors:
        return payload_errors, None, None, None
    try:
        canonical_payload = _deterministic_cbor(payload)
    except (TypeError, ValueError, struct.error):
        return ["FACT_RELATION_PAYLOAD_INVALID"], None, None, None
    payload_hex = candidate.get("canonicalRelationPayloadHex")
    if not isinstance(payload_hex, str) or payload_hex != canonical_payload.hex():
        return ["FACT_RELATION_PAYLOAD_NONCANONICAL"], None, None, None
    if candidate.get("sourceUniverseId") != context["sourceUniverseId"]:
        return ["FACT_SOURCE_UNIVERSE_MISMATCH"], None, None, None
    if candidate.get("targetUniverseId") not in context["allowedTargetUniverseIds"]:
        return ["FACT_TARGET_UNIVERSE_NOT_ADMITTED"], None, None, None
    if schema.get("universeRule") == "same-only" and \
            candidate.get("targetUniverseId") != candidate.get("sourceUniverseId"):
        return ["FACT_TARGET_UNIVERSE_MISMATCH"], None, None, None
    anchors = candidate.get("anchors")
    anchor_schema = contract.get("anchorSchema") or {}
    if not isinstance(anchors, list) or not anchors or any(
            _anchor_errors(anchor, context, anchor_schema) for anchor in anchors):
        return ["FACT_ANCHOR_INVALID"], None, None, None
    try:
        anchor_bytes = [_cve1(anchor) for anchor in anchors]
    except (TypeError, ValueError, struct.error):
        return ["FACT_ANCHOR_INVALID"], None, None, None
    if anchor_bytes != sorted(anchor_bytes) or len(anchor_bytes) != len(set(anchor_bytes)):
        return ["FACT_ANCHOR_INVALID"], None, None, None
    identity_input = {
        "snapshotId": context["snapshotId"],
        "relation": relation,
        "layer": candidate["layer"],
        "producer": candidate["producer"],
        "producerVersion": candidate["producerVersion"],
        "schemaVersion": candidate["schemaVersion"],
        "resolution": candidate["resolution"],
        "confidenceMillionths": candidate["confidenceMillionths"],
        "language": candidate["language"],
        "sourceUniverseId": candidate["sourceUniverseId"],
        "targetUniverseId": candidate["targetUniverseId"],
        "relationSchemaId": schema_id,
        "canonicalRelationPayload": payload_hex,
        "anchors": anchors,
    }
    try:
        preimage, fact_id = _fact_id(identity_input, contract.get("factIdContract") or {})
    except (TypeError, ValueError, struct.error):
        return ["FACT_ID_PREIMAGE_INVALID"], None, None, None
    source_anchors = [a for a in anchors if a.get("kind") == "source-span"]
    envelope = {
        "factId": fact_id,
        "snapshotId": context["snapshotId"],
        "relation": relation,
        "layer": candidate["layer"],
        "producer": candidate["producer"],
        "producerVersion": candidate["producerVersion"],
        "schemaVersion": candidate["schemaVersion"],
        "resolution": candidate["resolution"],
        "confidence": candidate["confidenceMillionths"] / 1_000_000,
        "language": candidate["language"],
    }
    if source_anchors:
        primary = min(source_anchors, key=lambda a: (
            a["path"].encode("utf-8"), a["startByte"], a["endByte"],
            a["contentSha256"].encode("ascii")))
        envelope["span"] = {k: primary[k] for k in ("path", "startByte", "endByte")}
    record = {
        "envelope": envelope,
        "payload": {
            "sourceUniverseId": candidate["sourceUniverseId"],
            "targetUniverseId": candidate["targetUniverseId"],
            "relationSchemaId": schema_id,
            "canonicalRelationPayload": payload_hex,
            "anchors": anchors,
        },
    }
    return [], record, preimage, fact_id


def _set_path(value: dict, path: str, replacement) -> None:
    parts = path.split(".")
    cursor = value
    for part in parts[:-1]:
        cursor = cursor[int(part)] if isinstance(cursor, list) else cursor[part]
    final = parts[-1]
    if isinstance(cursor, list):
        cursor[int(final)] = replacement
    else:
        cursor[final] = replacement


def sufficiency(req: dict, view: dict, reg: dict, depth: int = 0) -> dict:
    """Pure (requirement, fact view) -> {satisfied} | {satisfied, deficiency}.

    Collects every applicable cause, then reports the single most specific one.
    Collecting-then-ranking rather than returning on first failure is deliberate:
    a view can be simultaneously provider-unavailable and budget-exhausted, and
    early return would make the reported cause depend on check order rather than
    on the declared precedence."""
    rel = req["relation"]
    causes: list[str] = []

    entry = view.get(rel)
    if entry is None:
        return {"satisfied": False, "deficiency": "required-relation-missing"}

    ladder = reg["relations"][rel]["ladder"]
    have, need = entry["resolution"], req["minResolution"]
    if have not in ladder:
        return {"satisfied": False, "deficiency": "required-relation-missing"}
    if ladder.index(have) < ladder.index(need):
        causes.append(REASON_TO_DEFICIENCY.get(
            entry.get("rungUnavailableBecause"), "required-relation-missing"))

    if entry.get("confidence", 1.0) < req.get("minConfidence", 0.0):
        causes.append("confidence-floor-unmet")

    # F5 — an unavailable result must not masquerade as a clean one.
    if req["completeness"] == "complete" and entry.get("coverage") != "complete":
        causes.append(REASON_TO_DEFICIENCY.get(
            entry.get("rungUnavailableBecause"), "required-relation-missing"))

    # F11 — a derived relation is only as good as what it was derived from.
    if depth < 4:
        for dep in reg.get("dependsOn", {}).get(rel, []):
            sub = sufficiency({**dep, "completeness": "partial-ok"}, view, reg, depth + 1)
            if not sub["satisfied"]:
                causes.append(sub["deficiency"])

    if not causes:
        return {"satisfied": True}
    return {"satisfied": False,
            "deficiency": min(causes, key=PRECEDENCE.index)}


def apply_profile(base: dict | None, prof: dict, reg: dict) -> dict:
    """F10 — profiles strengthen only. A profile with no base requirement is
    accepted but materialises nothing: a label is not a consumer."""
    if base is None:
        return {"accepted": True, "materialises": False}
    rel = base["relation"]
    ladder = reg["relations"][rel]["ladder"]
    eff = dict(base)
    if "minResolution" in prof:
        if ladder.index(prof["minResolution"]) < ladder.index(base["minResolution"]):
            return {"accepted": False, "reason": "profiles may strengthen, never weaken"}
        eff["minResolution"] = prof["minResolution"]
    if "minConfidence" in prof:
        if prof["minConfidence"] < base.get("minConfidence", 0.0):
            return {"accepted": False, "reason": "profiles may strengthen, never weaken"}
        eff["minConfidence"] = prof["minConfidence"]
    if "completeness" in prof:
        rank = {"partial-ok": 0, "complete": 1}
        if rank[prof["completeness"]] < rank[base["completeness"]]:
            return {"accepted": False, "reason": "profiles may strengthen, never weaken"}
        eff["completeness"] = prof["completeness"]
    return {"accepted": True, "effective": eff, "materialises": True}


def _fact_envelope_record_errors(value: dict, schema: dict) -> list[str]:
    if not isinstance(value, dict):
        return ["FACT_ENVELOPE_NOT_AN_OBJECT"]
    allowed = set(schema.get("requiredFields", [])) | set(schema.get("optionalFields", []))
    if set(value) - allowed:
        return ["FACT_ENVELOPE_UNKNOWN_FIELD"]
    if set(schema.get("requiredFields", [])) - set(value):
        return ["FACT_ENVELOPE_MISSING_REQUIRED_FIELD"]
    return []


def _fact_record_errors(c: dict, resolved_inputs: dict | None) -> list[str]:
    f: list[str] = []
    contract = c.get("factRecordContractV1") or {}
    if contract.get("contractId") != "opensip.fact-record.v1" or \
            contract.get("owner") != "FACT-PLANE" or \
            contract.get("componentIds") != FACT_RECORD_COMPONENT_IDS:
        f.append("F12: fact-record contract/component identifiers are absent or drifted")
        return f
    if contract.get("providerProfiles") != PROVIDER_PROFILES:
        f.append("F12: canonical TypeScript/Rust provider profiles are not exact")
    candidate_schema = contract.get("candidateSchema") or {}
    if candidate_schema.get("id") != FACT_RECORD_COMPONENT_IDS["factCandidate"] or \
            candidate_schema.get("closed") is not True or \
            candidate_schema.get("additionalProperties") is not False or \
            set(candidate_schema.get("required", [])) != CANDIDATE_FIELDS or \
            candidate_schema.get("optional") != [] or \
            set((candidate_schema.get("fields") or {})) != CANDIDATE_FIELDS:
        f.append("F12: FactCandidateV1 is not the exact closed provider candidate")
    context_schema = contract.get("hostAdmissionContextSchema") or {}
    if context_schema.get("closed") is not True or \
            context_schema.get("additionalProperties") is not False or \
            set(context_schema.get("required", [])) != CONTEXT_FIELDS or \
            context_schema.get("optional") != [] or \
            "never copied" not in context_schema.get("requestIdRule", ""):
        f.append("F12: host admission context is not exact/closed against RequestId authority")
    source_span = contract.get("sourceSpanSchema") or {}
    if source_span.get("id") != FACT_RECORD_COMPONENT_IDS["sourceSpan"] or \
            source_span.get("closed") is not True or \
            source_span.get("additionalProperties") is not False or \
            set(source_span.get("required", [])) != {"path", "startByte", "endByte"} or \
            source_span.get("optional") != []:
        f.append("F12: SourceSpanV1 is not an exact closed byte-span projection")
    anchor = contract.get("anchorSchema") or {}
    if anchor.get("id") != FACT_RECORD_COMPONENT_IDS["anchorRef"] or \
            anchor.get("closed") is not True or anchor.get("additionalProperties") is not False or \
            set(anchor.get("required", [])) != ANCHOR_FIELDS or anchor.get("optional") != [] or \
            set((anchor.get("variants") or {})) != {"source-span", "fact-ref"}:
        f.append("F12: AnchorRefV1 is not the exact closed two-variant record")
    admitted = contract.get("admittedRecordSchema") or {}
    payload_schema = admitted.get("payload") or {}
    admitted_payload_fields = {
        "sourceUniverseId", "targetUniverseId", "relationSchemaId",
        "canonicalRelationPayload", "anchors",
    }
    if admitted.get("id") != "opensip.fact-record.v1" or admitted.get("closed") is not True or \
            admitted.get("additionalProperties") is not False or \
            set(admitted.get("required", [])) != {"envelope", "payload"} or \
            admitted.get("optional") != [] or payload_schema.get("closed") is not True or \
            payload_schema.get("additionalProperties") is not False or \
            set(payload_schema.get("required", [])) != admitted_payload_fields or \
            payload_schema.get("optional") != [] or \
            set((payload_schema.get("fields") or {})) != admitted_payload_fields:
        f.append("F12: admitted FactRecordV1/envelope+payload shape is not exact and closed")

    registry = contract.get("relationPayloadSchemaRegistryV1") or {}
    schemas = registry.get("schemas") or {}
    rels = (c.get("relationRegistry") or {}).get("relations") or {}
    if registry.get("id") != FACT_RECORD_COMPONENT_IDS["relationPayloadRegistry"] or \
            registry.get("version") != 1 or registry.get("closed") is not True or \
            set(schemas) != set(rels) or set(schemas) != set(RELATION_SPECS):
        f.append("F12: v1 relation payload registry is not exact/total over live relations")
    else:
        schema_ids: list[str] = []
        for relation, expected in RELATION_SPECS.items():
            actual = schemas.get(relation) or {}
            expected_id = f"opensip.relation.{relation}.v1"
            allowed_keys = {"schemaId", "schemaVersion", "closed"} | set(expected)
            if relation == "clones":
                allowed_keys.add("bodyIdentityBoundary")
            if set(actual) != allowed_keys or actual.get("schemaId") != expected_id or \
                    actual.get("schemaVersion") != 1 or actual.get("closed") is not True or \
                    any(actual.get(key) != value for key, value in expected.items()) or \
                    set(actual.get("fields", {})) != set(actual.get("required", [])) | \
                    set(actual.get("optional", [])):
                f.append(f"F12: relation payload schema '{relation}' is not the exact v1 schema")
            schema_ids.append(actual.get("schemaId"))
        if len(schema_ids) != len(set(schema_ids)):
            f.append("F12: relation payload schema IDs are not unique")
    cbor = registry.get("canonicalPayloadEncoding") or {}
    if cbor.get("mapOrder") != \
            "ascending unsigned lexicographic order of each key's deterministic-CBOR bytes" or \
            "unknown fields" not in cbor.get("forbidden", []) or \
            "Decode once" not in cbor.get("admission", ""):
        f.append("F12: deterministic relation-payload CBOR/admission profile drifted")

    mapping = contract.get("candidateToAdmittedMapping") or {}
    destinations = {
        "candidateOrdinal": None,
        "relation": "envelope.relation",
        "resolution": "envelope.resolution",
        "layer": "envelope.layer",
        "producer": "envelope.producer",
        "producerVersion": "envelope.producerVersion",
        "schemaVersion": "envelope.schemaVersion",
        "language": "envelope.language",
        "sourceUniverseId": "payload.sourceUniverseId",
        "targetUniverseId": "payload.targetUniverseId",
        "confidenceMillionths": "envelope.confidence",
        "relationSchemaId": "payload.relationSchemaId",
        "canonicalRelationPayload": "payload.canonicalRelationPayload",
        "anchors": "payload.anchors",
    }
    if mapping.get("id") != FACT_RECORD_COMPONENT_IDS["candidateAdmission"] or \
            mapping.get("fieldDestinations") != destinations or \
            set((mapping.get("hostInjected") or {})) != {"snapshotId", "factId"} or \
            set((mapping.get("derived") or {})) != {
                "confidence", "span", "canonicalRelationPayload"}:
        f.append("F12: FactCandidateV1 to admitted FactRecordV1 mapping is not exact/total")

    fid = contract.get("factIdContract") or {}
    framing = fid.get("preimageFraming") or {}
    if fid.get("id") != FACT_RECORD_COMPONENT_IDS["factId"] or \
            fid.get("owner") != "Rust host only" or fid.get("algorithm") != "SHA-256" or \
            fid.get("regex") != r"^fact:sha256:[0-9a-f]{64}$" or \
            framing.get("domainBytes") != \
            "UTF-8 bytes 6f70656e7369702e666163742d696400 (ASCII opensip.fact-id followed by one NUL byte)" or \
            framing.get("recipeVersion") != 1 or \
            [(x.get("tag"), x.get("name")) for x in fid.get("preimageFields", [])] != \
            FACT_ID_FIELDS or "RequestId" not in fid.get("excludedInputs", []) or \
            "candidateOrdinal" not in fid.get("excludedInputs", []):
        f.append("F13: FACT-ID-V1 host ownership/domain/framing/input set drifted")
    cve = fid.get("canonicalValueEncoding") or {}
    if cve.get("id") != "CVE1" or cve.get("normativeSource") != \
            "resolved-inputs.v2.json#planIdContract.canonicalValueEncoding":
        f.append("F13: FACT-ID-V1 does not join the exact CVE1 contract")
    elif resolved_inputs is None:
        f.append(f"F13: could not load {RESOLVED_INPUTS} for the CVE1 join")
    else:
        live_cve = (resolved_inputs.get("planIdContract") or {}).get("canonicalValueEncoding") or {}
        if live_cve.get("name") != "CVE1" or set(live_cve.get("closedTypes", [])) != {
                "null", "false", "true", "unsigned-64", "negative-signed-64",
                "NFC-UTF8-string", "array", "string-keyed-map"}:
            f.append("F13: live resolved-inputs CVE1 grammar is unavailable or drifted")

    vectors = {v.get("id"): v for v in contract.get("vectors", []) if isinstance(v, dict)}
    expected_vector_ids = {
        "fact-id-v1-typescript-declares", "fact-id-v1-rust-cross-universe-call"}
    computed: dict[str, str] = {}
    if set(vectors) != expected_vector_ids or len(vectors) != len(expected_vector_ids):
        f.append("F13: exact TypeScript/Rust FACT-ID-V1 vector set is absent or duplicated")
    else:
        for vector_id in sorted(expected_vector_ids):
            vector = vectors[vector_id]
            errors, record, preimage, fact_id = _admit_vector(vector, contract, rels)
            if errors:
                f.append(f"F13 {vector_id}: candidate did not admit — {errors[0]}")
                continue
            computed[vector_id] = fact_id
            if len(preimage or b"") != vector.get("expectedPreimageByteLength") or \
                    fact_id != vector.get("expectedFactId") or \
                    not isinstance(fact_id, str) or FACT_ID_RE.fullmatch(fact_id) is None or \
                    (record or {}).get("envelope", {}).get("factId") != fact_id:
                f.append(f"F13 {vector_id}: preimage length or independent FactId oracle drifted")
            if set((record or {}).get("envelope", {})) - (REQUIRED_ENVELOPE | OPTIONAL_ENVELOPE) or \
                    set((record or {}).get("payload", {})) != admitted_payload_fields:
                f.append(f"F12 {vector_id}: admitted record is not the exact envelope+payload shape")

    expected_negatives = {
        "reject-unknown-relation-schema": "FACT_RELATION_SCHEMA_UNKNOWN",
        "reject-schema-version-mismatch": "FACT_RELATION_SCHEMA_MISMATCH",
        "reject-payload-unknown-field": "FACT_RELATION_PAYLOAD_INVALID",
        "reject-payload-malformed-field": "FACT_RELATION_PAYLOAD_INVALID",
        "reject-unknown-relation": "FACT_RELATION_UNKNOWN",
        "reject-relation-schema-cross-wire": "FACT_RELATION_SCHEMA_MISMATCH",
        "reject-source-universe-substitution": "FACT_SOURCE_UNIVERSE_MISMATCH",
        "reject-target-outside-admitted-domain": "FACT_TARGET_UNIVERSE_NOT_ADMITTED",
        "reject-same-only-cross-universe": "FACT_TARGET_UNIVERSE_MISMATCH",
        "reject-anchor-unknown-field": "FACT_ANCHOR_INVALID",
        "reject-anchor-out-of-bounds": "FACT_ANCHOR_INVALID",
        "reject-anchor-content-substitution": "FACT_ANCHOR_INVALID",
    }
    negatives = {x.get("id"): x for x in contract.get("negativeFixtures", [])
                 if isinstance(x, dict)}
    if set(negatives) != set(expected_negatives) or len(negatives) != len(expected_negatives):
        f.append("F12: fact-record negative fixture set is not exact")
    else:
        for fixture_id, expected in expected_negatives.items():
            fixture = negatives[fixture_id]
            base = vectors.get(fixture.get("baseVectorId"))
            if base is None or fixture.get("expected") != expected:
                f.append(f"F12 {fixture_id}: base or expected outcome drifted")
                continue
            candidate = copy.deepcopy(base)
            changes = fixture.get("setMany") or [fixture.get("set")]
            try:
                for change in changes:
                    _set_path(candidate, change["path"], copy.deepcopy(change["value"]))
                errors, _, _, _ = _admit_vector(candidate, contract, rels)
            except (KeyError, IndexError, TypeError, ValueError):
                errors = ["FIXTURE_NOT_EXECUTABLE"]
            if errors != [expected]:
                f.append(f"F12 {fixture_id}: derived {errors}, expected exactly [{expected}]")

    variation = contract.get("requestIdInvarianceVector") or {}
    request_ids = variation.get("requestIds") or []
    expected_ids = variation.get("expectedFactIds") or []
    base = vectors.get(variation.get("baseVectorId"))
    if variation.get("id") != "fact-id-v1-request-id-invariance" or \
            len(request_ids) != 2 or request_ids[0] == request_ids[1] or \
            any(not isinstance(x, str) or REQUEST_ID_RE.fullmatch(x) is None for x in request_ids) or \
            len(expected_ids) != 2 or expected_ids[0] != expected_ids[1] or \
            any(not isinstance(x, str) or FACT_ID_RE.fullmatch(x) is None for x in expected_ids) or \
            base is None:
        f.append("F14: RequestId invariance vector is malformed, equal-input, or equality-only junk")
    else:
        outputs: list[str] = []
        for request_id in request_ids:
            candidate = copy.deepcopy(base)
            candidate["context"]["requestId"] = request_id
            errors, _, _, fact_id = _admit_vector(candidate, contract, rels)
            if errors:
                outputs = []
                break
            outputs.append(fact_id)
        if outputs != expected_ids or expected_ids[0] != computed.get(variation["baseVectorId"]):
            f.append("F14: RequestId variation does not recompute the exact base FACT-ID-V1")
    return f


def _check(c: dict, d9: dict | None, resolved_inputs: dict | None = None) -> list[str]:
    f: list[str] = []
    reg = c["relationRegistry"]
    rels = reg["relations"]

    # ---- F1 envelope ----
    envelope_schema = c["factEnvelope"]
    env = envelope_schema["fields"]
    for req_field in REQUIRED_ENVELOPE:
        if req_field not in env:
            f.append(f"F1: fact envelope is missing required field '{req_field}'")
    if envelope_schema.get("closed") is not True or \
            envelope_schema.get("additionalProperties") is not False or \
            set(envelope_schema.get("requiredFields", [])) != REQUIRED_ENVELOPE or \
            set(envelope_schema.get("optionalFields", [])) != OPTIONAL_ENVELOPE or \
            set(env) != REQUIRED_ENVELOPE | OPTIONAL_ENVELOPE or \
            envelope_schema.get("unknownFieldOutcome") != "FACT_ENVELOPE_UNKNOWN_FIELD":
        f.append("F1: FactEnvelope is not the exact closed required/optional schema")
    if any(env.get(field, {}).get("optional") is not True for field in OPTIONAL_ENVELOPE) or \
            any(env.get(field, {}).get("optional") is True for field in REQUIRED_ENVELOPE):
        f.append("F1: FactEnvelope required/optional declarations disagree with field metadata")
    for bad in FORBIDDEN_ENVELOPE & set(env):
        f.append(f"F1: envelope declares '{bad}', a global judgment C-1 forbids")
    fixtures = {item.get("id"): item for item in c.get("factEnvelopeFixtures", [])}
    expected_negative_fixtures = {
        "fact-envelope-reject-request-id": "FACT_ENVELOPE_UNKNOWN_FIELD",
        "fact-envelope-reject-arbitrary-extension": "FACT_ENVELOPE_UNKNOWN_FIELD",
    }
    if {key: fixtures.get(key, {}).get("expected") for key in expected_negative_fixtures} != \
            expected_negative_fixtures:
        f.append("F1: FactEnvelope unknown-field fixture set/outcomes are not exact")
    positive = fixtures.get("fact-envelope-valid-minimal") or {}
    base_envelope = positive.get("envelope") or {}
    if positive.get("valid") is not True or \
            _fact_envelope_record_errors(base_envelope, envelope_schema):
        f.append("F1: minimal exact FactEnvelope fixture is not valid")
    for fixture_id in expected_negative_fixtures:
        fixture = fixtures.get(fixture_id) or {}
        candidate = copy.deepcopy(base_envelope)
        candidate.update(fixture.get("addField") or {})
        errors = _fact_envelope_record_errors(candidate, envelope_schema)
        if fixture.get("valid") is not False or errors != [fixture.get("expected")]:
            f.append(f"F1 {fixture_id}: unknown field is not rejected by its exact outcome")

    # ---- F12..F14 generic admitted fact record / identity ----
    f.extend(_fact_record_errors(c, resolved_inputs))

    # ---- F2 ladders ----
    for name, r in rels.items():
        ladder = r.get("ladder") or []
        if not ladder:
            f.append(f"F2: relation '{name}' has an empty ladder")
        if len(ladder) != len(set(ladder)):
            f.append(f"F2: relation '{name}' has duplicate rungs")

    # ---- F6/F7 no global ordering ----
    owner: dict[str, list[str]] = {}
    for name, r in rels.items():
        for rung in r.get("ladder", []):
            owner.setdefault(rung, []).append(name)
    for name, r in rels.items():
        if "rank" in r or "order" in r:
            f.append(f"F7: relation '{name}' declares a rank/order field — layers are not ordered")
    if "layerOrder" in c or "tierOrder" in c or "globalLadder" in c:
        f.append("F7: contract declares a global layer/tier ordering, which C-1 forbids")

    # ---- F9 live cross-check against D9 ----
    vocab = c["deficiencyVocabulary"]["values"]
    if d9 is None:
        f.append(f"F9: could not load {D9} — the vocabulary subset claim is unverified")
    else:
        d9_defs = set(d9["scenarioAxesSchema"]["properties"]["deficiency"]["enum"])
        for v in vocab:
            if v not in d9_defs:
                f.append(f"F9: deficiency '{v}' is not expressible in D9 — a Coverage "
                         f"state with no way to terminate")
    for v in PRECEDENCE:
        if v not in vocab:
            f.append(f"F9: precedence names '{v}' but the vocabulary does not declare it")
    for v in vocab:
        if v not in PRECEDENCE:
            f.append(f"F9: vocabulary declares '{v}' but the precedence does not rank it")

    # ---- sufficiency goldens ----
    for g in c["goldenCases"]:
        gid, req = g["id"], g["requirement"]
        rel = req["relation"]
        if rel not in rels:
            f.append(f"F3 {gid}: requirement names unregistered relation '{rel}'")
            continue
        ladder = rels[rel]["ladder"]

        # F3/F6 — the rung must belong to THIS relation, not merely to some relation
        if req["minResolution"] not in ladder:
            holders = owner.get(req["minResolution"], [])
            if holders:
                f.append(f"F6 {gid}: minResolution '{req['minResolution']}' belongs to "
                         f"{holders}, not to '{rel}' — resolutions are not comparable "
                         f"across relations")
            else:
                f.append(f"F3 {gid}: minResolution '{req['minResolution']}' is not a rung "
                         f"of '{rel}'")
            continue

        got = sufficiency(req, g["view"], reg)
        exp = g["expected"]

        if got["satisfied"] != exp["satisfied"]:
            f.append(f"F4 {gid}: derived satisfied={got['satisfied']}, expected "
                     f"{exp['satisfied']}")
            continue
        if got["satisfied"]:
            if "deficiency" in got:
                f.append(f"F4 {gid}: satisfied result carries a deficiency")
            # F8 — one-rung top must be satisfied outright
            if len(ladder) == 1 and req["minResolution"] == ladder[0] and "deficiency" in got:
                f.append(f"F8 {gid}: authoritative one-rung relation reported as degraded")
        else:
            if "deficiency" not in got:
                f.append(f"F4 {gid}: unsatisfied result carries no deficiency")
            elif got["deficiency"] != exp.get("deficiency"):
                f.append(f"F4 {gid}: derived deficiency '{got['deficiency']}', expected "
                         f"'{exp.get('deficiency')}'")
            elif got["deficiency"] not in vocab:
                f.append(f"F9 {gid}: deficiency '{got['deficiency']}' outside vocabulary")

    # ---- F5 there must be a golden proving unknown never satisfies complete ----
    if not any(g["requirement"]["completeness"] == "complete"
               and not g["expected"]["satisfied"]
               and (g["view"].get(g["requirement"]["relation"], {}) or {}).get("coverage") == "unknown"
               for g in c["goldenCases"]):
        f.append("F5: no golden proves coverage=unknown fails completeness=complete")

    # ---- F8 there must be a golden proving a one-rung relation is authoritative ----
    if not any(len(rels[g["requirement"]["relation"]]["ladder"]) == 1
               and g["expected"]["satisfied"]
               for g in c["goldenCases"] if g["requirement"]["relation"] in rels):
        f.append("F8: no golden proves a one-rung relation is satisfied outright — "
                 "C-1's central claim is untested")

    # ---- F10 profile goldens ----
    for g in c["profileGoldens"]:
        gid = g["id"]
        got = apply_profile(g["base"], g["profile"], reg)
        exp = g["expected"]
        if got["accepted"] != exp["accepted"]:
            f.append(f"F10 {gid}: accepted={got['accepted']}, expected {exp['accepted']}")
            continue
        if "materialises" in exp and got.get("materialises") != exp["materialises"]:
            f.append(f"F10 {gid}: materialises={got.get('materialises')}, expected "
                     f"{exp['materialises']} — a label is not a consumer")
        if exp.get("effective"):
            for k, v in exp["effective"].items():
                if got.get("effective", {}).get(k) != v:
                    f.append(f"F10 {gid}: effective {k}={got.get('effective',{}).get(k)}, "
                             f"expected {v}")
    return f


def check(c: object, d9: dict | None, resolved_inputs: dict | None = None) -> list[str]:
    """Total contract boundary for every successfully parsed JSON root."""
    if not isinstance(c, dict) or not c:
        return ["FP-TOTALITY-ROOT: contract root must be a non-empty object"]
    registry = c.get("relationRegistry")
    if not isinstance(registry, dict) or not isinstance(registry.get("relations"), dict):
        return ["FP-TOTALITY-SHAPE: relationRegistry.relations must be an object"]
    try:
        return _check(c, d9, resolved_inputs)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [f"FP-TOTALITY-EXCEPTION: malformed contract shape "
                f"({type(exc).__name__})"]


# --------------------------------------------------------------------------
# --selftest: a checker that only validates a good artifact proves nothing.
# --------------------------------------------------------------------------
def _m_global_ladder(c):
    c["layerOrder"] = ["inventory", "syntax", "semantic", "derived"]

def _m_envelope_quality(c):
    c["factEnvelope"]["fields"]["quality"] = {"type": "string"}

def _m_cross_relation_rung(c):
    for g in c["goldenCases"]:
        if g["id"] == "syntax-relation-is-authoritative":
            g["requirement"]["minResolution"] = "resolved-binding"

def _m_unknown_satisfies_complete(c):
    for g in c["goldenCases"]:
        if g["id"] == "unknown-coverage-never-satisfies-complete":
            g["expected"] = {"satisfied": True}

def _m_syntax_is_degraded(c):
    for g in c["goldenCases"]:
        if g["id"] == "syntax-relation-is-authoritative":
            g["expected"] = {"satisfied": False, "deficiency": "required-relation-missing"}

def _m_deficiency_outside_d9(c):
    c["deficiencyVocabulary"]["values"].append("facts-were-vibes")

def _m_profile_weakens(c):
    for g in c["profileGoldens"]:
        if g["id"] == "profile-may-not-lower-resolution":
            g["expected"] = {"accepted": True}

def _m_label_materialises(c):
    for g in c["profileGoldens"]:
        if g["id"] == "profile-alone-does-not-materialise":
            g["expected"]["materialises"] = True

def _m_drop_dependency(c):
    del c["relationRegistry"]["dependsOn"]["reachability"]

def _m_empty_ladder(c):
    c["relationRegistry"]["relations"]["declares"]["ladder"] = []


def _m_confidence_as_relation_missing(c):
    for g in c["goldenCases"]:
        if g["id"] == "confidence-floor-unmet":
            g["expected"]["deficiency"] = "required-relation-missing"

def _m_drop_confidence_from_vocab(c):
    c["deficiencyVocabulary"]["values"] = [
        v for v in c["deficiencyVocabulary"]["values"] if v != "confidence-floor-unmet"]


def _m_open_fact_envelope(c):
    c["factEnvelope"]["closed"] = False
    c["factEnvelope"]["additionalProperties"] = True


def _m_allow_request_id_in_fact_envelope(c):
    c["factEnvelope"]["fields"]["requestId"] = {"type": "string", "optional": True}
    c["factEnvelope"]["optionalFields"].append("requestId")


def _m_drop_request_id_rejection_fixture(c):
    c["factEnvelopeFixtures"] = [
        item for item in c["factEnvelopeFixtures"]
        if item["id"] != "fact-envelope-reject-request-id"
    ]


def _fact_vector(c, vector_id="fact-id-v1-typescript-declares"):
    return next(v for v in c["factRecordContractV1"]["vectors"] if v["id"] == vector_id)


def _m_unknown_relation_schema(c):
    _fact_vector(c)["candidate"]["relationSchemaId"] = "opensip.relation.unknown.v1"


def _m_malformed_relation_schema_version(c):
    _fact_vector(c)["candidate"]["schemaVersion"] = 2


def _m_unknown_relation_payload_field(c):
    _fact_vector(c)["candidate"]["decodedRelationPayload"]["futureField"] = True


def _m_malformed_relation_payload(c):
    _fact_vector(c)["candidate"]["decodedRelationPayload"]["declared"] = 7


def _m_noncanonical_relation_payload(c):
    _fact_vector(c)["candidate"]["canonicalRelationPayloadHex"] = "00"


def _m_unknown_fact_relation(c):
    _fact_vector(c)["candidate"]["relation"] = "vibes"


def _m_substitute_source_universe(c):
    _fact_vector(c)["candidate"]["sourceUniverseId"] = "sha256:" + "9" * 64


def _m_substitute_target_universe(c):
    _fact_vector(c, "fact-id-v1-rust-cross-universe-call")["candidate"][
        "targetUniverseId"] = "sha256:" + "9" * 64


def _m_malformed_anchor(c):
    _fact_vector(c)["candidate"]["anchors"][0]["requestId"] = \
        "req1_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


def _m_prefixed_fact_provider(c):
    _fact_vector(c)["candidate"]["producer"] = "provider.typescript-semantic"


def _m_include_request_id_in_fact_id(c):
    c["factRecordContractV1"]["factIdContract"]["preimageFields"].append(
        {"tag": 15, "name": "requestId"})


def _m_alias_fact_id_to_body_domain(c):
    c["factRecordContractV1"]["factIdContract"]["preimageFraming"]["domainBytes"] = \
        "opensip.fact-identity.v1"


def _m_corrupt_fact_id_vector(c):
    _fact_vector(c)["expectedFactId"] = "fact:sha256:" + "0" * 64


def _m_equal_request_ids(c):
    variation = c["factRecordContractV1"]["requestIdInvarianceVector"]
    variation["requestIds"][1] = variation["requestIds"][0]


def _m_junk_request_fact_ids(c):
    c["factRecordContractV1"]["requestIdInvarianceVector"]["expectedFactIds"] = [
        "equal-junk", "equal-junk"]

MUTATIONS = [
    ("declare a global layer ordering (F7 / C-1)", _m_global_ladder),
    ("add a 'quality' field to the envelope (F1 / C-1)", _m_envelope_quality),
    ("require another relation's rung (F6)", _m_cross_relation_rung),
    ("let coverage=unknown satisfy complete (F5 / TO-5)", _m_unknown_satisfies_complete),
    ("report an authoritative syntax fact as degraded (F8 / C-1)", _m_syntax_is_degraded),
    ("add a deficiency D9 cannot express (F9)", _m_deficiency_outside_d9),
    ("let a profile weaken a floor (F10)", _m_profile_weakens),
    ("let a bare label materialise a relation (F10)", _m_label_materialises),
    ("drop a derived relation's dependency (F11)", _m_drop_dependency),
    ("map confidence floor to required-relation-missing (R1-FP-01)", _m_confidence_as_relation_missing),
    ("drop confidence-floor-unmet from vocabulary (R1-FP-01)", _m_drop_confidence_from_vocab),
    ("empty a relation's ladder (F2)", _m_empty_ladder),
    ("open FactEnvelope to unknown fields (R6-IP02-01)", _m_open_fact_envelope),
    ("admit RequestId into FactEnvelope (R6-IP02-01)",
     _m_allow_request_id_in_fact_envelope),
    ("drop the RequestId unknown-field fixture (R6-IP02-01)",
     _m_drop_request_id_rejection_fixture),
    ("accept an unknown relation payload schema (R5R-DLTS-02)",
     _m_unknown_relation_schema),
    ("accept a malformed relation schema version (R5R-DLTS-02)",
     _m_malformed_relation_schema_version),
    ("accept an unknown relation payload field (R5R-DLTS-02)",
     _m_unknown_relation_payload_field),
    ("accept a malformed relation payload value (R5R-DLTS-02)",
     _m_malformed_relation_payload),
    ("accept noncanonical relation payload bytes (R5R-DLTS-02)",
     _m_noncanonical_relation_payload),
    ("accept an unregistered fact relation (R5R-DLTS-02)",
     _m_unknown_fact_relation),
    ("substitute the admitted source universe (R5R-DLTS-02)",
     _m_substitute_source_universe),
    ("substitute a target outside the admitted domain (R5R-DLTS-02)",
     _m_substitute_target_universe),
    ("open a typed anchor with RequestId (R5R-DLTS-02/R6R-IP02-01)",
     _m_malformed_anchor),
    ("alias a fact producer with provider.* (R5R-DLTS-05)",
     _m_prefixed_fact_provider),
    ("include RequestId in FACT-ID-V1 (R6R-IP02-01)",
     _m_include_request_id_in_fact_id),
    ("alias generic FACT-ID-V1 to normalized body identity (R5R-DLTS-02)",
     _m_alias_fact_id_to_body_domain),
    ("corrupt an exact FACT-ID-V1 vector (R5R-DLTS-02)",
     _m_corrupt_fact_id_vector),
    ("reuse one RequestId in the invariance vector (R6R-IP02-01)",
     _m_equal_request_ids),
    ("replace computed fact identities with equal junk strings (R6R-IP02-01)",
     _m_junk_request_fact_ids),
]


def selftest(base: dict, d9: dict | None, resolved_inputs: dict | None) -> int:
    # A mutation suite only means anything against a clean base. Otherwise every row
    # echoes the pre-existing failure and reports "all rejected" — a false assurance
    # that actually occurred on the first run of check-evidence.py.
    pre = check(base, d9, resolved_inputs)
    if pre:
        print(f"REFUSING to self-test: the base contract has {len(pre)} finding(s), so "
              f"every mutation would be masked by them.")
        for x in pre[:5]:
            print("  -", x)
        return 1
    print("mutation self-test — each row must be REJECTED\n")
    escaped = 0
    for name, root in TOTALITY_ROOT_CASES:
        findings = check(copy.deepcopy(root), d9, resolved_inputs)
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  parsed-JSON root {name}")
        print(f"          {findings[0] if findings else 'NO FINDING — root survived'}")
    for name, mut in MUTATIONS:
        c = copy.deepcopy(base)
        mut(c)
        findings = check(c, d9, resolved_inputs)
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  {name}")
        print(f"          {findings[0] if findings else 'NO FINDING — mutation survived'}")
    print()
    if escaped:
        print(f"{escaped}/{len(MUTATIONS) + len(TOTALITY_ROOT_CASES)} retained cases "
              "ESCAPED — the proof path is optional")
        return 1
    print(f"all {len(MUTATIONS)} semantic mutations and {len(TOTALITY_ROOT_CASES)} "
          "root-shape cases rejected — the proof path is load-bearing")
    return 0


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--selftest"]
    p = pathlib.Path(args[0]) if args else pathlib.Path(__file__).with_name(BINDING)
    if not p.exists():
        print(f"missing contract: {p}", file=sys.stderr)
        return 2
    c = loads_strict(p.read_text())
    d9p = pathlib.Path(__file__).with_name(D9)
    d9 = loads_strict(d9p.read_text()) if d9p.exists() else None
    rip = pathlib.Path(__file__).with_name(RESOLVED_INPUTS)
    resolved_inputs = loads_strict(rip.read_text()) if rip.exists() else None

    if "--selftest" in sys.argv:
        return selftest(c, d9, resolved_inputs)
    f = check(c, d9, resolved_inputs)
    if not f:
        n, m = len(c["goldenCases"]), len(c["profileGoldens"])
        print(f"fact-plane contract OK — {p.name}, {n} sufficiency + {m} profile goldens, "
              f"F1..F14 clean (F9 cross-checked against {D9}; FACT-ID-V1 uses live CVE1)")
        return 0
    print(f"{len(f)} finding(s) in {p.name}:")
    for x in f:
        print("  -", x)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
