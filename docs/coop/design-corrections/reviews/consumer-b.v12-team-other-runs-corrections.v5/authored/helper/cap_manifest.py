"""Capability-manifest admission BEFORE encoding.

Inherited gates (delivery.v4 CAP-MANIFEST-ID-V1) in order:
ADM-TYPE, ADM-CLOSED, ADM-DOMAIN, ADM-ORDER.

Effective ADM-DOMAIN registry is capability-manifest-domains.v2.json
(successor of delivery.v4 valueDomains within declared scope).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from helper.cve1 import encode as cve1_encode
from helper.errors import AdmissionError

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-other-runs-corrections.v5/subject")
REG_PATH = KIT / "docs/coop/design-corrections/native/capability-manifest-domains.v2.json"

_REG = None


def registry() -> dict:
    global _REG
    if _REG is None:
        _REG = json.loads(REG_PATH.read_text())
    return _REG


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
    "AbsentCapability": ["providerId", "language", "relationIds", "coverageState", "deficiency"],
}

SET_FIELDS = {
    # sort key, uniqueness
    "providers": ("providerId", True),
    "coverageForAbsent": ("providerId", True),
    "platformIds": (None, True),  # element itself
    "relationIds": (None, True),
}


def _nfc_bytes(s: str) -> bytes:
    if type(s) is not str:
        raise AdmissionError("ADM-TYPE", "expected string", extra={"got": type(s).__name__})
    return s.encode("utf-8")


def _exact_int(x: Any, *, path: str) -> int:
    if type(x) is bool or type(x) is not int:
        raise AdmissionError(
            "ADM-TYPE",
            f"{path}: exact JSON integer required; {type(x).__name__} is not an integer",
            path=path,
        )
    return x


def _exact_str(x: Any, *, path: str) -> str:
    if type(x) is not str:
        raise AdmissionError(
            "ADM-TYPE",
            f"{path}: exact JSON string required; {type(x).__name__} is not a string",
            path=path,
        )
    return x


def _closed_record(obj: Any, keys: list[str], *, path: str) -> dict:
    if type(obj) is not dict:
        raise AdmissionError("ADM-CLOSED", f"{path}: record must be object", path=path)
    got = list(obj.keys())
    if sorted(got) != sorted(keys) or len(got) != len(keys):
        raise AdmissionError(
            "ADM-CLOSED",
            f"{path}: closed key set {keys} got {got}",
            path=path,
            extra={"expected": keys, "got": got},
        )
    return obj


GATE_ORDER = ("ADM-TYPE", "ADM-CLOSED", "ADM-DOMAIN", "ADM-ORDER")


def _adm_type_provider(p: Any, *, path: str) -> None:
    if type(p) is not dict:
        raise AdmissionError("ADM-TYPE", f"{path}: expected object", path=path)
    for field in ("providerId", "language", "providerVersionSource", "toolchainIdentitySource"):
        if field in p:
            _exact_str(p[field], path=f"{path}.{field}")
    if "relations" in p:
        rels = p["relations"]
        if type(rels) is not dict:
            raise AdmissionError("ADM-TYPE", f"{path}.relations must be map", path=f"{path}.relations")
        for k, v in rels.items():
            kp = f"{path}.relations[{k!r}]"
            _exact_str(k, path=kp)
            _exact_str(v, path=kp)
    if "platformIds" in p:
        plats = p["platformIds"]
        if type(plats) is not list:
            raise AdmissionError("ADM-TYPE", f"{path}.platformIds must be array", path=f"{path}.platformIds")
        for j, plat in enumerate(plats):
            _exact_str(plat, path=f"{path}.platformIds[{j}]")


def _adm_type_absent(a: Any, *, path: str) -> None:
    if type(a) is not dict:
        raise AdmissionError("ADM-TYPE", f"{path}: expected object", path=path)
    for field in ("providerId", "language", "coverageState", "deficiency"):
        if field in a:
            _exact_str(a[field], path=f"{path}.{field}")
    if "relationIds" in a:
        rids = a["relationIds"]
        if type(rids) is not list:
            raise AdmissionError("ADM-TYPE", f"{path}.relationIds must be array", path=f"{path}.relationIds")
        for j, rid in enumerate(rids):
            _exact_str(rid, path=f"{path}.relationIds[{j}]")


def _adm_type(manifest: Any) -> None:
    """ADM-TYPE before any key-set or registry comparison."""
    if type(manifest) is not dict:
        raise AdmissionError("ADM-TYPE", "$: expected object", path="$")
    if "schemaVersion" in manifest:
        _exact_int(manifest["schemaVersion"], path="$.schemaVersion")
    if "profile" in manifest:
        _exact_str(manifest["profile"], path="$.profile")
    if "providers" in manifest:
        if type(manifest["providers"]) is not list:
            raise AdmissionError("ADM-TYPE", "$.providers must be array", path="$.providers")
        for i, p in enumerate(manifest["providers"]):
            _adm_type_provider(p, path=f"$.providers[{i}]")
    if "coverageForAbsent" in manifest:
        if type(manifest["coverageForAbsent"]) is not list:
            raise AdmissionError("ADM-TYPE", "$.coverageForAbsent must be array", path="$.coverageForAbsent")
        for i, a in enumerate(manifest["coverageForAbsent"]):
            _adm_type_absent(a, path=f"$.coverageForAbsent[{i}]")


def _adm_closed(manifest: dict) -> dict:
    root = _closed_record(manifest, RECORD_KEYS["CapabilityManifestV1"], path="$")
    for i, p in enumerate(root["providers"]):
        _closed_record(p, RECORD_KEYS["ProviderCapability"], path=f"$.providers[{i}]")
    for i, a in enumerate(root["coverageForAbsent"]):
        _closed_record(a, RECORD_KEYS["AbsentCapability"], path=f"$.coverageForAbsent[{i}]")
    return root


def _adm_domain(root: dict) -> None:
    reg = registry()["registries"]
    platforms = set(reg["PLATFORM-ID-DOMAIN-V1"]["members"])
    relations = set(reg["RELATION-DOMAIN-V2"]["members"])
    ladders = reg["RELATION-LADDER-DOMAIN-V2"]["ladders"]
    deficiencies = set(reg["DEFICIENCY-DOMAIN-V1"]["members"])
    cov_states = set(reg["COVERAGE-STATE-DOMAIN-V1"]["members"])
    for i, rec in enumerate(root["providers"]):
        path = f"$.providers[{i}]"
        for k, v in rec["relations"].items():
            kp = f"{path}.relations[{k!r}]"
            if k not in relations:
                raise AdmissionError(
                    "ADM-DOMAIN",
                    f"{kp}: relation key not in RELATION-DOMAIN-V2",
                    path=kp,
                    extra={"value": k},
                )
            allowed_rungs = ladders.get(k, [])
            if v not in allowed_rungs:
                raise AdmissionError(
                    "ADM-DOMAIN",
                    f"{kp}: rung {v!r} is not a member of {k} ladder",
                    path=kp,
                    extra={"relation": k, "rung": v, "ladder": allowed_rungs},
                )
        for j, plat in enumerate(rec["platformIds"]):
            pp = f"{path}.platformIds[{j}]"
            if plat not in platforms:
                raise AdmissionError(
                    "ADM-DOMAIN",
                    f"{pp}: platformId not in PLATFORM-ID-DOMAIN-V1",
                    path=pp,
                    extra={"value": plat},
                )
    for i, rec in enumerate(root["coverageForAbsent"]):
        path = f"$.coverageForAbsent[{i}]"
        if rec["coverageState"] not in cov_states:
            raise AdmissionError(
                "ADM-DOMAIN",
                f"{path}.coverageState not in COVERAGE-STATE-DOMAIN-V1",
                path=f"{path}.coverageState",
                extra={"value": rec["coverageState"]},
            )
        if rec["deficiency"] not in deficiencies:
            raise AdmissionError(
                "ADM-DOMAIN",
                f"{path}.deficiency not in DEFICIENCY-DOMAIN-V1",
                path=f"{path}.deficiency",
                extra={"value": rec["deficiency"]},
            )
        for j, rid in enumerate(rec["relationIds"]):
            rp = f"{path}.relationIds[{j}]"
            if rid not in relations:
                raise AdmissionError(
                    "ADM-DOMAIN",
                    f"{rp}: relationId not in RELATION-DOMAIN-V2",
                    path=rp,
                    extra={"value": rid},
                )


def _adm_order(root: dict) -> None:
    # Declared traversal: (1) providers[i].platformIds (2) coverageForAbsent[i].relationIds
    # (3) providers by providerId (4) coverageForAbsent by providerId.
    def strict_asc(items: list[str], *, path: str) -> None:
        seen = set()
        prev = None
        for x in items:
            b = _nfc_bytes(x)
            if x in seen:
                raise AdmissionError(
                    "ADM-ORDER",
                    f"{path}: duplicate {x!r} is an ordering violation",
                    path=path,
                    extra={"value": x},
                )
            seen.add(x)
            if prev is not None and b <= prev:
                raise AdmissionError(
                    "ADM-ORDER",
                    f"{path}: not strictly ascending NFC UTF-8 ({x!r})",
                    path=path,
                    extra={"value": x},
                )
            prev = b

    for i, p in enumerate(root["providers"]):
        strict_asc(p["platformIds"], path=f"$.providers[{i}].platformIds")
    for i, a in enumerate(root["coverageForAbsent"]):
        strict_asc(a["relationIds"], path=f"$.coverageForAbsent[{i}].relationIds")
    strict_asc([p["providerId"] for p in root["providers"]], path="$.providers")
    strict_asc([a["providerId"] for a in root["coverageForAbsent"]], path="$.coverageForAbsent")


def admit(manifest: Any) -> dict:
    """Run four gates in published order. First observed refusal is the exception.

    Later hypothesized checks are not run.
    """
    _adm_type(manifest)
    root = _adm_closed(manifest)
    _adm_domain(root)
    _adm_order(root)
    return {"ok": True, "manifest": root, "gatePassed": list(GATE_ORDER)}


def first_refusal(manifest: Any) -> dict:
    try:
        r = admit(manifest)
        return {"ok": True, "masksLater": False, "remainingGatesMasked": [], **r}
    except AdmissionError as e:
        later = []
        if e.code in GATE_ORDER:
            later = list(GATE_ORDER[GATE_ORDER.index(e.code) + 1 :])
        return {
            "ok": False,
            "firstRefusal": e.as_dict(),
            "gate": e.code,
            "masksLater": bool(later),
            "remainingGatesMasked": later,
            "note": "Subsequent gates are not executed after first refusal.",
        }


def capability_manifest_id(manifest: Any) -> dict:
    admitted = admit(manifest)
    committed = cve1_encode(admitted["manifest"])
    digest = hashlib.sha256(b"opensip.capability-manifest.v1\x00" + committed).hexdigest()
    return {
        "ok": True,
        "capabilityManifestId": digest,
        "committedBytesHex": committed.hex(),
        "committedBytesLength": len(committed),
        "recipe": 'hex(SHA-256(UTF8("opensip.capability-manifest.v1") || 0x00 || CVE1(CapabilityManifestV1)))',
        "textForm": "^[0-9a-f]{64}$",
        "schemaVersion": admitted["manifest"]["schemaVersion"],
    }
