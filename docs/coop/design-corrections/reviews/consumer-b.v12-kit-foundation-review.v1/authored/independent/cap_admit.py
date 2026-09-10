"""Capability-manifest admission BEFORE encoding.

Gate order from capability-manifest-domains.v2.json: ADM-TYPE, ADM-CLOSED,
ADM-DOMAIN, ADM-ORDER. Recipe CAP-MANIFEST-ID-V1 from the same document and
delivery.v4. Not the consumer helper.
"""
from __future__ import annotations

import copy
from typing import Any

from independent.kit_core import AdmissionError, capability_manifest_id_from_bytes, cve1_encode
from independent.schema_and_order import load_json

REG = load_json("native/capability-manifest-domains.v2.json")
GATE_ORDER = list(REG["gateOrder"])
RECORD_KEYS = {
    name: spec["requiredKeys"]
    for name, spec in REG["recordShape"].items()
    if isinstance(spec, dict) and spec.get("kind") == "RECORD"
}
PLATFORMS = set(REG["registries"]["PLATFORM-ID-DOMAIN-V1"]["members"])
RELATIONS = set(REG["registries"]["RELATION-DOMAIN-V2"]["members"])
LADDERS = REG["registries"]["RELATION-LADDER-DOMAIN-V2"]["ladders"]
DEFICIENCIES = set(REG["registries"]["DEFICIENCY-DOMAIN-V1"]["members"])
COV_STATES = set(REG["registries"]["COVERAGE-STATE-DOMAIN-V1"]["members"])


def _type_name(x: Any) -> str:
    if type(x) is bool:
        return "bool"
    if type(x) is int:
        return "int"
    if type(x) is str:
        return "str"
    if type(x) is list:
        return "list"
    if type(x) is dict:
        return "dict"
    if x is None:
        return "null"
    return type(x).__name__


def _adm_type(manifest: dict) -> None:
    if type(manifest.get("schemaVersion")) is not int or type(manifest.get("schemaVersion")) is bool:
        # bool is a subclass of int in Python; exact JSON integer forbids bool
        if type(manifest.get("schemaVersion")) is bool or type(manifest.get("schemaVersion")) is not int:
            raise AdmissionError(
                "ADM-TYPE",
                f"$.schemaVersion: exact JSON integer required; {_type_name(manifest.get('schemaVersion'))} is not an integer",
                path="$.schemaVersion",
            )
    for k in ("profile",):
        if k in manifest and type(manifest[k]) is not str:
            raise AdmissionError("ADM-TYPE", f"$.{k}: exact JSON string required", path=f"$.{k}")
    for i, p in enumerate(manifest.get("providers") or []):
        if type(p) is not dict:
            raise AdmissionError("ADM-TYPE", f"$.providers[{i}] not object", path=f"$.providers[{i}]")
        for k in ("providerId", "language", "providerVersionSource", "toolchainIdentitySource"):
            if k in p and type(p[k]) is not str:
                raise AdmissionError("ADM-TYPE", f"$.providers[{i}].{k}: string", path=f"$.providers[{i}].{k}")
        if "platformIds" in p:
            if type(p["platformIds"]) is not list:
                raise AdmissionError("ADM-TYPE", "platformIds array", path=f"$.providers[{i}].platformIds")
            for j, pid in enumerate(p["platformIds"]):
                if type(pid) is not str:
                    raise AdmissionError("ADM-TYPE", "platformId string", path=f"$.providers[{i}].platformIds[{j}]")
        if "relations" in p:
            if type(p["relations"]) is not dict:
                raise AdmissionError("ADM-TYPE", "relations map", path=f"$.providers[{i}].relations")
            for rk, rv in p["relations"].items():
                if type(rk) is not str or type(rv) is not str:
                    raise AdmissionError("ADM-TYPE", "relation key/value strings", path=f"$.providers[{i}].relations")
    for i, a in enumerate(manifest.get("coverageForAbsent") or []):
        if type(a) is not dict:
            raise AdmissionError("ADM-TYPE", "absent record", path=f"$.coverageForAbsent[{i}]")
        for k in ("providerId", "language", "coverageState", "deficiency"):
            if k in a and type(a[k]) is not str:
                raise AdmissionError("ADM-TYPE", f"{k} string", path=f"$.coverageForAbsent[{i}].{k}")


def _closed(obj: dict, keys: list[str], path: str) -> None:
    got = list(obj.keys())
    if set(got) != set(keys) or len(got) != len(keys):
        raise AdmissionError(
            "ADM-CLOSED",
            f"{path}: closed key set {keys} got {got}",
            path=path,
            extra={"expected": keys, "got": got},
        )


def _adm_closed(manifest: dict) -> None:
    _closed(manifest, RECORD_KEYS["CapabilityManifestV1"], "$")
    for i, p in enumerate(manifest["providers"]):
        _closed(p, RECORD_KEYS["ProviderCapability"], f"$.providers[{i}]")
    for i, a in enumerate(manifest["coverageForAbsent"]):
        _closed(a, RECORD_KEYS["AbsentCapability"], f"$.coverageForAbsent[{i}]")


