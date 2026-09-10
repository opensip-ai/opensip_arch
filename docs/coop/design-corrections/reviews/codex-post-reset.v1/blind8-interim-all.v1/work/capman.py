"""Capability-manifest admission, independently reconstructed.

Sources (all in the kit):
  identity-and-evidence.md section 3 (the committed-CVE1 paragraph; selects the
      registry BY NAME and restates the four inherited gates in their order)
  native/capability-manifest-domains.v2.json  (the selected ADM-DOMAIN registry,
      record shapes, gateOrder, traversalOrder, declaredOPEN, decoderBounds)
  docs/coop/artifacts/resolved-inputs.v2.json#planIdContract.canonicalValueEncoding (CVE1)
  docs/coop/artifacts/delivery.v4.json .../orderingRuling.perFieldRuling
      (the inherited DL-ORD declared sort keys, reproduced verbatim by selection)
"""
from __future__ import annotations

import json
import struct
import unicodedata

import osip

REG = json.loads(osip.doc_bytes(
    "docs/coop/design-corrections/native/capability-manifest-domains.v2.json").decode())
REGISTRIES = REG["registries"]
SHAPES = REG["recordShape"]
DECODER = REG["decoderBounds"]

# delivery.v4 orderingRuling.perFieldRuling, selected unchanged by the successor
SORT_KEYS = {
    "providers": "providerId",
    "coverageForAbsent": "providerId",
    "platformIds": None,      # the element string itself
    "relationIds": None,
}


class Cve1DecodeError(Exception):
    pass


def cve1_decode(b: bytes):
    """Bounded, total-refusing CVE1 decode.  Trailing bytes, unknown tags,
    non-NFC text, duplicate keys and unsorted map keys all refuse."""
    val, i = _dec(b, 0, 0)
    if i != len(b):
        raise Cve1DecodeError("trailing bytes")
    return val


def _dec(b, i, depth):
    if depth > DECODER["maxNesting"]:
        raise Cve1DecodeError("nesting over %d" % DECODER["maxNesting"])
    if i >= len(b):
        raise Cve1DecodeError("truncated")
    tag = b[i]
    i += 1
    if tag == 0x00:
        return None, i
    if tag == 0x01:
        return False, i
    if tag == 0x02:
        return True, i
    if tag == 0x03:
        return struct.unpack(">Q", b[i:i + 8])[0], i + 8
    if tag == 0x07:
        return struct.unpack(">q", b[i:i + 8])[0], i + 8
    if tag == 0x04:
        (n,) = struct.unpack(">I", b[i:i + 4])
        i += 4
        s = b[i:i + n].decode("utf-8")
        if unicodedata.normalize("NFC", s) != s:
            raise Cve1DecodeError("non-NFC text")
        return s, i + n
    if tag == 0x05:
        (n,) = struct.unpack(">I", b[i:i + 4])
        if n > DECODER["maxCollectionItems"]:
            raise Cve1DecodeError("collection over bound")
        i += 4
        out = []
        for _ in range(n):
            v, i = _dec(b, i, depth + 1)
            out.append(v)
        return out, i
    if tag == 0x06:
        (n,) = struct.unpack(">I", b[i:i + 4])
        if n > DECODER["maxCollectionItems"]:
            raise Cve1DecodeError("collection over bound")
        i += 4
        out, prev = {}, None
        for _ in range(n):
            k, i = _dec(b, i, depth + 1)
            if not isinstance(k, str):
                raise Cve1DecodeError("map key is not a string")
            if k in out:
                raise Cve1DecodeError("duplicate map key")
            kb = k.encode("utf-8")
            if prev is not None and not prev < kb:
                raise Cve1DecodeError("unsorted map keys")
            prev = kb
            v, i = _dec(b, i, depth + 1)
            out[k] = v
        return out, i
    raise Cve1DecodeError("unknown tag 0x%02x" % tag)


# --------------------------------------------------------------------------

def _domain(name):
    r = REGISTRIES[name]
    return set(r["members"]) if "members" in r else None


