import sys, json
sys.path.insert(0, "/tmp/opensip-design-corrections/consumer-b.v5/output/ref")
import opensip_ref as R

print("C tests")
print(R.C({"b": 1, "a": 2}))
print(R.C({"é": "x", "e": "y"}))
print(R.C([1, -1, 0, 18446744073709551615]))
print(R.C({"s": 'a"b\\c/d\t '}))
print("H:", R.H("subject-scope", {"schemaVersion": 2}))
print("frame:", R.frame("subject-scope", {"schemaVersion": 2}))

for bad in [
    b'{"a":1,"a":2}',
    b'{"a":1.0}',
    b'{"a":1e0}',
    b'{"a":-0}',
    b'{"a":NaN}',
    b'{"a":18446744073709551616}',
    b'{"a":"\xed\xa0\x80"}',
]:
    try:
        R.parse(bad)
        print("ADMITTED(!)", bad)
    except R.Refuse as e:
        print("refused", bad, "->", e.code)

# depth: root container counts as 1
deep = "x"
v = "leaf"
for _ in range(31):
    v = [v]
R.check_bounds(v)
print("depth 32 ok")
v2 = [v]
try:
    R.check_bounds(v2)
    print("depth 33 ADMITTED(!)")
except R.Refuse as e:
    print("depth 33 refused", e.code)

# CVE1 cross-check against the illustration embedded in delivery.v4 (NOT used as oracle
# for any designed vector; only to test that my reading of the CVE1 prose is faithful).
d = R.doc_json("docs/coop/artifacts/delivery.v4.json")
op = d["derivedFrom"]["operations"][17]["value"]
vec = op["vectors"]["byId"]["DCM-1-core"]
print("embedded DCM-1 committedBytesSha256:", vec["committedBytesSha256"])
print("embedded DCM-1 capabilityManifestId :", vec["capabilityManifestId"])
hexbytes = bytes.fromhex(vec["committedBytesHex"])
print("recompute id from embedded bytes    :",
      R.hashlib.sha256(R.CAP_MANIFEST_DOMAIN + b"\x00" + hexbytes).hexdigest())
print("byte length match:", len(hexbytes) == vec["committedByteLength"])
