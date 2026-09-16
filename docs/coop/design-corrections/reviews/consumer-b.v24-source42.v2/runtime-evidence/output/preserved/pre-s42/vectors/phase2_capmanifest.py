"""Phase 2: capability-manifest admission before encoding (CAP-MANIFEST-ID-V1 with the successor registry)."""
import copy
import json
import sys

sys.path.insert(0, '/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v2/output/preserved/pre-s42/ref')
sys.path.insert(0, '/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v2/output/preserved/pre-s42/tools')
import canonical as K
import cve1
import status as S

ADM = cve1.CapabilityAdmission()
failures = []


def check(c, label):
    if not c:
        failures.append(label)


BASE = {
    "schemaVersion": 1,
    "profile": "consumer-b-mixed",
    "providers": [
        {"providerId": "rust-semantic", "language": "rust", "providerVersionSource": "release-manifest:rust-semantic",
         "toolchainIdentitySource": "release-manifest", "relations": {"calls": "resolved-callee", "imports": "resolved-target",
                                                                     "unresolved-edge": "observed", "types": "checked"},
         "platformIds": ["linux-aarch64-gnu", "macos-aarch64"]},
        {"providerId": "syntax-all", "language": "*", "providerVersionSource": "release-manifest:syntax-grammars",
         "toolchainIdentitySource": "release-manifest", "relations": {"clones": "normalized-body-hash", "declares": "syntactic",
                                                                     "file": "enumerated", "package": "manifest-declared"},
         "platformIds": ["all-supported"]},
    ],
    "coverageForAbsent": [
        {"providerId": "typescript-semantic", "language": "typescript", "relationIds": ["calls", "imports", "references"],
         "coverageState": "unavailable", "deficiency": "provider-unavailable"}
    ]}

vectors = {"positives": [], "negatives": [], "explanatory": []}
pos = ADM.admit(BASE)
vectors["positives"].append({"class": "valid", "name": "mixed provider manifest with unresolved-edge", "manifest": BASE, "admission": pos})
check(pos["result"] == "ADMIT", "base admit")
# reordered JSON keys and map insertion order -> identical committed bytes
perm = {"coverageForAbsent": BASE["coverageForAbsent"], "providers": [
    {k: BASE["providers"][0][k] for k in reversed(list(BASE["providers"][0].keys()))} | {"relations": {"types": "checked", "unresolved-edge": "observed", "imports": "resolved-target", "calls": "resolved-callee"}},
    BASE["providers"][1]], "profile": "consumer-b-mixed", "schemaVersion": 1}
p2 = ADM.admit(perm)
vectors["positives"].append({"class": "valid", "name": "same manifest, different JSON key/map order", "admission": p2,
                             "sameId": p2.get("capabilityManifestId") == pos["capabilityManifestId"]})
check(p2.get("capabilityManifestId") == pos["capabilityManifestId"], "order-free id")
# raw JSON bytes route: lexical admission precedes gates
raw = json.dumps(BASE).encode()
p3 = ADM.admit(K.parse_raw(raw))
vectors["positives"].append({"class": "valid", "name": "raw JSON bytes -> lexical admission -> gates", "sameId": p3["capabilityManifestId"] == pos["capabilityManifestId"]})
# decode committed bytes and re-admit
dec = cve1.decode(bytes.fromhex(pos["committedBytesHex"]))
p4 = ADM.admit(dec)
vectors["positives"].append({"class": "valid", "name": "decode(committed) re-admits to same id", "sameId": p4["capabilityManifestId"] == pos["capabilityManifestId"]})
check(p4["capabilityManifestId"] == pos["capabilityManifestId"], "decode readmit")
# minimal syntax-only manifest used later by the syntax Runs
SYN = {"schemaVersion": 1, "profile": "syntax-only-release",
       "providers": [{"providerId": "syntax-all", "language": "*", "providerVersionSource": "release-manifest:syntax-grammars",
                      "toolchainIdentitySource": "release-manifest",
                      "relations": {"clones": "normalized-body-hash", "control-flow": "syntactic", "declares": "syntactic",
                                    "file": "enumerated", "literal": "syntactic", "package": "manifest-declared", "vcs-change": "vcs-reported"},
                      "platformIds": ["all-supported"]}],
       "coverageForAbsent": [{"providerId": "rust-semantic", "language": "rust", "relationIds": ["calls", "imports", "reachability", "references", "types", "unresolved-edge"],
                              "coverageState": "unavailable", "deficiency": "language-tier-unsupported"},
                             {"providerId": "typescript-semantic", "language": "typescript", "relationIds": ["calls", "imports", "reachability", "references", "types", "unresolved-edge"],
                              "coverageState": "unavailable", "deficiency": "language-tier-unsupported"}]}
