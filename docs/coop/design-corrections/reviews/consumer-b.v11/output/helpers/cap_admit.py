"""Capability-manifest admission BEFORE encoding.

Recipe: DELIVERY v4 CAP-MANIFEST-ID-V1
Effective registry: capability-manifest-domains.v2.json (successor of delivery.v4 valueDomains).
Gates in order: ADM-TYPE, ADM-CLOSED, ADM-DOMAIN, ADM-ORDER.
"""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any

from helpers.cve1 import encode as cve1_encode
from helpers.paths import KIT

_REGISTRY = None


def load_registry() -> dict[str, Any]:
    global _REGISTRY
    if _REGISTRY is None:
        p = KIT / "docs/coop/design-corrections/native/capability-manifest-domains.v2.json"
        _REGISTRY = json.loads(p.read_text())
    return _REGISTRY


RECORD_KEYS = {
    "CapabilityManifestV1": ["schemaVersion", "profile", "providers", "coverageForAbsent"],
    "ProviderCapability": [
        "providerId",
        "language",
        "providerVersionSource",
        "toolchainIdentitySource",
        "relations",
        "platformIds",
    ],
    "AbsentCapability": [
        "providerId",
        "language",
        "relationIds",
        "coverageState",
        "deficiency",
    ],
}

STRING_FIELDS = {
    ("CapabilityManifestV1", "profile"),
    ("ProviderCapability", "providerId"),
    ("ProviderCapability", "language"),
    ("ProviderCapability", "providerVersionSource"),
    ("ProviderCapability", "toolchainIdentitySource"),
    ("AbsentCapability", "providerId"),
    ("AbsentCapability", "language"),
    ("AbsentCapability", "coverageState"),
    ("AbsentCapability", "deficiency"),
}


class CapRefusal(Exception):
    def __init__(self, gate: str, code: str, message: str, *, path: str = "$") -> None:
        super().__init__(f"{gate}:{code}:{path}:{message}")
        self.gate = gate
        self.code = code
        self.message = message
        self.path = path


def _type_is_int(x: Any) -> bool:
    return type(x) is int


def _type_is_str(x: Any) -> bool:
    return type(x) is str


def admit(manifest: Any) -> dict[str, Any]:
    """Admit a CapabilityManifestV1. Returns {ok, firstRefusal, allRefusals, hypothesizedMasked}."""
    refusals: list[dict[str, Any]] = []
    try:
        _adm_type(manifest)
    except CapRefusal as e:
        refusals.append(_ref(e))
        return _result(False, refusals, "ADM-TYPE")
    try:
        _adm_closed(manifest)
    except CapRefusal as e:
        refusals.append(_ref(e))
        return _result(False, refusals, "ADM-CLOSED")
    try:
        _adm_domain(manifest)
    except CapRefusal as e:
        refusals.append(_ref(e))
        return _result(False, refusals, "ADM-DOMAIN")
    try:
        _adm_order(manifest)
    except CapRefusal as e:
        refusals.append(_ref(e))
        return _result(False, refusals, "ADM-ORDER")
    committed = cve1_encode(manifest)
    cap_id = hashlib.sha256(
        b"opensip.capability-manifest.v1\x00" + committed
    ).hexdigest()
    return {
        "ok": True,
        "firstRefusal": None,
        "allRefusals": [],
        "hypothesizedMasked": [],
        "committedBytesHex": committed.hex(),
        "capabilityManifestId": cap_id,
        "classification": "valid",
    }


def _result(ok: bool, refusals: list[dict[str, Any]], first_gate: str) -> dict[str, Any]:
    later = {
        "ADM-TYPE": ["ADM-CLOSED", "ADM-DOMAIN", "ADM-ORDER"],
        "ADM-CLOSED": ["ADM-DOMAIN", "ADM-ORDER"],
        "ADM-DOMAIN": ["ADM-ORDER"],
        "ADM-ORDER": [],
    }[first_gate]
    return {
        "ok": ok,
        "firstRefusal": refusals[0] if refusals else None,
        "allRefusals": refusals,
        "hypothesizedMasked": [
            {"gate": g, "note": "not observed; first refusal already returned"}
            for g in later
        ],
        "classification": "invalid",
    }


def _ref(e: CapRefusal) -> dict[str, Any]:
    return {"gate": e.gate, "code": e.code, "path": e.path, "message": e.message}


