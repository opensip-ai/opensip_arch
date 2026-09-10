"""Capability-manifest admission (ADM-TYPE, ADM-CLOSED, ADM-DOMAIN, ADM-ORDER) then CVE1 identity.

Owners:
- identity-and-evidence.md §3 (effective registry + four gates)
- native/capability-manifest-domains.v2.json
- delivery.v4.json derivedFrom.operations[17] CAP-MANIFEST-ID-V1
"""
from __future__ import annotations

from typing import Any

from .codec import AdmissionError, capability_manifest_id, encode_cve1

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

RELATIONS = [
    "calls",
    "clones",
    "control-flow",
    "declares",
    "file",
    "imports",
    "literal",
    "package",
    "reachability",
    "references",
    "types",
    "unresolved-edge",
    "vcs-change",
]
RELATION_SET = set(RELATIONS)

LADDERS = {
    "calls": ["syntactic-callee-name", "resolved-callee"],
    "clones": ["normalized-body-hash"],
    "control-flow": ["syntactic"],
    "declares": ["syntactic"],
    "file": ["enumerated"],
    "imports": ["syntactic-specifier", "resolved-target"],
    "literal": ["syntactic"],
    "package": ["manifest-declared"],
    "reachability": ["from-resolved-calls"],
    "references": ["syntactic-name-match", "resolved-binding"],
    "types": ["annotated", "checked"],
    "unresolved-edge": ["observed"],
    "vcs-change": ["vcs-reported"],
}

PLATFORMS = {
    "all-supported",
    "linux-x86_64-gnu",
    "linux-aarch64-gnu",
    "macos-aarch64",
    "macos-x86_64",
    "windows-x86_64-msvc",
    "windows-aarch64-msvc",
    "linux-x86_64-musl",
}

DEFICIENCIES = {
    "required-relation-missing",
    "provider-unavailable",
    "language-tier-unsupported",
    "budget-exhausted",
    "confidence-floor-unmet",
}

COVERAGE_STATES = {"unavailable"}

GATE_ORDER = ["ADM-TYPE", "ADM-CLOSED", "ADM-DOMAIN", "ADM-ORDER"]


def _is_exact_int(x: Any) -> bool:
    return type(x) is int  # noqa: E721 — ADM-TYPE: bool is not an integer


def _is_str(x: Any) -> bool:
    return type(x) is str  # noqa: E721


def _closed_record(obj: Any, kind: str, path: str, violations: list[dict]) -> None:
    keys = RECORD_KEYS[kind]
    if type(obj) is not dict:
        violations.append({"gate": "ADM-CLOSED", "path": path, "reason": f"{kind} is not a record"})
        return
    got = list(obj.keys())
    if sorted(got) != sorted(keys) or len(got) != len(keys):
        violations.append(
            {
                "gate": "ADM-CLOSED",
                "path": path,
                "reason": f"{kind} key set {got} != {keys}",
            }
        )


def _utf8_asc_unique(items: list[str], path: str, violations: list[dict]) -> None:
    prev = None
    for i, s in enumerate(items):
        if not _is_str(s):
            continue
        b = s.encode("utf-8")
        if prev is not None and b <= prev:
            violations.append(
                {
                    "gate": "ADM-ORDER",
                    "path": f"{path}[{i}]",
                    "reason": "not strictly ascending unique NFC UTF-8 bytes",
                    "code": "RELEASE.CAPABILITY_MANIFEST_NOT_CANONICAL",
                }
            )
            return
        prev = b


