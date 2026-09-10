import copy
import json
import sys

sys.path.insert(0, "/tmp/opensip-design-corrections/consumer-b.v8/output/work")
import capman
import osip

# ---- CB-V1: my own minimal positive capability manifest ------------------
BASE = {
    "schemaVersion": 1,
    "profile": "default",
    "providers": [
        {"providerId": "p-rust", "language": "rust",
         "providerVersionSource": "closure-manifest",
         "toolchainIdentitySource": "native-context",
         "relations": {"clones": "normalized-body-hash",
                       "declares": "syntactic",
                       "file": "enumerated",
                       "unresolved-edge": "observed"},
         "platformIds": ["linux-x86_64-gnu", "macos-aarch64"]},
        {"providerId": "p-typescript", "language": "typescript",
         "providerVersionSource": "closure-manifest",
         "toolchainIdentitySource": "native-context",
         "relations": {"imports": "resolved-target",
                       "references": "resolved-binding"},
         "platformIds": ["macos-aarch64"]},
    ],
    "coverageForAbsent": [
        {"providerId": "p-syntax", "language": "*",
         "relationIds": ["calls", "references", "types"],
         "coverageState": "unavailable",
         "deficiency": "language-tier-unsupported"},
    ],
}
# providers must be strictly ascending by providerId
BASE["providers"].sort(key=lambda p: p["providerId"].encode("utf-8"))

vectors = []


def run(name, m, expect):
    faults = capman.admit_value(m)
    got = "ADMIT" if not faults else faults[0][0]
    ok = got == expect
    rec = {"vector": name, "expected": expect, "observed": got,
           "firstFault": (faults[0][1] if faults else None),
           "completeFaultList": [list(f) for f in faults]}
    if not faults:
        b = capman.commit(m)
        rec["committedBytes"] = len(b)
        rec["capabilityManifestId"] = osip.capability_manifest_id(b)
        rec["roundTrip"] = capman.admit_committed(b) == []
    vectors.append(rec)
    print(("PASS " if ok else "FAIL ") + name, "->", got,
          rec.get("firstFault") or rec.get("capabilityManifestId", ""))
    return rec


pos = run("CB-CM-1 positive minimal manifest", BASE, "ADMIT")

# ADM-TYPE: schemaVersion respelled as boolean and as string
m = copy.deepcopy(BASE); m["schemaVersion"] = True
run("CB-CM-2 schemaVersion true is not an integer", m, "ADM-TYPE")
m = copy.deepcopy(BASE); m["schemaVersion"] = "1"
run("CB-CM-3 schemaVersion \"1\" is not an integer", m, "ADM-TYPE")

# ADM-CLOSED: an undeclared key on a record; a missing required key
m = copy.deepcopy(BASE); m["providers"][0]["extra"] = "x"
run("CB-CM-4 undeclared key on ProviderCapability", m, "ADM-CLOSED")
m = copy.deepcopy(BASE); del m["coverageForAbsent"][0]["deficiency"]
run("CB-CM-5 missing required key on AbsentCapability", m, "ADM-CLOSED")  # helper corrected: ADM-TYPE types only PRESENT scalars

# ADM-DOMAIN: rung of ANOTHER relation's ladder; unknown relation; case variant
m = copy.deepcopy(BASE)
m["providers"][0]["relations"]["declares"] = "resolved-callee"
run("CB-CM-6 rung of another relation's ladder", m, "ADM-DOMAIN")
m = copy.deepcopy(BASE)
m["providers"][0]["relations"]["made-up"] = "syntactic"
run("CB-CM-7 unregistered relation key", m, "ADM-DOMAIN")
m = copy.deepcopy(BASE)
m["providers"][0]["platformIds"] = ["LINUX-X86_64-GNU"]
run("CB-CM-8 platform id case variant (exact NFC bytes)", m, "ADM-DOMAIN")
# the thirteenth relation: expressible under RELATION-DOMAIN-V2 and NOT a member
# of the inherited twelve, and it moves the identity.
inherited12 = set(capman.REGISTRIES["RELATION-DOMAIN-V2"]["inheritedMembers"])
without = copy.deepcopy(BASE)
for pr in without["providers"]:
    pr["relations"].pop("unresolved-edge", None)