def admit_value(m):
    """The four inherited gates in their inherited order:
    ADM-TYPE, ADM-CLOSED, ADM-DOMAIN, ADM-ORDER.  Returns a COMPLETE ordered
    fault list; the first entry is the first observed refusal.  Within
    ADM-ORDER the declared traversal is used, so 'the first violation' is
    reproducible."""
    faults = []

    # ---- ADM-TYPE : exact JSON type BEFORE any content comparison
    def typ(v, want, where, present=True):
        if not present:
            return False        # ADM-TYPE types a PRESENT scalar; an absent key
                                # has no type and is ADM-CLOSED's to refuse.
        if want == "integer":
            ok = isinstance(v, int) and not isinstance(v, bool)
        elif want == "string":
            ok = isinstance(v, str)
        elif want == "array":
            ok = isinstance(v, list)
        elif want == "object":
            ok = isinstance(v, dict) and not isinstance(v, bool)
        else:
            ok = False
        if not ok:
            faults.append(("ADM-TYPE", "%s is not a JSON %s (%r)" % (where, want, v)))
        return ok

    if not typ(m, "object", "CapabilityManifestV1"):
        return faults
    typ(m.get("schemaVersion"), "integer", "CapabilityManifestV1.schemaVersion", "schemaVersion" in m)
    typ(m.get("profile"), "string", "CapabilityManifestV1.profile", "profile" in m)
    typ(m.get("providers"), "array", "CapabilityManifestV1.providers", "providers" in m)
    typ(m.get("coverageForAbsent"), "array", "CapabilityManifestV1.coverageForAbsent", "coverageForAbsent" in m)
    for i, p in enumerate(m.get("providers") or []):
        if typ(p, "object", "providers[%d]" % i):
            for f in ("providerId", "language", "providerVersionSource",
                      "toolchainIdentitySource"):
                typ(p.get(f), "string", "providers[%d].%s" % (i, f), f in p)
            typ(p.get("relations"), "object", "providers[%d].relations" % i, "relations" in p)
            typ(p.get("platformIds"), "array", "providers[%d].platformIds" % i, "platformIds" in p)
            for k, v in (p.get("relations") or {}).items():
                typ(v, "string", "providers[%d].relations[%s]" % (i, k))
            for j, v in enumerate(p.get("platformIds") or []):
                typ(v, "string", "providers[%d].platformIds[%d]" % (i, j))
    for i, a in enumerate(m.get("coverageForAbsent") or []):
        if typ(a, "object", "coverageForAbsent[%d]" % i):
            for f in ("providerId", "language", "coverageState", "deficiency"):
                typ(a.get(f), "string", "coverageForAbsent[%d].%s" % (i, f), f in a)
            typ(a.get("relationIds"), "array", "coverageForAbsent[%d].relationIds" % i, "relationIds" in a)
            for j, v in enumerate(a.get("relationIds") or []):
                typ(v, "string", "coverageForAbsent[%d].relationIds[%d]" % (i, j))
    if faults:
        return faults

    # ---- ADM-CLOSED : every reachable RECORD carries exactly its key set
    def closed(obj, shape, where):
        want = set(SHAPES[shape]["requiredKeys"])
        got = set(obj.keys())
        if got != want:
            faults.append(("ADM-CLOSED", "%s keys %s != %s"
                           % (where, sorted(got), sorted(want))))

    closed(m, "CapabilityManifestV1", "CapabilityManifestV1")
    for i, p in enumerate(m["providers"]):
        closed(p, "ProviderCapability", "providers[%d]" % i)
    for i, a in enumerate(m["coverageForAbsent"]):
        closed(a, "AbsentCapability", "coverageForAbsent[%d]" % i)
    if faults:
        return faults

    # ---- ADM-DOMAIN : every scalar bound to a named registry or declared OPEN
    rel_dom = _domain("RELATION-DOMAIN-V2")
    ladders = REGISTRIES["RELATION-LADDER-DOMAIN-V2"]["ladders"]
    plat = _domain("PLATFORM-ID-DOMAIN-V1")
    defi = _domain("DEFICIENCY-DOMAIN-V1")
    cst = _domain("COVERAGE-STATE-DOMAIN-V1")
    for i, p in enumerate(m["providers"]):
        for k, v in p["relations"].items():
            if k not in rel_dom:
                faults.append(("ADM-DOMAIN",
                               "providers[%d].relations key %r not in RELATION-DOMAIN-V2"
                               % (i, k)))
            elif v not in ladders[k]:
                faults.append(("ADM-DOMAIN",
                               "providers[%d].relations[%s]=%r is not a rung of that "
                               "relation's ladder %r" % (i, k, v, ladders[k])))
        for v in p["platformIds"]:
            if v not in plat:
                faults.append(("ADM-DOMAIN",
                               "providers[%d].platformIds %r not in PLATFORM-ID-DOMAIN-V1"
                               % (i, v)))
    for i, a in enumerate(m["coverageForAbsent"]):
        for v in a["relationIds"]:
            if v not in rel_dom:
                faults.append(("ADM-DOMAIN",
                               "coverageForAbsent[%d].relationIds %r not in "
                               "RELATION-DOMAIN-V2" % (i, v)))
        if a["coverageState"] not in cst:
            faults.append(("ADM-DOMAIN", "coverageForAbsent[%d].coverageState %r"
                           % (i, a["coverageState"])))
        if a["deficiency"] not in defi:
            faults.append(("ADM-DOMAIN", "coverageForAbsent[%d].deficiency %r"
                           % (i, a["deficiency"])))
    if faults:
        return faults

    # ---- ADM-ORDER : declared traversal, complete violation list
    def ascending(items, key, where):
        prev = None
        for it in items:
            v = it if key is None else it[key]
            kb = unicodedata.normalize("NFC", v).encode("utf-8")
            if prev is not None and not prev < kb:
                faults.append(("ADM-ORDER",
                               "%s not strictly ascending / duplicate at %r" % (where, v)))
                return
            prev = kb

    for i, p in enumerate(m["providers"]):
        ascending(p["platformIds"], None, "providers[%d].platformIds" % i)
    for i, a in enumerate(m["coverageForAbsent"]):
        ascending(a["relationIds"], None, "coverageForAbsent[%d].relationIds" % i)
    ascending(m["providers"], SORT_KEYS["providers"], "providers")
    ascending(m["coverageForAbsent"], SORT_KEYS["coverageForAbsent"], "coverageForAbsent")
    return faults


def admit_committed(committed: bytes):
    """Admit the committed CVE1 artifact bytes: decode, run the four gates, and
    check that re-encoding the admitted value reproduces the committed bytes."""
    try:
        val = cve1_decode(committed)
    except (Cve1DecodeError, struct.error, UnicodeDecodeError) as e:
        return [("CVE1_DECODE", str(e))]
    faults = admit_value(val)
    if faults:
        return faults
    if osip.cve1(val) != committed:
        return [("CVE1_ROUNDTRIP", "committed bytes are not CVE1 of their own parse")]
    return []


def commit(manifest) -> bytes:
    """A release builder's step 2: committedBytes = CVE1(admitted manifest)."""
    faults = admit_value(manifest)
    if faults:
        raise ValueError("manifest not admissible: %r" % (faults[0],))
    return osip.cve1(manifest)