def _adm_type(m: Any) -> None:
    if type(m) is not dict:
        raise CapRefusal("ADM-TYPE", "NOT_OBJECT", "manifest is not an object")
    sv = m.get("schemaVersion")
    if not _type_is_int(sv):
        raise CapRefusal(
            "ADM-TYPE",
            "SCHEMA_VERSION_TYPE",
            f"schemaVersion must be JSON integer, got {type(sv).__name__}",
            path="$.schemaVersion",
        )
    if "profile" in m and not _type_is_str(m["profile"]):
        raise CapRefusal("ADM-TYPE", "PROFILE_TYPE", "profile must be string", path="$.profile")
    providers = m.get("providers")
    if type(providers) is list:
        for i, p in enumerate(providers):
            if type(p) is not dict:
                raise CapRefusal("ADM-TYPE", "PROVIDER_TYPE", "provider not object", path=f"$.providers[{i}]")
            for k in (
                "providerId",
                "language",
                "providerVersionSource",
                "toolchainIdentitySource",
            ):
                if k in p and not _type_is_str(p[k]):
                    raise CapRefusal(
                        "ADM-TYPE",
                        "SCALAR_TYPE",
                        f"{k} must be string",
                        path=f"$.providers[{i}].{k}",
                    )
            plats = p.get("platformIds")
            if type(plats) is list:
                for j, x in enumerate(plats):
                    if not _type_is_str(x):
                        raise CapRefusal(
                            "ADM-TYPE",
                            "PLATFORM_TYPE",
                            "platformId must be string",
                            path=f"$.providers[{i}].platformIds[{j}]",
                        )
            rels = p.get("relations")
            if type(rels) is dict:
                for rk, rv in rels.items():
                    if not _type_is_str(rk) or not _type_is_str(rv):
                        raise CapRefusal(
                            "ADM-TYPE",
                            "RELATION_TYPE",
                            "relation key and value must be strings",
                            path=f"$.providers[{i}].relations",
                        )
    absent = m.get("coverageForAbsent")
    if type(absent) is list:
        for i, a in enumerate(absent):
            if type(a) is not dict:
                raise CapRefusal("ADM-TYPE", "ABSENT_TYPE", "absent not object", path=f"$.coverageForAbsent[{i}]")
            for k in ("providerId", "language", "coverageState", "deficiency"):
                if k in a and not _type_is_str(a[k]):
                    raise CapRefusal(
                        "ADM-TYPE",
                        "SCALAR_TYPE",
                        f"{k} must be string",
                        path=f"$.coverageForAbsent[{i}].{k}",
                    )
            rids = a.get("relationIds")
            if type(rids) is list:
                for j, x in enumerate(rids):
                    if not _type_is_str(x):
                        raise CapRefusal(
                            "ADM-TYPE",
                            "RELATION_ID_TYPE",
                            "relationId must be string",
                            path=f"$.coverageForAbsent[{i}].relationIds[{j}]",
                        )


def _closed_record(obj: dict, keys: list[str], path: str, name: str) -> None:
    got = list(obj.keys())
    if sorted(got) != sorted(keys) or len(got) != len(keys):
        raise CapRefusal(
            "ADM-CLOSED",
            "KEY_SET",
            f"{name} must carry exactly {keys}, got {got}",
            path=path,
        )


def _adm_closed(m: dict) -> None:
    _closed_record(m, RECORD_KEYS["CapabilityManifestV1"], "$", "CapabilityManifestV1")
    if type(m["providers"]) is not list:
        raise CapRefusal("ADM-CLOSED", "PROVIDERS_ARRAY", "providers must be array", path="$.providers")
    if type(m["coverageForAbsent"]) is not list:
        raise CapRefusal(
            "ADM-CLOSED",
            "ABSENT_ARRAY",
            "coverageForAbsent must be array",
            path="$.coverageForAbsent",
        )
    for i, p in enumerate(m["providers"]):
        if type(p) is not dict:
            raise CapRefusal("ADM-CLOSED", "PROVIDER_OBJECT", "provider not object", path=f"$.providers[{i}]")
        _closed_record(p, RECORD_KEYS["ProviderCapability"], f"$.providers[{i}]", "ProviderCapability")
        if type(p["relations"]) is not dict:
            raise CapRefusal(
                "ADM-CLOSED",
                "RELATIONS_MAP",
                "relations is a MAP not a record",
                path=f"$.providers[{i}].relations",
            )
        if type(p["platformIds"]) is not list:
            raise CapRefusal(
                "ADM-CLOSED",
                "PLATFORMS_ARRAY",
                "platformIds must be array",
                path=f"$.providers[{i}].platformIds",
            )
    for i, a in enumerate(m["coverageForAbsent"]):
        if type(a) is not dict:
            raise CapRefusal("ADM-CLOSED", "ABSENT_OBJECT", "absent not object", path=f"$.coverageForAbsent[{i}]")
        _closed_record(a, RECORD_KEYS["AbsentCapability"], f"$.coverageForAbsent[{i}]", "AbsentCapability")
        if type(a["relationIds"]) is not list:
            raise CapRefusal(
                "ADM-CLOSED",
                "RELATIONIDS_ARRAY",
                "relationIds must be array",
                path=f"$.coverageForAbsent[{i}].relationIds",
            )


