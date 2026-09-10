import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import json
import osref as O

print("keys:", O.C({"b": 1, "a": 2}))
nfc = "é"
nfd = "é"
print("nfc:", O.C({nfc: nfc}), "nfd:", O.C({nfd: nfd}), "distinct:", O.C({nfc: 1}) != O.C({nfd: 1}))
print("slash/ctl:", O.C(["a/b", "x\ty", "", " ", "qr"]))
print("nonbmp keys:", O.C({"\U0001f600": 1, "￿": 2}))
print("H:", O.H("snapshot", {"schemaVersion": 2}))
for bad in ['{"a":1,"a":2}', '{"a":1.0}', '{"a":1e0}', '{"a":-0}', '{"a":NaN}', '{"a":Infinity}']:
    try:
        O.parse(bad)
        print("ADMITTED(!)", bad)
    except O.Refuse as e:
        print("refuse", bad, "->", e.code)
print("u64max:", O.parse('{"a":18446744073709551615}'))
for bad in ['{"a":18446744073709551616}', '{"a":-9223372036854775809}']:
    try:
        O.parse(bad)
        print("ADMITTED(!)", bad)
    except O.Refuse as e:
        print("refuse", bad, "->", e.code)
print("depth31 ok:", O.check_depth(json.loads("[" * 31 + "]" * 31)))
print("depth32 ok:", O.check_depth(json.loads("[" * 32 + "]" * 32)))
try:
    O.check_depth(json.loads("[" * 33 + "]" * 33))
except O.Refuse as e:
    print("refuse depth33 ->", e.code, e.detail)
print("scalar-at-root depth:", O.check_depth("x"))
try:
    O.parse('"\\ud800"')
except O.Refuse as e:
    print("lone surrogate ->", e.code)
print("order canonical-set:", O.check_order("canonical-set", ["a", "b"]))
try:
    O.check_order("canonical-set", ["b", "a"])
except O.Refuse as e:
    print("unsorted set ->", e.code)
try:
    O.check_order("canonical-set", ["a", "a"])
except O.Refuse as e:
    print("dup set ->", e.code)
print("canonical-order repeats:", O.check_order("canonical-order", ["a", "a", "b"]))
try:
    O.check_order("frobnicate", ["a"])
except O.Refuse as e:
    print("unknown annotation ->", e.code)
print("cve1 examples:")
print(" null", O.cve1(None).hex(), " true", O.cve1(True).hex(), " 1", O.cve1(1).hex())
print(" -1", O.cve1(-1).hex())
print(' "a"', O.cve1("a").hex())
print(" []", O.cve1([]).hex(), " {}", O.cve1({}).hex())