def _adm_domain(manifest: dict) -> None:
    for i, p in enumerate(manifest["providers"]):
        for j, pid in enumerate(p["platformIds"]):
            if pid not in PLATFORMS:
                raise AdmissionError(
                    "ADM-DOMAIN",
                    f"$.providers[{i}].platformIds[{j}]: platformId not in PLATFORM-ID-DOMAIN-V1",
                    path=f"$.providers[{i}].platformIds[{j}]",
                    extra={"value": pid},
                )
        for rel, rung in p["relations"].items():
            if rel not in RELATIONS:
                raise AdmissionError(
                    "ADM-DOMAIN",
                    f"$.providers[{i}].relations key {rel!r} not in RELATION-DOMAIN-V2",
                    path=f"$.providers[{i}].relations",
                    extra={"relation": rel},
                )
            ladder = LADDERS[rel]
            if rung not in ladder:
                raise AdmissionError(
                    "ADM-DOMAIN",
                    f"$.providers[{i}].relations[{rel!r}]: rung {rung!r} is not a member of {rel} ladder",
                    path=f"$.providers[{i}].relations[{rel!r}]",
                    extra={"relation": rel, "rung": rung, "ladder": ladder},
                )
    for i, a in enumerate(manifest["coverageForAbsent"]):
        if a["coverageState"] not in COV_STATES:
            raise AdmissionError("ADM-DOMAIN", "coverageState", path=f"$.coverageForAbsent[{i}].coverageState")
        if a["deficiency"] not in DEFICIENCIES:
            raise AdmissionError("ADM-DOMAIN", "deficiency", path=f"$.coverageForAbsent[{i}].deficiency")
        for j, rid in enumerate(a["relationIds"]):
            if rid not in RELATIONS:
                raise AdmissionError("ADM-DOMAIN", "relationId", path=f"$.coverageForAbsent[{i}].relationIds[{j}]")


def _utf8_sorted(vals: list[str]) -> bool:
    b = [v.encode("utf-8") for v in vals]
    return b == sorted(b) and len(b) == len(set(b))


def _adm_order(manifest: dict) -> None:
    # Traversal: (1) each providers[i].platformIds (2) each coverageForAbsent[i].relationIds
    # (3) providers by providerId (4) coverageForAbsent by providerId
    for i, p in enumerate(manifest["providers"]):
        ids = p["platformIds"]
        if not _utf8_sorted(ids):
            # first offending value in declared order
            prev = None
            for v in ids:
                if prev is not None and v.encode("utf-8") <= prev.encode("utf-8"):
                    raise AdmissionError(
                        "ADM-ORDER",
                        f"$.providers[{i}].platformIds: not strictly ascending NFC UTF-8 ({v!r})",
                        path=f"$.providers[{i}].platformIds",
                        extra={"value": v},
                    )
                prev = v
            raise AdmissionError("ADM-ORDER", f"$.providers[{i}].platformIds", path=f"$.providers[{i}].platformIds")
    for i, a in enumerate(manifest["coverageForAbsent"]):
        if not _utf8_sorted(a["relationIds"]):
            raise AdmissionError("ADM-ORDER", f"$.coverageForAbsent[{i}].relationIds", path=f"$.coverageForAbsent[{i}].relationIds")
    pids = [p["providerId"] for p in manifest["providers"]]
    if not _utf8_sorted(pids):
        prev = None
        for v in pids:
            if prev is not None and v.encode("utf-8") <= prev.encode("utf-8"):
                raise AdmissionError(
                    "ADM-ORDER",
                    f"$.providers: not strictly ascending NFC UTF-8 ({v!r})",
                    path="$.providers",
                    extra={"value": v},
                )
            prev = v
        raise AdmissionError("ADM-ORDER", "$.providers", path="$.providers")
    aids = [a["providerId"] for a in manifest["coverageForAbsent"]]
    if not _utf8_sorted(aids):
        raise AdmissionError("ADM-ORDER", "$.coverageForAbsent", path="$.coverageForAbsent")


GATES = {
    "ADM-TYPE": _adm_type,
    "ADM-CLOSED": _adm_closed,
    "ADM-DOMAIN": _adm_domain,
    "ADM-ORDER": _adm_order,
}


def first_refusal(manifest: dict) -> dict:
    remaining = list(GATE_ORDER)
    for gate in GATE_ORDER:
        remaining = remaining[1:]
        try:
            GATES[gate](manifest)
        except AdmissionError as e:
            return {
                "ok": False,
                "gate": gate,
                "firstRefusal": e.as_dict(),
                "masksLater": bool(remaining),
                "remainingGatesMasked": list(remaining),
            }
    committed = cve1_encode(manifest)
    cid = capability_manifest_id_from_bytes(committed)
    return {"ok": True, "capabilityManifestId": cid, "committedBytesHex": committed.hex(), "gateOrder": GATE_ORDER}


def admit(manifest: dict) -> dict:
    return first_refusal(copy.deepcopy(manifest))