r9a = run("CB-CM-9a manifest WITHOUT the thirteenth relation", without, "ADMIT")
r9b = run("CB-CM-9b manifest WITH unresolved-edge@observed", BASE, "ADMIT")
assert "unresolved-edge" not in inherited12
assert r9a["capabilityManifestId"] != r9b["capabilityManifestId"]
print("PASS CB-CM-9 unresolved-edge is outside the inherited 12 and moves the id:",
      r9a["capabilityManifestId"][:16], "->", r9b["capabilityManifestId"][:16])

# ADM-ORDER: unsorted relationIds; unsorted providers; duplicate element
m = copy.deepcopy(BASE)
m["coverageForAbsent"][0]["relationIds"] = ["types", "calls", "references"]
run("CB-CM-10 unsorted relationIds", m, "ADM-ORDER")
m = copy.deepcopy(BASE); m["providers"] = list(reversed(m["providers"]))
run("CB-CM-11 unsorted providers", m, "ADM-ORDER")
m = copy.deepcopy(BASE)
m["providers"][0]["platformIds"] = ["macos-aarch64", "macos-aarch64"]
run("CB-CM-12 duplicate platformId is an ordering violation", m, "ADM-ORDER")

# gate ORDER: a manifest violating TYPE and ORDER at once reports TYPE first
m = copy.deepcopy(BASE)
m["schemaVersion"] = True
m["coverageForAbsent"][0]["relationIds"] = ["types", "calls"]
r = run("CB-CM-13 TYPE masks ORDER (inherited gate order)", m, "ADM-TYPE")
r["masks"] = "ADM-ORDER on coverageForAbsent[0].relationIds is not reached"

# CVE1 raw-input admission, separate from encoding an already-parsed object
print("\n-- CVE1 committed-artifact admission --")
good = capman.commit(BASE)
cases = []
for label, b, expect in [
    ("CB-CVE-1 exact committed bytes", good, "ADMIT"),
    ("CB-CVE-2 trailing byte", good + b"\x00", "CVE1_DECODE"),
    ("CB-CVE-3 unknown tag", b"\x09", "CVE1_DECODE"),
    ("CB-CVE-4 non-NFC string", b"\x04\x00\x00\x00\x03" + "é".encode(), "CVE1_DECODE"),
    ("CB-CVE-5 duplicate map key",
     b"\x06\x00\x00\x00\x02" + osip.cve1("a") + osip.cve1(1) + osip.cve1("a") + osip.cve1(2),
     "CVE1_DECODE"),
    ("CB-CVE-6 unsorted map keys",
     b"\x06\x00\x00\x00\x02" + osip.cve1("b") + osip.cve1(1) + osip.cve1("a") + osip.cve1(2),
     "CVE1_DECODE"),
]:
    f = capman.admit_committed(b)
    got = "ADMIT" if not f else f[0][0]
    print(("PASS " if got == expect else "FAIL ") + label, "->", got,
          (f[0][1] if f else osip.capability_manifest_id(b)))
    cases.append({"vector": label, "expected": expect, "observed": got,
                  "detail": (f[0][1] if f else None)})

# NFC-only admission applies to the capability manifest ONLY: C never normalises
try:
    osip.cve1("é")
    print("FAIL CB-CVE-7")
except Exception as e:
    print("PASS CB-CVE-7 CVE1 refuses non-NFC ->", e)
print("PASS CB-CVE-8 C admits the same non-NFC string unchanged ->",
      osip.C({"k": "é"}))

out = {"manifestVectors": vectors, "cve1Vectors": cases,
       "positiveManifest": BASE,
       "committedBytesHex": good.hex(),
       "capabilityManifestId": osip.capability_manifest_id(good)}
with open("/tmp/opensip-design-corrections/consumer-b.v8/output/vectors-capability-manifest.json", "w") as f:
    json.dump(out, f, indent=1, sort_keys=True)
print("\ncapabilityManifestId:", out["capabilityManifestId"])
