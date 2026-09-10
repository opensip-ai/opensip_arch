import sys, hashlib, struct, unicodedata
sys.path.insert(0, '/tmp/opensip-design-corrections/consumer-b.v6/output/ref')
from osip import *

out = {}

# V-C1 hand-spelled canonical bytes
x = {"b": 1, "a": "xé", "é": [1, -1, 0], "z": {"k": True}}
c = C(x)
expect = b'{"a":"x\xc3\xa9","b":1,"z":{"k":true},"\xc3\xa9":[1,-1,0]}'
out["C1_bytes"] = c.decode()
out["C1_matches_hand_spelled"] = (c == expect)

# V-C2 control escaping / non-escaped chars
c2 = C({"s": " /\\\"\b\t\n\f\r\x01 "})
out["C2_bytes"] = c2.decode("utf-8")

# V-H1 frame
d = "subject-scope"
fr = frame(d, {"a": 1})
hand = (b"opensip.product.v1\x00" + d.encode() + b"\x00"
        + struct.pack(">Q", len(C({"a": 1}))) + C({"a": 1}))
out["H1_frame_hand_equal"] = (fr == hand)
out["H1_H"] = H(d, {"a": 1})
out["H1_H_differs_from_raw_sha_of_C"] = H(d, {"a": 1}) != hashlib.sha256(C({"a": 1})).hexdigest()
out["H1_frame_hex"] = fr.hex()

# V-CVE1 hand check
v = {"schemaVersion": 1, "profile": "p"}
b = cve1(v)
hand = (b"\x06" + struct.pack(">I", 2)
        + b"\x04" + struct.pack(">I", 7) + b"profile" + b"\x04" + struct.pack(">I", 1) + b"p"
        + b"\x04" + struct.pack(">I", 13) + b"schemaVersion" + b"\x03" + struct.pack(">Q", 1))
out["CVE1_hand_equal"] = (b == hand)
out["CVE1_hex"] = b.hex()
out["CVE1_capability_manifest_id"] = capability_manifest_id(b)

# negatives
neg = {}
for name, fn in [
    ("C_float", lambda: C(1.0)),
    ("C_dup_after_parse", lambda: C({"a": 1.5})),
    ("CVE1_float", lambda: cve1(1.0)),
    ("CVE1_int_underflow", lambda: cve1(-(2 ** 63) - 1)),
    ("CVE1_int_overflow", lambda: cve1(2 ** 64)),
    ("CVE1_non_nfc", lambda: cve1("Å")),   # decomposed A-ring
]:
    try:
        fn()
        neg[name] = "NOT-REFUSED (defect)"
    except Refuse as e:
        neg[name] = str(e)
neg["CVE1_nfc_ok"] = cve1(unicodedata.normalize("NFC", "Å")).hex()
neg["CVE1_negative_int"] = cve1(-1).hex()
out["negatives"] = neg

print(__import__("json").dumps(out, indent=1, ensure_ascii=False))
