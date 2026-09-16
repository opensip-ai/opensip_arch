"""Reviewer-independent maximal owner-valid StepTermination (review-04): constructed by hand from common:3 limits (not build_owner),
using 6-byte canonical escapes (U+0001..U+001F) for every bounded string, validated against the pinned owner schema and the owner codec."""
import copy, hashlib, json, sys
from pathlib import Path
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
SUBJ = Path("/tmp/opensip-implementation/m1-report-projection-subject-04")
pins = {p["path"]: p for p in json.loads((SUBJ / "source-pins.json").read_bytes())["files"]}
def pinned(path):
    raw = Path(path).read_bytes(); pin = pins[str(path)]
    assert hashlib.sha256(raw).hexdigest() == pin["sha256"]
    return raw
def load_source(name, path):
    m = type(sys)(name); m.__file__ = str(path); exec(compile(pinned(path), str(path), "exec"), m.__dict__); return m
cm = load_source("cm", ARCH / "docs/implementation/m1/metadata-v2/check_metadata.py")
reference, registry, documents = cm.load(ARCH)
C = "urn:opensip:product-v1:workflows:evaluator3:common:3#/$defs/"
common = documents["urn:opensip:product-v1:workflows:evaluator3:common:3"]["$defs"]
canon = lambda v: json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
CTRL = [chr(c) for c in range(1, 32)]
def ctrl_text(n, index=None, width=3):
    head = ""
    if index is not None:
        digits = []
        for _ in range(width):
            digits.append(CTRL[index % 31]); index //= 31
        head = "".join(reversed(digits))
    return head + CTRL[0] * (n - len(head))
pin_def = common["PinnedPurgeDisclosure"]
max_pins = pin_def["properties"]["activePins"]["maxItems"]
pin_len = pin_def["properties"]["activePins"]["items"]["properties"]["pinId"]["maxLength"]
kinds = pin_def["properties"]["activePins"]["items"]["properties"]["kind"]["enum"]
text_len = common["BoundedText"]["maxLength"]
run = "run3:" + "f" * 64
def termination(pins_n, chars=ctrl_text):
    pins_list = sorted([{"pinId": chars(pin_len, i), "kind": max(kinds, key=len)} for i in range(pins_n)], key=lambda p: p["pinId"].encode())
    return {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "authority": "authoritative", "runId": run,
            "executionId": "exec1_" + "f" * 32, "coverageId": "coverage2:" + "f" * 64,
            "domainDetail": {"code": "evidence.pinned", "remedy": chars(text_len), "subject": chars(text_len),
                             "purgeDisclosure": {"runId": run, "activePins": pins_list, "consequences": pin_def["properties"]["consequences"]["const"]}}}
out = {"limits": {"activePinsMaxItems": max_pins, "pinIdMaxLength": pin_len, "boundedTextMaxLength": text_len, "longestPinKind": max(kinds, key=len)}}
t = termination(max_pins)
raw = canon(t)
try:
    reference.validate({"$ref": C + "StepTermination"}, t, registry); schema_ok = True
except Exception as exc:
    schema_ok = "invalid: " + str(exc).splitlines()[0][:200]
try:
    reference.typed(t); typed_ok = True
except Exception as exc:
    typed_ok = type(exc).__name__ + ": " + str(exc)[:120]
try:
    reference.parse(raw); codec = "accepted"
except Exception as exc:
    codec = type(exc).__name__ + ": " + str(exc)[:120]
derivations = json.loads((SUBJ / "owner/budget-derivations.v1.json").read_bytes())
out["maximalStepTermination"] = {"bytes": len(raw), "ownerSchemaValid": schema_ok, "ownerTypedValid": typed_ok, "ownerCanonicalCodec(canonical.parse)": codec,
                                  "authorStructuralBound": derivations["stepTerminationStructuralMaxBytes"], "slackBytes": derivations["stepTerminationStructuralMaxBytes"] - len(raw),
                                  "boundHolds": len(raw) <= derivations["stepTerminationStructuralMaxBytes"]}
pd = t["domainDetail"]["purgeDisclosure"]
out["maximalPinnedPurgeDisclosure"] = {"bytes": len(canon(pd)), "authorStructuralBound": derivations["pinnedPurgeDisclosureStructuralMaxBytes"]}
# which structural terms are unreachable (mutually exclusive branch members counted by the structural walk)
excl = {"signal": "interrupted only", "reasonCodes": "indeterminate only", "faultCause": "operational-failed only"}
out["structuralCountsMutuallyExclusiveMembers"] = excl
# 4-byte (non-escaped) alternative for comparison
wide = lambda n, index=None: (("%04d" % index) if index is not None else "") + "\U0001F600" * (n - (4 if index is not None else 0))
out["fourByteVariantBytes"] = len(canon(termination(max_pins, wide)))
Path(__file__).with_name("maxima_independent.json").write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps(out, indent=1))
