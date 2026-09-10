"""Capability-manifest admission BEFORE encoding.

Gates in order: ADM-TYPE, ADM-CLOSED, ADM-DOMAIN, ADM-ORDER.
Selected registry: capability-manifest-domains.v2.json (successor of
delivery.v4 valueDomains within declared scope). Recipe: DELIVERY v4
CAP-MANIFEST-ID-V1.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from . import cve1, h

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v13/subject")

CAP_KEYS = ("schemaVersion", "profile", "providers", "coverageForAbsent")
PROVIDER_KEYS = (
    "providerId",
    "language",
    "providerVersionSource",
    "toolchainIdentitySource",
    "relations",
    "platformIds",
)
ABSENT_KEYS = ("providerId", "language", "relationIds", "coverageState", "deficiency")


class CapRefusal(Exception):
    def __init__(self, gate: str, message: str, masks_later: list[str] | None = None):
        super().__init__(f"{gate}: {message}")
        self.gate = gate
        self.message = message
        self.firstRefusal = gate
        self.masksLater = masks_later or []


def _load_registry() -> dict:
    p = KIT / "docs/coop/design-corrections/native/capability-manifest-domains.v2.json"
    return json.loads(p.read_text())


REG = _load_registry()
RELATIONS = set(REG["registries"]["RELATION-DOMAIN-V2"]["members"])
LADDERS = {
    k: list(v) for k, v in REG["registries"]["RELATION-LADDER-DOMAIN-V2"]["ladders"].items()
}
PLATFORMS = set(REG["registries"]["PLATFORM-ID-DOMAIN-V1"]["members"])
DEFICIENCIES = set(REG["registries"]["DEFICIENCY-DOMAIN-V1"]["members"])
COVERAGE_STATES = set(REG["registries"]["COVERAGE-STATE-DOMAIN-V1"]["members"])


def _is_int(x: Any) -> bool:
    return type(x) is int  # bool is not an integer


def _is_str(x: Any) -> bool:
    return type(x) is str


def _keys(obj: dict) -> list[str]:
    return list(obj.keys())


def _exact_keys(obj: dict, required: tuple[str, ...], where: str) -> Optional[str]:
    got = set(obj.keys())
    want = set(required)
    if got != want:
        return f"{where}: field set {sorted(got)} != {sorted(want)}"
    return None


def adm_type(doc: Any) -> Optional[str]:
    """Exact JSON type before content comparison."""
    if type(doc) is not dict:
        return "CapabilityManifestV1: not a JSON object"
    if "schemaVersion" in doc and not _is_int(doc["schemaVersion"]):
        t = type(doc["schemaVersion"]).__name__
        return f"schemaVersion is a JSON integer; got {t}"
    if "profile" in doc and not _is_str(doc["profile"]):
        return "profile is a JSON string"
    providers = doc.get("providers")
    if providers is not None:
        if type(providers) is not list:
            return "providers is a JSON array"
        for i, p in enumerate(providers):
            if type(p) is not dict:
                return f"providers[{i}] is not an object"
            for k in ("providerId", "language", "providerVersionSource", "toolchainIdentitySource"):
                if k in p and not _is_str(p[k]):
                    return f"providers[{i}].{k} is a JSON string"
            if "platformIds" in p:
                if type(p["platformIds"]) is not list:
                    return f"providers[{i}].platformIds is a JSON array"
                for j, plat in enumerate(p["platformIds"]):
                    if not _is_str(plat):
                        return f"providers[{i}].platformIds[{j}] is a JSON string"
            if "relations" in p:
                if type(p["relations"]) is not dict:
                    return f"providers[{i}].relations is a JSON object/MAP"
                for rk, rv in p["relations"].items():
                    if not _is_str(rk) or not _is_str(rv):
                        return f"providers[{i}].relations entries are strings"
    absents = doc.get("coverageForAbsent")
    if absents is not None:
        if type(absents) is not list:
            return "coverageForAbsent is a JSON array"
        for i, a in enumerate(absents):
            if type(a) is not dict:
                return f"coverageForAbsent[{i}] is not an object"
            for k in ("providerId", "language", "coverageState", "deficiency"):
                if k in a and not _is_str(a[k]):
                    return f"coverageForAbsent[{i}].{k} is a JSON string"
            if "relationIds" in a:
                if type(a["relationIds"]) is not list:
                    return f"coverageForAbsent[{i}].relationIds is a JSON array"
                for j, r in enumerate(a["relationIds"]):
                    if not _is_str(r):
                        return f"coverageForAbsent[{i}].relationIds[{j}] is a JSON string"
    return None


def adm_closed(doc: dict) -> Optional[str]:
    msg = _exact_keys(doc, CAP_KEYS, "CapabilityManifestV1")
    if msg:
        return msg
    for i, p in enumerate(doc["providers"]):
        msg = _exact_keys(p, PROVIDER_KEYS, "ProviderCapability")
        if msg:
            return f"providers[{i}] {msg}"
        # relations is a MAP: no key set. Values are scalars; already typed.
    for i, a in enumerate(doc["coverageForAbsent"]):
        msg = _exact_keys(a, ABSENT_KEYS, "AbsentCapability")
        if msg:
            return f"coverageForAbsent[{i}] {msg}"
    return None


def adm_domain(doc: dict) -> Optional[str]:
    """Exact NFC UTF-8 byte membership. No case folding / alias / trim."""
    for i, p in enumerate(doc["providers"]):
        for rel, rung in p["relations"].items():
            rb = rel.encode("utf-8")
            if rel not in RELATIONS:
                return f"ProviderCapability.relations key {rel!r} is not a member of RELATION-DOMAIN-V2"
            ladder = LADDERS[rel]
            if rung not in ladder:
                return (
                    f"ProviderCapability.relations value {rung!r} is not a rung of {rel} "
                    f"ladder {ladder}"
                )
        for plat in p["platformIds"]:
            if plat not in PLATFORMS:
                return f"ProviderCapability.platformIds: {plat!r} is not a member of PLATFORM-ID-DOMAIN-V1"
    for i, a in enumerate(doc["coverageForAbsent"]):
        for rel in a["relationIds"]:
            if rel not in RELATIONS:
                return f"AbsentCapability.relationIds: {rel!r} is not a member of RELATION-DOMAIN-V2"
        if a["deficiency"] not in DEFICIENCIES:
            return f"AbsentCapability.deficiency: {a['deficiency']!r} is not a member of DEFICIENCY-DOMAIN-V1"
        if a["coverageState"] not in COVERAGE_STATES:
            return f"AbsentCapability.coverageState: {a['coverageState']!r} is not a member of COVERAGE-STATE-DOMAIN-V1"
    return None


def _strict_asc_unique(items: list[str], label: str) -> Optional[str]:
    encoded = [s.encode("utf-8") for s in items]
    for i in range(1, len(encoded)):
        if encoded[i] <= encoded[i - 1]:
            return (
                f"{label}: not strictly ascending by declared key UTF-8 bytes at index {i} "
                f"({items[i-1]!r} then {items[i]!r})"
            )
    return None


def adm_order(doc: dict) -> list[str]:
    """Declared traversal: (1) each providers[i].platformIds (2) each
    coverageForAbsent[i].relationIds (3) providers by providerId
    (4) coverageForAbsent by providerId. Complete list, not first-only."""
    violations: list[str] = []
    for i, p in enumerate(doc["providers"]):
        msg = _strict_asc_unique(p["platformIds"], "ProviderCapability.platformIds")
        if msg:
            violations.append(f"providers[{i}] {msg}")
    for i, a in enumerate(doc["coverageForAbsent"]):
        msg = _strict_asc_unique(a["relationIds"], "AbsentCapability.relationIds")
        if msg:
            violations.append(f"coverageForAbsent[{i}] {msg}")
    msg = _strict_asc_unique([p["providerId"] for p in doc["providers"]], "CapabilityManifestV1.providers")
    if msg:
        violations.append(msg)
    msg = _strict_asc_unique(
        [a["providerId"] for a in doc["coverageForAbsent"]],
        "CapabilityManifestV1.coverageForAbsent",
    )
    if msg:
        violations.append(msg)
    return violations


GATE_ORDER = ("ADM-TYPE", "ADM-CLOSED", "ADM-DOMAIN", "ADM-ORDER")


def admit(doc: Any) -> dict:
    """Run all four gates. First observed refusal is the gate that failed.
    Later hypothesized checks are listed as masked, not executed as pass."""
    masked = list(GATE_ORDER)
    t = adm_type(doc)
    if t:
        raise CapRefusal("ADM-TYPE", t, masks_later=masked[1:])
    c = adm_closed(doc)
    if c:
        raise CapRefusal("ADM-CLOSED", c, masks_later=masked[2:])
    d = adm_domain(doc)
    if d:
        raise CapRefusal("ADM-DOMAIN", d, masks_later=masked[3:])
    o = adm_order(doc)
    if o:
        raise CapRefusal("ADM-ORDER", " | ".join(o), masks_later=[])
    committed = cve1.encode(doc)
    ident = h.capability_manifest_id(committed)
    return {
        "admitted": True,
        "capabilityManifestId": ident,
        "committedBytesHex": committed.hex(),
        "committedBytesDigest": h.raw_sha256(committed),
        "gates": GATE_ORDER,
        "registry": "docs/coop/design-corrections/native/capability-manifest-domains.v2.json",
        "recipe": "CAP-MANIFEST-ID-V1",
    }


def first_refusal(doc: Any) -> dict:
    try:
        result = admit(doc)
        return {"admitted": True, **result}
    except CapRefusal as e:
        return {
            "admitted": False,
            "firstRefusal": e.gate,
            "message": e.message,
            "masksLater": e.masksLater,
        }