ps = ADM.admit(SYN)
vectors["positives"].append({"class": "valid", "name": "syntax-only release manifest", "manifest": SYN, "admission": ps})
check(ps["result"] == "ADMIT", "syntax manifest")


def neg(name, mutate, expected_first, masking_expected=None):
    m = copy.deepcopy(BASE)
    mutate(m)
    r = ADM.admit(m)
    entry = {"class": "invalid", "name": name, "manifest": m, "result": r["result"], "firstRefusal": r.get("firstRefusal"),
             "violations": r.get("violations"), "masksLater": r.get("masksLaterHypothesizedCheck", False),
             "maskedLater": r.get("maskedLater", {}), "domainReasonCode": r.get("domainReasonCode")}
    vectors["negatives"].append(entry)
    check(r["result"] == "REFUSE" and r.get("firstRefusal") == expected_first, f"neg {name}")
    if masking_expected is not None:
        check(entry["masksLater"] == masking_expected, f"masking {name}")
    return entry


# ADM-TYPE
e = neg("schemaVersion boolean true", lambda m: m.__setitem__("schemaVersion", True), "ADM-TYPE", False)
enc_true = cve1.encode(dict(BASE, schemaVersion=True))
vectors["explanatory"].append({"class": "explanatory", "name": "CVE1 is total on booleans: without ADM-TYPE a different id would be minted",
                               "idIfEncoded": cve1.capability_manifest_id(enc_true), "admittedId": pos["capabilityManifestId"],
                               "differs": cve1.capability_manifest_id(enc_true) != pos["capabilityManifestId"]})
neg("schemaVersion numeric string", lambda m: m.__setitem__("schemaVersion", "1"), "ADM-TYPE", False)
neg("schemaVersion parsed float 1.0", lambda m: m.__setitem__("schemaVersion", 1.0), "ADM-TYPE", False)
neg("relation rung not a string", lambda m: m["providers"][0]["relations"].__setitem__("calls", 2), "ADM-TYPE", True)
raw_float = json.dumps(BASE).replace('"schemaVersion": 1', '"schemaVersion": 1.0').encode()
try:
    K.parse_raw(raw_float)
    lexr = None
except K.AdmissionError as exc:
    lexr = exc.boundary
vectors["negatives"].append({"class": "invalid", "name": "raw bytes with 1.0", "firstRefusal": lexr, "masksLater": True,
                             "maskedLater": {"ADM-TYPE": ["$.schemaVersion:expected-integer:float (never reached)"]}})
check(lexr == "LEX_FLOAT_OR_EXPONENT", "raw float")
# ADM-CLOSED
neg("undeclared key in ProviderCapability", lambda m: m["providers"][0].__setitem__("notes", "x"), "ADM-CLOSED", False)
neg("missing platformIds", lambda m: m["providers"][1].pop("platformIds"), "ADM-CLOSED", False)
neg("undeclared top-level key", lambda m: m.__setitem__("releaseChannel", "beta"), "ADM-CLOSED", False)
# ADM-DOMAIN
neg("rung of another relation (calls: syntactic)", lambda m: m["providers"][0]["relations"].__setitem__("calls", "syntactic"), "ADM-DOMAIN", False)
neg("case-variant platform ALL-SUPPORTED", lambda m: m["providers"][1].__setitem__("platformIds", ["ALL-SUPPORTED"]), "ADM-DOMAIN", False)
neg("alias relation key unresolved_edge", lambda m: m["providers"][0]["relations"].__setitem__("unresolved_edge", "observed"), "ADM-DOMAIN", False)
neg("deficiency outside DEFICIENCY-DOMAIN-V1", lambda m: m["coverageForAbsent"][0].__setitem__("deficiency", "input-closure-incomplete"), "ADM-DOMAIN", False)
neg("coverageState other than unavailable", lambda m: m["coverageForAbsent"][0].__setitem__("coverageState", "unknown"), "ADM-DOMAIN", False)
# ADM-ORDER
e = neg("providers not ascending by providerId", lambda m: m.__setitem__("providers", list(reversed(m["providers"]))), "ADM-ORDER", False)
check(e["domainReasonCode"] == "RELEASE.CAPABILITY_MANIFEST_NOT_CANONICAL", "order reason")
neg("platformIds duplicate", lambda m: m["providers"][0].__setitem__("platformIds", ["macos-aarch64", "macos-aarch64"]), "ADM-ORDER", False)
e = neg("relationIds unsorted and providers unsorted (complete list in traversal order)",
        lambda m: (m["coverageForAbsent"][0].__setitem__("relationIds", ["references", "calls"]), m.__setitem__("providers", list(reversed(m["providers"])))),
        "ADM-ORDER", False)
