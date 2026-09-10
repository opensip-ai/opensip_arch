#!/usr/bin/env python
"""P8 - S-5(a): is CVE1 now CONSTRUCTIBLE, not merely verifiable?

The blind consumer could VERIFY capabilityManifestId from committed bytes but
could not PRODUCE those bytes, because CVE1's eight closed types were not stated
in the kit. v6 keeps CVE1 in resolved-inputs.v2.json and declares it a normative
dependency. Test: implement a CVE1 DECODER and ENCODER from that document alone,
round-trip every published committedBytesHex, and re-derive all seven ids.
"""
import json, hashlib
from pathlib import Path

S = Path("/tmp/opensip-design-corrections/candidate-subject.v6/docs")
RI = json.loads((S / "coop/artifacts/resolved-inputs.v2.json").read_text())
CVE = RI["planIdContract"]["canonicalValueEncoding"]
DEL = json.loads((S / "coop/artifacts/delivery.v4.json").read_text())
OP = next(v for v in DEL["derivedFrom"]["operations"]
          if v["path"] == "capabilityManifestIdentity")
VEC = OP["value"]["vectors"]["byId"]


# ---- decoder written from the eight encodings alone --------------------------
def decode(b, i=0):
    t = b[i]; i += 1
    if t == 0x00: return None, i
    if t == 0x01: return False, i
    if t == 0x02: return True, i
    if t == 0x03:
        return int.from_bytes(b[i:i + 8], "big"), i + 8
    if t == 0x07:
        return int.from_bytes(b[i:i + 8], "big", signed=True), i + 8
    if t == 0x04:
        n = int.from_bytes(b[i:i + 4], "big"); i += 4
        return b[i:i + n].decode("utf-8"), i + n
    if t == 0x05:
        n = int.from_bytes(b[i:i + 4], "big"); i += 4
        out = []
        for _ in range(n):
            v, i = decode(b, i); out.append(v)
        return out, i
    if t == 0x06:
        n = int.from_bytes(b[i:i + 4], "big"); i += 4
        out = {}
        for _ in range(n):
            k, i = decode(b, i)
            v, i = decode(b, i)
            out[k] = v
        return out, i
    raise ValueError("unknown CVE1 tag 0x%02x at %d" % (t, i - 1))


def encode(v):
    if v is None: return b"\x00"
    if v is True: return b"\x02"
    if v is False: return b"\x01"
    if isinstance(v, int):
        if v < 0:
            return b"\x07" + v.to_bytes(8, "big", signed=True)
        return b"\x03" + v.to_bytes(8, "big")
    if isinstance(v, str):
        e = v.encode("utf-8")
        return b"\x04" + len(e).to_bytes(4, "big") + e
    if isinstance(v, list):
        return b"\x05" + len(v).to_bytes(4, "big") + b"".join(encode(x) for x in v)
    if isinstance(v, dict):
        items = sorted(v.items(), key=lambda kv: kv[0].encode("utf-8"))
        return (b"\x06" + len(items).to_bytes(4, "big")
                + b"".join(encode(k) + encode(x) for k, x in items))
    raise TypeError(type(v))


out = {"probe": "P8-S5-CVE1-constructibility",
       "closedTypes": CVE["closedTypes"],
       "typeCount": len(CVE["closedTypes"]),
       "allEightTagsPresent": len(CVE["encodings"]) == 8,
       "constraints": CVE["constraints"]}

results = {}
for vid, row in VEC.items():
    cb = bytes.fromhex(row["committedBytesHex"])
    r = {}
    try:
        val, end = decode(cb)
        r["decoded"] = end == len(cb)
        re_enc = encode(val)
        r["roundTripByteIdentical"] = re_enc == cb
        r["idReproduced"] = hashlib.sha256(
            b"opensip.capability-manifest.v1\x00" + cb).hexdigest() == row["capabilityManifestId"]
        r["sha256Reproduced"] = hashlib.sha256(cb).hexdigest() == row.get("committedBytesSha256")
        # constructibility: re-derive the id from the DECODED VALUE via my encoder
        r["idFromReEncodedValue"] = hashlib.sha256(
            b"opensip.capability-manifest.v1\x00" + re_enc).hexdigest() == row["capabilityManifestId"]
    except Exception as e:
        r["error"] = type(e).__name__ + ":" + str(e)[:120]
    results[vid] = r

out["vectors"] = results
out["allDecoded"] = all(v.get("decoded") for v in results.values())
out["allRoundTripByteIdentical"] = all(v.get("roundTripByteIdentical") for v in results.values())
out["allIdsReproduced"] = all(v.get("idReproduced") for v in results.values())
out["allConstructibleFromValue"] = all(v.get("idFromReEncodedValue") for v in results.values())
out["vectorCount"] = len(results)
print(json.dumps(out, indent=1))
