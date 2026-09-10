#!/usr/bin/env python
"""ADV-1/2/3 structural checks, the retired false rationale (BV6-V4-CR-1 /
BV6-V5-CR-1), and CB6-NEW-4 digest movement - over the frozen bytes.

Assesses the ACTUAL chosen wording, not the prior reviewer's inferred reading.
"""
import hashlib
import json
import os
import re
import sys

ROOT = "/tmp/opensip-design-corrections/candidate-subject.v17"
DC = os.path.join(ROOT, "docs/coop/design-corrections")
CT = os.path.join(ROOT, "docs/v2/contracts/product-v1")
OUT = sys.argv[1]


def J(p):
    with open(p) as fh:
        return json.load(fh)


def T(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


rep = {}
native = J(os.path.join(DC, "native/native-evidence.schemas.v2.json"))

# ---------------- ADV-2: the two confidence clauses ----------------
td = native["$defs"].get("TypeDerivationV1", {})
props = td.get("properties", {})
rep["adv2"] = {
    "typeDerivationConfidenceIsConst":
        props.get("confidenceMillionths", {}).get("const") == 1000000,
    "typeDerivationMethodIsConst":
        props.get("confidenceMethod", {}).get("const") == "native.confidence.v1",
    "typeDerivationConfidenceSchema": props.get("confidenceMillionths"),
    "typeDerivationMethodSchema": props.get("confidenceMethod"),
}
ve = native["$defs"].get("ViewEntryV3", {})
vp = ve.get("properties", {})
rep["adv2"].update({
    "viewEntryConfidenceSchema": vp.get("confidenceMillionths"),
    "viewEntryHasNoConfidenceMethod": "confidenceMethod" not in vp,
    "viewEntryDomainIsFullRange":
        vp.get("confidenceMillionths", {}).get("minimum") == 0
        and vp.get("confidenceMillionths", {}).get("maximum") == 1000000,
})
# the named defensive regression case must exist and be an evaluator input
cases = J(os.path.join(DC, "native/native-cases.v2.json"))
blob = json.dumps(cases)
name = "sufficiency-v2-confidence-floor-precedes-one-rung-existential-shortcut"
rep["adv2"]["namedRegressionCasePresent"] = name in blob
found = []
def walk(o):
    if isinstance(o, dict):
        if o.get("id") == name or o.get("name") == name:
            found.append(o)
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)
walk(cases)
rep["adv2"]["regressionCaseRecord"] = json.dumps(found)[:1500] if found else None
rep["adv2"]["regressionCaseUses100000AgainstFloor900000"] = (
    "100000" in json.dumps(found) and "900000" in json.dumps(found))
# it must NOT be a ViewEntryV3 / provider emission
rep["adv2"]["regressionCaseIsNotAViewEntryV3"] = (
    "ViewEntryV3" not in json.dumps(found))

# ---------------- ADV-3: the D9 extension ----------------
d9c_path = os.path.join(ROOT, "docs/coop/artifacts/d9-exit-contract.v1.14.json")
d9_bytes = open(d9c_path, "rb").read()
d9 = json.loads(d9_bytes)
inherited_map = d9["codeMaps"]["faultCauseToErrorCode"]
rep["adv3"] = {
    "inheritedContractSha256": hashlib.sha256(d9_bytes).hexdigest(),
    "inheritedContractUnchanged":
        hashlib.sha256(d9_bytes).hexdigest()
        == "8dd3303855f49bfdbb2751ee65f54a906405f0654159ebe815472f73cdf7da31",
    "inheritedFaultCauseCount": len(inherited_map),
    "inheritedHasHostInvariant": "host-invariant" in inherited_map,
    "inheritedErrorCodes": sorted(set(inherited_map.values())),
    "illegalStateAlreadyInInheritedVocabulary":
        "SYSTEM.OUTCOME.ILLEGAL_STATE" in set(inherited_map.values()),
}
# find the successor extension in the native schema bundle / contract
nb = json.dumps(native)
rep["adv3"]["successorMentionsHostInvariant"] = "host-invariant" in nb
md = T(os.path.join(CT, "native-evidence.md"))
rep["adv3"]["contractDisclosesTheExtension"] = (
    "host-invariant" in md and "d9-exit-contract" in md)
m = re.search(r"[^\n]*host-invariant[^\n]*", md)
rep["adv3"]["contractSentence"] = m.group(0)[:600] if m else None
rep["adv3"]["contractCallsItFutureOrCrossUnitObligation"] = bool(
    re.search(r"host-invariant", md)) and bool(
    re.search(r"(future|obligation|successor|not yet|owed)", md, re.I))