check(len(e["violations"]) == 2 and e["violations"][0].startswith("$.coverageForAbsent[0].relationIds") and e["violations"][1].startswith("$.providers"),
      "traversal order")
# masking: type failure masking later domain+order violations
neg("type error masks domain and order violations",
    lambda m: (m.__setitem__("schemaVersion", True), m["providers"][1].__setitem__("platformIds", ["windows-x86_64-msvc", "all-supported"])),
    "ADM-TYPE", True)
neg("closed failure masks domain violation",
    lambda m: (m["providers"][0].__setitem__("extra", 1), m["coverageForAbsent"][0].__setitem__("deficiency", "nope")),
    "ADM-CLOSED", True)
# OPEN position non-NFC: gates pass, CVE1 encoder refuses
m = copy.deepcopy(BASE)
m["providers"][0]["providerVersionSource"] = "release-manifest:résumé"
r = ADM.admit(m)
vectors["negatives"].append({"class": "invalid", "name": "non-NFC text in a declared OPEN position", "firstRefusal": r["firstRefusal"],
                             "violations": r["violations"], "masksLater": False,
                             "note": "OPEN positions are bound by ADM-TYPE only; CVE1 NFC constraint refuses at encoding (not normalised)."})
check(r["firstRefusal"] == "CVE1-ENCODE", "nfc open")
# inherited 12-member domain could not express unresolved-edge (explanatory)
reg = ADM.reg["registries"]["RELATION-DOMAIN-V2"]
vectors["explanatory"].append({"class": "explanatory", "name": "unresolved-edge only admissible under the successor domain",
                               "inheritedMembers": reg["inheritedMembers"], "addedMembers": reg["addedMembers"],
                               "baseManifestUsesUnresolvedEdge": "unresolved-edge" in BASE["providers"][0]["relations"],
                               "wouldFailInheritedDomain": "unresolved-edge" not in reg["inheritedMembers"]})
# ladder mirror drift check against the single ladder authority
rel_reg = K.parse_raw(open('/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v2/subject/docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json', 'rb').read())["x-opensip-relation-registry"]["relations"]
mirror = ADM.reg["registries"]["RELATION-LADDER-DOMAIN-V2"]["ladders"]
drift = {k: (rel_reg[k]["ladder"], mirror.get(k)) for k in rel_reg if rel_reg[k]["ladder"] != mirror.get(k)}
vectors["explanatory"].append({"class": "explanatory", "name": "RELATION-LADDER-DOMAIN-V2 mirror equals ladder authority exactly and in order", "drift": drift})
check(not drift and set(mirror) == set(rel_reg), "ladder mirror")

out = dict(vectors, gateOrder=ADM.gate_order, registry="docs/coop/design-corrections/native/capability-manifest-domains.v2.json",
           recipe="hex(SHA-256(UTF8('opensip.capability-manifest.v1') || 0x00 || CVE1(CapabilityManifestV1)))",
           assertionFailures=failures)
S.dump('vectors/capability-manifests.json', out)
print(json.dumps({"failures": failures, "positives": len(vectors["positives"]), "negatives": len(vectors["negatives"]),
                  "baseId": pos["capabilityManifestId"], "syntaxId": ps["capabilityManifestId"]}, indent=1))
sys.exit(1 if failures else 0)
