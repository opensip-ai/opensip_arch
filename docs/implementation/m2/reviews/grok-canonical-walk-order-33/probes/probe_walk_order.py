"""Permutations of one canonical object: hashes vs first-fault walk order."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
C_PATH = ARCH / "docs/coop/design-corrections/foundation/canonical.py"
I_PATH = (
    ARCH
    / "docs/implementation/m2/stage-meta-reference-selection-v1/reference/identity_model.py"
)
OUT = Path("/tmp/opensip-implementation/m2-grok-canonical-walk-order-33/review/probes")
INSERTION = Path(
    "/tmp/opensip-implementation/m2-full-walk-trial-32/initial-insertion-order-oracle/shared-result.json"
)
CURRENT = Path("/tmp/opensip-implementation/m2-full-walk-trial-32/shared-result.json")


def load_c():
    spec = importlib.util.spec_from_file_location("probe_canonical", C_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def walk_undeclared(value, *, sorted_keys=False):
    """Clone of selected identity_model walk 973–983 for a digest-carrying object."""
    items = sorted(value.items()) if sorted_keys else list(value.items())
    for name, _item in items:
        raise RuntimeError("UNDECLARED_PROPERTY:" + name)


def main():
    C = load_c()
    a = {"zzz": 1, "aaa": 2}
    b = {"aaa": 2, "zzz": 1}
    ca, cb = C.canonical(a), C.canonical(b)
    pa, pb = C.parse(ca), C.parse(cb)
    first_raw = []
    for label, obj in (("zzz-then-aaa", a), ("aaa-then-zzz", b)):
        try:
            walk_undeclared(obj, sorted_keys=False)
        except RuntimeError as exc:
            first_raw.append({"label": label, "keys": list(obj), "firstFault": str(exc)})
    first_proj = []
    for label, obj in (("zzz-then-aaa", pa), ("aaa-then-zzz", pb)):
        try:
            walk_undeclared(obj, sorted_keys=False)
        except RuntimeError as exc:
            first_proj.append({"label": label, "keys": list(obj), "firstFault": str(exc)})
    first_explicit = []
    for label, obj in (("zzz-then-aaa", a), ("aaa-then-zzz", b)):
        try:
            walk_undeclared(obj, sorted_keys=True)
        except RuntimeError as exc:
            first_explicit.append({"label": label, "firstFault": str(exc)})

    hid = lambda v: hashlib.sha256(
        b"opensip.product.v1\0fact\0" + len(C.canonical(v)).to_bytes(8, "big") + C.canonical(v)
    ).hexdigest()

    insertion = json.loads(INSERTION.read_bytes())
    current = json.loads(CURRENT.read_bytes())
    report = {
        "selectedIdentity": {
            "path": str(I_PATH.relative_to(ARCH)),
            "bytes": I_PATH.stat().st_size,
            "sha256": hashlib.sha256(I_PATH.read_bytes()).hexdigest(),
            "walkItems": "950-983 value.items() insertion order",
        },
        "canonicalBytesEqual": ca == cb,
        "canonicalUtf8": ca.decode(),
        "parseCanonicalKeyOrder": [list(pa), list(pb)],
        "btreeEquivalentKeyOrder": sorted(a),
        "identityHexEqual": hid(a) == hid(b),
        "firstFaultRawInsertion": first_raw,
        "firstFaultAfterParseCanonical": first_proj,
        "firstFaultExplicitSortedWalk": first_explicit,
        "rawFirstFaultsDiffer": first_raw[0]["firstFault"] != first_raw[1]["firstFault"],
        "projectionFirstFaultsAgree": first_proj[0]["firstFault"] == first_proj[1]["firstFault"],
        "projectionMatchesUtf8KeyOrder": first_proj[0]["firstFault"] == "UNDECLARED_PROPERTY:aaa",
        "preservedInsertionOracleMismatches": insertion.get("mismatches"),
        "currentSharedMismatches": current.get("mismatches"),
        "currentSharedDistribution": current.get("distribution"),
        "currentScope": current.get("scope"),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "probe-results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in report if k not in ("canonicalUtf8", "currentScope")}, indent=2))


if __name__ == "__main__":
    main()