# ---------------- retired false rationale ----------------
# BV6-V4-CR-1 / BV6-V5-CR-1: the claim that JSON Schema CANNOT decide the plane
# "because relation is a CanonicalIdentifier / not an enum" is FALSE and must be
# gone from EVERY non-review document, replaced by the "deliberately leaves"
# formulation.
BAD_PATTERNS = [
    r"cannot decide",
    r"canonical identifier rather than an enum",
    r"CanonicalIdentifier, not an enum",
    r"is not an enum",
    r"rather than an enum",
]
GOOD_PATTERN = r"deliberately leaves"

scanned, hits = 0, []
for base in (DC, CT):
    for dp, dn, fns in os.walk(base):
        if "/reviews" in dp:
            dn[:] = [d for d in dn if d != "reviews"]
        if "/reviews/" in dp or dp.endswith("/reviews"):
            continue
        for fn in fns:
            if not fn.endswith((".json", ".md", ".py")):
                continue
            p = os.path.join(dp, fn)
            try:
                txt = T(p)
            except Exception:
                continue
            scanned += 1
            for pat in BAD_PATTERNS:
                for mm in re.finditer(pat, txt, re.I):
                    s = max(0, mm.start() - 220)
                    ctx = txt[s:mm.end() + 220].replace("\n", " ")
                    hits.append({"file": os.path.relpath(p, ROOT),
                                 "pattern": pat, "context": ctx})
rep["retiredRationale"] = {
    "filesScanned": scanned,
    "rawHitCount": len(hits),
    "hits": hits[:60],
    "note": "Raw hits are triaged by hand below; a phrase match is not by "
            "itself the retired claim.",
}
# The specific retired causal claim: 'cannot decide' JOINED to the relation type.
joined = [h for h in hits
          if re.search(r"cannot decide", h["context"], re.I)
          and re.search(r"(not an enum|rather than an enum|canonical ?identifier)",
                        h["context"], re.I)]
rep["retiredRationale"]["retiredCausalClaimOccurrences"] = joined
rep["retiredRationale"]["retiredCausalClaimIsGone"] = not joined

# the replacement formulation must be present in all three named carriers
for rel in ("workflows/schemas/repair.schema.json",
            "native/native-evidence.schemas.v2.json",
            "workflows/check_workflows.v1.py"):
    rep["retiredRationale"]["replacementPresentIn:" + rel] = bool(
        re.search(GOOD_PATTERN, T(os.path.join(DC, rel)), re.I))
rep["retiredRationale"]["replacementPresentIn:workflows-and-surfaces.md"] = bool(
    re.search(GOOD_PATTERN, T(os.path.join(CT, "workflows-and-surfaces.md")), re.I))

# the neighbouring check id the handoff says is DELIBERATELY retained
cw = T(os.path.join(DC, "workflows/check_workflows.v1.py"))
rep["retiredRationale"]["neighbouringCheckIdRetained"] = (
    "repair.the-schema-alone-cannot-decide-the-plane" in cw)

# ---------------- CB6-NEW-4: schema-document digest movement ----------------
# A registered schema document's digest IS committed, so editing it moves
# retained-Run identities over fixtures. Verify the digest is the raw SHA-256 of
# the document and that it MOVED between v16 and v17.
v16 = "/tmp/opensip-design-corrections/post-reset-review.v17/copies/v16-extract"
mv = {}
for rel in ("native/native-evidence.schemas.v2.json",
            "foundation/relation-payload-schemas.v2.json"):
    a = os.path.join(v16, "docs/coop/design-corrections", rel)
    b = os.path.join(DC, rel)
    if os.path.isfile(a):
        mv[rel] = {
            "v16RawSha256": hashlib.sha256(open(a, "rb").read()).hexdigest(),
            "v17RawSha256": hashlib.sha256(open(b, "rb").read()).hexdigest(),
        }
        mv[rel]["digestMoved"] = mv[rel]["v16RawSha256"] != mv[rel]["v17RawSha256"]
rep["cb6New4DigestMovement"] = mv
rep["cb6New4AllRegisteredSchemaDigestsMoved"] = all(
    v["digestMoved"] for v in mv.values())

with open(OUT, "w") as fh:
    json.dump(rep, fh, indent=1, sort_keys=True, default=str)

print("=== ADV-2 ===")
for k, v in rep["adv2"].items():
    print("  %-46s %s" % (k, json.dumps(v)[:160]))
print("=== ADV-3 ===")
for k, v in rep["adv3"].items():
    print("  %-46s %s" % (k, json.dumps(v)[:200]))
print("=== retired rationale ===")
for k, v in rep["retiredRationale"].items():
    if k == "hits":
        continue
    print("  %-46s %s" % (k, json.dumps(v)[:400]))
print("=== CB6-NEW-4 ===")
print(json.dumps(rep["cb6New4DigestMovement"], indent=1))
