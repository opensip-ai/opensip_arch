"""Law 8: are the two baseline-scope public details actually carriable?

A Refusal whose detail code is absent from BOTH the closed public-detail registry and
the mirrored StepTermination enum cannot be published. This checks registry membership,
schema enum membership, agreement between them, and the claimed count of 289.
"""
import json
import os
import re
import sys

ROOT = sys.argv[1]
DC = os.path.join(ROOT, "docs/coop/design-corrections")
TARGETS = [
    "BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER",
    "BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH",
]

reg = json.load(open(os.path.join(DC, "public-detail-registry.v1.json")))
common = json.load(open(os.path.join(DC, "workflows/schemas/common.schema.json")))


def collect_codes(obj, acc):
    """Registry codes may be keys or 'code' fields; collect both shapes."""
    if isinstance(obj, dict):
        if "code" in obj and isinstance(obj["code"], str):
            acc.add(obj["code"])
        for k, v in obj.items():
            if re.fullmatch(r"[A-Z][A-Z0-9_]*\.[A-Z0-9_]+", k):
                acc.add(k)
            collect_codes(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            collect_codes(v, acc)


reg_codes = set()
collect_codes(reg, reg_codes)


def find_enums(obj, path=""):
    if isinstance(obj, dict):
        if "enum" in obj and isinstance(obj["enum"], list):
            yield (path, obj["enum"])
        for k, v in obj.items():
            yield from find_enums(v, f"{path}/{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from find_enums(v, f"{path}/{i}")


enums = list(find_enums(common))
detail_enums = [
    (p, e) for p, e in enums
    if any(isinstance(x, str) and "." in x and x.isupper() for x in e)
]

out = {
    "registryTopKeys": list(reg.keys()),
    "registryCodeCount": len(reg_codes),
    "targets": {},
    "detailEnums": [
        {"path": p, "size": len(e), "containsTargets":
         [t for t in TARGETS if t in e]}
        for p, e in detail_enums
    ],
}

# the mirrored enum: the largest detail-code enum in common.schema.json
if detail_enums:
    biggest = max(detail_enums, key=lambda pe: len(pe[1]))
    out["mirroredEnumPath"] = biggest[0]
    out["mirroredEnumSize"] = len(biggest[1])
    enum_set = set(biggest[1])
    out["registryMinusEnum"] = sorted(reg_codes - enum_set)[:40]
    out["enumMinusRegistry"] = sorted(enum_set - reg_codes)[:40]
    out["registryMinusEnumCount"] = len(reg_codes - enum_set)
    out["enumMinusRegistryCount"] = len(enum_set - reg_codes)
else:
    enum_set = set()

for t in TARGETS:
    out["targets"][t] = {
        "inRegistry": t in reg_codes,
        "inMirroredEnum": t in enum_set,
    }

print(json.dumps(out, indent=2))