def admit_capability_manifest(obj: Any) -> dict:
    """Run the four gates in declared order. First-violation list uses declared traversal.

    Traversal for ADM-ORDER diagnostics: (1) providers[i].platformIds;
    (2) coverageForAbsent[i].relationIds; (3) providers; (4) coverageForAbsent.
    """
    violations: list[dict] = []

    # ADM-TYPE
    def t_int(x, path):
        if not _is_exact_int(x):
            violations.append({"gate": "ADM-TYPE", "path": path, "reason": f"not exact JSON integer (got {type(x).__name__})"})

    def t_str(x, path):
        if not _is_str(x):
            violations.append({"gate": "ADM-TYPE", "path": path, "reason": f"not exact JSON string (got {type(x).__name__})"})

    if type(obj) is not dict:
        raise AdmissionError("ADM-TYPE", "manifest is not a JSON object", gate="ADM-TYPE")

    t_int(obj.get("schemaVersion"), "$.schemaVersion")
    t_str(obj.get("profile"), "$.profile")
    providers = obj.get("providers")
    absent = obj.get("coverageForAbsent")
    if type(providers) is not list:
        violations.append({"gate": "ADM-TYPE", "path": "$.providers", "reason": "providers is not an array"})
        providers = []
    if type(absent) is not list:
        violations.append({"gate": "ADM-TYPE", "path": "$.coverageForAbsent", "reason": "coverageForAbsent is not an array"})
        absent = []

    for i, p in enumerate(providers):
        if type(p) is not dict:
            violations.append({"gate": "ADM-TYPE", "path": f"$.providers[{i}]", "reason": "not an object"})
            continue
        for k in ("providerId", "language", "providerVersionSource", "toolchainIdentitySource"):
            t_str(p.get(k), f"$.providers[{i}].{k}")
        plats = p.get("platformIds")
        if type(plats) is not list:
            violations.append({"gate": "ADM-TYPE", "path": f"$.providers[{i}].platformIds", "reason": "not an array"})
        else:
            for j, plat in enumerate(plats):
                t_str(plat, f"$.providers[{i}].platformIds[{j}]")
        rels = p.get("relations")
        if type(rels) is not dict:
            violations.append({"gate": "ADM-TYPE", "path": f"$.providers[{i}].relations", "reason": "relations is not a map"})
        else:
            for rk, rv in rels.items():
                t_str(rk, f"$.providers[{i}].relations key")
                t_str(rv, f"$.providers[{i}].relations.{rk}")

    for i, a in enumerate(absent):
        if type(a) is not dict:
            violations.append({"gate": "ADM-TYPE", "path": f"$.coverageForAbsent[{i}]", "reason": "not an object"})
            continue
        for k in ("providerId", "language", "coverageState", "deficiency"):
            t_str(a.get(k), f"$.coverageForAbsent[{i}].{k}")
        rids = a.get("relationIds")
        if type(rids) is not list:
            violations.append({"gate": "ADM-TYPE", "path": f"$.coverageForAbsent[{i}].relationIds", "reason": "not an array"})
        else:
            for j, r in enumerate(rids):
                t_str(r, f"$.coverageForAbsent[{i}].relationIds[{j}]")

    type_hits = [v for v in violations if v["gate"] == "ADM-TYPE"]
    if type_hits:
        return {"admitted": False, "firstGate": "ADM-TYPE", "violations": violations, "masksLater": GATE_ORDER[1:]}

    # ADM-CLOSED
    _closed_record(obj, "CapabilityManifestV1", "$", violations)
    for i, p in enumerate(providers):
        _closed_record(p, "ProviderCapability", f"$.providers[{i}]", violations)
        # relations is a MAP, not a record — no key set
    for i, a in enumerate(absent):
        _closed_record(a, "AbsentCapability", f"$.coverageForAbsent[{i}]", violations)
    closed_hits = [v for v in violations if v["gate"] == "ADM-CLOSED"]
    if closed_hits:
        return {"admitted": False, "firstGate": "ADM-CLOSED", "violations": violations, "masksLater": GATE_ORDER[2:]}

    # ADM-DOMAIN
    for i, p in enumerate(providers):
        for plat in p.get("platformIds") or []:
            if plat not in PLATFORMS:
                violations.append(
                    {
                        "gate": "ADM-DOMAIN",
                        "path": f"$.providers[{i}].platformIds",
                        "reason": f"{plat!r} not in PLATFORM-ID-DOMAIN-V1",
                    }
                )
        rels = p.get("relations") or {}
        for rk, rv in rels.items():
            if rk not in RELATION_SET:
                violations.append(
                    {
                        "gate": "ADM-DOMAIN",
                        "path": f"$.providers[{i}].relations",
                        "reason": f"relation key {rk!r} not in RELATION-DOMAIN-V2",
                    }
                )
            else:
                ladder = LADDERS[rk]
                if rv not in ladder:
                    violations.append(
                        {
                            "gate": "ADM-DOMAIN",
                            "path": f"$.providers[{i}].relations.{rk}",
                            "reason": f"rung {rv!r} not in RELATION-LADDER-DOMAIN-V2 for {rk}",
                        }
                    )
    for i, a in enumerate(absent):
        for r in a.get("relationIds") or []:
            if r not in RELATION_SET:
                violations.append(
                    {
                        "gate": "ADM-DOMAIN",
                        "path": f"$.coverageForAbsent[{i}].relationIds",
                        "reason": f"{r!r} not in RELATION-DOMAIN-V2",
                    }
                )
        if a.get("coverageState") not in COVERAGE_STATES:
            violations.append(
                {
                    "gate": "ADM-DOMAIN",
                    "path": f"$.coverageForAbsent[{i}].coverageState",
                    "reason": f"{a.get('coverageState')!r} not in COVERAGE-STATE-DOMAIN-V1",
                }
            )
        if a.get("deficiency") not in DEFICIENCIES:
            violations.append(
                {
                    "gate": "ADM-DOMAIN",
                    "path": f"$.coverageForAbsent[{i}].deficiency",
                    "reason": f"{a.get('deficiency')!r} not in DEFICIENCY-DOMAIN-V1",
                }
            )
    domain_hits = [v for v in violations if v["gate"] == "ADM-DOMAIN"]
    if domain_hits:
        return {"admitted": False, "firstGate": "ADM-DOMAIN", "violations": violations, "masksLater": GATE_ORDER[3:]}

    # ADM-ORDER (declared traversal)
    for i, p in enumerate(providers):
        _utf8_asc_unique(list(p.get("platformIds") or []), f"$.providers[{i}].platformIds", violations)
    for i, a in enumerate(absent):
        _utf8_asc_unique(list(a.get("relationIds") or []), f"$.coverageForAbsent[{i}].relationIds", violations)
    _utf8_asc_unique([p.get("providerId") for p in providers], "$.providers", violations)
    _utf8_asc_unique([a.get("providerId") for a in absent], "$.coverageForAbsent", violations)

    order_hits = [v for v in violations if v["gate"] == "ADM-ORDER"]
    if order_hits:
        return {"admitted": False, "firstGate": "ADM-ORDER", "violations": violations, "masksLater": []}

    committed = encode_cve1(obj)
    ident = capability_manifest_id(committed)
    return {
        "admitted": True,
        "firstGate": None,
        "violations": [],
        "masksLater": [],
        "committedBytes": committed,
        "capabilityManifestId": ident,
        "capabilityManifestBytesDigest": __import__("hashlib").sha256(committed).hexdigest(),
    }


def minimal_manifest(*, profile: str, providers: list[dict], coverage_for_absent: list[dict] | None = None) -> dict:
    return {
        "schemaVersion": 1,
        "profile": profile,
        "providers": providers,
        "coverageForAbsent": coverage_for_absent or [],
    }
