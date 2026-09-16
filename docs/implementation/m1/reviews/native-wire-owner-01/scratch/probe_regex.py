import json, re, sys
IDL = json.load(open("/tmp/opensip-implementation/m1-native-wire-owner-subject-01/wire-carriers.v1.json"))
EV = json.load(open("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/native/native-evidence.schemas.v2.json"))
S = IDL["scalars"]
P = S["Rust3CanonicalPath"]["type"]["pattern"]
N = EV["$defs"]["CanonicalPath"]["pattern"]
NUL, NL, BS = chr(0), chr(10), chr(92)
cases = ["a/b", "a/../b", "a" + NL + "/../b", "a" + NL + "//b", "x" + NL + "/..", "a/.", "a" + NL + "/.",
         "./a", "a//b", "a/", "C:x", "a" + NL + "/b/", "a" + NL + "b"]


def rust2_rule(s):
    segs = s.split("/")
    return (not s.startswith("/")) and BS not in s and NUL not in s and not re.match(r"[A-Za-z]:", s) \
        and all(g not in ("", ".", "..") for g in segs)


out = {"rust3CanonicalPath": {}, "native2CanonicalPath": {}}
for s in cases:
    out["rust3CanonicalPath"][repr(s)] = {"pattern": bool(re.search(P, s)), "rust2Rule": rust2_rule(s)}
    out["native2CanonicalPath"][repr(s)] = {"pattern": bool(re.search(N, s)), "rust2Rule": rust2_rule(s)}
PK = S["Rust3PackageKey"]["type"]
out["packageKey"] = {repr(s): {"pattern": bool(re.search(PK["pattern"], s)), "scalars": len(s), "minScalars": PK["minScalars"]}
                     for s in ["a 1 ", "ab 1 ", "a b c", "a b c d", "n 1.0 path+file:///my proj"]}
# DependencyPackageSourceV1 bounds vs entries.packageKey maxLength
pkg = EV["$defs"]["DependencyPackageSourceV1"]["properties"]
out["packageKeyMaxFromPackageRow"] = pkg["name"]["maxLength"] + pkg["version"]["maxLength"] + pkg["sourceId"]["maxLength"] + 2
out["entriesPackageKeyMaxLength"] = EV["$defs"]["DependencySourceManifestV3"]["properties"]["entries"]["items"]["properties"]["packageKey"]["maxLength"]
out["sourceIdMinLength"] = pkg["sourceId"].get("minLength")
# key order vs tuple order counterexample with a byte below 0x20 in name
a, b = ("a", "1", "x"), ("a" + chr(1), "1", "x")
tuple_order = sorted([a, b], key=lambda t: tuple(x.encode() for x in t))
key_order = sorted([a, b], key=lambda t: " ".join(t).encode())
out["keyVsTupleOrderWithControlByte"] = {"tuple": [repr(x) for x in tuple_order], "key": [repr(x) for x in key_order],
                                         "equal": tuple_order == key_order, "schemaForbidsControlInName": "pattern" in pkg["name"]}
look = re.compile(r"\(\?<?[=!]")
out["scalarsWithLookaround"] = sorted(k for k, v in S.items() if "pattern" in v["type"] and look.search(v["type"]["pattern"]))
out["scalarsWithLookbehind"] = sorted(k for k, v in S.items() if "pattern" in v["type"] and "(?<" in v["type"]["pattern"])
out["patternDialectDeclared"] = any("dialect" in json.dumps(IDL[k]).lower() or "ecma" in json.dumps(IDL[k]).lower() for k in ("privateRepresentation", "profiles"))
json.dump(out, sys.stdout, indent=1)
