import sys
sys.path.insert(0, "/tmp/opensip-design-corrections/consumer-b.v8/output/work")
import osip

print(osip.C({"b": 1, "a": [1, 2], "z": "x/y"}))
print(osip.C({"s": ' "\\' + chr(1) + chr(0x7F) + chr(0x2028)}))
print(osip.H("subject-scope", {"schemaVersion": 2}))
print(osip.ident("plan", {"a": 1}))

negatives = [
    b'{"a":1,"a":2}',
    b'{"a":1.0}',
    b'{"a":1e0}',
    b'{"a":-0}',
    b'{"a":NaN}',
    b'{"a":"\\ud800"}',
    b'{"a":18446744073709551616}',
    b'{"a":01}',
    b'\xff\xfe',
]
for raw in negatives:
    try:
        osip.admit_raw(raw)
        print("ADMIT  ", raw)
    except osip.AdmissionError as e:
        print("REFUSE ", raw, "->", e.code, e.detail)

deep33 = b"[" * 33 + b"1" + b"]" * 33
try:
    osip.admit_raw(deep33)
    print("depth33 ADMIT")
except osip.AdmissionError as e:
    print("depth33 REFUSE", e.code, e.detail)
deep32 = b"[" * 32 + b"1" + b"]" * 32
print("depth32 ADMIT depth=", osip.admit_raw(deep32)[1])

print("cve1 1      ", osip.cve1(1).hex())
print("cve1 -1     ", osip.cve1(-1).hex())
print("cve1 'a'    ", osip.cve1("a").hex())
print("cve1 ['a']  ", osip.cve1(["a"]).hex())
print("cve1 {a:T}  ", osip.cve1({"a": True}).hex())
print("cve1 null/F ", osip.cve1(None).hex(), osip.cve1(False).hex())

# frame round trip
fr = osip.frame("run", {"schemaVersion": 2})
print("frame parse", osip.parse_frame(fr))
try:
    osip.parse_frame(osip.C({"schemaVersion": 2}))
except osip.AdmissionError as e:
    print("payload-as-frame REFUSE", e.code)

# body identity worked example from identity-and-evidence section 3
span = b"a=1\n"
print("l0 payload", osip.l0_payload(span).hex())
