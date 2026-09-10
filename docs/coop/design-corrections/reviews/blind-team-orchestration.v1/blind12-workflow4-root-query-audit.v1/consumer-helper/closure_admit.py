"""Retained-closure admission over exported store bytes.

identity-and-evidence.md §3: fetch exact referenced artifacts, rehash, rejoin
owning schema/order/digest/registry/native laws. Not helper self-mint equality.
"""
from __future__ import annotations

import hashlib
from typing import Any

from helper.body_identity import parse_body_identity_frame
from helper.canonical import C
from helper.errors import AdmissionError
from helper.identity import parse_h_frame
from helper.lexical import admit_raw
from helper.schema_admit import validate_against
from helper.store import Store


REL = "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"
NATIVE = "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
SINV = "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json"
ENUM = "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json"


def rehash(store: Store, digest: str) -> bytes:
    raw = store.get(digest)
    got = hashlib.sha256(raw).hexdigest()
    if got != digest:
        raise AdmissionError("BLOB_REHASH", f"{digest} rehashes to {got}")
    return raw


def parse_canonical(store: Store, digest: str) -> Any:
    raw = rehash(store, digest)
    obj = admit_raw(raw)
    if C(obj) != raw:
        raise AdmissionError("CANONICAL_REMAINDER", digest)
    return obj


def parse_typed_h(store: Store, typed_id: str, domain: str) -> dict:
    rec = store.object_table[typed_id]
    frame = rehash(store, rec["digest"])
    parsed = parse_h_frame(frame, allowed_domains={domain})
    if parsed["digest"] != rec["digest"]:
        raise AdmissionError("H_DIGEST", typed_id)
    return parsed["value"]


def parse_native_h(store: Store, hex_digest: str, domain: str) -> dict:
    frame = rehash(store, hex_digest)
    parsed = parse_h_frame(frame, allowed_domains={domain})
    return parsed["value"]


def closure_tree_digests(closure: dict) -> set[str]:
    return {row["sha256"] for row in closure.get("tree") or []}


def admit_syntax_native_context(store: Store, ctx: dict) -> dict:
    """native-evidence.md §1.2 grammar tree: definitions, bundle, normalizer spec."""
    bundle = ctx["grammarBundle"]
    closure_id = bundle["closureId"]
    closure = parse_typed_h(store, closure_id, "closure")
    if closure["kind"] != "grammar":
        raise AdmissionError("GRAMMAR_CLOSURE_KIND", closure["kind"])
    tree = closure_tree_digests(closure)
    missing = []
    required = {
        "bundleDigest": bundle["bundleDigest"],
        "specificationDigest": bundle["normalizer"]["specificationDigest"],
    }
    for g in bundle["grammars"]:
        required[f"grammarDigest:{g['grammarId']}"] = g["grammarDigest"]
    for name, d in required.items():
        rehash(store, d)
        if d not in tree:
            missing.append({"name": name, "digest": d})
    if missing:
        raise AdmissionError("GRAMMAR_TREE_RETENTION", str(missing))
    if bundle["parserVersion"] != closure["semanticVersion"]:
        raise AdmissionError(
            "PARSER_VERSION",
            f"{bundle['parserVersion']} != {closure['semanticVersion']}",
        )
    # Recursively fetch every tree member
    for row in closure["tree"]:
        blob = rehash(store, row["sha256"])
        if len(blob) != row["bytes"]:
            raise AdmissionError("TREE_MEMBER_LENGTH", row["path"])
    return {"closure": closure, "tree": sorted(tree), "missing": missing}


def admit_body_identity_frame(store: Store, body_identity: str, *, expected_span: bytes | None = None) -> dict:
    if not body_identity.startswith("sha256:"):
        raise AdmissionError("BODY_IDENTITY_SPELLING", body_identity)
    suffix = body_identity[len("sha256:") :]
    frame = rehash(store, suffix)
    parsed = parse_body_identity_frame(frame)
    if expected_span is not None and parsed.get("levelId") == "L0-verbatim":
        if parsed["l0Span"] != expected_span:
            raise AdmissionError("L0_SPAN_JOIN", "retained L0 span does not equal anchor bytes")
    return parsed


def admit_declares_payload(store: Store, payload_digest: str) -> dict:
    payload = parse_canonical(store, payload_digest)
    r = validate_against(payload, REL, selector="#/$defs/DeclaresPayloadV1", label="DeclaresPayloadV1")
    if not r["stockOk"]:
        raise AdmissionError("DECLARES_PAYLOAD_SCHEMA", str(r["errors"][:5]))
    return payload


def admit_unit_membership(store: Store, membership_digest: str) -> dict:
    memb = parse_canonical(store, membership_digest)
    r = validate_against(memb, NATIVE, selector="#/$defs/UnitMembershipV1", label="UnitMembershipV1")
    if not r["stockOk"]:
        raise AdmissionError("MEMBERSHIP_SCHEMA", str(r["errors"][:5]))
    invented = []
    for unit in memb.get("units") or []:
        if unit.get("unitKind") == "syntax-only":
            invented.append(unit)
    for row in memb.get("rows") or []:
        if row.get("membership") == "syntax-only" and row.get("unitOrdinal") is not None:
            invented.append(row)
    if invented:
        raise AdmissionError("SYNTAX_ONLY_INVENTED_UNIT", str(invented))
    return memb


def admit_enumeration_inventories(store: Store, enum_plan: dict, inventories: list[dict]) -> dict:
    expected = []
    for ci, cell in enumerate(enum_plan["cells"]):
        for pb in cell["programBindings"]:
            for kind in cell["kinds"]:
                expected.append((ci, pb["ordinal"], kind))
    present = {(inv["cellOrdinal"], inv["programOrdinal"], inv["kind"]): inv for inv in inventories}
    missing = [loc for loc in expected if loc not in present]
    extra = [k for k in present if k not in set(expected)]
    if missing or extra:
        raise AdmissionError(
            "ENUMERATION_INVENTORY_MISSING_RECORD",
            f"missing={missing} extra={extra}",
        )
    for inv in inventories:
        r = validate_against(inv, SINV, selector="#", label=f"sinv-{inv['cellOrdinal']}-{inv['kind']}")
        if not r["stockOk"]:
            raise AdmissionError("INVENTORY_SCHEMA", str(r["errors"][:5]))
    return {"expected": expected, "present": sorted(present)}