def _adm_domain(m: dict) -> None:
    reg = load_registry()
    relations = set(reg["registries"]["RELATION-DOMAIN-V2"]["members"])
    ladders = reg["registries"]["RELATION-LADDER-DOMAIN-V2"]["ladders"]
    platforms = set(reg["registries"]["PLATFORM-ID-DOMAIN-V1"]["members"])
    deficiencies = set(reg["registries"]["DEFICIENCY-DOMAIN-V1"]["members"])
    cov_states = set(reg["registries"]["COVERAGE-STATE-DOMAIN-V1"]["members"])
    for i, p in enumerate(m["providers"]):
        for j, plat in enumerate(p["platformIds"]):
            if plat not in platforms:
                raise CapRefusal(
                    "ADM-DOMAIN",
                    "PLATFORM",
                    f"{plat!r} not in PLATFORM-ID-DOMAIN-V1",
                    path=f"$.providers[{i}].platformIds[{j}]",
                )
        for rk, rv in p["relations"].items():
            if rk not in relations:
                raise CapRefusal(
                    "ADM-DOMAIN",
                    "RELATION_KEY",
                    f"{rk!r} not in RELATION-DOMAIN-V2",
                    path=f"$.providers[{i}].relations",
                )
            allowed = ladders.get(rk, [])
            if rv not in allowed:
                raise CapRefusal(
                    "ADM-DOMAIN",
                    "RELATION_RUNG",
                    f"rung {rv!r} is not a member of {rk} ladder {allowed}",
                    path=f"$.providers[{i}].relations.{rk}",
                )
    for i, a in enumerate(m["coverageForAbsent"]):
        if a["coverageState"] not in cov_states:
            raise CapRefusal(
                "ADM-DOMAIN",
                "COVERAGE_STATE",
                f"{a['coverageState']!r} not in COVERAGE-STATE-DOMAIN-V1",
                path=f"$.coverageForAbsent[{i}].coverageState",
            )
        if a["deficiency"] not in deficiencies:
            raise CapRefusal(
                "ADM-DOMAIN",
                "DEFICIENCY",
                f"{a['deficiency']!r} not in DEFICIENCY-DOMAIN-V1",
                path=f"$.coverageForAbsent[{i}].deficiency",
            )
        for j, rid in enumerate(a["relationIds"]):
            if rid not in relations:
                raise CapRefusal(
                    "ADM-DOMAIN",
                    "RELATION_ID",
                    f"{rid!r} not in RELATION-DOMAIN-V2",
                    path=f"$.coverageForAbsent[{i}].relationIds[{j}]",
                )


def _strict_ascending(items: list[str], path: str, label: str) -> None:
    encoded = [s.encode("utf-8") for s in items]
    for i in range(1, len(encoded)):
        if encoded[i] <= encoded[i - 1]:
            raise CapRefusal(
                "ADM-ORDER",
                "NOT_CANONICAL",
                f"{label} not strictly ascending unique NFC UTF-8 (RELEASE.CAPABILITY_MANIFEST_NOT_CANONICAL)",
                path=path,
            )


def _adm_order(m: dict) -> None:
    """Traversal: (1) each providers[i].platformIds (2) each coverageForAbsent[i].relationIds
    (3) providers by providerId (4) coverageForAbsent by providerId."""
    for i, p in enumerate(m["providers"]):
        _strict_ascending(p["platformIds"], f"$.providers[{i}].platformIds", "platformIds")
    for i, a in enumerate(m["coverageForAbsent"]):
        _strict_ascending(a["relationIds"], f"$.coverageForAbsent[{i}].relationIds", "relationIds")
    _strict_ascending(
        [p["providerId"] for p in m["providers"]],
        "$.providers",
        "providers.providerId",
    )
    _strict_ascending(
        [a["providerId"] for a in m["coverageForAbsent"]],
        "$.coverageForAbsent",
        "coverageForAbsent.providerId",
    )


def canonicalise_for_release(authoring: dict) -> dict:
    """Producer-side sort only. Consumers never sort. Used to construct committed vectors."""
    m = deepcopy(authoring)
    for p in m.get("providers", []):
        p["platformIds"] = sorted(p.get("platformIds", []), key=lambda s: s.encode("utf-8"))
        # relations map is sorted by CVE1 itself
    for a in m.get("coverageForAbsent", []):
        a["relationIds"] = sorted(a.get("relationIds", []), key=lambda s: s.encode("utf-8"))
    m["providers"] = sorted(m.get("providers", []), key=lambda p: p["providerId"].encode("utf-8"))
    m["coverageForAbsent"] = sorted(
        m.get("coverageForAbsent", []), key=lambda a: a["providerId"].encode("utf-8")
    )
    return m
